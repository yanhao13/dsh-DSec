"""Tests for sandbox-id routing (paper §3.2: ids encode the owning edge)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec import idgen


class TestSandboxIds(unittest.TestCase):
    def test_round_trip_encodes_owning_edge(self):
        sid = idgen.new_sandbox_id("edge-07", 42)
        parsed = idgen.parse_sandbox_id(sid)
        self.assertEqual(parsed.edge_id, "edge-07")
        self.assertEqual(parsed.seq, 42)
        self.assertEqual(idgen.owning_edge(sid), "edge-07")

    def test_unique_ids(self):
        ids = {idgen.new_sandbox_id("edge-01", i) for i in range(100)}
        self.assertEqual(len(ids), 100)

    def test_routing_key_stability(self):
        # Any apiserver instance must derive the same owning edge (paper §3.2).
        sid = idgen.new_sandbox_id("edge-99", 7)
        for _ in range(10):
            self.assertEqual(idgen.owning_edge(sid), "edge-99")

    def test_malformed_id_rejected(self):
        with self.assertRaises(ValueError):
            idgen.parse_sandbox_id("nope")
        with self.assertRaises(ValueError):
            idgen.parse_sandbox_id("dsec-abc")


if __name__ == "__main__":
    unittest.main()
