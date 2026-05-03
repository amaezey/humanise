#!/usr/bin/env python3
"""Tests for format_two_layer() — dual-mode audit renderer.

Shape (post-rework):
- `**Audit summary**` heading
- Three summary lines (counts / severity / signal stacking)
- `**Auto-detected**` mini-header
- Auto-detected flagged items, severity-descending (x ! ?), unbold names
- `**Agent-assessed**` mini-header
- Agent-assessed flagged items, severity-descending, unbold names
- (full-report only) brief notes + coverage tables under each mini-header
- `**Next steps**` heading + prompt

Em dashes are forbidden in the audit format itself (the skill flags em
dash overuse; using them in the audit format would be hypocritical).

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


# --- Default mode: zero-flag draft renders the full shape (R9) ---

print("=== default mode: zero-flag draft renders full shape ===")

clear_render = format_two_layer(all_clear_results(), depth="balanced")
visible_total = len([cid for cid in ALL_CHECKS if cid != "overall-signal-stacking"])

if not clear_render.startswith("**Audit summary**"):
    fail(f"audit body should open with bold '**Audit summary**'; got:\n{clear_render[:200]}")
else:
    ok("audit body opens with bold '**Audit summary**'")

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

# Mini-headers always render even with zero flags (R9 — no all-clear collapse).
if "**Auto-detected**" not in clear_render:
    fail(f"default mode should always render the **Auto-detected** mini-header; got:\n{clear_render}")
else:
    ok("default mode renders the **Auto-detected** mini-header even with zero flags")

if "**Agent-assessed**" not in clear_render:
    fail(f"default mode should always render the **Agent-assessed** mini-header; got:\n{clear_render}")
else:
    ok("default mode renders the **Agent-assessed** mini-header even with zero flags")

# Em-dash purge — the audit format itself cannot contain em dashes.
audit_only = clear_render.split("**Next steps**", 1)[0]
if "—" in audit_only:
    fail(f"audit format must be em-dash-free (em dashes are flagged as AI tells); got:\n{audit_only}")
else:
    ok("audit format is em-dash-free")


# --- Default mode: trailing **Next steps** + prompt ---

print("\n=== default mode: trailing **Next steps** + prompt ===")

if "**Next steps**" not in clear_render:
    fail(f"default mode should emit a `**Next steps**` heading; got:\n{clear_render}")
elif "Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?" not in clear_render:
    fail(f"default mode should carry the next-step prompt verbatim; got:\n{clear_render}")
elif not clear_render.rstrip().endswith("?"):
    fail(f"default mode should end with the next-step question; got:\n{clear_render}")
else:
    ok("default mode emits **Next steps** + prompt and ends with a question")


# --- Default mode: flagged item shape (unbold name, colon separator) ---

print("\n=== default mode: flagged block shape ===")

exercised_ids = {"no-collaborative-artifacts", "no-em-dashes"}
mixed_results = [
    flag("no-collaborative-artifacts", evidence_phrases=["I'll generate the report for you"]),
    flag("no-em-dashes", evidence_phrases=["EMDASHTOKEN"]),
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
    (line for line in mixed_render.splitlines() if "Em dashes" in line and not line.startswith("**")),
    None,
)
if em_dash_block is None:
    fail(f"default render missing Em dashes block; got:\n{mixed_render}")
elif em_dash_block != '! Em dashes: "EMDASHTOKEN"':
    fail(f"Em dashes block should render exactly '! Em dashes: \"EMDASHTOKEN\"' (unbold name, colon, no Action); got {em_dash_block!r}")
else:
    ok('Em dashes block renders as `! Em dashes: "EMDASHTOKEN"` (unbold name, colon, no Action)')

audit_body = mixed_render.split("**Next steps**", 1)[0]
if "Action:" in audit_body:
    fail(f"audit body should not carry any 'Action:' clause; got:\n{audit_body}")
else:
    ok("audit body carries no 'Action:' clause")


# --- Severity glyphs across tiers ---

print("\n=== severity glyphs ===")

expected_glyphs = {
    "Em dashes": "!",
    "Assistant residue": "x",
}
for label, glyph in expected_glyphs.items():
    block = next(
        (line for line in mixed_render.splitlines() if label in line and not line.startswith("**")),
        None,
    )
    if block is None:
        fail(f"default render missing block for {label!r}; got:\n{mixed_render}")
    elif not block.startswith(f"{glyph} {label}"):
        fail(f"{label!r} block should use glyph {glyph!r} and unbold name; got {block!r}")
    else:
        ok(f"{label!r} renders with glyph {glyph!r} and unbold name")


# --- Severity-descending sort within each block (x > ! > ?) ---

print("\n=== severity-descending sort within each block ===")

# Build a multi-severity case: 1 hard_fail, 2 strong_warning, 2 context_warning,
# all auto-detected. Confirm they render in x ! ! ? ? order.
multi_severity_ids = ["no-collaborative-artifacts", "no-em-dashes", "no-filler-phrases", "no-curly-quotes", "no-staccato-sequences"]
multi_severity_results = [
    flag(cid, evidence_phrases=["fragment"])
    for cid in multi_severity_ids
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid not in multi_severity_ids
]
multi_render = format_two_layer(multi_severity_results, depth="balanced")
auto_section_lines = []
in_auto = False
for line in multi_render.splitlines():
    if line == "**Auto-detected**":
        in_auto = True
        continue
    if line.startswith("**") and in_auto:
        break
    if in_auto and line and (line[0] in "x!?"):
        auto_section_lines.append(line[0])

# Expected glyph order: x first (hard_fail), then ! (strong_warning), then ? (context_warning)
expected_order = sorted(auto_section_lines, key=lambda g: {"x": 0, "!": 1, "?": 2}[g])
if auto_section_lines != expected_order:
    fail(f"flagged items should render severity-descending; got order {auto_section_lines!r}, expected {expected_order!r}")
else:
    ok(f"flagged items render severity-descending: {' '.join(auto_section_lines)}")


# --- Three-line summary block (R1, R2, R3) ---

print("\n=== three-line summary block ===")

audit_body_lines = [line for line in audit_body.splitlines() if line]
if len(audit_body_lines) < 4 or audit_body_lines[0] != "**Audit summary**":
    fail(f"audit body should open with '**Audit summary**' heading; got {audit_body_lines[:4]!r}")
elif not audit_body_lines[1].startswith("Auto-detected:"):
    fail(f"audit body second line should be the R1 counts line; got {audit_body_lines[1]!r}")
elif not audit_body_lines[2].startswith("Severity:"):
    fail(f"audit body third line should be the R2 severity line; got {audit_body_lines[2]!r}")
elif not audit_body_lines[3].startswith("Signal stacking"):
    fail(f"audit body fourth line should be the R3 signal-stacking line; got {audit_body_lines[3]!r}")
else:
    ok("audit body opens with bold heading + counts/severity/signal-stacking summary")

if "Signal stacking: clear (weaker AI signals are not accumulating)" not in mixed_render:
    fail(f"R3 signal-stacking clear line missing; got:\n{mixed_render}")
else:
    ok("R3 signal-stacking clear line renders canonical phrasing")


# --- Full-report mode: mini-headers + brief notes + 4-column coverage tables ---

print("\n=== full-report mode: mini-headers + coverage tables ===")

full_render = format_two_layer(mixed_results, depth="balanced", mode="full_report")

if "**Auto-detected**" not in full_render:
    fail(f"full-report should carry the **Auto-detected** mini-header; got:\n{full_render[:600]}")
else:
    ok("full-report carries **Auto-detected** mini-header")

if "Checks the script runs against the text directly." not in full_render:
    fail(f"full-report should carry auto-detected brief note; got:\n{full_render[:600]}")
else:
    ok("full-report carries auto-detected brief note")

if "**Agent-assessed**" not in full_render:
    fail(f"full-report should carry the **Agent-assessed** mini-header; got:\n{full_render[:1200]}")
else:
    ok("full-report carries **Agent-assessed** mini-header")

if "Checks that are judged by an LLM based on reading the whole draft." not in full_render:
    fail(f"full-report should carry agent-assessed brief note; got:\n{full_render[:1200]}")
else:
    ok("full-report carries agent-assessed brief note")

if "| Pattern | Severity | Result | Detail |" not in full_render:
    fail(f"full-report sub-table header should be 'Pattern | Severity | Result | Detail'; got:\n{full_render[:1200]}")
else:
    ok("full-report carries the 4-column sub-table header")

if "| --- | --- | --- | --- |" not in full_render:
    fail(f"full-report sub-table separator should be 4-column; got:\n{full_render[:1200]}")
else:
    ok("full-report sub-table separator is 4-column")

# Action column dropped.
auto_section = full_render.split("**Auto-detected**", 1)[1].split("**Agent-assessed**", 1)[0]
if "| Pattern | Result | Action |" in auto_section or "| Action |" in auto_section:
    fail(f"full-report auto-detected section should not include the Action column; got:\n{auto_section[:600]}")
else:
    ok("full-report auto-detected section does not carry the Action column")

em_dash_row = next(
    (line for line in auto_section.splitlines() if "Em dashes" in line and "|" in line),
    None,
)
if em_dash_row is None:
    fail(f"full-report missing Em dashes row; got:\n{auto_section[:600]}")
elif "| strong warning |" not in em_dash_row:
    fail(f"Em dashes row should carry severity 'strong warning'; got {em_dash_row!r}")
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


# --- Full-report mode: trailing **Next steps** + mode-specific prompt ---

print("\n=== full-report mode: prompt drops 'full coverage report' ===")

full_report_prompt = "Want suggestions for edits, a full rewrite, or to save this audit as a file?"
default_prompt = "Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?"

if "**Next steps**" not in full_render:
    fail(f"full-report mode should emit a `**Next steps**` heading; got tail:\n{full_render[-400:]}")
elif full_report_prompt not in full_render:
    fail(f"full-report mode should carry the mode-specific next-step prompt verbatim; got tail:\n{full_render[-400:]}")
elif default_prompt in full_render:
    fail("full-report mode must NOT carry the default-mode prompt offering 'the full coverage report' (writer just read it)")
elif not full_render.rstrip().endswith("?"):
    fail(f"full-report mode should end with the next-step question; got tail:\n{full_render[-400:]}")
else:
    ok("full-report mode emits **Next steps** + mode-specific prompt without the 'full coverage report' option")


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
elif "—" in collapse_line:
    fail(f"category-collapse line must be em-dash-free; got {collapse_line!r}")
else:
    ok(f"{COLLAPSE_CATEGORY!r} category collapses to em-dash-free one-liner: {collapse_line!r}")


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
    flag("no-em-dashes", evidence_phrases=["EMDASHTOKEN"]),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid not in {"overall-signal-stacking", "no-em-dashes"}
]
signal_stacking_render = format_two_layer(signal_stacking_flagged_results, depth="balanced")

if "Signal stacking triggered: 5 of 4 threshold" not in signal_stacking_render:
    fail(f"R3 line should report 'Signal stacking triggered: N of M threshold (...)' when meta-check is flagged; got:\n{signal_stacking_render[:600]}")
else:
    ok("R3 stand-alone line carries 'Signal stacking triggered: 5 of 4 threshold (...)'")

if "**Signal stacking**" in signal_stacking_render:
    fail("default render should not surface the suppressed Signal stacking category heading")
else:
    ok("default render does not include the suppressed category")


# --- Phrase cap (3 + overflow in default; all in full-report) ---

print("\n=== phrase cap: default 3+overflow, full-report all ===")

phrases = [f"phrase{i}" for i in range(LAYER_1_PHRASE_CAP + 4)]
many_phrase_results = [
    flag("no-triad-density", evidence_phrases=phrases),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS
    if cid != "no-triad-density"
]
many_render_default = format_two_layer(many_phrase_results, depth="balanced")
many_audit_body = many_render_default.split("**Next steps**", 1)[0]

triad_block = next(
    (line for line in many_audit_body.splitlines() if "Triad density" in line and not line.startswith("**")),
    None,
)
if triad_block is None:
    fail(f"default render missing Triad density block; got:\n{many_audit_body}")
else:
    quote_count = triad_block.count('"phrase')
    if quote_count != LAYER_1_PHRASE_CAP:
        fail(f"default mode should cap at {LAYER_1_PHRASE_CAP} phrases; counted {quote_count} in {triad_block!r}")
    elif f"(+{len(phrases) - LAYER_1_PHRASE_CAP} more)" not in triad_block:
        fail(f"default mode should append (+N more) suffix; got {triad_block!r}")
    else:
        ok(f"default mode caps phrases at {LAYER_1_PHRASE_CAP} and appends overflow indicator")

# Full-report mode renders all phrases, no overflow.
many_render_full = format_two_layer(many_phrase_results, depth="balanced", mode="full_report")
many_full_body = many_render_full.split("**Auto-detected**", 1)[1]
triad_block_full = next(
    (line for line in many_full_body.splitlines() if "Triad density" in line and not line.startswith("**") and "|" not in line),
    None,
)
if triad_block_full is None:
    fail(f"full-report missing Triad density block; got:\n{many_full_body[:1000]}")
else:
    quote_count = triad_block_full.count('"phrase')
    if quote_count != len(phrases):
        fail(f"full-report should render all {len(phrases)} phrases; counted {quote_count}")
    elif "more)" in triad_block_full:
        fail(f"full-report should not append (+N more); got {triad_block_full!r}")
    else:
        ok(f"full-report renders all {len(phrases)} phrases with no overflow indicator")


# --- _action_for_check on agent-judgement contract items (R17) ---

print("\n=== _action_for_check resolves on agent-judgement items (R17) ===")

_action_for_check = _grade._action_for_check

strong_agent_item = {"id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning"}
if _action_for_check(strong_agent_item, "balanced") != "fix":
    fail(f"strong_warning agent item at Balanced should map to 'fix'; got {_action_for_check(strong_agent_item, 'balanced')!r}")
else:
    ok("strong_warning agent item at Balanced → 'fix'")

context_agent_item = {"id": "structural_monotony", "status": "flagged", "severity": "context_warning"}
balanced_action = _action_for_check(context_agent_item, "balanced")
if balanced_action != "preserve_with_disclosure_or_user_decision":
    fail(f"context_warning agent item at Balanced should map to "
         f"'preserve_with_disclosure_or_user_decision'; got {balanced_action!r}")
else:
    ok("context_warning agent item at Balanced → 'preserve_with_disclosure_or_user_decision'")


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
