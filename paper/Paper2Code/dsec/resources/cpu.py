"""QoS-aware CPU scheduling (paper §5.2, §8.5).

Agent sandboxes spend most of their lives waiting for the model, so DSec
overcommits CPU heavily. The risk is SMT-level interference: a latency-sensitive
(LS) thread contending with best-effort (BE) work on its sibling hardware
thread. DSec applies a two-layer policy:

1. BE sandboxes run under SCHED_IDLE, so they yield whenever an LS task is
   runnable;
2. LS sandboxes get core-scheduling cookies (prctl PR_SCHED_CORE), preventing
   unrelated BE work from running on the sibling thread of the same physical
   core.

In the paper, this reduces SMT-induced per-step latency inflation from 45.2%
to 17.3% at 50% background load. Linux hosts get the real kernel mechanisms;
other hosts get a deterministic contention model calibrated to those anchors.
"""
from __future__ import annotations

import ctypes
import ctypes.util
import os
import platform
from typing import Dict, Optional

from ..types import QOS_BEST_EFFORT, QOS_LATENCY_SENSITIVE

IS_LINUX = platform.system() == "Linux"

# Linux sched(7): SCHED_IDLE is priority class 5.
SCHED_IDLE = 5

# prctl(PR_SCHED_CORE) — kernel core scheduling (paper §5.2).
_PR_SCHED_CORE = 62
_PR_SCHED_CORE_CREATE = 1
_PR_SCHED_CORE_SCOPE_THREAD_GROUP = 1
_PROCESS_COOKIE_SEED = 1


class CpuQoS:
    """Assigns sandboxes to LS/BE classes and applies the two-layer policy."""

    def __init__(self, physical_cores: int = 4, smt_threads: int = 2, os_enforce: bool = True):
        self.physical_cores = physical_cores
        self.smt_threads = smt_threads
        self.os_enforce = os_enforce and IS_LINUX
        self.assignments: Dict[str, str] = {}
        self.cookies: Dict[str, int] = {}
        self._next_cookie = _PROCESS_COOKIE_SEED + 1

    def assign(self, sandbox_id: str, qos_class: str) -> None:
        self.assignments[sandbox_id] = qos_class

    def release(self, sandbox_id: str) -> None:
        self.assignments.pop(sandbox_id, None)
        self.cookies.pop(sandbox_id, None)

    def cookie_for(self, sandbox_id: str) -> Optional[int]:
        """Core-scheduling cookie for an LS sandbox's process tree."""
        if self.assignments.get(sandbox_id) != QOS_LATENCY_SENSITIVE:
            return None
        if sandbox_id not in self.cookies:
            self.cookies[sandbox_id] = self._next_cookie
            self._next_cookie += 1
        return self.cookies[sandbox_id]

    def preexec_fn(self, sandbox_id: str):
        """preexec_fn for subprocess.Popen: applies the child's QoS class."""

        def apply() -> None:
            qos = self.assignments.get(sandbox_id, QOS_LATENCY_SENSITIVE)
            if qos == QOS_BEST_EFFORT:
                self._set_sched_idle()
            cookie = self.cookie_for(sandbox_id)
            if cookie is not None:
                self._set_core_sched_cookie(cookie)

        return apply

    # -- real kernel mechanisms (Linux only) -------------------------------------
    def _set_sched_idle(self) -> None:
        if not self.os_enforce:
            return
        libc = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6", use_errno=True)

        class _SchedParam(ctypes.Structure):
            _fields_ = [("sched_priority", ctypes.c_int)]

        param = _SchedParam(0)
        try:
            rc = libc.sched_setscheduler(0, SCHED_IDLE, ctypes.byref(param))
            if rc != 0:
                pass  # kernel without SCHED_IDLE support; degrade silently
        except Exception:
            pass

    def _set_core_sched_cookie(self, cookie: int) -> None:
        if not self.os_enforce:
            return
        libc = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6", use_errno=True)
        try:
            libc.prctl(_PR_SCHED_CORE, _PR_SCHED_CORE_CREATE, 0,
                       _PR_SCHED_CORE_SCOPE_THREAD_GROUP, cookie)
        except Exception:
            pass

    # -- deterministic contention model (anchored to paper §8.5) -------------------
    # Fig. 13 anchors at 50% background load: unprotected 45.2%, SCHED_IDLE
    # alone 41.8% (improves by at most 3.4%), SCHED_IDLE + core scheduling
    # 17.3%. Linear in load, matching the paper's curve shape.
    _SLOPES = {
        "baseline": 0.904,
        "sched_idle": 0.836,
        "idle_core": 0.346,
    }

    def latency_inflation(self, be_load_fraction: float, protection: str = "baseline") -> float:
        """Modeled per-step latency inflation under co-located BE load."""
        slope = self._SLOPES.get(protection, self._SLOPES["baseline"])
        return slope * min(max(be_load_fraction, 0.0), 0.5)

    def smt_contention_saved(self, be_load_fraction: float) -> float:
        """Inflation avoided by core scheduling vs SCHED_IDLE alone."""
        return self.latency_inflation(be_load_fraction, "sched_idle") - self.latency_inflation(
            be_load_fraction, "idle_core"
        )
