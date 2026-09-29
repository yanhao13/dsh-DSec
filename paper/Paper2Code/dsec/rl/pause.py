"""Pause/resume coordination with preemptible RL training (paper §6.3).

GPU-job preemption is inevitable, and sandbox state must remain on DSec until
the rollout completes — but many idle sandboxes would otherwise keep consuming
memory while training is suspended. The RL framework proactively sends pause
requests to all sandboxes associated with a preempted job, letting DSec reclaim
memory while preserving execution state. Any subsequent request to a paused
sandbox transparently resumes it before executing (implemented in the edge).

- **Containers**: docker pause freezes the process tree; the edge then enables
  swapping (memory.swap.max) and triggers proactive reclamation
  (memory.reclaim), reclaiming anonymous and file-backed pages while preserving
  execution state. Resume applies MADV_WILLNEED to the process mappings
  (asynchronous prefetch) and issues docker unpause.
- **MicroVMs**: memory and execution state are saved in a snapshot, then the
  running Firecracker process terminates, releasing runtime memory. Resume
  starts a new process and restores the snapshot.
"""
from __future__ import annotations

from typing import Dict, List

from ..metrics import Metrics


class PauseCoordinator:
    """Batch pause/resume of every sandbox attached to a training job."""

    def __init__(self, server, metrics: Metrics = None):
        self.server = server
        self.metrics = metrics or Metrics(name="pause-coordinator")
        self.jobs: Dict[str, List[str]] = {}  # job_id -> sandbox ids

    def register_job(self, job_id: str, sandbox_ids: List[str]) -> None:
        self.jobs[job_id] = list(sandbox_ids)

    async def pause_job(self, principal: str, job_id: str, reason: str = "training-preempted") -> int:
        """The RL framework's proactive pause on GPU preemption (§6.3)."""
        paused = 0
        for sandbox_id in self.jobs.get(job_id, []):
            try:
                await self.server.pause(principal, sandbox_id)
                paused += 1
            except Exception:
                continue
        self.metrics.inc("pause_events")
        self.metrics.inc("paused_sandboxes", paused)
        return paused

    async def resume_job(self, principal: str, job_id: str) -> int:
        """Training restarts: sandboxes resume transparently on first use.

        Explicit resume issues MADV_WILLNEED prefetch / docker unpause, or
        snapshot restore for microVMs (§6.3).
        """
        resumed = 0
        for sandbox_id in self.jobs.get(job_id, []):
            try:
                await self.server.resume(principal, sandbox_id)
                resumed += 1
            except Exception:
                continue
        self.metrics.inc("resume_events")
        self.metrics.inc("resumed_sandboxes", resumed)
        return resumed

    def active_job_sandboxes(self, job_id: str) -> List[str]:
        return list(self.jobs.get(job_id, []))
