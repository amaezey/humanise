#!/usr/bin/env python3
"""Tests for format_two_layer() — dual-layer audit renderer.

Covers:
- Zero-flag draft renders the full three-line summary (R9, no collapse)
- Layer 1 + Layer 2 separator on flagged input
- Layer 1 per-flagged-pattern block shape (R6 — U5): glyph + name + optional
  quoted phrase, no Action clause
- Severity glyphs (x / ! / ?)
- Layer 2 sub-table shape (R15 / R18 — U4): four columns
  Pattern | Severity | Result | Detail
- Layer 2 category collapse to one-liner when every check clear
- Layer 2 ordering matches the eight patterns.md headings
- overall-signal-stacking suppressed from Layer 1 + Layer 2
- Phrase cap at 3 with overflow indicator
- _action_for_check resolves on agent-judgement-shaped items (U1 + U5
  wiring — severity field flows through `_action_for_check` for downstream
  callers; not surfaced in the audit body itself per R6/R18)

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


# --- Zero-flag draft renders the full three-line shape (R9, U4) ---
#
# U4 removed the all-clear collapse. A clean draft now emits the full
# three-line summary with all-zero counts plus a Layer-2 coverage block
# showing every category collapsed; no single-line shortcut.

print("=== zero-flag draft renders full three-line summary (no collapse) ===")

clear_render = format_two_layer(all_clear_results(), depth="balanced")
clear_lines = clear_render.splitlines()
visible_total = len([cid for cid in ALL_CHECKS if cid != "overall-signal-stacking"])

if "\n---\n" not in clear_render:
    fail(f"clean-draft render must include the Layer 1/Layer 2 separator (no collapse); got:\n{clear_render}")
else:
    ok("clean-draft render keeps the Layer 1/Layer 2 separator")

expected_counts = f"Auto-detected: 0 of {visible_total} flagged · Agent-assessed: 0 of 0 flagged"
if expected_counts not in clear_render:
    fail(f"clean-draft render missing counts line {expected_counts!r}; got:\n{clear_render}")
else:
    ok("clean-draft render carries the counts line with all-zero auto/agent counts")

if "Severity: 0 hard fail · 0 strong warning · 0 context warning" not in clear_render:
    fail(f"clean-draft render missing all-zero severity line; got:\n{clear_render}")
else:
    ok("clean-draft render carries the all-zero severity line")

if "Signal stacking: clear (weaker AI signals are not accumulating)" not in clear_render:
    fail(f"clean-draft render missing the stand-alone signal-stacking clear line; got:\n{clear_render}")
else:
    ok("clean-draft render carries the stand-alone signal-stacking clear line")

# No legacy collapsed shape — the canonical Phase-3 single-line all-clear
# shape and the inline `· signal stacking: ...` suffix are both retired.
if "of 48 clear · agent reading clean · signal stacking: clear." in clear_render:
    fail(f"legacy collapsed all-clear single-line shape should be retired; got:\n{clear_render}")
else:
    ok("legacy collapsed all-clear single-line shape is retired")

# Confidence label removed (R14) — must not appear.
for forbidden in ("Confidence:", "Low.", "Medium.", "High."):
    if forbidden in clear_render:
        fail(f"clean-draft render should not include confidence label {forbidden!r}; got:\n{clear_render}")
        break
else:
    ok("clean-draft render carries no confidence label (R14)")


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
        fail(f"Layer 1 should not include {forbidden!r}; found in:\n{layer_1}")
        break
else:
    ok("Layer 1 carries no description / why-this-matters labels")

# U5 (R6): Action clause is retired. Layer 1 flagged blocks render as
# `<glyph> **<name>** — "<phrase>"` (or just `<glyph> **<name>**` for
# structural patterns with no quotable phrase). Verify on the no-em-dashes
# block (em-dashes is strong_warning per patterns.json → glyph '!').
em_dash_block = next(
    (line for line in layer_1.splitlines() if "Em dashes" in line),
    None,
)
if em_dash_block is None:
    fail(f"Layer 1 missing Em dashes block; got:\n{layer_1}")
elif em_dash_block != '! **Em dashes** — "—"':
    fail(f"Em dashes block should render exactly '! **Em dashes** — \"—\"'; got {em_dash_block!r}")
else:
    ok('Em dashes block renders as `! **Em dashes** — "—"` (no Action clause, R6)')

if "Action:" in layer_1:
    fail(f"Layer 1 should not carry any 'Action:' clause post-U5 (R6); got:\n{layer_1}")
else:
    ok("Layer 1 carries no 'Action:' clause (R6)")


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


# --- Three-line summary block (R1, R2, R3 — U4) ---

print("\n=== three-line summary block ===")

# Layer 1 has: heading, counts_line, severity_line, signal_stacking_line, blank, [blocks...]
layer_1_lines = [line for line in layer_1.splitlines() if line]
if len(layer_1_lines) < 4 or layer_1_lines[0] != "Audit":
    fail(f"Layer 1 should open with 'Audit' heading; got {layer_1_lines[:4]!r}")
elif not layer_1_lines[1].startswith("Auto-detected:"):
    fail(f"Layer 1 second line should be the R1 counts line; got {layer_1_lines[1]!r}")
elif not layer_1_lines[2].startswith("Severity:"):
    fail(f"Layer 1 third line should be the R2 severity line; got {layer_1_lines[2]!r}")
elif "signal stacking:" in layer_1_lines[2].lower():
    fail(f"R2 severity line should not carry the inline signal-stacking suffix; got {layer_1_lines[2]!r}")
elif not layer_1_lines[3].startswith("Signal stacking:"):
    fail(f"Layer 1 fourth line should be the R3 signal-stacking line; got {layer_1_lines[3]!r}")
else:
    ok("Layer 1 opens with the three-line summary block (counts / severity / signal stacking)")

# The R3 signal-stacking line on a non-triggered draft is the canonical
# 'clear (weaker AI signals are not accumulating)' phrase.
if "Signal stacking: clear (weaker AI signals are not accumulating)" not in layer_1:
    fail(f"R3 signal-stacking clear line missing; got:\n{layer_1}")
else:
    ok("R3 signal-stacking clear line renders canonical phrasing")

# Confirm legacy multi-sentence prose did not survive.
if "AI-pressure looks for accumulation" in mixed_render:
    fail("Legacy multi-sentence pressure explanation should be gone")
elif "weaker AI-writing signals stacked to" in mixed_render:
    fail("Legacy short_signal_stacking_explanation prose should be gone (U4 dropped the helper)")
else:
    ok("Legacy multi-sentence signal-stacking explanation removed")


# --- Layer 2 sub-table shape (R15, R18 — U4 four-column) ---

print("\n=== Layer 2 sub-table shape (4-column) ===")

if "| Pattern | Severity | Result | Detail |" not in layer_2:
    fail(f"Layer 2 sub-table header should be the U4 4-column 'Pattern | Severity | Result | Detail'; got:\n{layer_2[:600]}")
else:
    ok("Layer 2 sub-table header is the U4 4-column shape")

if "| --- | --- | --- | --- |" not in layer_2:
    fail(f"Layer 2 sub-table separator should be 4-column; got:\n{layer_2[:600]}")
else:
    ok("Layer 2 sub-table separator is 4-column")

# Action column dropped per R18.
if "| Pattern | Result | Action |" in layer_2 or "Action |" in layer_2.split("**Next step**", 1)[0]:
    fail(f"Layer 2 should not include the Action column (R18); got:\n{layer_2[:600]}")
else:
    ok("Layer 2 does not carry the Action column (R18)")

# Severity column reads the renamed labels (lowercase, space-separated).
em_dash_row = next(
    (line for line in layer_2.splitlines() if "Em dashes" in line and "|" in line),
    None,
)
if em_dash_row is None:
    fail(f"Layer 2 missing Em dashes row; got:\n{layer_2[:600]}")
elif "| strong warning |" not in em_dash_row:
    fail(f"Em dashes row should carry severity 'strong warning' (lowercase, space-separated); got {em_dash_row!r}")
elif "| Flagged |" not in em_dash_row:
    fail(f"Em dashes row should carry result 'Flagged'; got {em_dash_row!r}")
else:
    ok("Layer 2 Em dashes row: severity + Flagged + Detail (guidance) present")

# No legacy six-column shape.
if "| What it looks for | What happened here | Why this matters |" in layer_2:
    fail("Layer 2 should not include legacy six-column header columns")
else:
    ok("Layer 2 does not carry legacy six-column header")


# --- Layer 2 category ordering (R2) ---

print("\n=== Layer 2 category ordering ===")

# Each category appears at least once in Layer 2 (collapsed or expanded), in
# CATEGORY_ORDER. Signal stacking is suppressed (overall meta).
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

if "**Signal stacking**" in mixed_render:
    fail("Signal stacking category heading should be suppressed (R8/R22)")
else:
    ok("Signal stacking category suppressed from output")


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


# --- overall-signal-stacking suppression (R8/R22) ---

print("\n=== overall-signal-stacking suppression ===")

# Build a contract where the meta-check is flagged.
signal_stacking_flagged_results = [
    annotate_result({
        "text": "overall-signal-stacking",
        "passed": False,
        "evidence": "Overall signal stacking 5/4",
        "score": 5,
        "threshold": 4,
        "components": ["paragraph length uniformity"],
        "vocabulary_signal_stacking": {"points": 0, "reasons": [], "worst_generic": 0,
                                "gptzero_matches": [], "kobak_style_distinct": 0,
                                "kobak_style_density": 0.0, "kobak_style_sample": []},
    }),
    flag("no-em-dashes", evidence_phrases=["—"]),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid not in {"overall-signal-stacking", "no-em-dashes"}
]
signal_stacking_render = format_two_layer(signal_stacking_flagged_results, depth="balanced")

# R3 stand-alone signal-stacking line should report triggered + threshold.
if "Signal stacking: triggered — 5 of 4 threshold" not in signal_stacking_render:
    fail(f"R3 line should report 'Signal stacking: triggered — N of M threshold (...)' when meta-check is flagged; got:\n{signal_stacking_render[:600]}")
else:
    ok("R3 stand-alone line carries 'Signal stacking: triggered — 5 of 4 threshold (...)'")

# But the meta-check itself should not appear as a Layer 1 block or Layer 2 row.
if "**Signal stacking**" in signal_stacking_render:
    fail("Layer 2 should not surface the suppressed Signal stacking category heading")
else:
    ok("Layer 2 does not include the suppressed category")

# The check's short_name should not appear as a flagged-pattern block.
if "**Signal stacking from stacked AI tells**" in signal_stacking_render:
    fail("Layer 1 / Layer 2 should not include the overall-signal-stacking block")
else:
    ok("Layer 1 / Layer 2 does not include the meta-check block")

# If signal stacking is the only flagged programmatic check, the audit is not
# all-clear: the meta-check stays suppressed as a row/block, but survives in
# the verdict token.
signal_stacking_only_results = [
    annotate_result({
        "text": "overall-signal-stacking",
        "passed": False,
        "evidence": "Overall signal stacking 5/4",
        "score": 5,
        "threshold": 4,
        "components": ["paragraph length uniformity"],
        "vocabulary_signal_stacking": {"points": 0, "reasons": [], "worst_generic": 0,
                                "gptzero_matches": [], "kobak_style_distinct": 0,
                                "kobak_style_density": 0.0, "kobak_style_sample": []},
    }),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid != "overall-signal-stacking"
]
signal_stacking_only_render = format_two_layer(signal_stacking_only_results, depth="balanced")

if "of 48 clear · agent reading clean · signal stacking: clear." in signal_stacking_only_render:
    fail(f"signal-stacking-only failure must not render the legacy collapsed all-clear line; got:\n{signal_stacking_only_render}")
elif "Signal stacking: triggered — 5 of 4 threshold" not in signal_stacking_only_render:
    fail(f"signal-stacking-only failure should surface as the R3 triggered line; got:\n{signal_stacking_only_render}")
elif "1 context_warning" in signal_stacking_only_render:
    fail(f"suppressed signal-stacking meta-check should not inflate visible severity counts; got:\n{signal_stacking_only_render}")
else:
    ok("signal-stacking-only failure renders as 'Signal stacking: triggered — N of M threshold (...)' without inflating severity counts")


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


# --- _action_for_check on agent-judgement contract items (U1 + U5 wiring) ---
#
# U1 added severity to every agent-judgement contract item; U5 verifies the
# same `_action_for_check` function — previously called only from Layer-1
# auto-detected blocks — resolves correctly on agent-judgement-shaped items
# now that severity is on the item record. The Action verb itself is not
# surfaced in the audit body post-R6, but downstream callers (Suggestions,
# Rewrite) consume the depth-aware action mapping; that mapping must keep
# working across both block kinds (R17).

print("\n=== _action_for_check resolves on agent-judgement items (U1 + U5) ===")

_action_for_check = _grade._action_for_check

# Strong-warning agent item at Balanced depth → "fix"; at All → "fix".
strong_agent_item = {"id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning"}
if _action_for_check(strong_agent_item, "balanced") != "fix":
    fail(f"strong_warning agent item at Balanced should map to 'fix'; got {_action_for_check(strong_agent_item, 'balanced')!r}")
else:
    ok("strong_warning agent item at Balanced → 'fix'")

if _action_for_check(strong_agent_item, "all") != "fix":
    fail(f"strong_warning agent item at All should map to 'fix'; got {_action_for_check(strong_agent_item, 'all')!r}")
else:
    ok("strong_warning agent item at All → 'fix'")

# Context-warning agent item at Balanced → "preserve_with_disclosure_or_user_decision".
context_agent_item = {"id": "structural_monotony", "status": "flagged", "severity": "context_warning"}
balanced_action = _action_for_check(context_agent_item, "balanced")
if balanced_action != "preserve_with_disclosure_or_user_decision":
    fail(f"context_warning agent item at Balanced should map to "
         f"'preserve_with_disclosure_or_user_decision'; got {balanced_action!r}")
else:
    ok("context_warning agent item at Balanced → 'preserve_with_disclosure_or_user_decision'")

if _action_for_check(context_agent_item, "all") != "fix":
    fail(f"context_warning agent item at All should map to 'fix'; got {_action_for_check(context_agent_item, 'all')!r}")
else:
    ok("context_warning agent item at All → 'fix' (depth=all upgrades every severity)")

# Same severity / depth pair must yield the same action whether the item is
# auto-detected or agent-assessed (R17). The function reads only `severity`,
# so equivalence is by construction — pin it explicitly.
auto_strong = {"id": "no-em-dashes", "status": "flagged", "severity": "strong_warning"}
agent_strong = {"id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning"}
if _action_for_check(auto_strong, "balanced") != _action_for_check(agent_strong, "balanced"):
    fail("R17 broken: same severity should resolve to same action for auto-detected and agent-assessed items")
else:
    ok("R17 holds: severity × depth → action mapping is shared across both blocks")


# --- U4 unit tests on _format_layer_1 (severity aggregation, judgement counts) ---
#
# format_two_layer's `judgement` arg is always [] off the regex contract;
# real judgement merges happen at U7's --judgement-file site. To exercise
# severity aggregation and the agent-counts column we call _format_layer_1
# directly with a synthetic visible+judgement pair.

print("\n=== _format_layer_1 — severity counts aggregate across both blocks ===")

_format_layer_1 = _grade._format_layer_1

# 1 strong-warning auto + 1 strong-warning agent → severity line "0 hard fail · 2 strong warning · 0 context warning".
synthetic_visible = [
    {"id": "no-em-dashes", "status": "flagged", "severity": "strong_warning", "category": "Style", "evidence": {"quoted_phrases": ["—"]}, "failure_modes": []},
] + [
    {"id": cid, "status": "clear", "severity": "context_warning", "category": "Style", "evidence": {}, "failure_modes": []}
    for cid in ("no-curly-quotes", "no-boldface-overuse")
]
synthetic_judgement = [
    {"id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning", "answer": "register holds without breaks", "evidence": {}},
    {"id": "structural_monotony", "status": "clear", "severity": "context_warning", "answer": "varies", "evidence": {}},
]
clear_stacking = {"triggered": False, "score": 0, "threshold": 4, "components": [], "vocabulary_points": 0}
agg_render = _format_layer_1("Audit", clear_stacking, synthetic_visible, synthetic_judgement, "balanced")

if "Auto-detected: 1 of 3 flagged · Agent-assessed: 1 of 2 flagged" not in agg_render:
    fail(f"counts line should aggregate auto + agent flagged + total counts; got:\n{agg_render}")
else:
    ok("counts line aggregates auto-detected and agent-assessed totals correctly")

if "Severity: 0 hard fail · 2 strong warning · 0 context warning" not in agg_render:
    fail(f"severity line should aggregate severities across both blocks (1 auto strong + 1 agent strong = 2 strong warning); got:\n{agg_render}")
else:
    ok("severity line aggregates severities across auto-detected and agent-assessed flagged items")


print("\n=== _format_layer_1 — empty judgement (regex-only invocation) ===")

empty_judgement_render = _format_layer_1("Audit", clear_stacking, synthetic_visible, [], "balanced")
if "Auto-detected: 1 of 3 flagged · Agent-assessed: 0 of 0 flagged" not in empty_judgement_render:
    fail(f"empty-judgement counts line should show 'Agent-assessed: 0 of 0 flagged'; got:\n{empty_judgement_render}")
else:
    ok("empty-judgement counts line shows 'Agent-assessed: 0 of 0 flagged'")

if "Severity: 0 hard fail · 1 strong warning · 0 context warning" not in empty_judgement_render:
    fail(f"empty-judgement severity line should aggregate only programmatic counts; got:\n{empty_judgement_render}")
else:
    ok("empty-judgement severity line aggregates only programmatic counts")


print("\n=== _format_layer_1 — signal stacking triggered line ===")

triggered_stacking = {"triggered": True, "score": 5, "threshold": 4,
                       "components": ["em dashes", "tonal uniformity"], "vocabulary_points": 1}
triggered_render = _format_layer_1("Audit", triggered_stacking, synthetic_visible, [], "balanced")
if "Signal stacking: triggered — 5 of 4 threshold (em dashes, tonal uniformity)" not in triggered_render:
    fail(f"R3 triggered line should render score / threshold / components; got:\n{triggered_render}")
else:
    ok("R3 triggered line renders 'Signal stacking: triggered — 5 of 4 threshold (em dashes, tonal uniformity)'")


# --- Counts line uses the visible total (meta-check excluded) ---

print("\n=== counts line auto_total excludes meta-check ===")

clear_count = len([cid for cid in ALL_CHECKS if cid != "overall-signal-stacking"])
expected_counts_line = f"Auto-detected: 0 of {clear_count} flagged · Agent-assessed: 0 of 0 flagged"
if expected_counts_line not in clear_render:
    fail(f"counts line should report visible auto_total = {clear_count}; expected {expected_counts_line!r}, got:\n{clear_render}")
else:
    ok(f"counts line auto_total = {clear_count} (overall-signal-stacking excluded)")


# --- Summary ---

if FAILURES:
    print(f"\n{FAILURES} FAILURES")
    sys.exit(1)
print("\n========================================")
print("ALL PASSED")
