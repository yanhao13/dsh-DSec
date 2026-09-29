"""Tests for the §5.2 memory model against the paper's §8.4 anchors."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.resources.memory import firecracker_workload, reductions


class TestMemoryWorkload(unittest.TestCase):
    """Fig. 12 replay: pmem+DAX cuts peak ~40.2%; DAMON+balloon FPR cuts the
    time-integrated usage ~21.2% (tolerance bands: the paper's numbers are
    workload-mix dependent)."""

    def setUp(self):
        self.results = firecracker_workload()
        self.red = reductions(self.results)

    def test_pmem_reduces_peak_usage(self):
        self.assertGreater(self.red["pmem_peak_pct"], 30.0)
        self.assertLess(self.red["pmem_peak_pct"], 50.0)

    def test_fpr_reduces_time_integral(self):
        self.assertGreater(self.red["fpr_integral_pct"], 15.0)
        self.assertLess(self.red["fpr_integral_pct"], 27.0)

    def test_combined_is_lowest(self):
        # "Combining both mechanisms produces the lowest overall consumption."
        combined = self.results["pmem+fpr"]
        self.assertLess(combined.integral_mb_s, self.results["fpr"].integral_mb_s)
        self.assertLess(combined.peak_mb, self.results["baseline"].peak_mb)

    def test_fpr_leaves_peak_largely_unchanged(self):
        # FPR alone leaves peak usage largely unchanged (paper §8.4).
        ratio = self.results["fpr"].peak_mb / self.results["baseline"].peak_mb
        self.assertGreater(ratio, 0.95)

    def test_pmem_struct_page_metadata_cost(self):
        # struct-page metadata: 1/64 of the pmem capacity (paper §5.2).
        from dsec.resources.memory import GuestMemory

        guest = GuestMemory("g", ram_limit_mb=512, pmem_dax=True)
        guest.pmem_meta_mb = 300.0 / 64.0
        self.assertAlmostEqual(guest.pmem_meta_mb, 4.6875, places=4)


if __name__ == "__main__":
    unittest.main()
