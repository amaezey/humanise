#!/usr/bin/env python3
"""Tests for U6 agent-judgement rendering.

U6 retired the parallel `**Agent-judgement reading**` block. Agent-assessed
items now live in two surfaces:

- Default mode: agent-flagged items render inline in the audit body, in the
  same `<glyph> **<label>**` shape as auto-detected flagged items (R5/R7).
  Clear agent items do not appear at all.
- Full-report mode: a `**Agent-assessed patterns**` section sits below the
  audit body with the brief note + a flat 8-row coverage table (R12/R14).
  Clear items render as table rows with answer/value text in Detail; flagged
  items render as `(see above)` pointing back at the inline bullet block.

Covers:
- _judgement_label mechanical transform (unchanged)
- agent-flagged state / list / composite shapes inline in default mode (R7)
- severity glyph mirroring auto-detected (x / ! / ?) on agent-flagged items
- 8 items in registry order in the full-report agent-assessed coverage table
- composite-clear with empty watchlist renders "watchlist coverage pending"
  in the coverage Detail column
- default mode emits no `**Agent-judgement reading**` parallel block
- severity line aggregates agent + auto-detected severities (R2 / R17)
- both halves clear → full three-line summary, no agent block in default body

Run: python3 dev/evals/test_agent_judgement_render.py
"""

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("grade", ROOT / "humanise" / "scripts" / "grade.py")
_grade = importlib.util.module_from_spec(_spec)
if _spec.loader is None:
    raise RuntimeError("Could not load humanise/scripts/grade.py")
_spec.loader.exec_module(_grade)

format_two_layer = _grade.format_two_layer
_judgement_label = _grade._judgement_label
ALL_CHECKS = _grade.ALL_CHECKS
annotate_result = _grade.annotate_result

FAILURES = 0


def fail(msg):
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {msg}")


def ok(msg):
    print(f"  ok: {msg}")


def all_clear_judgement():
    """Build a clear-status judgement list covering all 8 records."""
    return [
        {"id": "structural_monotony", "status": "clear", "answer": "sections vary", "evidence": {}},
        {"id": "tonal_uniformity", "status": "clear", "answer": "register breaks at least once", "evidence": {}},
        {"id": "faux_specificity", "status": "clear", "answer": [], "evidence": {}},
        {"id": "neutrality_collapse", "status": "clear", "answer": "takes a position", "evidence": {}},
        {"id": "even_jargon_distribution", "status": "clear", "answer": "jargon clumps where the writer knows things", "evidence": {}},
        {"id": "forced_synesthesia", "status": "clear", "answer": [], "evidence": {}},
        {"id": "generic_metaphors", "status": "clear", "answer": [], "evidence": {}},
        {"id": "genre_specific", "status": "clear",
         "answer": {"genre_detected": "default", "watchlist_findings": []}, "evidence": {}},
    ]


def clean_results():
    return [annotate_result({"text": cid, "passed": True, "evidence": "clean"}) for cid in ALL_CHECKS]


def with_patched_judgement(judgement, fn):
    """Run fn() with humanise.grade.human_report monkey-patched to inject a
    judgement list into the contract. The grader's empty default would
    otherwise prevent format_two_layer from exercising the new code paths.

    Accepts the U7 `agent_judgement_items` kwarg from format_two_layer and
    discards it — the patch injects its own hard-coded judgement so the
    overlay parameter is moot here.
    """
    original = _grade.human_report

    def patched(results, agent_judgement_items=None):
        del agent_judgement_items  # patch ignores the overlay; uses its own injection.
        contract = original(results)
        contract["agent_judgement"] = judgement
        return contract

    _grade.human_report = patched
    try:
        return fn()
    finally:
        _grade.human_report = original


# --- _judgement_label transform ---

print("=== _judgement_label mechanical transform ===")
for item_id, expected in [
    ("structural_monotony", "Structural monotony"),
    ("tonal_uniformity", "Tonal uniformity"),
    ("faux_specificity", "Faux specificity"),
    ("neutrality_collapse", "Neutrality collapse"),
    ("even_jargon_distribution", "Even jargon distribution"),
    ("forced_synesthesia", "Forced synesthesia"),
    ("generic_metaphors", "Generic metaphors"),
    ("genre_specific", "Genre specific"),
]:
    actual = _judgement_label(item_id)
    if actual != expected:
        fail(f"_judgement_label({item_id!r}) → {actual!r}, expected {expected!r}")
    else:
        ok(f"{item_id} → {expected!r}")


