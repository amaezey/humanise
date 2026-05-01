#!/usr/bin/env python3
"""Tests for humanise/vocabulary.yml — user-facing strings + prose templates.

Covers U9 of the audit-report redesign plan:
- load_vocabulary() shape + schema_version pin
- key-existence for every key the renderer reads
- string_for() placeholder substitution + fail-fast cases
- byte-equivalence: refactored renderer preserves the legacy text on a fixed
  set of canonical strings (catches accidental edits to vocabulary.yml)

Run: python3 dev/evals/test_vocabulary.py
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUMANISE = ROOT / "humanise"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    if str(HUMANISE) not in sys.path:
        sys.path.insert(0, str(HUMANISE))
    spec.loader.exec_module(module)
    return module


registries = _load_module("registries", HUMANISE / "registries.py")

FAILURES = 0


def fail(msg):
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"  ok: {msg}")


# --- load_vocabulary() shape ---

print("=== load_vocabulary ===")

vocab = registries.load_vocabulary()

if not isinstance(vocab, dict):
    fail(f"load_vocabulary must return dict, got {type(vocab).__name__}")
else:
    ok("loaded vocabulary as dict")

if vocab.get("schema_version") != "1":
    fail(f"schema_version must be '1', got {vocab.get('schema_version')!r}")
else:
    ok("schema_version pinned to '1'")

# Confirm caching: second call returns the same object.
if registries.load_vocabulary() is vocab:
    ok("load_vocabulary caches the parsed payload")
else:
    fail("load_vocabulary should cache the parsed payload but returned a fresh object")


# --- Required top-level sections ---

print("\n=== top-level sections ===")

REQUIRED_SECTIONS = {
    "severity_labels",
    "action_labels",
    "status_labels",
    "pressure_status",
    "failure_modes",
    "depth_consequence",
    "depth_summary",
    "section_headings",
    "inline_labels",
    "templates",
    "pressure_explanation",
}

missing_sections = sorted(REQUIRED_SECTIONS - set(vocab))
if missing_sections:
    fail(f"vocabulary.yml missing required sections: {missing_sections}")
else:
    ok(f"every required top-level section present ({len(REQUIRED_SECTIONS)})")


# --- Per-section key coverage ---

print("\n=== severity_labels ===")
for sev in ("hard_fail", "strong_warning", "context_warning"):
    try:
        label = registries.severity_label(sev)
    except KeyError as e:
        fail(f"severity_label({sev!r}) raised: {e}")
        continue
    if not isinstance(label, str) or not label:
        fail(f"severity_label({sev!r}) returned empty/non-string: {label!r}")
    else:
        ok(f"severity_label({sev!r}) = {label!r}")

print("\n=== action_labels ===")
for action in ("fix", "preserve_with_disclosure_or_user_decision"):
    try:
        label = registries.action_label(action)
    except KeyError as e:
        fail(f"action_label({action!r}) raised: {e}")
        continue
    if not isinstance(label, str) or not label:
        fail(f"action_label({action!r}) returned empty/non-string: {label!r}")
    else:
        ok(f"action_label({action!r}) = {label!r}")

print("\n=== status_labels ===")
for status in ("clear", "flagged", "none"):
    try:
        label = registries.status_label(status)
    except KeyError as e:
        fail(f"status_label({status!r}) raised: {e}")
        continue
    if not isinstance(label, str) or not label:
        fail(f"status_label({status!r}) returned empty/non-string: {label!r}")
    else:
        ok(f"status_label({status!r}) = {label!r}")

print("\n=== pressure_status ===")
if registries.pressure_status(True) != "triggered":
    fail(f"pressure_status(True) should be 'triggered', got {registries.pressure_status(True)!r}")
else:
    ok("pressure_status(True) = 'triggered'")
if registries.pressure_status(False) != "clear":
    fail(f"pressure_status(False) should be 'clear', got {registries.pressure_status(False)!r}")
else:
    ok("pressure_status(False) = 'clear'")


# --- failure_modes catalogue ---

print("\n=== failure_modes ===")
EXPECTED_FAILURE_KEYS = {
    "provenance_residue",
    "synthetic_significance",
    "frictionless_structure",
    "generic_abstraction",
    "voice_erasure",
    "genre_misfit",
}
catalogue = registries.failure_mode_metadata()
missing_keys = sorted(EXPECTED_FAILURE_KEYS - set(catalogue))
if missing_keys:
    fail(f"failure_modes missing keys: {missing_keys}")
else:
    ok(f"failure_modes carries all six expected keys")
for key, meta in catalogue.items():
    if "label" not in meta or "summary" not in meta:
        fail(f"failure_modes[{key!r}] missing label/summary")
        continue
    if not meta["label"] or not meta["summary"]:
        fail(f"failure_modes[{key!r}] has empty label or summary")


# --- depth_consequence ---

print("\n=== depth_consequence ===")
for sev in ("hard_fail", "strong_warning", "context_warning"):
    try:
        text = registries.depth_consequence_text(sev)
    except KeyError as e:
        fail(f"depth_consequence_text({sev!r}) raised: {e}")
        continue
    if not text or not isinstance(text, str):
        fail(f"depth_consequence_text({sev!r}) returned empty/non-string: {text!r}")
    else:
        ok(f"depth_consequence_text({sev!r}) → {text[:48]!r}...")


# --- depth_summary ---

print("\n=== depth_summary ===")
for key in (
    "balanced_strong_or_hard",
    "balanced_context_only",
    "balanced_clean",
    "all_clean",
    "all_failures",
):
    try:
        text = registries.string_for(f"depth_summary.{key}")
    except KeyError as e:
        fail(f"depth_summary.{key} raised: {e}")
        continue
    if not text:
        fail(f"depth_summary.{key} empty")
    else:
        ok(f"depth_summary.{key} populated")


# --- templates: round-trip placeholder substitution ---

print("\n=== templates: placeholder substitution ===")

summary_flagged = registries.string_for(
    "templates.summary_flagged", flagged=3, total=49
)
expected_flagged = "3 of 49 checks were flagged for AI-style writing patterns."
if summary_flagged != expected_flagged:
    fail(f"summary_flagged: expected {expected_flagged!r}, got {summary_flagged!r}")
else:
    ok("templates.summary_flagged renders byte-equivalent to legacy text")

summary_all_clear = registries.string_for("templates.summary_all_clear", total=49)
expected_all_clear = "All 49 checks were clear."
if summary_all_clear != expected_all_clear:
    fail(f"summary_all_clear: expected {expected_all_clear!r}, got {summary_all_clear!r}")
else:
    ok("templates.summary_all_clear renders byte-equivalent to legacy text")

severity_line = registries.string_for(
    "templates.severity_line",
    hard_fail=0,
    strong_warning=2,
    context_warning=1,
    pressure="clear",
)
expected_severity = "0 hard_fail · 2 strong_warning · 1 context_warning · pressure: clear"
if severity_line != expected_severity:
    fail(f"severity_line: expected {expected_severity!r}, got {severity_line!r}")
else:
    ok("templates.severity_line renders byte-equivalent to legacy text")

table_header = registries.string_for("templates.table_header", depth="All")
expected_header = "| Check | Status | What it looks for | What happened here | Why this matters | All action |"
if table_header != expected_header:
    fail(f"table_header: expected {expected_header!r}, got {table_header!r}")
else:
    ok("templates.table_header renders byte-equivalent to legacy text")

# Table separator must remain six pipes — depended on by a downstream renderer test in U11.
sep = registries.string_for("templates.table_separator")
if sep != "|---|---|---|---|---|---|":
    fail(f"table_separator drift: got {sep!r}")
else:
    ok("templates.table_separator preserved")


# --- string_for() fail-fast modes ---

print("\n=== string_for fail-fast ===")

try:
    registries.string_for("templates.does_not_exist")
except KeyError as e:
    if "templates.does_not_exist" in str(e):
        ok("string_for raises KeyError with the dotted key on miss")
    else:
        fail(f"string_for KeyError missing key path: {e}")
else:
    fail("string_for did not raise on unknown key")

try:
    registries.string_for("templates.summary_all_clear")  # missing required {total}
except KeyError as e:
    if "total" in str(e) and "summary_all_clear" in str(e):
        ok("string_for raises KeyError naming the missing placeholder + template key")
    else:
        fail(f"string_for placeholder error message unhelpful: {e}")
else:
    fail("string_for did not raise on missing placeholder")

try:
    registries.string_for("templates")  # nested dict, not a string
except TypeError as e:
    if "string template" in str(e):
        ok("string_for raises TypeError when the resolved value is not a string")
    else:
        fail(f"string_for non-string error message unhelpful: {e}")
else:
    fail("string_for did not raise on non-string vocabulary value")


# --- Renderer integration: every f-string with user-facing text routes through registries ---

print("\n=== renderer integration ===")

import re as _re  # noqa: E402

renderer_source = (HUMANISE / "grade.py").read_text()

# These literals would be the legacy hardcoded forms. If any reappear in
# grade.py, U9's "no hardcoded user-facing strings" claim is broken.
LEGACY_LITERALS = [
    'SEVERITY_LABELS = {',
    'ACTION_LABELS = {',
    'FAILURE_MODE_METADATA = {',
    '"Must fix"',
    '"Strong AI-writing signal"',
    '"Disclose or ask before preserving"',
    '"Frictionless structure"',
    '"Provenance residue"',
    '"Fix at Balanced and All."',
    '"All checks pass."',
    '"Hard failures or strong warnings remain',
    '"AI-pressure looks for accumulation',
]

residual = [lit for lit in LEGACY_LITERALS if lit in renderer_source]
if residual:
    fail(
        f"grade.py still contains legacy hardcoded user-facing strings: {residual}. "
        f"Move them to vocabulary.yml."
    )
else:
    ok(f"grade.py contains no legacy hardcoded user-facing strings ({len(LEGACY_LITERALS)} checked)")


# --- Summary ---

if FAILURES:
    print(f"\n{FAILURES} FAILURES")
    sys.exit(1)
print("\n========================================")
print("ALL PASSED")
