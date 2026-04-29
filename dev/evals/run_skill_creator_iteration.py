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
    spec = importlib.util.spec_from_file_location("humanise_grade", ROOT / "humanise" / "grade.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load humanise/grade.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GRADE = load_grade_module()


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
        timeout=900,
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
                    int(entry.get("input_tokens", 0))
                    + int(entry.get("output_tokens", 0))
                    + int(entry.get("cache_creation_input_tokens", 0))
                    + int(entry.get("cache_read_input_tokens", 0))
                    for entry in usage
                    if isinstance(entry, dict)
                )
            elif isinstance(usage, dict):
                total_tokens = int(
                    usage.get("input_tokens", 0)
                    + usage.get("output_tokens", 0)
                    + usage.get("cache_creation_input_tokens", 0)
                    + usage.get("cache_read_input_tokens", 0)
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
        timeout=900,
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


def catalogue_hits(output: str) -> set[str]:
    lower = output.lower()
    hits = set()
    for check_id, (label, _) in GRADE.CHECK_REPORT_TEXT.items():
        terms = {label.lower(), check_id.replace("-", " ")}
        terms.add(label.lower().replace("ai", "AI").lower())
        if any(term in lower for term in terms):
            hits.add(check_id)
    return hits


def grade_one_assertion(name: str, output: str, input_text: str, generated: str) -> tuple[bool, str]:
    if name == "audit-flags-present":
        hits = catalogue_hits(output)
        return len(hits) >= 5, f"Referenced {len(hits)} catalogue pattern(s): {sorted(hits)[:10]}"
    if name == "low-flag-count-on-human-prose":
        hits = catalogue_hits(output)
        return len(hits) <= 3, f"Referenced {len(hits)} catalogue pattern(s): {sorted(hits)[:10]}"
    if name == "each-flag-has-quoted-phrase":
        result = GRADE.check_audit_shape("every-flag-block-contains-input-substring", output, input_text)
        return result["passed"], result["evidence"]
    if name == "each-flag-has-explanation":
        result = GRADE.check_audit_shape("every-flag-block-has-explanation", output, input_text)
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
) -> None:
    evals = read_json(EVALS_PATH)["evals"]
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

    grade_completed_runs(evals)

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


def main() -> int:
    global ITERATION
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill-creator-path", type=Path, required=True)
    parser.add_argument("--iteration", type=int, default=1)
    parser.add_argument("--model", default=None)
    parser.add_argument("--executor", choices=["claude", "codex"], default="claude")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--include-old-skill",
        action="store_true",
        help="Run the pre-rewrite snapshot for every eval. Default runs it only for audit-human guardrails.",
    )
    parser.add_argument("--no-reset", action="store_true")
    parser.add_argument("--static-viewer", action="store_true")
    args = parser.parse_args()
    ITERATION = WORKSPACE / f"iteration-{args.iteration}"

    run_iteration(
        skill_creator_path=args.skill_creator_path.resolve(),
        model=args.model,
        workers=args.workers,
        reset=not args.no_reset,
        static_viewer=args.static_viewer,
        executor_name=args.executor,
        include_old_skill=args.include_old_skill,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
