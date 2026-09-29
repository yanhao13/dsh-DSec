"""Edge: per-node sandbox runtime (paper §3.1, §3.3, §7).

Each node runs an edge, which handles creation requests for the container,
microVM, QEMU full-VM, and FnCall backends. Before accepting a creation
request, the edge checks the node's current capacity and rejects it if capacity
is insufficient — node-local admission complements the placement engine's
decision, which is based on periodically refreshed cluster state. During
creation the edge provisions storage, applies the network policy, and launches
the runtime. It also tracks the sandbox lifecycle, coordinates snapshots,
releases node-local resources when a sandbox stops or its TTL expires, and runs
the memory reclamation ticks (DAMON + balloon free-page reporting).
"""
from __future__ import annotations

import asyncio
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import idgen
from .aether import Aether
from .backends import (
    ContainerBackend,
    FnCallBackend,
    FnCallPool,
    FullVMBackend,
    MicroVMBackend,
)
from .backends.base import Backend, SandboxContext, SandboxState
from .errors import AdmissionError, BackendUnavailable, NotFound
from .layers.registry import LayerRegistry
from .metrics import Metrics
from .resources.cpu import CpuQoS
from .resources.memory import MemoryManager
from .types import (
    BACKEND_CONTAINER,
    BACKEND_FNCALL,
    BACKEND_FULLVM,
    BACKEND_MICROVM,
    NodeCapacity,
    SandboxSpec,
)

# Admission overcommit factors (paper §4.3: sparse CPU, constrained memory).
CPU_OVERCOMMIT = 16.0
MEMORY_OVERCOMMIT = 2.0


