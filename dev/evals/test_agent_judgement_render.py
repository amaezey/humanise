#!/usr/bin/env python3
"""Tests for format_agent_judgement() — Phase 3 agent-judgement parallel block (U12).

Covers all nine plan-spec scenarios:
- 8 items render in judgement.json registry order
- polymorphic genre slot renders genre + findings
- status binary (no severity column, no `mixed` state, no severity glyphs)
- all 8 clear → single 'agent reading clean' line within block
- only genre slot fires → single block with genre finding (no programmatic block)
- list-shape item with zero entries → Clear, not empty list
- detected genre with empty watchlist → 'Watchlist coverage pending.'
- agent-judgement findings do NOT inflate verdict-line severity counts
- R8 single-line response takes precedence when both blocks clear

Run: python3 dev/evals/test_agent_judgement_render.py
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

format_agent_judgement = _grade.format_agent_judgement
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
    """
    original = _grade.human_report

    def patched(results):
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


# --- 8 items render in registry order ---

print("\n=== 8 items in registry order ===")

# Build in REVERSE order so the sort is what gets verified.
mixed = [
    {"id": "genre_specific", "status": "clear",
     "answer": {"genre_detected": "default", "watchlist_findings": []}, "evidence": {}},
    {"id": "generic_metaphors", "status": "clear", "answer": [], "evidence": {}},
    {"id": "forced_synesthesia", "status": "clear", "answer": [], "evidence": {}},
    {"id": "even_jargon_distribution", "status": "flagged",
     "answer": "jargon spreads uniformly across the text", "evidence": {}},
    {"id": "neutrality_collapse", "status": "clear", "answer": "takes a position", "evidence": {}},
    {"id": "faux_specificity", "status": "clear", "answer": [], "evidence": {}},
    {"id": "tonal_uniformity", "status": "flagged",
     "answer": "register holds without breaks", "evidence": {}},
    {"id": "structural_monotony", "status": "flagged",
     "answer": "every section follows the same arc", "evidence": {}},
]

mixed_render = format_agent_judgement(mixed)

EXPECTED_ORDER = [
    "Structural monotony",
    "Tonal uniformity",
    "Faux specificity",
    "Neutrality collapse",
    "Even jargon distribution",
    "Forced synesthesia",
    "Generic metaphors",
    "Genre specific",
]
positions = [mixed_render.find(label) for label in EXPECTED_ORDER]
if any(p < 0 for p in positions):
    missing = [label for p, label in zip(positions, EXPECTED_ORDER) if p < 0]
    fail(f"missing labels in render: {missing}\n--- render ---\n{mixed_render}")
elif positions != sorted(positions):
    fail(f"items not in registry order; positions={positions}\n--- render ---\n{mixed_render}")
else:
    ok("8 items render in judgement.json registry order")


# --- header carries flagged-of-total count ---

print("\n=== header shape ===")

if "**Agent-judgement reading — 3 flagged of 8**" not in mixed_render:
    fail(f"expected '**Agent-judgement reading — 3 flagged of 8**'; got first line: "
         f"{mixed_render.splitlines()[0]!r}")
else:
    ok("header carries flagged-of-total count")


# --- U5 (R7): flagged items use glyph + bold-name shape; clear items don't ---

print("\n=== flagged items use glyph + bold-name shape (R7) ===")

# `mixed` is a substring of "mixed_intentional" (old token, removed in U12 schema rewrite)
# and shouldn't appear standalone. The mechanical transform of any judgement id
# also doesn't produce 'mixed', so any occurrence is a regression.
if " mixed " in f" {mixed_render.lower()} " or "mixed_intentional" in mixed_render:
    fail("agent block should not include `mixed` state vocabulary")
else:
    ok("no 'mixed' state vocabulary in render")

# Pre-U5 invariant ("no severity glyphs anywhere") is retired by U5. Flagged
# items now lead with `! `, `x `, or `? `; clear items keep the dash-prefixed
# `- <Label> — <Status>[: ...]` shape so the two are visually distinguishable.
flagged_lines = [line for line in mixed_render.splitlines() if line[:2] in {"x ", "! ", "? "}]
clear_lines = [
    line for line in mixed_render.splitlines()
    if line.startswith("- ") and " — Clear" in line
]
if not flagged_lines:
    fail(f"flagged items should lead with severity glyph; got:\n{mixed_render}")
