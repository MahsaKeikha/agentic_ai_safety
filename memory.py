from __future__ import annotations
from pathlib import Path
from config import AgentConfig


class SafetyMemory:
    def __init__(self, config: AgentConfig | None = None):
        self.config = config or AgentConfig()
        self.config.ensure_dirs()

    def read_system(self, system_id: str) -> str:
        path = self.config.systems_dir / f"{system_id}.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def read_policy(self) -> str:
        path = self.config.policies_dir / "acceptable_use.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def write_note(self, name: str, content: str) -> Path:
        path = self.config.notes_dir / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path

    def read_note(self, name: str) -> str:
        path = self.config.notes_dir / (name if name.endswith(".md") else f"{name}.md")
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def write_draft(self, name: str, content: str) -> Path:
        path = self.config.drafts_dir / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path

    def write_export(self, name: str, content: str) -> Path:
        path = self.config.exports_dir / name
        path.write_text(content, encoding="utf-8")
        return path

    def write_incident_template(self, name: str, content: str) -> Path:
        path = self.config.incidents_dir / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path
