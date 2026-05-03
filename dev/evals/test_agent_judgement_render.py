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


# --- status binary: no severity column, no severity glyphs, no `mixed` ---

print("\n=== status binary, no severity surface ===")

for forbidden in ("hard_fail", "strong_warning", "context_warning"):
    if forbidden in mixed_render:
        fail(f"agent block should not include severity term {forbidden!r}")
        break
else:
    ok("no severity terms in agent block")

# `mixed` is a substring of "mixed_intentional" (old token, removed in U12 schema rewrite)
# and shouldn't appear standalone. The mechanical transform of any judgement id
# also doesn't produce 'mixed', so any occurrence is a regression.
if " mixed " in f" {mixed_render.lower()} " or "mixed_intentional" in mixed_render:
    fail("agent block should not include `mixed` state vocabulary")
else:
    ok("no 'mixed' state vocabulary in render")

# Severity glyphs: x !  ?  — none should appear at the start of any bullet line.
# Each agent bullet starts with '- '. Glyph-style lines start with the glyph.
for line in mixed_render.splitlines():
    if line[:2] in {"x ", "! ", "? "}:
        fail(f"bullet uses severity glyph: {line!r}")
        break
else:
    ok("no severity glyphs leading any line")


# Polymorphic genre slot test deleted in U3 (audit-output redesign): the
# previous fixture asserted a `| Genre specific | Flagged | Fix |` table-row
# shape that the current renderer never produced. U5 reworks
# `_render_judgement_item` / `_render_judgement_list_item` /
# `_render_judgement_composite_item` onto the new glyph + sub-bullet shape
# (`! **Genre specific** — Genre detected: <genre>` + watchlist sub-bullets)
# and adds the replacement composite-genre fixture per its plan.


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


# --- only genre slot fires → single block (integration via format_two_layer) ---

print("\n=== only genre slot fires → single block ===")

only_genre_judgement = all_clear_judgement()
only_genre_judgement[-1] = {
    "id": "genre_specific",
    "status": "flagged",
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

if genre_only_render.startswith("Audit\n"):
    fail(f"only-genre case should suppress programmatic block; got:\n{genre_only_render}")
elif "Severity:" in genre_only_render:
    fail(f"only-genre case should suppress programmatic verdict line; got:\n{genre_only_render}")
elif "**Agent-judgement reading" not in genre_only_render:
    fail(f"only-genre case should render agent block; got:\n{genre_only_render}")
elif "Genre detected: academic" not in genre_only_render:
    fail(f"genre slot should render detected genre; got:\n{genre_only_render}")
elif "as we have seen" not in genre_only_render:
    fail(f"genre slot should render watchlist findings; got:\n{genre_only_render}")
else:
    ok("only-genre-flagged → single agent block (no programmatic block)")


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


# --- agent findings don't inflate verdict-line severity counts ---

print("\n=== verdict line ignores agent findings ===")

# Build agent-only-flagged scenario: programmatic clear, agent has 3 flagged.
# Programmatic block must be suppressed entirely; verdict line never appears,
# so by construction the severity counts from agent findings can't leak in.
agent_only_flagged = all_clear_judgement()
agent_only_flagged[0] = {
    "id": "structural_monotony", "status": "flagged",
    "answer": "every section follows the same arc", "evidence": {},
}
agent_only_flagged[1] = {
    "id": "tonal_uniformity", "status": "flagged",
    "answer": "register holds without breaks", "evidence": {},
}
agent_only_flagged[3] = {
    "id": "neutrality_collapse", "status": "flagged",
    "answer": "hedges its position", "evidence": {},
}

integration_render = with_patched_judgement(
    agent_only_flagged,
    lambda: format_two_layer(clean_results(), depth="balanced"),
)

# Programmatic block should be absent → no verdict line possible.
if integration_render.startswith("Audit\n") or "Severity:" in integration_render:
    fail(f"agent-only-flagged should not surface programmatic verdict line; got:\n{integration_render}")
# Sanity: the agent block must still report 3 flagged.
elif "**Agent-judgement reading — 3 flagged of 8**" not in integration_render:
    fail(f"agent block should report 3 flagged of 8; got:\n{integration_render}")
else:
    ok("agent-only-flagged: programmatic verdict line never emitted (counts can't be inflated)")


# --- R8 single-line wins when both blocks clear ---

print("\n=== R8 single-line wins when both halves clear ===")

both_clear_render = with_patched_judgement(
    all_clear_judgement(),
    lambda: format_two_layer(clean_results(), depth="balanced"),
)

if "**Agent-judgement reading" in both_clear_render:
    fail(f"both-clear render should be R8 single-line, not show agent block; "
         f"got:\n{both_clear_render}")
elif "agent reading clean" not in both_clear_render:
    fail(f"R8 single-line should mention 'agent reading clean'; got:\n{both_clear_render}")
elif both_clear_render.count("\n") > 1:
    fail(f"R8 single-line should be one summary line + next-step prompt; got:\n{both_clear_render}")
else:
    ok("R8 single-line wins when programmatic + agent both clear")


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
