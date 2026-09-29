"""Request/response types shared across the SDK, control plane, and runtime."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# Backend kinds (paper §2.2). FnCall is a separate execution path (§3.1).
BACKEND_FNCALL = "fncall"
BACKEND_CONTAINER = "container"
BACKEND_MICROVM = "microvm"
BACKEND_FULLVM = "fullvm"
BACKENDS = (BACKEND_FNCALL, BACKEND_CONTAINER, BACKEND_MICROVM, BACKEND_FULLVM)

# CPU QoS classes (paper §5.2).
QOS_LATENCY_SENSITIVE = "LS"
QOS_BEST_EFFORT = "BE"


@dataclass
class ResourceLimits:
    """Per-sandbox resource limits (Listing 1 of the paper)."""

    memory_limit_mb: int = 512
    cpu_cores_limit: float = 1.0
    disk_limit_mb: int = 1024


@dataclass
class NetworkRules:
    """Task-specific network permissions by service/mirror (paper §6.5, Listing 1).

    ``allow`` maps a service name (e.g. ``"pypi"``, ``"npm"``, ``"github"``) to
    whether it is reachable. Hosts not covered by any rule are denied by default
    (deny-by-default allowlist).
    """

    allow: Dict[str, bool] = field(default_factory=dict)

    def clone(self) -> "NetworkRules":
        return NetworkRules(allow=dict(self.allow))

    def allowed_service(self, service: str) -> bool:
        return bool(self.allow.get(service, False))

    def update(self, rules: Dict[str, bool]) -> "NetworkRules":
        """Dynamic policy update as tasks move between stages (paper §6.5)."""
        out = self.clone()
        out.allow.update(rules)
        return out


@dataclass
class LayerRef:
    """Reference to an independently versioned environment layer (paper §5.1)."""

    name: str
    version: str
    kind: str  # "base" | "workspace" | "toolkit"


@dataclass
class SandboxSpec:
    """Fully resolved creation request (paper §2.1, §2.3)."""

    backend: str
    image: str  # base image / environment identifier
    workspace: Optional[LayerRef] = None
    toolkits: List[LayerRef] = field(default_factory=list)
    limits: ResourceLimits = field(default_factory=ResourceLimits)
    ttl_running_stop: float = 300.0  # idle timeout, seconds (paper §2.1)
    ttl_absolute: float = 3600.0  # hard lifetime, seconds (paper §2.3)
    network: NetworkRules = field(default_factory=NetworkRules)
    init_user: str = "root"
    qos: str = QOS_LATENCY_SENSITIVE
    project: str = ""
    labels: Dict[str, str] = field(default_factory=dict)
    gpu: bool = False
    gpu_mode: str = "shared"  # "shared" | "exclusive" (paper §2.2 FnCall)

    def required_backend_capability(self) -> str:
        return "gpu" if self.gpu else "cpu"


@dataclass
class RunResult:
    """Outcome of a shell command or tool call inside a sandbox."""

    exit_code: int
    stdout: bytes = b""
    stderr: bytes = b""
    truncated: bool = False
    duration_ms: float = 0.0

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.truncated

    def text(self, stream: str = "stdout") -> str:
        data = self.stdout if stream == "stdout" else self.stderr
        return data.decode("utf-8", "replace")


@dataclass
class FileStat:
    name: str
    size: int
    is_dir: bool
    mode: int = 0o644


@dataclass
class HttpResult:
    status: int
    body: bytes = b""
    headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class FnCallTask:
    """Task specification for the FnCall backend (paper §2.2)."""

    task_type: str
    command: str  # code or script to run
    files: Dict[str, bytes] = field(default_factory=dict)  # dependency files
    timeout: float = 60.0
    gpu: bool = False
    gpu_mode: str = "shared"


@dataclass
class NodeCapacity:
    """Static hardware capacity of an edge node (paper §3.3 admission)."""

    cpu_cores: float = 8.0
    memory_mb: int = 8192
    disk_mb: int = 20 * 1024
    max_sandboxes: int = 256
    backends: List[str] = field(default_factory=lambda: list(BACKENDS))
    gpu_instances: int = 0  # MIG partitions if GPU-equipped (paper §7)


@dataclass
class DiffEntry:
    """One changed file in a snapshot diff (paper §6.1 pack_diff)."""

    path: str
    op: str  # "add" | "modify" | "delete" (whiteout)
    content: Optional[bytes] = None
    size: int = 0
