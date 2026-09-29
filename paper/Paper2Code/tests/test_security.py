"""Tests for reward-hacking mitigations (paper §6.4, §6.5)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.errors import AccessDenied, NetworkPolicyViolation
from dsec.rl.security import SecurityPolicy
from dsec.types import NetworkRules


class FakeCtx:
    def __init__(self, sandbox_id="sb-1", rules=None):
        self.sandbox_id = sandbox_id
        self.spec = type("S", (), {"network": rules or NetworkRules(allow={})})()


class TestProtectedPaths(unittest.TestCase):
    def setUp(self):
        self.policy = SecurityPolicy()
        self.ctx = FakeCtx()

    def test_chronus_log_scrape_blocked(self):
        # Agents scraped chronus logs for leaked answers (paper §6.4).
        with self.assertRaises(AccessDenied):
            self.policy.check_file_access(self.ctx, "/var/log/chronus/session.log", "read")

    def test_chronus_socket_forgery_blocked(self):
        with self.assertRaises(AccessDenied):
            self.policy.check_file_access(self.ctx, "/run/chronus.sock", "write")

    def test_bash_overwrite_blocked(self):
        # Agents overwrote /bin/bash to inject commands into later sessions.
        with self.assertRaises(AccessDenied):
            self.policy.check_file_access(self.ctx, "/bin/bash", "write")
        self.assertIn("protected-path-write", self.policy.misbehavior.kinds())

    def test_kpagecgroup_kernel_bug_path_blocked(self):
        # grep -r over /proc read /proc/kpagecgroup and crashed the kernel
        # (paper §6.4); the platform path is denied.
        with self.assertRaises(AccessDenied):
            self.policy.check_file_access(self.ctx, "/proc/kpagecgroup", "read")

    def test_ordinary_workspace_files_allowed(self):
        self.policy.check_file_access(self.ctx, "/workspace/repo/app.py", "read")
        self.policy.check_file_access(self.ctx, "/workspace/repo/app.py", "write")

    def test_apparmor_profile_generation(self):
        profile = self.policy.apparmor_profile("sb-9")
        self.assertIn("profile dsec-sandbox-sb-9", profile)
        self.assertIn("deny /var/log/chronus/** rwlkx,", profile)
        self.assertIn("deny /bin/bash rwlkx,", profile)


class TestNetworkAllowlist(unittest.TestCase):
    def test_pypi_allowed_npm_denied(self):
        # Listing 1: network_rules={"npm": False, "pypi": True}.
        ctx = FakeCtx(rules=NetworkRules(allow={"npm": False, "pypi": True}))
        policy = SecurityPolicy()
        policy.check_network(ctx, "https://pypi.org/simple/requests/")
        with self.assertRaises(NetworkPolicyViolation):
            policy.check_network(ctx, "https://registry.npmjs.org/react")

    def test_deny_by_default(self):
        # Allowlist semantics: anything not covered is denied (§6.5).
        ctx = FakeCtx(rules=NetworkRules(allow={}))
        policy = SecurityPolicy()
        with self.assertRaises(NetworkPolicyViolation):
            policy.check_network(ctx, "https://proxy.golang.org/github.com/x/y")

    def test_port_scan_and_mirror_discovery_recorded(self):
        # Agents scanned ports/services for reachable mirrors (paper §6.4).
        ctx = FakeCtx(rules=NetworkRules(allow={"pypi": True}))
        policy = SecurityPolicy()
        try:
            policy.check_network(ctx, "https://mirror.internal.example/")
        except NetworkPolicyViolation:
            pass
        self.assertIn("network-denied", policy.misbehavior.kinds())

    def test_dynamic_policy_update(self):
        # Policies update dynamically as tasks move between stages (§6.5).
        rules = NetworkRules(allow={"pypi": True})
        updated = rules.update({"npm": True, "github": True})
        ctx = FakeCtx(rules=updated)
        policy = SecurityPolicy()
        policy.check_network(ctx, "https://registry.npmjs.org/react")
        policy.check_network(ctx, "https://github.com/x/y")

    def test_ebpf_rule_rendering(self):
        policy = SecurityPolicy()
        rules = policy.render_ebpf_rules(NetworkRules(allow={"pypi": True, "npm": False}))
        self.assertEqual(len(rules), 2)
        self.assertEqual(rules[0]["service"], "pypi")
        self.assertEqual(rules[0]["default"], "drop")
        self.assertEqual(rules[0]["match"]["proto"], "tcp")


if __name__ == "__main__":
    unittest.main()
