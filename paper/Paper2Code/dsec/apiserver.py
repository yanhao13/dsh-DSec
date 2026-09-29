"""API server: stateless cluster ingress (paper §3.2).

Training/evaluation code invokes libdsec from trusted GPU servers, while
sandboxes execute untrusted model-generated code and may access external
networks — the two sides are network-isolated with the apiserver as the only
permitted path. All sandbox requests pass through this ingress.

The apiserver maintains no per-sandbox state: each sandbox id encodes its
owning edge, so any apiserver instance can resolve and forward a request
directly to the target edge, letting the ingress tier scale horizontally.
"""
from __future__ import annotations

import asyncio
from typing import Dict, List, Optional, Tuple

from . import idgen
from .errors import AdmissionError, NotFound
from .iam import IAM, OP_CREATE, OP_LIST, OP_OPS, OP_STOP, Quota
from .placement import PlacementEngine
from .types import FileStat, HttpResult, RunResult, SandboxSpec
from .watcher import Watcher

PLACEMENT_RETRIES = 3


class ApiServer:
    """Ingress: IAM -> placement -> edge forwarding."""

    def __init__(self, iam: IAM, placement: PlacementEngine, edges: Dict[str, object],
                 watcher: Optional[Watcher] = None):
        self.iam = iam
        self.placement = placement
        self.edges = edges
        self.watcher = watcher
        # Only routing facts: sandbox_id -> (edge_id, project, held quota).
        self._registry: Dict[str, Tuple[str, str, Quota]] = {}
        self._tokens: Dict[str, Tuple[str, str, str]] = {}  # terminal token -> (sandbox, terminal_id, token)
        self._lock = asyncio.Lock()

    async def start(self) -> None:
        if self.watcher is not None:
            await self.watcher.start()

    async def stop(self) -> None:
        if self.watcher is not None:
            await self.watcher.stop()

    # -- creation --------------------------------------------------------------------
    async def create_sandbox(self, principal: str, spec: SandboxSpec) -> Tuple[str, str, str]:
        """Authorize, place, and create; returns (sandbox_id, terminal_id, token)."""
        project = self.iam.authorize(principal, OP_CREATE, spec.project)
        # Placement reads the watcher's fleet view; make sure a first snapshot
        # exists (the periodic loop may not have run yet).
        if self.watcher is not None and not self.watcher.fleet.edges:
            await self.watcher.collect_once()
        need = Quota(cpu=spec.limits.cpu_cores_limit,
                     memory_mb=spec.limits.memory_limit_mb,
                     max_sandboxes=1)
        self.iam.consume(project, need)
        held = need
        last_error: Optional[Exception] = None
        for _ in range(PLACEMENT_RETRIES):
            edge_id = self.placement.place(spec)
            edge = self.edges[edge_id]
            try:
                sandbox_id = await edge.create(spec)
            except AdmissionError as exc:
                # Edge retains final admission authority (§7): deprioritize it
                # and try an alternative node.
                last_error = exc
                self.placement.penalize(edge_id)
                continue
            self.placement.settle(edge_id)
            terminal_id, token = await edge.open_session(sandbox_id)
            self._registry[sandbox_id] = (edge_id, spec.project, held)
            self._tokens[sandbox_id] = (sandbox_id, terminal_id, token)
            return sandbox_id, terminal_id, token
        self.iam.release(project, held)
        raise last_error or AdmissionError("placement failed")

    # -- routing ------------------------------------------------------------------------
    def resolve_edge(self, sandbox_id: str):
        edge_id = idgen.owning_edge(sandbox_id)
        if edge_id not in self.edges:
            raise NotFound("no edge %s registered" % edge_id)
        return self.edges[edge_id]

    def _check_registered(self, sandbox_id: str) -> None:
        if sandbox_id not in self._registry:
            raise NotFound("unknown sandbox %s" % sandbox_id)

    # -- operation forwarding --------------------------------------------------------------
    async def run(self, sandbox_id: str, terminal_id: str, token: str, command: str, *,
                  timeout: float = 60.0, env=None, stdin: bytes = b"") -> RunResult:
        self._check_registered(sandbox_id)
        return await self.resolve_edge(sandbox_id).run(
            sandbox_id, terminal_id, token, command, timeout=timeout, env=env, stdin=stdin)

    async def read_file(self, sandbox_id: str, terminal_id: str, token: str,
                        path: str, max_bytes: int) -> bytes:
        self._check_registered(sandbox_id)
        return await self.resolve_edge(sandbox_id).read_file(
            sandbox_id, terminal_id, token, path, max_bytes)

    async def write_file(self, sandbox_id: str, terminal_id: str, token: str,
                         path: str, data: bytes, mode: int) -> None:
        self._check_registered(sandbox_id)
        return await self.resolve_edge(sandbox_id).write_file(
            sandbox_id, terminal_id, token, path, data, mode)

    async def list_dir(self, sandbox_id: str, terminal_id: str, token: str,
                       path: str) -> List[FileStat]:
        self._check_registered(sandbox_id)
        return await self.resolve_edge(sandbox_id).list_dir(sandbox_id, terminal_id, token, path)

    async def http(self, sandbox_id: str, terminal_id: str, token: str,
                   url: str, method: str = "GET", body: bytes = b"") -> HttpResult:
        self._check_registered(sandbox_id)
        return await self.resolve_edge(sandbox_id).http(
            sandbox_id, terminal_id, token, url, method, body)

    async def open_session(self, sandbox_id: str) -> Tuple[str, str]:
        self._check_registered(sandbox_id)
        return await self.resolve_edge(sandbox_id).open_session(sandbox_id)

    async def close_session(self, sandbox_id: str, terminal_id: str, token: str) -> None:
        self._check_registered(sandbox_id)
        await self.resolve_edge(sandbox_id).close_session(sandbox_id, terminal_id, token)

    # -- lifecycle ---------------------------------------------------------------------------
    async def pause(self, principal: str, sandbox_id: str) -> None:
        edge_id, project_path, _ = self._registry[sandbox_id]
        self.iam.authorize(principal, OP_OPS, project_path)
        await self.edges[edge_id].pause(sandbox_id)

    async def resume(self, principal: str, sandbox_id: str) -> None:
        edge_id, project_path, _ = self._registry[sandbox_id]
        self.iam.authorize(principal, OP_OPS, project_path)
        await self.edges[edge_id].resume(sandbox_id)

    async def stop_sandbox(self, principal: str, sandbox_id: str) -> None:
        entry = self._registry.pop(sandbox_id, None)
        if entry is None:
            raise NotFound("unknown sandbox %s" % sandbox_id)
        edge_id, project_path, held = entry
        self.iam.authorize(principal, OP_STOP, project_path)
        project = self.iam.projects[project_path]
        await self.edges[edge_id].destroy(sandbox_id)
        self.iam.release(project, held)
        self._tokens.pop(sandbox_id, None)

    async def list_sandboxes(self, principal: str, project_path: str) -> List[dict]:
        self.iam.authorize(principal, OP_LIST, project_path)
        out = []
        for sandbox_id, (edge_id, path, _) in self._registry.items():
            if path.startswith(project_path):
                edge = self.edges[edge_id]
                ctx = edge.sandboxes.get(sandbox_id)
                state = ctx.state if ctx is not None else "gone"
                out.append({"sandbox_id": sandbox_id, "edge_id": edge_id,
                            "project": path, "state": state})
        return out

    def state(self, sandbox_id: str) -> str:
        entry = self._registry.get(sandbox_id)
        if entry is None:
            return "gone"
        edge_id, _, _ = entry
        ctx = self.edges[edge_id].sandboxes.get(sandbox_id)
        return ctx.state if ctx is not None else "gone"
