#!/usr/bin/env python3
"""Bursty sandbox creation with power-of-k placement (paper §4.1, §7, §2.4).

Rollout and evaluation jobs create sandboxes in bursts: a single job may
request up to 32K instances. This demo submits a burst of creations, measures
the creation rate, shows power-of-k load spreading across edges, and exercises
TTL reclamation of idle sessions — the lifecycle behavior behind the paper's
production anchors (~5,000 creates/s, ~3M sandboxes/day on ~160 nodes).
"""
import asyncio
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _common import hr, make_cluster, teardown  # noqa: E402
from dsec.client import DSecContainerRunArgs  # noqa: E402
from dsec.types import BACKEND_CONTAINER, SandboxSpec  # noqa: E402

BURST = 200
CONCURRENCY = 40


async def main():
    cluster = make_cluster(n_edges=3, gpu_edges=1)
    client = cluster["clients"]["user"]
    await client.open()
    server = cluster["server"]
    edges = cluster["edges"]

    hr("Burst creation — %d sandboxes, power-of-k placement" % BURST)
    args = DSecContainerRunArgs(
        container_image="demo-os:v1",
        memory_limit_mb=64, cpu_cores_limit=0.25,
        ttl_running_stop=1.0, ttl_absolute=3600,
        labels={"image_loading": "eager", "task": "burst-demo"},
    )
    spec = args.to_spec()

    sem = asyncio.Semaphore(CONCURRENCY)
    start = time.perf_counter()

    async def create_one():
        async with sem:
            return await server.create_sandbox("user", spec)

    ids = await asyncio.gather(*(create_one() for _ in range(BURST)))
    elapsed = time.perf_counter() - start
    rate = BURST / elapsed
    print("created %d sandboxes in %.2f s -> %.0f creates/s" % (BURST, elapsed, rate))

    placement = {"edge-%02d" % i: 0 for i in range(1, 4)}
    from dsec.idgen import owning_edge

    for sid, _, _ in ids:
        placement[owning_edge(sid)] += 1
    print("placement spread (power-of-k, least-loaded of 2 samples):")
    for edge_id, count in placement.items():
        print("   %s: %d sandboxes (running: %d)" % (
            edge_id, count, len(edges[edge_id].sandboxes)))

    hr("TTL reclamation of idle sessions (§2.3)")
    print("idle timeout is 1.0 s; sleeping 3 s so the edge's TTL loop reclaims…")
    for edge in edges.values():
        edge.ttl_interval = 0.5  # speed up the sweep for the demo
        await edge.start()
    await asyncio.sleep(3.0)
    remaining = sum(len(e.sandboxes) for e in edges.values())
    reclaimed = sum(e.metrics.get("ttl_reclaims") for e in edges.values())
    print("live sandboxes after TTL sweep: %d (reclaimed %d)" % (remaining, reclaimed))
    for edge in edges.values():
        await edge.stop()

    hr("Production-scale context (§2.4)")
    import dsec as _dsec

    scale = _dsec.PAPER_SCALE
    print("one production unit: ~%d nodes / %d cores / %d TB DRAM" % (
        scale["nodes_per_unit"], scale["cores_per_unit"], scale["dram_tb_per_unit"]))
    print("serves ~%d sandboxes/day, peak %d concurrent, %d creates/s" % (
        scale["sandboxes_per_day"], scale["peak_concurrency"], scale["creates_per_second"]))
    print("largest jobs request up to %d sandboxes" % scale["max_sandboxes_per_burst"])

    await teardown(cluster)


if __name__ == "__main__":
    asyncio.run(main())
