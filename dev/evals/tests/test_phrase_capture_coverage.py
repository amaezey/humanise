#!/usr/bin/env python3
"""Lightweight coverage test for phrase capture across all flagged checks.

Runs grade.py against the noisy AI samples and verifies every flagged
check exposes either:
  - one or more `quoted_phrases` that substring-match the input, or
  - a `metric` string (for checks whose signal is a draft-wide
    measurement rather than a quotable span — see METRIC_ONLY_CHECKS), or
  - is in the STRUCTURAL_NO_PHRASE allow-list (signal is structural; no
    single span captures it).

Any flagged check outside those buckets is a phrase-capture gap. This
test is the gate that catches the class of bug where a regex-only check
flags but renders as a bare `<glyph> <name>` line with no evidence the
user can act on.

Run: python3 dev/evals/test_phrase_capture_coverage.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SAMPLES = sorted((ROOT / "dev" / "evals" / "samples" / "generated-ai").glob("*.md"))

_spec = importlib.util.spec_from_file_location("grade", ROOT / "human-eyes" / "scripts" / "grade.py")
grade = importlib.util.module_from_spec(_spec)
if _spec.loader is None:
    raise RuntimeError("Could not load human-eyes/scripts/grade.py")
_spec.loader.exec_module(grade)

# Checks whose signal is a draft-wide metric, not a quotable span. Each
# must surface a `metric` string in its result so the renderer shows
# `<glyph> <name>: <metric>` instead of a bare opener.
METRIC_ONLY_CHECKS = {
    "vocabulary-diversity",
    "paragraph-length-uniformity",
    "sentence-length-variance",
}

# Checks whose signal is genuinely structural — no single phrase or
# scalar metric is informative. Bare-opener rendering is acceptable.
STRUCTURAL_NO_PHRASE: set[str] = set()

# Meta checks that the renderer suppresses entirely — they don't surface
# in the audit body so phrase capture is moot.
SUPPRESSED_FROM_RENDER = {
    "overall-signal-stacking",
}

FAILURES = []


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def normalise(s: str) -> str:
    import re
    return re.sub(r"\s+", " ", s.lower()).strip()


print(f"=== phrase-capture coverage across {len(SAMPLES)} AI samples ===\n")

flagged_seen: dict[str, list[str]] = {}
checks_without_phrases: dict[str, list[str]] = {}

for sample in SAMPLES:
    text = sample.read_text(encoding="utf-8")
    norm_text = normalise(text)
    results = [grade.annotate_result(fn(text)) for fn in grade.ALL_CHECKS.values()]
    contract = grade.human_report(results)
    for c in contract["programmatic_checks"]:
        if c["status"] != "flagged":
            continue
        cid = c["id"]
        if cid in SUPPRESSED_FROM_RENDER:
            continue
        flagged_seen.setdefault(cid, []).append(sample.name)
        ev = c.get("evidence") or {}
        phrases = ev.get("quoted_phrases") or []
        metric = ev.get("metric")

        if cid in METRIC_ONLY_CHECKS:
            if not metric:
                fail(f"{cid} (metric-only) flagged on {sample.name} but no metric string in evidence")
            continue
        if cid in STRUCTURAL_NO_PHRASE:
            continue
        if not phrases:
            checks_without_phrases.setdefault(cid, []).append(sample.name)
            continue
        # Verify at least one captured phrase substring-matches the input.
        if not any(normalise(p) in norm_text for p in phrases):
            fail(
                f"{cid} flagged on {sample.name}: phrases captured but none "
                f"substring-match input. First phrase: {phrases[0][:80]!r}"
            )

if checks_without_phrases:
    for cid, samples in sorted(checks_without_phrases.items()):
        fail(
            f"{cid} flagged but exposes no phrases on {len(samples)} sample(s) "
            f"(e.g. {samples[0]}). Either add phrase capture, or add to "
            f"METRIC_ONLY_CHECKS / STRUCTURAL_NO_PHRASE allow-list."
        )

if not FAILURES:
    print(f"\n{len(flagged_seen)} distinct check IDs flagged across the corpus; all carry phrases or metrics or are allow-listed.")

print("\n========================================")
if FAILURES:
    print(f"{len(FAILURES)} FAILURE(S)")
    sys.exit(1)
print("ALL PASSED")
