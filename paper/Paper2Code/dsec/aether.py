"""Aether: the per-sandbox proxy (paper §3.1, §3.3).

Container and VM sandboxes run aether, which establishes a communication
channel with the edge — a Unix domain socket for Linux containers, vsock for VM
backends. The edge monitors sandbox health through this channel and marks the
sandbox failed if the channel closes. For each operation, aether uses the
operation's terminal-session identifier to create or locate the corresponding
chronus instance, then forwards the operation over the local channel; when a
session ends, aether terminates the corresponding chronus process tree.

Session identifiers are SDK-issued tokens: an agent forging RPC requests
directly to chronus sockets (paper §6.4) is rejected here because it cannot
produce a valid token.
"""
from __future__ import annotations

import secrets
import time
from typing import Dict, Tuple

from .errors import AccessDenied
from .types import HttpResult, RunResult
from .backends.base import Backend, SandboxContext
from .chronus import ShellSession

TRANSPORT_UNIX_SOCKET = "unix-socket"
TRANSPORT_VSOCK = "vsock"


class Aether:
    """Multiplexes SDK operations onto chronus shell sessions."""

    def __init__(self, sandbox_id: str, ctx: SandboxContext, backend: Backend,
                 transport: str = TRANSPORT_UNIX_SOCKET):
        self.sandbox_id = sandbox_id
        self.ctx = ctx
        self.backend = backend
        self.transport = transport
        self.sessions: Dict[str, ShellSession] = {}
        self.tokens: Dict[str, str] = {}  # terminal_id -> SDK-issued token
        self.alive = True
        self.last_seen = time.monotonic()

    # -- session management -----------------------------------------------------
    def open_session(self, terminal_id: str = "") -> Tuple[str, str]:
        """Create a chronus session; returns (terminal_id, sdk token)."""
        terminal_id = terminal_id or "term-%s" % secrets.token_hex(4)
        if terminal_id in self.sessions:
            return terminal_id, self.tokens[terminal_id]
        token = secrets.token_hex(16)
        self.sessions[terminal_id] = ShellSession(terminal_id, self.ctx, self.backend)
        self.tokens[terminal_id] = token
        self.last_seen = time.monotonic()
        return terminal_id, token

    def _authenticate(self, terminal_id: str, token: str) -> ShellSession:
        """Locate the chronus instance; forged RPCs carry no valid token."""
        session = self.sessions.get(terminal_id)
        if session is None or self.tokens.get(terminal_id) != token:
            if self.ctx.security is not None:
                self.ctx.security.misbehavior.record(
                    self.sandbox_id, "forged-chronus-rpc",
                    "unauthenticated terminal id %r" % terminal_id)
            raise AccessDenied("invalid terminal-session credentials")
        self.last_seen = time.monotonic()
        return session

    def close_session(self, terminal_id: str, token: str) -> None:
        """End a session; aether terminates the chronus process tree (§3.3)."""
        session = self._authenticate(terminal_id, token)
        session.kill()
        self.sessions.pop(terminal_id, None)
        self.tokens.pop(terminal_id, None)

    def close_all(self) -> None:
        for session in self.sessions.values():
            session.kill()
        self.sessions.clear()
        self.tokens.clear()

    # -- operation forwarding ------------------------------------------------------
    async def run(self, terminal_id: str, token: str, command: str, *,
                  timeout: float = 60.0, env=None, stdin: bytes = b"") -> RunResult:
        session = self._authenticate(terminal_id, token)
        return await session.exec(command, timeout=timeout, env=env, stdin=stdin)

    async def read_file(self, terminal_id: str, token: str, path: str, max_bytes: int) -> bytes:
        return await self._authenticate(terminal_id, token).read_file(path, max_bytes)

    async def write_file(self, terminal_id: str, token: str, path: str, data: bytes, mode: int) -> None:
        await self._authenticate(terminal_id, token).write_file(path, data, mode)

    async def list_dir(self, terminal_id: str, token: str, path: str) -> list:
        return await self._authenticate(terminal_id, token).list_dir(path)

    async def http(self, terminal_id: str, token: str, url: str, method: str = "GET",
                   body: bytes = b"") -> HttpResult:
        return await self._authenticate(terminal_id, token).http(url, method=method, body=body)

    def mark_failed(self) -> None:
        """The edge marks the sandbox failed when the channel closes (§3.3)."""
        self.alive = False
        self.ctx.set_state("failed")
