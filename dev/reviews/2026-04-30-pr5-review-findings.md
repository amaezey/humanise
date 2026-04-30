---
date: 2026-04-30
topic: pr5-review-findings
pr: https://github.com/amaezey/humanise/pull/5
pr_branch: codex/humanise-iteration-loop
review_run_id: 20260430-080004-59ee2000
artifact_path: dev/reviews/2026-04-30-pr5-artifacts/
reviewers: 14
raw_findings: 116
deduped_findings: ~60
---

# PR #5 review findings

Output of a multi-reviewer code + document review of the genre-paired comparative-report harness PR. Fourteen reviewers ran in parallel: 8 code reviewers (correctness, testing, maintainability, project-standards, kieran-python, adversarial, reliability, cli-readiness), 5 doc reviewers (coherence, feasibility, scope-guardian, product-lens, adversarial-document), 1 learnings researcher.

Per-reviewer JSON artifacts persisted to [`dev/reviews/2026-04-30-pr5-artifacts/`](2026-04-30-pr5-artifacts/) (13 files, 248KB total). Original /tmp run dir was at `/tmp/compound-engineering/ce-code-review/20260430-080004-59ee2000/` but is local-only — the persisted copy is the canonical fallback if you need a finding's full `why_it_matters` + `evidence` fields beyond what's summarised in this doc.

---

## Read this first — three strategic decisions

Everything below is consequence of these three. Decide them before working through the table.

### 1. The README narrative is logically inconsistent with itself

The README headline `+44% more strong-signal hits than the humans they're rewriting` is presented as load-bearing. The same README and research doc also conclude `the strong signals don't separate humans from AI`.

The actual data (`Hum 1.8 / AI fresh 2.0 / AI rewrite 2.6` strong-signal hits per group) is **monotonic in the expected direction**. That's signals working, not failing.

The leap from "AI rewrites trigger more flags than humans" to "patterns are register-coded, not authorship-coded" assumes the rewriter preserves human register. **If the rewriter just imports its own AI tells, the strong signals are working as designed** — and demoting them on this data destroys real signal.

Decide: (a) the signals work and the +44% headline stands (drop the reframe), or (b) the signals don't generalise to this register and the +44% comes out of the headline. Both options are defensible. Shipping both is not.

Sources: adversarial-document ADV-001, ADV-008, ADV-011 · product-lens P0-premise-pitch-survival.

### 2. The README has a new pitch but the skill still has the old one

The README opens "flags patterns in prose that often look like AI did it". `humanise/SKILL.md`, `humanise/references/severity-detail.md`, `humanise/references/alternatives.md` (16 table headers), and `dev/evals/evals.json` (15 prompt copies) all still use the old "AI tell, fix it" framing.

The audit-voice reframe ("AI tell" → "review priority — verify this is working") is a 32+ string sweep, not a one-file edit.

Decide: land the sweep, or hold the README. Current state — new pitch, old artefact — is the worst option.

Sources: product-lens P0-identity-drift-undeclared, P0-premise-pitch-survival · feasibility F3.

### 3. The plan ships architecture; the research says the substance problem is unsolved

The implementation plan executes 4-action split, depth dial collapse (3→2), `alternatives.md`, `--mode → --depth` rename, harness build. The research findings doc lists **five substance items** as queued: audit-voice reframe, demote/recategorise patterns, body-stats checks, genre-aware thresholds, mean-sentence-length as a check. None are in the executed plan.

If this is intentional sequencing (architecture first, substance next iteration) — say so in the plan. If not, add a substance tier before the next iteration.

Sources: product-lens P1-goal-work-misalignment · feasibility F6.

---

## Already applied (autofixes from this session)

- [x] `README.md:18` — `**Suggest**` → `**Suggestions**` (verb/noun consistency with the four-action vocabulary)
- [x] `dev/evals/run_skill_creator_iteration.py:157-170` — null-safe token getters (`usage.get("input_tokens", 0)` → `(usage.get("input_tokens") or 0)`); fixes crash on null token fields from `claude --output-format json`
- [x] `dev/evals/run_skill_creator_iteration.py:999` — dropped redundant trailing `grade_completed_runs(evals)` call (every job in `as_completed` already calls `grade_run` in both success and except paths)
- [x] `dev/evals/run_grade_sweep.py:54,65,80` — renamed local var `mode_counts` → `depth_check_status_counts` to match the dict key it populates (cleanup after `--mode → --depth` rename)
- [x] `dev/plans/2026-04-28-humanise-refocus.md` — added "superseded by" banner at top pointing to `humanise-implementation.md`

`test_grade.py` passes after these edits. The `grade_completed_runs` function definition is left in place — only the redundant call was removed.

---

## P0 — Must resolve before merge