# --- Default mode: agent-flagged items inline in audit body (R5 / R7) ---

print("\n=== default mode: agent-flagged items render inline in audit body ===")

mixed = all_clear_judgement()
mixed[0] = {
    "id": "structural_monotony", "status": "flagged", "severity": "strong_warning",
    "answer": "every section follows the same arc", "evidence": {},
}
mixed[1] = {
    "id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning",
    "answer": "register holds without breaks", "evidence": {},
}
mixed[2] = {
    "id": "faux_specificity", "status": "flagged", "severity": "strong_warning",
    "answer": [
        {"phrase": "approximately 30%", "why_unspecific": "fake-precise quantifier"},
    ],
    "evidence": {},
}

default_render = with_patched_judgement(
    mixed,
    lambda: format_two_layer(clean_results(), depth="balanced"),
)

if "**Agent-judgement reading" in default_render:
    fail(f"U6 retired the parallel **Agent-judgement reading** block; should not appear in default mode. Got:\n{default_render}")
else:
    ok("default mode does not emit the retired parallel block")

if "! **Structural monotony** — every section follows the same arc" not in default_render:
    fail(f"agent-flagged state item should render inline in audit body; got:\n{default_render}")
else:
    ok("state-flagged item renders inline in audit body (R5/R7)")

if "! **Faux specificity**\n" not in default_render:
    fail(f"agent-flagged list-item header should render inline; got:\n{default_render}")
elif '  - "approximately 30%" — fake-precise quantifier' not in default_render:
    fail(f"agent-flagged list-item sub-bullet should render inline; got:\n{default_render}")
else:
    ok("list-flagged item header + sub-bullet render inline (R5/R7)")


# --- Default mode: severity glyphs mirror auto-detected (x / ! / ?) ---

print("\n=== default mode: severity glyphs mirror auto-detected ===")

tri_severity = all_clear_judgement()
tri_severity[0] = {
    "id": "structural_monotony", "status": "flagged", "severity": "hard_fail",
    "answer": "every section follows the same arc", "evidence": {},
}
tri_severity[1] = {
    "id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning",
    "answer": "register holds without breaks", "evidence": {},
}
tri_severity[3] = {
    "id": "neutrality_collapse", "status": "flagged", "severity": "context_warning",
    "answer": "hedges its position", "evidence": {},
}
tri_render = with_patched_judgement(
    tri_severity,
    lambda: format_two_layer(clean_results(), depth="balanced"),
)
expected_glyph_lines = {
    "Structural monotony": "x",
    "Tonal uniformity": "!",
    "Neutrality collapse": "?",
}
glyph_mismatch = []
for label, glyph in expected_glyph_lines.items():
    line = next((line for line in tri_render.splitlines() if label in line), None)
    if line is None or not line.startswith(f"{glyph} **{label}**"):
        glyph_mismatch.append((label, glyph, line))
if glyph_mismatch:
    fail(f"severity-glyph mismatches in default-mode render: {glyph_mismatch}")
else:
    ok("hard_fail / strong_warning / context_warning render with x / ! / ? on agent flagged items inline")


# --- Composite-flagged in default mode: AE3 + watchlist sub-bullets ---

print("\n=== default mode: composite-flagged renders inline with sub-bullets (AE3) ===")

composite_flagged = all_clear_judgement()
composite_flagged[-1] = {
    "id": "genre_specific", "status": "flagged", "severity": "context_warning",
    "answer": {
        "genre_detected": "academic",
        "watchlist_findings": [
            {"phrase": "as we have seen", "why_flagged": "rubric echo"},
        ],
    },
    "evidence": {},
}
composite_render = with_patched_judgement(
    composite_flagged,
    lambda: format_two_layer(clean_results(), depth="balanced"),
)
expected_composite_block = (
    "? **Genre specific** — Genre detected: academic\n"
    '  - "as we have seen" — rubric echo'
)
if expected_composite_block in composite_render:
    ok("composite-flagged renders inline: `? **Genre specific** — Genre detected: academic` + sub-bullet")
else:
    fail(f"composite-flagged shape mismatch; expected:\n{expected_composite_block}\ngot:\n{composite_render}")


