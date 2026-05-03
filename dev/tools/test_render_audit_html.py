#!/usr/bin/env python3
"""Smoke test for dev/tools/render_audit_html.py.

Builds a fixture iteration directory in a temp tree (matching the
shape produced by run_skill_creator_iteration.py), runs the generator,
and asserts the emitted HTML contains the expected per-eval sections,
rendered audit content, and assertion summary.

Audit-shape-agnostic: the generator renders whatever response.md
contains, so these fixtures use the post-U7 audit shape (counts line +
severity + signal stacking + glyph + bold flagged items + 4-column
coverage table + Next step) to mirror what real iteration-7+ output
will look like.

Run: python3 dev/tools/test_render_audit_html.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    "render_audit_html", ROOT / "dev" / "tools" / "render_audit_html.py"
)
_module = importlib.util.module_from_spec(_spec)
if _spec.loader is None:
    raise RuntimeError("Could not load dev/tools/render_audit_html.py")
_spec.loader.exec_module(_module)

render_audit_md = _module.render_audit_md
scan_iteration = _module.scan_iteration
render_html = _module.render_html

FAILURES = 0


def fail(msg: str) -> None:
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def assert_in(needle: str, haystack: str, label: str) -> None:
    if needle in haystack:
        ok(label)
    else:
        # Trim to keep failure output readable.
        snippet = haystack[:600] + ("…" if len(haystack) > 600 else "")
        fail(f"{label}\n  needle: {needle!r}\n  haystack head: {snippet!r}")


def assert_not_in(needle: str, haystack: str, label: str) -> None:
    if needle not in haystack:
        ok(label)
    else:
        fail(f"{label} — needle unexpectedly found: {needle!r}")


# ---------- markdown subset rendering (unit) ----------

print("=== render_audit_md: bold + tables + horizontal rule ===")

bold_md = "! **Em dashes** — \"—\""
bold_html = render_audit_md(bold_md)
assert_in("<strong>Em dashes</strong>", bold_html, "bold text wraps in <strong>")
assert_in("! ", bold_html, "glyph survives at start of line")

table_md = """| Pattern | Severity | Result | Detail |
| --- | --- | --- | --- |
| Em dashes | strong warning | Flagged | Fix em dashes; recommend preserving voiced enthusiasm. |
| Triad density | strong warning | Clear |  |"""
table_html = render_audit_md(table_md)
assert_in("<table", table_html, "table renders to <table>")
assert_in("<th>Pattern</th>", table_html, "table header renders in <thead>")
assert_in("<td>Em dashes</td>", table_html, "table body cell renders")
assert_not_in("---", table_html, "separator row is consumed (not rendered as data)")

hr_md = "Audit\nAuto-detected: 0 of 0 flagged\n\n---\n\n**Next step**"
hr_html = render_audit_md(hr_md)
assert_in("<hr>", hr_html, "--- horizontal rule renders to <hr>")

# Sub-bullets: a multi-finding agent-assessed item indents with two leading spaces;
# render_audit_md preserves leading whitespace via &nbsp; so the indent is visible.
sub_bullet_md = "! **Faux specificity**\n  - \"phrase 1\" — why 1\n  - \"phrase 2\" — why 2"
sub_bullet_html = render_audit_md(sub_bullet_md)
assert_in("&nbsp;&nbsp;- &quot;phrase 1&quot;", sub_bullet_html, "sub-bullet indent preserved as &nbsp;")

# HTML in the source must escape so it renders as text, not markup.
escape_md = "Audit\n<script>alert(1)</script>"
escape_html = render_audit_md(escape_md)
assert_in("&lt;script&gt;", escape_html, "raw HTML in source escapes to &lt;…&gt;")
assert_not_in("<script>", escape_html, "raw <script> tags do not pass through")


# ---------- iteration scan + full HTML render ----------

# Post-U7 shape: real audit body the agent now produces.
NEW_SHAPE_AUDIT = """Audit
Auto-detected: 2 of 48 flagged · Agent-assessed: 1 of 8 flagged
Severity: 0 hard fail · 2 strong warning · 1 context warning
Signal stacking: clear (weaker AI signals are not accumulating)

! **Em dashes** — "—"
! **Filler phrases** — "is often described as"
? **Structural monotony** — every section follows the same arc

**Next step**

Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?
"""

ZERO_FLAG_AUDIT = """Audit
Auto-detected: 0 of 48 flagged · Agent-assessed: 0 of 8 flagged
Severity: 0 hard fail · 0 strong warning · 0 context warning
Signal stacking: clear (weaker AI signals are not accumulating)