class Edge:
    """Node-local admission, provisioning, lifecycle, and reclamation."""

    def __init__(self, edge_id: str, capacity: NodeCapacity, store, registry: LayerRegistry, *,
                 rootfs_base: str = "", security=None, cpu_qos: Optional[CpuQoS] = None,
                 memory: Optional[MemoryManager] = None, chunk_cache=None,
                 docker_backend=None, microvm_backend=None, fullvm_backend=None,
                 fncall_pools: Optional[Dict[str, FnCallPool]] = None,
                 ttl_interval: float = 5.0, reclaim_interval: float = 30.0,
                 cold_age_s: float = 300.0):
        self.edge_id = edge_id
        self.capacity = capacity
        self.store = store
        self.registry = registry
        self.rootfs_base = rootfs_base or tempfile.mkdtemp(prefix="dsec-edge-")
        os.makedirs(self.rootfs_base, exist_ok=True)
        self.security = security
        self.cpu_qos = cpu_qos or CpuQoS()
        self.memory = memory or MemoryManager(host_memory_mb=capacity.memory_mb)
        self.chunk_cache = chunk_cache
        self.metrics = Metrics(name="edge-%s" % edge_id)
        self.backends: Dict[str, Backend] = {
            BACKEND_CONTAINER: docker_backend or ContainerBackend(),
            BACKEND_MICROVM: microvm_backend or MicroVMBackend(),
            BACKEND_FULLVM: fullvm_backend or FullVMBackend(),
        }
        self.fncall_pools = fncall_pools or {}
        self.backends[BACKEND_FNCALL] = FnCallBackend(
            cpu_pool=self.fncall_pools.get("cpu"),
            gpu_pool=self.fncall_pools.get("gpu"),
        )
        self.sandboxes: Dict[str, SandboxContext] = {}
        self._seq = 0
        self._stopping = False
        self._ttl_task: Optional[asyncio.Task] = None
        self._reclaim_task: Optional[asyncio.Task] = None
        self.ttl_interval = ttl_interval
        self.reclaim_interval = reclaim_interval
        self.cold_age_s = cold_age_s
        self.rejections = 0

    # -- startup -------------------------------------------------------------------
    async def start(self) -> None:
        for pool in self.fncall_pools.values():
            await pool.start()
        self._ttl_task = asyncio.create_task(self._ttl_loop())
        self._reclaim_task = asyncio.create_task(self._reclaim_loop())

    async def stop(self) -> None:
        self._stopping = True
        for task in (self._ttl_task, self._reclaim_task):
            if task is not None:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
        for pool in self.fncall_pools.values():
            await pool.stop()
        for sandbox_id in list(self.sandboxes):
            await self.destroy(sandbox_id)
        shutil.rmtree(self.rootfs_base, ignore_errors=True)

    # -- admission -------------------------------------------------------------------
    def _admit(self, spec: SandboxSpec) -> None:
        """Node-local admission: reject if capacity is insufficient (paper §7)."""
        if spec.backend not in self.capacity.backends:
            self.rejections += 1
            raise AdmissionError("backend %r not provided by edge %s" % (spec.backend, self.edge_id))
        if spec.gpu and self.capacity.gpu_instances <= 0:
            self.rejections += 1
            raise AdmissionError("edge %s has no GPU" % self.edge_id)
        count = len(self.sandboxes)
        if count >= self.capacity.max_sandboxes:
            self.rejections += 1
            raise AdmissionError("edge %s at sandbox capacity (%d)" % (self.edge_id, count))
        cpu_used = sum(s.spec.limits.cpu_cores_limit for s in self.sandboxes.values())
        if cpu_used + spec.limits.cpu_cores_limit > self.capacity.cpu_cores * CPU_OVERCOMMIT:
            self.rejections += 1
            raise AdmissionError("edge %s CPU overcommit limit reached" % self.edge_id)
        mem_used = sum(s.spec.limits.memory_limit_mb for s in self.sandboxes.values())
        if mem_used + spec.limits.memory_limit_mb > self.capacity.memory_mb * MEMORY_OVERCOMMIT:
            self.rejections += 1
            raise AdmissionError("edge %s memory overcommit limit reached" % self.edge_id)

    # -- creation ---------------------------------------------------------------------
    def _parse_ref(self, image: str) -> Tuple[str, str]:
        if ":" in image:
            name, version = image.rsplit(":", 1)
            return name, version
        return image, "latest"

    async def create(self, spec: SandboxSpec) -> str:
        """Provision and launch a sandbox (paper §3.3 creation path)."""
        self._admit(spec)
        self._seq += 1
        sandbox_id = idgen.new_sandbox_id(self.edge_id, self._seq)
        rootfs_dir = os.path.join(self.rootfs_base, sandbox_id)
        ctx = SandboxContext(
            sandbox_id=sandbox_id,
            spec=spec,
            rootfs_dir=rootfs_dir,
            metrics=self.metrics,
            cpu_qos=self.cpu_qos,
            memory=self.memory,
            security=self.security,
            chunk_cache=self.chunk_cache,
            store=self.store,
            metadata={
                "project": spec.project,
                "user": spec.labels.get("user", ""),
                "task": spec.labels.get("task", ""),
                "network_policy": None,
                "log": [],
            },
        )
        self.cpu_qos.assign(sandbox_id, spec.qos)
        try:
            await self._provision_layers(ctx)
            self._apply_network_policy(ctx)
            backend = self.backends[spec.backend]
            await backend.create(ctx)
            aether = Aether(sandbox_id, ctx, backend)
            ctx.metadata["aether"] = aether
            ctx.set_state(SandboxState.RUNNING)
        except Exception as exc:
            ctx.set_state(SandboxState.FAILED)
            shutil.rmtree(rootfs_dir, ignore_errors=True)
            self.cpu_qos.release(sandbox_id)
            self.metrics.inc("create_failures")
            if isinstance(exc, (AdmissionError, BackendUnavailable)):
                raise
            raise BackendUnavailable("create failed: %r" % exc)
        self.sandboxes[sandbox_id] = ctx
        self.metrics.inc("creations")
        self.metrics.inc("sandboxes_%s" % spec.backend)
        self.metrics.inc("create_seconds", time.monotonic() - ctx.created_at)
        return sandbox_id

    async def _provision_layers(self, ctx: SandboxContext) -> None:
        """Resolve the environment stack: base + workspace + toolkits (§5.1)."""
        spec = ctx.spec
        if spec.backend == BACKEND_FNCALL:
            return
        if spec.backend == BACKEND_FULLVM:
            name, version = self._parse_ref(spec.image)
            ctx.metadata["vm_image_layer"] = self.registry.get_layer(name, version)
            return
        base_name, base_version = self._parse_ref(spec.image)
        eager = spec.labels.get("image_loading", "eager") == "eager"
        fetch_layer = self.registry.get_layer if eager else self.registry.get_layer_paths
        layers = [fetch_layer(base_name, base_version)]
        images = [self.registry.get_image(base_name, base_version)]
        if spec.workspace is not None:
            layers.append(fetch_layer(spec.workspace.name, spec.workspace.version))
            images.append(self.registry.get_image(spec.workspace.name, spec.workspace.version))
        for toolkit in spec.toolkits:
            layers.append(fetch_layer(toolkit.name, toolkit.version))
            images.append(self.registry.get_image(toolkit.name, toolkit.version))
        ctx.metadata["layer_stack"] = layers
        ctx.metadata["erofs_images"] = images
        # Register a memory guest for reclamation accounting (§5.2, §6.3).
        pmem = spec.labels.get("pmem_dax", "0") in ("1", "true", "yes")
        fpr = spec.labels.get("balloon_fpr", "0") in ("1", "true", "yes")
        self.memory.register(
            sandbox_id=ctx.sandbox_id,
            ram_mb=spec.limits.memory_limit_mb,
            pmem_dax=pmem,
            fpr_enabled=fpr,
            pmem_capacity_mb=sum(img.data_bytes for img in images) / 1e6,
        )
        ctx.guest_mem_id = ctx.sandbox_id

    def _apply_network_policy(self, ctx: SandboxContext) -> None:
        """Apply the per-sandbox network policy (eBPF allowlist, paper §6.5)."""
        if self.security is not None:
            ctx.metadata["network_policy"] = self.security.render_ebpf_rules(ctx.spec.network)

    # -- operations forwarding ------------------------------------------------------------
    def _ctx(self, sandbox_id: str) -> SandboxContext:
        ctx = self.sandboxes.get(sandbox_id)
        if ctx is None:
            raise NotFound("sandbox %s not on edge %s" % (sandbox_id, self.edge_id))
        return ctx

    def aether(self, sandbox_id: str) -> Aether:
        return self._ctx(sandbox_id).metadata["aether"]

    async def run(self, sandbox_id: str, terminal_id: str, token: str, command: str, *,
                  timeout: float = 60.0, env=None, stdin: bytes = b""):
        ctx = self._ctx(sandbox_id)
        if ctx.state == SandboxState.PAUSED:
            await self.resume(sandbox_id)  # transparent resume before ops (§6.3)
        return await self.aether(sandbox_id).run(terminal_id, token, command,
                                                 timeout=timeout, env=env, stdin=stdin)

    async def read_file(self, sandbox_id: str, terminal_id: str, token: str, path: str, max_bytes: int):
        return await self.aether(sandbox_id).read_file(terminal_id, token, path, max_bytes)

    async def write_file(self, sandbox_id: str, terminal_id: str, token: str, path: str, data: bytes, mode: int):
        return await self.aether(sandbox_id).write_file(terminal_id, token, path, data, mode)

    async def list_dir(self, sandbox_id: str, terminal_id: str, token: str, path: str):
        return await self.aether(sandbox_id).list_dir(terminal_id, token, path)

    async def http(self, sandbox_id: str, terminal_id: str, token: str, url: str, method: str, body: bytes):
        return await self.aether(sandbox_id).http(terminal_id, token, url, method, body)

    async def open_session(self, sandbox_id: str) -> Tuple[str, str]:
        return self.aether(sandbox_id).open_session()

    async def close_session(self, sandbox_id: str, terminal_id: str, token: str) -> None:
        self.aether(sandbox_id).close_session(terminal_id, token)

    # -- lifecycle -----------------------------------------------------------------------------
    async def pause(self, sandbox_id: str) -> None:
        ctx = self._ctx(sandbox_id)
        if ctx.state == SandboxState.PAUSED:
            return
        backend = self.backends[ctx.spec.backend]
        await backend.pause(ctx)
        self.metrics.inc("pauses")

    async def resume(self, sandbox_id: str) -> None:
        ctx = self._ctx(sandbox_id)
        if ctx.state != SandboxState.PAUSED:
            return
        backend = self.backends[ctx.spec.backend]
        await backend.resume(ctx)
        self.metrics.inc("resumes")

    async def snapshot(self, sandbox_id: str) -> dict:
        ctx = self._ctx(sandbox_id)
        return await self.backends[ctx.spec.backend].snapshot(ctx)

    async def destroy(self, sandbox_id: str) -> None:
        ctx = self.sandboxes.pop(sandbox_id, None)
        if ctx is None:
            return
        if self.memory is not None and sandbox_id in self.memory.guests:
            self.memory.release(sandbox_id)
        self.cpu_qos.release(sandbox_id)
        backend = self.backends[ctx.spec.backend]
        try:
            await backend.destroy(ctx)
        finally:
            self.metrics.inc("destructions")
            self.metrics.inc("sandbox_seconds", time.monotonic() - ctx.created_at)

    # -- background loops --------------------------------------------------------------------------
    async def _ttl_loop(self) -> None:
        """Stop idle (ttl_running_stop) or expired (ttl_absolute) sandboxes (§2.3)."""
        while not self._stopping:
            await asyncio.sleep(self.ttl_interval)
            await self._ttl_pass()

    async def _ttl_pass(self) -> int:
        """One TTL sweep; returns the number of sandboxes reclaimed."""
        reclaimed = 0
        now = time.monotonic()
        for sandbox_id, ctx in list(self.sandboxes.items()):
            if ctx.state != SandboxState.RUNNING:
                continue
            idle = now - ctx.last_active
            age = now - ctx.created_at
            if idle >= ctx.spec.ttl_running_stop or age >= ctx.spec.ttl_absolute:
                self.metrics.inc("ttl_reclaims")
                await self.destroy(sandbox_id)
                reclaimed += 1
        return reclaimed

    async def _reclaim_loop(self) -> None:
        """Periodic DAMON reclamation + balloon free-page reporting (§5.2)."""
        while not self._stopping:
            await asyncio.sleep(self.reclaim_interval)
            self.memory.damon_reclaim(time.monotonic(), self.cold_age_s)
            self.memory.free_page_reporting()

    # -- watcher stats --------------------------------------------------------------------------------
    def stats(self):
        from .watcher import EdgeStats

        running: Dict[str, int] = {}
        per_user: Dict[str, int] = {}
        per_task: Dict[str, int] = {}
        for ctx in self.sandboxes.values():
            running[ctx.spec.backend] = running.get(ctx.spec.backend, 0) + 1
            user = ctx.metadata.get("user") or "-"
            per_user[user] = per_user.get(user, 0) + 1
            task = ctx.metadata.get("task") or "-"
            per_task[task] = per_task.get(task, 0) + 1
        cpu_used = sum(s.spec.limits.cpu_cores_limit for s in self.sandboxes.values())
        mem_used = self.memory.host_usage_mb()
        return EdgeStats(
            edge_id=self.edge_id,
            healthy=True,
            running=running,
            per_user=per_user,
            per_task=per_task,
            cpu_used=cpu_used,
            cpu_capacity=self.capacity.cpu_cores,
            mem_used_mb=mem_used,
            mem_capacity_mb=self.capacity.memory_mb,
            gpu_instances=self.capacity.gpu_instances,
            gpu_used=sum(1 for s in self.sandboxes.values() if s.spec.gpu),
            backends=list(self.capacity.backends),
            last_seen=time.monotonic(),
        )
