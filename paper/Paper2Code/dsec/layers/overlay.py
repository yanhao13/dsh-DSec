"""Overlayfs-compatible stacking semantics in pure Python (paper §5.1).

The paper uses overlayfs because bind mounts *replace* the target path while
environment layers need *append* semantics: files must merge into the existing
directory tree without hiding the contents below, and runtime writes must land
in a writable upper layer. This module implements exactly those semantics:

- lower layers stack with priority ``top-most wins`` (toolkits override
  workspaces override base images);
- whiteout files (``.wh.<name>``) represent deletions of lower entries;
- opaque directory markers (``.wh..wh..opq``) hide a whole lower subtree, used
  for directory removal and layer collapsing (paper §5.3);
- every runtime write copies up into the writable upper layer, leaving the
  read-only layers untouched.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .layer import Layer

WHITEOUT_PREFIX = ".wh."
OPAQUE_MARKER = ".wh..wh..opq"


def _norm(path: str) -> str:
    path = path.replace("\\", "/").strip("/")
    parts = [p for p in path.split("/") if p not in ("", ".")]
    out: List[str] = []
    for p in parts:
        if p == "..":
            if out:
                out.pop()
        else:
            out.append(p)
    return "/".join(out)


def _split(path: str) -> Tuple[str, str]:
    parent, _, name = path.rpartition("/")
    return parent, name


def _is_whiteout(path: str) -> bool:
    return _split(path)[1].startswith(WHITEOUT_PREFIX)


def _dirs_of(paths) -> set:
    dirs = set()
    for path in paths:
        parts = path.split("/")
        for i in range(1, len(parts)):
            dirs.add("/".join(parts[:i]))
    return dirs


class OverlayFS:
    """Read-only lower layers plus a writable in-memory upper layer.

    ``lowers[0]`` is the bottom layer (base image); ``lowers[-1]`` has highest
    priority. The merged view is computed eagerly on every mutation, which keeps
    lookup semantics obviously correct for a reference implementation.
    """

    def __init__(self, lowers: Iterable[Layer], upper: Optional[Dict[str, bytes]] = None):
        self.lowers: List[Dict[str, bytes]] = [dict(layer.files) for layer in lowers]
        self.upper: Dict[str, bytes] = dict(upper) if upper is not None else {}

    # -- merged view ------------------------------------------------------------
    def merged_files(self) -> Dict[str, bytes]:
        """Bottom-up merge applying whiteouts and opaque markers at each level."""
        out: Dict[str, bytes] = {}
        for level in self.lowers + [self.upper]:
            hidden: List[str] = []  # lower paths hidden by this level
            for path, data in level.items():
                if data is None:
                    continue
                name = _split(path)[1]
                if name == OPAQUE_MARKER:
                    dirpath = _split(path)[0]
                    hidden.append(dirpath)
                    continue
                if name.startswith(WHITEOUT_PREFIX):
                    parent = _split(path)[0]
                    target = name[len(WHITEOUT_PREFIX):]
                    hidden.append((parent + "/" + target).lstrip("/"))
                    continue
                out[path] = data
            for h in hidden:
                if h == "":
                    out.clear()
                    continue
                for p in list(out):
                    if p == h or p.startswith(h + "/"):
                        del out[p]
        return out

    def _lower_only(self) -> Dict[str, bytes]:
        """Merged view of the lowers alone (their own whiteouts applied)."""
        out: Dict[str, bytes] = {}
        for level in self.lowers:
            hidden: List[str] = []
            for path, data in level.items():
                if data is None:
                    continue
                name = _split(path)[1]
                if name == OPAQUE_MARKER:
                    hidden.append(_split(path)[0])
                    continue
                if name.startswith(WHITEOUT_PREFIX):
                    parent = _split(path)[0]
                    target = name[len(WHITEOUT_PREFIX):]
                    hidden.append((parent + "/" + target).lstrip("/"))
                    continue
                out[path] = data
            for h in hidden:
                if h == "":
                    out.clear()
                    continue
                for p in list(out):
                    if p == h or p.startswith(h + "/"):
                        del out[p]
        return out

    def diff_from_lowers(self) -> Dict[str, bytes]:
        """Added/modified paths: merged state differing from the lower stack."""
        merged = self.merged_files()
        lower = self._lower_only()
        return {p: d for p, d in merged.items() if lower.get(p) != d}

    def deletions(self) -> List[str]:
        """Lower paths hidden by the upper layer (whiteouts / opaque markers)."""
        merged = self.merged_files()
        lower = self._lower_only()
        return sorted(p for p in lower if p not in merged)

    # -- queries ----------------------------------------------------------------
    def _view(self) -> Dict[str, bytes]:
        return self.merged_files()

    def exists(self, path: str) -> bool:
        path = _norm(path)
        view = self._view()
        return path in view or path in _dirs_of(view)

    def is_file(self, path: str) -> bool:
        return _norm(path) in self._view()

    def is_dir(self, path: str) -> bool:
        path = _norm(path)
        if path == "":
            return True
        if path in self._view():
            return False
        return path in _dirs_of(self._view())

    def read(self, path: str) -> bytes:
        path = _norm(path)
        view = self._view()
        if path not in view:
            raise FileNotFoundError(path)
        return view[path]

    def listdir(self, path: str = "") -> List[str]:
        path = _norm(path)
        view = self._view()
        if path and path not in view and path not in _dirs_of(view):
            raise NotADirectoryError(path)
        prefix = path + "/" if path else ""
        names = set()
        for p in list(view) + sorted(_dirs_of(view)):
            if not p.startswith(prefix):
                continue
            rest = p[len(prefix):]
            if rest and "/" not in rest:
                names.add(rest)
        return sorted(names)

    # -- writes (copy-up into the upper layer) ------------------------------------
    def write(self, path: str, data: bytes) -> None:
        path = _norm(path)
        if self.is_dir(path):
            raise IsADirectoryError(path)
        parent, name = _split(path)
        if parent:
            self.mkdir(parent)
        self.upper[path] = bytes(data)
        if name:
            self.upper.pop(parent + "/" + WHITEOUT_PREFIX + name, None)

    def mkdir(self, path: str) -> None:
        path = _norm(path)
        if path == "":
            return
        if self.is_file(path):
            raise NotADirectoryError(path)
        if self.is_dir(path):
            return
        parent, name = _split(path)
        if parent:
            self.mkdir(parent)
            # creating a dir re-exposes a whiteouted name
            self.upper.pop(parent + "/" + WHITEOUT_PREFIX + name, None)
            # drop the parent's opaque marker so the new dir is visible
            self.upper.pop(parent + "/" + OPAQUE_MARKER, None)
        self.upper.setdefault(path, None)  # existence marker; None never materializes

    def remove(self, path: str, recursive: bool = False) -> None:
        """Delete a file or directory (whiteout / opaque markers)."""
        path = _norm(path)
        if self.is_dir(path):
            if not recursive and self.listdir(path):
                raise OSError("directory not empty: %r" % path)
            for p in list(self.upper):
                if p == path or p.startswith(path + "/"):
                    del self.upper[p]
            self.upper[path + "/" + OPAQUE_MARKER] = b""  # hide lower subtree
            parent, name = _split(path)
            if name:
                self.upper[parent + "/" + WHITEOUT_PREFIX + name] = b""
            return
        if self.is_file(path):
            self.upper.pop(path, None)
            parent, name = _split(path)
            if name:
                self.upper[parent + "/" + WHITEOUT_PREFIX + name] = b""
            return
        raise FileNotFoundError(path)

    def materialize(self, target_dir: str) -> None:
        """Write the merged view to a real directory (the sandbox rootfs)."""
        root = Path(target_dir)
        root.mkdir(parents=True, exist_ok=True)
        for path, data in self.merged_files().items():
            dest = root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)


class UpperDir:
    """Writable upper layer backed by a real directory (the running sandbox).

    The materialized rootfs directory *is* the upper layer: writes go straight
    to local disk (paper §5.3: "writes stay local"), and a snapshot is just the
    directory's contents.
    """

    def __init__(self, rootfs_dir: str):
        self.root = Path(rootfs_dir)

    def read(self, relpath: str) -> bytes:
        p = self.root / _norm(relpath)
        if not p.is_file():
            raise FileNotFoundError(relpath)
        return p.read_bytes()

    def write(self, relpath: str, data: bytes) -> None:
        p = self.root / _norm(relpath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)

    def exists(self, relpath: str) -> bool:
        return (self.root / _norm(relpath)).exists()

    def listdir(self, relpath: str = "") -> List[str]:
        p = self.root / _norm(relpath)
        if not p.is_dir():
            raise NotADirectoryError(relpath)
        return sorted(e.name for e in p.iterdir())

    def snapshot_files(self) -> Dict[str, bytes]:
        out: Dict[str, bytes] = {}
        for path in self.root.rglob("*"):
            if path.is_file():
                out[path.relative_to(self.root).as_posix()] = path.read_bytes()
        return out

    def clear(self) -> None:
        import shutil

        if self.root.exists():
            shutil.rmtree(self.root)
