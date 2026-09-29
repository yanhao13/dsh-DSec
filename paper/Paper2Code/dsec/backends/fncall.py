"""FnCall backend: precreated execution pools (paper §2.2, §7).

FnCall targets short, stateless tasks (OJ workloads, compilation, serverless
programs, GPU kernels, utility code). Tasks run in reusable precreated CPU or
GPU containers, avoiding per-invocation provisioning overhead. For GPU work:

- **shared mode**: multiple containers share a GPU instance, maximizing
  utilization for lightweight workloads;
- **exclusive mode**: one container reserves a GPU instance for its lifecycle
  (performance-sensitive tasks such as operator evaluation);
- **MIG partitioning**: each GPU is partitioned into isolated instances so
  benchmarks run concurrently with exclusive access (paper §7);
- CPU FnCall handles compilation and passes artifacts to GPU FnCall, and a warm
  pool of pre-initialized processes lets requests start executing directly.

FnCall follows a separate request path: it uses neither aether nor chronus
(paper §3.1); the submitted task executes directly in a precreated container
followed by best-effort cleanup of task state.
"""
from __future__ import annotations

import asyncio
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from ..errors import BackendUnavailable, SandboxTimeout
from ..types import FnCallTask, RunResult
from .base import Backend, SandboxContext
from .process import DEFAULT_OUTPUT_CAP, ProcessEngine


@dataclass
class _PoolSlot:
    engine: ProcessEngine
    scratch: str
    busy: bool = False
    gpu_instance: Optional[int] = None


class FnCallPool:
    """Precreated executor pool with shared/exclusive GPU accounting."""

    def __init__(self, kind: str = "cpu", *, gpu_mode: str = "shared",
                 gpu_instances: int = 0, mig_per_gpu: int = 7, size: int = 4,
                 warm_size: int = 0, output_cap: int = DEFAULT_OUTPUT_CAP,
                 warm_imports: Optional[List[str]] = None, metrics=None):
        self.kind = kind
        self.gpu_mode = gpu_mode
        self.gpu_instances = gpu_instances
        self.mig_per_gpu = mig_per_gpu
        self.size = size
        self.output_cap = output_cap
        self.warm_imports = warm_imports or []
        self.metrics = metrics
        self.slots: List[_PoolSlot] = []
        self._instance_owners: Dict[int, str] = {}  # gpu instance -> owner task id
        self._lock = asyncio.Lock()
        self.submitted = 0
        self.queued = 0

    async def start(self) -> None:
        """Precreate the pool; warm processes import libraries in advance (§7)."""
        for i in range(self.size):
            scratch = tempfile.mkdtemp(prefix="dsec-fncall-%s-" % self.kind)
            engine = ProcessEngine(scratch, sandbox_id="fncall-%s-%d" % (self.kind, i),
                                   output_cap=self.output_cap)
            if self.warm_imports:
                imports = "; ".join("import %s" % m for m in self.warm_imports)
                await engine.run(["python3", "-c", imports], timeout=120)
            self.slots.append(_PoolSlot(engine=engine, scratch=scratch))

    async def stop(self) -> None:
        for slot in self.slots:
            slot.engine.kill()
            shutil.rmtree(slot.scratch, ignore_errors=True)
        self.slots.clear()

    def _acquire_gpu(self, task_id: str) -> Optional[int]:
        """Reserve a GPU (MIG) instance for an exclusive task."""
        if self.kind != "gpu" or self.gpu_mode != "exclusive":
            return None
        total = self.gpu_instances * self.mig_per_gpu
        for instance in range(total):
            if instance not in self._instance_owners:
                self._instance_owners[instance] = task_id
                return instance
        return None  # caller must wait

    def _release_gpu(self, task_id: str) -> None:
        for instance, owner in list(self._instance_owners.items()):
            if owner == task_id:
                del self._instance_owners[instance]

    async def submit(self, task: FnCallTask) -> RunResult:
        """Run one stateless task in a precreated executor with cleanup."""
        if self.kind == "gpu" and not self.gpu_instances:
            raise BackendUnavailable("GPU FnCall requested on a CPU-only node")
        self.submitted += 1
        task_id = "task-%d" % self.submitted
        deadline = asyncio.get_event_loop().time() + 30.0
        while True:
            async with self._lock:
                gpu = self._acquire_gpu(task_id)
                if gpu is not None or self.gpu_mode != "exclusive":
                    break
            if asyncio.get_event_loop().time() > deadline:
                raise BackendUnavailable("no GPU instance available for exclusive FnCall")
            self.queued += 1
            await asyncio.sleep(0.01)
        async with self._lock:
            slot = next((s for s in self.slots if not s.busy), None)
            if slot is None:
                # Pool is saturated; execute a transient extra executor.
                scratch = tempfile.mkdtemp(prefix="dsec-fncall-extra-")
                slot = _PoolSlot(engine=ProcessEngine(scratch, output_cap=self.output_cap),
                                 scratch=scratch, busy=True)
                self.slots.append(slot)
            else:
                slot.busy = True
        try:
            # Materialize task dependency files (compilation artifacts path §7).
            scratch_root = Path(slot.scratch)
            scratch_root.mkdir(parents=True, exist_ok=True)
            for rel, data in task.files.items():
                dest = scratch_root / rel.lstrip("/")
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            result = await slot.engine.run_shell_cmd(task.command, timeout=task.timeout)
            if self.metrics is not None:
                self.metrics.inc("fncall_%s_runs" % self.kind)
                self.metrics.inc("fncall_gpu_%s_secs" % self.gpu_mode, result.duration_ms / 1000)
            return result
        except SandboxTimeout:
            raise
        finally:
            # Best-effort cleanup of task state (paper §3.1).
            for rel in task.files:
                try:
                    (scratch_root / rel.lstrip("/")).unlink()
                except OSError:
                    pass
            async with self._lock:
                slot.busy = False
            self._release_gpu(task_id)


