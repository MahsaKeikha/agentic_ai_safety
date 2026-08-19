from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from config import AgentConfig
from llm_client import LLMClient, LLMResponse
from memory import SafetyMemory


@dataclass
class AgentResult:
    ok: bool
    output: str
    artifacts: Dict[str, Any] = field(default_factory=dict)
    log: List[str] = field(default_factory=list)

    def add(self, msg: str) -> None:
        self.log.append(msg)


class BaseAgent:
    name = "base"

    def __init__(self, config: AgentConfig, memory: SafetyMemory, llm: LLMClient | None = None):
        self.config = config
        self.memory = memory
        self.llm = llm or LLMClient(config)

    def _complete(self, system: str, user: str) -> LLMResponse:
        return self.llm.complete(system, user)
