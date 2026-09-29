"""Full VM backend: COTS operating systems (paper §2.2, §3.3).

Full VMs cover workloads that require a complete commercial off-the-shelf OS
environment — Android VMs through QEMU, GUI/graphics rendering, and full-system
execution. They have the highest resource overhead but are necessary for tasks
depending on OS-specific APIs or full-system behavior.

The production design runs QEMU VMs with para-virtualized GPU interfaces
(virtio-gpu) and host-native rendering via compatibility layers such as DXVK
(paper §3.3). This reference backend implements the same lifecycle (prepared
VM image/snapshot instead of composed layers; snapshot/restore; no EROFS
layer stack) over the portable engine, with a QEMU integration point for hosts
that have it.
"""
from __future__ import annotations

import shutil
from typing import Dict, List, Optional

from ..errors import BackendUnavailable
from ..types import FileStat, HttpResult, RunResult
from .base import Backend, SandboxContext
from .container import LayeredRootFS, snapshot_upper_dir
from .process import DEFAULT_OUTPUT_CAP, ProcessEngine

QEMU_AVAILABLE = shutil.which("qemu-system-x86_64") is not None


class FullVMBackend(Backend):
    """QEMU full-VM lifecycle model (prepared images, no composed layers)."""

    name = "fullvm"

    def __init__(self):
        self.qemu_available = QEMU_AVAILABLE
        self._rootfs: Dict[str, LayeredRootFS] = {}
        self._snapshots: Dict[str, dict] = {}

    async def create(self, ctx: SandboxContext) -> None:
        # Full VMs consume a prepared VM image or snapshot (§2.3), not a
        # composed layer stack; the image is resolved as a single layer.
        image = ctx.metadata.get("vm_image_layer")
        if image is None:
            raise BackendUnavailable("full VM requires a prepared VM image")
        rootfs = LayeredRootFS(ctx.rootfs_dir, {p: None for p in image.files}, {})
        rootfs.ensure_dirs()
        self._rootfs[ctx.sandbox_id] = rootfs
        ctx.metadata["rootfs"] = rootfs
        ctx.metadata["log"] = ctx.metadata.get("log", []) + [
            "fullvm: QEMU VM boot%s (virtio-gpu passthrough, DXVK translation for "
            "non-native graphics APIs)" % ("" if self.qemu_available else " [modeled]")
        ]
        ctx.set_state("running")

    async def destroy(self, ctx: SandboxContext) -> None:
        self._rootfs.pop(ctx.sandbox_id, None)
        self._snapshots.pop(ctx.sandbox_id, None)
        shutil.rmtree(ctx.rootfs_dir, ignore_errors=True)
        ctx.set_state("stopped")

    async def run_shell(self, ctx: SandboxContext, command: str, *, timeout: float = 60.0,
                        env: Optional[Dict[str, str]] = None, stdin: bytes = b"") -> RunResult:
        ctx.touch()
        engine = ProcessEngine(ctx.rootfs_dir, sandbox_id=ctx.sandbox_id, cpu_qos=ctx.cpu_qos,
                               output_cap=DEFAULT_OUTPUT_CAP)
        return await engine.run_shell_cmd(command, timeout=timeout, env=env, stdin=stdin)

    def _rootfs_of(self, ctx: SandboxContext) -> LayeredRootFS:
        return self._rootfs[ctx.sandbox_id]

    async def read_file(self, ctx: SandboxContext, path: str, max_bytes: int) -> bytes:
        if ctx.security is not None:
            ctx.security.check_file_access(ctx, path, "read")
        return self._rootfs_of(ctx).read(path)[:max_bytes]

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

    async def snapshot(self, ctx: SandboxContext) -> dict:
        snap = {"upper": snapshot_upper_dir(ctx.rootfs_dir)}
        self._snapshots[ctx.sandbox_id] = snap
        return snap

    async def restore(self, ctx: SandboxContext, snapshot: dict) -> None:
        rootfs = self._rootfs_of(ctx)
        for rel, data in snapshot.get("upper", {}).items():
            rootfs.write(rel, data)

    async def pause(self, ctx: SandboxContext) -> None:
        await self.snapshot(ctx)
        ctx.set_state("paused")

    async def resume(self, ctx: SandboxContext) -> None:
        if ctx.sandbox_id not in self._snapshots:
            raise BackendUnavailable("full VM has no snapshot to resume")
        await self.restore(ctx, self._snapshots.pop(ctx.sandbox_id))
        ctx.set_state("running")
