#!/usr/bin/env python3
"""Regenerate the corpus-wide grade sweep report."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = ROOT / "dev" / "evals" / "grade-sweep-report.json"
SAMPLE_ROOT = ROOT / "dev" / "evals" / "samples"
SETS = {
    "existing_samples": sorted(SAMPLE_ROOT.glob("*.md")),
    "generated_ai": sorted((SAMPLE_ROOT / "generated-ai").glob("*.md")),
    "human_sourced": sorted((SAMPLE_ROOT / "human-sourced").glob("*.md")),
}


def load_grade_module():
    spec = importlib.util.spec_from_file_location("grade", ROOT / "humanise" / "scripts" / "grade.py")
    grade = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise RuntimeError("Could not load humanise/scripts/grade.py")
    spec.loader.exec_module(grade)
    return grade


def grade_file(grade, path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    results = [grade.annotate_result(fn(text)) for fn in grade.ALL_CHECKS.values()]
    total = len(results)
    passed = sum(1 for result in results if result["passed"])
    failures = [result for result in results if not result["passed"]]
    failures_by_severity: dict[str, int] = {}

    for failure in failures:
        severity = failure["severity"]
        failures_by_severity[severity] = failures_by_severity.get(severity, 0) + 1

    return {
        "file": str(path.relative_to(ROOT)),
        "pass_rate": f"{passed}/{total}",
        "failures_by_severity": failures_by_severity,
        "depth_results": grade.depth_results(results),
        "failed_checks": [failure["text"] for failure in failures],
    }


def summarise(items: list[dict]) -> dict:
    fail_counts = [len(item["failed_checks"]) for item in items]
    severity_totals: dict[str, int] = {}
    depth_check_status_counts: dict[str, dict[str, int]] = {}
    action_totals: dict[str, dict[str, int]] = {}
    check_hits: dict[str, int] = {}

    for item in items:
        for severity, count in item["failures_by_severity"].items():
            severity_totals[severity] = severity_totals.get(severity, 0) + count
        for check in item["failed_checks"]:
            check_hits[check] = check_hits.get(check, 0) + 1
        for depth, data in item["depth_results"].items():
            status = data["check_status"]
            depth_check_status_counts.setdefault(depth, {})[status] = depth_check_status_counts.setdefault(depth, {}).get(status, 0) + 1
            action_totals.setdefault(
                depth,
                {"required_fixes": 0, "preservable_with_disclosure": 0, "user_decision_needed": 0},
            )
            action_totals[depth]["required_fixes"] += len(data["required_fixes"])
            action_totals[depth]["preservable_with_disclosure"] += len(data["preservable_with_disclosure"])
            action_totals[depth]["user_decision_needed"] += len(data["user_decision_needed"])

    return {
        "n": len(items),
        "avg_failed_checks": round(sum(fail_counts) / len(items), 2) if items else 0,
        "min_failed_checks": min(fail_counts) if fail_counts else 0,
        "max_failed_checks": max(fail_counts) if fail_counts else 0,
        "severity_totals": dict(sorted(severity_totals.items())),
        "depth_check_status_counts": depth_check_status_counts,
        "depth_action_totals": action_totals,
        "top_failed_checks": sorted(check_hits.items(), key=lambda item: (-item[1], item[0]))[:15],
    }


def main() -> int:
    grade = load_grade_module()
    report = {"sets": {}, "summary": {}}

    for name, files in SETS.items():
        items = [grade_file(grade, path) for path in files]
        report["sets"][name] = items
        report["summary"][name] = summarise(items)

    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
