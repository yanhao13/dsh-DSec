"""Memory efficiency under high-density overcommit (paper §5.2, §8.4).

MicroVMs waste memory in two ways. First, image data read through a virtual
block device is cached once by the host and again by each guest, duplicating
the same data across the guest-host boundary. Second, free pages inside a guest
are not returned to the host without explicit reporting, and guests experience
little internal pressure to reclaim inactive pages.

DSec combines three kernel mechanisms:

- **virtio-pmem with DAX** maps file accesses directly to host-backed pages,
  so co-located microVMs share one host page-cache copy (paper §8.4: 40.2%
  peak reduction);
- **DAMON** samples access bits and evicts cold file pages through the kernel
  reclaim path;
- **virtio-balloon free-page reporting** scans the buddy allocator and reports
  free pages (order-9 = 2 MiB regions by default) so the host releases them
  via madvise(MADV_DONTNEED) (paper §8.4: 21.2% time-integrated reduction).

This module provides a deterministic per-guest accounting model of those
mechanisms plus the Linux madvise hook used for real host release.
"""
from __future__ import annotations

import ctypes
import ctypes.util
import platform
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

IS_LINUX = platform.system() == "Linux"

# virtio-pmem struct-page metadata: 4 KiB pages, 64-byte struct page ->
# guest RAM equal to 1/64 of the pmem device capacity (paper §5.2).
PMEM_STRUCT_PAGE_OVERHEAD = 1.0 / 64.0

# virtio-balloon free-page reporting order-9: 2 MiB regions (paper §5.2).
FPR_ORDER_BYTES_MB = 2


@dataclass
class GuestMemory:
    """Per-guest memory state (one Firecracker microVM or container)."""

    sandbox_id: str
    ram_limit_mb: float  # requested capacity
    pmem_dax: bool = False
    fpr_enabled: bool = False
    resident_mb: float = 0.0  # pages currently host-backed
    anon_mb: float = 0.0  # anonymous pages in use
    file_cache: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # key -> (mb, last_access)
    pmem_meta_mb: float = 0.0

    def __post_init__(self) -> None:
        self.resident_mb = self.ram_limit_mb

    def demand_mb(self) -> float:
        return self.anon_mb + self.cache_mb()

    def cache_mb(self) -> float:
        return sum(mb for mb, _ in self.file_cache.values())

    def free_mb(self) -> float:
        """Pages in the buddy allocator (reportable by the balloon)."""
        return max(self.resident_mb - self.demand_mb(), 0.0)


