"""Firecracker microVM backend (paper §2.2, §5.3, §6.3).

MicroVMs provide a stronger isolation boundary than containers while retaining
Linux compatibility — used for security-sensitive tasks and computer-use
workloads. This backend models the Firecracker lifecycle and its storage path:

- read-only base/toolkit layers are EROFS images exposed to the guest as block
  devices; the guest root filesystem is overlayfs with an ext4 writable upper
  (the OverlayBD/ublk path, served in 256 KiB chunks with a second-level local
  cache, paper §5.3);
- memory follows the §5.2 model: virtio-pmem+DAX shares one host page-cache
  copy across co-located microVMs; DAMON + balloon free-page reporting reclaim
  idle guest memory;
- pausing snapshots memory/execution state, terminates the Firecracker process,
  and releases runtime memory; resume starts a new process and restores the
  snapshot (paper §6.3).
"""
from __future__ import annotations

import shutil
import time
from typing import Dict, List, Optional

from ..errors import PreconditionError
from ..types import FileStat, HttpResult, RunResult
from .base import Backend, SandboxContext
from .container import LayeredRootFS, snapshot_upper_dir
from .process import DEFAULT_OUTPUT_CAP, ProcessEngine

FIRECRACKER_AVAILABLE = shutil.which("firecracker") is not None


