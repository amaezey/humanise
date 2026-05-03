#!/usr/bin/env python3
"""
diff_renders.py — Phase 2 verification harness.

Runs humanise/scripts/grade.py JSON output over the U10 corpus and either captures
a baseline or verifies current output matches the captured baseline.

Phase 2 (U7-U9) is a no-op refactor; this harness is the gate that proves it.

Usage:
    python3 dev/evals/diff_renders.py --capture
    python3 dev/evals/diff_renders.py --verify   (default)

This is the U10a skeleton — equality check + first-divergence report. U10b
will extend it with structured key-path diff output and baseline-regeneration
support for U8's deliberate contract-shape changes.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GRADE = REPO_ROOT / "humanise" / "scripts" / "grade.py"
BASELINE_DIR = REPO_ROOT / "dev" / "evals" / "diff_baseline"

CORPUS = [
    "dev/skill-workspace/iteration-1/eval-0-audit-ai-cultural/with_skill/run-1/outputs/prompt.md",
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
    p = Path(path)
    if "skill-workspace" in path:
        parts = p.parts
        iter_part = next((x for x in parts if x.startswith("iteration-")), None)
        eval_part = next((x for x in parts if x.startswith("eval-")), None)
        if iter_part and eval_part:
            iter_num = iter_part.split("-")[1]
            return f"iter-{iter_num}-{eval_part}"
    return p.stem


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
