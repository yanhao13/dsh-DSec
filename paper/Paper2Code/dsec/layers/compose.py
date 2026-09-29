"""Environment composition and layer-maintenance cost model (paper §5.1).

Fusing base images, workspaces, and toolkits into monolithic OCI images creates
a combinatorial maintenance burden: upgrading m base images costs O(m·N) and
upgrading k toolkits costs O(k·N) when they are combined with N workspaces.
Versioning the three components independently reduces both to O(m) and O(k):
only the changed layers are rebuilt and recombined with existing ones.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .layer import KIND_BASE, KIND_TOOLKIT, KIND_WORKSPACE, Layer
from .overlay import OverlayFS
from .registry import LayerRegistry

COLLAPSE_THRESHOLD_BYTES = 3 * 1024 * 1024 * 1024  # paper §5.3: 3 GB


@dataclass
class ComposedEnvironment:
    """The runtime overlay stack for one sandbox: base + workspace + toolkits."""

    base: Layer
    workspace: Optional[Layer] = None
    toolkits: List[Layer] = field(default_factory=list)
    collapsed: bool = False

    def stack(self) -> List[Layer]:
        layers = [self.base]
        if self.workspace is not None:
            layers.append(self.workspace)
        layers.extend(self.toolkits)
        return layers  # priority: toolkits > workspace > base

    def overlay(self) -> OverlayFS:
        return OverlayFS(self.stack())

    def merged_files(self) -> Dict[str, bytes]:
        return self.overlay().merged_files()

    @property
    def total_size_bytes(self) -> int:
        return sum(l.size_bytes for l in self.stack())

    def describe(self) -> str:
        parts = ["%s:%s" % (self.base.name, self.base.version)]
        if self.workspace is not None:
            parts.append("%s:%s" % (self.workspace.name, self.workspace.version))
        for t in self.toolkits:
            parts.append("%s:%s" % (t.name, t.version))
        return "[" + " + ".join(parts) + "]"


class EnvironmentComposer:
    """Composes sandbox environments from independently versioned layers."""

    def __init__(self, registry: LayerRegistry):
        self.registry = registry

    def compose(self, base_ref, workspace_ref=None, toolkit_refs=None) -> ComposedEnvironment:
        """Resolve layer refs into a stack (base at the bottom, toolkits on top)."""
        base = self.registry.get_layer(*base_ref)
        workspace = self.registry.get_layer(*workspace_ref) if workspace_ref else None
        toolkits = [self.registry.get_layer(*r) for r in (toolkit_refs or [])]
        return ComposedEnvironment(base=base, workspace=workspace, toolkits=toolkits)

    def collapse_layers(self, env: ComposedEnvironment) -> ComposedEnvironment:
        """Collapse consecutive layers within the size threshold (paper §5.3).

        Consecutive layers whose combined size stays under 3 GB merge into one
        layer, preserving whiteout/priority semantics via the overlay merge.
        """
        stack = env.stack()
        merged: List[Layer] = []
        i = 0
        while i < len(stack):
            j = i + 1
            total = stack[i].size_bytes
            while j < len(stack) and total + stack[j].size_bytes <= COLLAPSE_THRESHOLD_BYTES:
                total += stack[j].size_bytes
                j += 1
            if j > i + 1:
                group = stack[i:j]
                name = "+".join(l.name for l in group)
                version = "+".join(l.version for l in group)
                files = OverlayFS(group).merged_files()
                merged.append(Layer(name=name, version=version, kind=KIND_BASE, files=files))
            else:
                merged.append(stack[i])
            i = j
        collapsed = ComposedEnvironment(
            base=merged[0],
            workspace=merged[1] if len(merged) > 1 and merged[1].kind == KIND_WORKSPACE else None,
            toolkits=[m for m in merged[1:] if m.kind == KIND_TOOLKIT],
            collapsed=True,
        )
        return collapsed


def monolithic_rebuild_cost(n_bases: int, n_workspaces: int, n_toolkits: int,
                            m_bases: int, k_toolkits: int) -> int:
    """Image rebuilds required when base/toolkit layers are fused into images.

    Upgrading m base images forces rebuilding their workspace combinations
    (O(m·N)); upgrading k toolkits costs O(k·N). (Paper §5.1.)
    """
    return m_bases * n_workspaces + k_toolkits * n_workspaces


def layered_rebuild_cost(m_bases: int, k_toolkits: int) -> int:
    """Image rebuilds under independent versioning: O(m) + O(k) (paper §5.1)."""
    return m_bases + k_toolkits
