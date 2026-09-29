#!/usr/bin/env python3
"""Agent-misbehavior mitigations (paper §6.4, §6.5).

Replays the paper's observed attack patterns against the platform defenses:
chronus log scraping, /bin/bash overwrite, forged chronus RPCs, network
allowlist violations, and unbounded command output — each blocked and recorded
in the misbehavior log, with the sandbox surviving every attempt.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _common import hr, make_cluster, teardown  # noqa: E402
from dsec.client import DSecContainerRunArgs  # noqa: E402
from dsec.errors import AccessDenied, NetworkPolicyViolation  # noqa: E402


async def attempt(desc, fn):
    try:
        await fn()
        print("  [ALLOWED?!] %s" % desc)
    except (AccessDenied, NetworkPolicyViolation) as exc:
        print("  [BLOCKED] %s -> %s" % (desc, exc))


async def main():
    cluster = make_cluster(n_edges=1, gpu_edges=0)
    client = cluster["clients"]["user"]
    security = cluster["security"]
    await client.open()

    hr("§6.4 — agent attacks from production experience")
    sb = await client.run_container(DSecContainerRunArgs(
        container_image="demo-os:v1",
        network_rules={"pypi": True, "npm": False},
        labels={"image_loading": "eager"}))
    edge = cluster["server"].resolve_edge(sb.sandbox_id)

    await attempt("scrape chronus logs for leaked answers",
                  lambda: sb.read_file("/var/log/chronus/session.log"))
    await attempt("overwrite /bin/bash to inject commands",
                  lambda: sb.write_file("/bin/bash", b"#!/bin/sh\necho pwned\n"))
    await attempt("read /proc/kpagecgroup (the kernel-crash path)",
                  lambda: sb.read_file("/proc/kpagecgroup"))
    await attempt("forge an RPC to a chronus socket without an SDK token",
                  lambda: edge.sandboxes[sb.sandbox_id].metadata["aether"].run(
                      "term-forged", "garbage-token", "echo pwn"))
    await attempt("reach npm (denied by the task allowlist)",
                  lambda: sb.http("https://registry.npmjs.org/react"))
    await attempt("reach an internal mirror (deny-by-default)",
                  lambda: sb.http("https://mirror.internal.example/"))

    r = await sb.run_shell("yes", timeout=30)  # §6.4: unbounded output
    print("  'yes' output capture: cut at %d bytes (truncated=%s) — the paper's"
          " tens-of-GB log incident is prevented" % (len(r.stdout), r.truncated))

    hr("Misbehavior log (§6.4 observability)")
    for event in security.misbehavior.events:
        print("  ", event)
    print("\nsandbox survived every attempt:", (await sb.run_shell("echo alive")).text().strip())
    await sb.stop()
    await teardown(cluster)


if __name__ == "__main__":
    asyncio.run(main())
