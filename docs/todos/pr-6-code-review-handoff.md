# PR 6 code review handoff

Date: 2026-05-01

Scope: PR #6, `docs/audit-report` into `main`

Review run artifact: `/tmp/compound-engineering/ce-code-review/20260501-112537-e249a7f5/`

## Status

The ce-code-review process found four actionable findings. Two safe-auto fixes have already been applied in the isolated review worktree at `/tmp/humanise-pr-6-review`:

1. `humanise/SKILL.md`: changed installed-skill references from `humanise/judgement.yaml` to `judgement.yaml`.
2. `humanise/grade.py`: precompiled the compound-modifier regex and skipped sentences without hyphens before scanning.

Verification already run after those fixes:

```bash
python3 dev/evals/test_grade.py
python3 dev/evals/test_judgement_yaml.py
(cd humanise && test -f grade.py && test -f judgement.yaml && test -f references/patterns.md)
```

All three checks passed.

## Remaining findings for follow-up review

### 1. Seven active checks still lack numbered catalogue mappings

Severity: P1

Location: `humanise/references/patterns.md:1058`

Reviewer source: correctness

Problem:

R16 in `docs/plans/2026-04-30-001-feat-audit-report-redesign-plan.md` says every `ALL_CHECKS` entry maps to a numbered pattern in `patterns.md` or is removed. The current PR still documents seven active checks only under `Severity for unnumbered checks`, and that section says they will be promoted or folded in follow-up work after Phase 1.

Why it matters:

Phase 1 is described as closing the catalogue/check integrity gap. If active checks remain in an orphan table, users can still be flagged by checks without a proper numbered pattern entry or explicit fold, and the README/PR description overstate the resolved map.

Suggested fix:

Promote each of these seven checks to a numbered pattern entry, or fold each into an existing numbered entry with the fold documented beside that pattern:

- `no-em-dashes`
- `no-formulaic-openers`
- `no-anaphora`
- `sentence-length-variance`
- `no-this-chains`
- `no-triad-density`
- `vocabulary-diversity`

Then tighten the meta-test so `CHECK_METADATA` / `ALL_CHECKS` cannot pass through the unnumbered-checks table alone.

Follow-up reviewer questions:

- Should this be fixed in PR #6, or should the PR description/README be narrowed so Phase 1 no longer claims the map is fully resolved?
- If folding is preferred, which existing numbered entries should own each check?
- Should the `Severity for unnumbered checks` table disappear entirely once the map is resolved?

Suggested verification:

```bash
python3 dev/evals/test_grade.py
python3 humanise/grade.py --format markdown --depth all dev/evals/samples/generated-ai/ai-08-feedback-education.md
```

### 2. All-clear fallback matches too loosely

Severity: P2

Location: `humanise/grade.py:2747`

Reviewer sources: maintainability, kieran-python

Problem:

`ALL_CLEAR_LINE_RE` is an unanchored substring regex. The audit-shape checks treat a match against that regex as enough to satisfy the programmatic block and agent-judgement block requirements for the all-clear path.

Why it matters:

A malformed response could include the phrase `Audit clean: no AI tells detected, agent reading clean` inside a longer report and still pass the all-clear shape checks, even though it is not the canonical single-line all-clear output.

Suggested fix:

Anchor `ALL_CLEAR_LINE_RE` to the full stripped line, or update the check to split non-empty lines and require one complete line to match the canonical all-clear text. Add a regression fixture where the all-clear phrase appears inside a longer malformed response and must fail.

Follow-up reviewer questions:

- Should the PR keep the Phase 1 all-clear sentence, or switch now to the Phase 3-style `X of X clear · agent reading clean · pressure: clear` shape described elsewhere in the plan?
- If Phase 1 keeps the sentence, should `test_grade.py` assert that no bold block headers appear in the all-clear case?

Suggested verification:

```bash
python3 dev/evals/test_grade.py
```

## Additional residual risks

- Audit-shape checks currently verify header presence, not that all eight `judgement.yaml` records appear in order with schema-shaped evidence.
- The full live skill iteration harness was not rerun after the review. A future reviewer may want to run `python3 dev/evals/run_skill_creator_iteration.py` on a small targeted set if runtime confidence is needed.
- `dev/evals/test_judgement_yaml.py` imports PyYAML. This passed locally, but a clean environment needs PyYAML available.

## Current working tree note

This handoff doc was written after the safe-auto fixes. At the time of writing, the worktree contains modifications to:

- `humanise/SKILL.md`
- `humanise/grade.py`
- `docs/todos/pr-6-code-review-handoff.md`
