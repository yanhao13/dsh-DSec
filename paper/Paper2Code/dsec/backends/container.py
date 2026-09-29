"""Container backend with dynamic lower-layer insertion (paper §2.2, §5.1, §7).

Containers are the main backend for software-engineering and general tool-use
workloads. The production runtime is a modified dockerd that dynamically
composes the overlayfs stack at sandbox creation: the base image sits at the
bottom, the workspace is inserted as a read-only layer above it, and each
toolkit is stacked on top, with runtime writes directed to the writable upper
layer (the dockerd change is ~30 lines of Go, paper §7). This backend applies
the same composition and insertion at creation time.

When a Docker daemon is available and the request names a plain OCI image, the
backend delegates to it; otherwise it executes through the portable engine over
a materialized layer stack, with either eager extraction or EROFS-style
on-demand loading (paper §5.3) as the data path.
"""
from __future__ import annotations

import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional

from ..errors import BackendUnavailable
from ..types import FileStat, HttpResult, RunResult
from .base import Backend, SandboxContext
from .process import DEFAULT_OUTPUT_CAP, ProcessEngine

DOCKER_AVAILABLE = shutil.which("docker") is not None


def snapshot_upper_dir(rootfs_dir: str) -> dict:
    """Capture every file of the writable layer (pack_diff / pause, §6)."""
    from pathlib import Path

    root = Path(rootfs_dir)
    upper = {}
    if root.is_dir():
        for path in root.rglob("*"):
            if path.is_file():
                upper[path.relative_to(root).as_posix()] = path.read_bytes()
    return upper


class LayeredRootFS:
    """Writable upper on local disk over lazily-fetched EROFS layers.

    Reads resolve: upper (local) first, then the EROFS image serving the path —
    fetching only that file's chunks from 3FS on first access. This is the
    on-demand image-loading path of paper §5.3 in a portable implementation:
    no kernel EROFS mount is available, so a fetched file is materialized into
    the upper on first access instead of being paged in on the fly.
    """

    def __init__(self, rootfs_dir: str, manifest: Optional[Dict[str, Optional[bytes]]],
                 images_by_path: Optional[Dict[str, object]] = None,
                 ondemand_stats=None):
        self.rootfs = Path(rootfs_dir)
        self.manifest = manifest or {}
        self.images_by_path = images_by_path or {}
        self.ondemand_stats = ondemand_stats  # dict for fetched-bytes accounting

    def ensure_dirs(self) -> None:
        for path in self.manifest:
            (self.rootfs / path).parent.mkdir(parents=True, exist_ok=True)

    def exists(self, path: str) -> bool:
        rel = path.lstrip("/")
        if (self.rootfs / rel).exists():
            return True
        return rel in self.manifest or any(rel.startswith(p) for p in self.manifest)

    def read(self, path: str) -> bytes:
        rel = path.lstrip("/")
        local = self.rootfs / rel
        if local.is_file():
            return local.read_bytes()
        image = self.images_by_path.get(rel)
        if image is None:
            raise FileNotFoundError(path)
        data = image.read_all(rel)  # lazy: fetches only this file's chunks
        if self.ondemand_stats is not None:
            self.ondemand_stats["fetched"] = self.ondemand_stats.get("fetched", 0) + len(data)
        local.parent.mkdir(parents=True, exist_ok=True)
        local.write_bytes(data)
        return data

    def write(self, path: str, data: bytes) -> None:
        rel = path.lstrip("/")
        dest = self.rootfs / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)

    def listdir(self, path: str) -> List[FileStat]:
        rel = path.strip("/")
        base = self.rootfs / rel
        names = {}
        if base.is_dir():
            for entry in base.iterdir():
                names[entry.name] = entry.is_dir()
        prefix = rel + "/" if rel else ""
        for p in self.manifest:
            if not p.startswith(prefix):
                continue
            rest = p[len(prefix):]
            if rest and "/" not in rest:
                names.setdefault(rest, False)
        out = []
        for name in sorted(names):
            entry = self.rootfs / rel / name
            size = entry.stat().st_size if entry.exists() else 0
            out.append(FileStat(name=name, size=size, is_dir=names[name], mode=0o644))
        return out


