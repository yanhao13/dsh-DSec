"""Immutable, content-addressed layer model (paper §5.1, §2.2)."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

KIND_BASE = "base"
KIND_WORKSPACE = "workspace"
KIND_TOOLKIT = "toolkit"
KINDS = (KIND_BASE, KIND_WORKSPACE, KIND_TOOLKIT)


@dataclass
class Layer:
    """One immutable environment layer: a mapping of relative paths to bytes.

    Layers of different kinds share one representation; the compositor stacks
    them with priority ``toolkit > workspace > base`` (paper Fig. 4b).
    """

    name: str
    version: str
    kind: str
    files: Dict[str, bytes] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.kind not in KINDS:
            raise ValueError("unknown layer kind %r" % self.kind)
        for path, data in self.files.items():
            if not isinstance(data, bytes):
                self.files[path] = bytes(data)

    @property
    def ref(self) -> Tuple[str, str]:
        return (self.name, self.version)

    @property
    def size_bytes(self) -> int:
        return sum(len(d) for d in self.files.values())

    def digest(self) -> str:
        """Content digest over name/kind and every file, in sorted path order."""
        h = hashlib.sha256()
        h.update(self.name.encode())
        h.update(b"\0")
        h.update(self.kind.encode())
        for path in sorted(self.files):
            h.update(path.encode())
            h.update(b"\0")
            h.update(hashlib.sha256(self.files[path]).digest())
        return h.hexdigest()

    def iter_paths(self) -> List[str]:
        """All regular-file paths plus implicit parent directories."""
        paths = set()
        for path in self.files:
            parts = path.split("/")
            for i in range(1, len(parts)):
                paths.add("/".join(parts[:i]))
            paths.add(path)
        return sorted(paths)

    @classmethod
    def build_from_dir(cls, name: str, version: str, kind: str, dirpath: str, ignore=None) -> "Layer":
        """Build a layer from a directory tree (e.g. an agent-built workspace)."""
        ignore = ignore or set()
        root = Path(dirpath)
        files: Dict[str, bytes] = {}
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(root).as_posix()
            if rel in ignore:
                continue
            files[rel] = path.read_bytes()
        return cls(name=name, version=version, kind=kind, files=files)

    def with_file(self, path: str, data: bytes) -> "Layer":
        out = Layer(self.name, self.version, self.kind, dict(self.files))
        out.files[path] = data
        return out
