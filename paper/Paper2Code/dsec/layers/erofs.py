"""EROFS-style read-only image format with on-demand loading (paper §5.3).

EROFS separates filesystem metadata from file data. DSec downloads the metadata
to the worker's local disk while leaving file data on 3FS, so metadata traversal
and pathname lookup never incur remote I/O. File content is served through
buffered on-demand reads: only the compressed 256 KiB chunks covering the
requested range are fetched, and kernel-style readahead coalesces adjacent
blocks into larger requests. A second-level local chunk cache keeps evicted
chunks available without another 3FS fetch.

This reference format mirrors those properties:

- *metadata* (per-file chunk maps, sizes, digests) lives in local memory and is
  serializable to a local JSON manifest;
- *data* lives in the :class:`~dsec.storage.store.RemoteStore` as immutable
  per-chunk blobs;
- reads fetch only the chunks they touch (plus one readahead chunk), in bulk.
"""
from __future__ import annotations

import hashlib
import json
import zlib
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Set

from ..storage.store import ChunkCache, RemoteStore


@dataclass
class _ChunkRef:
    digest: str
    usize: int
    csize: int


@dataclass
class _FileMeta:
    size: int
    mode: int
    chunks: List[_ChunkRef] = field(default_factory=list)


class ErofsImage:
    """A compressed, read-only, randomly-accessible image backed by the store."""

    CHUNK_SIZE = 256 * 1024  # OverlayBD/ublk chunk granularity (paper §5.3)

    def __init__(
        self,
        name: str,
        store: RemoteStore,
        cache: ChunkCache,
        files: Dict[str, _FileMeta],
        compress: bool = True,
    ):
        self.name = name
        self.store = store
        self.cache = cache
        self.files = files
        self.compress = compress
        self.bytes_read_total = 0
        self.bytes_read_remote = 0

    # -- build (offline image publication) -------------------------------------
    @classmethod
    def build(
        cls,
        name: str,
        files: Dict[str, bytes],
        store: RemoteStore,
        cache: Optional[ChunkCache] = None,
        compress: bool = True,
    ) -> "ErofsImage":
        cache = cache or ChunkCache()
        metas: Dict[str, _FileMeta] = {}
        for path in sorted(files):
            data = bytes(files[path])
            chunks: List[_ChunkRef] = []
            for start in range(0, max(len(data), 1), cls.CHUNK_SIZE):
                piece = data[start:start + cls.CHUNK_SIZE]
                digest = hashlib.sha256(piece).hexdigest()
                blob = zlib.compress(piece, 6) if compress else piece
                key = cls._chunk_key(name, digest)
                if not store.has_object(key):
                    store.put_object(key, blob)
                chunks.append(_ChunkRef(digest=digest, usize=len(piece), csize=len(blob)))
            metas[path] = _FileMeta(size=len(data), mode=0o644, chunks=chunks)
        return cls(name=name, store=store, cache=cache, files=metas, compress=compress)

    @staticmethod
    def _chunk_key(image: str, digest: str) -> str:
        return "erofs/%s/%s" % (image, digest)

    # -- metadata (local) --------------------------------------------------------
    @property
    def metadata_bytes(self) -> int:
        return len(json.dumps(self.metadata_dict()).encode("utf-8"))

    def metadata_dict(self) -> Dict[str, dict]:
        return {
            "name": self.name,
            "files": {p: asdict(m) for p, m in self.files.items()},
            "compress": self.compress,
        }

    def write_metadata(self, local_path: str) -> None:
        """Persist metadata locally (paper §5.3: metadata stays on the node)."""
        with open(local_path, "w") as fh:
            json.dump(self.metadata_dict(), fh)

    @classmethod
    def load_metadata(cls, local_path: str, store: RemoteStore, cache: ChunkCache) -> "ErofsImage":
        with open(local_path) as fh:
            meta = json.load(fh)
        files = {
            p: _FileMeta(size=m["size"], mode=m["mode"], chunks=[_ChunkRef(**c) for c in m["chunks"]])
            for p, m in meta["files"].items()
        }
        return cls(meta["name"], store, cache, files, compress=meta.get("compress", True))

    @property
    def data_bytes(self) -> int:
        return sum(c.csize for m in self.files.values() for c in m.chunks)

    def file_paths(self) -> Set[str]:
        return set(self.files)

    def stat(self, path: str) -> _FileMeta:
        meta = self.files.get(path)
        if meta is None:
            raise FileNotFoundError(path)
        return meta

    def has_file(self, path: str) -> bool:
        return path in self.files

    # -- on-demand reads ----------------------------------------------------------
    def read_file(self, path: str, offset: int = 0, size: int = -1, readahead: bool = True) -> bytes:
        """Read a file range, fetching only the chunks it covers (plus readahead)."""
        meta = self.stat(path)
        if offset < 0 or offset > meta.size:
            raise ValueError("bad offset")
        if size < 0:
            size = meta.size - offset
        size = min(size, meta.size - offset)
        start_chunk = offset // self.CHUNK_SIZE
        end_byte = offset + size
        end_chunk = (end_byte + self.CHUNK_SIZE - 1) // self.CHUNK_SIZE
        if readahead and end_chunk < len(meta.chunks):
            end_chunk += 1  # kernel readahead: coalesce the next chunk (§5.3)
        parts: List[bytes] = []
        for idx in range(start_chunk, min(end_chunk, len(meta.chunks))):
            ref = meta.chunks[idx]
            parts.append(self._fetch_chunk(ref))
        data = b"".join(parts)
        chunk_offset = offset - start_chunk * self.CHUNK_SIZE
        return data[chunk_offset:chunk_offset + size]

    def read_all(self, path: str) -> bytes:
        return self.read_file(path, 0, -1)

    def _fetch_chunk(self, ref: _ChunkRef) -> bytes:
        self.bytes_read_total += ref.usize
        cached = self.cache.get(ref.digest)
        if cached is not None:
            return cached
        blob = self.store.read_range(self._chunk_key(self.name, ref.digest), 0, ref.csize)
        data = zlib.decompress(blob) if self.compress else blob
        self.bytes_read_remote += ref.csize
        self.cache.put(ref.digest, data)
        return data

    def materialize_subset(self, target_dir: str, paths: Optional[Set[str]] = None) -> List[str]:
        """Materialize a subset (or all) files to disk — the eager path."""
        import os
        from pathlib import Path

        chosen = self.file_paths() if paths is None else set(paths) & self.file_paths()
        written = []
        for path in sorted(chosen):
            data = self.read_all(path)
            dest = Path(target_dir) / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            written.append(path)
        return written
