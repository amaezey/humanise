#!/usr/bin/env python3
"""render_audit_html.py — Generate audit-fidelity.html for an iteration.

Reads dev/skill-workspace/iteration-N/ and emits a single static HTML file
at the workspace root that renders each eval's response.md as a writer
would see it (markdown to HTML), alongside that run's benchmark assertion
results. Audit-shape-agnostic: renders whatever the agent actually wrote,
including any drift from the spec — that is the point.

Precedent: dev/tools/render_patterns_md.py.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_EVALS_JSON = REPO_ROOT / "dev" / "evals" / "evals.json"

CONFIG_ORDER = {"with_skill": 0, "old_skill": 1}


# ---------- markdown subset to HTML ----------

_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_TABLE_SEP_CELL_RE = re.compile(r"^:?-+:?$")


def _inline_md(text: str) -> str:
    """Escape HTML, then convert **bold** to <strong>."""
    escaped = html.escape(text)
    return _BOLD_RE.sub(r"<strong>\1</strong>", escaped)


def _is_table_row(line: str) -> bool:
    return line.lstrip().startswith("|")


def _is_table_separator(cells: list[str]) -> bool:
    return all(_TABLE_SEP_CELL_RE.match(c) for c in cells if c)


def _split_table_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _render_table(rows: list[str]) -> str:
    parsed = [_split_table_row(r) for r in rows]
    has_separator = len(parsed) >= 2 and _is_table_separator(parsed[1])
    if has_separator:
        header = parsed[0]
        body = parsed[2:]
    else:
        header = None
        body = parsed
    out = ['<table class="audit-table">']
    if header:
        out.append("<thead><tr>")
        for cell in header:
            out.append(f"<th>{_inline_md(cell)}</th>")
        out.append("</tr></thead>")
    out.append("<tbody>")
    for row in body:
        out.append("<tr>")
        for cell in row:
            out.append(f"<td>{_inline_md(cell)}</td>")
        out.append("</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_audit_md(text: str) -> str:
    """Render the audit's small markdown subset to HTML.

    Handles bold (**...**), pipe tables, --- horizontal rules, and
    paragraph blocks separated by blank lines. Lines within a paragraph
    block keep their leading whitespace (rendered as &nbsp;) and are
    joined with <br>. Glyphs (x ! ? ✓ ✗) pass through as plain UTF-8.
    """
    lines = text.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped == "---":
            out.append("<hr>")
            i += 1
            continue
        if _is_table_row(line):
            j = i
            while j < len(lines) and _is_table_row(lines[j]):
                j += 1
            out.append(_render_table(lines[i:j]))
            i = j
            continue
        block = []
        while i < len(lines) and lines[i].strip() and lines[i].strip() != "---" and not _is_table_row(lines[i]):
            block.append(lines[i])
            i += 1
        rendered_lines = []
        for raw in block:
            leading = len(raw) - len(raw.lstrip(" "))
            indent = "&nbsp;" * leading
            rendered_lines.append(indent + _inline_md(raw.lstrip(" ")))
        out.append('<p class="audit-line-block">' + "<br>".join(rendered_lines) + "</p>")
    return "\n".join(out)


# ---------- iteration scan ----------

def _eval_dir_name(item: dict) -> str:
    return f"eval-{item['id']}-{item['name']}"


def _resolve_eval_file(path: str) -> Path | None:
    candidates = [
        REPO_ROOT / path,
        REPO_ROOT / "dev" / path,
        REPO_ROOT / "dev" / "evals" / path,
        REPO_ROOT / "dev" / "evals" / "samples" / Path(path).name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _read_evals_json(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["evals"] if isinstance(data, dict) and "evals" in data else data


def _input_draft_for(eval_item: dict) -> str:
    parts = []
    for raw_path in eval_item.get("files", []):
        resolved = _resolve_eval_file(raw_path)
        if resolved and resolved.exists():
            parts.append(f"=== {raw_path} ===\n\n" + resolved.read_text(encoding="utf-8"))
    return "\n\n".join(parts)


def _runs_sorted(runs: list[dict]) -> list[dict]:
    return sorted(
        runs,
        key=lambda r: (
            CONFIG_ORDER.get(r.get("configuration", ""), 99),
            r.get("configuration", ""),
            int(r.get("run_number", 0)),
        ),
    )


def scan_iteration(iteration_dir: Path, evals: list[dict]) -> dict:
    benchmark_path = iteration_dir / "benchmark.json"
    if benchmark_path.exists():
        benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    else:
        benchmark = {"runs": [], "metadata": {}}

    runs_by_eval: dict[int, list[dict]] = {}
    for run in benchmark.get("runs", []):
        runs_by_eval.setdefault(run["eval_id"], []).append(run)

    eval_views = []
    for item in evals:
        eval_dir = iteration_dir / _eval_dir_name(item)
        if not eval_dir.exists():
            continue
        runs = []
        for run_summary in _runs_sorted(runs_by_eval.get(item["id"], [])):
            config = run_summary["configuration"]
            run_n = run_summary["run_number"]
            response_path = eval_dir / config / f"run-{run_n}" / "outputs" / "response.md"
            response_md = response_path.read_text(encoding="utf-8") if response_path.exists() else None
            runs.append({
                "config": config,
                "run_number": run_n,
                "response_md": response_md,
                "result": run_summary.get("result", {}),
                "expectations": run_summary.get("expectations", []),
            })
        eval_views.append({
            "id": item["id"],
            "name": item["name"],
            "prompt": item["prompt"],
            "input_draft": _input_draft_for(item),
            "runs": runs,
        })
    return {
        "iteration_dir": iteration_dir,
        "metadata": benchmark.get("metadata", {}),
        "evals": eval_views,
    }


# ---------- HTML assembly ----------

PAGE_CSS = """
:root {
  --bg: #faf9f5;
  --surface: #ffffff;
  --border: #e8e6dc;
  --text: #141413;
  --text-muted: #8b8a82;
  --accent: #d97757;
  --green: #4f6f3a;
  --green-bg: #eef2e8;
  --red: #b04a3a;
  --red-bg: #fceaea;
  --grey-bg: #f1efe8;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Lora', Georgia, 'Times New Roman', serif; background: var(--bg); color: var(--text); line-height: 1.55; padding: 2rem 1.5rem; max-width: 1280px; margin: 0 auto; }
.page-header { border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }
.page-header h1 { font-size: 1.5rem; font-weight: 600; }
.page-header .meta { color: var(--text-muted); font-size: 0.9rem; margin-top: 0.35rem; }
.eval-index { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 1rem 1.25rem; margin-bottom: 2rem; }
.eval-index h2 { font-size: 1rem; margin-bottom: 0.5rem; font-weight: 600; }
.eval-index ol { list-style: decimal inside; font-size: 0.9rem; line-height: 1.7; }
.eval-index a { color: var(--accent); text-decoration: none; }
.eval-index a:hover { text-decoration: underline; }
.eval-index .index-meta { color: var(--text-muted); }
.eval-section { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 1.25rem 1.5rem; margin-bottom: 2rem; }
.eval-header h2 { font-size: 1.15rem; font-weight: 600; }
.eval-header .prompt { color: var(--text-muted); font-size: 0.875rem; margin-top: 0.25rem; font-style: italic; }
.input-draft { margin: 1rem 0; }
.input-draft summary { cursor: pointer; color: var(--text-muted); font-size: 0.875rem; user-select: none; }
.input-draft summary:hover { color: var(--text); }
.input-draft pre { background: var(--bg); border: 1px solid var(--border); padding: 0.75rem; border-radius: 4px; font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace; font-size: 0.8125rem; line-height: 1.5; white-space: pre-wrap; max-height: 400px; overflow: auto; margin-top: 0.5rem; }
.run-block { margin-top: 1rem; border-top: 1px solid var(--border); }
.run-block:first-of-type { border-top: none; }
.run-summary { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 0; cursor: pointer; user-select: none; list-style: none; }
.run-summary::-webkit-details-marker { display: none; }
.run-summary::before { content: "▸"; color: var(--text-muted); font-size: 0.75rem; transition: transform 0.15s; }
.run-block[open] .run-summary::before { transform: rotate(90deg); display: inline-block; }
.run-label { font-weight: 600; }
.run-config { color: var(--text-muted); font-size: 0.875rem; }
.run-badge { padding: 0.125rem 0.625rem; border-radius: 999px; font-size: 0.8125rem; font-weight: 600; margin-left: auto; }
.run-badge.pass { background: var(--green-bg); color: var(--green); }
.run-badge.fail { background: var(--red-bg); color: var(--red); }
.run-detail { display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; padding: 0.5rem 0 1rem 0; }
@media (max-width: 900px) { .run-detail { grid-template-columns: 1fr; } }
.audit-render { font-size: 0.95rem; min-width: 0; word-wrap: break-word; }
.audit-render p.audit-line-block { margin: 0.65rem 0; }
.audit-render hr { border: 0; border-top: 1px solid var(--border); margin: 1.25rem 0; }
.audit-render .audit-table { border-collapse: collapse; margin: 0.75rem 0; font-size: 0.85rem; width: 100%; }
.audit-render .audit-table th, .audit-render .audit-table td { border: 1px solid var(--border); padding: 0.4rem 0.6rem; text-align: left; vertical-align: top; }
.audit-render .audit-table th { background: var(--grey-bg); font-weight: 600; }
.audit-render strong { font-weight: 600; }
.assertions h3 { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--text-muted); margin-bottom: 0.5rem; font-weight: 600; }
.assertions ul { list-style: none; }
.assertion { padding: 0.5rem 0; border-bottom: 1px solid var(--border); font-size: 0.85rem; }
.assertion:last-child { border-bottom: none; }
.assertion-status { font-weight: 600; margin-right: 0.4rem; }
.assertion-status.pass { color: var(--green); }
.assertion-status.fail { color: var(--red); }
.assertion-status.deferred { color: var(--text-muted); }
.assertion-evidence { color: var(--text-muted); font-size: 0.8rem; margin-top: 0.25rem; word-wrap: break-word; }
.empty-response { color: var(--text-muted); font-style: italic; padding: 1rem; background: var(--bg); border: 1px dashed var(--border); border-radius: 4px; }
""".strip()


def _badge(passed: int, total: int) -> str:
    if total == 0:
        return '<span class="run-badge fail">— no result</span>'
    cls = "pass" if passed == total else "fail"
    glyph = "✓" if passed == total else "✗"
    return f'<span class="run-badge {cls}">{glyph} {passed}/{total}</span>'


def _classify_assertion(exp: dict) -> tuple[str, str]:
    passed = exp.get("passed")
    evidence = (exp.get("evidence") or "").lower()
    if passed and ("deferred" in evidence or "qualitative" in evidence):
        return ("deferred", "⊘")
    if passed:
        return ("pass", "✓")
    return ("fail", "✗")


def _render_assertions(expectations: list[dict]) -> str:
    if not expectations:
        return '<h3>Assertions</h3><p class="empty-response">No assertion results recorded.</p>'
    items = []
    for exp in expectations:
        cls, glyph = _classify_assertion(exp)
        text = exp.get("text", "")
        evidence = exp.get("evidence", "") or ""
        items.append(
            '<li class="assertion">'
            f'<span class="assertion-status {cls}">{glyph}</span>'
            f'{html.escape(text)}'
            f'<div class="assertion-evidence">{html.escape(evidence)}</div>'
            '</li>'
        )
    return f'<h3>Assertions</h3><ul>{"".join(items)}</ul>'


def _render_run(run: dict, default_open: bool) -> str:
    response_md = run.get("response_md")
    result = run.get("result", {})
    passed = int(result.get("passed", 0))
    total = int(result.get("total", 0))
    badge = _badge(passed, total)
    open_attr = " open" if default_open else ""
    if response_md is None:
        body = '<p class="empty-response">response.md missing — run did not produce output.</p>'
    elif not response_md.strip():
        body = '<p class="empty-response">response.md is empty.</p>'
    else:
        body = render_audit_md(response_md)
    assertions_html = _render_assertions(run.get("expectations", []))
    summary = (
        '<summary class="run-summary">'
        f'<span class="run-label">{html.escape(run["config"])}</span>'
        f'<span class="run-config">· run {run["run_number"]}</span>'
        f'{badge}'
        '</summary>'
    )
    return (
        f'<details class="run-block"{open_attr}>'
        f'{summary}'
        '<div class="run-detail">'
        f'<div class="audit-render">{body}</div>'
        f'<div class="assertions">{assertions_html}</div>'
        '</div>'
        '</details>'
    )


def _render_eval(eval_view: dict) -> str:
    runs = eval_view.get("runs", [])
    seen_first_per_config: set[str] = set()
    rendered_runs = []
    for run in runs:
        cfg = run["config"]
        is_first = cfg not in seen_first_per_config
        seen_first_per_config.add(cfg)
        is_failing = int(run.get("result", {}).get("failed", 0)) > 0
        default_open = is_first or is_failing
        rendered_runs.append(_render_run(run, default_open))

    input_draft = eval_view.get("input_draft", "")
    if input_draft:
        line_count = len(input_draft.splitlines())
        input_draft_html = (
            '<details class="input-draft">'
            f'<summary>Input draft ({line_count} lines)</summary>'
            f'<pre>{html.escape(input_draft)}</pre>'
            '</details>'
        )
    else:
        input_draft_html = ""

    runs_html = "".join(rendered_runs) if rendered_runs else '<p class="empty-response">No runs recorded for this eval.</p>'

    return (
        f'<section class="eval-section" id="eval-{eval_view["id"]}">'
        '<div class="eval-header">'
        f'<h2>{html.escape(eval_view["name"])}</h2>'
        f'<div class="prompt">{html.escape(eval_view["prompt"])}</div>'
        '</div>'
        f'{input_draft_html}'
        f'{runs_html}'
        '</section>'
    )


def _render_index(eval_views: list[dict]) -> str:
    items = []
    for ev in eval_views:
        total_passed = sum(int(r.get("result", {}).get("passed", 0)) for r in ev["runs"])
        total_total = sum(int(r.get("result", {}).get("total", 0)) for r in ev["runs"])
        n_runs = len(ev["runs"])
        items.append(
            '<li>'
            f'<a href="#eval-{ev["id"]}">{html.escape(ev["name"])}</a> '
            f'<span class="index-meta">— {total_passed}/{total_total} across {n_runs} run(s)</span>'
            '</li>'
        )
    return f'<div class="eval-index"><h2>Evals</h2><ol>{"".join(items)}</ol></div>'


def render_html(scan: dict) -> str:
    metadata = scan.get("metadata", {})
    eval_views = scan["evals"]
    timestamp = metadata.get("timestamp") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    iteration_label = scan["iteration_dir"].name
    n_evals = len(eval_views)
    n_runs = sum(len(ev["runs"]) for ev in eval_views)

    parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>Audit fidelity — {html.escape(iteration_label)}</title>',
        '<style>',
        PAGE_CSS,
        '</style>',
        '</head>',
        '<body>',
        '<div class="page-header">',
        f'<h1>Audit fidelity — {html.escape(iteration_label)}</h1>',
        f'<div class="meta">Generated {html.escape(timestamp)} · {n_evals} eval(s) · {n_runs} run(s)</div>',
        '</div>',
        _render_index(eval_views),
    ]
    for ev in eval_views:
        parts.append(_render_eval(ev))
    parts.append('</body></html>')
    return "\n".join(parts)


# ---------- CLI ----------

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render an iteration's audits as a static HTML page.")
    parser.add_argument("iteration_dir", type=Path, help="Path to dev/skill-workspace/iteration-N")
    parser.add_argument("--evals-json", type=Path, default=DEFAULT_EVALS_JSON,
                        help="Path to evals.json (default: dev/evals/evals.json)")
    parser.add_argument("--out", type=Path, default=None,
                        help="Output HTML path (default: <iteration_dir>/audit-fidelity.html)")
    args = parser.parse_args(argv)

    iteration_dir = args.iteration_dir.resolve()
    if not iteration_dir.exists():
        print(f"error: iteration directory does not exist: {iteration_dir}", file=sys.stderr)
        return 1

    out_path = args.out or (iteration_dir / "audit-fidelity.html")
    evals = _read_evals_json(args.evals_json)
    scan = scan_iteration(iteration_dir, evals)
    html_text = render_html(scan)
    out_path.write_text(html_text, encoding="utf-8")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
