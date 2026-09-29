**not o3-mini, deepseek-v4-pro is the model working here. for reference: [going-doer/Paper2Code(4.8k)](https://github.com/going-doer/paper2code).**

# Paper2Code → DSec — DeepSeek Elastic Compute

A faithful, runnable implementation of the sandbox platform described in
**"DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective
Agentic Training at Scale"** ([arXiv:2609.22978](https://arxiv.org/abs/2609.22978)).

DSec is the production sandbox platform behind DeepSeek's agentic RL training:
a unified SDK over FnCall / container / microVM / full-VM backends, composable
EROFS environment layers, high-density memory and CPU management, 3FS-backed
on-demand image loading, and explicit co-design with the RL framework
(preemption-safe resumption, pack_diff environments, reward-hacking
mitigation). One production unit spans ~160 nodes and serves ~3M sandboxes/day
with 380K concurrent sandboxes and 5,000+ creations per second.

This repository is a **single-process cluster reference implementation**:
every component (IAM, apiserver, placement engine, watcher, edge, aether,
chronus, all four backends) is a real object speaking a real message protocol,
so the entire platform runs on any Python 3.9+ host with **zero dependencies**
and no external services. Linux-native hooks (SCHED_IDLE, core scheduling,
madvise, real Docker/QEMU, AppArmor profiles) activate automatically when the
host provides them.

```console
$ python3 -m unittest discover -s tests -t .     # 86 tests, stdlib only
$ python3 examples/demo_minimal.py               # paper Listing 1
```

## Quick start

```python
import asyncio
from dsec.client import DSecClient, DSecContainerRunArgs

async def main():
    # ... (cluster assembled by examples/_common.make_cluster())
    client = DSecClient()
    await client.open()
    args = DSecContainerRunArgs(
        container_image="registry.../sphinx-9658:official",
        memory_limit_mb=4096, cpu_cores_limit=4,
        ttl_running_stop=300,                      # idle timeout
        network_rules={"npm": False, "pypi": True},
        init_user="root",
    )
    sandbox = await client.run_container(args, timeout=120)
    result = await sandbox.run_shell("echo hello world")
    await sandbox.stop()

asyncio.run(main())
```

`examples/demo_minimal.py` runs this listing against an in-process cluster.

## Layout

```
dsec/
  client.py        libdsec: unified SDK entry point (§2.1)
  apiserver.py     stateless ingress; sandbox ids encode the owning edge (§3.2)
  iam.py           IAM: nested projects, quotas, bounded delegation (§3.2)
  placement.py     filter + power-of-k-choices placement (§3.2, §7)
  watcher.py       fleet health/load polling; stateless rebuild (§3.2)
  edge.py          node-local admission, provisioning, TTL, reclamation (§3.3)
  aether.py        per-sandbox proxy; terminal-session multiplexing (§3.3)
  chronus.py       shell sessions: exec / fs / http / streaming (§3.3)
  backends/        FnCall, container, microVM, full VM + portable engine (§2.2)
  layers/          versioned layers, overlayfs semantics, EROFS images (§5.1, §5.3)
  storage/         3FS-like remote store + 256 KiB second-level chunk cache (§5.3)
  resources/       CPU QoS (LS/BE, SCHED_IDLE, core scheduling) (§5.2)
                   memory (virtio-pmem DAX, DAMON, balloon FPR) (§5.2)
  rl/              pack_diff, pause/resume, agent-loop decoupling,
                   AppArmor/eBPF-style mitigations (§6)
  cloud.py         cloud bursting with selective offloading (§3.4)
tests/             86 unittest cases incl. end-to-end cluster tests
examples/          runnable demos reproducing the paper's listings & figures
docs/              paper→code mapping and evaluation notes
```

## Demos

| Demo | Reproduces |
|---|---|
| `examples/demo_minimal.py` | Listing 1: a minimal libdsec session |
| `examples/demo_burst.py` | §4.1/§7: burst creation, power-of-k spread, TTL reclamation |
| `examples/demo_layers.py` | §5.1: composable layers vs monolithic rebuild cost (O(m·N)→O(m)) |
| `examples/demo_resources.py` | §8.4 Fig. 12 (memory) and §8.5 Fig. 13 (CPU QoS) replays |
| `examples/demo_ondemand.py` | §5.3/§8.2: EROFS on-demand loading vs eager image pull |
| `examples/demo_rl.py` | §6: agent-loop decoupling, preemption pause/resume, pack_diff |
| `examples/demo_security.py` | §6.4/§6.5: the paper's real agent attacks, blocked & logged |

## Platform notes (what the reference implementation does differently)

This is a paper-faithful *reference* implementation, not the production
cluster. The important concessions, all documented in
`docs/IMPLEMENTATION.md`:

- **Execution**: sandbox commands run through a portable `subprocess` engine
  inside the composed rootfs. On hosts with Docker/QEMU/Firecracker, the
  corresponding backends detect and use them.
- **No kernel EROFS/overlayfs**: overlay merge + whiteouts + copy-up are
  implemented in pure Python (`dsec/layers/overlay.py`); EROFS on-demand
  loading is implemented as local metadata + 256 KiB chunk fetch through a
  second-level cache (`dsec/layers/erofs.py`). Sandbox creation defaults to
  eager materialization so shell commands see a complete rootfs; pass
  `labels={"image_loading": "ondemand"}` for the lazy path.
- **3FS**: modeled as a content-addressed remote store with the paper's
  asymmetric I/O profile (bulk reads fast, small random I/O penalized).
- **Kernel QoS**: the exact mechanisms (SCHED_IDLE, PR_SCHED_CORE, madvise,
  AppArmor profiles, eBPF allowlists) are applied on Linux; elsewhere the same
  policies run through deterministic models calibrated to the paper's
  measured anchors (§8.4: −40.2%/−21.2%; §8.5: 45.2%→17.3%).
