"""Tests for the EROFS on-demand loading model (paper §5.3)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.layers.erofs import ErofsImage
from dsec.storage.store import ChunkCache, RemoteStore


class TestErofs(unittest.TestCase):
    def setUp(self):
        self.store = RemoteStore()
        self.cache = ChunkCache(capacity_bytes=16 * 1024 * 1024)
        self.files = {
            # Two distinct 256 KiB chunks so dedup cannot merge them.
            "a.bin": bytes(range(256)) * 1024 + os.urandom(256 * 1024),
            "b.bin": os.urandom(300 * 1024),  # 300 KiB -> 2 chunks
            "c.txt": b"hello",
        }
        self.image = ErofsImage.build("img", self.files, self.store, self.cache)

    def test_metadata_local_data_remote(self):
        # Metadata (pathname lookup) never triggers remote I/O (§5.3).
        self.assertIn("a.bin", self.image.file_paths())
        self.assertEqual(self.image.stat("c.txt").size, 5)
        self.assertEqual(self.store.total_bytes_fetched, 0)

    def test_lazy_fetch_only_covered_chunk(self):
        # Reading 10 bytes must fetch one 256 KiB chunk, not the whole image
        # (readahead disabled here; it has its own test).
        self.assertEqual(self.image.read_file("a.bin", 0, 10, readahead=False),
                         self.files["a.bin"][:10])
        fetched = self.store.total_bytes_fetched
        self.assertLess(fetched, self.image.CHUNK_SIZE * 1.5)
        total = self.image.data_bytes
        self.assertLess(fetched, total / 4)  # far below the full image

    def test_readahead_fetches_next_chunk(self):
        # Kernel readahead coalesces the following chunk into the fetch (§5.3):
        # a 1-byte read must pull two chunks (the covered one + the next).
        self.image.read_file("a.bin", 0, 1)
        chunks = self.image.files["a.bin"].chunks
        fetched = self.store.total_bytes_fetched
        self.assertGreaterEqual(fetched, chunks[0].csize + chunks[1].csize)
        self.assertEqual(len(chunks), 2)

    def test_second_level_cache_serves_evictions(self):
        # Once a chunk has been fetched, later reads are served by the local
        # 256 KiB chunk cache — no further 3FS fetches (paper §5.3).
        self.image.read_file("b.bin", 0, 10)
        first_fetched = self.store.total_bytes_fetched
        self.image.read_file("b.bin", 0, 10)
        self.image.read_file("b.bin", 10, 10)
        self.assertEqual(self.store.total_bytes_fetched, first_fetched)

    def test_materialize_subset(self):
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            written = self.image.materialize_subset(tmp, {"c.txt"})
            self.assertEqual(written, ["c.txt"])
            self.assertEqual((Path(tmp) / "c.txt").read_bytes(), b"hello")
            self.assertFalse((Path(tmp) / "a.bin").exists())

    def test_compression_round_trip(self):
        import zlib

        blob = self.store.get_object(
            self.image._chunk_key("img", self.image.files["c.txt"].chunks[0].digest))
        self.assertEqual(zlib.decompress(blob), b"hello")


if __name__ == "__main__":
    unittest.main()
