from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional

from agents.eval_agent import EvalPlannerAgent
from agents.gatekeeper_agent import GatekeeperAgent
from agents.hazard_agent import HazardAgent
from agents.incident_agent import IncidentAgent
from agents.policy_agent import PolicyAgent
from agents.redteam_agent import RedTeamAgent
from agents.residual_agent import ResidualRiskAgent
from agents.scope_agent import ScopeAgent
from audit import AuditTrail
from config import AgentConfig
from llm_client import LLMClient
from memory import SafetyMemory
from security.permissions import BoundSafetyMemory, PermissionPolicy


@dataclass
class ReviewRunReport:
    system_id: str
    steps: List[str] = field(default_factory=list)
    ok: bool = True
    audit_path: str = ""
    audit_valid: bool = False

    def log(self, msg: str) -> None:
        self.steps.append(msg)
        print(f"[ai-safety] {msg}")


class SafetyOrchestrator:
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.config.ensure_dirs()
        self.audit = AuditTrail(self.config.review_root / "audit" / "events.jsonl")
        self.permission_policy = PermissionPolicy.default()
        self.memory = SafetyMemory(self.config)
        self.llm = LLMClient(self.config)

        def bound(actor: str) -> BoundSafetyMemory:
            return BoundSafetyMemory(self.memory, actor, self.permission_policy, self.audit)

        self.scope = ScopeAgent(self.config, bound("scope"), self.llm)
        self.hazard = HazardAgent(self.config, bound("hazard"), self.llm)
        self.policy = PolicyAgent(self.config, bound("policy"), self.llm)
        self.eval_planner = EvalPlannerAgent(self.config, bound("eval_planner"), self.llm)
        self.red_team = RedTeamAgent(self.config, bound("red_team"), self.llm)
        self.residual = ResidualRiskAgent(self.config, bound("residual_risk"), self.llm)
        self.incident = IncidentAgent(self.config, bound("incident"), self.llm)
        self.gatekeeper = GatekeeperAgent(self.config, bound("gatekeeper"), self.llm)
        self.orchestrator_memory = bound("orchestrator")

    def run(self, system_id: str, *, ship: bool = False) -> ReviewRunReport:
        report = ReviewRunReport(
            system_id=system_id,
            audit_path=str(self.audit.path),
        )
        self.audit.append(
            actor="orchestrator",
            action="review_start",
            target=system_id,
            outcome="started",
            details={"ship_requested": ship},
        )
        pipeline = [
            ("scope", lambda: self.scope.run(system_id)),
            ("hazard", lambda: self.hazard.run(system_id)),
            ("policy", lambda: self.policy.run(system_id)),
            ("eval_planner", lambda: self.eval_planner.run(system_id)),
            ("red_team", lambda: self.red_team.run(system_id)),
            ("residual_risk", lambda: self.residual.run(system_id)),
            ("incident", lambda: self.incident.run(system_id)),
            ("gatekeeper", lambda: self.gatekeeper.run(system_id)),
        ]
        for name, operation in pipeline:
            self.audit.append(actor="orchestrator", action="stage_start", target=name, outcome="started")
            result = operation()
            outcome = "allowed" if result.ok else "failed"
            self.audit.append(actor="orchestrator", action="stage_result", target=name, outcome=outcome)
            report.log(f"{name}: {'ok' if result.ok else 'FAIL'}")
            if not result.ok:
                report.ok = False
                self.audit.append(
                    actor="orchestrator",
                    action="review_stop",
                    target=system_id,
                    outcome="failed_closed",
                    details={"failed_stage": name},
                )
                report.audit_valid = self.audit.verify()["valid"]
                return report
        if ship:
            self.orchestrator_memory.write_export(
                f"{system_id}_APPROVED.txt",
                f"Human approved safety pack for {system_id}. Not a legal certification.\n",
            )
            self.audit.append(
                actor="orchestrator",
                action="human_release_gate",
                target=system_id,
                outcome="approved",
            )
            report.log("APPROVED flag written. Still not a formal certification.")
        else:
            self.audit.append(
                actor="orchestrator",
                action="human_release_gate",
                target=system_id,
                outcome="awaiting_human",
            )
            report.log("HUMAN GATE: review safety_pack.md then re-run with --ship if approving")
        report.audit_valid = self.audit.verify()["valid"]
        return report
