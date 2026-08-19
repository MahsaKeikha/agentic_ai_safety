from __future__ import annotations
from pathlib import Path
from config import SYSTEMS_DIR, POLICIES_DIR, NOTES_DIR, DRAFTS_DIR, EXPORTS_DIR, INCIDENTS_DIR


class SafetyMemory:
    def read_system(self, system_id: str) -> str:
        path = SYSTEMS_DIR / f"{system_id}.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def read_policy(self) -> str:
        path = POLICIES_DIR / "acceptable_use.md"
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def write_note(self, name: str, content: str) -> Path:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        path = NOTES_DIR / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path

    def read_note(self, name: str) -> str:
        path = NOTES_DIR / (name if name.endswith(".md") else f"{name}.md")
        return path.read_text(encoding="utf-8") if path.exists() else ""

    def write_draft(self, name: str, content: str) -> Path:
        DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
        path = DRAFTS_DIR / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path

    def write_export(self, name: str, content: str) -> Path:
        EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
        path = EXPORTS_DIR / name
        path.write_text(content, encoding="utf-8")
        return path

    def write_incident_template(self, name: str, content: str) -> Path:
        INCIDENTS_DIR.mkdir(parents=True, exist_ok=True)
        path = INCIDENTS_DIR / (name if name.endswith(".md") else f"{name}.md")
        path.write_text(content, encoding="utf-8")
        return path