| ID | Where | Issue | Reviewer(s) | Conf | Route | Fix |
|----|-------|-------|-------------|------|-------|-----|
| P0-DOC-01 | `README.md` "Why this exists" + "What we found" | Identity drift: skill changed from AI detector → writing-quality reviewer without naming the change. Pitch and findings contradict each other. | product-lens | 75 | manual → human | Pick one of (a) review tool surfacing patterns AI overuses, drop the detection framing; or (b) body-stats audit (sentence/paragraph variance) with the catalogue as diagnostic context. Rewrite opener and "Why this exists" around the choice. |
| P0-DOC-02 | `README.md` vs `humanise/SKILL.md`, `humanise/references/*`, `dev/evals/evals.json` | Pitch / artefact mismatch: README uses reframed voice, skill files still use "AI tell". 32+ string sites. | product-lens, feasibility | 100 | manual → human | Either land the sweep across all 32+ sites, or hold the README until the sweep ships. |
| P0-DOC-03 | `README.md`, `dev/research/2026-04-29-genre-paired-corpus-findings.md` | Causal claim inverted: same N=5 dataset reads as "+44% load-bearing" AND "directional, doesn't separate". Counter-hypothesis (rewriter adds its own tells, signals working as designed) unaddressed. | adversarial-document | 75 | manual → human | Either supply CIs and remove the "directional" caveat, or move +44% out of headline position and acknowledge the counter-hypothesis explicitly. |
| P0-CODE-04 | `dev/evals/test_grade.py` | Seven new `check_audit_shape_*` functions in `humanise/grade.py:4825-4928` have **zero unit tests** despite being the contract between the iteration runner and the grader. A regex regression silently mis-grades every audit eval. | testing | 100 | manual → downstream-resolver | Add expect_pass / expect_fail tests for each of: `check_audit_shape_block_precedes_rewrite_block`, `check_every_flag_block_contains_input_substring`, `check_every_flag_block_has_explanation`, `check_final_non_empty_line_ends_with_question`, `check_no_large_prose_block_not_in_input`, `check_suggestion_block_count_equals_flag_count`, `check_every_suggestion_block_has_replacement`. Each needs a passing example, a failing example, and the vacuously-true / missing-section edge cases. |
| P0-CODE-05 | `dev/evals/test_grade.py` | `regrade()` and the new depth API (`humanise/grade.py:4954-4980`) are untested but power four eval assertions in `run_skill_creator_iteration.py:347-355`. Nothing pins the new `('balanced','all')` contract. | testing | 100 | manual → downstream-resolver | Cover: `depth='balanced'` returns fewer must-fix items than `depth='all'` when only context_warnings fail; `ValueError` on unknown depth (light/medium/hard); `all_failures` vs `fails` diverge when context warnings exist; `failed_checks` at `depth='all'` equals `all_failed_checks`. Also test `action_for_depth()` and `depth_consequence()` directly. |

---

## P1 — High impact, should fix

### Document / planning

