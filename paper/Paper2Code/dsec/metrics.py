"""Lightweight metrics registry used by the control plane and demos.

The paper reports platform-scale counters (§2.4) and mechanism-level
measurements (§8): creations per second, memory saved, disk writes avoided,
latency inflation. This module provides the instrumentation those numbers
derive from, without external dependencies.
"""
from __future__ import annotations

import time
from collections import defaultdict
from typing import Dict, List, Tuple


class Metrics:
    """Counters, gauges, and monotonic timers."""

    def __init__(self, name: str = "dsec"):
        self.name = name
        self.counters: Dict[str, float] = defaultdict(float)
        self.gauges: Dict[str, float] = {}
        self._series: Dict[str, List[Tuple[float, float]]] = defaultdict(list)
        self._start = time.monotonic()

    # -- counters -----------------------------------------------------------
    def inc(self, key: str, amount: float = 1.0) -> None:
        self.counters[key] += amount

    def get(self, key: str) -> float:
        return self.counters.get(key, 0.0)

    # -- gauges --------------------------------------------------------------
    def set(self, key: str, value: float) -> None:
        self.gauges[key] = value

    # -- time series (for peak / time-integrated measurements) ----------------
    def sample(self, key: str, value: float, t: float = None) -> None:
        t = time.monotonic() if t is None else t
        self._series[key].append((t, value))
        self.gauges[key] = value

    def peak(self, key: str) -> float:
        values = [v for _, v in self._series[key]]
        return max(values) if values else 0.0

    def time_integral(self, key: str) -> float:
        """Integrate the sampled series over time (value-seconds)."""
        pts = self._series[key]
        if not pts:
            return 0.0
        total = 0.0
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            total += 0.5 * (v0 + v1) * (t1 - t0)
        return total

    def snapshot(self) -> Dict[str, float]:
        out = dict(self.counters)
        out.update({k: v for k, v in self.gauges.items()})
        return out
