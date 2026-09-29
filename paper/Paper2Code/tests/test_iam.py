"""Tests for IAM nested projects, quotas, and bounded delegation (paper §3.2)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.errors import PermissionDenied, QuotaExceeded
from dsec.iam import IAM, OP_CREATE, OP_MANAGE, OP_PACK, Quota


class TestIAM(unittest.TestCase):
    def setUp(self):
        self.iam = IAM()
        for p in ("admin", "alice", "bob", "agent"):
            self.iam.add_principal(p)
        self.iam.projects["root"].grants["admin"] = {
            OP_CREATE, OP_MANAGE, OP_PACK, "sandbox.ops", "sandbox.stop", "sandbox.list"}
        self.iam.projects["root"].grant("alice", {OP_CREATE, OP_MANAGE}, "admin")
        self.iam.projects["root"].grant("bob", {OP_CREATE}, "admin")

    def test_multi_level_nesting(self):
        p1 = self.iam.create_project("root", "team-a", Quota(cpu=100, memory_mb=100000, max_sandboxes=100), "alice")
        p2 = self.iam.create_project("root/team-a", "group-x", Quota(cpu=40, memory_mb=40000, max_sandboxes=40), "alice")
        p3 = self.iam.create_project("root/team-a/group-x", "sub-y", Quota(cpu=10, memory_mb=10000, max_sandboxes=10), "alice")
        self.assertEqual(p3.path(), "root/team-a/group-x/sub-y")

    def test_subproject_quota_bounded_by_parent_remaining(self):
        p1 = self.iam.create_project("root", "team-a", Quota(cpu=100, memory_mb=100000, max_sandboxes=100), "alice")
        # Consume 90% of the parent, then a child may not exceed the remainder.
        self.iam.consume(p1, Quota(cpu=90, memory_mb=90000, max_sandboxes=90))
        with self.assertRaises(QuotaExceeded):
            self.iam.create_project("root/team-a", "greedy", Quota(cpu=20, memory_mb=20000, max_sandboxes=20), "alice")
        self.iam.create_project("root/team-a", "humble", Quota(cpu=10, memory_mb=10000, max_sandboxes=10), "alice")

    def test_cannot_grant_permission_not_held(self):
        # Alice holds OP_MANAGE but not OP_PACK on root: she cannot grant pack
        # permissions (delegation bounded by the parent, paper §3.2).
        with self.assertRaises(PermissionDenied):
            self.iam.projects["root"].grant("bob", {OP_PACK}, "alice")

    def test_policy_does_not_escalate_downward(self):
        # Bob has no create right: he cannot delegate it to a subproject.
        with self.assertRaises(PermissionDenied):
            self.iam.create_project("root", "bob-team", Quota(cpu=1, memory_mb=1, max_sandboxes=1), "bob")

    def test_quota_consume_walks_chain_and_release(self):
        p1 = self.iam.create_project("root", "team-a", Quota(cpu=10, memory_mb=1000, max_sandboxes=10), "alice")
        self.iam.consume(p1, Quota(cpu=5, memory_mb=500, max_sandboxes=5))
        self.assertEqual(p1.used.max_sandboxes, 5)
        self.assertEqual(self.iam.projects["root"].used.max_sandboxes, 5)
        self.iam.release(p1, Quota(cpu=5, memory_mb=500, max_sandboxes=5))
        self.assertEqual(p1.used.max_sandboxes, 0)
        self.assertEqual(self.iam.projects["root"].used.max_sandboxes, 0)

    def test_agents_use_same_management_api(self):
        # Agents and harnesses can be principals too (paper §3.2).
        self.iam.projects["root"].grant("agent", {OP_CREATE}, "alice")
        project = self.iam.authorize("agent", OP_CREATE, "root")
        self.assertEqual(project.path(), "root")

    def test_deny_when_ungranted(self):
        with self.assertRaises(PermissionDenied):
            self.iam.authorize("bob", OP_MANAGE, "root")


if __name__ == "__main__":
    unittest.main()