| ID | Where | Issue | Reviewer(s) | Conf | Route | Fix |
|----|-------|-------|-------------|------|-------|-----|
| P1-DOC-06 | `dev/research/2026-04-29-genre-paired-corpus-findings.md`, `README.md` | N=5 per group with no CIs. README treats it as load-bearing; doc admits it's directional. Demotions + new-signal additions both pre-stage on this corpus. | adv-doc, scope-guardian, product-lens | 100 | manual → human | Add a gate: no demotions until N≥10/group with non-overlapping CIs. Mark current findings as "provisional pending larger N" in README. Add bootstrap CIs to the findings doc. |
| P1-DOC-07 | `dev/research/2026-04-29-genre-paired-corpus-findings.md` | Severe length confound: Human 3,568w mean vs AI rewrite 1,126w. Flag-counts not length-normalised. Tucker Max prompt asked for 9,700w, model returned ~1,500w — generation failure unaddressed. | adv-doc | 75 | manual → human | Compute flags-per-1k-words alongside raw counts. Re-run Tucker Max generation or document why the underrun was accepted. Flag the markdown-headings inversion as a possible length artefact. |
| P1-DOC-08 | `dev/evals/genre-paired-personal-essay-prompts.md` | Selection bias: human corpus is 5 practitioner-bloggers (Forte, Critchlow, Tucker Max, Roberts, Sylvester-Bradley) — exactly the registers most heavily ingested by LLMs. The "humans use these patterns too" finding may be measuring corpus selection. | adv-doc | 75 | manual → human | Document inclusion criterion. Replicate on non-blogger humans (academic essay, longform journalism, personal letter) before any reframe changes generalise. |
| P1-DOC-09 | `README.md` "Where to be careful" | Honesty over-claim: README states manufactured insight is "genuinely AI-correlated" but the same PR's data shows it firing 2/5 on humans, 0/5 on AI rewrites. | product-lens, adv-doc | 100 | manual → human | Limit the "AI-correlated" claim to patterns where corpus data shows separation (em dashes do; manufactured insight does not). Carry the n=5, length-confound, single-rewriter caveats up into the README, not just "Where to be careful". |
| P1-DOC-10 | `dev/research/2026-04-29-genre-paired-corpus-findings.md` "What's queued" | Three of four "new candidate signals" (ghost-spectral, negation density, unicode flair) **already exist** as wired-in grader checks at `humanise/grade.py:1042, 1115, 1365`. Framing as "add" is wrong; the work is "tune thresholds and recategorise". Only `sentence-length-mean` is genuinely new. | feasibility | 100 | manual → human | Reframe the queued list: tune existing check thresholds vs add new check (mean sentence length). Audit each existing check's classification (severity, audit_priority) against the new evidence. |
| P1-CODE-11 | `humanise/grade.py:836` | `check_sentence_variance` uses `sd > 4` — but human stdev is 17.0 and AI is 7.3. Both clear 4.0 trivially. The findings doc itself flags this; the implementation plan doesn't pick it up. | feasibility | 100 | gated_auto → downstream-resolver | Raise threshold so AI samples (stdev ~7) fail and human samples (stdev ~17) pass. Threshold around 10 with the current corpus, but validate against larger N before locking in. |
| P1-DOC-12 | `humanise/SKILL.md`, `humanise/references/severity-detail.md`, `humanise/references/alternatives.md`, `dev/evals/evals.json` | "AI tell" hardcoded across 32+ sites. Audit-voice reframe will leak unless executed as a sweep. | feasibility | 100 | manual → downstream-resolver | Sweep all 32+ sites coherently. Define a single canonical phrasing first ("review priority", "high-correlation pattern", whichever wins) and apply uniformly. |
| P1-DOC-13 | `dev/evals/test_grade.py`, `dev/evals/evals.json`, `dev/skill-workspace/iteration-{1..4}/` | Demote/reclassify will break `test_grade.py` (hardcoded check names: `no-em-dashes`, `no-manufactured-insight`, `no-anaphora`, `no-markdown-headings`, `vocabulary-diversity`), invalidate `evals.json` flag-count thresholds, and re-baseline iteration scores. | feasibility | 100 | manual → human | Plan the demotion as a single coordinated commit: update `test_grade.py` expectations, recalibrate `evals.json` thresholds, regenerate iteration baselines, update README claims. Don't do it piecemeal. |
| P1-DOC-14 | `dev/research/2026-04-29-genre-paired-corpus-findings.md` | "Grow corpus past N=5" has no sourcing/licensing/topic-pairing strategy. Length asymmetry acknowledged as confound, not addressed. | feasibility | 75 | manual → human | Define: where humans come from (criteria, count target, sourcing), how length pairing is enforced (target word count + tolerance band), what the rewriter pool looks like (single model vs multi-model), licensing for any quoted samples. |
| P1-DOC-15 | Across `plan/research/README` | No validation strategy tied to discrimination problem. Plan's success criteria (≥80% pass, within 10% blind eval) measure pass rates, not whether the gap improved. | feasibility, product-lens | 100 | manual → human | Add a discrimination metric to the plan: e.g., "human-vs-AI mean strong-signal-hit gap, length-normalised, with bootstrap CI". Set a target. Run it as a release gate. |
| P1-DOC-16 | `dev/plans/2026-04-28-humanise-refocus.md` | (now resolved by autofix — banner added). | coherence, scope-guardian, adv-doc | 100 | safe_auto → review-fixer | **Done** in this session. |
| P1-DOC-17 | `dev/brainstorms/2026-04-28-humanise-refocus-requirements.md` (R17), `dev/plans/2026-04-28-humanise-refocus.md` Part 2 | Depth dial collapsed 3→2 mid-implementation. Brainstorm R17 still specifies three settings; refocus plan severity table still has three mode columns. | coherence F2, scope SG-04 | 100 | gated_auto → downstream-resolver | Add a brief "Status update" note at the top of the brainstorm flagging the amendment (don't rewrite — brainstorm is a protected artefact). The refocus plan banner already added covers part of this. |
| P1-DOC-18 | `dev/TESTING.md` | Describes the old 10-sample methodology (5 classics + 5 AI-slop) and 21-check grader. Fully superseded by the genre-paired corpus and 43-check grader. | coherence F8 | 75 | manual → downstream-resolver | Update to describe the current genre-paired methodology, or add a new section on the current approach with a note archiving the old methodology. |
| P1-DOC-19 | `README.md` "What's next", `dev/research/2026-04-29-genre-paired-corpus-findings.md` | Four candidate signals listed at equal weight despite ~10× evidence gap. Sentence-length-mean has a 2.3× separation; ghost/spectral/negation/unicode flair fire 2/5 in one genre, 0/5 elsewhere. | scope-guardian, adv-doc | 75 | manual → human | Split into two tiers: "implement now" (tune sentence-length-variance threshold, add mean-sentence-length check) and "revisit when N grows" (ghost-spectral, negation, unicode flair). |

### Code / runtime

| ID | Where | Issue | Reviewer(s) | Conf | Route | Fix |
|----|-------|-------|-------------|------|-------|-----|
| P1-CODE-20 | `dev/evals/run_skill_creator_iteration.py:2146-2149, 2265` | Default behaviour wipes the prior iteration directory (`reset = not args.no_reset`). No resume contract. A 45-minute run that crashes 12/18 evals in cannot recover unless the operator remembered `--no-reset`. | reliability, adversarial, cli-readiness | 100 | manual → human | Flip default: `--reset` must be explicit; default preserves. Add `--resume` to skip jobs whose `response.md` exists and is not an ERROR. Add `--only NAME[,NAME]` and `--only-failed`. Document resume semantics in `--help`. |
| P1-CODE-21 | `dev/evals/run_grade_sweep.py:86-101` | `--help` ignored — `main()` parses no args. Running `python3 run_grade_sweep.py --help` skips help, runs the full sweep, **overwrites the tracked `grade-sweep-report.json`**, prints summary JSON. Discovery action is the destructive action. | cli-readiness | 100 | manual → downstream-resolver | Add an argparse parser even with no other args: `parser = argparse.ArgumentParser(description=...); parser.parse_args()` before any work. Optionally add `--output PATH` and `--groups`. |
| P1-CODE-22 | `dev/evals/run_skill_creator_iteration.py:983-997, 1075` | `main()` always returns `0` even when `run_iteration` recorded "ERROR" rows. Silent failure for autonomous loops checking `$?`. | cli-readiness | 95 | manual → downstream-resolver | Track failed_runs in `run_iteration`. Return non-zero if any run produced ERROR. Codes: 0=ok, 1=partial, 2=usage/config, 3=fatal. Also write a top-level `run_summary.json` with `{status, failed_runs[]}` so agents don't scrape stdout. |
| P1-CODE-23 | `dev/evals/run_skill_creator_iteration.py:1387-1428` (codex run) | Codex tempfile leak: `tempfile.NamedTemporaryFile(delete=False)` is created **before** the try/finally cleanup; `subprocess.TimeoutExpired` bypasses unlink and propagates uncaught. | reliability, kieran-python, adversarial, correctness | 100 | gated_auto → review-fixer | Move the unlink into a try/finally that wraps `subprocess.run` as well, not just the read. |
| P1-CODE-24 | `dev/evals/run_skill_creator_iteration.py:2180-2201` | No SIGINT/SIGTERM handler. Ctrl-C waits for all 8 in-flight executors to hit the 900s timeout; quota burned for discarded work; orphaned subprocesses. | reliability, kieran-python, adversarial | 100 | manual → human | Migrate from `subprocess.run` inside `ThreadPoolExecutor` to `subprocess.Popen` + signal-aware supervisor. Install a SIGINT handler that terminates children, reaps, flushes outputs, then exits non-zero. |
| P1-CODE-25 | `dev/evals/run_skill_creator_iteration.py:273` | `extract_generated_text` falls back to the **entire output** when no `Rewrite`/`Draft` header is found. For rewrite evals this means the regrade scores the audit prose (with its quoted AI-tell evidence) — guaranteeing artificial failures that look like "rewrite quality regressed" when the true cause is "rewrite never produced." | correctness, testing | 100 | manual → downstream-resolver | Return `''` when both Rewrite and Draft headers are missing rather than the full output, so missing-rewrite is reported as missing rather than as failed-grading on quoted audit evidence. |
| P1-CODE-26 | `dev/evals/run_skill_creator_iteration.py:264-275` vs `humanise/grade.py` | Two parallel parsers for the `**Audit**`/`**Rewrite**`/`**Draft**`/`**Suggestions**` section contract. Iteration runner uses `re.IGNORECASE`; `grade.py` does not. They can disagree on lowercase headers. | testing | 75 | manual → downstream-resolver | Consolidate into one parser in `grade.py` and import from the iteration runner. Or add a parity test that runs both parsers against the same fixtures and asserts equal output. |
| P1-CODE-27 | `dev/evals/run_skill_creator_iteration.py:505` (`analyze_sample_body`) | Untested but feeds `performance-report.md` and `README.md`. Unhandled paths: empty body, single-sentence body (stdev `len()>1` branch), zero-word body (TTR division-by-zero), unicode-only text, frontmatter-stripping `text.split('---', 2)[2]` heuristic. | testing | 100 | manual → downstream-resolver | Add `dev/evals/test_iteration.py` (or expand `test_grade.py`) importing `analyze_sample_body` and asserting numeric outputs on fixed strings covering each edge. |

---

## P2 — Moderate

### Code reliability / correctness

| ID | Where | Issue | Reviewer(s) | Conf | Route | Fix |
|----|-------|-------|-------------|------|-------|-----|
| P2-CODE-28 | `dev/evals/run_skill_creator_iteration.py:2207-2248` | No timeout on `aggregate_benchmark` / viewer subprocess calls. A hang in aggregation hangs the runner forever **after** a 90+min eval pass — exactly where the cheap phase burns hours of completed work. | reliability | 100 | gated_auto → downstream-resolver | Add `timeout=` to all three `subprocess.run` / `Popen` calls. 60s for aggregate, 30s for viewer probe, fast-fail. |
| P2-CODE-29 | `dev/evals/run_skill_creator_iteration.py:1256-1258` (`write_json`) | Non-atomic JSON writes — `path.write_text` direct, no write-tmp + rename. Crash mid-write corrupts `benchmark.json` / `performance-report.json` / `grading.json`; next iteration breaks on `json.loads`. | reliability | 100 | gated_auto → downstream-resolver | `tmp = path.with_suffix(path.suffix + '.tmp'); tmp.write_text(...); tmp.replace(path)`. |
| P2-CODE-30 | `dev/evals/run_skill_creator_iteration.py:567` (`load_corpus_groups`), `:966` (`read_json(EVALS_PATH)`) | No structural validation of `corpus.json` / `evals.json`. `load_corpus_groups` silently swallows `FileNotFoundError` per path. Typo'd group names → silent group shrinkage; missing assertion `name` → `KeyError` mid-run after expensive subprocess calls. | testing, adversarial, kieran-python | 100 | gated_auto → downstream-resolver | Add `validate_corpus()` / `validate_evals()` called early. Assert: groups dict has `human`/`ai_fresh`/`ai_rewrite`, every path resolves via `resolve_eval_file`, every eval has int `id` and string `name`, every assertion has `name`+`type`+`description`. Add a unit test that loads the live JSON and asserts validators pass. |
| P2-CODE-31 | `dev/evals/run_skill_creator_iteration.py:1277-1278, 2151-2158` | Path traversal via `evals.json` `item.name`. If name contains `../`, output paths escape the workspace. | adversarial | 80 | gated_auto → downstream-resolver | Sanitize via `pathlib.PurePath` parts check, or use a `slugify` step that strips path separators. |
| P2-CODE-32 | `dev/evals/run_skill_creator_iteration.py:1294-1316` | Argv length overflow with corpus > ~1MB: a single sample exceeding the OS arg limit makes `claude`/`codex` invocation fail with `E2BIG`. | adversarial | 85 | gated_auto → downstream-resolver | Detect input size; if over a threshold, write to a tempfile and pass via stdin or `--input-file` instead of inlining into argv. |
| P2-CODE-33 | `dev/evals/run_skill_creator_iteration.py:1335-1338` | Stripping `ANTHROPIC_API_KEY` from claude env breaks any environment authenticating via API key vs subscription. | adversarial | 70 | manual → human | Decide: is API-key auth supported, or only subscription? Document the choice. If supported, don't strip the key. |
| P2-CODE-34 | `dev/evals/run_skill_creator_iteration.py:1319-1428` | No retries on subprocess executor calls. Single transient failure = permanent eval failure. | reliability | 90 | gated_auto → downstream-resolver | Wrap `run_claude` / `run_codex` in a retry decorator: 2 retries with exponential backoff for non-zero exit / timeout, no retry for 4xx-style "your prompt is bad". |
| P2-CODE-35 | `dev/evals/run_skill_creator_iteration.py:2161-2179` | No health check on `claude`/`codex` binary before spawning N workers. Missing binary fails 36 jobs with cryptic `[Errno 2]` instead of one clear error. | reliability | 90 | gated_auto → downstream-resolver | `if not shutil.which(executor_name): sys.exit(f"executor {executor_name!r} not found in PATH")` early in `main()`. |
| P2-CODE-36 | Across `humanise/grade.py`, `dev/skill-workspace/iteration-*/` | Determinism violation across iterations: changing thresholds in `humanise/grade.py` makes "iteration N" corpus baseline incomparable to "iteration N-1" — even though the PR claims they're identical. | adversarial, feasibility | 75 | advisory → human | Stamp `grader_version` (commit SHA + threshold-set hash) into each saved iteration's `grading.json` so cross-iteration comparisons can detect drift. |
| P2-CODE-37 | `dev/evals/run_skill_creator_iteration.py:1051` | Required `--skill-creator-path` has no help text, no default, no env var fallback. First-time invocation in a fresh checkout has no path forward. | cli-readiness | 100 | manual → downstream-resolver | `help='Path to the skill-creator repo. Defaults to $SKILL_CREATOR_PATH or ../skill-creator.'` Add default via `os.environ` + `ROOT.parent` fallback; drop `required=True`; validate existence early. Add example to README and `parser.epilog`. |
| P2-CODE-38 | `dev/evals/run_skill_creator_iteration.py:1051-1062` | Most argparse flags carry no `help=` text (`--iteration`, `--no-reset`, `--static-viewer`, `--workers`, `--model`). | cli-readiness | 100 | manual → downstream-resolver | Add `help=` to every flag. Particularly: `--iteration` ('Workspace dir N; uses dev/skill-workspace/iteration-N. Default 1.'), `--no-reset` ('Preserve existing dir contents to resume after interruption.'), `--static-viewer` ('Generate review.html instead of launching the live viewer.'), `--workers` ('Concurrent eval runs; high values may hit rate limits.'). |
| P2-CODE-39 | `dev/evals/run_skill_creator_iteration.py` — print() throughout | Progress is prose stdout; no `--format jsonl`, no stderr/stdout discipline. Agents wanting structured progress have to regex prose. | cli-readiness | 95 | manual → downstream-resolver | Send progress to stderr; reserve stdout for machine output. Add `--format {text,jsonl}`; emit per-event `{event, eval, config, duration_s, status}`. Default `--format=auto` (jsonl when stdout is not a TTY). |
| P2-CODE-40 | `dev/evals/run_skill_creator_iteration.py:31, 1049, 1064` | Module-level mutable global `ITERATION` rebound in `main()`; ~12 helpers read it directly. Action-at-a-distance hides bugs once a second entry point exists. | kieran-python, maintainability | 100 | manual → downstream-resolver | Compute `iteration_dir` from args; thread explicitly through `prepare_workspace` / `run_iteration` / `grade_completed_runs`. Remove the global mutation. |
| P2-CODE-41 | `dev/evals/run_skill_creator_iteration.py:299-371` (`grade_one_assertion`) | 70-line if/elif registry begging to be a dispatch dict. ~25 `if name == ...` branches with alias sets like `{'no-em-dashes-in-rewrite','no-em-dashes'}`. | kieran-python | 75 | manual → downstream-resolver | Define `ASSERTION_HANDLERS: dict[str, Callable]`; aliases become two keys pointing to the same callable. Surface the supported names; decouple from `evals.json` drift. |
| P2-CODE-42 | `dev/evals/run_skill_creator_iteration.py:615-890` (`build_performance_report`) | 280-line do-everything mixing data assembly + Markdown rendering. Borderline today; adding a fifth section should trigger split. | kieran-python | 75 | manual → downstream-resolver | Extract data assembly into `_compute_performance_data()` returning a dict; pass to `_render_performance_markdown(data)`. |

### Documentation / orphans

| ID | Where | Issue | Reviewer(s) | Conf | Route | Fix |
|----|-------|-------|-------------|------|-------|-----|
| P2-DOC-43 | `humanise/references/example.md` (65 LOC), `humanise/references/severity-detail.md` (59 LOC) | Added but never linked from `SKILL.md` or any other reference. | maintainability | 100 | manual → human | Either link both from `SKILL.md`, or delete. |
| P2-DOC-44 | `humanise/examples ai.txt` | 575-line / ~100KB unreferenced text file with **a space in its filename**. Ships inside the published skill directory. | maintainability, correctness | 100 | manual → human | Move to `dev/evals/manual-pastes/` or delete. Rename to remove the space if kept. |

---

## P3 — Polish

Small fixes; batch in a follow-up PR. Each row is self-contained.

| ID | Where | Issue | Source | Fix |
|----|-------|-------|--------|-----|
| P3-CODE-45 | `dev/evals/run_skill_creator_iteration.py:937` | `_relative_report_path` takes unused `readme_path` parameter. | maintainability | Drop the parameter. (Held for review — could break callers; verify before applying.) |
| P3-CODE-46 | `dev/evals/run_skill_creator_iteration.py:551, 663, 714` | `grade_input_file` marked "legacy" in its own docstring but still has live callers. | maintainability | Either rewrite the docstring to describe its actual current role, or migrate callers to `grade_sample_file` and delete. |
| P3-CODE-47 | `dev/evals/run_skill_creator_iteration.py:293` | `catalogue_hits` third `terms.add` line is a no-op: `label.lower().replace('ai','AI').lower()` re-lowers what it just unlowered. | correctness | Drop the line, or compute a real case variant. |
| P3-CODE-48 | `dev/evals/run_skill_creator_iteration.py:59` | Hard-coded `/opt/homebrew/bin/python3.12` first-probe is macOS-specific magic. | kieran-python | Move probe order into a documented helper; allow override via `$SKILL_CREATOR_PYTHON`. |
| P3-CODE-49 | `dev/evals/run_skill_creator_iteration.py:36-45` | Module-loaded `grade.py` at import time is a startup-cost trap and a test-isolation problem (singleton state leaks across runs in same process). | kieran-python, adversarial | Lazy-load `GRADE` on first use; or refactor to import as a module rather than via `importlib.spec_from_file_location`. |
| P3-CODE-50 | `dev/evals/run_skill_creator_iteration.py:392-395, 987-997` | Broad `except Exception` at the assertion level loses traceback context; masks grader bugs as eval failures. | kieran-python, reliability | `logging.exception(...)` instead of `f"ERROR: {exc}"`. |
| P3-CODE-51 | `dev/evals/run_skill_creator_iteration.py:1036-1045` (detached viewer Popen) | Result discarded; no PID file, no shutdown story. Repeat invocations stack viewer processes. | reliability, kieran-python | Write a PID file; detect existing process at startup; provide `--stop-viewer` flag. |
| P3-CODE-52 | `dev/evals/run_skill_creator_iteration.py:147-176` | Token-counting branch only catches `JSONDecodeError`; `TypeError` on non-numeric values from a future schema would escape. | kieran-python | Wrap the addition in a `try/except (TypeError, ValueError): pass` — schema-drift-tolerant. |
| P3-CODE-53 | `dev/evals/run_skill_creator_iteration.py:510, 1495` | Adapter pokes `GRADE.split_sentences`, `GRADE.CHECK_REPORT_TEXT`, `GRADE.regrade` etc. No `__all__` in `grade.py` — implicit, rename-fragile boundary. | kieran-python | Define `__all__` in `humanise/grade.py` listing the exported names; or import the named functions explicitly at the top of the iteration runner. |
| P3-CODE-54 | `dev/evals/run_skill_creator_iteration.py:299-371` | Magic numbers (`>=5, <=3, <=12, 0.45, >35, 213-288`) without named constants. | kieran-python, maintainability | Lift to module-level constants with one-line provenance comments (which corpus run / which eval established each threshold). |
| P3-CODE-55 | `dev/evals/test_grade.py:1167, 1185` | Hard-coded `'43 checks'` count and `'len(_markdown_rows) != 44'`. Breaks the moment a check is added. | testing | Replace with `len(_full_table_report["all_checks"]) != len(ALL_CHECKS)` and `len(_markdown_rows) != len(ALL_CHECKS) + 1`. |
| P3-CODE-56 | `dev/evals/test_grade.py:1186` | Test asserts on literal `'\\| ... \\| All action \\|'` markdown header — couples to exact `depth.title()` capitalisation. | testing | Assert on parsed table structure (header contains `Check`, `Status`, `depth_key.title()`) rather than literal string. |
| P3-CODE-57 | `dev/evals/run_skill_creator_iteration.py:90` (`build_prompt`) | Embeds full input file contents into prompt; large samples may push past context limits. (Conf 25 — speculative.) | correctness | No action for current corpus sizes; reconsider if essays grow past ~50KB. |
| P3-CODE-58 | `humanise/grade.py:2679` (`regrade(text='')`) | Would still execute every check on empty string; `rewrite-passes-*` could give misleading "pass" on truly-empty rewrite blocks. | correctness | Add an empty-text guard to `regrade()`, or document the `rewrite-produced` precondition. |
| P3-CODE-59 | `dev/evals/run_skill_creator_iteration.py` `**Rewrite**` vs `## Rewrite` | Section parsing brittleness — model output using `## Rewrite` heading silently bypasses `extract_generated_text`. | adversarial | Accept both heading styles in the section parser, or document the contract in `humanise/SKILL.md`'s output template. |
| P3-CODE-60 | `dev/evals/run_skill_creator_iteration.py:1339-1346, 1405-1411, 2180` | Subprocess `capture_output=True` buffers fully in memory; 8 workers × `claude --verbose` JSON could pressure memory on long outputs. | adversarial | Stream stdout to disk (`stdout=open(...)`) for large outputs; or cap captured size. |
| P3-DOC-61 | `dev/research/2026-04-29-genre-paired-corpus-findings.md` "What's queued" | Genre-aware threshold system queued before corpus is large enough to justify it. Listed as action item alongside an explicit corpus caveat ("n=5 per group. Findings are directional"). | scope-guardian | Move to "future research directions" gated explicitly on N≥10 corpus confirmation. |
| P3-DOC-62 | `dev/plans/2026-04-28-humanise-implementation.md` | Reports 86.6% mean pass rate against per-case ≥80% bar with "qualitative sign-off, whichever is the gating criterion" escape hatch. | adv-doc | Drop the qualitative escape hatch or make it falsifiable (e.g., specific named reviewer's signoff with checklist). |
| P3-DOC-63 | `dev/brainstorms/2026-04-28-humanise-refocus-requirements.md`, `dev/plans/2026-04-28-humanise-implementation.md` "Open decisions" | Implementation plan's "Open decisions" says "none currently open" while the brainstorm's "Deferred to Planning" list has 8 items, not all traceable to resolutions. Headless / programmatic invocation contract is one. | scope-guardian, adv-doc | Add a Resolved/Deferred table to the implementation plan with one row per brainstorm-deferred item. |
| P3-DOC-64 | `dev/research/2026-04-29-genre-paired-corpus-findings.md` "Mae's reframe" | Reframe is rationalisation, not progress, until a behaviour change is specified — "Two audiences, two rules" keeps rewrite policy identical and softens audit voice with no metric for whether the reframe improved anything. | adv-doc | Define a measurable success criterion for the reframe before shipping. |

---

## Pre-existing (do not block this PR)

| ID | Where | Issue | Source | Fix |
|----|-------|-------|--------|-----|
| PRE-01 | `dev/evals/evals.json.bak` | Backup file checked in. | correctness, maintainability | Delete; rely on git history; add `*.bak` to `.gitignore`. |

---

## Suggested fix order

1. **Strategic decisions** (the three in "Read this first"). Unblocks everything else.
2. **P0 testing gaps** (P0-CODE-04, P0-CODE-05). Blocking because they're the contract between the iteration runner and the grader.
3. **Doc back-annotation** (P1-DOC-17, P1-DOC-18). Mostly mechanical once #1 is decided.
4. **Harness reliability cluster** (P1-CODE-20, -23, -24, -25, -26 + P2-CODE-28, -29, -30, -34, -35). Default-wipes, codex tempfile leak, Ctrl-C handling, missing timeouts, atomic writes, fallback-to-full-output, parallel parsers.
5. **CLI-readiness cluster** (P1-CODE-21, -22 + P2-CODE-37, -38, -39). Sharp footguns for autonomous loops.
6. **Orphan files** (P2-DOC-43, P2-DOC-44). Link or delete.
7. **P3 polish.** Batch in a follow-up PR.

---

## Decoupling option

The corpus-quality questions (length confound, selection bias, N=5, counter-hypothesis, +44% inflation) are **P1-blocking for the README claims, not for the code that ships the harness.**

Decoupling the harness merge from the README narrative is viable: ship the infrastructure, hold the README until iteration 5+ corpus growth gives load-bearing numbers. The plan even hints at this — N≥10 per group is in the queued list.

If you take this path:
1. Revert / hold the README rewrite portion of this PR
2. Land the harness, corpus, body-stats, planning docs
3. Run iteration 5+ with N≥10 per group
4. Land the README rewrite as a separate PR with bootstrap CIs and the strategic decisions made

---

## Cross-reviewer agreement (promotions to anchor 100)

These findings had 2+ reviewers independently flag the same issue and were promoted from anchor 75 → 100 during synthesis:

- Codex tempfile leak on `TimeoutExpired` — 4 reviewers (reliability, kieran-python, adversarial, correctness)
- Default-wipes-prior-iteration — 4 reviewers (reliability, adversarial, cli-readiness ×2)
- Ctrl-C orphans subprocesses — 3 reviewers (reliability, kieran-python, adversarial)
- Section parsing brittleness — 3 reviewers (correctness, testing, adversarial)
- Two plans no superseded marker — 3 reviewers (coherence, scope-guardian, adv-doc)
- Successful runs graded twice — 3 reviewers (correctness, reliability, adversarial)
- Pitch / artefact mismatch — 2 reviewers (product-lens, feasibility)
- "AI tell" hardcoded across files — 2 reviewers (product-lens, feasibility)
- N=5 with no CIs — 3 reviewers (adv-doc, scope-guardian, product-lens)
- Mutable global ITERATION — 2 reviewers (kieran-python, maintainability)
- Manufactured-insight overclaim — 2 reviewers (product-lens, adv-doc)
- Validation strategy gap — 2 reviewers (feasibility, product-lens)
- Determinism violation — 2 reviewers (adversarial, feasibility)
- Magic numbers / threshold provenance — 2 reviewers (kieran-python, maintainability)

---

## Reviewer roster + artifact paths

All artifacts persisted to [`dev/reviews/2026-04-30-pr5-artifacts/`](2026-04-30-pr5-artifacts/). Each file contains the reviewer's full analysis including `why_it_matters` and `evidence` per finding (detail-tier fields not surfaced in this summary doc).

| Reviewer | Findings | File |
|----------|----------|------|
| correctness | 10 | [`correctness.json`](2026-04-30-pr5-artifacts/correctness.json) |
| testing | 8 | [`testing.json`](2026-04-30-pr5-artifacts/testing.json) |
| maintainability | 8 | [`maintainability.json`](2026-04-30-pr5-artifacts/maintainability.json) |
| project-standards | 0 | [`project-standards.json`](2026-04-30-pr5-artifacts/project-standards.json) |
| kieran-python | 15 | [`kieran-python.json`](2026-04-30-pr5-artifacts/kieran-python.json) |
| adversarial | 14 | [`adversarial.json`](2026-04-30-pr5-artifacts/adversarial.json) |
| reliability | 11 | [`reliability.json`](2026-04-30-pr5-artifacts/reliability.json) |
| cli-readiness | 7 | [`cli-readiness.json`](2026-04-30-pr5-artifacts/cli-readiness.json) |
| coherence | 10 | [`coherence.json`](2026-04-30-pr5-artifacts/coherence.json) |
| feasibility | 10 | [`feasibility.json`](2026-04-30-pr5-artifacts/feasibility.json) |
| scope-guardian | 5 | [`scope-guardian.json`](2026-04-30-pr5-artifacts/scope-guardian.json) |
| product-lens | 7 | [`product-lens.json`](2026-04-30-pr5-artifacts/product-lens.json) |
| adversarial-document | 11 | [`adversarial-document.json`](2026-04-30-pr5-artifacts/adversarial-document.json) |
| learnings-researcher | n/a | (free-form notes — not on disk; key correction folded into "Already applied") |

Reviewers not run and why:
- `security`, `performance`, `api-contract`, `data-migrations` — non-applicable scope
- `previous-comments` — PR has zero existing review comments
- `kieran-typescript`, `kieran-rails`, `dhh-rails`, `swift-ios`, `julik-frontend-races` — no matching files
- `design-lens`, `security-lens` — no UI / security implications

`project-standards` returned zero findings — no `CLAUDE.md` / `AGENTS.md` exists in the repo to audit against. Adding a top-level `AGENTS.md` capturing your conventions (skill frontmatter, `humanise/references/` vs `dev/`, no-spaces-in-filenames, where corpus and eval artefacts live, protected-artifact paths) would let `project-standards` run productively on future PRs.

---

## Residual risks worth flagging

- `claude` is invoked with `--allowedTools Read,Bash` and `--add-dir ROOT`. **A prompt-injection in a corpus file could make the executor run shell commands** with the user's permissions. (adversarial residual)
- `update_readme_performance_block` rewrites a marker-bounded section of the published README on every run. Any harness data-quality bug auto-publishes to the user-facing pitch. (adversarial residual)
- `humanise/grade.py` is loaded once as a module singleton (`GRADE`); state mutation in tests/dev tools leaks across runs in the same process.
- `ThreadPoolExecutor` + `subprocess.run` is the wrong primitive for cancellable workers; cleanup hazards will keep accumulating until migrated to `Popen` + signal-aware supervisor.
- Once research findings live in the user-facing README, every iteration's findings become a candidate for inclusion — README will grow rather than stay focused on the writer's call-to-action.

---

## What changed in this session

- Five `safe_auto` autofixes applied (see "Already applied" above).
- `dev/evals/test_grade.py` re-run: ALL PASSED.
- This findings doc written.

Pick up from "Read this first" in the next session.
