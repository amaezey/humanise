#!/usr/bin/env python3
"""Run one skill-creator style output-quality iteration for humanise.

This is a thin adapter around Anthropic's skill-creator workflow:
- execute each eval against the current skill and the pre-rewrite snapshot
- save outputs in the workspace layout expected by skill-creator
- grade programmatic assertions into grading.json
- call skill-creator's aggregate_benchmark.py and generate_review.py
"""

from __future__ import annotations

import argparse
import concurrent.futures
import importlib.util
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVALS_PATH = ROOT / "dev" / "evals" / "evals.json"
WORKSPACE = ROOT / "dev" / "skill-workspace"
ITERATION = WORKSPACE / "iteration-1"
CURRENT_SKILL = ROOT / "humanise"
OLD_SKILL = WORKSPACE / "skill-snapshot"


def load_grade_module():
    spec = importlib.util.spec_from_file_location("humanise_grade", ROOT / "humanise" / "scripts" / "grade.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load humanise/scripts/grade.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GRADE = load_grade_module()

# patterns.json replaces CHECK_REPORT_TEXT (U7 of the audit-report redesign).
# Loaded once at module scope; consumers iterate _PATTERN_LABELS for (id, label) pairs.
# Skips _meta / _extra_entries (page-level content for U15 generator).
import json as _json
_PATTERN_LABELS = {
    cid: rec["short_name"]
    for cid, rec in _json.loads((ROOT / "humanise" / "scripts" / "patterns.json").read_text()).items()
    if not cid.startswith("_")
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def python_for_skill_creator() -> str:
    """Use a Python new enough for upstream skill-creator type syntax."""
    for candidate in ("/opt/homebrew/bin/python3.12", "python3.12", sys.executable):
        try:
            proc = subprocess.run(
                [candidate, "-c", "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if proc.returncode == 0:
                return candidate
        except OSError:
            continue
    return sys.executable


def eval_dir_name(item: dict) -> str:
    return f"eval-{item['id']}-{item['name']}"


def resolve_eval_file(path: str) -> Path:
    candidates = [
        ROOT / path,
        ROOT / "dev" / path,
        ROOT / "dev" / "evals" / path,
        ROOT / "dev" / "evals" / "samples" / Path(path).name,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(path)


def build_prompt(item: dict, skill_path: Path) -> str:
    file_blocks = []
    for raw_path in item.get("files", []):
        path = resolve_eval_file(raw_path)
        text = path.read_text(encoding="utf-8")
        file_blocks.append(f"Input file: {path}\n\n```markdown\n{text}\n```")

    inputs = "\n\n".join(file_blocks) if file_blocks else "No input files."
    return f"""You are running an evaluation of a local writing skill.

Use the skill at:
{skill_path / "SKILL.md"}

Read that skill and any referenced files you need from the same skill directory.
Do not edit repository files. Do not save files. Return only the final user-facing output for the task.
Do not mention this evaluation harness.

Task prompt:
{item["prompt"]}

Inputs:
{inputs}
"""


def run_claude(prompt: str, model: str | None) -> tuple[str, str, int]:
    cmd = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--verbose",
        "--allowedTools",
        "Read,Bash",
        "--add-dir",
        str(ROOT),
    ]
    if model:
        cmd.extend(["--model", model])

    env = {
        k: v for k, v in os.environ.items()
        if k not in {"CLAUDECODE", "ANTHROPIC_API_KEY"}
    }
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=1800,
    )

    raw = proc.stdout.strip()
    response = raw
    total_tokens = 0
    if raw:
        try:
            parsed = json.loads(raw)
            result_event = parsed[-1] if isinstance(parsed, list) and parsed else parsed
            if not isinstance(result_event, dict):
                result_event = {}
            response = result_event.get("result") or result_event.get("message") or raw
            usage = result_event.get("usage") or {}
            if isinstance(usage, list):
                total_tokens = sum(
                    int(entry.get("input_tokens") or 0)
                    + int(entry.get("output_tokens") or 0)
                    + int(entry.get("cache_creation_input_tokens") or 0)
                    + int(entry.get("cache_read_input_tokens") or 0)
                    for entry in usage
                    if isinstance(entry, dict)
                )
            elif isinstance(usage, dict):
                total_tokens = int(
                    (usage.get("input_tokens") or 0)
                    + (usage.get("output_tokens") or 0)
                    + (usage.get("cache_creation_input_tokens") or 0)
                    + (usage.get("cache_read_input_tokens") or 0)
                )
        except json.JSONDecodeError:
            pass

    if proc.returncode != 0:
        response = (
            "ERROR: claude run failed\n\n"
            f"Return code: {proc.returncode}\n\n"
            f"STDERR:\n{proc.stderr}\n\nSTDOUT:\n{proc.stdout}"
        )
    return response, proc.stderr, total_tokens


def run_codex(prompt: str, model: str | None) -> tuple[str, str, int]:
    with tempfile.NamedTemporaryFile(prefix="humanise-codex-output-", suffix=".md", delete=False) as f:
        output_path = Path(f.name)
    cmd = [
        "codex",
        "exec",
        "-C",
        str(ROOT),
        "-s",
        "read-only",
        "--ephemeral",
        "--output-last-message",
        str(output_path),
    ]
    if model:
        cmd.extend(["--model", model])
    cmd.append(prompt)

    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=1800,
    )
    try:
        response = output_path.read_text(encoding="utf-8")
    except OSError:
        response = proc.stdout
    finally:
        try:
            output_path.unlink()
        except OSError:
            pass

    if proc.returncode != 0:
        response = (
            "ERROR: codex run failed\n\n"
            f"Return code: {proc.returncode}\n\n"
            f"STDERR:\n{proc.stderr}\n\nSTDOUT:\n{proc.stdout}"
        )
    return response, proc.stderr, 0


def run_model(item: dict, config: str, skill_path: Path, run_dir: Path, model: str | None, executor_name: str) -> dict:
    outputs_dir = run_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    prompt = build_prompt(item, skill_path)
    (outputs_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    start = time.time()
    error_count = 0
    if executor_name == "claude":
        response, stderr, total_tokens = run_claude(prompt, model)
    elif executor_name == "codex":
        response, stderr, total_tokens = run_codex(prompt, model)
    else:
        raise ValueError(f"Unknown executor: {executor_name}")
    duration = time.time() - start
    if response.startswith("ERROR:"):
        error_count = 1

    (outputs_dir / "response.md").write_text(response, encoding="utf-8")
    if stderr.strip():
        (outputs_dir / "stderr.txt").write_text(stderr, encoding="utf-8")

    timing = {
        "total_tokens": total_tokens,
        "duration_ms": int(duration * 1000),
        "total_duration_seconds": round(duration, 3),
    }
    write_json(run_dir / "timing.json", timing)
    write_json(outputs_dir / "metrics.json", {
        "configuration": config,
        "output_chars": len(response),
        "errors_encountered": error_count,
        "total_tool_calls": 0,
    })
    return timing


def section_text(output: str, header: str) -> str:
    pattern = re.compile(rf"^\*\*{re.escape(header)}\*\*\s*$", re.MULTILINE | re.IGNORECASE)
    match = pattern.search(output)
    if not match:
        return ""
    next_match = re.search(r"^\*\*[^*]+\*\*\s*$", output[match.end():], re.MULTILINE)
    end = match.end() + next_match.start() if next_match else len(output)
    return output[match.end():end].strip()


def extract_generated_text(output: str) -> str:
    return section_text(output, "Rewrite") or section_text(output, "Draft") or output


def sentence_lengths(text: str) -> list[int]:
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    return [len(re.findall(r"\b\w+\b", s)) for s in sentences]


def paragraph_lengths(text: str) -> list[int]:
    paragraphs = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    return [len(re.findall(r"\b\w+\b", p)) for p in paragraphs]


# Names the skill emits in Layer 1 flag blocks that don't match the patterns.json
# short_name verbatim. Lower-cased keys; values are catalogue check_ids.
_LAYER_1_NAME_ALIASES = {
    "copula avoidance": "no-copula-avoidance",
    "contrived contrast / negative parallelism": "no-negative-parallelisms",
    "rule of three": "no-forced-triads",
    "curly quotation marks": "no-curly-quotes",
    "staccato rhythm in extended contexts": "no-staccato-sequences",
    "ghost/spectral language": "no-ghost-spectral-density",
    "unicode flair": "no-unicode-flair",
    "signal stacking": "overall-signal-stacking",
}

# Layer-1 flagged-item opener: `<glyph> <Name>` or `<glyph> <Name>: "<phrase>"`.
# Pattern names render unbold (post-rework). Captures the name up to the colon,
# end-of-line, or the `(+N more)` overflow tail.
_LAYER_1_NAME_RE = re.compile(r"^[x!?]\s+([A-Z][A-Za-z0-9 '\-]+?)(?:\s*[:.]|\s*$)")


def catalogue_hits(output: str) -> set[str]:
    """Distinct catalogue-pattern IDs that appear as Layer-1 programmatic flags
    (`! **Name** — ...` or `? **Name** — ...`) inside the response's audit section.

    Replaces an earlier substring-matching heuristic that broke under U11's
    two-layer renderer: section tables now list every pattern with Clear/Flagged
    status, so a substring match against the full response always returned the
    entire catalogue. Only flagged Layer-1 blocks count here.
    """
    audit = GRADE._audit_section(output) or ""
    if not audit:
        return set()
    label_to_id = {label.lower(): cid for cid, label in _PATTERN_LABELS.items()}
    hits: set[str] = set()
    for line in audit.splitlines():
        match = _LAYER_1_NAME_RE.match(line)
        if not match:
            continue
        name_lc = match.group(1).strip().lower()
        cid = label_to_id.get(name_lc) or _LAYER_1_NAME_ALIASES.get(name_lc)
        if cid:
            hits.add(cid)
    return hits


def grade_one_assertion(name: str, output: str, input_text: str, generated: str) -> tuple[bool, str]:
    if name == "audit-flags-present":
        hits = catalogue_hits(output)
        return len(hits) >= 5, f"Referenced {len(hits)} catalogue pattern(s): {sorted(hits)[:10]}"
    if name == "low-flag-count-on-human-prose":
        hits = catalogue_hits(output)
        return len(hits) <= 3, f"Referenced {len(hits)} catalogue pattern(s): {sorted(hits)[:10]}"
    if name == "low-flag-count-on-human-prose-runaway-guard":
        hits = catalogue_hits(output)
        return len(hits) <= 12, f"Referenced {len(hits)} catalogue pattern(s): {sorted(hits)[:10]}"
    if name == "each-flag-has-quoted-phrase":
        result = GRADE.check_audit_shape("every-flag-block-contains-input-substring", output, input_text)
        return result["passed"], result["evidence"]
    if name == "ends-with-next-step-question":
        result = GRADE.check_audit_shape("final-non-empty-line-ends-with-question", output, input_text)
        return result["passed"], result["evidence"]
    if name in {"no-rewritten-draft", "no-full-rewrite"}:
        result = GRADE.check_audit_shape("no-large-prose-block-not-in-input", output, input_text)
        return result["passed"], result["evidence"]
    if name in {"audit-shown-before-suggestions", "audit-shown-before-rewrite"}:
        result = GRADE.check_audit_shape("audit-shape-block-precedes-rewrite-block", output, input_text)
        return result["passed"], result["evidence"]
    if name == "suggestion-count-matches-flag-count":
        result = GRADE.check_audit_shape("suggestion-block-count-equals-flag-count", output, input_text)
        return result["passed"], result["evidence"]
    if name == "each-suggestion-has-replacement":
        result = GRADE.check_audit_shape("every-suggestion-block-has-replacement", output, input_text)
        return result["passed"], result["evidence"]
    if name == "has-programmatic-block":
        result = GRADE.check_audit_shape("audit-shape-has-programmatic-block", output, input_text)
        return result["passed"], result["evidence"]
    if name == "audit-counts-line-present":
        result = GRADE.check_audit_shape("audit-shape-counts-line", output, input_text)
        return result["passed"], result["evidence"]
    if name == "audit-severity-line-present":
        result = GRADE.check_audit_shape("audit-shape-severity-line", output, input_text)
        return result["passed"], result["evidence"]
    if name == "audit-signal-stacking-line-present":
        result = GRADE.check_audit_shape("audit-shape-signal-stacking-line", output, input_text)
        return result["passed"], result["evidence"]
    if name == "audit-flagged-items-glyph-shape":
        result = GRADE.check_audit_shape("audit-shape-flagged-items-glyph-shape", output, input_text)
        return result["passed"], result["evidence"]
    if name == "coverage-tables-include-severity":
        result = GRADE.check_audit_shape("audit-shape-severity-in-coverage-table", output, input_text)
        return result["passed"], result["evidence"]
    if name == "coverage-tables-omit-action":
        result = GRADE.check_audit_shape("audit-shape-no-action-column", output, input_text)
        return result["passed"], result["evidence"]
    if name == "rewrite-produced":
        input_words = len(re.findall(r"\b\w+\b", input_text))
        gen_words = len(re.findall(r"\b\w+\b", generated))
        changed = generated.strip() and generated.strip() not in input_text
        similar = input_words == 0 or gen_words >= max(50, int(input_words * 0.45))
        return changed and similar, f"generated_words={gen_words}; input_words={input_words}; changed={changed}"
    if name in {"no-em-dashes-in-rewrite", "no-em-dashes"}:
        return "—" not in generated, f"em dash count={generated.count('—')}"
    if name in {"no-delve-in-rewrite", "no-delve"}:
        count = len(re.findall(r"\bdelv(e|es|ing)\b", generated, re.IGNORECASE))
        return count == 0, f"delve count={count}"
    if name == "no-manufactured-insight":
        result = GRADE.annotate_result(GRADE.check_manufactured_insight(generated))
        return result["passed"], result.get("evidence", "")
    if name == "no-signposted-conclusions":
        result = GRADE.annotate_result(GRADE.check_signposted_conclusions(generated))
        return result["passed"], result.get("evidence", "")
    if name == "rewrite-passes-balanced-grader":
        result = GRADE.regrade(generated, depth="balanced")
        return result["fails"] == 0, f"balanced failures={result['failed_checks']}"
    if name == "rewrite-passes-all-grader":
        result = GRADE.regrade(generated, depth="all")
        return result["fails"] == 0, f"all failures={result['failed_checks']}"
    if name == "draft-passes-balanced-grader":
        result = GRADE.regrade(generated, depth="balanced")
        return result["fails"] == 0, f"balanced failures={result['failed_checks']}"
    if name == "sentence-length-variance-improved":
        before = sentence_lengths(input_text)
        after = sentence_lengths(generated)
        before_stdev = statistics.stdev(before) if len(before) > 1 else 0.0
        after_stdev = statistics.stdev(after) if len(after) > 1 else 0.0
        return after_stdev > before_stdev, f"input_stdev={before_stdev:.2f}; output_stdev={after_stdev:.2f}"
    if name == "paragraph-length-not-uniform":
        lengths = paragraph_lengths(generated)
        value = statistics.stdev(lengths) if len(lengths) > 1 else 0.0
        return value > 35, f"paragraph_word_count_stdev={value:.2f}; lengths={lengths}"
    if name == "no-input-draft-required":
        return input_text == "", "input files empty" if input_text == "" else "input text was present"
    if name == "word-count-near-target":
        count = len(re.findall(r"\b\w+\b", generated))
        return 213 <= count <= 288, f"word_count={count}"
    raise KeyError(name)


def grade_run(item: dict, run_dir: Path) -> dict:
    output = (run_dir / "outputs" / "response.md").read_text(encoding="utf-8")
    input_parts = []
    for raw_path in item.get("files", []):
        input_parts.append(resolve_eval_file(raw_path).read_text(encoding="utf-8"))
    input_text = "\n\n".join(input_parts)
    generated = extract_generated_text(output)

    expectations = []
    for assertion in item.get("assertions", []):
        text = assertion["description"]
        if assertion.get("type") != "programmatic":
            expectations.append({
                "text": text,
                "passed": True,
                "evidence": "Qualitative assertion deferred to Mae in the review viewer.",
            })
            continue
        try:
            passed, evidence = grade_one_assertion(assertion["name"], output, input_text, generated)
        except Exception as exc:  # keep the viewer useful even when an assertion needs work
            passed, evidence = False, f"grader error for {assertion['name']}: {exc}"
        expectations.append({"text": text, "passed": bool(passed), "evidence": evidence})

    passed_count = sum(1 for exp in expectations if exp["passed"])
    total = len(expectations)
    timing = read_json(run_dir / "timing.json") if (run_dir / "timing.json").exists() else {}
    grading = {
        "expectations": expectations,
        "summary": {
            "passed": passed_count,
            "failed": total - passed_count,
            "total": total,
            "pass_rate": round(passed_count / total, 4) if total else 0.0,
        },
        "execution_metrics": {
            "total_tool_calls": 0,
            "errors_encountered": 0,
            "output_chars": len(output),
        },
        "timing": timing,
        "claims": [],
        "user_notes_summary": {
            "uncertainties": [],
            "needs_review": ["Qualitative assertions are intentionally left for human review."],
            "workarounds": [],
        },
        "eval_feedback": {
            "overall": "Programmatic checks were graded by adapter code; qualitative assertions should be reviewed in the viewer.",
            "suggestions": [],
        },
    }
    write_json(run_dir / "grading.json", grading)
    return grading


def grade_completed_runs(evals: list[dict]) -> None:
    for item in evals:
        for config in ("with_skill", "old_skill"):
            run_dir = ITERATION / eval_dir_name(item) / config / "run-1"
            if (run_dir / "outputs" / "response.md").exists():
                grade_run(item, run_dir)


def normalize_benchmark_config_order(path: Path) -> None:
    """Make benchmark deltas read as current skill minus baseline."""
    if not path.exists():
        return
    benchmark = read_json(path)
    summary = benchmark.get("run_summary", {})
    if "with_skill" not in summary or "old_skill" not in summary:
        return

    with_eval_ids = {
        run.get("eval_id")
        for run in benchmark.get("runs", [])
        if run.get("configuration") == "with_skill"
    }
    old_eval_ids = {
        run.get("eval_id")
        for run in benchmark.get("runs", [])
        if run.get("configuration") == "old_skill"
    }
    with_summary = summary["with_skill"]
    old_summary = summary["old_skill"]
    same_eval_set = with_eval_ids == old_eval_ids
    if same_eval_set:
        delta = {
            "pass_rate": f"{with_summary['pass_rate']['mean'] - old_summary['pass_rate']['mean']:+.2f}",
            "time_seconds": f"{with_summary['time_seconds']['mean'] - old_summary['time_seconds']['mean']:+.1f}",
            "tokens": f"{with_summary['tokens']['mean'] - old_summary['tokens']['mean']:+.0f}",
        }
    else:
        delta = {
            "pass_rate": "n/a",
            "time_seconds": "n/a",
            "tokens": "n/a",
        }
        benchmark.setdefault("notes", []).append(
            "Old-skill baseline ran only on audit-human guardrails, so aggregate delta is intentionally suppressed."
        )
    benchmark["run_summary"] = {
        "with_skill": with_summary,
        "old_skill": old_summary,
        "delta": delta,
    }
    benchmark["runs"] = sorted(
        benchmark.get("runs", []),
        key=lambda run: (
            run.get("eval_id", 0),
            0 if run.get("configuration") == "with_skill" else 1,
            run.get("run_number", 0),
        ),
    )
    write_json(path, benchmark)


def is_audit_only_case(item: dict) -> bool:
    """Audit-only cases produce a comparable flag count for the corpus claim."""
    return item.get("name", "").startswith("audit-")


def audit_case_corpus_class(item: dict) -> str | None:
    name = item.get("name", "")
    if name.startswith("audit-ai-"):
        return "ai"
    if name.startswith("audit-human-"):
        return "human"
    return None


def analyze_sample_body(filepath: Path) -> dict:
    """Body-level stats for a sample: sentence/paragraph length, TTR, em-dashes, curly-quote density.
    Length-aware because long-form essays naturally have lower TTR — these are diagnostics, not gates."""
    text = filepath.read_text(encoding="utf-8")
    body = text.split("---", 2)[2] if text.startswith("---") and "---" in text[3:] else text
    sentences = [s for s in GRADE.split_sentences(body) if s.strip()]
    sentence_lens = [len(re.findall(r"\b\w+\b", s)) for s in sentences]
    paragraphs = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    para_lens = [len(re.findall(r"\b\w+\b", p)) for p in paragraphs]
    words = re.findall(r"\b\w+\b", body.lower())
    return {
        "word_count": len(words),
        "sentence_count": len(sentence_lens),
        "sentence_len_mean": statistics.mean(sentence_lens) if sentence_lens else 0.0,
        "sentence_len_stdev": statistics.stdev(sentence_lens) if len(sentence_lens) > 1 else 0.0,
        "paragraph_count": len(para_lens),
        "paragraph_len_mean": statistics.mean(para_lens) if para_lens else 0.0,
        "paragraph_len_stdev": statistics.stdev(para_lens) if len(para_lens) > 1 else 0.0,
        "type_token_ratio": (len(set(words)) / len(words)) if words else 0.0,
        "em_dashes": body.count("—"),
        "curly_quotes": sum(body.count(c) for c in "“”‘’"),
    }


def grade_sample_file(filepath: Path) -> dict:
    """Grade a sample file. Returns flag counts + body stats."""
    results = GRADE.grade_file(str(filepath))
    failures = [r for r in results if not r["passed"]]
    severity_counts: dict[str, int] = {}
    for r in failures:
        sev = r.get("severity") or "unknown"
        severity_counts[sev] = severity_counts.get(sev, 0) + 1
    signal_stacking_check = next(
        (r for r in results if r.get("text") == "overall-signal-stacking"),
        None,
    )
    signal_stacking_triggered = signal_stacking_check is not None and not signal_stacking_check.get("passed", True)
    return {
        "input_file": str(filepath.relative_to(ROOT)),
        "total_flags": len(failures),
        "severity_counts": severity_counts,
        "signal_stacking_triggered": signal_stacking_triggered,
        "body_stats": analyze_sample_body(filepath),
    }


def grade_input_file(item: dict) -> dict | None:
    """Legacy single-file grader used in earlier audit-case-driven baselines.
    Kept for backward compatibility; new code uses grade_sample_file directly."""
    files = item.get("files") or []
    if not files:
        return None
    path = resolve_eval_file(files[0])
    graded = grade_sample_file(path)
    return {
        "input_file": graded["input_file"],
        "total_flags": graded["total_flags"],
        "severity_counts": graded["severity_counts"],
        "signal_stacking_triggered": graded["signal_stacking_triggered"],
    }


def load_corpus_groups() -> dict | None:
    """Load corpus.json if present. Returns dict with group → list[Path] or None."""
    corpus_path = ROOT / "dev" / "evals" / "corpus.json"
    if not corpus_path.exists():
        return None
    data = read_json(corpus_path)
    groups_raw = data.get("groups", {})
    out: dict[str, list[Path]] = {}
    for group_name, paths in groups_raw.items():
        resolved = []
        for p in paths:
            try:
                resolved.append(resolve_eval_file(p))
            except FileNotFoundError:
                pass
        out[group_name] = resolved
    return {"groups": out, "raw": data}


def extract_audit_reported_count(grading: dict) -> int | None:
    """Pull the catalogue-pattern count out of an audit-shaped assertion's evidence."""
    target_assertions = {
        "Output references at least 5 distinct AI patterns from the catalogue",
        "Catastrophic over-flagging guard: human prose should not produce more than 12 distinct flags",
        "Known-human reflective prose should produce at most 3 flags",
        "Known-human prose should produce at most 3 flags",
    }
    for exp in grading.get("expectations", []):
        if exp.get("text") in target_assertions:
            evidence = exp.get("evidence", "")
            match = re.match(r"Referenced (\d+) catalogue pattern", evidence)
            if match:
                return int(match.group(1))
    return None


def previous_iteration_dir(current: Path) -> Path | None:
    name = current.name
    match = re.fullmatch(r"iteration-(\d+)", name)
    if not match:
        return None
    n = int(match.group(1))
    if n <= 1:
        return None
    candidate = current.parent / f"iteration-{n - 1}"
    return candidate if candidate.exists() else None


def build_performance_report(evals: list[dict], iteration_dir: Path) -> tuple[str, dict]:
    """Build performance-report.md content + a JSON sidecar for future regression checks."""
    benchmark_path = iteration_dir / "benchmark.json"
    if not benchmark_path.exists():
        return "Performance report unavailable: benchmark.json missing.\n", {}
    benchmark = read_json(benchmark_path)

    # Per-eval pass rates from with_skill runs only.
    per_eval_runs: dict[int, list[dict]] = {}
    for run in benchmark.get("runs", []):
        if run.get("configuration") != "with_skill":
            continue
        per_eval_runs.setdefault(run["eval_id"], []).append(run)
    per_eval = []
    for item in evals:
        runs = per_eval_runs.get(item["id"], [])
        if not runs:
            continue
        rates = [r["result"]["pass_rate"] for r in runs]
        per_eval.append({
            "id": item["id"],
            "name": item["name"],
            "pass_rate": sum(rates) / len(rates),
            "runs": len(runs),
        })

    # Corpus characterisation: read from corpus.json (genre-paired groups) if available;
    # fall back to audit cases in evals.json for legacy single-iteration setups.
    corpus_data = load_corpus_groups()
    if corpus_data is not None:
        corpus_rows = []
        for group_name, paths in corpus_data["groups"].items():
            for path in paths:
                graded = grade_sample_file(path)
                corpus_rows.append({
                    "type": group_name,
                    "eval_id": None,
                    "eval_name": Path(graded["input_file"]).stem,
                    **graded,
                })
    else:
        corpus_rows = []
        for item in evals:
            if not is_audit_only_case(item):
                continue
            cls = audit_case_corpus_class(item)
            if cls is None:
                continue
            graded = grade_input_file(item)
            if graded is None:
                continue
            corpus_rows.append({
                "eval_id": item["id"],
                "eval_name": item["name"],
                "type": cls,
                **graded,
            })

    def _mean(values: list[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    # Group rows by type
    group_rows: dict[str, list[dict]] = {}
    for r in corpus_rows:
        group_rows.setdefault(r["type"], []).append(r)

    def _group_means(group: list[dict]) -> dict:
        return {
            "n": len(group),
            "total": _mean([r["total_flags"] for r in group]),
            "strong": _mean([r["severity_counts"].get("strong_warning", 0) for r in group]),
            "context": _mean([r["severity_counts"].get("context_warning", 0) for r in group]),
            "sentence_len_mean": _mean([r["body_stats"]["sentence_len_mean"] for r in group if "body_stats" in r]),
            "sentence_len_stdev": _mean([r["body_stats"]["sentence_len_stdev"] for r in group if "body_stats" in r]),
            "paragraph_len_stdev": _mean([r["body_stats"]["paragraph_len_stdev"] for r in group if "body_stats" in r]),
            "type_token_ratio": _mean([r["body_stats"]["type_token_ratio"] for r in group if "body_stats" in r]),
            "word_count": _mean([r["body_stats"]["word_count"] for r in group if "body_stats" in r]),
        }

    group_summary = {name: _group_means(rows) for name, rows in group_rows.items()}

    def _gap_pct(a: float, b: float) -> str:
        if b == 0:
            return "n/a"
        return f"{(a - b) / b * 100:+.0f}%"

    # Audit fidelity: audit-reported count vs grader count. Driven by evals.json audit cases
    # (per-eval signal, not corpus-baseline signal).
    fidelity_rows = []
    for item in evals:
        if not is_audit_only_case(item):
            continue
        eval_dir = iteration_dir / f"eval-{item['id']}-{item['name']}" / "with_skill" / "run-1"
        grading_path = eval_dir / "grading.json"
        if not grading_path.exists():
            continue
        grading = read_json(grading_path)
        audit_count = extract_audit_reported_count(grading)
        # Grade the input file directly to get grader's flag count
        grader_data = grade_input_file(item)
        if grader_data is None:
            continue
        grader_count = grader_data["total_flags"]
        cls = audit_case_corpus_class(item) or "?"
        # Refine class for genre-paired cases
        if "ai-fresh" in item["name"]:
            cls = "ai_fresh"
        elif "ai-rewrite" in item["name"]:
            cls = "ai_rewrite"
        fidelity = (
            f"{audit_count / grader_count * 100:.0f}%"
            if audit_count is not None and grader_count
            else "n/a"
        )
        fidelity_rows.append({
            "eval_id": item["id"],
            "eval_name": item["name"],
            "type": cls,
            "grader_count": grader_count,
            "audit_count": audit_count,
            "fidelity_pct": fidelity,
        })

    # Regression check: compare to previous iteration's performance-report.json.
    prev_dir = previous_iteration_dir(iteration_dir)
    prev_data: dict = {}
    if prev_dir is not None:
        prev_report = prev_dir / "performance-report.json"
        if prev_report.exists():
            prev_data = read_json(prev_report)
    prev_per_eval = {row["name"]: row for row in prev_data.get("per_eval", [])}
    regression_rows = []
    for row in per_eval:
        prev = prev_per_eval.get(row["name"])
        if prev is None:
            continue
        delta = row["pass_rate"] - prev["pass_rate"]
        regression_rows.append({
            "name": row["name"],
            "prev_pass_rate": prev["pass_rate"],
            "this_pass_rate": row["pass_rate"],
            "delta": delta,
            "regressed": delta < -0.05,
        })

    # Build markdown.
    lines: list[str] = []
    lines.append(f"# Performance report — {iteration_dir.name}")
    lines.append("")
    lines.append(f"Run timestamp: {benchmark.get('metadata', {}).get('timestamp', 'unknown')}")
    lines.append(f"Evals run: {len(per_eval)}")
    overall_mean = _mean([row["pass_rate"] for row in per_eval])
    lines.append(f"Mean pass rate: {overall_mean * 100:.1f}%")
    lines.append("")
    lines.append("## Per-eval pass rates")
    lines.append("")
    lines.append("| ID | Name | Pass rate | Runs |")
    lines.append("|---|---|---|---|")
    for row in per_eval:
        lines.append(f"| {row['id']} | {row['name']} | {row['pass_rate'] * 100:.1f}% | {row['runs']} |")
    lines.append("")
    lines.append("## Human-vs-AI flag baseline")
    lines.append("")
    if corpus_data is not None:
        lines.append(
            "Grader output on the genre-paired corpus (see `dev/evals/corpus.json`). "
            "Three groups: human originals, AI fresh-writes from matched-topic prompts, "
            "and AI-rewrites of the human originals. Deterministic — independent of how the skill renders its audit."
        )
    else:
        lines.append(
            "Grader output on each audit case's input file. Deterministic corpus characterisation, "
            "independent of how the skill renders its audit."
        )
    lines.append("")
    lines.append("| Sample | Group | Total | Strong | Context | Signal stacking |")
    lines.append("|---|---|---|---|---|---|")
    for row in corpus_rows:
        sample_name = Path(row["input_file"]).stem
        sev = row["severity_counts"]
        signal_stacking = "triggered" if row["signal_stacking_triggered"] else "—"
        lines.append(
            f"| {sample_name} | {row['type']} | {row['total_flags']} "
            f"| {sev.get('strong_warning', 0)} | {sev.get('context_warning', 0)} | {signal_stacking} |"
        )
    if group_summary:
        lines.append("")
        lines.append("**Group means:**")
        lines.append("")
        lines.append("| Group | n | Total | Strong | Context |")
        lines.append("|---|---|---|---|---|")
        for name, s in group_summary.items():
            lines.append(f"| {name} | {s['n']} | {s['total']:.1f} | {s['strong']:.1f} | {s['context']:.1f} |")
        # Pairwise gaps if 'human' is present
        if 'human' in group_summary:
            human = group_summary['human']
            for other in [n for n in group_summary if n != 'human']:
                o = group_summary[other]
                lines.append(
                    f"| Gap ({other} vs human) | | {_gap_pct(o['total'], human['total'])} "
                    f"| {_gap_pct(o['strong'], human['strong'])} | {_gap_pct(o['context'], human['context'])} |"
                )
    lines.append("")
    lines.append("## Body-level statistics")
    lines.append("")
    lines.append(
        "Sentence/paragraph length variance is the strongest non-pattern signal separating humans from AI in long-form essay register "
        "(humans cluster around longer, more variable sentences; AI clusters around shorter, more uniform ones). "
        "Tracked across iterations to surface drift even when pattern flags don't move."
    )
    lines.append("")
    if group_summary:
        lines.append("| Group | n | Words | Sent. mean | Sent. stdev | Para. stdev | TTR |")
        lines.append("|---|---|---|---|---|---|---|")
        for name, s in group_summary.items():
            lines.append(
                f"| {name} | {s['n']} | {s['word_count']:.0f} | {s['sentence_len_mean']:.1f} "
                f"| {s['sentence_len_stdev']:.1f} | {s['paragraph_len_stdev']:.1f} | {s['type_token_ratio']:.2f} |"
            )
    lines.append("")
    lines.append("## Audit fidelity")
    lines.append("")
    lines.append(
        "How faithfully the skill's audit surfaces patterns the grader found. "
        "Lower fidelity means the audit is suppressing flags the grader caught."
    )
    lines.append("")
    lines.append("| Eval | Type | Grader | Audit reported | Fidelity |")
    lines.append("|---|---|---|---|---|")
    for row in fidelity_rows:
        lines.append(
            f"| {row['eval_name']} | {row['type']} | {row['grader_count']} "
            f"| {row['audit_count'] if row['audit_count'] is not None else '—'} | {row['fidelity_pct']} |"
        )
    lines.append("")
    lines.append("## Regression vs previous iteration")
    lines.append("")
    if not regression_rows:
        lines.append("_No previous iteration data available, or no comparable evals._")
    else:
        lines.append("Advisory only — flagged for review when an eval's pass rate dropped >5%.")
        lines.append("")
        lines.append("| Eval | Prev | This | Δ | Regressed? |")
        lines.append("|---|---|---|---|---|")
        for row in regression_rows:
            mark = "yes" if row["regressed"] else "—"
            lines.append(
                f"| {row['name']} | {row['prev_pass_rate'] * 100:.1f}% | {row['this_pass_rate'] * 100:.1f}% "
                f"| {row['delta'] * 100:+.1f}% | {mark} |"
            )
    lines.append("")

    structured = {
        "iteration": iteration_dir.name,
        "timestamp": benchmark.get("metadata", {}).get("timestamp"),
        "overall_mean_pass_rate": overall_mean,
        "per_eval": per_eval,
        "corpus_baseline": {
            "groups": {name: rows for name, rows in group_rows.items()},
            "group_means": group_summary,
            "pairwise_gaps": (
                {
                    other: {
                        "total_pct": _gap_pct(group_summary[other]["total"], group_summary["human"]["total"]),
                        "strong_pct": _gap_pct(group_summary[other]["strong"], group_summary["human"]["strong"]),
                        "context_pct": _gap_pct(group_summary[other]["context"], group_summary["human"]["context"]),
                    }
                    for other in group_summary if other != "human"
                }
                if "human" in group_summary else {}
            ),
        },
        "audit_fidelity": fidelity_rows,
        "regression": regression_rows,
    }
    return "\n".join(lines), structured


README_PERFORMANCE_START = "<!-- performance:start -->"
README_PERFORMANCE_END = "<!-- performance:end -->"


def update_readme_performance_block(structured: dict, readme_path: Path) -> None:
    """Replace the marker-bounded performance block in README.md with a condensed summary."""
    if not readme_path.exists() or not structured:
        return
    text = readme_path.read_text(encoding="utf-8")
    if README_PERFORMANCE_START not in text or README_PERFORMANCE_END not in text:
        return  # README hasn't opted in yet; don't touch
    iteration = structured.get("iteration", "iteration-?")
    timestamp = structured.get("timestamp", "")
    overall = structured.get("overall_mean_pass_rate", 0.0)
    pairwise = structured.get("corpus_baseline", {}).get("pairwise_gaps", {})
    regressions = sum(1 for r in structured.get("regression", []) if r.get("regressed"))

    if pairwise:
        gap_lines = [
            f"- Human-vs-{other} flag gap: total {gaps['total_pct']} / strong {gaps['strong_pct']}"
            for other, gaps in pairwise.items()
        ]
    else:
        gap_lines = ["- Comparative corpus not configured."]

    block_lines = [
        README_PERFORMANCE_START,
        f"**{iteration}** ({timestamp})",
        "",
        f"- Mean pass rate: {overall * 100:.1f}% across {len(structured.get('per_eval', []))} evals",
        *gap_lines,
        f"- Regressions vs prev iteration: {regressions}",
        "",
        f"[Full report]({_relative_report_path(readme_path, structured)})",
        README_PERFORMANCE_END,
    ]
    new_block = "\n".join(block_lines)
    pattern = re.compile(
        re.escape(README_PERFORMANCE_START) + r".*?" + re.escape(README_PERFORMANCE_END),
        re.DOTALL,
    )
    readme_path.write_text(pattern.sub(new_block, text), encoding="utf-8")


def _relative_report_path(readme_path: Path, structured: dict) -> str:
    iteration = structured.get("iteration", "iteration-?")
    return f"dev/skill-workspace/{iteration}/performance-report.md"


def prepare_workspace(evals: list[dict], reset: bool) -> None:
    if reset and ITERATION.exists():
        shutil.rmtree(ITERATION)
    ITERATION.mkdir(parents=True, exist_ok=True)
    for item in evals:
        directory = ITERATION / eval_dir_name(item)
        directory.mkdir(parents=True, exist_ok=True)
        write_json(directory / "eval_metadata.json", {
            "eval_id": item["id"],
            "eval_name": item["name"],
            "prompt": item["prompt"],
            "assertions": item.get("assertions", []),
        })


def run_iteration(
    skill_creator_path: Path,
    model: str | None,
    workers: int,
    reset: bool,
    static_viewer: bool,
    executor_name: str,
    include_old_skill: bool,
    only: set[str] | None = None,
) -> None:
    evals = read_json(EVALS_PATH)["evals"]
    if only:
        evals = [e for e in evals if e["name"] in only]
        if not evals:
            raise SystemExit(f"--only matched no evals: {sorted(only)}")
    prepare_workspace(evals, reset=reset)

    jobs = []
    for item in evals:
        base = ITERATION / eval_dir_name(item)
        jobs.append((item, "with_skill", CURRENT_SKILL, base / "with_skill" / "run-1"))
        if include_old_skill or item["name"].startswith("audit-human-"):
            jobs.append((item, "old_skill", OLD_SKILL, base / "old_skill" / "run-1"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(run_model, item, config, skill_path, run_dir, model, executor_name): (item, config, run_dir)
            for item, config, skill_path, run_dir in jobs
        }
        for future in concurrent.futures.as_completed(future_map):
            item, config, run_dir = future_map[future]
            try:
                timing = future.result()
                print(f"completed {item['name']} / {config} in {timing.get('total_duration_seconds')}s", flush=True)
                grade_run(item, run_dir)
            except Exception as exc:
                outputs = run_dir / "outputs"
                outputs.mkdir(parents=True, exist_ok=True)
                (outputs / "response.md").write_text(f"ERROR: {exc}\n", encoding="utf-8")
                write_json(run_dir / "timing.json", {
                    "total_tokens": 0,
                    "duration_ms": 0,
                    "total_duration_seconds": 0,
                })
                grade_run(item, run_dir)
                print(f"failed {item['name']} / {config}: {exc}", flush=True)

    aggregate = skill_creator_path / "scripts" / "aggregate_benchmark.py"
    py = python_for_skill_creator()
    subprocess.run([
        py,
        str(aggregate),
        str(ITERATION),
        "--skill-name",
        "humanise",
        "--skill-path",
        str(CURRENT_SKILL),
    ], cwd=skill_creator_path, check=True)
    normalize_benchmark_config_order(ITERATION / "benchmark.json")

    report_md, report_data = build_performance_report(evals, ITERATION)
    (ITERATION / "performance-report.md").write_text(report_md, encoding="utf-8")
    write_json(ITERATION / "performance-report.json", report_data)
    if only is None:
        update_readme_performance_block(report_data, ROOT / "README.md")
    print(f"performance report written to {ITERATION / 'performance-report.md'}", flush=True)

    viewer = skill_creator_path / "eval-viewer" / "generate_review.py"
    if static_viewer:
        subprocess.run([
            py,
            str(viewer),
            str(ITERATION),
            "--skill-name",
            "humanise",
            "--benchmark",
            str(ITERATION / "benchmark.json"),
            "--static",
            str(ITERATION / "review.html"),
        ], cwd=skill_creator_path, check=True)
    else:
        log_path = ITERATION / "viewer.log"
        with log_path.open("w", encoding="utf-8") as log:
            subprocess.Popen([
                py,
                str(viewer),
                str(ITERATION),
                "--skill-name",
                "humanise",
                "--benchmark",
                str(ITERATION / "benchmark.json"),
            ], cwd=skill_creator_path, stdout=log, stderr=subprocess.STDOUT)
        print(f"viewer launched; log={log_path}", flush=True)

    audit_fidelity_generator = ROOT / "dev" / "tools" / "render_audit_html.py"
    subprocess.run(
        [sys.executable, str(audit_fidelity_generator), str(ITERATION)],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    global ITERATION
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-creator-path", type=Path, required=True)
    parser.add_argument("--iteration", type=int, default=1)
    parser.add_argument("--model", default=None)
    parser.add_argument("--executor", choices=["claude", "codex"], default="claude")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--include-old-skill",
        action="store_true",
        help="Run the pre-rewrite snapshot for every eval. Default runs it only for audit-human guardrails.",
    )
    parser.add_argument("--no-reset", action="store_true")
    parser.add_argument("--static-viewer", action="store_true")
    parser.add_argument(
        "--only",
        default=None,
        help="Comma-separated list of eval names to run; skips all others.",
    )
    args = parser.parse_args()
    ITERATION = WORKSPACE / f"iteration-{args.iteration}"
    only = {n.strip() for n in args.only.split(",") if n.strip()} if args.only else None

    run_iteration(
        skill_creator_path=args.skill_creator_path.resolve(),
        model=args.model,
        workers=args.workers,
        reset=not args.no_reset,
        static_viewer=args.static_viewer,
        executor_name=args.executor,
        include_old_skill=args.include_old_skill,
        only=only,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
