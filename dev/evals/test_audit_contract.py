#!/usr/bin/env python3
"""Tests the audit-format-v1 contract emitted by humanise/grade.py human_report().

Hand-rolled assertions per the plan's no-deps stance — the contract is small
enough to validate without a full JSON Schema library. The schema file at
humanise/contracts/audit-format-v1.json is the authoritative shape and is
loaded for completeness checks (required fields, enums) but the assertions
below are written explicitly for actionable error messages.

Run: python3 dev/evals/test_audit_contract.py
"""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUMANISE = ROOT / "humanise"
CONTRACT_PATH = HUMANISE / "contracts" / "audit-format-v1.json"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    if str(HUMANISE) not in sys.path:
        sys.path.insert(0, str(HUMANISE))
    spec.loader.exec_module(module)
    return module


grade = _load_module("humanise_grade", HUMANISE / "grade.py")
registries = _load_module("registries", HUMANISE / "registries.py")

human_report = grade.human_report
annotate_result = grade.annotate_result
ALL_CHECKS = grade.ALL_CHECKS

FAILURES = 0


def fail(msg):
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"  ok: {msg}")


# --- schema file loads as JSON ---

print("=== schema file ===")
schema = json.loads(CONTRACT_PATH.read_text())
required_top = set(schema["required"])
expected_top = {"schema_version", "programmatic_checks", "agent_judgement", "aggregates", "metadata"}
if required_top != expected_top:
    fail(f"schema required top-level fields {required_top} should be {expected_top}")
else:
    ok(f"schema declares required top-level fields: {sorted(required_top)}")

if not schema.get("additionalProperties") is False:
    fail("schema must set additionalProperties: false at top level")
else:
    ok("schema rejects additional top-level properties")


# --- representative grade.py output ---

print("\n=== representative output (synthetic-hard-fail-only) ===")

import subprocess
sample = ROOT / "dev/evals/samples/synthetic/synthetic-hard-fail-only.md"
result = subprocess.run(
    ["python3", str(HUMANISE / "grade.py"), "--format", "json", str(sample)],
    capture_output=True, text=True, check=True,
)
contract = json.loads(result.stdout)["human_report"]


# --- top-level shape ---

print("\n=== top-level shape ===")

if set(contract) != expected_top:
    fail(f"contract top-level keys {set(contract)} should equal {expected_top}")
else:
    ok("contract has exactly the expected top-level keys")

if contract["schema_version"] != "1":
    fail(f"schema_version should be '1', got {contract['schema_version']!r}")
else:
    ok("schema_version pinned to '1'")


# --- programmatic_checks ---

print("\n=== programmatic_checks ===")

pc = contract["programmatic_checks"]
if not isinstance(pc, list):
    fail(f"programmatic_checks should be list, got {type(pc).__name__}")
elif len(pc) != len(ALL_CHECKS):
    fail(f"programmatic_checks should have {len(ALL_CHECKS)} entries, got {len(pc)}")
else:
    ok(f"programmatic_checks has {len(pc)} entries (one per ALL_CHECKS)")

# Every entry has required fields, valid status, valid severity, known id.
required_check_fields = {"id", "status", "severity", "category", "failure_modes", "evidence"}
valid_status = {"clear", "flagged"}
valid_severity = {"hard_fail", "strong_warning", "context_warning"}
known_ids = set(ALL_CHECKS)
all_ok = True
for entry in pc:
    if set(entry) != required_check_fields:
        fail(f"check {entry.get('id')!r} keys {set(entry)} should be {required_check_fields}")
        all_ok = False
        break
    if entry["status"] not in valid_status:
        fail(f"check {entry['id']!r} status {entry['status']!r} not in {valid_status}")
        all_ok = False
        break
    if entry["severity"] not in valid_severity:
        fail(f"check {entry['id']!r} severity {entry['severity']!r} not in {valid_severity}")
        all_ok = False
        break
    if entry["id"] not in known_ids:
        fail(f"check {entry['id']!r} not in ALL_CHECKS")
        all_ok = False
        break
if all_ok:
    ok("every programmatic_check has required fields, valid status/severity, known id")


# --- common evidence envelope ---

print("\n=== common evidence envelope ===")

