"""pack_diff: checkpoint a sandbox into a reusable environment (paper §6.1).

Manually constructing the large number of environments required by agentic RL
is impractical; instead, agents build environments interactively on the same
infrastructure used for training and evaluation. At any point, an agent can
checkpoint a sandbox by taking an incremental disk snapshot (pack_diff), which
can later be restored as a new sandbox. This turns an interactive session
directly into a reusable environment.

Two production rules are modeled here: builder and runtime agents use separate
accounts (enforced through IAM principals), and build-time residual data is
removed from the writable layer before packing so reference answers are not
carried into the resulting image.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from ..layers.layer import KIND_WORKSPACE, Layer
from ..layers.overlay import OverlayFS
from ..layers.registry import LayerRegistry
from ..types import LayerRef, SandboxSpec

# Residual files removed before packing (paper §6.1: reference answers).
RESIDUAL_GLOBS = ("answer", "solution", ".reference", "REFERENCE", "*.gold")


def _is_residual(path: str) -> bool:
    name = path.split("/")[-1].lower()
    return any(g.lower().lstrip("*.") in name for g in RESIDUAL_GLOBS)


async def _current_upper(sandbox) -> Dict[str, bytes]:
    """Snapshot the sandbox's writable layer via the platform file API."""
    edge = sandbox.client.server.resolve_edge(sandbox.sandbox_id)
    ctx = edge.sandboxes[sandbox.sandbox_id]
    backend = edge.backends[ctx.spec.backend]
    snap = await backend.snapshot(ctx)
    return snap.get("upper", {})


async def pack_diff(sandbox, name: str, version: str, *, clean: bool = True,
                    registry: Optional[LayerRegistry] = None) -> LayerRef:
    """Incremental snapshot of the sandbox's writable layer -> layer publish.

    Returns a LayerRef that can be restored by :func:`restore_from_pack`.
    """
    from ..errors import PermissionDenied

    server = sandbox.client.server
    edge = server.resolve_edge(sandbox.sandbox_id)
    # Builder/runtime account separation is an IAM property; packing requires
    # the pack permission, which is granted to builder principals only (§6.1).
    entry = server._registry.get(sandbox.sandbox_id)
    if entry is None:
        raise PermissionDenied("sandbox not registered")
    project_path = entry[1]
    try:
        server.iam.authorize(sandbox.client.principal, "pack.diff", project_path)
    except PermissionDenied:
        raise PermissionDenied(
            "pack_diff requires the pack.diff grant (builder principal, §6.1)")

    ctx = edge.sandboxes[sandbox.sandbox_id]
    layers: List[Layer] = ctx.metadata.get("layer_stack", [])
    if not layers:
        raise ValueError("sandbox has no layer stack to diff against")
    lower = OverlayFS(layers).merged_files()
    upper = await _current_upper(sandbox)
    if clean:
        upper = {p: d for p, d in upper.items() if not _is_residual(p)}
    # Whiteouts: paths present in the lowers but absent from the upper become
    # per-directory whiteout markers (overlayfs semantics, §5.1).
    files: Dict[str, bytes] = {}
    for path in sorted(lower):
        if path not in upper:
            parent, _, basename = path.rpartition("/")
            files[(parent + "/" if parent else "") + ".wh." + basename] = b""
        elif upper[path] != lower[path]:
            files[path] = upper[path]
    for path, data in upper.items():
        if path not in lower and path not in files:
            files[path] = data

    reg = registry
    if reg is None:
        # Resolve the edge's registry (the platform-level layer store).
        reg = edge.registry
    layer = Layer(name=name, version=version, kind=KIND_WORKSPACE, files=files)
    reg.publish(layer)
    if edge.metrics is not None:
        edge.metrics.inc("pack_diffs")
        edge.metrics.inc("pack_diff_files", len(files))
    return LayerRef(name=name, version=version, kind=KIND_WORKSPACE)


async def restore_from_pack(registry: LayerRegistry, pack: LayerRef, spec: SandboxSpec):
    """Restore a packed environment as a new sandbox's workspace layer."""
    spec.workspace = pack
    return spec
