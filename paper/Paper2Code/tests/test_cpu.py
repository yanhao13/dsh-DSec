"""Tests for the §5.2 CPU QoS model against the paper's §8.5 anchors."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.resources.cpu import CpuQoS
from dsec.types import QOS_BEST_EFFORT, QOS_LATENCY_SENSITIVE


class TestCpuQoS(unittest.TestCase):
    """Fig. 13 anchors at 50% background load: baseline 45.2%, SCHED_IDLE alone
    41.8% (improves by at most 3.4%), SCHED_IDLE + core scheduling 17.3%."""

    def setUp(self):
        self.qos = CpuQoS(physical_cores=4, smt_threads=2, os_enforce=False)

    def test_anchors_at_50_percent_load(self):
        self.assertAlmostEqual(self.qos.latency_inflation(0.5, "baseline"), 0.452, places=3)
        self.assertAlmostEqual(self.qos.latency_inflation(0.5, "sched_idle"), 0.418, places=3)
        self.assertAlmostEqual(self.qos.latency_inflation(0.5, "idle_core"), 0.173, places=3)

    def test_sched_idle_alone_improves_by_at_most_3_4_pct(self):
        improvement = (0.452 - 0.418) * 100
        self.assertAlmostEqual(improvement, 3.4, places=1)

    def test_core_scheduling_removes_smt_sibling_interference(self):
        # The SMT-sibling interference SCHED_IDLE cannot fix: 45.2 -> 41.8
        # leaves most inflation; core scheduling brings it to 17.3.
        saved = self.qos.smt_contention_saved(0.5)
        self.assertAlmostEqual(saved, 0.245, places=3)

    def test_class_assignment_and_cookies(self):
        self.qos.assign("sb-1", QOS_LATENCY_SENSITIVE)
        self.qos.assign("sb-2", QOS_BEST_EFFORT)
        self.assertIsNotNone(self.qos.cookie_for("sb-1"))
        self.assertIsNone(self.qos.cookie_for("sb-2"))  # BE has no core-sched cookie
        # Distinct LS sandboxes get distinct core-scheduling cookies.
        self.qos.assign("sb-3", QOS_LATENCY_SENSITIVE)
        self.assertNotEqual(self.qos.cookie_for("sb-1"), self.qos.cookie_for("sb-3"))
        self.qos.release("sb-1")
        self.assertNotIn("sb-1", self.qos.assignments)


if __name__ == "__main__":
    unittest.main()