required_envelope = {"quoted_phrases", "locations", "counts", "raw"}
all_envelope_ok = True
for entry in pc:
    env = entry["evidence"]
    if set(env) != required_envelope:
        fail(f"check {entry['id']!r} evidence keys {set(env)} should be {required_envelope}")
        all_envelope_ok = False
        break
    if not isinstance(env["quoted_phrases"], list):
        fail(f"check {entry['id']!r} evidence.quoted_phrases must be list")
        all_envelope_ok = False
        break
    if not isinstance(env["locations"], list):
        fail(f"check {entry['id']!r} evidence.locations must be list")
        all_envelope_ok = False
        break
    if not isinstance(env["counts"], dict):
        fail(f"check {entry['id']!r} evidence.counts must be dict")
        all_envelope_ok = False
        break
    if not isinstance(env["raw"], dict):
        fail(f"check {entry['id']!r} evidence.raw must be dict")
        all_envelope_ok = False
        break
if all_envelope_ok:
    ok(f"every programmatic_check.evidence has the four common envelope fields")

# Spot-check: a flagged check with known matches should populate quoted_phrases.
collab = next((e for e in pc if e["id"] == "no-collaborative-artifacts"), None)
if collab and collab["status"] == "flagged":
    if not collab["evidence"]["quoted_phrases"]:
        fail(f"no-collaborative-artifacts is flagged but evidence.quoted_phrases is empty: {collab['evidence']}")
    else:
        ok(f"no-collaborative-artifacts evidence.quoted_phrases = {collab['evidence']['quoted_phrases']}")


# --- aggregates ---

print("\n=== aggregates ===")

aggr = contract["aggregates"]
if set(aggr) != {"by_severity", "by_category", "ai_pressure"}:
    fail(f"aggregates keys {set(aggr)} should be {{'by_severity', 'by_category', 'ai_pressure'}}")
else:
    ok("aggregates has by_severity / by_category / ai_pressure")

if set(aggr["by_severity"]) != {"hard_fail", "strong_warning", "context_warning"}:
    fail(f"by_severity keys {set(aggr['by_severity'])} should be the three tiers")
else:
    ok("by_severity has all three severity tiers")

# by_severity sums to total flagged count
flagged_count = sum(1 for e in pc if e["status"] == "flagged")
sev_sum = sum(aggr["by_severity"].values())
if sev_sum != flagged_count:
    fail(f"by_severity sum {sev_sum} should equal flagged_count {flagged_count}")
else:
    ok(f"by_severity sum ({sev_sum}) equals flagged count")

ap = aggr["ai_pressure"]
required_ap = {"score", "threshold", "triggered", "components", "vocabulary_points"}
if set(ap) != required_ap:
    fail(f"ai_pressure keys {set(ap)} should be {required_ap}")
else:
    ok("ai_pressure has all required fields")
if not isinstance(ap["triggered"], bool):
    fail(f"ai_pressure.triggered must be bool, got {type(ap['triggered']).__name__}")
else:
    ok("ai_pressure.triggered is boolean")


# --- metadata ---

print("\n=== metadata ===")

md = contract["metadata"]
if "schema_version" not in md or md["schema_version"] != "1":
    fail(f"metadata.schema_version should be '1', got {md.get('schema_version')!r}")
else:
    ok("metadata.schema_version = '1'")
if "grader_version" not in md:
    fail("metadata.grader_version missing")
else:
    ok(f"metadata.grader_version = {md['grader_version']!r}")
if "timestamp" not in md:
    fail("metadata.timestamp missing")
else:
    ok("metadata.timestamp present")
if "run_id" not in md:
    fail("metadata.run_id missing")
else:
    ok("metadata.run_id present")


# --- no prose strings at the top level ---

print("\n=== no-prose smoke test ===")

forbidden = {"overview", "confidence", "ai_pressure_explanation", "score", "failed_checks", "all_checks"}
present = forbidden & set(contract)
if present:
    fail(f"contract should not carry pre-formatted prose; found legacy keys: {present}")
else:
    ok(f"no legacy prose keys present (R14: confidence, overview, ai_pressure_explanation removed)")


# --- all-clear case ---

print("\n=== all-clear contract ===")

clear_contract = human_report([
    annotate_result({"text": cid, "passed": True, "evidence": "clean"}) for cid in ALL_CHECKS
])
clear_aggr = clear_contract["aggregates"]
if any(clear_aggr["by_severity"].values()):
    fail(f"all-clear: by_severity should be all-zero, got {clear_aggr['by_severity']}")
elif clear_aggr["by_category"]:
    fail(f"all-clear: by_category should be empty, got {clear_aggr['by_category']}")
elif clear_aggr["ai_pressure"]["triggered"]:
    fail("all-clear: ai_pressure.triggered should be False")
else:
    ok("all-clear case: all aggregates report zero / not-triggered")


# --- summary ---

print("\n========================================")
if FAILURES:
    print(f"FAILED: {FAILURES} assertion(s)")
    sys.exit(1)
print("ALL PASSED")
