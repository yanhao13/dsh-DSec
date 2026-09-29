#!/usr/bin/env python3
"""High-density memory + CPU QoS replays (paper §5.2, §8.4, §8.5).

Fig. 12 replay: four Firecracker configurations (baseline, virtio-pmem+DAX,
DAMON+balloon free-page reporting, both) under a real agentic-RL-shaped
workload, measuring peak and time-integrated host memory usage.

Fig. 13 replay: latency-sensitive agent time under co-located best-effort
load with no protection, SCHED_IDLE alone, and SCHED_IDLE + core scheduling.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _common import hr  # noqa: E402
from dsec.resources.cpu import CpuQoS  # noqa: E402
from dsec.resources.memory import firecracker_workload, reductions  # noqa: E402


async def main():
    hr("§8.4 Fig. 12 — host memory under overcommit (20 microVMs)")
    results = firecracker_workload()
    red = reductions(results)
    print("config        peak host mem    time-integrated   reduction")
    for name, res in results.items():
        print("  %-11s %12.0f MiB %15.0f MiB·s" % (name, res.peak_mb, res.integral_mb_s))
    print("\nvs baseline:")
    print("  virtio-pmem+DAX cuts peak usage by %.1f%% (paper: 40.2%%)" % red["pmem_peak_pct"])
    print("  DAMON+balloon FPR cuts time-integrated usage by %.1f%% (paper: 21.2%%)"
          % red["fpr_integral_pct"])
    print("  combined cuts time-integrated usage by %.1f%%" % red["combined_integral_pct"])

    hr("§8.5 Fig. 13 — LS agent latency under BE co-location")
    qos = CpuQoS(os_enforce=False)
    print("background load | baseline | SCHED_IDLE | +core scheduling")
    for load in (0.1, 0.2, 0.3, 0.4, 0.5):
        base = qos.latency_inflation(load, "baseline")
        idle = qos.latency_inflation(load, "sched_idle")
        core = qos.latency_inflation(load, "idle_core")
        print("   %4.0f%%          | %6.1f%%  | %6.1f%%    | %6.1f%%"
              % (load * 100, base * 100, idle * 100, core * 100))
    print("\nat 50%% BE load: inflation falls from 45.2%% to 17.3%% with the")
    print("two-layer policy (SCHED_IDLE for BE + core scheduling for LS).")


if __name__ == "__main__":
    asyncio.run(main())