elif not clear_lines:
    fail(f"clear items should still use the dash-prefixed shape; got:\n{mixed_render}")
else:
    ok(f"flagged items use glyph leader ({len(flagged_lines)} lines) and clear items keep dash shape ({len(clear_lines)} lines)")

# The pre-U5 `- <Label> — Flagged[: ...]` shape on flagged items must be gone.
import re as _re_check
old_shape = _re_check.findall(r"^- [^—\n]+ — Flagged", mixed_render, _re_check.MULTILINE)
if old_shape:
    fail(f"pre-U5 '- <Label> — Flagged' shape leaked: {old_shape}")
else:
    ok("pre-U5 '- <Label> — Flagged' shape no longer appears on flagged items")


# --- U5 R7 happy paths: state, list, composite flagged shapes ---

print("\n=== U5 R7: state-flagged renders `! **Label** — <value>` ===")

state_flagged = all_clear_judgement()
state_flagged[1] = {
    "id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning",
    "answer": "register holds without breaks", "evidence": {},
}
state_render = format_agent_judgement(state_flagged)
state_lines = [line for line in state_render.splitlines() if "Tonal uniformity" in line]
if state_lines and state_lines[0] == "! **Tonal uniformity** — register holds without breaks":
    ok("state-flagged renders `! **Tonal uniformity** — register holds without breaks`")
else:
    fail(f"state-flagged shape mismatch; got: {state_lines[:1]!r}")


print("\n=== U5 R7: list-flagged renders header + sub-bullets per finding ===")

list_flagged = all_clear_judgement()
list_flagged[2] = {
    "id": "faux_specificity", "status": "flagged", "severity": "strong_warning",
    "answer": [
        # judgement.json's faux_specificity schema uses `why_unspecific`; the
        # renderer looks up the schema's `why_*` field name dynamically.
        {"phrase": "approximately 30%", "why_unspecific": "fake-precise quantifier"},
        {"phrase": "research suggests", "why_unspecific": "phantom citation pattern"},
    ],
    "evidence": {},
}
list_render = format_agent_judgement(list_flagged)
expected_list_block = (
    "! **Faux specificity**\n"
    '  - "approximately 30%" — fake-precise quantifier\n'
    '  - "research suggests" — phantom citation pattern'
)
if expected_list_block in list_render:
    ok("list-flagged with 2 findings → header + 2 sub-bullets in the R7 shape (covers AE3)")
else:
    fail(f"list-flagged shape mismatch; expected:\n{expected_list_block}\ngot:\n{list_render}")


print("\n=== U5 R7: composite-flagged renders `! **Label** — Genre detected: <genre>` + sub-bullets ===")

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
composite_render = format_agent_judgement(composite_flagged)
expected_composite_block = (
    "? **Genre specific** — Genre detected: academic\n"
    '  - "as we have seen" — rubric echo'
)
if expected_composite_block in composite_render:
    ok("composite-flagged renders `? **Genre specific** — Genre detected: academic` + sub-bullet")
else:
    fail(f"composite-flagged shape mismatch; expected:\n{expected_composite_block}\ngot:\n{composite_render}")


# --- U5 (R7): composite-flagged with severity-tier glyph mapping ---

print("\n=== U5 R7: severity glyphs mirror auto-detected (x / ! / ?) ===")

# All three severities exercised in one render — confirms the agent-judgement
# block uses the same severity → glyph mapping as Layer-1 auto-detected.
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
tri_render = format_agent_judgement(tri_severity)
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
    fail(f"severity-glyph mismatches: {glyph_mismatch}")
else:
    ok("hard_fail / strong_warning / context_warning render with x / ! / ? on agent flagged items")


# --- all clear → single 'agent reading clean' line ---

print("\n=== all clear → clean line ===")

clear_render = format_agent_judgement(all_clear_judgement())
clear_lines = clear_render.splitlines()
if len(clear_lines) != 2:
    fail(f"all-clear-within-block should be 2 lines (header + clean line); "
         f"got {len(clear_lines)}: {clear_render!r}")
elif clear_lines[1] != "agent reading clean":
    fail(f"clean body should read 'agent reading clean'; got {clear_lines[1]!r}")
elif "Flagged" in clear_render:
    fail(f"all-clear render should not say 'Flagged'; got: {clear_render!r}")
else:
    ok("all-clear → '**Agent-judgement reading**' + 'agent reading clean'")


# --- only genre slot fires → both blocks (R9, no collapse, U4) ---

