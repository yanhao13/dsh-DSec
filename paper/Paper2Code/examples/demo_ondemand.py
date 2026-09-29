#!/usr/bin/env python3
"""On-demand EROFS image loading vs eager extraction (paper §5.3, §8.2, Tab. 3).

Fig. 10 replay: eager full-image pulling delays creation and writes ~2x the
data; EROFS on-demand loading mounts layers directly and fetches only the
sandbox's working set — the paper measures 1.71x slower completion for eager
pulling and ~57% fewer cumulative disk writes for the on-demand path.

Tab. 3 replay: runtime access covers only 4.2–13.3% of image data, so fetching
the whole image is mostly waste. This demo builds a multi-file image, creates
sandboxes under both policies, and lets each sandbox touch only a fraction of
its files through the file API, then compares bytes fetched from 3FS and
extraction writes.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _common import hr, make_cluster, teardown  # noqa: E402
from dsec.client import DSecContainerRunArgs  # noqa: E402
from dsec.layers.layer import Layer  # noqa: E402

N_FILES = 60
FILE_SIZE = 64 * 1024
N_SANDBOXES = 30
ACCESS_FRACTION = 0.10  # the agent touches ~10% of the image (Tab. 3 range)


async def main():
    cluster = make_cluster(n_edges=2, gpu_edges=0)
    store = cluster["store"]
    registry = cluster["registry"]
    client = cluster["clients"]["user"]
    await client.open()

    hr("Build a diverse task image (60 files, %.1f MiB)" % (N_FILES * FILE_SIZE / 1e6))
    # Incompressible payloads so chunk-fetch accounting is meaningful.
    files = {"pkg/f%02d.py" % i: os.urandom(FILE_SIZE) for i in range(N_FILES)}
    files["pkg/main.py"] = b"print('entry')\n"
    registry.publish(Layer("diverse-image", "v1", "base", files))
    accessed = ["pkg/f%02d.py" % i for i in range(0, int(N_FILES * ACCESS_FRACTION))]

    async def run_policy(policy):
        cluster["cache"].clear()  # isolate the two runs (second-level cache)
        store.total_bytes_fetched = 0
        for edge in cluster["edges"].values():
            edge.metrics.counters["disk_extract_bytes"] = 0
        args = DSecContainerRunArgs(
            container_image="diverse-image:v1",
            memory_limit_mb=128, cpu_cores_limit=0.5,
            ttl_running_stop=3600,
            labels={"image_loading": policy},
        )
        sandboxes = []
        for _ in range(N_SANDBOXES):
            sb = await client.run_container(args)
            sandboxes.append(sb)
        # The agent's working set: read ~10% of the files through the file API.
        for sb in sandboxes:
            for path in accessed[:5]:
                try:
                    await sb.read_file(path, max_bytes=64 * 1024)
                except FileNotFoundError:
                    pass
        # Node disk writes: eager = full extraction at creation; ondemand =
        # only the files the agent actually touched, materialized on access
        # (the portable stand-in for an EROFS mount).
        materialized = 0
        for edge in cluster["edges"].values():
            for ctx in edge.sandboxes.values():
                materialized += ctx.metadata.get("ondemand_stats", {}).get("fetched", 0)
        for sb in sandboxes:
            await sb.stop()
        fetched = store.total_bytes_fetched
        extracts = sum(
            e.metrics.get("disk_extract_bytes") for e in cluster["edges"].values())
        writes = extracts + materialized
        return fetched, writes

    hr("§8.2 — eager pull vs on-demand EROFS loading")
    eager_fetched, eager_writes = await run_policy("eager")
    lazy_fetched, lazy_writes = await run_policy("ondemand")
    total_image = sum(len(d) for d in files.values())
    print("total image data: %.1f MiB (incompressible)" % (total_image / 1e6))
    print("policy     bytes fetched from 3FS    node disk writes (extract+materialize)")
    print("  eager    %12.1f MiB           %12.1f MiB"
          % (eager_fetched / 1e6, eager_writes / 1e6))
    print("  ondemand %12.1f MiB           %12.1f MiB"
          % (lazy_fetched / 1e6, lazy_writes / 1e6))
    if eager_writes > 0:
        print("node disk-write reduction: %d%% fewer (paper: ~57%% with 1.71x faster"
              " completion)" % (100 * (1 - lazy_writes / eager_writes)))
    if eager_fetched > 0:
        print("3FS traffic reduction:      %d%% less (working-set-only fetch, Tab. 3)"
              % (100 * (1 - lazy_fetched / eager_fetched)))

    await teardown(cluster)


if __name__ == "__main__":
    asyncio.run(main())
