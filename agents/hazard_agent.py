from agents.base import BaseAgent, AgentResult

SYSTEM = """You are the Hazard agent.
List plausible harm classes and misuse paths for this system. Stay at category level. No actionable attack recipes.
"""


class HazardAgent(BaseAgent):
    name = "hazard"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"System: {system_id}\n\n## Scope\n{self.memory.read_note(f'{system_id}_scope')}\n\n"
            f"## Brief\n{self.memory.read_system(system_id)}\n\nHazard map."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{system_id}_hazards", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
