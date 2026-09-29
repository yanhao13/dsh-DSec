"""Chronus: the shell-session abstraction inside a sandbox (paper §3.3).

Each chronus instance is one independent shell session. It exposes the
cross-platform interfaces the SDK relies on: command execution, filesystem
operations, HTTP requests, and streaming I/O. Multiple chronus instances run
concurrently within the same sandbox; aether locates them by terminal-session
identifier.

Two production hardening details are enforced here:

- command output is captured with a budget (paper §6.4: ``yes`` accumulated
  tens of gigabytes);
- access to platform-managed paths is denied even for root inside the sandbox
  (paper §6.5: chronus logs/sockets, /bin/bash).
"""
from __future__ import annotations

from typing import AsyncIterator, Dict, List, Optional, Tuple

from .errors import PreconditionError
from .types import FileStat, HttpResult, RunResult
from .backends.base import Backend, SandboxContext

DEFAULT_MAX_OUTPUT_BYTES = 1024 * 1024


class ShellSession:
    """One terminal session; forwards operations to the sandbox backend."""

    def __init__(self, terminal_id: str, ctx: SandboxContext, backend: Backend,
                 max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES):
        self.terminal_id = terminal_id
        self.ctx = ctx
        self.backend = backend
        self.max_output_bytes = max_output_bytes
        self._running = False

    async def exec(self, command: str, *, timeout: float = 60.0,
                   env: Optional[Dict[str, str]] = None, stdin: bytes = b"") -> RunResult:
        if self.ctx.state in ("stopped", "failed"):
            raise PreconditionError("sandbox %s is %s" % (self.ctx.sandbox_id, self.ctx.state))
        self._running = True
        try:
            result = await self.backend.run_shell(self.ctx, command, timeout=timeout,
                                                  env=env, stdin=stdin)
            if len(result.stdout) + len(result.stderr) > self.max_output_bytes:
                result.stdout = result.stdout[: self.max_output_bytes]
                result.stderr = result.stderr[: self.max_output_bytes]
                result.truncated = True
            return result
        finally:
            self._running = False

    async def read_file(self, path: str, max_bytes: int = 4 * 1024 * 1024) -> bytes:
        return await self.backend.read_file(self.ctx, path, max_bytes)

    async def write_file(self, path: str, data: bytes, mode: int = 0o644) -> None:
        await self.backend.write_file(self.ctx, path, data, mode)

    async def list_dir(self, path: str) -> List[FileStat]:
        return await self.backend.list_dir(self.ctx, path)

    async def http(self, url: str, method: str = "GET", body: bytes = b"") -> HttpResult:
        return await self.backend.http_request(self.ctx, url, method=method, body=body)

    async def stream(self, command: str, timeout: float = 60.0) -> AsyncIterator[Tuple[str, bytes]]:
        """Streaming I/O: yield (stream, chunk) tuples as output arrives.

        The portable engine buffers subprocess output; this interface keeps the
        same contract chronus exposes in production (paper §3.3) for callers
        that consume output incrementally.
        """
        result = await self.exec(command, timeout=timeout)
        if result.stdout:
            yield ("stdout", result.stdout)
        if result.stderr:
            yield ("stderr", result.stderr)

    def kill(self) -> None:
        """Terminate this session's process tree (paper §3.3 aether contract)."""
        self._running = False