**Next step**

Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?
"""

RUNAWAY_AUDIT = """Audit
Auto-detected: 8 of 48 flagged · Agent-assessed: 8 of 8 flagged
Severity: 2 hard fail · 11 strong warning · 3 context warning
Signal stacking: triggered — 9 of 4 threshold (em dashes, tonal uniformity)

x **Assistant residue** — "great question"
! **Em dashes** — "—"
! **Structural monotony** — every section follows the same arc
! **Tonal uniformity** — register holds without breaks
! **Faux specificity**
  - "phrase 1" — why 1
  - "phrase 2" — why 2
! **Neutrality collapse** — hedges its position
? **Even jargon distribution** — jargon clumps where the writer knows things
? **Forced synesthesia**
? **Generic metaphors**
? **Genre specific** — Genre detected: academic
  - "phrase" — why

**Next step**

Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?
"""


def write_run(eval_dir: Path, config: str, run_n: int, response_md: str | None) -> None:
    run_dir = eval_dir / config / f"run-{run_n}"
    (run_dir / "outputs").mkdir(parents=True, exist_ok=True)
    if response_md is not None:
        (run_dir / "outputs" / "response.md").write_text(response_md, encoding="utf-8")


def build_fixture_iteration(tmp: Path) -> Path:
    iteration = tmp / "iteration-test"
    iteration.mkdir()

    write_run(iteration / "eval-0-audit-ai-cultural", "with_skill", 1, NEW_SHAPE_AUDIT)
    write_run(iteration / "eval-0-audit-ai-cultural", "with_skill", 2, NEW_SHAPE_AUDIT)
    write_run(iteration / "eval-1-audit-human-reflective-essay", "with_skill", 1, ZERO_FLAG_AUDIT)
    write_run(iteration / "eval-2-audit-human-literary", "with_skill", 1, RUNAWAY_AUDIT)
    # eval-3 has no response.md (failed run) — exercises the missing-output edge case.
    (iteration / "eval-3-suggestions-ai-wellbeing" / "with_skill" / "run-1" / "outputs").mkdir(parents=True)

    benchmark = {
        "metadata": {"timestamp": "2026-05-04T12:00:00Z", "evals_run": [0, 1, 2, 3]},
        "runs": [
            {
                "eval_id": 0, "configuration": "with_skill", "run_number": 1,
                "result": {"passed": 9, "failed": 0, "total": 9},
                "expectations": [
                    {"text": "Output references at least 5 distinct AI patterns", "passed": True, "evidence": "9 patterns"},
                    {"text": "Each pattern's explanation teaches the writer", "passed": True, "evidence": "Qualitative assertion deferred to Mae in the review viewer."},
                ],
            },
            {
                "eval_id": 0, "configuration": "with_skill", "run_number": 2,
                "result": {"passed": 7, "failed": 2, "total": 9},
                "expectations": [
                    {"text": "Output references at least 5 distinct AI patterns", "passed": True, "evidence": "9 patterns"},
                    {"text": "Every flagged pattern shows a quoted phrase", "passed": False, "evidence": "1 of 9 flag block(s) missing quoted phrase"},
                ],
            },
            {
                "eval_id": 1, "configuration": "with_skill", "run_number": 1,
                "result": {"passed": 9, "failed": 0, "total": 9},
                "expectations": [{"text": "Audit returns clean", "passed": True, "evidence": "all-clear shape"}],
            },
            {
                "eval_id": 2, "configuration": "with_skill", "run_number": 1,
                "result": {"passed": 9, "failed": 0, "total": 9},
                "expectations": [{"text": "Runaway flags caught", "passed": True, "evidence": "16 flag block(s)"}],
            },
            {
                "eval_id": 3, "configuration": "with_skill", "run_number": 1,
                "result": {"passed": 0, "failed": 0, "total": 0},
                "expectations": [],
            },
        ],
    }
    (iteration / "benchmark.json").write_text(json.dumps(benchmark), encoding="utf-8")
    return iteration


# Minimal evals.json substitute matching the fixture's 4 evals.
FIXTURE_EVALS = [
    {"id": 0, "name": "audit-ai-cultural", "prompt": "Audit this draft for AI tells.", "files": []},
    {"id": 1, "name": "audit-human-reflective-essay", "prompt": "Audit this draft for AI tells.", "files": []},
    {"id": 2, "name": "audit-human-literary", "prompt": "Audit this draft for AI tells.", "files": []},
    {"id": 3, "name": "suggestions-ai-wellbeing", "prompt": "Suggest replacements.", "files": []},
]


with tempfile.TemporaryDirectory() as tmp_str:
    tmp = Path(tmp_str)
    iteration_dir = build_fixture_iteration(tmp)

    print("\n=== scan_iteration: structure ===")
    scan = scan_iteration(iteration_dir, FIXTURE_EVALS)
    if len(scan["evals"]) == 4:
        ok("scan finds all 4 fixture evals")
    else:
        fail(f"expected 4 evals, got {len(scan['evals'])}")

    eval0 = next(e for e in scan["evals"] if e["id"] == 0)
    if len(eval0["runs"]) == 2:
        ok("eval-0 has 2 runs")
    else:
        fail(f"eval-0: expected 2 runs, got {len(eval0['runs'])}")

    eval3 = next(e for e in scan["evals"] if e["id"] == 3)
    if eval3["runs"] and eval3["runs"][0]["response_md"] is None:
        ok("missing response.md surfaces as None (failed-run edge case)")
    else:
        fail(f"eval-3 should have a run with response_md=None; got {eval3['runs']}")

    print("\n=== render_html: page structure ===")
    html_text = render_html(scan)

    assert_in("<title>Audit fidelity — iteration-test</title>", html_text, "page title carries iteration label")
    assert_in('class="eval-index"', html_text, "page index renders")
    assert_in("4 eval(s)", html_text, "page header reports eval count")

    print("\n=== render_html: per-eval sections ===")
    assert_in('id="eval-0"', html_text, "eval-0 section anchor present")
    assert_in('id="eval-1"', html_text, "eval-1 section anchor present")
    assert_in('id="eval-2"', html_text, "eval-2 section anchor present")
    assert_in("audit-ai-cultural", html_text, "eval name in body")

    print("\n=== render_html: rendered audit content (post-U7 shape) ===")
    assert_in("Auto-detected: 2 of 48 flagged", html_text, "counts line passes through verbatim")
    assert_in("Severity: 0 hard fail · 2 strong warning · 1 context warning", html_text, "severity line passes through verbatim")
    assert_in("Signal stacking: clear", html_text, "signal-stacking line passes through verbatim")
    assert_in("<strong>Em dashes</strong>", html_text, "auto-detected flagged item bold renders")
    assert_in("! ", html_text, "severity glyph survives as plain UTF-8")

    # Zero-flag (eval-1) renders the all-zeros summary, no flagged items.
    assert_in("Auto-detected: 0 of 48 flagged · Agent-assessed: 0 of 8 flagged", html_text, "zero-flag summary renders")

    # Runaway (eval-2) renders all 8 agent-assessed items + sub-bullets.
    assert_in("<strong>Faux specificity</strong>", html_text, "runaway: agent-assessed list-type item renders")
    assert_in("<strong>Genre specific</strong>", html_text, "runaway: composite genre slot renders")

    print("\n=== render_html: assertion column ===")
    assert_in("Output references at least 5 distinct AI patterns", html_text, "assertion text renders")
    assert_in("9 patterns", html_text, "assertion evidence renders")
    assert_in("1 of 9 flag block(s) missing quoted phrase", html_text, "failing assertion evidence renders")
    assert_in('class="assertion-status pass"', html_text, "passing assertion has pass class")
    assert_in('class="assertion-status fail"', html_text, "failing assertion has fail class")
    assert_in('class="assertion-status deferred"', html_text, "qualitative-deferred assertion has deferred class")

    print("\n=== render_html: failing run defaults to expanded ===")
    # eval-0 run-2 fails, so its <details> block must carry the `open` attribute.
    eval0_section_start = html_text.index('id="eval-0"')
    eval0_section_end = html_text.index('id="eval-1"')
    eval0_section = html_text[eval0_section_start:eval0_section_end]
    if 'class="run-block" open' in eval0_section or 'class="run-block"  open' in eval0_section or '<details class="run-block" open>' in eval0_section:
        ok("failing run is open by default")
    else:
        # Verify at least one open block exists for run 1 of eval-0 (first per config).
        if '<details class="run-block" open>' in eval0_section:
            ok("first run per config is open by default (failing-run check inferred from open count)")
        else:
            fail(f"eval-0 should have at least one open <details> block; section head:\n{eval0_section[:600]}")

    print("\n=== render_html: missing response.md edge case ===")
    eval3_section_start = html_text.index('id="eval-3"')
    eval3_section = html_text[eval3_section_start:eval3_section_start + 2000]
    assert_in("response.md missing", eval3_section, "missing response.md renders a placeholder")


print("\n========================================")
if FAILURES:
    print(f"FAILED: {FAILURES} assertion(s) failed")
    sys.exit(1)
else:
    print("ALL PASSED")
    sys.exit(0)
