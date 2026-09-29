"""Independently versioned environment layers (paper §5.1).

A sandbox's content decomposes into a base image, a workspace, and toolkits —
logically independent layers with their own lifecycles. Published layers are
immutable, so upgrading a toolkit never rebuilds workspaces (O(k) instead of
O(k·N) maintenance cost).
"""
from .layer import Layer
from .overlay import OverlayFS, UpperDir
from .erofs import ErofsImage
from .registry import LayerRegistry
from .compose import EnvironmentComposer, ComposedEnvironment

__all__ = [
    "Layer",
    "OverlayFS",
    "UpperDir",
    "ErofsImage",
    "LayerRegistry",
    "EnvironmentComposer",
    "ComposedEnvironment",
]
