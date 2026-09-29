# Evaluation notes — reproducing the paper's §8 experiments

The paper evaluates four mechanisms on a 10-node test cluster. This repository
reproduces the same mechanisms and their measured anchors through deterministic
replays; run them with:

```console
$ python3 examples/demo_resources.py     # §8.4 Fig. 12, §8.5 Fig. 13
$ python3 examples/demo_ondemand.py      # §8.2 Fig. 10, Tab. 3
$ python3 examples/demo_layers.py        # §8.3, §5.1 cost model
$ python3 -m unittest tests.test_memory tests.test_cpu tests.test_erofs
```

## §8.2 On-demand image loading (Fig. 10, Tab. 3)

Paper: eager Docker pulling stretches completion by 1.71× and accumulates
~1,600 GB of node disk writes; on-demand EROFS loading plates at ~700 GB
(57% less). Tab. 3: runtime access covers 4.2–13.3% of image data.

Replay (`demo_ondemand.py`): a diverse multi-file image is served to 30
sandboxes under both policies; agents touch ~10% of the files through the
file API. On-demand fetches only the touched files (chunked, cached), eager
extracts everything. The demo prints the per-policy 3FS traffic and extraction
writes; the unit tests assert the fetch granularity (`test_erofs.py`).

## §8.3 Composable layers: EROFS vs tar (Fig. 11)

Paper: tar-based provisioning generates 5.5× the disk writes and 3.4× the peak
throughput of EROFS layer mounting (79 vs 45 minutes, 1.76×).

Replay (`demo_layers.py`): models the write traffic difference analytically
from the shared workspace stack — with tar, every sandbox extracts a full copy
of the workspace; with EROFS, the read-only layers are mounted and only the
writable upper layers hit local disk. The stacking semantics themselves are
unit-tested (`test_overlay.py`, `test_compose.py`).

## §8.4 Memory under overcommit (Fig. 12)

Paper anchors: virtio-pmem+DAX alone −40.2% peak host usage; DAMON+balloon
FPR alone −21.2% time-integrated usage; combined lowest.

Replay (`demo_resources.py`, `test_memory.py`): `firecracker_workload()`
drives 20 microVMs through boot → anonymous allocation → shared base-image
reads → idle, under the four configurations, and measures peak and
time-integrated host usage from the same accounting model the edge uses at
runtime (host page cache sharing, per-guest cache copies, struct-page
metadata = 1/64 of pmem capacity, order-9 balloon reporting). The tests hold
the reductions inside tolerance bands around the paper's anchors, since the
exact figures are workload-mix dependent there too.

## §8.5 CPU QoS under overcommit (Fig. 13)

Paper anchors at 50% background load: unprotected +45.2%, SCHED_IDLE alone
+41.8% (improves by ≤3.4%), SCHED_IDLE + core scheduling +17.3%.

Replay (`demo_resources.py`, `test_cpu.py`): the contention model is linear
in background load with the paper's three anchor points; on Linux hosts the
same policy applies the real kernel mechanisms (SCHED_IDLE, PR_SCHED_CORE
core-scheduling cookies).

## Deployment scale (§2.4, §4.1)

`demo_burst.py` measures a burst's creation rate and power-of-k placement
spread on a simulated fleet, exercises TTL reclamation, and prints the
paper's production anchors (160 nodes, 30K cores, 250 TB DRAM, 3M/day,
380K concurrent, 5K creates/s, 32K-sandbox bursts) for context.
