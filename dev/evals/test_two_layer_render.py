#!/usr/bin/env python3
"""Tests for format_two_layer() — dual-mode audit renderer.

U6 split the audit into two modes:

- Default mode (R5): heading + counts/severity/signal-stacking summary
  (R1–R3) + flagged items inline from both blocks (R6/R7) + next-step
  prompt. No coverage tables. No parallel `**Agent-judgement reading**`
  section.
- Full-report mode (R11–R14): same default content + two per-block sections
  (`**Auto-detected patterns**`, `**Agent-assessed patterns**`) with brief
  notes and coverage tables, then the next-step prompt.

Covers:
- Zero-flag draft renders the full three-line summary in default mode (R9)
- R6: flagged items have no Action clause
- Severity glyphs (x / ! / ?)
- Three-line summary block (R1, R2, R3)
- Full-report sub-table shape (R15, R18 — 4-column, no Action)
- Full-report category ordering (CATEGORY_ORDER)
- overall-signal-stacking suppression (R3 stand-alone line, no Layer-2 row)
- Phrase cap with overflow indicator
- _action_for_check resolves on agent-judgement-shaped items (U1 + U5)
- _format_audit_body severity aggregation, empty judgement, triggered stacking
- Counts line uses visible total (meta-check excluded)
- Trailing **Next step** + R8 prompt (U6)

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
    return [
        annotate_result({"text": cid, "passed": True, "evidence": "clean"})
        for cid in ALL_CHECKS
    ]


def flag(cid, evidence_phrases=None, evidence_text="flagged here"):
    payload = {
        "text": cid,
        "passed": False,
        "evidence": evidence_text,
    }
    if evidence_phrases is not None:
        payload["matches"] = list(evidence_phrases)
    return annotate_result(payload)


# --- Default mode: zero-flag draft renders the full three-line summary (R9) ---

print("=== default mode: zero-flag draft renders three-line summary ===")

clear_render = format_two_layer(all_clear_results(), depth="balanced")
visible_total = len([cid for cid in ALL_CHECKS if cid != "overall-signal-stacking"])

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

if "of 48 clear · agent reading clean · signal stacking: clear." in clear_render:
    fail(f"legacy collapsed all-clear single-line shape should be retired; got:\n{clear_render}")
else:
    ok("legacy collapsed all-clear single-line shape is retired (R9)")

# Default mode has no per-block sections and no agent-judgement parallel block.
if "**Auto-detected patterns**" in clear_render:
    fail("default mode should not include the **Auto-detected patterns** section heading")
else:
    ok("default mode does not include **Auto-detected patterns** section heading")

if "**Agent-judgement reading" in clear_render:
    fail("U6 retired the **Agent-judgement reading** parallel block; should not appear")
else:
    ok("default mode does not emit the retired **Agent-judgement reading** block")


# --- Default mode: trailing Next step + R8 prompt ---

print("\n=== default mode: trailing **Next step** + R8 prompt ===")

if "**Next step**" not in clear_render:
    fail(f"default mode should emit a `**Next step**` heading; got:\n{clear_render}")
elif "Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?" not in clear_render:
    fail(f"default mode should carry the R8 next-step prompt verbatim; got:\n{clear_render}")
elif not clear_render.rstrip().endswith("?"):
    fail(f"default mode should end with the next-step question; got:\n{clear_render}")
else:
    ok("default mode emits **Next step** + R8 prompt and ends with a question")


# --- Default mode: flagged Layer-1 block shape (R6 — no Action) ---

print("\n=== default mode: flagged block shape (R6) ===")

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

for forbidden in ("What it looks for:", "What happened here:", "Why this matters:"):
    if forbidden in mixed_render:
        fail(f"default render should not include {forbidden!r}; found in:\n{mixed_render}")
        break
else:
    ok("default render carries no description / why-this-matters labels")

em_dash_block = next(
    (line for line in mixed_render.splitlines() if "Em dashes" in line),
    None,
)
if em_dash_block is None:
    fail(f"default render missing Em dashes block; got:\n{mixed_render}")
elif em_dash_block != '! **Em dashes** — "—"':
    fail(f"Em dashes block should render exactly '! **Em dashes** — \"—\"'; got {em_dash_block!r}")
else:
    ok('Em dashes block renders as `! **Em dashes** — "—"` (no Action clause, R6)')

# The R8 next-step prompt contains the word "rewrite", which is a substring
# match risk for "Action:" hunting; scope to the audit body only.
audit_body = mixed_render.split("**Next step**", 1)[0]
if "Action:" in audit_body:
    fail(f"audit body should not carry any 'Action:' clause post-U5 (R6); got:\n{audit_body}")
else:
    ok("audit body carries no 'Action:' clause (R6)")


# --- Severity glyphs across tiers ---

print("\n=== severity glyphs ===")

expected_glyphs = {
    "Em dashes": "!",
    "Assistant residue": "x",
}
for label, glyph in expected_glyphs.items():
    block = next((line for line in mixed_render.splitlines() if label in line), None)
    if block is None:
        fail(f"default render missing block for {label!r}; got:\n{mixed_render}")
    elif not block.startswith(f"{glyph} **{label}**"):
        fail(f"{label!r} block should use glyph {glyph!r}; got {block!r}")
    else:
        ok(f"{label!r} renders with glyph {glyph!r}")


# --- Three-line summary block (R1, R2, R3) ---

print("\n=== three-line summary block ===")

audit_body_lines = [line for line in audit_body.splitlines() if line]
if len(audit_body_lines) < 4 or audit_body_lines[0] != "Audit":
    fail(f"audit body should open with 'Audit' heading; got {audit_body_lines[:4]!r}")
elif not audit_body_lines[1].startswith("Auto-detected:"):
    fail(f"audit body second line should be the R1 counts line; got {audit_body_lines[1]!r}")
elif not audit_body_lines[2].startswith("Severity:"):
    fail(f"audit body third line should be the R2 severity line; got {audit_body_lines[2]!r}")
elif "signal stacking:" in audit_body_lines[2].lower():
    fail(f"R2 severity line should not carry the inline signal-stacking suffix; got {audit_body_lines[2]!r}")
elif not audit_body_lines[3].startswith("Signal stacking:"):
    fail(f"audit body fourth line should be the R3 signal-stacking line; got {audit_body_lines[3]!r}")
else:
    ok("audit body opens with the three-line summary block (counts / severity / signal stacking)")

if "Signal stacking: clear (weaker AI signals are not accumulating)" not in mixed_render:
    fail(f"R3 signal-stacking clear line missing; got:\n{mixed_render}")
else:
    ok("R3 signal-stacking clear line renders canonical phrasing")

if "AI-pressure looks for accumulation" in mixed_render:
    fail("Legacy multi-sentence pressure explanation should be gone")
elif "weaker AI-writing signals stacked to" in mixed_render:
    fail("Legacy short_signal_stacking_explanation prose should be gone (U4 dropped the helper)")
else:
    ok("Legacy multi-sentence signal-stacking explanation removed")


# --- Full-report mode: per-block headings + brief notes + 4-column coverage tables ---

print("\n=== full-report mode: per-block sections ===")

full_render = format_two_layer(mixed_results, depth="balanced", mode="full_report")

if "**Auto-detected patterns** — 2 flagged of " not in full_render:
    fail(f"full-report should carry **Auto-detected patterns** heading with count; got:\n{full_render[:600]}")
else:
    ok("full-report renders **Auto-detected patterns** heading with flagged count")

if "Checks the script runs against the text directly." not in full_render:
    fail(f"full-report should carry auto-detected brief note; got:\n{full_render[:600]}")
else:
    ok("full-report carries auto-detected brief note")

if "**Agent-assessed patterns** — 0 flagged of 0" not in full_render:
    fail(f"full-report should carry **Agent-assessed patterns** heading with count; got:\n{full_render[:1200]}")
else:
    ok("full-report renders **Agent-assessed patterns** heading with flagged count")

if "Checks that are judged by an LLM based on reading the whole draft." not in full_render:
    fail(f"full-report should carry agent-assessed brief note; got:\n{full_render[:1200]}")
else:
    ok("full-report carries agent-assessed brief note")

# 4-column coverage table header (R15) appears in both auto-detected sub-tables
# and the agent-assessed flat table.
if "| Pattern | Severity | Result | Detail |" not in full_render:
    fail(f"full-report sub-table header should be the U4 4-column 'Pattern | Severity | Result | Detail'; got:\n{full_render[:1200]}")
else:
    ok("full-report carries the U4 4-column sub-table header")

if "| --- | --- | --- | --- |" not in full_render:
    fail(f"full-report sub-table separator should be 4-column; got:\n{full_render[:1200]}")
else:
    ok("full-report sub-table separator is 4-column")

# Action column dropped per R18.
auto_section = full_render.split("**Auto-detected patterns**", 1)[1].split("**Agent-assessed patterns**", 1)[0]
if "| Pattern | Result | Action |" in auto_section or "| Action |" in auto_section:
    fail(f"full-report auto-detected section should not include the Action column (R18); got:\n{auto_section[:600]}")
else:
    ok("full-report auto-detected section does not carry the Action column (R18)")

# Severity column reads the renamed labels (lowercase, space-separated).
em_dash_row = next(
    (line for line in auto_section.splitlines() if "Em dashes" in line and "|" in line),
    None,
)
if em_dash_row is None:
    fail(f"full-report missing Em dashes row; got:\n{auto_section[:600]}")
elif "| strong warning |" not in em_dash_row:
    fail(f"Em dashes row should carry severity 'strong warning' (lowercase, space-separated); got {em_dash_row!r}")
elif "| Flagged |" not in em_dash_row:
    fail(f"Em dashes row should carry result 'Flagged'; got {em_dash_row!r}")
else:
    ok("full-report Em dashes row: severity + Flagged + Detail (guidance) present")


# --- Full-report mode: category ordering ---

print("\n=== full-report mode: category ordering ===")

seen_at = []
for category in CATEGORY_ORDER:
    needle = f"**{category}**"
    if needle not in auto_section:
        fail(f"full-report missing category {category!r}")
        continue
    seen_at.append((category, auto_section.index(needle)))

if seen_at == sorted(seen_at, key=lambda pair: pair[1]):
    ok("full-report categories render in CATEGORY_ORDER")
else:
    fail(f"full-report categories out of order: {[c for c, _ in seen_at]}")

if "**Signal stacking**" in full_render:
    fail("Signal stacking category heading should be suppressed (overall meta)")
else:
    ok("Signal stacking category suppressed from output")


# --- Full-report mode: trailing **Next step** + mode-specific prompt ---

print("\n=== full-report mode: trailing **Next step** + prompt drops 'full coverage report' ===")

full_report_prompt = "Want suggestions for edits, a full rewrite, or to save this audit as a file?"
default_prompt = "Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?"

if "**Next step**" not in full_render:
    fail(f"full-report mode should emit a `**Next step**` heading; got tail:\n{full_render[-400:]}")
elif full_report_prompt not in full_render:
    fail(f"full-report mode should carry the mode-specific next-step prompt verbatim; got tail:\n{full_render[-400:]}")
elif default_prompt in full_render:
    fail("full-report mode must NOT carry the default-mode prompt offering 'the full coverage report' (writer just read it)")
elif not full_render.rstrip().endswith("?"):
    fail(f"full-report mode should end with the next-step question; got tail:\n{full_render[-400:]}")
else:
    ok("full-report mode emits **Next step** + mode-specific prompt without the 'full coverage report' option")


# --- Full-report mode: clear-category collapse to one-liner ---

print("\n=== full-report mode: clear-category collapse ===")

COLLAPSE_CATEGORY = "Sensory and atmospheric"
collapse_line = next(
    (line for line in auto_section.splitlines() if line.startswith(f"**{COLLAPSE_CATEGORY}**")),
    None,
)
if collapse_line is None:
    fail(f"full-report missing {COLLAPSE_CATEGORY!r} line; got:\n{auto_section}")
elif "clear" not in collapse_line or "/" not in collapse_line:
    fail(f"{COLLAPSE_CATEGORY!r} line should collapse to N/N clear; got {collapse_line!r}")
else:
    ok(f"{COLLAPSE_CATEGORY!r} category collapses to one-liner: {collapse_line!r}")


# --- overall-signal-stacking suppression ---

print("\n=== overall-signal-stacking suppression ===")

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

if "Signal stacking: triggered — 5 of 4 threshold" not in signal_stacking_render:
    fail(f"R3 line should report 'Signal stacking: triggered — N of M threshold (...)' when meta-check is flagged; got:\n{signal_stacking_render[:600]}")
else:
    ok("R3 stand-alone line carries 'Signal stacking: triggered — 5 of 4 threshold (...)'")

if "**Signal stacking**" in signal_stacking_render:
    fail("default render should not surface the suppressed Signal stacking category heading")
else:
    ok("default render does not include the suppressed category")

if "**Signal stacking from stacked AI tells**" in signal_stacking_render:
    fail("default render should not include the overall-signal-stacking flagged block")
else:
    ok("default render does not include the meta-check flagged block")

# Signal-stacking-only failure should also work — no all-clear collapse.
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
    ok("signal-stacking-only failure renders as R3 triggered line without inflating severity counts")


# --- Phrase cap (3 + overflow) ---

print("\n=== phrase cap ===")

phrases = [f"phrase{i}" for i in range(LAYER_1_PHRASE_CAP + 4)]
many_phrase_results = [
    flag("no-triad-density", evidence_phrases=phrases),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid != "no-triad-density"
]
many_render = format_two_layer(many_phrase_results, depth="balanced")
many_audit_body = many_render.split("**Next step**", 1)[0]

triad_block = next(
    (line for line in many_audit_body.splitlines() if "Triad density" in line),
    None,
)
if triad_block is None:
    fail(f"default render missing Triad density block; got:\n{many_audit_body}")
else:
    quote_count = triad_block.count('"phrase')
    if quote_count != LAYER_1_PHRASE_CAP:
        fail(f"audit body should cap at {LAYER_1_PHRASE_CAP} phrases; counted {quote_count} in {triad_block!r}")
    elif f"(+{len(phrases) - LAYER_1_PHRASE_CAP} more)" not in triad_block:
        fail(f"audit body should append (+N more) suffix; got {triad_block!r}")
    else:
        ok(f"audit body caps phrases at {LAYER_1_PHRASE_CAP} and appends overflow indicator")


# --- _action_for_check on agent-judgement contract items (U1 + U5 wiring, R17) ---

print("\n=== _action_for_check resolves on agent-judgement items (R17) ===")

_action_for_check = _grade._action_for_check

strong_agent_item = {"id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning"}
if _action_for_check(strong_agent_item, "balanced") != "fix":
    fail(f"strong_warning agent item at Balanced should map to 'fix'; got {_action_for_check(strong_agent_item, 'balanced')!r}")
else:
    ok("strong_warning agent item at Balanced → 'fix'")

if _action_for_check(strong_agent_item, "all") != "fix":
    fail(f"strong_warning agent item at All should map to 'fix'; got {_action_for_check(strong_agent_item, 'all')!r}")
else:
    ok("strong_warning agent item at All → 'fix'")

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

auto_strong = {"id": "no-em-dashes", "status": "flagged", "severity": "strong_warning"}
agent_strong = {"id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning"}
if _action_for_check(auto_strong, "balanced") != _action_for_check(agent_strong, "balanced"):
    fail("R17 broken: same severity should resolve to same action for auto-detected and agent-assessed items")
else:
    ok("R17 holds: severity × depth → action mapping is shared across both blocks")


# --- _format_audit_body: severity aggregation, judgement counts, triggered stacking ---

print("\n=== _format_audit_body — severity counts aggregate across both blocks ===")

_format_audit_body = _grade._format_audit_body

synthetic_visible = [
    {"id": "no-em-dashes", "status": "flagged", "severity": "strong_warning",
     "category": "Style", "evidence": {"quoted_phrases": ["—"]}, "failure_modes": []},
] + [
    {"id": cid, "status": "clear", "severity": "context_warning",
     "category": "Style", "evidence": {}, "failure_modes": []}
    for cid in ("no-curly-quotes", "no-boldface-overuse")
]
synthetic_judgement = [
    {"id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning",
     "answer": "register holds without breaks", "evidence": {}},
    {"id": "structural_monotony", "status": "clear", "severity": "context_warning",
     "answer": "varies", "evidence": {}},
]
clear_stacking = {"triggered": False, "score": 0, "threshold": 4, "components": [], "vocabulary_points": 0}
agg_render = _format_audit_body("Audit", clear_stacking, synthetic_visible, synthetic_judgement, "balanced")

if "Auto-detected: 1 of 3 flagged · Agent-assessed: 1 of 2 flagged" not in agg_render:
    fail(f"counts line should aggregate auto + agent flagged + total counts; got:\n{agg_render}")
else:
    ok("counts line aggregates auto-detected and agent-assessed totals correctly")

if "Severity: 0 hard fail · 2 strong warning · 0 context warning" not in agg_render:
    fail(f"severity line should aggregate severities across both blocks; got:\n{agg_render}")
else:
    ok("severity line aggregates severities across auto-detected and agent-assessed flagged items")

# The agent-flagged item should render inline in the audit body (R5).
if "! **Tonal uniformity** — register holds without breaks" not in agg_render:
    fail(f"audit body should carry the agent-flagged state item inline; got:\n{agg_render}")
else:
    ok("agent-flagged state item renders inline in audit body (R5)")


print("\n=== _format_audit_body — empty judgement (regex-only invocation) ===")

empty_judgement_render = _format_audit_body("Audit", clear_stacking, synthetic_visible, [], "balanced")
if "Auto-detected: 1 of 3 flagged · Agent-assessed: 0 of 0 flagged" not in empty_judgement_render:
    fail(f"empty-judgement counts line should show 'Agent-assessed: 0 of 0 flagged'; got:\n{empty_judgement_render}")
else:
    ok("empty-judgement counts line shows 'Agent-assessed: 0 of 0 flagged'")

if "Severity: 0 hard fail · 1 strong warning · 0 context warning" not in empty_judgement_render:
    fail(f"empty-judgement severity line should aggregate only programmatic counts; got:\n{empty_judgement_render}")
else:
    ok("empty-judgement severity line aggregates only programmatic counts")


print("\n=== _format_audit_body — signal-stacking triggered line ===")

triggered_stacking = {"triggered": True, "score": 5, "threshold": 4,
                      "components": ["em dashes", "tonal uniformity"], "vocabulary_points": 1}
triggered_render = _format_audit_body("Audit", triggered_stacking, synthetic_visible, [], "balanced")
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


# --- Mode validation ---

print("\n=== mode parameter validation ===")

try:
    format_two_layer(all_clear_results(), mode="bogus")
except ValueError as e:
    if "mode" in str(e):
        ok("invalid mode raises ValueError naming the parameter")
    else:
        fail(f"ValueError raised but message unhelpful: {e}")
else:
    fail("format_two_layer should raise ValueError on invalid mode")


# --- Summary ---

if FAILURES:
    print(f"\n{FAILURES} FAILURES")
    sys.exit(1)
print("\n========================================")
print("ALL PASSED")
