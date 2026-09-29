#!/usr/bin/env python3
"""Composable environment layers (paper §5.1, §4.2, §8.3).

Demonstrates:
- base + workspace + toolkit stacking with overlayfs priority semantics;
- the maintenance-cost win: upgrading m base images / k toolkits costs O(m)+O(k)
  instead of O(m·N)+O(k·N) under monolithic image fusing;
- production catalog sizes (11,266 base images, 102,171 workspaces, 103
  toolkits in one week, paper Tab. 2);
- layer collapsing under the 3 GB threshold with whiteout preservation (§5.3).
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _common import hr, make_cluster, teardown  # noqa: E402
from dsec.layers.compose import (  # noqa: E402
    EnvironmentComposer,
    layered_rebuild_cost,
    monolithic_rebuild_cost,
)
from dsec.layers.layer import Layer  # noqa: E402
from dsec.layers.overlay import OverlayFS  # noqa: E402


async def main():
    cluster = make_cluster(n_edges=1, gpu_edges=0)
    registry = cluster["registry"]

    hr("§5.1 — composable layers vs monolithic images")
    n_bases, n_workspaces, n_toolkits = 11_266, 102_171, 103  # Tab. 2
    m_upgrades, k_upgrades = 10, 3
    mono = monolithic_rebuild_cost(n_bases, n_workspaces, n_toolkits, m_upgrades, k_upgrades)
    layered = layered_rebuild_cost(m_upgrades, k_upgrades)
    print("upgrading %d base images and %d toolkits:" % (m_upgrades, k_upgrades))
    print("   monolithic images: %d rebuilds   (O(m·N) + O(k·N))" % mono)
    print("   layered versioning: %d rebuilds   (O(m) + O(k))" % layered)
    print("   -> %.0fx fewer rebuilds" % (mono / layered))

    hr("Layer priority: toolkit > workspace > base (Fig. 4b)")
    env = EnvironmentComposer(registry).compose(
        ("demo-os", "v1"), ("task-repo", "v1"), [("harness", "v1")])
    merged = env.merged_files()
    print("stack:", env.describe())
    print("   workspace/data.txt ->", merged["workspace/data.txt"].decode().strip(),
          "(workspace layer)")
    print("   workspace/app.py   ->", merged["workspace/app.py"].decode().strip(),
          "(workspace overrides base)")

    hr("Toolkit upgrade rebuilds only the toolkit layer (O(k))")
    before = len(registry.rebuild_log)
    registry.republish(Layer("harness", "v2", "toolkit", {
        "tools/run.py": b"print('harness v2')\n"}))
    print("rebuild log delta after upgrading harness:", len(registry.rebuild_log) - before)
    print("last log:", registry.rebuild_log[-1])

    hr("§8.3 — EROFS layer mounting vs per-sandbox tar extraction")
    # The paper: tar-based provisioning generates ~5.5x the disk-write traffic
    # and 3.4x the peak throughput of the EROFS path, taking 1.76x longer.
    # Modeled from one shared layer serving many sandboxes:
    workspace_bytes = env.total_size_bytes
    n_sandboxes = 100
    tar_writes = n_sandboxes * workspace_bytes  # every sandbox extracts a copy
    erofs_writes = 0  # shared layer mounted read-only; only upper-layer writes
    print("workspace stack size: %.1f MiB across %d sandboxes" % (workspace_bytes / 1e6, n_sandboxes))
    print("   tar extraction writes: %.1f GiB" % (tar_writes / 1e9))
    print("   EROFS mount writes:    %.1f GiB (5.5x less in the paper's run)"
           % (erofs_writes / 1e9))

    hr("§5.3 — layer collapsing under 3 GB with whiteout semantics")
    small1 = Layer("small-1", "v1", "base", {"a.txt": b"a", "gone.txt": b"x"})
    small2 = Layer("small-2", "v1", "base", {"b.txt": b"b", ".wh.gone.txt": b""})
    stack = OverlayFS([small1, small2])
    collapsed = stack.merged_files()
    print("merged small layers:", sorted(collapsed))
    print("whiteout preserved through collapse: 'gone.txt' absent ->",
          "gone.txt" not in collapsed)

    await teardown(cluster)


if __name__ == "__main__":
    asyncio.run(main())
