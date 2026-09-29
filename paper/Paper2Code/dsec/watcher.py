"""Cluster health and load monitoring (paper §3.2).

The watcher periodically probes the health of each edge and host and collects
scheduling-relevant state: running sandboxes across backend types, broken down
per edge, per user, and per task. Neither the watcher nor the placement engine
requires durable state — the watcher can rebuild its fleet view after a restart
by polling the edges again.
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class EdgeStats:
    edge_id: str = ""
    healthy: bool = True
    running: Dict[str, int] = field(default_factory=dict)  # backend -> count
    per_user: Dict[str, int] = field(default_factory=dict)
    per_task: Dict[str, int] = field(default_factory=dict)
    cpu_used: float = 0.0
    cpu_capacity: float = 1.0
    mem_used_mb: float = 0.0
    mem_capacity_mb: float = 1.0
    gpu_instances: int = 0
    gpu_used: int = 0
    backends: List[str] = field(default_factory=list)
    cloud: bool = False
    last_seen: float = 0.0


@dataclass
class FleetView:
    generation: int = 0
    edges: Dict[str, EdgeStats] = field(default_factory=dict)
    collected_at: float = 0.0

    def healthy_edges(self) -> Dict[str, EdgeStats]:
        return {e: s for e, s in self.edges.items() if s.healthy}


class Watcher:
    """Polls registered edges and publishes fleet snapshots."""

    def __init__(self, probe_interval: float = 5.0):
        self.probe_interval = probe_interval
        self._edges: Dict[str, object] = {}
        self._view = FleetView()
        self._generation = 0
        self._task: Optional[asyncio.Task] = None
        self._probes = 0

    def register_edge(self, edge) -> None:
        self._edges[edge.edge_id] = edge

    def unregister_edge(self, edge_id: str) -> None:
        self._edges.pop(edge_id, None)

    async def start(self) -> None:
        if self._task is None:
            self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        if self._task is not None:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def _run(self) -> None:
        while True:
            await self.collect_once()
            await asyncio.sleep(self.probe_interval)

    async def collect_once(self) -> None:
        """Poll every edge and rebuild the fleet view from scratch."""
        stats: Dict[str, EdgeStats] = {}
        for edge_id, edge in self._edges.items():
            stats[edge_id] = edge.stats()
        self._generation += 1
        self._view = FleetView(
            generation=self._generation,
            edges=stats,
            collected_at=time.monotonic(),
        )
        self._probes += 1

    @property
    def fleet(self) -> FleetView:
        return self._view

    def set_view(self, view: FleetView) -> None:
        """Replace the fleet snapshot (tests, or a forced rebuild)."""
        self._view = view

    @property
    def probes(self) -> int:
        return self._probes
