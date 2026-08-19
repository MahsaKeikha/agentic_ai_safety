from __future__ import annotations
from pathlib import Path
from config import REVIEW_ROOT


def read_text(path: str | Path) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = REVIEW_ROOT / p
    return p.read_text(encoding="utf-8") if p.exists() else ""


def write_text(path: str | Path, content: str) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = REVIEW_ROOT / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return str(p)
