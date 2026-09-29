"""Portable execution engine: runs real commands inside a sandbox rootfs.

This is the reference implementation's execution substrate on hosts without
Docker/Firecracker/QEMU. It applies the same runtime policies the kernel
mechanisms provide in production:

- the child runs with the sandbox's CPU QoS class (SCHED_IDLE / core-scheduling
  cookie on Linux);
- command output is captured with a hard budget — the paper records an agent
  invoking ``yes`` whose continuous output accumulated tens of gigabytes
  (§6.4); here the capture is cut and the process killed;
- all file access happens inside the materialized rootfs (the sandbox's
  filesystem boundary).
"""
from __future__ import annotations

import asyncio
import os
import shutil
import signal
from pathlib import Path
from typing import Dict, List, Optional

from ..errors import SandboxError, SandboxTimeout
from ..types import FileStat, HttpResult, RunResult
from .base import Backend, SandboxContext

DEFAULT_OUTPUT_CAP = 1024 * 1024  # 1 MiB per command (paper §6.4 output guard)
_READ_CHUNK = 64 * 1024


class ProcessEngine:
    """Executes commands via subprocess inside a rootfs directory."""

    def __init__(self, rootfs_dir: str, sandbox_id: str = "",
                 cpu_qos=None, output_cap: int = DEFAULT_OUTPUT_CAP,
                 base_env: Optional[Dict[str, str]] = None, shell: str = "/bin/sh"):
        self.rootfs = Path(rootfs_dir)
        self.sandbox_id = sandbox_id
        self.cpu_qos = cpu_qos
        self.output_cap = output_cap
        self.shell = shell
        self.base_env = dict(base_env or {})
        self._proc: Optional[asyncio.subprocess.Process] = None

    def _env(self, extra: Optional[Dict[str, str]]) -> Dict[str, str]:
        env = {
            "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
            "HOME": "/root",
            "LANG": "C.UTF-8",
        }
        env.update(self.base_env)
        env.update(extra or {})
        return env

    async def run(self, argv: List[str], *, cwd: str = "", timeout: float = 60.0,
                  env: Optional[Dict[str, str]] = None, stdin: bytes = b"") -> RunResult:
        cwd_path = self.rootfs / cwd.lstrip("/")
        if not cwd_path.is_dir():
            cwd_path = self.rootfs
        preexec = self.cpu_qos.preexec_fn(self.sandbox_id) if self.cpu_qos else None
        try:
            self._proc = await asyncio.create_subprocess_exec(
                *argv,
                cwd=str(cwd_path),
                env=self._env(env),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE if stdin else asyncio.subprocess.DEVNULL,
                preexec_fn=preexec,
            )
        except FileNotFoundError as exc:
            raise SandboxError("cannot exec %r: %s" % (argv[0], exc))
        out = bytearray()
        err = bytearray()
        truncated = False
        loop = asyncio.get_event_loop()
        start = loop.time()

        async def _pump(stream, sink) -> None:
            """Read one stream up to the shared cap; cut and kill on overflow."""
            nonlocal truncated
            while True:
                chunk = await stream.read(_READ_CHUNK)
                if not chunk:
                    return
                if not truncated and len(out) + len(err) + len(chunk) > self.output_cap:
                    # The `yes` case (paper §6.4): cut the capture, kill the
                    # process so unbounded output cannot fill node storage.
                    truncated = True
                    if self._proc is not None and self._proc.returncode is None:
                        self._proc.kill()
                room = max(self.output_cap - len(sink), 0)
                sink.extend(chunk[:room])

        async def _run():
            await asyncio.gather(_pump(self._proc.stdout, out), _pump(self._proc.stderr, err))
            return await self._proc.wait()

        try:
            if stdin:
                self._proc.stdin.write(stdin)
                await self._proc.stdin.drain()
                self._proc.stdin.close()
            await asyncio.wait_for(_run(), timeout=timeout)
        except asyncio.TimeoutError:
            self.kill()
            raise SandboxTimeout("command exceeded %.1fs" % timeout)
        duration_ms = (loop.time() - start) * 1000.0
        return RunResult(
            exit_code=self._proc.returncode if self._proc.returncode is not None else -1,
            stdout=bytes(out[: self.output_cap]),
            stderr=bytes(err[: self.output_cap]),
            truncated=truncated,
            duration_ms=duration_ms,
        )

    async def run_shell_cmd(self, command: str, **kwargs) -> RunResult:
        return await self.run([self.shell, "-c", command], **kwargs)

    def kill(self) -> None:
        if self._proc is not None and self._proc.returncode is None:
            try:
                self._proc.terminate()
            except ProcessLookupError:
                pass
        self._proc = None

    # -- signal management for pause/resume ------------------------------------
    async def freeze(self) -> bool:
        """SIGSTOP the current process tree; True if something was stopped."""
        if self._proc is not None and self._proc.returncode is None:
            try:
                self._proc.send_signal(signal.SIGSTOP)
            except ProcessLookupError:
                pass
            return True
        return False

    async def unfreeze(self) -> None:
        if self._proc is not None and self._proc.returncode is None:
            try:
                self._proc.send_signal(signal.SIGCONT)
            except ProcessLookupError:
                pass


