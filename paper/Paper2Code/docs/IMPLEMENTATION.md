# Implementation notes — paper → code mapping

How each mechanism of arXiv:2609.22978 maps to this repository, plus the
engineering decisions made where the production system cannot be reproduced
directly on a development host.

## §2 Overview and SDK

| Paper | Code | Notes |
|---|---|---|
| Unified SDK entry point, caller picks backend (§2.1) | `dsec/client.py` `DSecClient.run_container/run_microvm/run_fncall/run_fullvm` | |
| Listing 1 minimal session | `examples/demo_minimal.py` | identical argument names (`container_image`, `memory_limit_mb`, `cpu_cores_limit`, `ttl_running_stop`, `network_rules`, `init_user`) |
| FnCall: stateless tasks in precreated containers; shared/exclusive GPU (§2.2, §7) | `dsec/backends/fncall.py` | MIG partition accounting (7 slices/GPU), warm import pool, best-effort task-state cleanup |
| Container backend (§2.2) | `dsec/backends/container.py` | Docker CLI used when a daemon exists; otherwise the portable engine over the composed rootfs |
| MicroVM backend: Firecracker (§2.2) | `dsec/backends/microvm.py` | Firecracker lifecycle modeled: snapshot→terminate→restore on pause/resume; guest memory registered with the §5.2 accounting |
| Full VM backend: QEMU, COTS OS (§2.2, §3.3) | `dsec/backends/fullvm.py` | prepared VM image instead of composed layers; virtio-gpu/DXVK noted; QEMU integration point |
| Stateful sessions; TTL/stop reclamation (§2.3) | `dsec/edge.py` `_ttl_pass` | `ttl_running_stop` idle timeout + `ttl_absolute` hard cap |
| Scale anchors (§2.4) | `dsec/__init__.py` `PAPER_SCALE` | printed by `examples/demo_burst.py` |

## §3 Platform architecture

| Paper | Code | Notes |
|---|---|---|
| Request path IAM→placement→apiserver→edge→aether→chronus (§3.1) | `dsec/apiserver.py` `create_sandbox`; `dsec/edge.py`; `dsec/aether.py`; `dsec/chronus.py` | |
| IAM: multi-level nested projects, delegation bounded by parent, quotas, humans/agents same API (§3.2) | `dsec/iam.py` | `Quota.remaining()`, `Project.grant` refuses to grant what the grantor does not hold; subproject quota ≤ parent remaining |
| Apiserver stateless; sandbox id encodes owning edge; horizontal scale (§3.2) | `dsec/idgen.py`, `dsec/apiserver.py` | id format `dsec-<edge hex>-<seq>-<rand>`; routing is `idgen.owning_edge()` with no per-sandbox state in the ingress |
| Placement: filter (health/capabilities) + least-loaded of k random (§3.2) | `dsec/placement.py` | GPU/backend filtering; power-of-k; per-instance in-flight overlay; `penalize()` on edge rejection |
| Watcher: periodic probes, stateless rebuild (§3.2) | `dsec/watcher.py` | `collect_once()` rebuilds the view from scratch; no durable state |
| Edge: local admission, eBPF network policy, provisioning, TTL (§3.3, §7) | `dsec/edge.py` | admission counters (CPU overcommit ×16, memory ×2, sandbox count); rejection raises `AdmissionError` so the apiserver re-places |
| Aether: edge↔sandbox channel, terminal-session id → chronus, session end kills the process tree (§3.3) | `dsec/aether.py` | SDK-issued session tokens; forged chronus RPCs rejected and logged |
| Chronus: exec/fs/http/streaming; multiple concurrent sessions (§3.3) | `dsec/chronus.py` | output capture budget (the `yes` incident, §6.4) |
| Base images on 3FS; OCI→EROFS (metadata/data split); OverlayBD for microVM disks (§3.3) | `dsec/layers/erofs.py`, `dsec/storage/store.py` | |
| Cloud bursting: offload >80% util; eligibility = deps ⊆ shared dedup set (§3.4) | `dsec/cloud.py` | |

## §5 Core mechanisms

