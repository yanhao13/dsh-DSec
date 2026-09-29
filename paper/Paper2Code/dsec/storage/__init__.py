"""Image/workspace storage backed by a 3FS-like distributed filesystem."""
from .store import ChunkCache, RemoteStore

__all__ = ["RemoteStore", "ChunkCache"]
