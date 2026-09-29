"""Tests for composable layers and the maintenance-cost model (paper §5.1)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.layers.compose import (
    EnvironmentComposer,
    layered_rebuild_cost,
    monolithic_rebuild_cost,
)
from dsec.layers.layer import Layer
from dsec.layers.registry import LayerRegistry
from dsec.storage.store import ChunkCache, RemoteStore


class TestRebuildCostModel(unittest.TestCase):
    """Upgrading layers costs O(m)+O(k) layered vs O(m·N)+O(k·N) monolithic."""

    def test_monolithic_vs_layered(self):
        n_bases, n_workspaces, n_toolkits = 100, 1000, 50
        m, k = 10, 5
        mono = monolithic_rebuild_cost(n_bases, n_workspaces, n_toolkits, m, k)
        layered = layered_rebuild_cost(m, k)
        self.assertEqual(mono, (10 + 5) * 1000)
        self.assertEqual(layered, 15)
        self.assertLess(layered, mono / 100)

    def test_toolkit_upgrade_rebuilds_only_toolkit(self):
        store, cache = RemoteStore(), ChunkCache()
        reg = LayerRegistry(store, cache)
        reg.publish(Layer("base", "v1", "base", {"os": b"1"}))
        reg.publish(Layer("ws-a", "v1", "workspace", {"a": b"1"}))
        reg.publish(Layer("ws-b", "v1", "workspace", {"b": b"1"}))
        reg.publish(Layer("toolkit", "v1", "toolkit", {"t": b"1"}))
        composer = EnvironmentComposer(reg)
        for ws in ("ws-a", "ws-b"):
            composer.compose(("base", "v1"), ("ws-a" if ws == "ws-a" else "ws-b", "v1"),
                             [("toolkit", "v1")])
        # Upgrading the toolkit republishes exactly one layer (O(k), not O(k·N)).
        before = len(reg.rebuild_log)
        reg.republish(Layer("toolkit", "v2", "toolkit", {"t": b"2"}))
        self.assertEqual(len(reg.rebuild_log), before + 1)


class TestComposition(unittest.TestCase):
    def setUp(self):
        self.store = RemoteStore()
        self.reg = LayerRegistry(self.store, ChunkCache())
        self.reg.publish(Layer("base", "v1", "base", {
            "etc/os": b"base-os",
            "shared.txt": b"base-value",
        }))
        self.reg.publish(Layer("repo", "v1", "workspace", {
            "shared.txt": b"workspace-value",
            "repo/code.py": b"print(1)",
        }))
        self.reg.publish(Layer("harness", "v2", "toolkit", {
            "shared.txt": b"toolkit-value",
            "tools/run.sh": b"run",
        }))
        self.composer = EnvironmentComposer(self.reg)

    def test_stack_priority_toolkit_wins(self):
        env = self.composer.compose(("base", "v1"), ("repo", "v1"), [("harness", "v2")])
        merged = env.merged_files()
        self.assertEqual(merged["shared.txt"], b"toolkit-value")
        self.assertEqual(merged["etc/os"], b"base-os")
        self.assertIn("repo/code.py", merged)

    def test_stack_order(self):
        env = self.composer.compose(("base", "v1"), ("repo", "v1"), [("harness", "v2")])
        stack = env.stack()
        self.assertEqual(stack[0].kind, "base")
        self.assertEqual(stack[1].kind, "workspace")
        self.assertEqual(stack[2].kind, "toolkit")


if __name__ == "__main__":
    unittest.main()
