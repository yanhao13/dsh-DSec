"""Identity and Access Management with nested projects (paper §3.2).

IAM authenticates callers and authorizes all management requests. Projects
define scopes for resource management and access control; access policies say
which principals may perform which operations, and resource quotas bound
consumption. DSec supports multi-level project nesting: authorized principals
(including agents and harnesses) can create subprojects, delegate part of the
parent quota, and grant management permissions within them. Delegation is
bounded by the parent — a principal cannot grant permissions it does not hold,
and subproject policies and quotas cannot exceed the parent's limits.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from .errors import AuthError, PermissionDenied, QuotaExceeded

# Management operations.
OP_CREATE = "sandbox.create"
OP_STOP = "sandbox.stop"
OP_OPS = "sandbox.ops"
OP_LIST = "sandbox.list"
OP_MANAGE = "project.manage"
OP_PACK = "pack.diff"
OPS = (OP_CREATE, OP_STOP, OP_OPS, OP_LIST, OP_MANAGE, OP_PACK)


@dataclass
class Quota:
    cpu: float = 0.0
    memory_mb: int = 0
    max_sandboxes: int = 0

    def remaining_after(self, used: "Quota") -> "Quota":
        return Quota(
            cpu=max(self.cpu - used.cpu, 0.0),
            memory_mb=max(self.memory_mb - used.memory_mb, 0),
            max_sandboxes=max(self.max_sandboxes - used.max_sandboxes, 0),
        )

    def fits(self, need: "Quota") -> bool:
        return (
            self.cpu >= need.cpu
            and self.memory_mb >= need.memory_mb
            and self.max_sandboxes >= need.max_sandboxes
        )

    def add(self, other: "Quota") -> "Quota":
        return Quota(self.cpu + other.cpu, self.memory_mb + other.memory_mb,
                     self.max_sandboxes + other.max_sandboxes)


@dataclass
class Project:
    name: str
    parent: Optional["Project"] = None
    quota: Quota = field(default_factory=Quota)
    used: Quota = field(default_factory=Quota)
    grants: Dict[str, Set[str]] = field(default_factory=dict)  # principal -> ops

    def path(self) -> str:
        chain = []
        node: Optional[Project] = self
        while node is not None:
            chain.append(node.name)
            node = node.parent
        return "/".join(reversed(chain))

    def remaining(self) -> Quota:
        return self.quota.remaining_after(self.used)

    def check_policy(self, principal: str, op: str) -> bool:
        """Most specific grant wins; walking up, any grant along the path
        authorizes (subprojects only restrict quotas, never expand policies
        beyond what a grantor holds)."""
        node: Optional[Project] = self
        while node is not None:
            if op in node.grants.get(principal, ()):
                return True
            node = node.parent
        return False

    def grant(self, principal: str, ops: Set[str], actor: str) -> None:
        """Grant ops; the actor must hold OP_MANAGE and every op itself."""
        if not self.check_policy(actor, OP_MANAGE):
            raise PermissionDenied("%s lacks %s on %s" % (actor, OP_MANAGE, self.path()))
        for op in ops:
            if op != OP_MANAGE and not self.check_policy(actor, op):
                raise PermissionDenied(
                    "%s cannot grant %s it does not hold on %s" % (actor, op, self.path()))
        self.grants.setdefault(principal, set()).update(ops)

    def revoke(self, principal: str, ops: Set[str], actor: str) -> None:
        if not self.check_policy(actor, OP_MANAGE):
            raise PermissionDenied("only managers may revoke on %s" % self.path())
        self.grants.get(principal, set()).difference_update(ops)


class IAM:
    """The IAM service: principal registry + project tree."""

    def __init__(self):
        self._principals: Set[str] = set()
        root = Project(name="root", quota=Quota(cpu=1 << 20, memory_mb=1 << 30, max_sandboxes=1 << 30))
        self.projects: Dict[str, Project] = {root.path(): root}

    def add_principal(self, name: str) -> None:
        self._principals.add(name)

    def authenticate(self, principal: str) -> None:
        if principal not in self._principals:
            raise AuthError("unknown principal %r" % principal)

    def create_project(self, parent_path: str, name: str, quota: Quota, creator: str) -> Project:
        """Create a nested project; quota is bounded by the parent's remaining."""
        parent = self._project(parent_path)
        if not parent.check_policy(creator, OP_MANAGE):
            raise PermissionDenied("%s cannot manage %s" % (creator, parent_path))
        remaining = parent.remaining()
        if not remaining.fits(quota):
            raise QuotaExceeded(
                "quota %s exceeds parent remaining %s" % (quota, remaining))
        project = Project(name=name, parent=parent, quota=quota)
        path = project.path()
        if path in self.projects:
            raise QuotaExceeded("project %s exists" % path)
        self.projects[path] = project
        return project

    def authorize(self, principal: str, op: str, project_path: str) -> Project:
        """Authenticate + authorize an operation; returns the project."""
        self.authenticate(principal)
        project = self._project(project_path)
        if not project.check_policy(principal, op):
            raise PermissionDenied("%s denied %s on %s" % (principal, op, project_path))
        return project

    def consume(self, project: Project, need: Quota) -> None:
        """Reserve quota for a creation; walks up, bounded by parent quotas."""
        chain = self._chain(project)
        for node in chain:
            if not node.remaining().fits(need):
                raise QuotaExceeded("quota exhausted at %s" % node.path())
        for node in chain:
            node.used = node.used.add(need)

    def release(self, project: Project, held: Quota) -> None:
        for node in self._chain(project):
            node.used = Quota(
                cpu=max(node.used.cpu - held.cpu, 0.0),
                memory_mb=max(node.used.memory_mb - held.memory_mb, 0),
                max_sandboxes=max(node.used.max_sandboxes - held.max_sandboxes, 0),
            )

    def _project(self, path: str) -> Project:
        project = self.projects.get(path)
        if project is None:
            raise PermissionDenied("no such project %r" % path)
        return project

    @staticmethod
    def _chain(project: Project) -> List[Project]:
        chain = []
        node: Optional[Project] = project
        while node is not None:
            chain.append(node)
            node = node.parent
        return chain
