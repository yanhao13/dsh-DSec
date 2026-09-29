#!/usr/bin/env python3
"""RL-framework co-design (paper §6): agent-loop decoupling, preemption
pause/resume, pack_diff environment checkpointing, cloud bursting.

- §6.2: the agent loop lives outside the preemptible GPU pool — an agent
  sandbox (scaffold) plus a worker container (control layer) jointly retain the
  rollout state as its single source of truth, so a preempted trainer
  reconnects without command-log replay.
- §6.3: on preemption the framework pauses all job sandboxes, reclaiming
  memory while preserving state; the next request transparently resumes them.
- §6.1: pack_diff turns an interactive session into a reusable environment.
- §3.4: cloud bursting offloads eligible tasks above the 80% threshold.
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _common import hr, make_cluster, teardown  # noqa: E402
from dsec.client import DSecContainerRunArgs  # noqa: E402
from dsec.cloud import CloudOffloader  # noqa: E402
from dsec.rl.agentloop import AgentLoopController, Trainer, WorkerContainer  # noqa: E402
from dsec.rl.pause import PauseCoordinator  # noqa: E402
from dsec.types import LayerRef, SandboxSpec  # noqa: E402


async def main():
    cluster = make_cluster(n_edges=2, gpu_edges=1)
    client = cluster["clients"]["user"]
    builder = cluster["clients"]["builder"]
    await client.open()

    hr("§6.2 — agent loop decoupled from preemptible GPU training")
    # The builder principal owns the sandbox and holds the pack.diff grant
    # (§6.1: builder/runtime account separation).
    agent_sandbox = await builder.run_container(DSecContainerRunArgs(
        container_image="demo-os:v1", workspace=LayerRef(
            name="task-repo", version="v1", kind="workspace"),
        labels={"image_loading": "eager"}))
    worker = WorkerContainer(job_id="rl-job-42", agent_sandbox=agent_sandbox)
    AgentLoopController().register(worker)
    job_token = "job-token-42"
    trainer = Trainer(job_id="rl-job-42", job_token=job_token)
    assert trainer.connect(worker)

    await worker.step({"command": "echo step-1 > rollout.txt"})
    await worker.step({"command": "echo step-2 >> rollout.txt"})
    print("rollout steps so far:", worker.state.step)

    print("GPU training job preempted -> trainer detaches; worker + sandbox persist")
    worker.detach()
    trainer2 = Trainer(job_id="rl-job-42", job_token=job_token)
    assert trainer2.connect(worker)
    await worker.step({"command": "echo step-3 >> rollout.txt"})
    print("new trainer attached; total steps:", worker.state.step,
          "| command-log replays:", worker.state.replayed_commands())
    r = await agent_sandbox.run_shell("cat rollout.txt")
    print("rollout state (single source of truth):", r.text().strip().replace("\n", " / "))

    hr("§6.3 — preemption pause: reclaim memory, preserve state")
    coordinator = PauseCoordinator(cluster["server"])
    coordinator.register_job("rl-job-42", [agent_sandbox.sandbox_id])
    paused = await coordinator.pause_job("user", "rl-job-42", reason="training-preempted")
    print("paused %d sandbox(es); state: %s" % (paused, agent_sandbox.state))
    r = await agent_sandbox.run_shell("cat rollout.txt")  # transparent resume
    print("transparent resume on next request ->", r.text().strip().replace("\n", " / "),
          "| state:", agent_sandbox.state)

    hr("§6.1 — pack_diff: checkpoint the session into a reusable environment")
    ref = await agent_sandbox.pack_diff("agent-built-env", "v1")
    print("packed environment layer:", "%s:%s" % (ref.name, ref.version))
    sb2 = await builder.run_container(DSecContainerRunArgs(
        container_image="demo-os:v1", workspace=ref, labels={"image_loading": "eager"}))
    r = await sb2.run_shell("cat rollout.txt")
    print("restored sandbox sees the packed state:", r.text().strip().replace("\n", " / "))
    await sb2.stop()
    await agent_sandbox.stop()

    hr("§3.4 — cloud bursting above the 80% utilization threshold")
    offloader = CloudOffloader(shared_image_set={"demo-os:v1", "task-repo:v1"})
    results = {"onprem": 0, "cloud": 0}
    for util in (0.5, 0.85):
        for i in range(10):
            spec = SandboxSpec(backend="container",
                               image="demo-os:v1" if i % 2 == 0 else "rare-image:v9")
            results[offloader.route(spec, util)] += 1
    print("on-premise utilization 80%+ -> eligible overflow offloaded:",
          "%d cloud / %d on-prem" % (results["cloud"], results["onprem"]))

    await teardown(cluster)


if __name__ == "__main__":
    asyncio.run(main())
