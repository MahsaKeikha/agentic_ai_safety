from agents.base import BaseAgent, AgentResult

SYSTEM = """You are the Red team agent (defensive).
Propose test categories and expected safe behaviors. Do not provide step by step instructions for causing harm.
"""


class RedTeamAgent(BaseAgent):
    name = "red_team"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"System: {system_id}\n\n## Eval plan\n{self.memory.read_note(f'{system_id}_eval_plan')}\n\n"
            f"## Hazards\n{self.memory.read_note(f'{system_id}_hazards')}\n\nDefensive red team notes."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{system_id}_red_team", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