class MicroVMBackend(Backend):
    """Firecracker lifecycle model over the portable engine + memory model."""

    name = "microvm"

    def __init__(self):
        self.firecracker_available = FIRECRACKER_AVAILABLE
        self._rootfs: Dict[str, LayeredRootFS] = {}
        self._snapshots: Dict[str, dict] = {}

    # -- lifecycle -------------------------------------------------------------------
    def _compose_rootfs(self, ctx: SandboxContext) -> LayeredRootFS:
        from ..layers.overlay import OverlayFS

        layers: List = ctx.metadata.get("layer_stack", [])
        images: List = ctx.metadata.get("erofs_images", [])
        manifest = OverlayFS(layers).merged_files()
        if ctx.spec.labels.get("image_loading", "eager") == "eager":
            # Eager baseline (used when the whole working set is needed).
            OverlayFS(layers).materialize(ctx.rootfs_dir)
            rootfs = LayeredRootFS(ctx.rootfs_dir, {}, {})
        else:
            images_by_path: Dict[str, object] = {}
            for path in manifest:
                for image in reversed(images):
                    if image.has_file(path):
                        images_by_path[path] = image
                        break
            rootfs = LayeredRootFS(ctx.rootfs_dir, {p: None for p in manifest}, images_by_path,
                                   ondemand_stats=ctx.metadata.setdefault("ondemand_stats", {}))
            rootfs.ensure_dirs()
        ctx.metadata["rootfs"] = rootfs
        return rootfs

    def _register_memory(self, ctx: SandboxContext) -> None:
        if ctx.memory is None:
            return
        pmem = ctx.spec.labels.get("pmem_dax", "1") in ("1", "true", "yes")
        fpr = ctx.spec.labels.get("balloon_fpr", "1") in ("1", "true", "yes")
        ctx.memory.register(
            ctx.sandbox_id,
            ctx.spec.limits.memory_limit_mb,
            pmem_dax=pmem,
            fpr_enabled=fpr,
            pmem_capacity_mb=sum(img.data_bytes for img in ctx.metadata.get("erofs_images", [])) / 1e6,
        )
        ctx.guest_mem_id = ctx.sandbox_id

    async def create(self, ctx: SandboxContext) -> None:
        rootfs = self._compose_rootfs(ctx)
        self._rootfs[ctx.sandbox_id] = rootfs
        self._register_memory(ctx)
        ctx.metadata["log"] = ctx.metadata.get("log", []) + [
            "microvm: Firecracker boot (guest kernel 6.1, virtio-pmem=%s)" %
            ("DAX" if ctx.spec.labels.get("pmem_dax", "1") in ("1", "true", "yes") else "off")
        ]
        ctx.set_state("running")

    async def destroy(self, ctx: SandboxContext) -> None:
        self._rootfs.pop(ctx.sandbox_id, None)
        self._snapshots.pop(ctx.sandbox_id, None)
        if ctx.memory is not None and ctx.guest_mem_id in ctx.memory.guests:
            ctx.memory.release(ctx.guest_mem_id)
        shutil.rmtree(ctx.rootfs_dir, ignore_errors=True)
        ctx.set_state("stopped")

    # -- operations ---------------------------------------------------------------------
    async def _ensure_running(self, ctx: SandboxContext) -> None:
        if ctx.state == "paused":
            await self.resume(ctx)

    async def run_shell(self, ctx: SandboxContext, command: str, *, timeout: float = 60.0,
                        env: Optional[Dict[str, str]] = None, stdin: bytes = b"") -> RunResult:
        await self._ensure_running(ctx)
        ctx.touch()
        engine = ProcessEngine(ctx.rootfs_dir, sandbox_id=ctx.sandbox_id, cpu_qos=ctx.cpu_qos,
                               output_cap=DEFAULT_OUTPUT_CAP)
        result = await engine.run_shell_cmd(command, timeout=timeout, env=env, stdin=stdin)
        if ctx.metrics is not None:
            ctx.metrics.inc("tool_calls")
            ctx.metrics.inc("tool_call_ms", result.duration_ms)
        return result

    def _rootfs_of(self, ctx: SandboxContext) -> LayeredRootFS:
        return self._rootfs[ctx.sandbox_id]

    async def read_file(self, ctx: SandboxContext, path: str, max_bytes: int) -> bytes:
        await self._ensure_running(ctx)
        if ctx.security is not None:
            ctx.security.check_file_access(ctx, path, "read")
        data = self._rootfs_of(ctx).read(path)
        self._account_read(ctx, data)
        return data[:max_bytes]

    def _account_read(self, ctx: SandboxContext, data: bytes) -> None:
        """Guest page-cache accounting: host-shared (pmem) or per-guest copy."""
        if ctx.memory is not None and ctx.guest_mem_id in ctx.memory.guests:
            guest = ctx.memory.guests[ctx.guest_mem_id]
            if not guest.pmem_dax:
                ctx.memory.touch_file(ctx.guest_mem_id, "file-read-%s" % ctx.sandbox_id,
                                      max(len(data) / 1e6, 0.001), time.monotonic())

    async def write_file(self, ctx: SandboxContext, path: str, data: bytes, mode: int) -> None:
        await self._ensure_running(ctx)
        if ctx.security is not None:
            ctx.security.check_file_access(ctx, path, "write")
        self._rootfs_of(ctx).write(path, data)

    async def list_dir(self, ctx: SandboxContext, path: str) -> List[FileStat]:
        await self._ensure_running(ctx)
        return self._rootfs_of(ctx).listdir(path)

    async def http_request(self, ctx: SandboxContext, url: str, method: str = "GET",
                           body: bytes = b"") -> HttpResult:
        await self._ensure_running(ctx)
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

    # -- snapshot / pause / resume (paper §6.3) -------------------------------------------
    async def snapshot(self, ctx: SandboxContext) -> dict:
        snap = {"upper": snapshot_upper_dir(ctx.rootfs_dir), "state": ctx.state}
        self._snapshots[ctx.sandbox_id] = snap
        return snap

    async def restore(self, ctx: SandboxContext, snapshot: dict) -> None:
        rootfs = self._rootfs_of(ctx)
        for rel, data in snapshot.get("upper", {}).items():
            rootfs.write(rel, data)

    async def pause(self, ctx: SandboxContext) -> None:
        """Snapshot memory/exec state, terminate Firecracker, release memory."""
        snap = await self.snapshot(ctx)
        if ctx.memory is not None and ctx.guest_mem_id in ctx.memory.guests:
            ctx.memory.release(ctx.guest_mem_id)
        ctx.metadata["log"] = ctx.metadata.get("log", []) + [
            "microvm: pause — Firecracker process terminated, %d upper files snapshotted"
            % len(snap["upper"])
        ]
        ctx.set_state("paused")

    async def resume(self, ctx: SandboxContext) -> None:
        """Start a new process and restore the snapshot (paper §6.3)."""
        if ctx.sandbox_id not in self._snapshots:
            raise PreconditionError("microVM has no snapshot to resume")
        snapshot = self._snapshots.pop(ctx.sandbox_id)
        await self.restore(ctx, snapshot)
        self._register_memory(ctx)
        ctx.metadata["log"] = ctx.metadata.get("log", []) + [
            "microvm: resume — new Firecracker process, snapshot restored"
        ]
        ctx.set_state("running")