print("\n=== only genre slot fires → both blocks (no collapse) ===")

only_genre_judgement = all_clear_judgement()
only_genre_judgement[-1] = {
    "id": "genre_specific",
    "status": "flagged",
    "severity": "context_warning",
    "answer": {
        "genre_detected": "academic",
        "watchlist_findings": [{"phrase": "as we have seen", "why_flagged": "rubric echo"}],
    },
    "evidence": {},
}

genre_only_render = with_patched_judgement(
    only_genre_judgement,
    lambda: format_two_layer(clean_results(), depth="balanced"),
)

# Post-U4 (R9): the programmatic block is always present, but its counts
# show zero auto-detected flagged. The agent block still renders the genre.
if not genre_only_render.startswith("Audit\n"):
    fail(f"only-genre case should still emit the programmatic Audit header (R9, no collapse); got:\n{genre_only_render}")
elif "Auto-detected: 0 of " not in genre_only_render:
    fail(f"only-genre case counts line should show 'Auto-detected: 0 of N flagged'; got:\n{genre_only_render}")
elif "**Agent-judgement reading" not in genre_only_render:
    fail(f"only-genre case should render agent block; got:\n{genre_only_render}")
elif "Genre detected: academic" not in genre_only_render:
    fail(f"genre slot should render detected genre; got:\n{genre_only_render}")
elif "as we have seen" not in genre_only_render:
    fail(f"genre slot should render watchlist findings; got:\n{genre_only_render}")
else:
    ok("only-genre-flagged → programmatic three-line summary + agent block (no collapse)")


# --- list-shape item with zero entries → Clear, not empty list ---

print("\n=== list with zero entries → Clear ===")

# faux_specificity has list-shape; with empty answer + status=clear, render Clear.
# Force at least one item flagged so we don't hit the all-clear single-line path.
items_with_flagged_anchor = all_clear_judgement()
items_with_flagged_anchor[0] = {
    "id": "structural_monotony",
    "status": "flagged",
    "answer": "every section follows the same arc",
    "evidence": {},
}
empty_list_render = format_agent_judgement(items_with_flagged_anchor)

faux_lines = [line for line in empty_list_render.splitlines() if "Faux specificity" in line]
if not faux_lines:
    fail(f"missing 'Faux specificity' line; got:\n{empty_list_render}")
elif faux_lines[0] != "- Faux specificity — Clear":
    fail(f"empty list-shape should render '- Faux specificity — Clear'; got: {faux_lines[0]!r}")
else:
    ok("list-shape item with zero entries renders '- Faux specificity — Clear'")


# --- detected genre with empty watchlist → 'Watchlist coverage pending.' ---

print("\n=== empty watchlist → coverage pending ===")

# poetry's sub_records.watchlist is empty in judgement.json. Set genre_detected=poetry,
# findings=[]. Force at least one other item flagged to bypass all-clear path.
pending_items = all_clear_judgement()
pending_items[0] = {
    "id": "structural_monotony",
    "status": "flagged",
    "answer": "every section follows the same arc",
    "evidence": {},
}
pending_items[-1] = {
    "id": "genre_specific",
    "status": "clear",
    "answer": {"genre_detected": "poetry", "watchlist_findings": []},
    "evidence": {},
}
pending_render = format_agent_judgement(pending_items)

if "Watchlist coverage pending" not in pending_render:
    fail(f"empty-watchlist genre should render 'Watchlist coverage pending'; got:\n{pending_render}")
elif "Genre detected: poetry" not in pending_render:
    fail(f"genre line should name detected genre; got:\n{pending_render}")
else:
    ok("empty-watchlist genre → 'Genre detected: poetry. Watchlist coverage pending.'")


# --- severity line aggregates agent severities (R2 / R17, U4) ---

print("\n=== severity line aggregates agent severities ===")

# R17 maps agent severities through the same severity x depth → action mapping
# as auto-detected. R2's severity counts therefore aggregate auto + agent
# flagged counts. With 3 agent items flagged at strong_warning, the severity
# line must include those 3 even though zero auto-detected items are flagged.
agent_only_flagged = all_clear_judgement()
agent_only_flagged[0] = {
    "id": "structural_monotony", "status": "flagged", "severity": "strong_warning",
    "answer": "every section follows the same arc", "evidence": {},
}
agent_only_flagged[1] = {
    "id": "tonal_uniformity", "status": "flagged", "severity": "strong_warning",
    "answer": "register holds without breaks", "evidence": {},
}
agent_only_flagged[3] = {
    "id": "neutrality_collapse", "status": "flagged", "severity": "strong_warning",
    "answer": "hedges its position", "evidence": {},
}