class ProcessBackend(Backend):
    """Backend running directly through the portable engine (substrate).

    Used by the container/microVM backends as their execution engine, and by
    FnCall as its pooled executor.
    """

    name = "process"

    def __init__(self, engine_factory=None):
        self._engine_factory = engine_factory or (lambda ctx: ProcessEngine(
            ctx.rootfs_dir, sandbox_id=ctx.sandbox_id, cpu_qos=ctx.cpu_qos,
            output_cap=DEFAULT_OUTPUT_CAP))
        self._engines: Dict[str, ProcessEngine] = {}

    def engine(self, ctx: SandboxContext) -> ProcessEngine:
        engine = self._engines.get(ctx.sandbox_id)
        if engine is None:
            engine = self._engine_factory(ctx)
            self._engines[ctx.sandbox_id] = engine
        return engine

    async def create(self, ctx: SandboxContext) -> None:
        Path(ctx.rootfs_dir).mkdir(parents=True, exist_ok=True)
        ctx.set_state("running")

    async def destroy(self, ctx: SandboxContext) -> None:
        engine = self._engines.pop(ctx.sandbox_id, None)
        if engine is not None:
            engine.kill()
        shutil.rmtree(ctx.rootfs_dir, ignore_errors=True)
        ctx.set_state("stopped")

    async def run_shell(self, ctx: SandboxContext, command: str, *, timeout: float = 60.0,
                        env: Optional[Dict[str, str]] = None, stdin: bytes = b"") -> RunResult:
        ctx.touch()
        return await self.engine(ctx).run_shell_cmd(command, timeout=timeout, env=env, stdin=stdin)

    # -- file operations (all inside the rootfs) -----------------------------------
    def _resolve(self, ctx: SandboxContext, path: str) -> Path:
        rel = path.lstrip("/")
        root = Path(ctx.rootfs_dir).resolve()
        target = (root / rel).resolve()
        if not str(target).startswith(str(root) + os.sep) and target != root:
            raise PermissionError("path escapes sandbox rootfs: %r" % path)
        return target

    async def read_file(self, ctx: SandboxContext, path: str, max_bytes: int) -> bytes:
        if ctx.security is not None:
            ctx.security.check_file_access(ctx, path, "read")
        target = self._resolve(ctx, path)
        data = target.read_bytes()
        return data[:max_bytes]

    async def write_file(self, ctx: SandboxContext, path: str, data: bytes, mode: int) -> None:
        if ctx.security is not None:
            ctx.security.check_file_access(ctx, path, "write")
        target = self._resolve(ctx, path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        os.chmod(target, mode)

    async def list_dir(self, ctx: SandboxContext, path: str) -> List[FileStat]:
        target = self._resolve(ctx, path)
        out = []
        for entry in sorted(target.iterdir()):
            out.append(FileStat(name=entry.name, size=entry.stat().st_size,
                                is_dir=entry.is_dir(), mode=entry.stat().st_mode & 0o777))
        return out

    async def http_request(self, ctx: SandboxContext, url: str, method: str = "GET",
                           body: bytes = b"") -> HttpResult:
        if ctx.security is not None:
            ctx.security.check_network(ctx, url)
        import urllib.request

        req = urllib.request.Request(url, data=body, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return HttpResult(status=resp.status, body=resp.read(),
                                  headers=dict(resp.headers.items()))
        except urllib.error.HTTPError as exc:
            return HttpResult(status=exc.code, body=exc.read(), headers=dict(exc.headers.items()))

    async def snapshot(self, ctx: SandboxContext) -> dict:
        return {"cwd": "", "env": dict(self.engine(ctx).base_env)}

    async def restore(self, ctx: SandboxContext, snapshot: dict) -> None:
        engine = self.engine(ctx)
        engine.base_env = dict(snapshot.get("env", {}))

    async def pause(self, ctx: SandboxContext) -> None:
        engine = self.engine(ctx)
        await engine.freeze()
        # Memory reclamation while paused (paper §6.3: swap enable + reclaim).
        if ctx.memory is not None and ctx.guest_mem_id in ctx.memory.guests:
            guest = ctx.memory.guests[ctx.guest_mem_id]
            guest.fpr_enabled = True
            ctx.memory.damon_reclaim(float("inf"), 0.0)
            ctx.memory.free_page_reporting()
        ctx.set_state("paused")

    async def resume(self, ctx: SandboxContext) -> None:
        engine = self.engine(ctx)
        await engine.unfreeze()
        ctx.set_state("running")
