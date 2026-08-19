#!/usr/bin/env python3
from __future__ import annotations
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import AgentConfig
from orchestrator import SafetyOrchestrator


def main() -> int:
    p = argparse.ArgumentParser(description="Multi-agent AI safety review")
    p.add_argument("--system", required=True, help="System id, e.g. demo-chat-assistant")
    p.add_argument("--offline", action="store_true", default=True)
    p.add_argument("--live", action="store_true")
    p.add_argument("--ship", action="store_true")
    args = p.parse_args()
    config = AgentConfig(offline=not args.live, api_key=os.getenv("ANTHROPIC_API_KEY"))
    orch = SafetyOrchestrator(config)
    print(f"System: {args.system} | offline={config.offline}")
    report = orch.run(args.system, ship=args.ship)
    print("\n=== REPORT ===")
    for s in report.steps:
        print(" -", s)
    print("ok:", report.ok)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
