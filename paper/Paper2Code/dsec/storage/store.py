"""3FS-like remote image store and second-level local chunk cache (paper §5.3).

The paper's storage design follows the asymmetric I/O profile of 3FS:

1. *Writes stay local.* Sandbox writes land on the node's local disk, never in
   the remote store.
2. *Reads are on-demand and bulk.* Read-only image data is fetched only when
   accessed, in large requests that exploit 3FS's high sequential throughput.
3. *Metadata is kept local.* Small metadata reads never touch the remote store.

:class:`RemoteStore` models this profile deterministically: every range read is
classified as bulk (>= ``bulk_threshold`` bytes, throughput-costed) or small
(random I/O, latency-penalized). :class:`ChunkCache` is the second-level local
cache used by the OverlayBD/ublk path (256 KiB chunks) that survives page-cache
eviction (paper §5.3).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


class RemoteStore:
    """Content-addressed blob store with the 3FS asymmetric I/O model.

    Objects are immutable byte blobs. The store records the simulated cost of
    every access so experiments can compare eager vs. on-demand distribution
    (§8.2: on-demand loading cuts cumulative disk writes by ~57%).
    """

    def __init__(
        self,
        bulk_threshold: int = 64 * 1024,
        bulk_bandwidth_mbps: float = 4000.0,
        small_io_penalty_s: float = 0.0005,
        random_read_penalty_s: float = 0.0002,
    ):
        self.bulk_threshold = bulk_threshold
        self.bulk_bandwidth_mbps = bulk_bandwidth_mbps
        self.small_io_penalty_s = small_io_penalty_s
        self.random_read_penalty_s = random_read_penalty_s
        self._objects: Dict[str, bytes] = {}
        self.total_bytes_fetched = 0
        self.bulk_ios = 0
        self.small_ios = 0
        self.simulated_seconds = 0.0

    # -- write path: bulk, offline (image publication) -----------------------
    def put_object(self, key: str, data: bytes) -> None:
        """Publish an immutable blob (offline image publication path)."""
        self._objects[key] = bytes(data)

    def has_object(self, key: str) -> bool:
        return key in self._objects

    def get_object(self, key: str) -> bytes:
        """Fetch a whole blob (used by the *eager* distribution baseline)."""
        data = self._objects.get(key)
        if data is None:
            raise KeyError(key)
        self._charge(len(data), bulk=True)
        return data

    def read_range(self, key: str, offset: int, size: int) -> bytes:
        """Fetch ``[offset, offset+size)`` of a blob — the on-demand path."""
        data = self._objects.get(key)
        if data is None:
            raise KeyError(key)
        end = min(offset + size, len(data))
        if offset >= len(data):
            return b""
        chunk = bytes(data[offset:end])
        self._charge(len(chunk), bulk=len(chunk) >= self.bulk_threshold)
        return chunk

    def stats(self) -> Dict[str, float]:
        return {
            "total_bytes_fetched": self.total_bytes_fetched,
            "bulk_ios": self.bulk_ios,
            "small_ios": self.small_ios,
            "simulated_seconds": self.simulated_seconds,
        }

    def _charge(self, nbytes: int, bulk: bool) -> None:
        self.total_bytes_fetched += nbytes
        if bulk:
            self.bulk_ios += 1
            self.simulated_seconds += nbytes / (self.bulk_bandwidth_mbps * 1e6 / 8)
        else:
            self.small_ios += 1
            self.simulated_seconds += self.small_io_penalty_s + nbytes * self.random_read_penalty_s


@dataclass
class _Entry:
    key: str
    data: bytes


class ChunkCache:
    """Second-level local filesystem cache in 256 KiB chunks (paper §5.3).

    Even after a chunk is evicted from the page cache, it remains available
    here, so it never needs to be fetched from 3FS again.
    """

    CHUNK_SIZE = 256 * 1024

    def __init__(self, capacity_bytes: int = 8 * 1024 * 1024 * 1024):
        self.capacity = capacity_bytes
        self._entries: Dict[str, _Entry] = {}
        self._size = 0
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Optional[bytes]:
        entry = self._entries.get(key)
        if entry is None:
            self.misses += 1
            return None
        self.hits += 1
        # LRU refresh
        del self._entries[key]
        self._entries[key] = entry
        return entry.data

    def put(self, key: str, data: bytes) -> None:
        if len(data) > self.capacity:
            return
        existing = self._entries.pop(key, None)
        if existing is not None:
            self._size -= len(existing.data)
        self._entries[key] = _Entry(key, bytes(data))
        self._size += len(data)
        while self._size > self.capacity and len(self._entries) > 1:
            oldest_key = next(iter(self._entries))
            victim = self._entries.pop(oldest_key)
            self._size -= len(victim.data)

    def clear(self) -> None:
        self._entries.clear()
        self._size = 0

    @property
    def size_bytes(self) -> int:
        return self._size
