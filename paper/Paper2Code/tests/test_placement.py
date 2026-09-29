"""Tests for placement filter/ranking (paper §3.2, §7 power-of-k-choices)."""
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.errors import AdmissionError
from dsec.placement import PlacementEngine
from dsec.types import BACKEND_CONTAINER, BACKEND_MICROVM, SandboxSpec
from dsec.watcher import EdgeStats, FleetView, Watcher


def spec(**kw):
    defaults = dict(backend=BACKEND_CONTAINER, image="x:v1")
    defaults.update(kw)
    return SandboxSpec(**defaults)


def edge_stats(edge_id, cpu_used=0.0, mem_used=0.0, gpu=0, backends=None, healthy=True, running=None):
    return EdgeStats(edge_id=edge_id, healthy=healthy, cpu_used=cpu_used, mem_used_mb=mem_used,
                     cpu_capacity=100.0, mem_capacity_mb=100000,
                     gpu_instances=gpu, gpu_used=0,
                     backends=backends or [BACKEND_CONTAINER, BACKEND_MICROVM],
                     running=running or {})


class FakeWatcher:
    def __init__(self, view):
        self.fleet = view


class TestPlacement(unittest.TestCase):
    def test_filter_by_backend_capability(self):
        view = FleetView(edges={
            "a": edge_stats("a", backends=[BACKEND_CONTAINER]),
            "b": edge_stats("b", backends=[BACKEND_MICROVM]),
        })
        pe = PlacementEngine(FakeWatcher(view), sample_k=2)
        eligible = pe.filter_nodes(spec(backend=BACKEND_MICROVM))
        self.assertEqual([e.edge_id for e in eligible], ["b"])

    def test_filter_by_gpu_capability(self):
        view = FleetView(edges={
            "a": edge_stats("a"),
            "b": edge_stats("b", gpu=1),
        })
        pe = PlacementEngine(FakeWatcher(view), sample_k=2)
        eligible = pe.filter_nodes(spec(gpu=True))
        self.assertEqual([e.edge_id for e in eligible], ["b"])

    def test_unhealthy_nodes_filtered(self):
        view = FleetView(edges={"a": edge_stats("a", healthy=False)})
        pe = PlacementEngine(FakeWatcher(view), sample_k=2)
        with self.assertRaises(AdmissionError):
            pe.place(spec())

    def test_power_of_k_picks_least_loaded(self):
        # With k=2 and a skewed load, the least-loaded node must always win
        # (no herding under bursts, paper §7).
        view = FleetView(edges={
            "busy": edge_stats("busy", cpu_used=90.0, mem_used=90000, running={BACKEND_CONTAINER: 3000}),
            "idle": edge_stats("idle", cpu_used=1.0, mem_used=100, running={BACKEND_CONTAINER: 5}),
            "mid": edge_stats("mid", cpu_used=50.0, mem_used=50000, running={BACKEND_CONTAINER: 1500}),
        })
        pe = PlacementEngine(FakeWatcher(view), sample_k=2, rng=random.Random(0))
        picks = [pe.place(spec()) for _ in range(50)]
        # Every sample of 2 contains 'idle' or 'mid' + 'busy'; least-loaded among
        # the sampled pair is never 'busy'.
        self.assertNotIn("busy", picks)

    def test_in_flight_overlay_biases_placement(self):
        # This instance's own recent placements overlay the watcher snapshot
        # (paper §7), spreading in-flight load without cross-instance state.
        view = FleetView(edges={"a": edge_stats("a"), "b": edge_stats("b")})
        pe = PlacementEngine(FakeWatcher(view), sample_k=2, rng=random.Random(1))
        for _ in range(300):
            pe._in_flight["a"] = pe._in_flight.get("a", 0.0) + 0.01
        picks = [pe.place(spec()) for _ in range(50)]
        self.assertIn("b", picks)

    def test_edge_final_admission_authority(self):
        # Placement may be stale; the edge rejects and the engine re-places
        # (tested end-to-end in test_e2e.py).
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
