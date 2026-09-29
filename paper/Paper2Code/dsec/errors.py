"""Error hierarchy for DSec (paper §3.2, §3.3: IAM rejections, edge admission)."""
from __future__ import annotations


class DSecError(Exception):
    """Base class for all DSec errors."""


class InvalidRequest(DSecError):
    """Malformed or semantically invalid request."""


class AuthError(DSecError):
    """Authentication failed (unknown principal, bad token)."""


class PermissionDenied(DSecError):
    """Authorization failed: principal lacks the policy grant (paper §3.2 IAM)."""


class QuotaExceeded(DSecError):
    """Project resource quota exhausted (paper §3.2 IAM quotas)."""


class NotFound(DSecError):
    """Referenced object does not exist (sandbox, layer, project)."""


class AlreadyExists(DSecError):
    """Referenced object already exists (e.g. layer version re-published)."""


class AdmissionError(DSecError):
    """Edge-local admission rejected the creation request (paper §3.3, §7)."""


class SandboxError(DSecError):
    """Sandbox-level runtime failure (crashed, channel closed, backend error)."""


class SandboxTimeout(SandboxError):
    """Sandbox operation exceeded its time budget."""


class BackendUnavailable(DSecError):
    """Requested backend cannot run on this node (missing runtime/hardware)."""


class AccessDenied(DSecError):
    """Agent tried to access a platform-protected path or channel (paper §6.5)."""


class NetworkPolicyViolation(DSecError):
    """Requested network target is outside the sandbox allowlist (paper §6.5)."""


class OutputLimitExceeded(SandboxError):
    """Command output exceeded the capture budget and was cut (paper §6.4 `yes`)."""


class PreconditionError(DSecError):
    """Operation invalid in the sandbox's current lifecycle state."""