# --- Severity line aggregates agent + auto-detected (R2 / R17) ---

print("\n=== severity line aggregates agent severities (R2 / R17) ===")

three_agent_strong = all_clear_judgement()
three_agent_strong[0] = {
    "id": "structural_monotony", "status": "flagged", "severity": "strong_warning",
    "answer": "every section follows the same arc", "evidence": {},
}
three_agent_strong[1] = {
    "id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning",
    "answer": "register holds without breaks", "evidence": {},
}
three_agent_strong[3] = {
    "id": "neutrality_collapse", "status": "flagged", "severity": "strong_warning",
    "answer": "hedges its position", "evidence": {},
}
agg_render = with_patched_judgement(
    three_agent_strong,
    lambda: format_two_layer(clean_results(), depth="balanced"),
)
if "Auto-detected: 0 of " not in agg_render:
    fail(f"counts line should show 'Auto-detected: 0 of N flagged'; got:\n{agg_render}")
elif "Agent-assessed: 3 of 8 flagged" not in agg_render:
    fail(f"counts line should show 'Agent-assessed: 3 of 8 flagged'; got:\n{agg_render}")
elif "Severity: 0 hard fail · 3 strong warning · 0 context warning" not in agg_render:
    fail(f"severity line should aggregate the 3 agent strong_warning items; got:\n{agg_render}")
else:
    ok("agent-only-flagged: counts and severity lines aggregate agent severities (R2 / R17)")


# --- Both halves clear → full three-line summary, no agent body content ---

print("\n=== both halves clear → full three-line summary in default mode ===")

both_clear_render = with_patched_judgement(
    all_clear_judgement(),
    lambda: format_two_layer(clean_results(), depth="balanced"),
)
if not both_clear_render.startswith("Audit\n"):
    fail(f"both-clear default render should still emit the Audit header (R9, no collapse); got:\n{both_clear_render}")
elif "Auto-detected: 0 of " not in both_clear_render:
    fail(f"both-clear counts line should show 'Auto-detected: 0 of N flagged'; got:\n{both_clear_render}")
elif "Agent-assessed: 0 of 8 flagged" not in both_clear_render:
    fail(f"both-clear counts line should show 'Agent-assessed: 0 of 8 flagged'; got:\n{both_clear_render}")
elif "Severity: 0 hard fail · 0 strong warning · 0 context warning" not in both_clear_render:
    fail(f"both-clear severity line should be all-zero; got:\n{both_clear_render}")
elif "**Agent-judgement reading" in both_clear_render:
    fail(f"both-clear default render should not emit the retired parallel block; got:\n{both_clear_render}")
elif "agent reading clean" in both_clear_render:
    fail(f"both-clear default render should not carry the retired 'agent reading clean' line; got:\n{both_clear_render}")
else:
    ok("both halves clear → full three-line summary, no parallel block (R9 + U6)")


# --- Default mode: agent-flagged items NOT in their pre-U6 dash shape ---

print("\n=== default mode: pre-U6 '- Label — Flagged:' shape leaks nowhere ===")

old_shape = re.findall(r"^-\s+[^—\n]+—\s+Flagged", default_render, re.MULTILINE)
if old_shape:
    fail(f"pre-U6 dash-prefixed '- <Label> — Flagged' shape leaked: {old_shape}")
else:
    ok("pre-U6 '- <Label> — Flagged' shape no longer appears anywhere")


# --- Full-report mode: agent-assessed coverage table renders 8 rows in registry order ---

print("\n=== full-report mode: agent-assessed coverage table (R14) ===")

mixed_full = all_clear_judgement()
mixed_full[0] = {
    "id": "structural_monotony", "status": "flagged", "severity": "strong_warning",
    "answer": "every section follows the same arc", "evidence": {},
}
full_report_render = with_patched_judgement(
    mixed_full,
    lambda: format_two_layer(clean_results(), depth="balanced", mode="full_report"),
)
if "**Agent-assessed patterns** — 1 flagged of 8" not in full_report_render:
    fail(f"full-report should carry **Agent-assessed patterns** heading with count; got:\n{full_report_render}")
elif "Checks that are judged by an LLM based on reading the whole draft." not in full_report_render:
    fail(f"full-report should carry agent-assessed brief note; got:\n{full_report_render}")
