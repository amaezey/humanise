# Testing methodology

## Approach

The current testing regime has six layers. Each one catches a different class of problem.

**1. Genre-paired comparative corpus.** Five matched topics, three groups per topic: human originals, AI fresh-writes from matched briefs, AI rewrites of the same human originals. Same topics across all three lets the grader's flag densities be compared in matched register — the load-bearing claim is that humans should trip fewer flags than AI on the same topic. Lives in `dev/evals/corpus.json`.

**2. 18-eval harness.** Runs each eval against the current skill *and* a frozen `dev/skill-workspace/skill-snapshot/` (the pre-rewrite version) so every iteration is a controlled before/after. Driven by `dev/evals/run_skill_creator_iteration.py`. Outputs per-assertion grading, an aggregate benchmark, and an audit-fidelity report.

**3. Audit-fidelity contract check.** Confirms the audit's structured JSON output matches the schema in `human-eyes/scripts/contracts/audit-format-v1.json`. Catches drift in the contract that the human-readable preview can hide.

**4. Diff-renders regression gate.** `dev/evals/diff_renders.py` re-runs `grade.py` over a fixed corpus and pins every field of the output against a captured baseline. Any change to grader behaviour shows up as an explicit JSON diff. Used to lock down no-op refactors.

```bash
python3 dev/evals/diff_renders.py --verify
python3 dev/evals/diff_renders.py --capture   # only when grader output legitimately changes
```

**5. Programmatic grading.** 43-check `human-eyes/scripts/grade.py` covering 38 patterns plus structural tells. Severity metadata so failures interpret by mode (hard fail / strong / context warning), not as one flat category. Generated-AI fixtures should fail multiple checks. Human-sourced fixtures often trip context warnings (curly quotes, staccato, anaphora, rhetorical questions, triad density) — they're style references, not "must pass" fixtures.

```bash
python3 human-eyes/scripts/grade.py path/to/text.md
python3 human-eyes/scripts/grade.py path/to/text.md no-em-dashes,no-manufactured-insight
python3 dev/evals/run_grade_sweep.py
```

Outputs JSON with pass/fail, evidence, severity, depth guidance per check, and `depth_results` showing whether the text passes Balanced and All criteria.

**6. Self-tests for the grader.** `dev/evals/test_grade.py` asserts each check catches known-bad and passes known-clean text — the regression gate for the grader's regex layer. Run after any change to `grade.py` to prevent silent regex breakage.

```bash
python3 dev/evals/test_grade.py
```

## Results

Current performance lives in the auto-rewritten block in `README.md` and in full at `dev/skill-workspace/latest-performance-report.md`. The harness writes a dated archive entry to `dev/skill-workspace/reports/` on every run.

## Key findings

- **Pre-check/post-check loop is the breakthrough.** Without the script loop, models miss patterns they've been told to catch. With the loop in the workflow, they don't.
- **Experiential vacancy was the most useful conceptual addition.** Every agent used it as their primary diagnostic: "this essay contains no named people, no real places, no specific memories." That framing pushes toward replacement with something specific, not just removal of bad patterns.
- **Vague prohibition doesn't work on smart models.** Saying "no manufactured insight" wasn't enough. The model rationalised exceptions for humorous tone. Explicit examples and "non-negotiable even in casual writing" closed the loophole.
- **Claude doesn't produce the same slop as ChatGPT.** The sensory/atmospheric patterns (ghost language, quietness, synesthesia) rarely appeared in Claude output even with lazy prompts. The skill's new patterns are more relevant to ChatGPT-generated text.
- **Programmatic grading catches many surface and structural tells, but not all of them.** 43 script checks cover 38 patterns. Forced synesthesia, generic metaphors, tonal uniformity, faux specificity, neutrality collapse, citation validity, and fiction pacing still need human judgment in the self-audit step.

## Open questions

Hypotheses still on the table — register-distance scoring with calibrated densities, the comparison-engine product reframe, and others — are tracked in [`hypotheses.md`](hypotheses.md). Each entry stays open until tested or replaced by something cheaper or stronger.
