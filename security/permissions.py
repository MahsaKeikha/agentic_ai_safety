from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, TypeVar

from audit import AuditTrail
from memory import SafetyMemory

T = TypeVar("T")


class PermissionDenied(RuntimeError):
    pass


DEFAULT_PERMISSIONS = {
    "scope": {"read_system", "write_note"},
    "hazard": {"read_system", "read_note", "write_note"},
    "policy": {"read_policy", "read_note", "write_note"},
    "eval_planner": {"read_note", "write_note"},
    "red_team": {"read_note", "write_note"},
    "residual_risk": {"read_note", "write_note"},
    "incident": {"read_note", "write_incident"},
    "gatekeeper": {"read_note", "write_export"},
    "orchestrator": {"write_export"},
}


@dataclass(frozen=True)
class PermissionPolicy:
    grants: dict[str, set[str]]

    @classmethod
    def default(cls) -> "PermissionPolicy":
        return cls(grants={actor: set(actions) for actor, actions in DEFAULT_PERMISSIONS.items()})

    def allows(self, actor: str, action: str) -> bool:
        return action in self.grants.get(actor, set())


class BoundSafetyMemory:
    def __init__(self, memory: SafetyMemory, actor: str, policy: PermissionPolicy, audit: AuditTrail):
        self._memory = memory
        self.actor = actor
        self.policy = policy
        self.audit = audit

    def _call(self, action: str, target: str, operation: Callable[[], T]) -> T:
        if not self.policy.allows(self.actor, action):
            self.audit.append(actor=self.actor, action=action, target=target, outcome="denied")
            raise PermissionDenied(f"{self.actor} is not allowed to perform {action}")
        try:
            result = operation()
        except Exception as exc:
            self.audit.append(
                actor=self.actor,
                action=action,
                target=target,
                outcome="error",
                details={"error_type": type(exc).__name__},
            )
            raise
        self.audit.append(actor=self.actor, action=action, target=target, outcome="allowed")
        return result

    def read_system(self, system_id: str) -> str:
        return self._call("read_system", f"systems/{system_id}.md", lambda: self._memory.read_system(system_id))

    def read_policy(self) -> str:
        return self._call("read_policy", "policies/acceptable_use.md", self._memory.read_policy)

    def write_note(self, name: str, content: str):
        return self._call("write_note", f"notes/{name}", lambda: self._memory.write_note(name, content))

    def read_note(self, name: str) -> str:
        return self._call("read_note", f"notes/{name}", lambda: self._memory.read_note(name))

    def write_draft(self, name: str, content: str):
        return self._call("write_draft", f"drafts/{name}", lambda: self._memory.write_draft(name, content))

    def write_export(self, name: str, content: str):
        return self._call("write_export", f"exports/{name}", lambda: self._memory.write_export(name, content))

    def write_incident_template(self, name: str, content: str):
        return self._call(
            "write_incident",
            f"incidents/{name}",
            lambda: self._memory.write_incident_template(name, content),
        )