class MemoryManager:
    """Node-level memory accounting plus the three reclamation mechanisms."""

    def __init__(self, host_memory_mb: float = 16384.0, os_enforce: bool = True):
        self.host_memory_mb = host_memory_mb
        self.os_enforce = os_enforce and IS_LINUX
        self.guests: Dict[str, GuestMemory] = {}
        self.shared_cache: Dict[str, float] = {}  # host page cache: one copy per chunk
        self._samples: List[Tuple[float, float]] = []
        self.peak_mb = 0.0

    # -- lifecycle -------------------------------------------------------------
    def register(self, sandbox_id: str, ram_mb: float, *, pmem_dax: bool, fpr_enabled: bool,
                 pmem_capacity_mb: float = 0.0) -> GuestMemory:
        guest = GuestMemory(sandbox_id=sandbox_id, ram_limit_mb=ram_mb,
                            pmem_dax=pmem_dax, fpr_enabled=fpr_enabled)
        if pmem_dax:
            guest.pmem_meta_mb = pmem_capacity_mb * PMEM_STRUCT_PAGE_OVERHEAD
        self.guests[sandbox_id] = guest
        return guest

    def release(self, sandbox_id: str) -> None:
        self.guests.pop(sandbox_id, None)

    # -- events -------------------------------------------------------------------
    def touch_file(self, sandbox_id: str, chunk_key: str, size_mb: float, t: float) -> None:
        """A guest reads image data (via virtio-blk or virtio-pmem)."""
        guest = self.guests[sandbox_id]
        # The host page cache keeps exactly one copy, shared by co-located guests.
        self.shared_cache[chunk_key] = max(self.shared_cache.get(chunk_key, 0.0), size_mb)
        if not guest.pmem_dax:
            # virtio-blk: each guest caches its own copy in guest RAM.
            guest.file_cache[chunk_key] = (size_mb, t)
            self._inflate(guest)

    def set_anon(self, sandbox_id: str, mb: float) -> None:
        guest = self.guests[sandbox_id]
        guest.anon_mb = mb
        self._inflate(guest)

    def _inflate(self, guest: GuestMemory) -> None:
        """Balloon inflation on allocation: grow residency up to the limit."""
        if guest.demand_mb() > guest.resident_mb:
            guest.resident_mb = min(guest.ram_limit_mb, guest.demand_mb())

    def damon_reclaim(self, t: float, cold_age_s: float) -> float:
        """DAMON: evict file pages untouched beyond the cold-age threshold."""
        freed = 0.0
        for guest in self.guests.values():
            stale = [k for k, (mb, last) in guest.file_cache.items() if t - last >= cold_age_s]
            for key in stale:
                mb, _ = guest.file_cache.pop(key)
                freed += mb
        return freed

    def free_page_reporting(self) -> float:
        """virtio-balloon: report free pages in 2 MiB units; the host releases
        them via madvise(MADV_DONTNEED), modeled as a residency shrink."""
        released = 0.0
        for guest in self.guests.values():
            if not guest.fpr_enabled:
                continue
            reportable = int(guest.free_mb() // FPR_ORDER_BYTES_MB) * FPR_ORDER_BYTES_MB
            if reportable > 0:
                guest.resident_mb -= reportable
                released += reportable
        return released

    # -- measurement ------------------------------------------------------------------
    def host_usage_mb(self) -> float:
        """Host memory held for sandboxes: residency + shared page cache +
        per-guest cache copies (only for guests without virtio-pmem DAX)."""
        total = sum(self.shared_cache.values())
        for guest in self.guests.values():
            total += guest.resident_mb + guest.pmem_meta_mb
            if not guest.pmem_dax:
                total += guest.cache_mb()
        return total

    def sample(self, t: float) -> float:
        usage = self.host_usage_mb()
        self._samples.append((t, usage))
        self.peak_mb = max(self.peak_mb, usage)
        return usage

    def time_integral_mb_s(self) -> float:
        pts = self._samples
        if len(pts) < 2:
            return 0.0
        total = 0.0
        for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
            total += 0.5 * (v0 + v1) * (t1 - t0)
        return total

    # -- real host hook ----------------------------------------------------------------
    def madvise_dontneed(self, address: int, size: int) -> None:
        """Release host memory for a reported range (Linux; MADV_DONTNEED)."""
        if not self.os_enforce:
            return
        libc = ctypes.CDLL(ctypes.util.find_library("c") or "libc.so.6", use_errno=True)
        try:
            libc.madvise(ctypes.c_void_p(address), ctypes.c_size_t(size), 4)  # MADV_DONTNEED
        except Exception:
            pass


@dataclass
class ConfigResult:
    peak_mb: float
    integral_mb_s: float
    series: List[Tuple[float, float]] = field(default_factory=list)


def firecracker_workload(
    n_guests: int = 20,
    ram_mb: float = 512.0,
    anon_mb: float = 200.0,
    image_mb: float = 300.0,
    read_at: float = 60.0,
    cold_age_s: float = 400.0,
    report_period: float = 30.0,
    duration: float = 600.0,
) -> Dict[str, ConfigResult]:
    """Replay the paper's Fig. 12 workload under four Firecracker configs.

    All guests boot, allocate anonymous memory, read the shared base image
    during setup, then sit mostly idle while DAMON/balloon reclamation runs.
    Returns measured peak and time-integrated host usage per configuration.
    """
    configs = {
        "baseline": {"pmem": False, "fpr": False, "damon": False},
        "pmem": {"pmem": True, "fpr": False, "damon": False},
        "fpr": {"pmem": False, "fpr": True, "damon": True},
        "pmem+fpr": {"pmem": True, "fpr": True, "damon": True},
    }
    results: Dict[str, ConfigResult] = {}
    for name, cfg in configs.items():
        mgr = MemoryManager(host_memory_mb=1 << 40)
        for i in range(n_guests):
            guest = mgr.register(
                "vm-%d" % i, ram_mb,
                pmem_dax=cfg["pmem"], fpr_enabled=cfg["fpr"],
                pmem_capacity_mb=image_mb if cfg["pmem"] else 0.0,
            )
            guest.anon_mb = anon_mb
        read_done = False
        t = 0.0
        while t <= duration:
            if not read_done and t >= read_at:
                for i in range(n_guests):
                    mgr.touch_file("vm-%d" % i, "base-image", image_mb, t)
                read_done = True
            if cfg["damon"]:
                mgr.damon_reclaim(t, cold_age_s)
            if cfg["fpr"]:
                mgr.free_page_reporting()
            mgr.sample(t)
            t += report_period
        results[name] = ConfigResult(
            peak_mb=mgr.peak_mb, integral_mb_s=mgr.time_integral_mb_s(), series=list(mgr._samples)
        )
    return results


def reductions(results: Dict[str, ConfigResult]) -> Dict[str, float]:
    """Peak and time-integrated reductions vs. baseline (paper §8.4 anchors)."""
    base = results["baseline"]
    return {
        "pmem_peak_pct": 100.0 * (1 - results["pmem"].peak_mb / base.peak_mb),
        "fpr_integral_pct": 100.0 * (1 - results["fpr"].integral_mb_s / base.integral_mb_s),
        "combined_integral_pct": 100.0 * (1 - results["pmem+fpr"].integral_mb_s / base.integral_mb_s),
    }
