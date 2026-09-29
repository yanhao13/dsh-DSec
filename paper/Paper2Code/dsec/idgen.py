"""Sandbox identifiers that encode the owning edge (paper §3.2).

The apiserver keeps no per-sandbox state; every sandbox id embeds the id of the
edge that owns it, so any apiserver instance can resolve and forward a request
directly to the target edge. This is what lets the ingress tier scale
horizontally.
"""
from __future__ import annotations

import secrets
from typing import NamedTuple

_PREFIX = "dsec"


class ParsedId(NamedTuple):
    edge_id: str
    seq: int
    rand: int


def new_sandbox_id(edge_id: str, seq: int) -> str:
    """Encode an edge-owned sandbox id.

    Format: ``dsec-<edge hex>-<seq hex 8>-<rand hex 4>``.
    """
    edge_part = _encode(edge_id)
    rand = secrets.randbits(16)
    return "%s-%s-%08x-%04x" % (_PREFIX, edge_part, seq & 0xFFFFFFFF, rand)


def parse_sandbox_id(sandbox_id: str) -> ParsedId:
    """Decode the owning edge id and sequence number from a sandbox id."""
    parts = sandbox_id.split("-")
    if len(parts) != 4 or parts[0] != _PREFIX:
        raise ValueError("malformed sandbox id: %r" % sandbox_id)
    return ParsedId(edge_id=_decode(parts[1]), seq=int(parts[2], 16), rand=int(parts[3], 16))


def owning_edge(sandbox_id: str) -> str:
    """The edge id that owns the sandbox — routing key for the apiserver."""
    return parse_sandbox_id(sandbox_id).edge_id


def _encode(edge_id: str) -> str:
    return edge_id.encode("utf-8").hex()


def _decode(hex_text: str) -> str:
    return bytes.fromhex(hex_text).decode("utf-8")
