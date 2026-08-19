from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

REVIEW_ROOT = Path(__file__).resolve().parent / "examples" / "sample_review"
SYSTEMS_DIR = REVIEW_ROOT / "systems"
POLICIES_DIR = REVIEW_ROOT / "policies"
EVALS_DIR = REVIEW_ROOT / "evals"
NOTES_DIR = REVIEW_ROOT / "notes"
DRAFTS_DIR = REVIEW_ROOT / "drafts"
EXPORTS_DIR = REVIEW_ROOT / "exports"
INCIDENTS_DIR = REVIEW_ROOT / "incidents"
CHECKLISTS_DIR = Path(__file__).resolve().parent / "checklists"

DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096
TEMPERATURE = 0.2


@dataclass
class AgentConfig:
    review_root: Path = field(default_factory=lambda: REVIEW_ROOT)
    model: str = DEFAULT_MODEL
    max_tokens: int = MAX_TOKENS
    temperature: float = TEMPERATURE
    offline: bool = True
    api_key: Optional[str] = None

    def ensure_dirs(self) -> None:
        for d in (SYSTEMS_DIR, POLICIES_DIR, EVALS_DIR, NOTES_DIR, DRAFTS_DIR, EXPORTS_DIR, INCIDENTS_DIR):
            d.mkdir(parents=True, exist_ok=True)
