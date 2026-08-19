from agents.base import BaseAgent, AgentResult

SYSTEM = """You are the Scope agent for AI safety review.
Define users, data, capabilities, and out of scope items from the system brief. Do not invent product facts.
"""


class ScopeAgent(BaseAgent):
    name = "scope"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        brief = self.memory.read_system(system_id)
        if not brief:
            result.ok = False
            result.output = f"System brief {system_id} not found"
            return result
        resp = self._complete(SYSTEM, f"System: {system_id}\n\n{brief}\n\nWrite scope.")
        path = self.memory.write_note(f"{system_id}_scope", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
