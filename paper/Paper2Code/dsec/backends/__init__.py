"""Sandbox backends exposed through the unified SDK (paper §2.2, §3.3)."""
from .base import Backend, SandboxContext, SandboxState
from .process import ProcessEngine, ProcessBackend
from .fncall import FnCallBackend, FnCallPool
from .container import ContainerBackend
from .microvm import MicroVMBackend
from .fullvm import FullVMBackend

__all__ = [
    "Backend",
    "SandboxContext",
    "SandboxState",
    "ProcessEngine",
    "ProcessBackend",
    "FnCallBackend",
    "FnCallPool",
    "ContainerBackend",
    "MicroVMBackend",
    "FullVMBackend",
]
