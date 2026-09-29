"""Agent-loop decoupling from preemptible GPU training (paper §6.2).

Training jobs in the GPU cluster are routinely preempted. In earlier pipelines
the agent loop ran inside the preemptible GPU training pod together with
model-serving and the RL framework: when the GPU job was preempted, the agent
loop was lost while the sandbox persisted, and recovery relied on replaying a
command log — completed operations reused recorded results to avoid duplicate
side effects from non-idempotent commands.

Starting with DeepSeek-V4.1, rollout execution moves onto DSec and splits into
two components, both outside the preemptible GPU pool:

- the **agent sandbox** hosts the scaffold (e.g. DeepSeek Harness) and its tools;
- the **worker container** manages the sandbox and provides a scaffold-agnostic
  control layer for the rollout.

The worker container and agent sandbox jointly retain the complete rollout
state and act as its single source of truth: a preempted GPU job reconnects and
continues without reconstructing execution through command-log replay.
"""
from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class RolloutState:
    """The single source of truth for a rollout (paper §6.2)."""

    trajectory: List[dict] = field(default_factory=list)  # steps: action/observation pairs
    step: int = 0
    checkpoint: Dict[str, str] = field(default_factory=dict)
    done: bool = False

    def record(self, action: dict, observation: dict, reward: Optional[float] = None) -> None:
        entry = {"step": self.step, "action": action, "observation": observation}
        if reward is not None:
            entry["reward"] = reward
        self.trajectory.append(entry)
        self.step += 1

    def replayed_commands(self) -> int:
        """Command-log replay count — always 0 in the decoupled design."""
        return 0


class WorkerContainer:
    """Scaffold-agnostic control layer for one rollout (paper §6.2)."""

    def __init__(self, job_id: str, agent_sandbox, rollouts_dir: str = "/workspace/rollouts"):
        self.job_id = job_id
        self.agent_sandbox = agent_sandbox  # the DSec sandbox hosting the scaffold
        self.rollouts_dir = rollouts_dir
        self.state = RolloutState()
        self.attached_trainer: Optional["Trainer"] = None
        self.worker_token = secrets.token_hex(16)

    async def step(self, action: dict) -> dict:
        """Execute one agent step against the sandbox; state is retained here."""
        command = action.get("command", "true")
        timeout = action.get("timeout", 60.0)
        result = await self.agent_sandbox.run_shell(command, timeout=timeout)
        observation = {
            "exit_code": result.exit_code,
            "stdout": result.text(),
            "stderr": result.text("stderr"),
            "truncated": result.truncated,
        }
        reward = action.get("reward")  # verifier-provided, if any
        self.state.record(action, observation, reward)
        return observation

    async def checkpoint(self) -> str:
        """Persist the rollout state (single source of truth)."""
        token = secrets.token_hex(8)
        self.state.checkpoint[token] = self.state.step
        return token

    def detach(self) -> None:
        """Trainer preempted: the worker keeps the rollout state and lives on."""
        self.attached_trainer = None

    def attach(self, trainer: "Trainer", job_token: str) -> bool:
        """A (new) trainer reconnects; no command-log replay is needed."""
        if trainer.job_token != job_token:
            return False
        self.attached_trainer = trainer
        return True


class Trainer:
    """The preemptible GPU side: connects to workers via a job token."""

    def __init__(self, job_id: str, job_token: str):
        self.job_id = job_id
        self.job_token = job_token
        self.worker: Optional[WorkerContainer] = None

    def connect(self, worker: WorkerContainer) -> bool:
        return worker.attach(self, self.job_token)


class AgentLoopController:
    """Coordinates trainer <-> worker pairs for a training job."""

    def __init__(self):
        self.workers: Dict[str, WorkerContainer] = {}

    def register(self, worker: WorkerContainer) -> None:
        self.workers[worker.job_id] = worker

    def find(self, job_id: str) -> Optional[WorkerContainer]:
        return self.workers.get(job_id)
