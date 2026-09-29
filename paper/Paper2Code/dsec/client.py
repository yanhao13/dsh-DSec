"""libdsec: the unified Python SDK for DSec (paper §2.1).

libdsec gives users one entry point for creating and operating sandboxes while
requiring them to choose the backend appropriate for the task — the backends
have different startup costs, isolation boundaries, and OS capabilities, and
the SDK intentionally does not hide that. A typical request specifies the
sandbox type, image or environment identifier, CPU and memory limits, lifetime
settings, network rules, and the initial user context (Listing 1).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .types import (
    BACKEND_CONTAINER,
    BACKEND_FNCALL,
    BACKEND_FULLVM,
    BACKEND_MICROVM,
    QOS_BEST_EFFORT,
    QOS_LATENCY_SENSITIVE,
    FileStat,
    HttpResult,
    LayerRef,
    NetworkRules,
    ResourceLimits,
    RunResult,
    SandboxSpec,
)


@dataclass
class DSecRunArgs:
    """Common creation arguments (Listing 1 of the paper)."""

    image: str = ""
    memory_limit_mb: int = 512
    cpu_cores_limit: float = 1.0
    ttl_running_stop: float = 300.0  # idle timeout
    ttl_absolute: float = 3600.0
    network_rules: Dict[str, bool] = field(default_factory=dict)
    init_user: str = "root"
    qos: str = QOS_LATENCY_SENSITIVE
    project: str = "root"
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class DSecContainerRunArgs(DSecRunArgs):
    """Container backend arguments (paper Listing 1)."""

    container_image: str = ""
    workspace: Optional[LayerRef] = None
    toolkits: List[LayerRef] = field(default_factory=list)

    def to_spec(self) -> SandboxSpec:
        return SandboxSpec(
            backend=BACKEND_CONTAINER,
            image=self.container_image or self.image,
            workspace=self.workspace,
            toolkits=self.toolkits,
            limits=ResourceLimits(memory_limit_mb=self.memory_limit_mb,
                                  cpu_cores_limit=self.cpu_cores_limit),
            ttl_running_stop=self.ttl_running_stop,
            ttl_absolute=self.ttl_absolute,
            network=NetworkRules(allow=dict(self.network_rules)),
            init_user=self.init_user,
            qos=self.qos,
            project=self.project,
            labels=dict(self.labels),
        )


@dataclass
class DSecMicroVMRunArgs(DSecRunArgs):
    """MicroVM backend arguments; storage/memory knobs per paper §5.2/§5.3."""

    base_image: str = ""
    workspace: Optional[LayerRef] = None
    toolkits: List[LayerRef] = field(default_factory=list)
    pmem_dax: bool = True  # virtio-pmem with DAX
    balloon_fpr: bool = True  # DAMON + balloon free-page reporting

    def to_spec(self) -> SandboxSpec:
        labels = dict(self.labels)
        labels["pmem_dax"] = "1" if self.pmem_dax else "0"
        labels["balloon_fpr"] = "1" if self.balloon_fpr else "0"
        return SandboxSpec(
            backend=BACKEND_MICROVM,
            image=self.base_image or self.image,
            workspace=self.workspace,
            toolkits=self.toolkits,
            limits=ResourceLimits(memory_limit_mb=self.memory_limit_mb,
                                  cpu_cores_limit=self.cpu_cores_limit),
            ttl_running_stop=self.ttl_running_stop,
            ttl_absolute=self.ttl_absolute,
            network=NetworkRules(allow=dict(self.network_rules)),
            init_user=self.init_user,
            qos=self.qos,
            project=self.project,
            labels=labels,
        )


@dataclass
class DSecFnCallRunArgs:
    """FnCall backend arguments (paper §2.2: stateless task execution)."""

    task_type: str = "shell"
    gpu: bool = False
    gpu_mode: str = "shared"  # shared | exclusive
    project: str = "root"
    labels: Dict[str, str] = field(default_factory=dict)
    timeout: float = 60.0

    def to_spec(self) -> SandboxSpec:
        return SandboxSpec(
            backend=BACKEND_FNCALL,
            image="fncall:%s" % self.task_type,
            limits=ResourceLimits(memory_limit_mb=256, cpu_cores_limit=0.5),
            ttl_running_stop=60.0,
            ttl_absolute=600.0,
            network=NetworkRules(allow={}),
            qos=QOS_BEST_EFFORT,
            project=self.project,
            labels=dict(self.labels),
            gpu=self.gpu,
            gpu_mode=self.gpu_mode,
        )


@dataclass
class DSecFullVMRunArgs(DSecRunArgs):
    """Full VM backend arguments (paper §2.2: prepared VM image/snapshot)."""

    vm_image: str = ""

    def to_spec(self) -> SandboxSpec:
        return SandboxSpec(
            backend=BACKEND_FULLVM,
            image=self.vm_image or self.image,
            limits=ResourceLimits(memory_limit_mb=self.memory_limit_mb,
                                  cpu_cores_limit=self.cpu_cores_limit),
            ttl_running_stop=self.ttl_running_stop,
            ttl_absolute=self.ttl_absolute,
            network=NetworkRules(allow=dict(self.network_rules)),
            init_user=self.init_user,
            qos=self.qos,
            project=self.project,
            labels=dict(self.labels),
        )


class Sandbox:
    """A live sandbox session handle (paper §2.3 lifecycle)."""

    def __init__(self, client: "DSecClient", sandbox_id: str, backend: str,
                 terminal_id: str, token: str, timeout: float = 60.0):
        self.client = client
        self.sandbox_id = sandbox_id
        self.backend = backend
        self.terminal_id = terminal_id
        self.token = token
        self.timeout = timeout

    async def run_shell(self, command: str, *, timeout: float = None,
                        env: Optional[Dict[str, str]] = None,
                        stdin: bytes = b"") -> RunResult:
        """Execute a shell command; state persists across calls (§2.3)."""
        if timeout is None:
            timeout = self.timeout
        return await self.client.server.run(self.sandbox_id, self.terminal_id, self.token,
                                            command, timeout=timeout, env=env, stdin=stdin)

    async def run_tool(self, tool_name: str, args: Dict[str, str],
                       timeout: float = 60.0) -> RunResult:
        """Tool-call convenience: renders a shell invocation of the tool."""
        quoted = " ".join('%s="%s"' % (k, v.replace('"', '\\"')) for k, v in args.items())
        return await self.run_shell("%s %s" % (tool_name, quoted), timeout=timeout)

    async def read_file(self, path: str, max_bytes: int = 4 * 1024 * 1024) -> bytes:
        return await self.client.server.read_file(self.sandbox_id, self.terminal_id,
                                                  self.token, path, max_bytes)

    async def write_file(self, path: str, data: bytes, mode: int = 0o644) -> None:
        await self.client.server.write_file(self.sandbox_id, self.terminal_id, self.token,
                                            path, data, mode)

    async def list_dir(self, path: str = "") -> List[FileStat]:
        return await self.client.server.list_dir(self.sandbox_id, self.terminal_id,
                                                 self.token, path)

    async def http(self, url: str, method: str = "GET", body: bytes = b"") -> HttpResult:
        """Outbound HTTP through the sandbox proxy (network allowlist applies)."""
        return await self.client.server.http(self.sandbox_id, self.terminal_id, self.token,
                                             url, method, body)

    async def pack_diff(self, name: str, version: str, *, clean: bool = True) -> LayerRef:
        """Incremental snapshot -> reusable environment layer (paper §6.1)."""
        from .rl.packdiff import pack_diff

        ref = await pack_diff(self, name, version, clean=clean)
        return ref

    async def pause(self) -> None:
        """Suspend while preserving execution state (paper §6.3)."""
        await self.client.server.pause(self.client.principal, self.sandbox_id)

    async def resume(self) -> None:
        await self.client.server.resume(self.client.principal, self.sandbox_id)

    async def stop(self) -> None:
        """Release the sandbox explicitly (paper §2.3)."""
        await self.client.server.stop_sandbox(self.client.principal, self.sandbox_id)

    @property
    def state(self) -> str:
        return self.client.server.state(self.sandbox_id)


class DSecClient:
    """libdsec entry point: connect, create sandboxes of any backend, operate."""

    def __init__(self, server=None, principal: str = "user"):
        self.server = server
        self.principal = principal
        self._open = False

    async def open(self) -> None:
        """Connect to the service endpoint."""
        if self.server is None:
            raise ValueError("DSecClient requires a server (set `server=`)")
        await self.server.start() if hasattr(self.server, "start") else None
        self._open = True

    async def close(self) -> None:
        if self._open:
            await self.server.stop() if hasattr(self.server, "stop") else None
            self._open = False

    async def _create(self, spec: SandboxSpec) -> Sandbox:
        sandbox_id, terminal_id, token = await self.server.create_sandbox(self.principal, spec)
        return Sandbox(self, sandbox_id, spec.backend, terminal_id, token)

    async def run_container(self, args: DSecContainerRunArgs, timeout: float = 120.0) -> Sandbox:
        return await self._create(args.to_spec())

    async def run_microvm(self, args: DSecMicroVMRunArgs, timeout: float = 120.0) -> Sandbox:
        return await self._create(args.to_spec())

    async def run_fncall(self, args: DSecFnCallRunArgs) -> Sandbox:
        sandbox = await self._create(args.to_spec())
        sandbox.timeout = args.timeout
        return sandbox
    async def run_fullvm(self, args: DSecFullVMRunArgs, timeout: float = 120.0) -> Sandbox:
        return await self._create(args.to_spec())

    async def attach(self, sandbox_id: str, terminal_id: str = "", token: str = "") -> Sandbox:
        """Reconnect to an existing sandbox (worker-container reattach, §6.2)."""
        if not terminal_id:
            terminal_id, token = await self.server.open_session(sandbox_id)
        return Sandbox(self, sandbox_id, "", terminal_id, token)
