"""Tests for edge admission, TTL reclamation, and watcher stats (paper §3.3)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.errors import AdmissionError
from dsec.types import BACKEND_CONTAINER, NodeCapacity, SandboxSpec
from tests.helpers import ClusterTestCase


class TestEdgeAdmission(ClusterTestCase):
    async def test_sandbox_capacity_rejection(self):
        edge = self.edges["edge-01"]
        edge.capacity.max_sandboxes = 2
        spec = SandboxSpec(backend=BACKEND_CONTAINER, image="testos:v1", project="root",
                           labels={"image_loading": "eager"})
        s1 = await edge.create(spec)
        s2 = await edge.create(spec)
        with self.assertRaises(AdmissionError):
            await edge.create(spec)
        self.assertEqual(edge.rejections, 1)
        await edge.destroy(s1)
        await edge.destroy(s2)

    async def test_gpu_request_rejected_without_gpu(self):
        edge = self.edges["edge-01"]
        spec = SandboxSpec(backend=BACKEND_CONTAINER, image="testos:v1", gpu=True,
                           project="root", labels={"image_loading": "eager"})
        with self.assertRaises(AdmissionError):
            await edge.create(spec)

    async def test_ttl_reclaims_idle_sandboxes(self):
        edge = self.edges["edge-01"]
        spec = SandboxSpec(backend=BACKEND_CONTAINER, image="testos:v1", project="root",
                           ttl_running_stop=0.0, ttl_absolute=3600,
                           labels={"image_loading": "eager"})
        sandbox_id = await edge.create(spec)
        self.assertIn(sandbox_id, edge.sandboxes)
        reclaimed = await edge._ttl_pass()
        self.assertEqual(reclaimed, 1)
        self.assertNotIn(sandbox_id, edge.sandboxes)
        self.assertEqual(edge.metrics.get("ttl_reclaims"), 1)

    async def test_stats_reflect_running_sandboxes(self):
        edge = self.edges["edge-01"]
        spec = SandboxSpec(backend=BACKEND_CONTAINER, image="testos:v1", project="root",
                           labels={"user": "alice", "task": "t-1", "image_loading": "eager"})
        sandbox_id = await edge.create(spec)
        stats = edge.stats()
        self.assertEqual(stats.running.get(BACKEND_CONTAINER, 0), 1)
        self.assertEqual(stats.per_user.get("alice"), 1)
        self.assertEqual(stats.per_task.get("t-1"), 1)
        self.assertTrue(stats.healthy)
        await edge.destroy(sandbox_id)
        self.assertEqual(edge.stats().running.get(BACKEND_CONTAINER, 0), 0)


if __name__ == "__main__":
    unittest.main()