class FnCallBackend(Backend):
    """FnCall backend for stateless task execution (paper §2.2)."""

    name = "fncall"

    def __init__(self, cpu_pool: Optional[FnCallPool] = None, gpu_pool: Optional[FnCallPool] = None):
        self.cpu_pool = cpu_pool
        self.gpu_pool = gpu_pool
        self._task_map: Dict[str, FnCallTask] = {}

    async def create(self, ctx: SandboxContext) -> None:
        # FnCall has no per-sandbox environment: the task spec arrives with the
        # first operation; pools are precreated at edge start.
        ctx.set_state("running")

    async def destroy(self, ctx: SandboxContext) -> None:
        self._task_map.pop(ctx.sandbox_id, None)
        ctx.set_state("stopped")

    async def run_shell(self, ctx: SandboxContext, command: str, *, timeout: float = 60.0,
                        env: Optional[Dict[str, str]] = None, stdin: bytes = b"") -> RunResult:
        ctx.touch()
        task = self._task_map.get(ctx.sandbox_id) or FnCallTask(task_type="shell", command=command,
                                                                timeout=timeout)
        task = FnCallTask(task_type=task.task_type, command=command,
                          files=task.files, timeout=timeout,
                          gpu=ctx.spec.gpu, gpu_mode=ctx.spec.gpu_mode)
        self._task_map[ctx.sandbox_id] = task
        pool = self.gpu_pool if task.gpu else self.cpu_pool
        if pool is None:
            raise BackendUnavailable("FnCall pool not provisioned on this edge")
        return await pool.submit(task)

    async def snapshot(self, ctx: SandboxContext) -> dict:
        return {"task": self._task_map.get(ctx.sandbox_id, None)}

    async def restore(self, ctx: SandboxContext, snapshot: dict) -> None:
        task = snapshot.get("task")
        if task is not None:
            self._task_map[ctx.sandbox_id] = task
