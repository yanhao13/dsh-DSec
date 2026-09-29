"""Tests for overlayfs stacking semantics (paper §5.1)."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsec.layers.layer import Layer
from dsec.layers.overlay import OverlayFS


def layer(files, name="l", kind="base"):
    return Layer(name, "1", kind, files)


class TestOverlayPriority(unittest.TestCase):
    """Priority: toolkits > workspace > base; runtime writes go to the upper."""

    def test_top_layer_wins(self):
        ov = OverlayFS([
            layer({"a.txt": b"base", "b.txt": b"base-b"}),
            layer({"a.txt": b"workspace"}),
            layer({"a.txt": b"toolkit", "c.txt": b"toolkit-c"}),
        ])
        self.assertEqual(ov.read("a.txt"), b"toolkit")
        self.assertEqual(ov.read("b.txt"), b"base-b")
        self.assertEqual(ov.read("c.txt"), b"toolkit-c")

    def test_append_semantics_not_replace(self):
        # A workspace layer must merge into the base tree without hiding the
        # contents below (the bind-mount problem described in paper §4.2).
        ov = OverlayFS([
            layer({"usr/bin/x": b"x", "usr/lib/y": b"y"}),
            layer({"workspace/repo.py": b"print(1)"}),
        ])
        self.assertTrue(ov.is_file("usr/bin/x"))
        self.assertTrue(ov.is_file("usr/lib/y"))
        self.assertTrue(ov.is_file("workspace/repo.py"))
        self.assertIn("usr", ov.listdir(""))

    def test_write_copies_up_and_leaves_layers_untouched(self):
        lower = layer({"a.txt": b"base"})
        ov = OverlayFS([lower])
        ov.write("a.txt", b"modified")
        ov.write("new.txt", b"new")
        self.assertEqual(ov.read("a.txt"), b"modified")
        self.assertEqual(ov.read("new.txt"), b"new")
        self.assertEqual(lower.files["a.txt"], b"base")  # lower immutable
        self.assertEqual(ov.diff_from_lowers(), {"a.txt": b"modified", "new.txt": b"new"})


class TestWhiteouts(unittest.TestCase):
    def test_remove_hides_lower_file(self):
        ov = OverlayFS([layer({"a.txt": b"base"})])
        self.assertTrue(ov.is_file("a.txt"))
        ov.remove("a.txt")
        self.assertFalse(ov.exists("a.txt"))
        self.assertEqual(ov.deletions(), ["a.txt"])

    def test_whiteout_in_lower_layer(self):
        # A layer may ship whiteouts to hide files below it (collapsing §5.3).
        ov = OverlayFS([
            layer({"a.txt": b"base", "b.txt": b"keep"}),
            layer({".wh.a.txt": b""}),
        ])
        self.assertFalse(ov.exists("a.txt"))
        self.assertTrue(ov.is_file("b.txt"))

    def test_dir_removal_hides_subtree(self):
        ov = OverlayFS([layer({"d/f1": b"1", "d/sub/f2": b"2", "other": b"3"})])
        ov.remove("d", recursive=True)
        self.assertFalse(ov.exists("d"))
        self.assertFalse(ov.exists("d/sub"))
        self.assertTrue(ov.is_file("other"))

    def test_write_over_whiteout_revives_path(self):
        ov = OverlayFS([layer({"a.txt": b"base"})])
        ov.remove("a.txt")
        ov.write("a.txt", b"revived")
        self.assertEqual(ov.read("a.txt"), b"revived")

    def test_opaque_dir_hides_lower_entries(self):
        ov = OverlayFS([layer({"d/old.txt": b"old"})])
        ov.mkdir("d")
        ov.write("d/new.txt", b"new")
        # opaque marker set by remove() should hide lower 'd/old.txt'
        ov.remove("d/old.txt", recursive=True)
        self.assertFalse(ov.exists("d/old.txt"))
        self.assertTrue(ov.is_file("d/new.txt"))


class TestMaterializeAndDiff(unittest.TestCase):
    def test_materialize_writes_merged_view(self):
        ov = OverlayFS([layer({"a/b.txt": b"b", "a/c.txt": b"c"})])
        with tempfile.TemporaryDirectory() as tmp:
            ov.materialize(tmp)
            import pathlib

            self.assertEqual((pathlib.Path(tmp) / "a" / "b.txt").read_bytes(), b"b")

    def test_diff_reports_modify_add_delete(self):
        ov = OverlayFS([layer({"mod.txt": b"old", "del.txt": b"x", "keep.txt": b"k"})])
        ov.write("mod.txt", b"new")
        ov.write("add.txt", b"added")
        ov.remove("del.txt")
        diff = ov.diff_from_lowers()
        self.assertEqual(diff["mod.txt"], b"new")
        self.assertEqual(diff["add.txt"], b"added")
        self.assertEqual(ov.deletions(), ["del.txt"])


if __name__ == "__main__":
    unittest.main()
