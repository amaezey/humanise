#!/usr/bin/env python3
"""Self-tests for humanise/scripts/judgement.json.

Independent of the U7 registry loader. Loads the JSON directly so the
file's shape can be validated without going through the loader.

Run: python3 dev/evals/test_judgement_yaml.py
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JUDGEMENT_PATH = ROOT / "humanise" / "scripts" / "judgement.json"

FAILURES = 0


def fail(msg):
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"  ok: {msg}")


# --- file exists and parses cleanly ---

print("\n=== judgement.json load ===")
if not JUDGEMENT_PATH.exists():
    fail(f"judgement.json missing at {JUDGEMENT_PATH}")
    sys.exit(1)

with JUDGEMENT_PATH.open() as f:
    data = json.load(f)

if not isinstance(data, dict):
    fail(f"top-level JSON should be a mapping, got {type(data).__name__}")
    sys.exit(1)
ok("judgement.json parses as a mapping")


# --- top-level shape ---

print("\n=== judgement.json top-level keys ===")
for key in ("schema_version", "records"):
    if key not in data:
        fail(f"top-level key '{key}' missing")
    else:
        ok(f"top-level key '{key}' present")

if data.get("schema_version") != "1":
    fail(f"schema_version should be '1', got {data.get('schema_version')!r}")
else:
    ok("schema_version pinned to '1'")


# --- records list ---

print("\n=== judgement.json records ===")
records = data.get("records", [])
if not isinstance(records, list):
    fail(f"'records' should be a list, got {type(records).__name__}")
    sys.exit(1)

EXPECTED_IDS = [
    "structural_monotony",
    "tonal_uniformity",
    "faux_specificity",
    "neutrality_collapse",
    "even_jargon_distribution",
    "forced_synesthesia",
    "generic_metaphors",
    "genre_specific",
]
actual_ids = [r.get("id") for r in records]
if actual_ids != EXPECTED_IDS:
    fail(f"records order/ids mismatch.\n  expected: {EXPECTED_IDS}\n  got:      {actual_ids}")
else:
    ok(f"all 8 records present in canonical order")


# --- each record has required fields ---

REQUIRED_FIELDS = ("id", "pattern_ref", "prompt", "answer_schema", "flagged_when")
for record in records:
    rid = record.get("id", "<unknown>")
    for field in REQUIRED_FIELDS:
        if field not in record:
            fail(f"record `{rid}` missing required field `{field}`")
    schema = record.get("answer_schema") or {}
    if "type" not in schema:
        fail(f"record `{rid}` answer_schema missing `type`")
    elif schema["type"] not in ("trichotomy", "state", "list", "presence", "composite"):
        fail(f"record `{rid}` answer_schema.type unrecognised: {schema['type']!r}")
    else:
        ok(f"record `{rid}` has type={schema['type']}")


# --- pattern_ref values ---

print("\n=== judgement.json pattern_ref values ===")
EXPECTED_PATTERN_REFS = {
    "structural_monotony": None,
    "tonal_uniformity": 35,
    "faux_specificity": 36,
    "neutrality_collapse": 37,
    "even_jargon_distribution": None,
    "forced_synesthesia": 28,
    "generic_metaphors": 30,
    "genre_specific": 41,
}
for record in records:
    rid = record.get("id")
    expected = EXPECTED_PATTERN_REFS.get(rid)
    actual = record.get("pattern_ref")
    if actual != expected:
        fail(f"record `{rid}` pattern_ref should be {expected!r}, got {actual!r}")
    else:
        ok(f"record `{rid}` pattern_ref={expected!r}")


# --- polymorphic genre slot ---

print("\n=== judgement.json genre_specific sub_records ===")
genre_record = next((r for r in records if r.get("id") == "genre_specific"), None)
if genre_record is None:
    fail("genre_specific record missing")
else:
    sub = genre_record.get("sub_records", {})
    EXPECTED_GENRES = {"academic", "student_essay", "poetry", "fiction", "default"}
    actual_genres = set(sub.keys())
    if actual_genres != EXPECTED_GENRES:
        fail(f"genre_specific sub_records mismatch.\n  expected: {sorted(EXPECTED_GENRES)}\n  got:      {sorted(actual_genres)}")
    else:
        ok(f"genre_specific has all 5 sub_records: {sorted(EXPECTED_GENRES)}")
    # Each sub-record carries a watchlist (initially empty for non-default genres).
    for genre, sub_record in sub.items():
        if "watchlist" not in sub_record:
            fail(f"genre_specific.sub_records.{genre} missing `watchlist`")
        elif not isinstance(sub_record["watchlist"], list):
            fail(f"genre_specific.sub_records.{genre}.watchlist should be a list, got {type(sub_record['watchlist']).__name__}")
        else:
            ok(f"genre_specific.sub_records.{genre}.watchlist is a list (size={len(sub_record['watchlist'])})")


# --- JSON round-trip stability ---

print("\n=== judgement.json round-trip ===")
roundtripped = json.loads(json.dumps(data))
if roundtripped != data:
    fail("json.loads(json.dumps(data)) does not equal original data")
else:
    ok("data round-trips through JSON cleanly")


# --- Summary ---

print(f"\n{'='*40}")
if FAILURES:
    print(f"FAILED: {FAILURES} assertion(s) broken")
    sys.exit(1)
else:
    print("ALL PASSED")
    sys.exit(0)
