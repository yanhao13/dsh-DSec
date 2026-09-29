"""DSec — DeepSeek Elastic Compute reference implementation.

A faithful, runnable implementation of the platform described in
"DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective
Agentic Training at Scale" (arXiv:2609.22978).

The implementation is a single-process cluster reference: every component
(IAM, apiserver, placement engine, watcher, edge, aether, chronus, backends)
is a real object speaking a real message protocol, so the full platform runs
on any Python 3.9+ host. Linux-native hooks (SCHED_IDLE, core scheduling,
madvise, AppArmor profiles, docker/QEMU) activate when the host provides them.
"""

__version__ = "0.1.0"
__paper__ = "arXiv:2609.22978 — DeepSeek Elastic Compute (DSec)"

# Paper production anchors (§2.4), reproduced in demos as single-node simulations.
PAPER_SCALE = {
    "nodes_per_unit": 160,
    "cores_per_unit": 30_000,
    "dram_tb_per_unit": 250,
    "sandboxes_per_day": 3_000_000,
    "peak_concurrency": 380_000,
    "creates_per_second": 5_000,
    "microvms_per_node": 800,
    "containers_per_node": 3_200,
    "max_sandboxes_per_burst": 32_768,
}
