"""Sandbox placement: filter then power-of-k-choices ranking (paper §3.2, §7).

Placement proceeds in two stages. Filtering retains only healthy nodes that
provide the backend and hardware capabilities required by the request (e.g.
GPU-enabled sandboxes are restricted to GPU nodes). Ranking randomly samples k
eligible nodes and selects the least loaded, avoiding herding under bursty RL
environment creation.

Each placement-engine instance keeps a local view overlaying its own recent
placements that are not yet reflected in the periodic watcher snapshots,
accounting for in-flight load without cross-instance coordination. The edge
retains final admission authority: stale estimates never override local
resource limits (§7).
"""
from __future__ import annotations

import random
from typing import Dict, List, Optional

from .errors import AdmissionError
from .types import SandboxSpec
from .watcher import EdgeStats, FleetView


class PlacementEngine:
    """Filter/rank placement over the watcher's fleet view."""

    def __init__(self, watcher, sample_k: int = 2, rng: Optional[random.Random] = None):
        self.watcher = watcher
        self.sample_k = max(sample_k, 1)
        self.rng = rng or random.Random()
        # Per-instance overlay of in-flight placements not yet visible in the
        # periodic watcher snapshot (paper §7). No cross-instance coordination.
        self._in_flight: Dict[str, float] = {}  # edge_id -> synthetic load units
        self.placements = 0
        self.rejections = 0

    def _view(self) -> FleetView:
        return self.watcher.fleet

    def filter_nodes(self, spec: SandboxSpec, view: Optional[FleetView] = None) -> List[EdgeStats]:
        """Healthy nodes providing the required backend and capabilities."""
        view = view or self._view()
        out: List[EdgeStats] = []
        for stats in view.healthy_edges().values():
            if spec.backend not in stats.backends:
                continue
            if spec.gpu and stats.gpu_instances <= stats.gpu_used:
                continue
            out.append(stats)
        return out

    def load_score(self, stats: EdgeStats, spec: SandboxSpec) -> float:
        """Composite load: CPU, memory, running sandboxes, GPU pressure."""
        cpu_pressure = stats.cpu_used / max(stats.cpu_capacity, 1e-9)
        mem_pressure = stats.mem_used_mb / max(stats.mem_capacity_mb, 1e-9)
        count_pressure = sum(stats.running.values()) / 3200.0  # production container density anchor
        score = 0.5 * cpu_pressure + 0.3 * mem_pressure + 0.2 * count_pressure
        if spec.gpu:
            score += stats.gpu_used / max(stats.gpu_instances, 1)
        # Local overlay of this instance's in-flight placements (§7).
        score += self._in_flight.get(stats.edge_id, 0.0)
        return score

    def place(self, spec: SandboxSpec) -> str:
        """Select an edge for a creation request (power-of-k-choices)."""
        eligible = self.filter_nodes(spec)
        if not eligible:
            self.rejections += 1
            raise AdmissionError("no healthy node provides backend %r" % spec.backend)
        sample = self.rng.sample(eligible, min(self.sample_k, len(eligible)))
        best = min(sample, key=lambda s: self.load_score(s, spec))
        self._in_flight[best.edge_id] = self._in_flight.get(best.edge_id, 0.0) + 1.0 / 3200.0
        self.placements += 1
        return best.edge_id

    def settle(self, edge_id: str) -> None:
        """A placement became visible in the watcher view; drop the overlay."""
        self._in_flight[edge_id] = max(self._in_flight.get(edge_id, 0.0) - 1.0 / 3200.0, 0.0)

    def penalize(self, edge_id: str, units: float = 1000.0) -> None:
        """Temporarily deprioritize a node that rejected a placement (§7).

        Edge-local admission has the final say; when an edge rejects, the next
        placement attempt must select an alternative node.
        """
        self._in_flight[edge_id] = self._in_flight.get(edge_id, 0.0) + units
