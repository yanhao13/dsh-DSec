"""Tests for backends: process engine, microVM snapshots, FnCall pools."""
import asyncio
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.backends.fncall import FnCallPool
from dsec.backends.microvm import MicroVMBackend
from dsec.backends.process import DEFAULT_OUTPUT_CAP, ProcessEngine
from dsec.types import FnCallTask, SandboxSpec
from dsec.backends.base import SandboxContext
from dsec.layers.layer import Layer
from dsec.layers.registry import LayerRegistry
from dsec.metrics import Metrics
from dsec.resources.memory import MemoryManager
from dsec.storage.store import ChunkCache, RemoteStore


class TestProcessEngine(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.mkdtemp(prefix="dsec-proc-")
        os.makedirs(os.path.join(self.tmp, "work"), exist_ok=True)
        with open(os.path.join(self.tmp, "work", "hello.txt"), "w") as fh:
            fh.write("hi")

    async def test_shell_exec_and_state(self):
        engine = ProcessEngine(self.tmp)
        r = await engine.run_shell_cmd("echo hello")
        self.assertEqual(r.exit_code, 0)
        self.assertEqual(r.text().strip(), "hello")

    async def test_cwd_inside_rootfs(self):
        engine = ProcessEngine(self.tmp)
        r = await engine.run_shell_cmd("cat work/hello.txt")
        self.assertEqual(r.text(), "hi")

    async def test_output_cap_kills_yes(self):
        # The `yes` case (paper §6.4): unbounded output is cut and killed.
        engine = ProcessEngine(self.tmp, output_cap=4096)
        r = await engine.run_shell_cmd("yes", timeout=30)
        self.assertTrue(r.truncated)
        self.assertLessEqual(len(r.stdout), 4096)

    async def test_timeout(self):
        from dsec.errors import SandboxTimeout

        engine = ProcessEngine(self.tmp)
        with self.assertRaises(SandboxTimeout):
            await engine.run_shell_cmd("sleep 5", timeout=0.2)

    async def test_path_escape_rejected(self):
        from dsec.backends.base import SandboxContext
        from dsec.backends.process import ProcessBackend

        backend = ProcessBackend()
        ctx = SandboxContext(sandbox_id="sb", spec=SandboxSpec(backend="container", image="x"),
                             rootfs_dir=self.tmp, security=None)
        with self.assertRaises(PermissionError):
            await backend.read_file(ctx, "../../etc/hosts", 100)

    async def asyncTearDown(self):
        import shutil

        shutil.rmtree(self.tmp, ignore_errors=True)


class TestMicroVM(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.mkdtemp(prefix="dsec-vm-")
        self.store = RemoteStore()
        self.cache = ChunkCache()
        self.registry = LayerRegistry(self.store, self.cache)
        self.registry.publish(Layer("base", "v1", "base", {
            "etc/os": b"TestOS",
            "app/run.py": b"print('run')\n",
        }))
        self.memory = MemoryManager(host_memory_mb=8192)
        self.backend = MicroVMBackend()

    def make_ctx(self, sandbox_id="vm-1"):
        return SandboxContext(
            sandbox_id=sandbox_id,
            spec=SandboxSpec(backend="microvm", image="base:v1",
                             labels={"image_loading": "eager"}),
            rootfs_dir=os.path.join(self.tmp, sandbox_id),
            metrics=Metrics(), cpu_qos=None, memory=self.memory,
            security=None, chunk_cache=self.cache, store=self.store,
            metadata={
                "layer_stack": [self.registry.get_layer("base", "v1")],
                "erofs_images": [self.registry.get_image("base", "v1")],
            },
        )

    async def test_create_run_snapshot_pause_resume(self):
        ctx = self.make_ctx()
        await self.backend.create(ctx)
        r = await self.backend.run_shell(ctx, "cat etc/os")
        self.assertEqual(r.text(), "TestOS")
        # Stateful write, then pause (snapshot + Firecracker termination).
        await self.backend.write_file(ctx, "new.txt", b"state", 0o644)
        await self.backend.pause(ctx)
        self.assertEqual(ctx.state, "paused")
        self.assertNotIn("vm-1", self.memory.guests)  # runtime memory released
        # Transparent resume on next operation.
        await self.backend.resume(ctx)
        self.assertEqual(ctx.state, "running")
        self.assertEqual(await self.backend.read_file(ctx, "new.txt", 100), b"state")
        await self.backend.destroy(ctx)
        self.assertEqual(ctx.state, "stopped")

    async def test_guest_memory_registered_with_pmem_and_fpr(self):
        ctx = self.make_ctx()
        await self.backend.create(ctx)
        guest = self.memory.guests["vm-1"]
        self.assertTrue(guest.pmem_dax)
        self.assertTrue(guest.fpr_enabled)
        await self.backend.destroy(ctx)
        self.assertNotIn("vm-1", self.memory.guests)


class TestFnCallPool(unittest.IsolatedAsyncioTestCase):
    async def test_shared_cpu_pool_executes_and_cleans_task_state(self):
        pool = FnCallPool(kind="cpu", size=2)
        await pool.start()
        try:
            task = FnCallTask(task_type="oj", command="python3 -c 'print(42)'",
                              files={"task/in.py": b"x=1\n"})
            result = await pool.submit(task)
            self.assertEqual(result.exit_code, 0)
            self.assertIn("42", result.text())
            # Best-effort cleanup removed the task files (paper §3.1).
            for slot in pool.slots:
                if not slot.busy:
                    self.assertFalse(os.path.exists(os.path.join(slot.scratch, "task", "in.py")))
        finally:
            await pool.stop()

    async def test_exclusive_gpu_mode_uses_mig_instances(self):
        pool = FnCallPool(kind="gpu", gpu_mode="exclusive", gpu_instances=1,
                          mig_per_gpu=2, size=2)
        await pool.start()
        try:
            async def run_one(n):
                task = FnCallTask(task_type="op", command="python3 -c 'import time; time.sleep(0.05); print(%d)'" % n,
                                  gpu=True, gpu_mode="exclusive")
                return await pool.submit(task)

            r1, r2 = await asyncio.gather(run_one(1), run_one(2))
            self.assertEqual(r1.exit_code, 0)
            self.assertEqual(r2.exit_code, 0)
            self.assertEqual(len(pool._instance_owners), 0)  # released after
        finally:
            await pool.stop()


if __name__ == "__main__":
    unittest.main()