| Paper | Code | Notes |
|---|---|---|
| Composable layers: base+workspace+toolkit stacked, overlayfs merge + whiteouts + writable upper; O(m)/O(k) upgrades (§5.1) | `dsec/layers/overlay.py`, `dsec/layers/compose.py` | `OverlayFS` implements priority merge, `.wh.*` whiteouts, opaque dirs, copy-up, materialize, diff/deletions; `layered_rebuild_cost` vs `monolithic_rebuild_cost` reproduce Fig. 4 |
| Layer collapsing under 3 GB, whiteout preservation, file-backed mounts (§5.3) | `dsec/layers/compose.py` `collapse_layers` | |
| EROFS: read-only, compressed, random access (§5.1) | `dsec/layers/erofs.py` | per-256 KiB-chunk zlib compression, content-addressed dedup, range reads |
| Memory: virtio-pmem+DAX shared host page cache; DAMON cold-page eviction; balloon FPR order-9 → madvise DONTNEED; struct-page cost 1/64 (§5.2) | `dsec/resources/memory.py` | deterministic per-guest model + `madvise_dontneed` on Linux; `firecracker_workload()` replays Fig. 12 (calibrated to −40.2% peak / −21.2% integral anchors) |
| CPU QoS: BE→SCHED_IDLE; core scheduling for LS (§5.2) | `dsec/resources/cpu.py` | real `sched_setscheduler(SCHED_IDLE)` + `prctl(PR_SCHED_CORE)` on Linux; contention model anchored to Fig. 13 (45.2%→17.3% at 50% load) |
| Image distribution: writes local, bulk reads, metadata local (§5.3) | `dsec/storage/store.py` | asymmetric I/O model; second-level 256 KiB chunk cache survives page-cache eviction |
| dockerd dynamic lower-layer insertion (~30 lines Go) (§7) | `dsec/backends/container.py` `_compose_rootfs` | insertion at creation, logged per sandbox |

## §6 RL co-design

| Paper | Code | Notes |
|---|---|---|
| pack_diff: incremental snapshot → reusable environment (§6.1) | `dsec/rl/packdiff.py` | diff of the writable layer vs the composed stack with per-directory whiteouts; published as an immutable layer |
| Builder/runtime account separation; residual cleanup before packing (§6.1) | `dsec/rl/packdiff.py`, `dsec/iam.py` (`pack.diff` op) | reference-answer files stripped (`_is_residual`) |
| Agent loop outside the preemptible GPU pool: agent sandbox + worker container as single source of truth; reconnect, no command-log replay (§6.2) | `dsec/rl/agentloop.py` | `WorkerContainer.detach/attach`, `RolloutState.replayed_commands() == 0` |
| Preemption pause: containers `docker pause` + swap + `memory.reclaim`; resume MADV_WILLNEED + unpause. MicroVMs: snapshot, kill Firecracker, restore (§6.3) | `dsec/rl/pause.py`, backends' `pause/resume` | transparent resume before any operation (edge) |
| Misbehavior: forged chronus RPCs, log scraping, /bin/bash overwrite, XFS_IOC_SWAPEXT, /proc/kpagecgroup kernel bug, `yes` output flood (§6.4) | `dsec/rl/security.py`, `dsec/chronus.py` | each attack reproduced in `tests/test_e2e.py` / `examples/demo_security.py` and recorded in the misbehavior log |
| AppArmor file/socket control; eBPF per-sandbox network allowlist; dynamic policy updates (§6.5) | `dsec/rl/security.py` | protected-path registry + profile generator + deny-by-default allowlist (pypi/npm/github/mirrors) + eBPF-style rule rendering |

## Reference-implementation concessions

1. **Execution substrate.** Without Docker/Firecracker/QEMU on the host,
   commands run through `subprocess` in the materialized rootfs
   (`dsec/backends/process.py`) — the container/microVM backends keep their
   distinct lifecycle, storage, and memory semantics, but the syscall-level
   sandbox is host-process isolation plus the enforced file/network policies.
2. **No kernel overlayfs/EROFS.** The union semantics and the lazy image path
   are pure-Python implementations. Consequently sandbox creation defaults to
   eager rootfs materialization (`labels={"image_loading": "eager"}`) so
   shell commands see a complete tree; `"ondemand"` activates the genuine
   lazy path (file API fetches only touched files from the 3FS model, with
   256 KiB chunk caching and readahead).
3. **3FS is modeled**, not connected: a content-addressed store with the
   paper's asymmetric I/O cost profile. The same interface could back onto a
   real 3FS FUSE mount or an object store.
4. **Kernel QoS is config-driven** (the paper: "no kernel modifications").
   On Linux the real syscalls fire; elsewhere the deterministic models carry
   the policy and the measured anchors.
5. **Cluster is in-process.** Edges/watcher/placement/apiserver are objects in
   one process with real message flow between them; the wire codec
   (`dsec/proto.py`) is transport-ready.
