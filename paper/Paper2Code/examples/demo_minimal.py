#!/usr/bin/env python3
"""Paper Listing 1: a minimal sandbox session through libdsec (DSec §2.1).

    client = DSecClient()
    await client.open()
    args = DSecContainerRunArgs(
        container_image="registry.../sphinx-9658:official",
        memory_limit_mb=4096, cpu_cores_limit=4,
        ttl_running_stop=300,          # idle timeout
        network_rules={"npm": False, "pypi": True},
        init_user="root",
    )
    sandbox = await client.run_container(args, timeout=120)
    result = await sandbox.run_shell("echo hello world")
    await sandbox.stop()
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _common import hr, make_cluster, teardown  # noqa: E402
from dsec.client import DSecContainerRunArgs  # noqa: E402


async def main():
    cluster = make_cluster(n_edges=1, gpu_edges=0)
    client = cluster["clients"]["user"]
    await client.open()

    hr("Listing 1 — a minimal sandbox session through libdsec")
    args = DSecContainerRunArgs(
        container_image="demo-os:v1",
        memory_limit_mb=4096, cpu_cores_limit=4,
        ttl_running_stop=300,
        network_rules={"npm": False, "pypi": True},
        init_user="root",
        labels={"image_loading": "eager"},
    )
    sandbox = await client.run_container(args, timeout=120)
    print("created sandbox:", sandbox.sandbox_id, "(backend:", sandbox.backend + ")")
    result = await sandbox.run_shell("echo hello world")
    print("run_shell('echo hello world') ->", result.text().strip(),
          "(exit %d, %.1f ms)" % (result.exit_code, result.duration_ms))

    # State persists across calls (§2.3), and the network policy is attached.
    await sandbox.run_shell("echo persist > marker.txt")
    r = await sandbox.run_shell("cat marker.txt")
    print("state across calls: marker.txt =", repr(r.text().strip()))

    edge = cluster["server"].resolve_edge(sandbox.sandbox_id)
    policy = edge.sandboxes[sandbox.sandbox_id].metadata["network_policy"]
    print("applied eBPF-style network policy: pypi=%s npm=%s" % (
        any(p["service"] == "pypi" for p in policy),
        any(p["service"] == "npm" for p in policy)))

    await sandbox.stop()
    print("stopped; state now:", sandbox.state)
    await teardown(cluster)


if __name__ == "__main__":
    asyncio.run(main())
