from __future__ import annotations
import argparse
import json
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config import AgentConfig
from orchestrator import SafetyOrchestrator


def run_suite(scenarios_path: Path) -> dict:
    scenarios = json.loads(scenarios_path.read_text(encoding="utf-8"))
    results = []
    for scenario in scenarios:
        with tempfile.TemporaryDirectory() as temp:
            config = AgentConfig(review_root=Path(temp), offline=True)
            config.ensure_dirs()
            system_id = scenario["id"]
            (config.systems_dir / f"{system_id}.md").write_text(scenario["brief"], encoding="utf-8")
            (config.policies_dir / "acceptable_use.md").write_text(
                "Require least privilege, traceable evidence, fail-closed behavior, and human approval for consequential actions.",
                encoding="utf-8",
            )
            report = SafetyOrchestrator(config).run(system_id)
            locations = {
                "scope": config.notes_dir / f"{system_id}_scope.md",
                "hazards": config.notes_dir / f"{system_id}_hazards.md",
                "policy_map": config.notes_dir / f"{system_id}_policy_map.md",
                "eval_plan": config.notes_dir / f"{system_id}_eval_plan.md",
                "red_team": config.notes_dir / f"{system_id}_red_team.md",
                "residual_risk": config.notes_dir / f"{system_id}_residual_risk.md",
                "incident_plan": config.incidents_dir / f"{system_id}_incident_plan.md",
                "safety_pack": config.exports_dir / f"{system_id}_safety_pack.md",
            }
            missing = [name for name in scenario["expected"] if not locations[name].exists()]
            approved = (config.exports_dir / f"{system_id}_APPROVED.txt").exists()
            passed = report.ok and not missing and not approved and "HUMAN GATE" in report.steps[-1]
            results.append({
                "id": system_id,
                "passed": passed,
                "missing_artifacts": missing,
                "approval_marker_created": approved,
                "final_step": report.steps[-1] if report.steps else None,
            })
    passed_count = sum(1 for item in results if item["passed"])
    return {
        "suite": "f09-heldout-control-path",
        "scope": "Structural control-path evidence only. This is not a semantic safety benchmark or certification.",
        "passed": passed_count,
        "total": len(results),
        "pass_rate": passed_count / len(results) if results else 0,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenarios", type=Path, default=Path(__file__).with_name("heldout_scenarios.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run_suite(args.scenarios)
    rendered = json.dumps(result, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0 if result["passed"] == result["total"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
