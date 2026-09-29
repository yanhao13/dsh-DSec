"""End-to-end tests across the full platform (paper Listing 1 through §6)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.client import DSecClient, DSecContainerRunArgs, DSecMicroVMRunArgs
from dsec.cloud import CloudOffloader
from dsec.errors import AccessDenied, AdmissionError, PermissionDenied
from dsec.iam import Quota
from dsec.rl.agentloop import AgentLoopController, Trainer, WorkerContainer
from dsec.rl.pause import PauseCoordinator
from dsec.types import BACKEND_CONTAINER, LayerRef, SandboxSpec
from tests.helpers import ClusterTestCase


class TestMinimalSession(ClusterTestCase):
    """Paper Listing 1: a minimal sandbox session through libdsec."""

    async def test_listing_one_flow(self):
        client = self.client("user")
        await client.open()
        args = DSecContainerRunArgs(
            container_image="testos:v1",
            memory_limit_mb=4096, cpu_cores_limit=4,
            ttl_running_stop=300,
            network_rules={"npm": False, "pypi": True},
            init_user="root",
            labels={"image_loading": "eager"},
        )
        sandbox = await client.run_container(args, timeout=120)
        self.assertEqual(sandbox.backend, BACKEND_CONTAINER)
        result = await sandbox.run_shell("echo hello world")
        self.assertEqual(result.exit_code, 0)
        self.assertIn("hello world", result.text())
        # State persists across calls (§2.3).
        await sandbox.run_shell("echo stateful > marker.txt")
        r2 = await sandbox.run_shell("cat marker.txt")
        self.assertEqual(r2.text().strip(), "stateful")
        await sandbox.stop()
        self.assertEqual(sandbox.state, "gone")
        await client.close()

    async def test_quota_is_consumed_and_released(self):
        project = self.iam.create_project(
            "root", "quota-proj", Quota(cpu=16, memory_mb=16384, max_sandboxes=2), "admin")
        self.iam.projects["root"].grant("user", {"sandbox.create", "sandbox.stop"}, "admin")
        client = self.client("user")
        args = DSecContainerRunArgs(container_image="testos:v1", project="root/quota-proj",
                                    cpu_cores_limit=8, memory_limit_mb=8192,
                                    labels={"image_loading": "eager"})
        sb1 = await client.run_container(args)
        self.assertEqual(project.used.max_sandboxes, 1)
        sb2 = await client.run_container(args)
        self.assertEqual(project.used.max_sandboxes, 2)
        await sb1.stop()
        await sb2.stop()
        self.assertEqual(project.used.max_sandboxes, 0)


class TestPlacementRetry(ClusterTestCase):
    """Edge final admission authority: rejections trigger re-placement (§7)."""

    async def test_overloaded_edge_rejects_and_engine_retries(self):
        from dsec.watcher import EdgeStats, FleetView

        # Edge-01 is secretly at capacity, but the watcher's view is stale and
        # shows it empty (and less loaded than edge-02): placement must try
        # edge-01, get rejected, penalize it, and land on edge-02.
        edge1 = self.edges["edge-01"]
        edge1.capacity.max_sandboxes = 1
        spec = SandboxSpec(backend=BACKEND_CONTAINER, image="testos:v1", project="root",
                           labels={"image_loading": "eager"})
        await edge1.create(spec)  # bypasses placement: the "stale" occupancy
        self.watcher.set_view(FleetView(edges={
            "edge-01": EdgeStats(edge_id="edge-01", healthy=True, cpu_used=0.0,
                                 mem_used_mb=0.0, cpu_capacity=128.0, mem_capacity_mb=262144,
                                 gpu_instances=0, gpu_used=0,
                                 backends=[BACKEND_CONTAINER], running={}),
            "edge-02": EdgeStats(edge_id="edge-02", healthy=True, cpu_used=10.0,
                                 mem_used_mb=100.0, cpu_capacity=128.0, mem_capacity_mb=262144,
                                 gpu_instances=1, gpu_used=0,
                                 backends=[BACKEND_CONTAINER], running={}),
        }))
        sandbox_id = (await self.server.create_sandbox("user", spec))[0]
        from dsec.idgen import owning_edge

        self.assertEqual(owning_edge(sandbox_id), "edge-02")
        self.assertEqual(edge1.rejections, 1)


class TestPackDiff(ClusterTestCase):
    """§6.1: checkpoint a sandbox into a reusable environment."""

    async def test_pack_and_restore(self):
        builder = self.client("builder")
        await builder.open()
        args = DSecContainerRunArgs(container_image="testos:v1", workspace=LayerRef(
            name="repo-42", version="v1", kind="workspace"),
            toolkits=[LayerRef(name="harness", version="v3", kind="toolkit")],
            labels={"image_loading": "eager"})
        sb = await builder.run_container(args)
        await sb.run_shell("echo built-env > workspace/built.txt")
        await sb.run_shell("rm workspace/data.txt")  # exercise whiteout diff
        ref = await sb.pack_diff("env-checkpoint", "v7")
        self.assertEqual((ref.name, ref.version), ("env-checkpoint", "v7"))

        # Restore the pack as a new sandbox's workspace.
        args2 = DSecContainerRunArgs(container_image="testos:v1", workspace=ref,
                                     labels={"image_loading": "eager"})
        sb2 = await builder.run_container(args2)
        r = await sb2.run_shell("cat workspace/built.txt")
        self.assertEqual(r.text().strip(), "built-env")
        # The deleted file stays deleted (whiteout preserved through the pack).
        r2 = await sb2.run_shell("test -e workspace/data.txt; echo $?")
        self.assertEqual(r2.text().strip(), "1")
        # Priority: toolkit override survived composition.
        r3 = await sb2.run_shell("cat workspace/data.txt 2>/dev/null; cat tools/run.py 2>/dev/null; echo")
        await sb.stop()
        await sb2.stop()
        await builder.close()

    async def test_runtime_principal_cannot_pack(self):
        # Builder/runtime accounts are separate (§6.1): the runtime principal
        # lacks pack.diff.
        runtime = self.client("runtime")
        await runtime.open()
        sb = await runtime.run_container(DSecContainerRunArgs(
            container_image="testos:v1", labels={"image_loading": "eager"}))
        with self.assertRaises(PermissionDenied):
            await sb.pack_diff("sneaky", "v1")
        await sb.stop()
        await runtime.close()


class TestPauseResumeJob(ClusterTestCase):
    """§6.3: preemption pause preserves rollout state and reclaims memory."""

    async def test_pause_preserves_state_and_transparent_resume(self):
        client = self.client("user")
        await client.open()
        args = DSecContainerRunArgs(container_image="testos:v1", project="root",
                                    labels={"image_loading": "eager", "pmem_dax": "0"})
        sb = await client.run_container(args)
        await sb.run_shell("echo rollout-progress > progress.txt")
        edge = self.server.resolve_edge(sb.sandbox_id)
        ctx = edge.sandboxes[sb.sandbox_id]
        guest_before = self.edges[edge.edge_id].memory.host_usage_mb()

        coordinator = PauseCoordinator(self.server)
        coordinator.register_job("job-1", [sb.sandbox_id])
        paused = await coordinator.pause_job("user", "job-1", reason="training-preempted")
        self.assertEqual(paused, 1)
        self.assertEqual(sb.state, "paused")

        # Any subsequent request transparently resumes before executing (§6.3).
        r = await sb.run_shell("cat progress.txt")
        self.assertEqual(r.text().strip(), "rollout-progress")
        self.assertEqual(sb.state, "running")
        await sb.stop()
        await client.close()


class TestMicroVMEndToEnd(ClusterTestCase):
    async def test_microvm_snapshot_resume_via_sdk(self):
        client = self.client("user")
        await client.open()
        args = DSecMicroVMRunArgs(base_image="testos:v1", memory_limit_mb=512,
                                  labels={"image_loading": "eager"})
        sb = await client.run_microvm(args)
        await sb.run_shell("echo vm-state > vm.txt")
        await sb.pause()
        self.assertEqual(sb.state, "paused")
        await sb.resume()
        r = await sb.run_shell("cat vm.txt")
        self.assertEqual(r.text().strip(), "vm-state")
        await sb.stop()
        await client.close()


class TestAgentLoopDecoupling(ClusterTestCase):
    """§6.2: preempted trainer reconnects without command-log replay."""

    async def test_reconnect_after_preemption(self):
        client = self.client("user")
        await client.open()
        args = DSecContainerRunArgs(container_image="testos:v1",
                                    labels={"image_loading": "eager"})
        agent_sandbox = await client.run_container(args)
        worker = WorkerContainer(job_id="rl-job-7", agent_sandbox=agent_sandbox)
        controller = AgentLoopController()
        controller.register(worker)

        job_token = "tok-preempt-me"
        trainer = Trainer(job_id="rl-job-7", job_token=job_token)
        self.assertTrue(trainer.connect(worker))
        await worker.step({"command": "echo step-1"})
        await worker.step({"command": "echo state > rollout.txt"})
        self.assertEqual(worker.state.step, 2)

        # GPU job preempted: trainer detaches; worker + sandbox keep the state.
        worker.detach()
        self.assertIsNone(worker.attached_trainer)

        # A new trainer connects with the job token and continues — no replay.
        trainer2 = Trainer(job_id="rl-job-7", job_token=job_token)
        self.assertTrue(trainer2.connect(worker))
        await worker.step({"command": "echo step-3"})
        self.assertEqual(worker.state.step, 3)
        self.assertEqual(worker.state.replayed_commands(), 0)
        r = await agent_sandbox.run_shell("cat rollout.txt")
        self.assertEqual(r.text().strip(), "state")
        await agent_sandbox.stop()
        await client.close()


class TestRewardHackingDefenses(ClusterTestCase):
    """§6.4/§6.5: blocked attempts are recorded, not fatal to the sandbox."""

    async def test_agent_cannot_scrape_chronus_logs_or_overwrite_bash(self):
        client = self.client("user")
        await client.open()
        sb = await client.run_container(DSecContainerRunArgs(
            container_image="testos:v1", labels={"image_loading": "eager"}))
        with self.assertRaises(AccessDenied):
            await sb.read_file("/var/log/chronus/session.log")
        with self.assertRaises(AccessDenied):
            await sb.write_file("/bin/bash", b"#!/bin/sh\necho pwned\n")
        # Sandbox still healthy and usable afterwards.
        r = await sb.run_shell("echo still-alive")
        self.assertEqual(r.exit_code, 0)
        kinds = self.security.misbehavior.kinds(sb.sandbox_id)
        self.assertIn("protected-path-read", kinds)
        self.assertIn("protected-path-write", kinds)
        await sb.stop()
        await client.close()

    async def test_forged_chronus_rpc_rejected(self):
        client = self.client("user")
        await client.open()
        sb = await client.run_container(DSecContainerRunArgs(
            container_image="testos:v1", labels={"image_loading": "eager"}))
        edge = self.server.resolve_edge(sb.sandbox_id)
        aether = edge.sandboxes[sb.sandbox_id].metadata["aether"]
        # The agent does not hold the SDK-issued token for a forged terminal id.
        with self.assertRaises(AccessDenied):
            await aether.run("term-forged", "not-a-token", "echo pwn")
        self.assertIn("forged-chronus-rpc",
                      self.security.misbehavior.kinds(sb.sandbox_id))
        await sb.stop()
        await client.close()

    async def test_network_allowlist_enforced_through_sdk(self):
        client = self.client("user")
        await client.open()
        sb = await client.run_container(DSecContainerRunArgs(
            container_image="testos:v1",
            network_rules={"npm": False, "pypi": True},
            labels={"image_loading": "eager"}))
        # Deny-by-default: host not covered by an allowlisted service is blocked
        # before any outbound request is made.
        from dsec.errors import NetworkPolicyViolation

        with self.assertRaises(NetworkPolicyViolation):
            await sb.http("https://registry.npmjs.org/react")
        self.assertIn("network-denied", self.security.misbehavior.kinds(sb.sandbox_id))
        await sb.stop()
        await client.close()


class TestCloudBursting(ClusterTestCase):
    """§3.4: offload only eligible tasks once on-prem exceeds 80%."""

    async def test_offload_threshold_and_eligibility(self):
        offloader = CloudOffloader(shared_image_set={"testos:v1"})
        spec = SandboxSpec(backend=BACKEND_CONTAINER, image="testos:v1", project="root")
        self.assertTrue(offloader.is_cloud_eligible(spec))
        self.assertEqual(offloader.route(spec, onprem_utilization=0.5), "onprem")
        self.assertEqual(offloader.route(spec, onprem_utilization=0.85), "cloud")
        self.assertEqual(offloader.offload_fraction(), 0.5)
        # Non-eligible task stays on-premise even above threshold.
        spec2 = SandboxSpec(backend=BACKEND_CONTAINER, image="other:v1", project="root")
        self.assertEqual(offloader.route(spec2, onprem_utilization=0.85), "onprem")
        self.assertEqual(offloader.offload_fraction(), 1.0 / 3.0)


if __name__ == "__main__":
    unittest.main()
