from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from config import AgentConfig
from memory import SafetyMemory
from llm_client import LLMClient
from agents.scope_agent import ScopeAgent
from agents.hazard_agent import HazardAgent
from agents.policy_agent import PolicyAgent
from agents.eval_agent import EvalPlannerAgent
from agents.redteam_agent import RedTeamAgent
from agents.residual_agent import ResidualRiskAgent
from agents.incident_agent import IncidentAgent
from agents.gatekeeper_agent import GatekeeperAgent


@dataclass
class ReviewRunReport:
    system_id: str
    steps: List[str] = field(default_factory=list)
    ok: bool = True

    def log(self, msg: str) -> None:
        self.steps.append(msg)
        print(f"[ai-safety] {msg}")


class SafetyOrchestrator:
    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig()
        self.config.ensure_dirs()
        self.memory = SafetyMemory(self.config)
        self.llm = LLMClient(self.config)
        self.scope = ScopeAgent(self.config, self.memory, self.llm)
        self.hazard = HazardAgent(self.config, self.memory, self.llm)
        self.policy = PolicyAgent(self.config, self.memory, self.llm)
        self.eval_planner = EvalPlannerAgent(self.config, self.memory, self.llm)
        self.red_team = RedTeamAgent(self.config, self.memory, self.llm)
        self.residual = ResidualRiskAgent(self.config, self.memory, self.llm)
        self.incident = IncidentAgent(self.config, self.memory, self.llm)
        self.gatekeeper = GatekeeperAgent(self.config, self.memory, self.llm)

    def run(self, system_id: str, *, ship: bool = False) -> ReviewRunReport:
        report = ReviewRunReport(system_id=system_id)
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
        for name, fn in pipeline:
            r = fn()
            report.log(f"{name}: {'ok' if r.ok else 'FAIL'}")
            if not r.ok:
                report.ok = False
                return report
        if ship:
            self.memory.write_export(
                f"{system_id}_APPROVED.txt",
                f"Human approved safety pack for {system_id}. Not a legal certification.\n",
            )
            report.log("APPROVED flag written. Still not a formal certification.")
        else:
            report.log("HUMAN GATE: review safety_pack.md then re-run with --ship if approving")
        return report
