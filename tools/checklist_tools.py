from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List
from config import CHECKLISTS_DIR


@dataclass
class CheckItem:
    id: str
    text: str
    done: bool = False


def load_checklist(name: str) -> List[CheckItem]:
    path = CHECKLISTS_DIR / name
    if not path.exists():
        path = CHECKLISTS_DIR / f"{name}.md"
    if not path.exists():
        return []
    items = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = re.match(r"^-\s+\[([ xX])\]\s+(.+)$", line)
        if m:
            items.append(CheckItem(id=f"c{i}", text=m.group(2).strip(), done=m.group(1).lower() == "x"))
    return items


def checklist_report(items: List[CheckItem]) -> str:
    lines = ["## Checklist", ""]
    pending = 0
    for it in items:
        mark = "x" if it.done else " "
        lines.append(f"- [{mark}] {it.text}")
        if not it.done:
            pending += 1
    lines += ["", f"Pending: {pending} / {len(items)}"]
    return "\n".join(lines)
