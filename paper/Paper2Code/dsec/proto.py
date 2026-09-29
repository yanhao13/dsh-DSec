"""Wire protocol between libdsec and the apiserver (paper §3.2 ingress path).

Requests are plain JSON objects with base64-encoded binary fields. The
in-process transport uses these same codecs so the SDK is transport-agnostic.
"""
from __future__ import annotations

import base64
import json
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

from .types import LayerRef, NetworkRules, ResourceLimits, SandboxSpec


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64decode(text: str) -> bytes:
    return base64.b64decode(text.encode("ascii"))


@dataclass
class CreateRequest:
    spec: SandboxSpec
    principal: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"spec": _spec_to_dict(self.spec), "principal": self.principal}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CreateRequest":
        return cls(spec=_spec_from_dict(d["spec"]), principal=d.get("principal", ""))


@dataclass
class CreateResponse:
    sandbox_id: str = ""
    backend: str = ""
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "CreateResponse":
        return cls(**d)


@dataclass
class ExecRequest:
    sandbox_id: str
    command: str
    timeout: float = 60.0
    env: Dict[str, str] = field(default_factory=dict)
    stdin: bytes = b""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sandbox_id": self.sandbox_id,
            "command": self.command,
            "timeout": self.timeout,
            "env": self.env,
            "stdin": _b64encode(self.stdin),
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ExecRequest":
        return cls(
            sandbox_id=d["sandbox_id"],
            command=d["command"],
            timeout=d.get("timeout", 60.0),
            env=d.get("env", {}),
            stdin=_b64decode(d.get("stdin", "")),
        )


@dataclass
class ExecResponse:
    exit_code: int = 0
    stdout: bytes = b""
    stderr: bytes = b""
    truncated: bool = False
    duration_ms: float = 0.0
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exit_code": self.exit_code,
            "stdout": _b64encode(self.stdout),
            "stderr": _b64encode(self.stderr),
            "truncated": self.truncated,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ExecResponse":
        return cls(
            exit_code=d.get("exit_code", 0),
            stdout=_b64decode(d.get("stdout", "")),
            stderr=_b64decode(d.get("stderr", "")),
            truncated=d.get("truncated", False),
            duration_ms=d.get("duration_ms", 0.0),
            error=d.get("error", ""),
        )


@dataclass
class FileReadRequest:
    sandbox_id: str
    path: str
    max_bytes: int = 4 * 1024 * 1024

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FileReadRequest":
        return cls(**d)


@dataclass
class FileReadResponse:
    content: bytes = b""
    truncated: bool = False
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"content": _b64encode(self.content), "truncated": self.truncated, "error": self.error}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FileReadResponse":
        return cls(content=_b64decode(d.get("content", "")), truncated=d.get("truncated", False), error=d.get("error", ""))


@dataclass
class FileWriteRequest:
    sandbox_id: str
    path: str
    content: bytes
    mode: int = 0o644

    def to_dict(self) -> Dict[str, Any]:
        return {"sandbox_id": self.sandbox_id, "path": self.path, "content": _b64encode(self.content), "mode": self.mode}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "FileWriteRequest":
        return cls(sandbox_id=d["sandbox_id"], path=d["path"], content=_b64decode(d["content"]), mode=d.get("mode", 0o644))


@dataclass
class OkResponse:
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "OkResponse":
        return cls(**d)


@dataclass
class ListRequest:
    principal: str = ""
    project: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ListRequest":
        return cls(**d)


@dataclass
class SandboxInfo:
    sandbox_id: str
    backend: str
    state: str
    project: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SandboxInfo":
        return cls(**d)


@dataclass
class ListResponse:
    sandboxes: List[SandboxInfo] = field(default_factory=list)
    error: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"sandboxes": [s.to_dict() for s in self.sandboxes], "error": self.error}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ListResponse":
        return cls(sandboxes=[SandboxInfo.from_dict(s) for s in d.get("sandboxes", [])], error=d.get("error", ""))


def _spec_to_dict(spec: SandboxSpec) -> Dict[str, Any]:
    d = asdict(spec)
    d["network"] = {"allow": spec.network.allow}
    return d


def _spec_from_dict(d: Dict[str, Any]) -> SandboxSpec:
    limits = ResourceLimits(**d.get("limits", {}))
    network = NetworkRules(allow=d.get("network", {}).get("allow", {}))
    workspace = d.get("workspace")
    if isinstance(workspace, dict):
        workspace = LayerRef(**workspace)
    toolkits = [LayerRef(**t) if isinstance(t, dict) else t for t in d.get("toolkits", [])]
    return SandboxSpec(
        backend=d["backend"],
        image=d["image"],
        workspace=workspace,
        toolkits=toolkits,
        limits=limits,
        ttl_running_stop=d.get("ttl_running_stop", 300.0),
        ttl_absolute=d.get("ttl_absolute", 3600.0),
        network=network,
        init_user=d.get("init_user", "root"),
        qos=d.get("qos", "LS"),
        project=d.get("project", ""),
        labels=d.get("labels", {}),
        gpu=d.get("gpu", False),
        gpu_mode=d.get("gpu_mode", "shared"),
    )


def encode(obj: Any) -> bytes:
    """Serialize any request/response dataclass to wire bytes."""
    return json.dumps(obj.to_dict()).encode("utf-8")


def decode(data: bytes, cls: type) -> Any:
    """Deserialize wire bytes into a request/response dataclass."""
    return cls.from_dict(json.loads(data.decode("utf-8")))
