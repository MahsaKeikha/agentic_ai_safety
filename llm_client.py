from __future__ import annotations
import os
import re
from dataclasses import dataclass
from typing import Dict, Optional
from config import AgentConfig, DEFAULT_MODEL, MAX_TOKENS


@dataclass
class LLMResponse:
    text: str
    model: str
    offline: bool
    usage: Dict[str, int]


class LLMClient:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.offline = config.offline or not (config.api_key or os.getenv("ANTHROPIC_API_KEY"))
        self._client = None
        if not self.offline:
            try:
                import anthropic
                self._client = anthropic.Anthropic(
                    api_key=config.api_key or os.getenv("ANTHROPIC_API_KEY")
                )
            except Exception:
                self.offline = True

    def complete(self, system: str, user: str, **kwargs) -> LLMResponse:
        if self.offline:
            return self._offline(system, user)
        model = kwargs.get("model") or self.config.model or DEFAULT_MODEL
        msg = self._client.messages.create(
            model=model,
            max_tokens=kwargs.get("max_tokens") or self.config.max_tokens or MAX_TOKENS,
            temperature=self.config.temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        text = "".join(b.text for b in msg.content if hasattr(b, "text"))
        return LLMResponse(
            text=text, model=model, offline=False,
            usage={
                "input_tokens": getattr(msg.usage, "input_tokens", 0),
                "output_tokens": getattr(msg.usage, "output_tokens", 0),
            },
        )

    def _offline(self, system: str, user: str) -> LLMResponse:
        role = "general"
        s = system.lower()
        for key in ("scope", "hazard", "policy", "eval", "red", "residual", "incident", "gate"):
            if key in s:
                role = {
                    "eval": "eval_planner",
                    "red": "red_team",
                    "residual": "residual_risk",
                    "gate": "gatekeeper",
                }.get(key, key)
                break
        m = re.search(r"system[:\s]+([^\n]+)", user, re.I)
        sys_id = m.group(1).strip()[:40] if m else "system"
        templates = {
            "scope": (
                f"## Scope ({sys_id})\n"
                f"- Users: general employees\n"
                f"- Data: may include internal docs user pastes\n"
                f"- Capabilities: answer, summarize, draft\n"
                f"- Out of scope: autonomous tool execution on prod\n"
            ),
            "hazard": (
                f"## Hazard map ({sys_id})\n"
                f"1. Sensitive data leakage in answers\n"
                f"2. Over confident advice in regulated topics\n"
                f"3. Prompt injection via pasted content\n"
                f"4. Harassment or unsafe content if filters fail\n"
            ),
            "policy": (
                f"## Policy map ({sys_id})\n"
                f"- Aligns with acceptable use: yes with filters\n"
                f"- Gaps: unclear retention for pasted secrets\n"
                f"- Required: block list for credentials patterns\n"
            ),
            "eval_planner": (
                f"## Eval plan ({sys_id})\n"
                f"- Golden set: injection, PII, medical overclaim\n"
                f"- Metrics: refusal quality, false refuse rate\n"
                f"- Gate: fail closed if injection pass rate drops\n"
            ),
            "red_team": (
                f"## Red team ideas ({sys_id}) (defensive)\n"
                f"- Categories: injection, data exfil attempts, policy bypass tone\n"
                f"- Expected: refuse or safe completion\n"
                f"- No step by step attack recipes in this offline pack\n"
            ),
            "residual_risk": (
                f"## Residual risk ({sys_id})\n"
                f"- Medium: novel injection forms\n"
                f"- Low: basic PII regex after mitigations\n"
                f"- Owner: product + safety reviewer\n"
            ),
            "incident": (
                f"## Incident outline ({sys_id})\n"
                f"- Detect: user report or eval alert\n"
                f"- Contain: disable feature flag\n"
                f"- Notify: safety channel and legal if needed\n"
                f"- Learn: add case to golden set\n"
            ),
            "gatekeeper": (
                f"## Gatekeeper pack ({sys_id})\n"
                f"- Artifacts complete: scope through incident\n"
                f"- Recommendation: conditional release after eval gate\n"
                f"- Human must approve\n"
            ),
            "general": f"[offline safety] {user[:200]}\n",
        }
        text = templates.get(role, templates["general"])
        return LLMResponse(
            text=text, model="offline-standin", offline=True,
            usage={"input_tokens": 0, "output_tokens": len(text.split())},
        )
