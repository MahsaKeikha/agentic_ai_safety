from agents.base import BaseAgent, AgentResult

SYSTEM = """You are the Residual risk agent.
Summarize what risk remains after stated mitigations. Assign owners. Be conservative.
"""


class ResidualRiskAgent(BaseAgent):
    name = "residual_risk"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"System: {system_id}\n\n## Policy map\n{self.memory.read_note(f'{system_id}_policy_map')}\n\n"
            f"## Red team\n{self.memory.read_note(f'{system_id}_red_team')}\n\nResidual risk."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{system_id}_residual_risk", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
