from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

REVIEW_ROOT = Path(__file__).resolve().parent / "examples" / "sample_review"
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

    @property
    def systems_dir(self) -> Path:
        return self.review_root / "systems"

    @property
    def policies_dir(self) -> Path:
        return self.review_root / "policies"

    @property
    def evals_dir(self) -> Path:
        return self.review_root / "evals"

    @property
    def notes_dir(self) -> Path:
        return self.review_root / "notes"

    @property
    def drafts_dir(self) -> Path:
        return self.review_root / "drafts"

    @property
    def exports_dir(self) -> Path:
        return self.review_root / "exports"

    @property
    def incidents_dir(self) -> Path:
        return self.review_root / "incidents"

    def ensure_dirs(self) -> None:
        for directory in (
            self.systems_dir,
            self.policies_dir,
            self.evals_dir,
            self.notes_dir,
            self.drafts_dir,
            self.exports_dir,
            self.incidents_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)