else:
    ok("full-report renders **Agent-assessed patterns** heading + brief note")

# 8 items in judgement.json registry order
EXPECTED_ROW_ORDER = [
    "Structural monotony",
    "Tonal uniformity",
    "Faux specificity",
    "Neutrality collapse",
    "Even jargon distribution",
    "Forced synesthesia",
    "Generic metaphors",
    "Genre specific",
]
agent_section_start = full_report_render.find("**Agent-assessed patterns**")
agent_section = full_report_render[agent_section_start:]
positions = [agent_section.find(label) for label in EXPECTED_ROW_ORDER]
if any(p < 0 for p in positions):
    missing = [label for p, label in zip(positions, EXPECTED_ROW_ORDER) if p < 0]
    fail(f"full-report agent table missing rows: {missing}")
elif positions != sorted(positions):
    fail(f"full-report agent table rows out of registry order: positions={positions}")
else:
    ok("full-report agent-assessed table has 8 rows in judgement.json registry order")

# Flagged-row Detail column points back to inline bullets
flagged_row = next(
    (line for line in agent_section.splitlines()
     if "Structural monotony" in line and "|" in line),
    None,
)
if flagged_row is None:
    fail(f"missing Structural monotony row in agent table; got:\n{agent_section}")
elif "(see above)" not in flagged_row:
    fail(f"flagged row Detail column should be '(see above)'; got {flagged_row!r}")
elif "| Flagged |" not in flagged_row:
    fail(f"flagged row should carry result 'Flagged'; got {flagged_row!r}")
else:
    ok("flagged row Detail = '(see above)' (R15)")

# Clear-row Detail column carries the answer/value
clear_state_row = next(
    (line for line in agent_section.splitlines()
     if "Tonal uniformity" in line and "|" in line),
    None,
)
if clear_state_row is None or "register breaks at least once" not in clear_state_row:
    fail(f"clear state-row Detail should carry the answer text; got {clear_state_row!r}")
else:
    ok("clear state-row Detail carries the answer/value text (R15)")


# --- Full-report: composite-clear with empty watchlist → coverage pending in Detail ---

print("\n=== full-report mode: composite-clear with empty watchlist → 'coverage pending' ===")

pending_full = all_clear_judgement()
pending_full[-1] = {
    "id": "genre_specific", "status": "clear",
    "answer": {"genre_detected": "poetry", "watchlist_findings": []},
    "evidence": {},
}
# Force a programmatic flag to keep counts non-zero (avoids the "0 flagged of 8" branch)
pending_full[0] = {
    "id": "structural_monotony", "status": "flagged", "severity": "strong_warning",
    "answer": "every section follows the same arc", "evidence": {},
}
pending_render = with_patched_judgement(
    pending_full,
    lambda: format_two_layer(clean_results(), depth="balanced", mode="full_report"),
)
genre_row = next(
    (line for line in pending_render.splitlines()
     if "Genre specific" in line and "|" in line),
    None,
)
if genre_row is None:
    fail(f"missing Genre specific row in agent table; got:\n{pending_render}")
elif "watchlist coverage pending" not in genre_row.lower():
    fail(f"composite-clear genre row should mention watchlist coverage pending; got {genre_row!r}")
elif "Genre detected: poetry" not in genre_row:
    fail(f"composite-clear genre row should name the detected genre; got {genre_row!r}")
else:
    ok("composite-clear w/ empty watchlist → 'Genre detected: poetry; watchlist coverage pending' in Detail (R15)")


# --- Full-report: empty judgement renders a placeholder row ---

print("\n=== full-report mode: empty judgement → placeholder row ===")

empty_full = format_two_layer(clean_results(), depth="balanced", mode="full_report")
if "agent reading not provided" not in empty_full:
    fail(f"empty-judgement full-report should render placeholder Detail; got:\n{empty_full}")
elif "**Agent-assessed patterns** — 0 flagged of 0" not in empty_full:
    fail(f"empty-judgement heading should report 'flagged of 0'; got:\n{empty_full}")
else:
    ok("empty-judgement full-report renders the agent-assessed table with placeholder Detail")


# --- Summary ---

if FAILURES:
    print(f"\n{FAILURES} FAILURES")
    sys.exit(1)
print("\n========================================")
print("ALL PASSED")
