from agents.base import BaseAgent, AgentResult

SYSTEM = """You are the Policy agent.
Map the system to acceptable use rules. Note gaps and required controls. Do not invent legal advice.
"""


class PolicyAgent(BaseAgent):
    name = "policy"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"System: {system_id}\n\n## Policy\n{self.memory.read_policy()}\n\n"
            f"## Hazards\n{self.memory.read_note(f'{system_id}_hazards')}\n\nPolicy map."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{system_id}_policy_map", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
