#!/usr/bin/env python3
"""
diff_renders.py — grader regression gate.

Runs human-eyes/scripts/grade.py JSON output over a fixed corpus of inputs
and pins every field of the output against a captured baseline. Used to lock
down no-op refactors of grade.py and to catch unintended behaviour shifts.

Usage:
    python3 dev/evals/harness/diff_renders.py --verify   (default)
    python3 dev/evals/harness/diff_renders.py --capture  (only when grader output legitimately changes)
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
GRADE = REPO_ROOT / "human-eyes" / "scripts" / "grade.py"
BASELINE_DIR = REPO_ROOT / "dev" / "evals" / "diff_baseline"

CORPUS = [
    "dev/evals/samples/audit-fixtures/cultural-didion-skill-prompt.md",
    "dev/evals/samples/generated-ai/02-cultural-didion.md",
    "dev/evals/samples/generated-ai/03-tech-productivity-apps.md",
    "dev/evals/samples/generated-ai/04-science-mycorrhizal.md",
    "dev/evals/samples/generated-ai/06-wellbeing-sleep-grief.md",
    "dev/evals/samples/generated-ai/10-opinion-slow-creativity.md",
    "dev/evals/samples/human-sourced/19c-darwin-origin.md",
    "dev/evals/samples/human-sourced/20c-woolf-room.md",
    "dev/evals/samples/human-sourced/21c-alamut-agora-museum.md",
    "dev/evals/samples/synthetic/synthetic-all-clear.md",
    "dev/evals/samples/synthetic/synthetic-hard-fail-only.md",
]


def sample_id(path):
    return Path(path).stem


def canonicalise(payload, input_path):
    """Strip volatile fields and normalise path for stable diffing.

    The `file` field is path-dependent; normalise it to the canonical relative
    path from CORPUS so baselines are independent of how grade.py was invoked.
    audit-format-v1 metadata carries volatile timestamp/run_id fields; strip
    those nested fields before comparing baselines.
    """
    payload["file"] = input_path
    payload.pop("metadata", None)  # defensive — none today, future-proof
    report_metadata = payload.get("human_report", {}).get("metadata")
    if isinstance(report_metadata, dict):
        report_metadata.pop("timestamp", None)
        report_metadata.pop("run_id", None)
    return payload


def run_grade(input_path):
    full_path = REPO_ROOT / input_path
    result = subprocess.run(
        ["python3", str(GRADE), "--format", "json", str(full_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return canonicalise(json.loads(result.stdout), input_path)


def first_diff(a, b, path=""):
    """Return the first divergence between two JSON values, or None if equal."""
    if type(a) is not type(b):
        return f"{path or '.'}: type mismatch ({type(a).__name__} vs {type(b).__name__})"
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                return f"{path}.{k}: only in current"
            if k not in b:
                return f"{path}.{k}: only in baseline"
            sub = first_diff(a[k], b[k], f"{path}.{k}")
            if sub:
                return sub
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}: list length differs (baseline={len(a)}, current={len(b)})"
        for i, (av, bv) in enumerate(zip(a, b)):
            sub = first_diff(av, bv, f"{path}[{i}]")
            if sub:
                return sub
        return None
    if a != b:
        return f"{path or '.'}: value differs (baseline={repr(a)[:80]}, current={repr(b)[:80]})"
    return None


def capture():
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    for input_path in CORPUS:
        sid = sample_id(input_path)
        payload = run_grade(input_path)
        out = BASELINE_DIR / f"{sid}.json"
        out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        print(f"captured  {sid}")
    print(f"\n{len(CORPUS)} baselines written to {BASELINE_DIR.relative_to(REPO_ROOT)}/")


def verify():
    failures = []
    for input_path in CORPUS:
        sid = sample_id(input_path)
        baseline_path = BASELINE_DIR / f"{sid}.json"
        if not baseline_path.exists():
            failures.append((input_path, sid, "BASELINE MISSING"))
            continue
        baseline = json.loads(baseline_path.read_text())
        current = run_grade(input_path)
        diff = first_diff(baseline, current)
        if diff is not None:
            failures.append((input_path, sid, diff))

    if failures:
        for input_path, sid, diff in failures:
            print(f"FAIL  {sid}")
            print(f"      input: {input_path}")
            print(f"      diff:  {diff}")
        sys.exit(1)
    print(f"OK  {len(CORPUS)} baselines match current grade.py output")


if __name__ == "__main__":
    if "--capture" in sys.argv:
        capture()
    else:
        verify()
