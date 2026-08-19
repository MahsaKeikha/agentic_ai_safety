from agents.base import BaseAgent, AgentResult
from tools.checklist_tools import load_checklist, checklist_report

SYSTEM = """You are the Gatekeeper agent for AI safety.
Assemble a release readiness summary. Recommend approve, conditional, or block. Humans decide.
"""


class GatekeeperAgent(BaseAgent):
    name = "gatekeeper"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"System: {system_id}\n\n"
            f"## Scope\n{self.memory.read_note(f'{system_id}_scope')}\n\n"
            f"## Hazards\n{self.memory.read_note(f'{system_id}_hazards')}\n\n"
            f"## Eval\n{self.memory.read_note(f'{system_id}_eval_plan')}\n\n"
            f"## Residual\n{self.memory.read_note(f'{system_id}_residual_risk')}\n\nGate summary."
        )
        resp = self._complete(SYSTEM, user)
        items = load_checklist("release_gate.md")
        text = resp.text + ("\n\n" + checklist_report(items) if items else "")
        path = self.memory.write_export(f"{system_id}_safety_pack.md", text)
        result.output = text
        result.artifacts["path"] = str(path)
        result.add("pack ready. human ship gate required")
        return result
