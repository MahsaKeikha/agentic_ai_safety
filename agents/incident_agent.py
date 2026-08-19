from agents.base import BaseAgent, AgentResult

SYSTEM = """You are the Incident agent.
Outline detect, contain, notify, learn for AI safety incidents related to this system.
"""


class IncidentAgent(BaseAgent):
    name = "incident"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"System: {system_id}\n\n## Residual risk\n{self.memory.read_note(f'{system_id}_residual_risk')}\n\n"
            f"Incident response outline."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_incident_template(f"{system_id}_incident_plan", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
