"""Tests for the wire protocol codec (paper §3.2 ingress: requests over JSON)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec import proto
from dsec.types import LayerRef, NetworkRules, ResourceLimits, SandboxSpec


class TestProtoCodec(unittest.TestCase):
    def test_create_request_round_trip(self):
        spec = SandboxSpec(
            backend="container",
            image="registry/sphinx:v1",
            workspace=LayerRef(name="repo", version="v2", kind="workspace"),
            toolkits=[LayerRef(name="harness", version="v3", kind="toolkit")],
            limits=ResourceLimits(memory_limit_mb=4096, cpu_cores_limit=4),
            ttl_running_stop=300,
            network=NetworkRules(allow={"npm": False, "pypi": True}),
            init_user="root",
            project="root/team-a",
        )
        req = proto.CreateRequest(spec=spec, principal="user")
        decoded = proto.decode(proto.encode(req), proto.CreateRequest)
        self.assertEqual(decoded.spec.backend, "container")
        self.assertEqual(decoded.spec.image, "registry/sphinx:v1")
        self.assertEqual(decoded.spec.workspace, LayerRef("repo", "v2", "workspace"))
        self.assertEqual(decoded.spec.toolkits[0].name, "harness")
        self.assertEqual(decoded.spec.limits.memory_limit_mb, 4096)
        self.assertEqual(decoded.spec.network.allow, {"npm": False, "pypi": True})
        self.assertEqual(decoded.spec.project, "root/team-a")
        self.assertEqual(decoded.principal, "user")

    def test_exec_round_trip_with_binary(self):
        req = proto.ExecRequest(sandbox_id="dsec-x", command="cat f", stdin=b"\x00\x01\x02")
        decoded = proto.decode(proto.encode(req), proto.ExecRequest)
        self.assertEqual(decoded.stdin, b"\x00\x01\x02")
        self.assertEqual(decoded.sandbox_id, "dsec-x")

    def test_exec_response_round_trip(self):
        resp = proto.ExecResponse(exit_code=1, stdout=b"out\xff", stderr=b"err",
                                  truncated=True, duration_ms=3.5, error="")
        decoded = proto.decode(proto.encode(resp), proto.ExecResponse)
        self.assertEqual(decoded.stdout, b"out\xff")
        self.assertTrue(decoded.truncated)

    def test_file_and_list_round_trip(self):
        w = proto.FileWriteRequest(sandbox_id="s", path="/a", content=b"data")
        decoded_w = proto.decode(proto.encode(w), proto.FileWriteRequest)
        self.assertEqual(decoded_w.content, b"data")

        lst = proto.ListResponse(sandboxes=[proto.SandboxInfo("s1", "container", "running", "root")])
        decoded_l = proto.decode(proto.encode(lst), proto.ListResponse)
        self.assertEqual(decoded_l.sandboxes[0].state, "running")


if __name__ == "__main__":
    unittest.main()
