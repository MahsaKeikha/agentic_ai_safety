from agents.base import BaseAgent, AgentResult

SYSTEM = """You are the Eval planner agent.
Propose a minimal safety eval set and release gate metrics. Prefer fail closed language.
"""


class EvalPlannerAgent(BaseAgent):
    name = "eval_planner"

    def run(self, system_id: str, **kwargs) -> AgentResult:
        result = AgentResult(ok=True, output="")
        user = (
            f"System: {system_id}\n\n## Hazards\n{self.memory.read_note(f'{system_id}_hazards')}\n\n"
            f"## Policy map\n{self.memory.read_note(f'{system_id}_policy_map')}\n\nEval plan."
        )
        resp = self._complete(SYSTEM, user)
        path = self.memory.write_note(f"{system_id}_eval_plan", resp.text)
        result.output = resp.text
        result.artifacts["path"] = str(path)
        return result
