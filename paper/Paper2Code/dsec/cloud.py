"""Cloud bursting with selective offloading (paper §3.4).

DSec uses cloud VMs to absorb transient peaks while serving the steady-state
workload on-premise. When on-premise utilization exceeds 80%, the placement
engine offloads a portion of eligible incoming sandbox creation requests to
cloud VMs. Eligibility follows the image distribution design: a compact,
de-duplicated EROFS image set (30 TB covering the image files accessed by 70%
of container tasks) is synchronized offline to the cloud filesystem; container
tasks whose image dependencies are fully contained in that set are
cloud-eligible, and other tasks remain on-premise.
"""
from __future__ import annotations

from typing import Optional, Set

from .types import SandboxSpec

OFFLOAD_THRESHOLD = 0.80  # on-premise utilization trigger (paper §3.4)


class CloudOffloader:
    """Classifies tasks and splits placements between on-prem and cloud."""

    def __init__(self, shared_image_set: Optional[Set[str]] = None,
                 threshold: float = OFFLOAD_THRESHOLD):
        self.shared_image_set = shared_image_set or set()
        self.threshold = threshold
        self.offloaded = 0
        self.on_premise = 0

    def image_dependencies(self, spec: SandboxSpec) -> Set[str]:
        deps = {spec.image}
        if spec.workspace is not None:
            deps.add("%s:%s" % (spec.workspace.name, spec.workspace.version))
        for toolkit in spec.toolkits:
            deps.add("%s:%s" % (toolkit.name, toolkit.version))
        return deps

    def is_cloud_eligible(self, spec: SandboxSpec) -> bool:
        """Eligible when all image deps are inside the synchronized shared set."""
        return self.image_dependencies(spec) <= self.shared_image_set

    def should_offload(self, onprem_utilization: float) -> bool:
        return onprem_utilization > self.threshold

    def route(self, spec: SandboxSpec, onprem_utilization: float,
              eligible_fraction: float = 1.0) -> str:
        """Route one creation request: 'onprem' or 'cloud'."""
        if self.should_offload(onprem_utilization) and self.is_cloud_eligible(spec):
            self.offloaded += 1
            return "cloud"
        self.on_premise += 1
        return "onprem"

    def offload_fraction(self) -> float:
        total = self.offloaded + self.on_premise
        return self.offloaded / total if total else 0.0
