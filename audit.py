from __future__ import annotations
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any


class AuditIntegrityError(RuntimeError):
    pass


class AuditTrail:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    @staticmethod
    def _digest(payload: dict[str, Any]) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _last_record(self) -> dict[str, Any] | None:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return None
        last = None
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    last = json.loads(line)
        return last

    def append(
        self,
        *,
        actor: str,
        action: str,
        target: str,
        outcome: str,
        details: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        with self._lock:
            previous = self._last_record()
            payload = {
                "sequence": 1 if previous is None else previous["sequence"] + 1,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "actor": actor,
                "action": action,
                "target": target,
                "outcome": outcome,
                "details": details or {},
                "previous_hash": None if previous is None else previous["record_hash"],
            }
            payload["record_hash"] = self._digest(payload)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, sort_keys=True) + "\n")
                handle.flush()
                os.fsync(handle.fileno())
            return payload

    def verify(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"valid": True, "records": 0, "last_hash": None}
        previous_hash = None
        count = 0
        with self.path.open("r", encoding="utf-8") as handle:
            for expected_sequence, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise AuditIntegrityError(f"Invalid JSON at record {expected_sequence}") from exc
                record_hash = record.pop("record_hash", None)
                if record.get("sequence") != expected_sequence:
                    raise AuditIntegrityError(f"Invalid sequence at record {expected_sequence}")
                if record.get("previous_hash") != previous_hash:
                    raise AuditIntegrityError(f"Broken hash link at record {expected_sequence}")
                calculated = self._digest(record)
                if record_hash != calculated:
                    raise AuditIntegrityError(f"Record hash mismatch at record {expected_sequence}")
                previous_hash = record_hash
                count += 1
        return {"valid": True, "records": count, "last_hash": previous_hash}
