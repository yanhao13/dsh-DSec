"""Shared demo infrastructure: builds a small DSec cluster."""
from __future__ import annotations

import os
import sys
import tempfile

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
    "etc/os-release": b"NAME=DSecTestOS\nVERSION=1.0\n",
    "workspace/app.py": b"print('hello from the task repo')\n",
    "workspace/tests/test_app.py": b"def test_app(): assert True\n",
    "usr/bin/tool": b"#!/bin/sh\necho tool-v1\n",
    "data/blob.bin": bytes(512 * 1024),
}


def make_cluster(n_edges=2, gpu_edges=1, tmpdir=None, keep=False):
    """Build a store, registry, IAM, edges, watcher, placement, server, client."""
    tmpdir = tmpdir or tempfile.mkdtemp(prefix="dsec-demo-")
    store = RemoteStore()
    cache = ChunkCache(capacity_bytes=1 << 30)
    registry = LayerRegistry(store, cache, local_dir=os.path.join(tmpdir, "metadata"))
    registry.publish(Layer("demo-os", "v1", "base", dict(BASE_FILES)))
    registry.publish(Layer("task-repo", "v1", "workspace", {
        "workspace/app.py": b"print('app from workspace layer')\n",
        "workspace/data.txt": b"task data\n",
    }))
    registry.publish(Layer("harness", "v1", "toolkit", {
        "tools/run.py": b"print('harness tool')\n",
    }))

    iam = IAM()
    for principal in ("admin", "user", "builder", "trainer"):
        iam.add_principal(principal)
    iam.projects["root"].grants["admin"] = set(OPS)
    iam.projects["root"].grant("user", {
        "sandbox.create", "sandbox.ops", "sandbox.stop", "sandbox.list"}, "admin")
    iam.projects["root"].grant("builder", {
        "sandbox.create", "sandbox.ops", "sandbox.stop", "sandbox.list", "pack.diff"}, "admin")
    iam.projects["root"].grant("trainer", {
        "sandbox.create", "sandbox.ops", "sandbox.stop", "sandbox.list"}, "admin")

    security = SecurityPolicy()
    edges = {}
    for i in range(1, n_edges + 1):
        edge = Edge(
            "edge-%02d" % i,
            NodeCapacity(cpu_cores=256, memory_mb=1 << 20, max_sandboxes=10000,
                         gpu_instances=1 if i <= gpu_edges else 0),
            store, registry,
            rootfs_base=os.path.join(tmpdir, "rootfs-%d" % i),
            security=security,
        )
        edges[edge.edge_id] = edge
    watcher = Watcher(probe_interval=3600.0)
    for edge in edges.values():
        watcher.register_edge(edge)
    placement = PlacementEngine(watcher, sample_k=2)
    server = ApiServer(iam, placement, edges, watcher)
    clients = {p: DSecClient(server=server, principal=p) for p in ("user", "builder", "trainer")}
    return {
        "store": store, "cache": cache, "registry": registry, "iam": iam,
        "edges": edges, "watcher": watcher, "placement": placement,
        "server": server, "clients": clients, "security": security,
        "tmpdir": tmpdir, "keep": keep,
    }


async def teardown(cluster):
    for edge in cluster["edges"].values():
        await edge.stop()
    for client in cluster["clients"].values():
        await client.close()
    if not cluster["keep"]:
        import shutil

        shutil.rmtree(cluster["tmpdir"], ignore_errors=True)


def hr(title):
    line = "=" * 72
    print("\n%s\n  %s\n%s" % (line, title, line))
