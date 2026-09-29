"""High-density resource management (paper §5.2)."""
from .cpu import CpuQoS
from .memory import MemoryManager, firecracker_workload, reductions

__all__ = ["CpuQoS", "MemoryManager", "firecracker_workload", "reductions"]
