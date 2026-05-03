#!/usr/bin/env python3
"""Tests for format_two_layer() — Phase 3 dual-layer audit renderer (U11).

Covers:
- All-clear single-line response (R8)
- Layer 1 + Layer 2 separator on flagged input (R1)
- Layer 1 per-flagged-pattern block shape (R5): glyph + name + quoted phrase
  + action; no description, no "why this matters"
- Severity glyphs (x / ! / ?)
- Layer 2 sub-table shape (R4): three columns Pattern | Result | Action
- Layer 2 category collapse to one-liner when every check clear (R3)
- Layer 2 ordering matches the eight patterns.md headings (R2)
- overall-ai-signal-pressure suppressed from Layer 1 + Layer 2
- Phrase cap at 3 with overflow indicator
- Action column reflects depth (balanced vs all) (R22)

Run: python3 dev/evals/test_two_layer_render.py
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("grade", ROOT / "humanise" / "scripts" / "grade.py")
_grade = importlib.util.module_from_spec(_spec)
if _spec.loader is None:
    raise RuntimeError("Could not load humanise/scripts/grade.py")
_spec.loader.exec_module(_grade)

ALL_CHECKS = _grade.ALL_CHECKS
annotate_result = _grade.annotate_result
format_two_layer = _grade.format_two_layer
human_report = _grade.human_report
CATEGORY_ORDER = _grade.CATEGORY_ORDER
LAYER_1_PHRASE_CAP = _grade.LAYER_1_PHRASE_CAP

FAILURES = 0


def fail(msg):
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"  ok: {msg}")


def all_clear_results():
    """Build a results list where every check is clear."""
    return [
        annotate_result({"text": cid, "passed": True, "evidence": "clean"})
        for cid in ALL_CHECKS
    ]


def flag(cid, evidence_phrases=None, evidence_text="flagged here"):
    """Build a single failed-check result with optional quoted phrases.

    Phrases flow into the contract's `evidence.quoted_phrases` via the
    `matches` field that `_extract_quoted_phrases` reads first.
    """
    payload = {
        "text": cid,
        "passed": False,
        "evidence": evidence_text,
    }
    if evidence_phrases is not None:
        payload["matches"] = list(evidence_phrases)
    return annotate_result(payload)


# --- All-clear case (R8) ---

print("=== all-clear single-line ===")

clear_render = format_two_layer(all_clear_results(), depth="balanced")
clear_lines = clear_render.splitlines()

if "---" in clear_render:
    fail(f"all-clear render should not include a Layer 1/Layer 2 separator; got:\n{clear_render}")
else:
    ok("all-clear render carries no Layer 1/Layer 2 separator")

if len(clear_lines) != 2:
    fail(f"all-clear render should be two lines (one-liner + next-step prompt); got {len(clear_lines)} lines: {clear_render!r}")
else:
    ok("all-clear render is one-line summary plus next-step prompt")

if "agent reading clean" not in clear_lines[0] or "pressure: clear" not in clear_lines[0]:
    fail(f"all-clear summary missing canonical phrasing; got {clear_lines[0]!r}")
else:
    ok("all-clear summary names agent + pressure status")

# Confidence label removed (R14) — must not appear.
for forbidden in ("Confidence:", "Low.", "Medium.", "High."):
    if forbidden in clear_render:
        fail(f"all-clear render should not include confidence label {forbidden!r}; got:\n{clear_render}")
        break
else:
    ok("all-clear render carries no confidence label (R14)")


# --- Flagged case: Layer 1 + Layer 2 separator (R1) ---

print("\n=== flagged: Layer 1 + Layer 2 separator ===")

# Use one hard_fail (no-collaborative-artifacts) + one strong_warning
# (no-em-dashes) so we can exercise both the `x` and `!` glyphs from a
# single fixture. no-collaborative-artifacts is in 'Communication'; em-dashes
# is in 'Style'. Pick a third check that leaves at least one category clear
# for the collapse test.
exercised_ids = {"no-collaborative-artifacts", "no-em-dashes"}
mixed_results = [
    flag("no-collaborative-artifacts", evidence_phrases=["I'll generate the report for you"]),
    flag("no-em-dashes", evidence_phrases=["—"]),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid not in exercised_ids
]
mixed_render = format_two_layer(mixed_results, depth="balanced")

if "\n---\n" not in mixed_render:
    fail(f"flagged render should contain Layer 1/Layer 2 separator; got:\n{mixed_render[:600]}")
else:
    ok("flagged render contains Layer 1/Layer 2 separator")

layer_1, layer_2 = mixed_render.split("\n---\n", 1)


# --- Layer 1 per-flagged block shape (R5) ---

print("\n=== Layer 1 block shape ===")

for forbidden in ("What it looks for:", "What happened here:", "Why this matters:"):
    if forbidden in layer_1:
        fail(f"Layer 1 should not include {forbidden!r} (R5); found in:\n{layer_1}")
        break
else:
    ok("Layer 1 carries no description / why-this-matters labels (R5)")

# Glyph + name + quoted phrase + action — verify on the no-em-dashes block
# (em-dashes is strong_warning per patterns.yaml → glyph '!').
em_dash_block = next(
    (line for line in layer_1.splitlines() if "Em dashes" in line),
    None,
)
if em_dash_block is None:
    fail(f"Layer 1 missing Em dashes block; got:\n{layer_1}")
elif not em_dash_block.startswith("! **Em dashes**"):
    fail(f"Em dashes block should start with strong_warning glyph '!'; got {em_dash_block!r}")
elif '"—"' not in em_dash_block:
    fail(f"Em dashes block should quote the phrase; got {em_dash_block!r}")
elif "Action: Fix" not in em_dash_block:
    fail(f"Em dashes block should carry Action: Fix; got {em_dash_block!r}")
else:
    ok("Em dashes block: glyph + name + quoted phrase + action")


# --- Severity glyphs across tiers ---

print("\n=== severity glyphs ===")

# Both fixtures cover hard_fail (no-collaborative-artifacts → "Assistant
# residue") and strong_warning (no-em-dashes → "Em dashes"). The third
# tier (context_warning → '?') is exercised in the depth-aware Action
# section below using no-curly-quotes.
expected_glyphs = {
    "Em dashes": "!",
    "Assistant residue": "x",
}
for label, glyph in expected_glyphs.items():
    block = next((line for line in layer_1.splitlines() if label in line), None)
    if block is None:
        fail(f"Layer 1 missing block for {label!r}; got:\n{layer_1}")
    elif not block.startswith(f"{glyph} **{label}**"):
        fail(f"{label!r} block should use glyph {glyph!r}; got {block!r}")
    else:
        ok(f"{label!r} renders with glyph {glyph!r}")


# --- Pressure explanation: single sentence ---

print("\n=== one-sentence pressure explanation ===")

# Layer 1 has: heading, severity_line, pressure_sentence, blank, [blocks...]
layer_1_lines = [line for line in layer_1.splitlines() if line]
pressure_line = layer_1_lines[2] if len(layer_1_lines) >= 3 else ""
if not pressure_line.startswith("Pressure"):
    fail(f"Layer 1 third non-blank line should be pressure explanation; got {pressure_line!r}")
elif pressure_line.count(".") > 1:
    fail(f"Pressure explanation should be a single sentence (one period); got {pressure_line!r}")
else:
    ok("pressure explanation is a single sentence")

# Confirm legacy multi-sentence prose did not survive.
if "AI-pressure looks for accumulation" in mixed_render:
    fail("Legacy multi-sentence pressure explanation should be gone")
else:
    ok("Legacy multi-sentence pressure explanation removed")


# --- Layer 2 sub-table shape (R4) ---

print("\n=== Layer 2 sub-table shape ===")

if "| Pattern | Result | Action |" not in layer_2:
    fail(f"Layer 2 sub-table header should be three-column 'Pattern | Result | Action'; got:\n{layer_2[:600]}")
else:
    ok("Layer 2 sub-table header is three-column")

if "| --- | --- | --- |" not in layer_2:
    fail(f"Layer 2 sub-table separator should be three-column; got:\n{layer_2[:600]}")
else:
    ok("Layer 2 sub-table separator is three-column")

# No legacy six-column shape.
if "| What it looks for | What happened here | Why this matters |" in layer_2:
    fail("Layer 2 should not include legacy six-column header columns")
else:
    ok("Layer 2 does not carry legacy six-column header")


# --- Layer 2 category ordering (R2) ---

print("\n=== Layer 2 category ordering ===")

# Each category appears at least once in Layer 2 (collapsed or expanded), in
# CATEGORY_ORDER. Aggregate AI-signal pressure is suppressed (overall meta).
seen_at = []
for category in CATEGORY_ORDER:
    needle = f"**{category}**"
    if needle not in layer_2:
        fail(f"Layer 2 missing category {category!r}")
        continue
    seen_at.append((category, layer_2.index(needle)))

if seen_at == sorted(seen_at, key=lambda pair: pair[1]):
    ok("Layer 2 categories render in CATEGORY_ORDER")
else:
    fail(f"Layer 2 categories out of order: {[c for c, _ in seen_at]}")

if "Aggregate AI-signal pressure" in mixed_render:
    fail("Aggregate AI-signal pressure category should be suppressed (R8/R22)")
else:
    ok("Aggregate AI-signal pressure category suppressed from output")


# --- Layer 2 collapse to one-liner when every check clear (R3) ---

print("\n=== Layer 2 collapse on clear category ===")

# 'Sensory and atmospheric' has no flagged check in `mixed_results`, so it
# should collapse. Find the line and assert shape.
COLLAPSE_CATEGORY = "Sensory and atmospheric"
collapse_line = next(
    (line for line in layer_2.splitlines() if line.startswith(f"**{COLLAPSE_CATEGORY}**")),
    None,
)
if collapse_line is None:
    fail(f"Layer 2 missing {COLLAPSE_CATEGORY!r} line; got:\n{layer_2}")
elif "clear" not in collapse_line or "/" not in collapse_line:
    fail(f"{COLLAPSE_CATEGORY!r} line should collapse to N/N clear; got {collapse_line!r}")
elif "| Pattern | Result | Action |" in layer_2.split(collapse_line, 1)[1].split("**", 1)[0]:
    fail(f"{COLLAPSE_CATEGORY!r} category should collapse — found a sub-table after its heading: {collapse_line!r}")
else:
    ok(f"{COLLAPSE_CATEGORY!r} category collapses to one-liner: {collapse_line!r}")


# --- overall-ai-signal-pressure suppression (R8/R22) ---

print("\n=== overall-ai-signal-pressure suppression ===")

# Build a contract where the meta-check is flagged.
pressure_flagged_results = [
    annotate_result({
        "text": "overall-ai-signal-pressure",
        "passed": False,
        "evidence": "Overall AI-signal pressure 5/4",
        "score": 5,
        "threshold": 4,
        "components": ["paragraph length uniformity"],
        "vocabulary_pressure": {"points": 0, "reasons": [], "worst_generic": 0,
                                "gptzero_matches": [], "kobak_style_distinct": 0,
                                "kobak_style_density": 0.0, "kobak_style_sample": []},
    }),
    flag("no-em-dashes", evidence_phrases=["—"]),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid not in {"overall-ai-signal-pressure", "no-em-dashes"}
]
pressure_render = format_two_layer(pressure_flagged_results, depth="balanced")

# Verdict line should still report pressure: triggered.
if "pressure: triggered" not in pressure_render:
    fail("Verdict line should report 'pressure: triggered' when meta-check is flagged")
else:
    ok("Verdict line carries pressure: triggered")

# But the meta-check itself should not appear as a Layer 1 block or Layer 2 row.
if "Aggregate AI-signal pressure" in pressure_render:
    fail("Layer 2 should not surface the suppressed Aggregate AI-signal pressure category")
else:
    ok("Layer 2 does not include the suppressed category")

# The check's short_name should not appear.
if "Overall AI-signal pressure" in pressure_render:
    fail("Layer 1 / Layer 2 should not include the overall-ai-signal-pressure block")
else:
    ok("Layer 1 / Layer 2 does not include the meta-check block")

# If pressure is the only flagged programmatic check, the audit is not
# all-clear: the meta-check stays suppressed as a row/block, but survives in
# the verdict token.
pressure_only_results = [
    annotate_result({
        "text": "overall-ai-signal-pressure",
        "passed": False,
        "evidence": "Overall AI-signal pressure 5/4",
        "score": 5,
        "threshold": 4,
        "components": ["paragraph length uniformity"],
        "vocabulary_pressure": {"points": 0, "reasons": [], "worst_generic": 0,
                                "gptzero_matches": [], "kobak_style_distinct": 0,
                                "kobak_style_density": 0.0, "kobak_style_sample": []},
    }),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid != "overall-ai-signal-pressure"
]
pressure_only_render = format_two_layer(pressure_only_results, depth="balanced")

if "agent reading clean" in pressure_only_render:
    fail(f"pressure-only failure must not render all-clear; got:\n{pressure_only_render}")
elif "pressure: triggered" not in pressure_only_render:
    fail(f"pressure-only failure should survive in verdict token; got:\n{pressure_only_render}")
elif "1 context_warning" in pressure_only_render:
    fail(f"suppressed pressure meta-check should not inflate visible severity counts; got:\n{pressure_only_render}")
else:
    ok("pressure-only failure renders as pressure triggered without an all-clear line or visible severity count")


# --- Phrase cap (3 + overflow) ---

print("\n=== Layer 1 phrase cap ===")

phrases = [f"phrase{i}" for i in range(LAYER_1_PHRASE_CAP + 4)]  # 7 phrases when cap=3
many_phrase_results = [
    flag("no-triad-density", evidence_phrases=phrases),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid != "no-triad-density"
]
many_render = format_two_layer(many_phrase_results, depth="balanced")
many_layer_1 = many_render.split("\n---\n", 1)[0]

triad_block = next(
    (line for line in many_layer_1.splitlines() if "Triad density" in line),
    None,
)
if triad_block is None:
    fail(f"Layer 1 missing Triad density block; got:\n{many_layer_1}")
else:
    quote_count = triad_block.count('"phrase')
    if quote_count != LAYER_1_PHRASE_CAP:
        fail(f"Layer 1 should cap at {LAYER_1_PHRASE_CAP} phrases; counted {quote_count} in {triad_block!r}")
    elif f"(+{len(phrases) - LAYER_1_PHRASE_CAP} more)" not in triad_block:
        fail(f"Layer 1 should append (+N more) suffix; got {triad_block!r}")
    else:
        ok(f"Layer 1 caps phrases at {LAYER_1_PHRASE_CAP} and appends overflow indicator")


# --- Action column depth-awareness (R22) ---

print("\n=== Action column reflects depth ===")

# At Balanced, context_warning → "Disclose or ask before preserving"; at All
# every flagged → "Fix".
ctx_results = [
    flag("no-curly-quotes", evidence_phrases=['""']),  # context_warning per patterns.yaml
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid != "no-curly-quotes"
]
balanced_render = format_two_layer(ctx_results, depth="balanced")
all_render = format_two_layer(ctx_results, depth="all")

if "Disclose or ask before preserving" not in balanced_render:
    fail("Balanced depth should map context_warning to 'Disclose or ask before preserving'")
else:
    ok("Balanced depth maps context_warning to Disclose or ask before preserving")

if "Disclose or ask before preserving" in all_render:
    fail("All depth should never use 'Disclose or ask before preserving'")
elif "Action: Fix" not in all_render:
    fail("All depth should map every flagged severity to Fix")
else:
    ok("All depth maps every flagged severity to Fix")


# --- All-clear vs flagged: verify visible total excludes meta-check ---

print("\n=== visible total excludes meta-check ===")

clear_count = len([cid for cid in ALL_CHECKS if cid != "overall-ai-signal-pressure"])
expected_summary = f"{clear_count} of {clear_count} clear"
if expected_summary not in clear_render:
    fail(f"all-clear summary should exclude meta-check from visible total; expected {expected_summary!r}, got:\n{clear_render}")
else:
    ok(f"all-clear visible total = {clear_count} (excludes overall-ai-signal-pressure)")


# --- Summary ---

if FAILURES:
    print(f"\n{FAILURES} FAILURES")
    sys.exit(1)
print("\n========================================")
print("ALL PASSED")
