"""Shared cluster fixture for the DSec test suite (stdlib unittest only)."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.apiserver import ApiServer
from dsec.client import DSecClient
from dsec.edge import Edge
from dsec.iam import IAM, OPS
from dsec.layers.layer import Layer
from dsec.layers.registry import LayerRegistry
from dsec.placement import PlacementEngine
from dsec.rl.security import SecurityPolicy
from dsec.storage.store import ChunkCache, RemoteStore
from dsec.types import NodeCapacity
from dsec.watcher import Watcher

BASE_FILES = {
    "etc/os-release": b"NAME=TestOS\n",
    "workspace/app.py": b"print('app v1')\n",
    "workspace/data.txt": b"hello from workspace\n",
    "usr/lib/large.dat": bytes(1024 * 1024),  # 1 MiB blob for chunked reads
    "usr/lib/tiny.dat": b"tiny\n",
}


def make_layers():
    base = Layer("testos", "v1", "base", dict(BASE_FILES))
    workspace = Layer("repo-42", "v1", "workspace", {
        "workspace/app.py": b"print('app v2 from workspace')\n",
        "workspace/extra.txt": b"workspace extra\n",
    })
    toolkit = Layer("harness", "v3", "toolkit", {
        "tools/run.py": b"print('harness v3')\n",
        "workspace/data.txt": b"toolkit overrides data\n",  # priority demo
    })
    return base, workspace, toolkit


class ClusterTestCase(unittest.IsolatedAsyncioTestCase):
    """A running in-process cluster: 2 edges, watcher, placement, IAM, SDK."""

    async def asyncSetUp(self):
        self.tmpdir = tempfile.mkdtemp(prefix="dsec-test-")
        self.store = RemoteStore()
        self.cache = ChunkCache(capacity_bytes=256 * 1024 * 1024)
        self.registry = LayerRegistry(self.store, self.cache,
                                      local_dir=os.path.join(self.tmpdir, "metadata"))
        self.base, self.workspace, self.toolkit = make_layers()
        for layer in (self.base, self.workspace, self.toolkit):
            self.registry.publish(layer)

        self.iam = IAM()
        for principal in ("admin", "user", "builder", "runtime", "agent"):
            self.iam.add_principal(principal)
        self.iam.projects["root"].grants["admin"] = set(OPS)
        self.iam.projects["root"].grant("user", {
            "sandbox.create", "sandbox.ops", "sandbox.stop", "sandbox.list"}, "admin")
        self.iam.projects["root"].grant("builder", {
            "sandbox.create", "sandbox.ops", "sandbox.stop", "sandbox.list", "pack.diff"}, "admin")
        self.iam.projects["root"].grant("runtime", {
            "sandbox.create", "sandbox.ops", "sandbox.stop", "sandbox.list"}, "admin")

        self.security = SecurityPolicy()
        self.edges = {}
        for i in (1, 2):
            edge = Edge(
                "edge-%02d" % i,
                NodeCapacity(cpu_cores=128, memory_mb=262144, max_sandboxes=512,
                             gpu_instances=1 if i == 2 else 0),
                self.store, self.registry,
                rootfs_base=os.path.join(self.tmpdir, "rootfs-%d" % i),
                security=self.security,
            )
            self.edges[edge.edge_id] = edge
        self.watcher = Watcher(probe_interval=3600.0)
        for edge in self.edges.values():
            self.watcher.register_edge(edge)
        self.placement = PlacementEngine(self.watcher, sample_k=2)
        self.server = ApiServer(self.iam, self.placement, self.edges, self.watcher)
        self.clients = {}
        for principal in ("user", "builder", "runtime"):
            self.clients[principal] = DSecClient(server=self.server, principal=principal)

    async def asyncTearDown(self):
        for edge in self.edges.values():
            await edge.stop()
        for client in self.clients.values():
            await client.close()
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def client(self, principal="user") -> DSecClient:
        return self.clients[principal]
