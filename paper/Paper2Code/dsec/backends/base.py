"""Backend interface and the sandbox context shared with the runtime."""
from __future__ import annotations

import abc
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..types import FileStat, HttpResult, RunResult, SandboxSpec


class SandboxState:
    CREATING = "creating"
    RUNNING = "running"
    PAUSED = "paused"
    SNAPSHOTTED = "snapshotted"
    STOPPED = "stopped"
    FAILED = "failed"


@dataclass
class SandboxContext:
    """Everything the runtime and a backend share about one sandbox."""

    sandbox_id: str
    spec: SandboxSpec
    rootfs_dir: str = ""
    state: str = SandboxState.CREATING
    created_at: float = field(default_factory=time.monotonic)
    last_active: float = field(default_factory=time.monotonic)
    metadata: Dict[str, Any] = field(default_factory=dict)
    metrics: Any = None  # Metrics registry
    cpu_qos: Any = None  # CpuQoS
    memory: Any = None  # MemoryManager
    security: Any = None  # SecurityPolicy
    chunk_cache: Any = None  # ChunkCache (second-level local cache)
    store: Any = None  # RemoteStore (3FS)
    guest_mem_id: Optional[str] = None

    def touch(self) -> None:
        self.last_active = time.monotonic()

    def set_state(self, state: str) -> None:
        self.state = state


class Backend(abc.ABC):
    """A sandbox backend: FnCall, container, microVM, or full VM.

    Backends differ in startup cost, isolation, filesystem semantics, and OS
    capabilities (paper §2.2). The SDK intentionally does not hide these
    differences: callers pick the backend matching the workload.
    """

    name = "abstract"

    # -- lifecycle ------------------------------------------------------------
    @abc.abstractmethod
    async def create(self, ctx: SandboxContext) -> None:
        """Provision storage, apply policy, and bring the sandbox up."""

    @abc.abstractmethod
    async def destroy(self, ctx: SandboxContext) -> None:
        """Release the sandbox and all node-local resources (paper §2.3)."""

    # -- operations -----------------------------------------------------------
    @abc.abstractmethod
    async def run_shell(self, ctx: SandboxContext, command: str, *,
                        timeout: float = 60.0, env: Optional[Dict[str, str]] = None,
                        stdin: bytes = b"") -> RunResult:
        """Execute a shell command; the sandbox state persists across calls."""

    async def read_file(self, ctx: SandboxContext, path: str, max_bytes: int) -> bytes:
        raise NotImplementedError

    async def write_file(self, ctx: SandboxContext, path: str, data: bytes, mode: int) -> None:
        raise NotImplementedError

    async def list_dir(self, ctx: SandboxContext, path: str) -> List[FileStat]:
        raise NotImplementedError

    async def http_request(self, ctx: SandboxContext, url: str, method: str = "GET",
                           body: bytes = b"") -> HttpResult:
        raise NotImplementedError

    # -- state preservation (paper §6.1, §6.3) -----------------------------------
    async def snapshot(self, ctx: SandboxContext) -> Dict[str, Any]:
        """Serialize execution state (pack_diff / pause)."""
        raise NotImplementedError

    async def restore(self, ctx: SandboxContext, snapshot: Dict[str, Any]) -> None:
        raise NotImplementedError

    async def pause(self, ctx: SandboxContext) -> None:
        raise NotImplementedError

    async def resume(self, ctx: SandboxContext) -> None:
        raise NotImplementedError
