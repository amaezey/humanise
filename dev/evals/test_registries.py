#!/usr/bin/env python3
"""Tests for humanise/scripts/registries.py — pattern + judgement registry loaders.

Run: python3 dev/evals/test_registries.py
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUMANISE = ROOT / "humanise"

# Load registries.py and grade.py the same way the rest of the test suite does.
def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    if str(HUMANISE) not in sys.path:
        sys.path.insert(0, str(HUMANISE))
    spec.loader.exec_module(module)
    return module


registries = _load_module("registries", HUMANISE / "scripts" / "registries.py")
grade = _load_module("humanise_grade", HUMANISE / "scripts" / "grade.py")

ALL_CHECKS = grade.ALL_CHECKS

FAILURES = 0


def fail(msg):
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"  ok: {msg}")


# --- load_patterns() shape and completeness ---

print("=== load_patterns ===")

patterns = registries.load_patterns()
if not isinstance(patterns, dict):
    fail(f"load_patterns must return dict, got {type(patterns).__name__}")
elif len(patterns) == 0:
    fail("load_patterns returned empty dict")
else:
    ok(f"loaded {len(patterns)} patterns")

# Every ALL_CHECKS check_id must have a registry record.
missing = sorted(set(ALL_CHECKS) - set(patterns))
if missing:
    fail(f"{len(missing)} check_id(s) in ALL_CHECKS missing from patterns.json: {missing}")
else:
    ok(f"every ALL_CHECKS check_id ({len(ALL_CHECKS)}) has a patterns.json record")

# patterns.json should not contain unknown check_ids.
extra = sorted(set(patterns) - set(ALL_CHECKS))
if extra:
    fail(f"patterns.json contains check_id(s) not in ALL_CHECKS: {extra}")
else:
    ok("no unexpected check_ids in patterns.json")


# --- pattern_for() lookup ---

print("\n=== pattern_for ===")

rec = registries.pattern_for("no-em-dashes")
if rec.get("severity") != "strong_warning":
    fail(f"pattern_for('no-em-dashes').severity should be strong_warning, got {rec.get('severity')!r}")
elif rec.get("category") != "Style":
    fail(f"pattern_for('no-em-dashes').category should be Style, got {rec.get('category')!r}")
else:
    ok("pattern_for returns expected record for known check_id")

try:
    registries.pattern_for("definitely-not-a-real-check-id")
except KeyError as e:
    if "known" in str(e).lower():
        ok("pattern_for raises KeyError with known ids hint for unknown check_id")
    else:
        fail(f"pattern_for KeyError missing known-ids hint: {e}")
else:
    fail("pattern_for should raise KeyError for unknown check_id")


# --- helper functions used by grade.py ---

print("\n=== metadata_for / report_text_for / why_it_matters_for ===")

meta = registries.metadata_for("no-em-dashes")
expected_keys = {"severity", "failure_modes", "evidence_role", "guidance"}
if set(meta) != expected_keys:
    fail(f"metadata_for keys {set(meta)} should be {expected_keys}")
else:
    ok("metadata_for returns the four-field subset")

# Unknown check_id → defensive default (preserves pre-U7 annotate_result behaviour).
default_meta = registries.metadata_for("not-a-real-check")
if default_meta.get("severity") != "context_warning":
    fail(f"metadata_for fallback severity should be context_warning, got {default_meta.get('severity')!r}")
else:
    ok("metadata_for falls back to context_warning for unknown check_id")

label, description = registries.report_text_for("no-em-dashes")
if label != "Em dashes" or "em dash" not in description.lower():
    fail(f"report_text_for('no-em-dashes') unexpected: ({label!r}, {description!r})")
else:
    ok("report_text_for returns expected (label, description)")

# Unknown check_id → derived label fallback
fb_label, _ = registries.report_text_for("some-fake-check")
if fb_label != "Some Fake Check":
    fail(f"report_text_for fallback label should derive from id, got {fb_label!r}")
else:
    ok("report_text_for falls back to derived label for unknown check_id")

why = registries.why_it_matters_for("no-em-dashes")
if not isinstance(why, str) or "em dash" not in why.lower():
    fail(f"why_it_matters_for('no-em-dashes') unexpected: {why!r}")
else:
    ok("why_it_matters_for returns expected string")


# --- per-record schema validation ---

print("\n=== per-record schema ===")

for cid, rec in patterns.items():
    for required in ("category", "short_name", "description", "why_it_matters",
                     "severity", "failure_modes", "evidence_role", "guidance"):
        if required not in rec:
            fail(f"{cid} missing required field: {required}")
    if rec.get("severity") not in {"hard_fail", "strong_warning", "context_warning"}:
        fail(f"{cid} has invalid severity: {rec.get('severity')!r}")
    if rec.get("category") not in registries.VALID_CATEGORIES:
        fail(f"{cid} has invalid category: {rec.get('category')!r}")
    if not isinstance(rec.get("failure_modes"), list) or not rec["failure_modes"]:
        fail(f"{cid} failure_modes must be non-empty list")
ok(f"all {len(patterns)} records pass schema validation")


# --- alternatives content present where expected ---

print("\n=== alternatives content ===")

# 16 patterns are expected to have alternatives content (from alternatives.md).
with_alternatives = [cid for cid, rec in patterns.items() if "alternatives" in rec]
if len(with_alternatives) != 16:
    fail(f"expected 16 patterns with alternatives content, got {len(with_alternatives)}")
else:
    ok(f"{len(with_alternatives)} patterns carry alternatives content")


# --- judgement registry ---

print("\n=== load_judgement / judgement_for ===")

judgement = registries.load_judgement()
records = judgement.get("records", [])
if len(records) != 8:
    fail(f"expected 8 agent-judgement records, got {len(records)}")
else:
    ok("loaded 8 agent-judgement records")

j_rec = registries.judgement_for("structural_monotony")
if not isinstance(j_rec, dict) or j_rec.get("id") != "structural_monotony":
    fail(f"judgement_for('structural_monotony') unexpected: {j_rec}")
else:
    ok("judgement_for returns expected record for known id")

try:
    registries.judgement_for("not-a-real-judgement-id")
except KeyError:
    ok("judgement_for raises KeyError for unknown id")
else:
    fail("judgement_for should raise KeyError for unknown id")

try:
    registries._validate_judgement({
        "schema_version": "1",
        "records": [{"id": "broken", "prompt": "Prompt", "answer_schema": {"type": "state"}}],
    })
except ValueError as e:
    if "flagged_when" in str(e):
        ok("load_judgement validation names missing fields")
    else:
        fail(f"judgement validation error should name missing field, got: {e}")
else:
    fail("judgement validation should reject records missing flagged_when")


# --- summary ---

print("\n========================================")
if FAILURES:
    print(f"FAILED: {FAILURES} assertion(s)")
    sys.exit(1)
print("ALL PASSED")