class ContainerBackend(Backend):
    """Container backend: docker when present, layered rootfs otherwise."""

    name = "container"

    def __init__(self):
        self.docker_available = DOCKER_AVAILABLE
        self._rootfs: Dict[str, LayeredRootFS] = {}

    # -- docker helpers (only exercised when a daemon is reachable) ----------------
    async def _docker_create(self, ctx: SandboxContext) -> None:
        import asyncio

        image = ctx.spec.image
        proc = await asyncio.create_subprocess_exec(
            "docker", "run", "-d", "--name", ctx.sandbox_id,
            "--memory", "%dm" % ctx.spec.limits.memory_limit_mb,
            "--cpus", str(ctx.spec.limits.cpu_cores_limit),
            image, "sleep", "infinity",
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        _, err = await proc.communicate()
        if proc.returncode != 0:
            raise BackendUnavailable("docker run failed: %s" % err.decode().strip())

    async def _docker_run(self, ctx: SandboxContext, command: str, timeout: float) -> RunResult:
        import asyncio

        proc = await asyncio.create_subprocess_exec(
            "docker", "exec", ctx.sandbox_id, "/bin/sh", "-c", command,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return RunResult(exit_code=proc.returncode, stdout=out, stderr=err)
        except asyncio.TimeoutError:
            proc.kill()
            raise

    # -- lifecycle ------------------------------------------------------------------
    def _compose_rootfs(self, ctx: SandboxContext) -> LayeredRootFS:
        """Compose the layer stack and prepare the rootfs (paper §5.1, §7)."""
        from ..layers.overlay import OverlayFS

        layers: List = ctx.metadata.get("layer_stack", [])
        images: List = ctx.metadata.get("erofs_images", [])  # one per layer, bottom..top
        policy = ctx.spec.labels.get("image_loading", "eager")
        total_bytes = sum(l.size_bytes for l in layers)
        if policy == "eager":
            # Docker-cold baseline: extract everything at creation.
            OverlayFS(layers).materialize(ctx.rootfs_dir)
            if ctx.metrics is not None:
                ctx.metrics.inc("disk_extract_bytes", total_bytes)
                ctx.metrics.inc("eager_create_calls")
            rootfs = LayeredRootFS(ctx.rootfs_dir, {}, {})
        else:
            # EROFS on-demand: mount model — metadata local, data fetched on
            # access; no extraction writes at creation (paper §5.3).
            manifest = OverlayFS(layers).merged_files()
            images_by_path: Dict[str, object] = {}
            for path in manifest:
                for image in reversed(images):
                    if image.has_file(path):
                        images_by_path[path] = image
                        break
            rootfs = LayeredRootFS(
                ctx.rootfs_dir,
                {p: None for p in manifest},
                images_by_path,
                ondemand_stats=ctx.metadata.setdefault("ondemand_stats", {}),
            )
            rootfs.ensure_dirs()
            if ctx.metrics is not None:
                ctx.metrics.inc("ondemand_create_calls")
        if ctx.metrics is not None:
            ctx.metrics.inc("layer_insertions", len(layers))
        ctx.metadata["rootfs"] = rootfs
        ctx.metadata["log"] = ctx.metadata.get("log", []) + [
            "dockerd: dynamic lower-layer insertion for %s: %d layers" % (ctx.sandbox_id, len(layers))
        ]
        return rootfs

    async def create(self, ctx: SandboxContext) -> None:
        layers = ctx.metadata.get("layer_stack") or []
        plain_docker_image = bool(ctx.spec.labels.get("docker_image")) and not layers
        if self.docker_available and plain_docker_image:
            await self._docker_create(ctx)
            ctx.metadata["docker"] = True
        else:
            rootfs = self._compose_rootfs(ctx)
            self._rootfs[ctx.sandbox_id] = rootfs
            ctx.metadata["docker"] = False
        ctx.set_state("running")

    async def destroy(self, ctx: SandboxContext) -> None:
        if ctx.metadata.get("docker"):
            import asyncio

            await asyncio.create_subprocess_exec("docker", "rm", "-f", ctx.sandbox_id)
            ctx.metadata["docker"] = False
        else:
            self._rootfs.pop(ctx.sandbox_id, None)
            shutil.rmtree(ctx.rootfs_dir, ignore_errors=True)
        ctx.set_state("stopped")

    # -- operations -------------------------------------------------------------------
    async def run_shell(self, ctx: SandboxContext, command: str, *, timeout: float = 60.0,
                        env: Optional[Dict[str, str]] = None, stdin: bytes = b"") -> RunResult:
        ctx.touch()
        if ctx.metadata.get("docker"):
            return await self._docker_run(ctx, command, timeout)
        engine = ProcessEngine(ctx.rootfs_dir, sandbox_id=ctx.sandbox_id, cpu_qos=ctx.cpu_qos,
                               output_cap=DEFAULT_OUTPUT_CAP)
        result = await engine.run_shell_cmd(command, timeout=timeout, env=env, stdin=stdin)
        if ctx.metrics is not None:
            ctx.metrics.inc("tool_calls")
            ctx.metrics.inc("tool_call_ms", result.duration_ms)
        return result

    def _rootfs_of(self, ctx: SandboxContext) -> LayeredRootFS:
        rootfs = ctx.metadata.get("rootfs")
        if rootfs is None:
            rootfs = LayeredRootFS(ctx.rootfs_dir, {}, {})
            ctx.metadata["rootfs"] = rootfs
        return rootfs

    async def read_file(self, ctx: SandboxContext, path: str, max_bytes: int) -> bytes:
        if ctx.security is not None:
            ctx.security.check_file_access(ctx, path, "read")
        data = self._rootfs_of(ctx).read(path)
        return data[:max_bytes]

    async def write_file(self, ctx: SandboxContext, path: str, data: bytes, mode: int) -> None:
        if ctx.security is not None:
            ctx.security.check_file_access(ctx, path, "write")
        self._rootfs_of(ctx).write(path, data)

    async def list_dir(self, ctx: SandboxContext, path: str) -> List[FileStat]:
        return self._rootfs_of(ctx).listdir(path)

    async def http_request(self, ctx: SandboxContext, url: str, method: str = "GET",
                           body: bytes = b"") -> HttpResult:
        if ctx.security is not None:
            ctx.security.check_network(ctx, url)
        import urllib.error
        import urllib.request

        req = urllib.request.Request(url, data=body, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return HttpResult(status=resp.status, body=resp.read(),
                                  headers=dict(resp.headers.items()))
        except urllib.error.HTTPError as exc:
            return HttpResult(status=exc.code, body=exc.read(), headers=dict(exc.headers.items()))

    # -- state preservation ------------------------------------------------------------
    async def snapshot(self, ctx: SandboxContext) -> dict:
        return {"upper": snapshot_upper_dir(ctx.rootfs_dir), "state": ctx.state}

    async def restore(self, ctx: SandboxContext, snapshot: dict) -> None:
        rootfs = self._rootfs_of(ctx)
        for rel, data in snapshot.get("upper", {}).items():
            rootfs.write(rel, data)

    async def pause(self, ctx: SandboxContext) -> None:
        """docker pause + swap enable + proactive memory.reclaim (paper §6.3)."""
        if ctx.metadata.get("docker"):
            import asyncio

            await asyncio.create_subprocess_exec("docker", "pause", ctx.sandbox_id)
        else:
            engine = ProcessEngine(ctx.rootfs_dir, sandbox_id=ctx.sandbox_id, cpu_qos=ctx.cpu_qos)
            await engine.freeze()
        if ctx.memory is not None and ctx.guest_mem_id in ctx.memory.guests:
            guest = ctx.memory.guests[ctx.guest_mem_id]
            guest.fpr_enabled = True  # memory.swap.max enabled before reclaim
            ctx.memory.damon_reclaim(time.monotonic(), 0.0)
            ctx.memory.free_page_reporting()
        ctx.set_state("paused")

    async def resume(self, ctx: SandboxContext) -> None:
        """MADV_WILLNEED prefetch + docker unpause (paper §6.3)."""
        if ctx.metadata.get("docker"):
            import asyncio

            await asyncio.create_subprocess_exec("docker", "unpause", ctx.sandbox_id)
        else:
            engine = ProcessEngine(ctx.rootfs_dir, sandbox_id=ctx.sandbox_id, cpu_qos=ctx.cpu_qos)
            await engine.unfreeze()
        ctx.set_state("running")
