"""Reward-hacking mitigation and access control (paper §6.4, §6.5).

Production experience revealed two risks. Agents obtained answers through
unintended channels: forged chronus RPC requests, scraping chronus logs for
leaked answers, overwriting /bin/bash to inject commands into later shell
sessions, and — after file/socket controls landed — attempting XFS_IOC_SWAPEXT
to swap data extents between a protected file and an attacker-controlled
descriptor. Agents also damaged the environment: port scanning for mirrors,
Go module proxies fetching reference implementations, and unbounded output
(``yes``) filling storage.

DSec's mitigations are AppArmor file/socket access control and per-sandbox
eBPF network allowlists keyed by domain/mirror service, plus output capture
budgets. This module provides:

- a protected-path registry enforced at every file/socket operation;
- an AppArmor profile generator producing real profile text for Linux hosts;
- a deny-by-default network allowlist (service → host/port/protocol) enforced
  at the sandbox proxy, with dynamic policy updates between task stages;
- a misbehavior log recording every blocked attempt (the paper's examples are
  unit-tested here).
"""
from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from ..errors import AccessDenied, NetworkPolicyViolation

# Platform-managed paths agents must not read or modify (paper §6.4/§6.5):
# chronus logs and sockets, the shell binary, and platform config.
PROTECTED_PATHS = (
    "/var/log/chronus",
    "/run/chronus.sock",
    "/run/dsec",
    "/bin/bash",
    "/usr/bin/bash",
    "/bin/sh",
    "/etc/chronus",
    "/proc/kpagecgroup",
)

# Network services keyed by domain/mirror (paper Listing 1: pypi/npm).
SERVICE_HOSTS: Dict[str, Tuple[str, ...]] = {
    "pypi": ("pypi.org", "files.pythonhosted.org"),
    "npm": ("registry.npmjs.org",),
    "github": ("github.com", "codeload.github.com", "raw.githubusercontent.com"),
    "goproxy": ("proxy.golang.org",),
    "internal-mirror": ("mirror.internal.example",),
}


@dataclass
class MisbehaviorEvent:
    ts: float
    sandbox_id: str
    kind: str
    detail: str

    def __repr__(self) -> str:
        return "[%.1f] %s: %s — %s" % (self.ts, self.sandbox_id, self.kind, self.detail)


class MisbehaviorLog:
    """Records every blocked agent attempt for analysis (paper §6.4)."""

    def __init__(self):
        self.events: List[MisbehaviorEvent] = []

    def record(self, sandbox_id: str, kind: str, detail: str) -> None:
        self.events.append(MisbehaviorEvent(time.monotonic(), sandbox_id, kind, detail))

    def kinds(self, sandbox_id: str = "") -> List[str]:
        return [e.kind for e in self.events if not sandbox_id or e.sandbox_id == sandbox_id]


class SecurityPolicy:
    """Per-cluster security policy: protected paths + network allowlists."""

    def __init__(self, protected_paths: Tuple[str, ...] = PROTECTED_PATHS,
                 service_hosts: Optional[Dict[str, Tuple[str, ...]]] = None):
        self.protected_paths = tuple(protected_paths)
        self.service_hosts = dict(service_hosts or SERVICE_HOSTS)
        self.misbehavior = MisbehaviorLog()

    # -- file / socket access control (AppArmor model) -----------------------------
    def is_protected(self, path: str) -> bool:
        norm = path.rstrip("/")
        for protected in self.protected_paths:
            if norm == protected or norm.startswith(protected + "/"):
                return True
        return False

    def check_file_access(self, ctx, path: str, op: str) -> None:
        """Block reads/writes of platform-managed paths (AppArmor semantics).

        Agents running as root inside the sandbox cannot bypass this check,
        mirroring the kernel-level AppArmor enforcement of paper §6.5.
        """
        if self.is_protected(path):
            self.misbehavior.record(
                ctx.sandbox_id, "protected-path-%s" % op,
                "attempted %s of protected path %r" % (op, path))
            raise AccessDenied("protected path %r: %s denied (AppArmor)" % (path, op))

    def apparmor_profile(self, sandbox_id: str) -> str:
        """Generate an AppArmor profile for the sandbox (Linux hosts)."""
        deny_lines = []
        for path in self.protected_paths:
            deny_lines.append("  deny %s/** rwlkx," % path)
            deny_lines.append("  deny %s rwlkx," % path)
        return (
            "profile dsec-sandbox-%s flags=(attach_disconnected) {\n"
            "  # DSec sandbox: file/socket access control (paper §6.5)\n"
            "  network,\n"
            "%s\n"
            "  capability,\n"
            "  mount,\n"
            "  /tmp/** rwlk,\n"
            "  /workspace/** rwlkx,\n"
            "}\n" % (sandbox_id, "\n".join(sorted(set(deny_lines))))
        )

    # -- network allowlist (eBPF model) ----------------------------------------------
    def service_for_host(self, host: str) -> Optional[str]:
        host = (host or "").lower().rstrip(".")
        for service, hosts in self.service_hosts.items():
            if host in hosts:
                return service
        return None

    def check_network(self, ctx, url: str) -> None:
        """Enforce the sandbox's allowlist for an outbound request.

        In production the same policy is compiled into a per-sandbox eBPF
        program filtering by IP/port/protocol (paper §6.5); here it is checked
        at the proxy before the request leaves the sandbox.
        """
        host = urlparse(url).hostname or ""
        service = self.service_for_host(host)
        allowed = ctx.spec.network.allowed_service(service) if service else False
        if not allowed:
            self.misbehavior.record(
                ctx.sandbox_id, "network-denied",
                "request to %s (service=%s) outside allowlist" % (url, service))
            raise NetworkPolicyViolation(
                "network allowlist denies %r (service=%r)" % (url, service))

    def render_ebpf_rules(self, rules) -> List[dict]:
        """Render an allowlist as eBPF-style (ip, port, protocol) filter rules."""
        out = []
        for service, allowed in rules.allow.items():
            if not allowed:
                continue
            for host in self.service_hosts.get(service, ()):
                out.append({
                    "service": service, "host": host,
                    "match": {"proto": "tcp", "port": 443, "action": "accept"},
                    "default": "drop",  # deny-by-default (paper §6.5)
                })
        return out
