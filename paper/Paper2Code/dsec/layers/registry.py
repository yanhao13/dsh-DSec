"""Versioned, immutable layer registry (paper §5.1, §2.4).

Published layers are immutable and stored as EROFS images: metadata local on
the node, data in the remote store. During one production week the paper's
container backend served 11,266 base images, 102,171 workspaces and 103
toolkits — the registry models exactly that catalog structure.
"""
from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

from ..errors import AlreadyExists, NotFound
from ..storage.store import ChunkCache, RemoteStore
from .erofs import ErofsImage
from .layer import Layer


class LayerRegistry:
    """Catalog of (name, version) -> EROFS image + local metadata mirror."""

    def __init__(self, store: RemoteStore, cache: Optional[ChunkCache] = None, local_dir: Optional[str] = None):
        self.store = store
        self.cache = cache or ChunkCache()
        self.local_dir = local_dir
        self._images: Dict[Tuple[str, str], ErofsImage] = {}
        self._kinds: Dict[Tuple[str, str], str] = {}
        self._rebuild_log: List[str] = []
        if local_dir:
            os.makedirs(local_dir, exist_ok=True)

    # -- publish -----------------------------------------------------------------
    def publish(self, layer: Layer) -> ErofsImage:
        """Publish an immutable layer; a version may be published only once."""
        key = layer.ref
        if key in self._images:
            raise AlreadyExists("%s:%s already published" % key)
        image = ErofsImage.build(
            name="%s:%s" % key, files=layer.files, store=self.store, cache=self.cache
        )
        self._images[key] = image
        self._kinds[key] = layer.kind
        if self.local_dir:
            image.write_metadata(self._metadata_path(layer.name, layer.version))
        self._rebuild_log.append("publish %s:%s (%d files, %.1f MiB data)" % (
            layer.name, layer.version, len(layer.files), image.data_bytes / 1e6))
        return image

    def republish(self, layer: Layer) -> ErofsImage:
        """Replace an existing version (used only by tests and offline rebuilds)."""
        self._images.pop(layer.ref, None)
        return self.publish(layer)

    def _metadata_path(self, name: str, version: str) -> str:
        safe = "%s__%s.json" % (name.replace("/", "_"), version.replace("/", "_"))
        return os.path.join(self.local_dir or ".", safe)

    # -- lookup --------------------------------------------------------------------
    def get_image(self, name: str, version: str) -> ErofsImage:
        image = self._images.get((name, version))
        if image is None:
            raise NotFound("layer %s:%s" % (name, version))
        return image

    def get_layer(self, name: str, version: str) -> Layer:
        """Materialize the layer tree (reads all chunks — the eager path)."""
        image = self.get_image(name, version)
        files = {p: image.read_all(p) for p in image.file_paths()}
        kind = self._kinds.get((name, version), self._kind_of(name))
        return Layer(name=name, version=version, kind=kind, files=files)

    def get_layer_paths(self, name: str, version: str) -> Layer:
        """Path-only layer: full tree shape, no data fetched (on-demand path).

        Pathname lookup and layer stacking use only the metadata, which is
        local; file data is fetched later, on access (paper §5.3).
        """
        image = self.get_image(name, version)
        kind = self._kinds.get((name, version), self._kind_of(name))
        return Layer(name=name, version=version, kind=kind,
                     files={p: b"" for p in image.file_paths()})

    _KIND_HINTS = {"toolkit": "toolkit", "workspace": "workspace"}

    def _kind_of(self, name: str) -> str:
        for hint, kind in self._KIND_HINTS.items():
            if hint in name:
                return kind
        return "base"

    def versions(self, name: str) -> List[str]:
        return sorted(v for (n, v) in self._images if n == name)

    def names(self) -> List[str]:
        return sorted({n for (n, _) in self._images})

    def catalog_size(self) -> int:
        """Aggregate size of all published layer data (paper Tab. 2)."""
        return sum(img.data_bytes for img in self._images.values())

    @property
    def rebuild_log(self) -> List[str]:
        return list(self._rebuild_log)

    def count_by_kind(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for (name, _) in self._images:
            kind = self._kind_of(name)
            out[kind] = out.get(kind, 0) + 1
        return out
