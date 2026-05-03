#!/usr/bin/env python3
"""Tests for humanise/scripts/vocabulary.json — user-facing strings + prose templates.

Covers U9 of the audit-report redesign plan:
- load_vocabulary() shape + schema_version pin
- key-existence for every key the renderer reads
- string_for() placeholder substitution + fail-fast cases
- byte-equivalence: refactored renderer preserves the legacy text on a fixed
  set of canonical strings (catches accidental edits to vocabulary.json)

Run: python3 dev/evals/test_vocabulary.py
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HUMANISE = ROOT / "humanise"
SCRIPTS = HUMANISE / "scripts"


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec.loader.exec_module(module)
    return module


registries = _load_module("registries", SCRIPTS / "registries.py")

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
    "severity_glyphs",
    "action_labels",
    "status_labels",
    "signal_stacking_status",
    "failure_modes",
    "depth_consequence",
    "depth_summary",
    "section_headings",
    "inline_labels",
    "templates",
    "short_signal_stacking_explanation",
}

missing_sections = sorted(REQUIRED_SECTIONS - set(vocab))
if missing_sections:
    fail(f"vocabulary.json missing required sections: {missing_sections}")
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

print("\n=== signal_stacking_status ===")
if registries.signal_stacking_status(True) != "triggered":
    fail(f"signal_stacking_status(True) should be 'triggered', got {registries.signal_stacking_status(True)!r}")
else:
    ok("signal_stacking_status(True) = 'triggered'")
if registries.signal_stacking_status(False) != "clear":
    fail(f"signal_stacking_status(False) should be 'clear', got {registries.signal_stacking_status(False)!r}")
else:
    ok("signal_stacking_status(False) = 'clear'")


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

severity_line = registries.string_for(
    "templates.severity_line",
    hard_fail=0,
    strong_warning=2,
    context_warning=1,
    signal_stacking="clear",
)
expected_severity = "0 hard fail · 2 strong warning · 1 context warning · signal stacking: clear"
if severity_line != expected_severity:
    fail(f"severity_line: expected {expected_severity!r}, got {severity_line!r}")
else:
    ok("templates.severity_line renders byte-equivalent to expected text")

# Phase 3 dual-layer templates.
flagged_block = registries.string_for(
    "templates.flagged_pattern_block",
    glyph="x", name="Em dashes", quoted='"scene lands"', action="Fix",
)
expected_block = 'x **Em dashes** — "scene lands" — Action: Fix'
if flagged_block != expected_block:
    fail(f"flagged_pattern_block: expected {expected_block!r}, got {flagged_block!r}")
else:
    ok("templates.flagged_pattern_block renders byte-equivalent to expected text")

flagged_block_no_quote = registries.string_for(
    "templates.flagged_pattern_block_no_quote",
    glyph="!", name="Triad density", action="Fix",
)
expected_block_no_quote = "! **Triad density** — Action: Fix"
if flagged_block_no_quote != expected_block_no_quote:
    fail(f"flagged_pattern_block_no_quote: expected {expected_block_no_quote!r}, got {flagged_block_no_quote!r}")
else:
    ok("templates.flagged_pattern_block_no_quote renders byte-equivalent to expected text")

category_collapse = registries.string_for(
    "templates.category_collapse", category="Style", clear=6, total=6,
)
expected_collapse = "**Style** — 6/6 clear"
if category_collapse != expected_collapse:
    fail(f"category_collapse: expected {expected_collapse!r}, got {category_collapse!r}")
else:
    ok("templates.category_collapse renders byte-equivalent to expected text")

category_heading = registries.string_for(
    "templates.category_subtable_heading", category="Style", flagged=2, total=6,
)
expected_heading = "**Style** — 2 flagged of 6"
if category_heading != expected_heading:
    fail(f"category_subtable_heading: expected {expected_heading!r}, got {category_heading!r}")
else:
    ok("templates.category_subtable_heading renders byte-equivalent to expected text")

# Sub-table separator and header must remain three pipes — Layer 2 contract.
header = registries.string_for("templates.category_subtable_header")
if header != "| Pattern | Result | Action |":
    fail(f"category_subtable_header drift: got {header!r}")
else:
    ok("templates.category_subtable_header preserved")

sep = registries.string_for("templates.category_subtable_separator")
if sep != "| --- | --- | --- |":
    fail(f"category_subtable_separator drift: got {sep!r}")
else:
    ok("templates.category_subtable_separator preserved")

all_clear = registries.string_for("templates.all_clear_single_line", total=48)
expected_all_clear = "48 of 48 clear · agent reading clean · signal stacking: clear."
if all_clear != expected_all_clear:
    fail(f"all_clear_single_line: expected {expected_all_clear!r}, got {all_clear!r}")
else:
    ok("templates.all_clear_single_line renders byte-equivalent to expected text")

# Severity glyphs — Layer 1 per-flagged-pattern blocks.
for sev, expected_glyph in (("hard_fail", "x"), ("strong_warning", "!"), ("context_warning", "?")):
    glyph = registries.string_for(f"severity_glyphs.{sev}")
    if glyph != expected_glyph:
        fail(f"severity_glyphs.{sev}: expected {expected_glyph!r}, got {glyph!r}")
    else:
        ok(f"severity_glyphs.{sev} = {glyph!r}")


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
    registries.string_for("templates.all_clear_single_line")  # missing required {total}
except KeyError as e:
    if "total" in str(e) and "all_clear_single_line" in str(e):
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

renderer_source = (HUMANISE / "scripts" / "grade.py").read_text()

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
        f"Move them to vocabulary.json."
    )
else:
    ok(f"grade.py contains no legacy hardcoded user-facing strings ({len(LEGACY_LITERALS)} checked)")


# --- Summary ---

if FAILURES:
    print(f"\n{FAILURES} FAILURES")
    sys.exit(1)
print("\n========================================")
print("ALL PASSED")