integration_render = with_patched_judgement(
    agent_only_flagged,
    lambda: format_two_layer(clean_results(), depth="balanced"),
)

# Post-U4: programmatic block always renders, counts line reports 0 auto + 3 agent flagged,
# severity line aggregates the 3 strong_warning agent severities.
if "Auto-detected: 0 of " not in integration_render:
    fail(f"counts line should show 'Auto-detected: 0 of N flagged'; got:\n{integration_render}")
elif "Agent-assessed: 3 of 8 flagged" not in integration_render:
    fail(f"counts line should show 'Agent-assessed: 3 of 8 flagged'; got:\n{integration_render}")
elif "Severity: 0 hard fail · 3 strong warning · 0 context warning" not in integration_render:
    fail(f"severity line should aggregate the 3 agent strong_warning items; got:\n{integration_render}")
elif "**Agent-judgement reading — 3 flagged of 8**" not in integration_render:
    fail(f"agent block should report 3 flagged of 8; got:\n{integration_render}")
else:
    ok("agent-only-flagged: severity line aggregates agent severities (R2 + R17)")


# --- both halves clear → full three-line summary (R9, no collapse) ---

print("\n=== both halves clear → full three-line summary ===")

both_clear_render = with_patched_judgement(
    all_clear_judgement(),
    lambda: format_two_layer(clean_results(), depth="balanced"),
)

# Post-U4: zero-flag draft emits the three-line summary plus the agent
# block's clean form. No collapse to a single line (R9 retired R8).
if not both_clear_render.startswith("Audit\n"):
    fail(f"both-clear render should still emit the Audit header (R9, no collapse); got:\n{both_clear_render}")
elif "Auto-detected: 0 of " not in both_clear_render:
    fail(f"both-clear counts line should show 'Auto-detected: 0 of N flagged'; got:\n{both_clear_render}")
elif "Agent-assessed: 0 of 8 flagged" not in both_clear_render:
    fail(f"both-clear counts line should show 'Agent-assessed: 0 of 8 flagged'; got:\n{both_clear_render}")
elif "Severity: 0 hard fail · 0 strong warning · 0 context warning" not in both_clear_render:
    fail(f"both-clear severity line should be all-zero; got:\n{both_clear_render}")
elif "**Agent-judgement reading**" not in both_clear_render:
    fail(f"both-clear render should still surface the agent block (clean form); got:\n{both_clear_render}")
elif "agent reading clean" not in both_clear_render:
    fail(f"both-clear render should carry the 'agent reading clean' body; got:\n{both_clear_render}")
else:
    ok("both halves clear → full three-line programmatic summary + clean-form agent block (no collapse)")


# --- programmatic flagged + agent clear → both blocks render ---

print("\n=== programmatic flagged + agent clear → both blocks ===")

prog_flagged_results = [
    annotate_result({"text": "no-em-dashes", "passed": False, "evidence": "—",
                     "matches": ["—"]}),
] + [
    annotate_result({"text": cid, "passed": True, "evidence": "clean"})
    for cid in ALL_CHECKS if cid != "no-em-dashes"
]

dual_render = with_patched_judgement(
    all_clear_judgement(),
    lambda: format_two_layer(prog_flagged_results, depth="balanced"),
)

# Programmatic block present (verdict line + Em dashes block)
if "Severity:" not in dual_render:
    fail(f"programmatic block should be present; got:\n{dual_render}")
# Agent block in clean form
elif "**Agent-judgement reading**" not in dual_render:
    fail(f"agent block in clean form expected; got:\n{dual_render}")
elif "agent reading clean" not in dual_render:
    fail(f"agent clean body expected; got:\n{dual_render}")
# Two separators expected (Layer 1/2 split + programmatic/agent split)
elif dual_render.count("\n---\n") != 2:
    fail(f"expected two '\\n---\\n' separators; got {dual_render.count(chr(10) + '---' + chr(10))}:\n{dual_render}")
else:
    ok("programmatic flagged + agent clear → both blocks with two separators")


# --- Summary ---

if FAILURES:
    print(f"\n{FAILURES} FAILURES")
    sys.exit(1)
print("\n========================================")
print("ALL PASSED")
