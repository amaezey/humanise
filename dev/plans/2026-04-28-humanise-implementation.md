---
date: 2026-04-28
topic: humanise-implementation
supersedes: dev/plans/2026-04-28-humanise-refocus.md
informed-by: dev/brainstorms/2026-04-28-humanise-refocus-requirements.md
---

# Humanise: implementation plan

The brainstorm at `dev/brainstorms/2026-04-28-humanise-refocus-requirements.md` produced the user-facing model. This plan captures what's been done since, what's left, and the sequencing from here to a shippable skill backed by passing evals.

The plan is being executed via `/skill-creator:skill-creator` (chosen in lieu of `/ce-plan` because the iteration-loop framework is purpose-built for skill development with parallel with-skill / baseline runs, eval grading, and a review viewer).

---

## Status as of 2026-04-29

### Done

- **Brainstorm complete.** Requirements doc at `dev/brainstorms/2026-04-28-humanise-refocus-requirements.md`. Resolves the four-action model (Audit / Suggestions / Rewrite / Write), the depth dial scope (generative actions only), the depth scale (originally Obvious / Balanced / All; collapsed to Balanced / All on 2026-04-29 — see Decisions below), and the introduction of `references/alternatives.md`.
- **AI sample corpus expanded.** 10 new article-shaped AI samples (1100–1800 words each) added at `dev/evals/samples/generated-ai/01-10`. Topics: personal essay, cultural commentary, tech, science explainer, design craft, wellbeing, ideas/Stoicism, travel, hobby, opinion. Existing 18 shorter `ai-XX` samples retained; iteration set draws from the new 10.
- **`dev/evals/evals.json` rewritten and updated.** 8 cases covering all four actions. Case 4 (`rewrite-balanced-tech`) was originally `rewrite-obvious-tech` and got retargeted when Obvious was dropped. Old 14-case evals backed up to `evals.json.bak`.
- **`humanise/SKILL.md` rewritten and approved (2026-04-29).** Four-action model. Frontmatter description updated for richer triggering. Audit-as-default with optional Suggestions/Rewrite/Write. Depth dial (Balanced / All) only on generative actions. Audit findings shown alongside Rewrite/Suggestions output. Em-dash special-casing folded into strong warnings. References block points at `alternatives.md`.
- **`humanise/references/alternatives.md` authored.** Vetted human alternatives for the lexical patterns flagged by the grader. Used by the Suggestions action and by Rewrite/Write during the surface pass. ~350 lines.
- **`humanise/grade.py` updated.** Depth flag rename (`--mode light|medium|hard` → `--depth balanced|all`), audit-shape assertion registry (`AUDIT_SHAPE_CHECKS` with the seven shape checks the eval cases need), and a `regrade(text, depth=...)` helper for re-grading rewrite/draft outputs at a chosen depth. `dev/evals/test_grade.py`, `dev/evals/run_grade_sweep.py`, `README.md`, `dev/TESTING.md`, and the references files all updated to the new depth API. Test suite green.
- **Pre-rewrite snapshot** of `humanise/` saved at `dev/skill-workspace/skill-snapshot/` so iteration 1's baseline runs can compare against the prior version.

### Decisions made beyond the brainstorm

These were resolved during implementation and are recorded here so they're captured outside the SKILL.md and evals.json:

- **Default depth** is **Balanced**. The skill asks if it can; falls back to Balanced otherwise.
- **Depth-setting names** are ~~Obvious / Balanced / All~~ **Balanced / All** (2026-04-29 amendment). The original 3-point dial collapsed to 2 because Obvious and Balanced compiled to identical grader behaviour (both fix `hard_fail` + `strong_warning`, leave `context_warning` for disclosure). Rather than carry a user-facing distinction the grader couldn't enforce, Mae chose to drop Obvious. Balanced now subsumes the lighter pass.
- **Audit findings are always shown** in Rewrite and Suggestions output, not absorbed silently. The reasoning: a rewrite that the writer didn't see flagged isn't teaching them anything; the audit is the educational layer.
- **Suggestions sourcing splits by pattern type.** Lexical patterns (delve, hedging, em dashes, formulaic depth phrases, AI vocabulary) draw replacements from `references/alternatives.md`. Structural patterns (paragraph-length uniformity, anaphoric scaffolding, sentence-length variance) get contextual rewriting suggestions composed by the agent.
- **The 3-point depth dial** is what the user picks; the existing 3 grader severity classes (`hard_fail` / `strong_warning` / `context_warning`) are intrinsic to patterns. The two map roughly — Obvious ≈ hard_fail+strong_warning addressed; Balanced ≈ same plus context_warnings the writer would notice; All ≈ everything including subtle structural patterns — but the mapping is implementation detail the SKILL.md doesn't expose.

---

## Remaining work

> Steps 1–3 (SKILL.md review, `alternatives.md` authoring, `grade.py` updates) are all done as of 2026-04-29. See the Done section above. The next step is iteration loop 1.

### 4. Iteration loop 1 (next)

Following skill-creator's process:

- Spawn 8 with-skill subagents (one per eval case) and 8 baseline subagents (against `dev/skill-workspace/skill-snapshot/`) in parallel. Total 16 subagents.
- Each subagent saves outputs to `dev/skill-workspace/iteration-1/<eval-name>/{with_skill,old_skill}/outputs/`.
- Capture `total_tokens` and `duration_ms` per subagent into `timing.json`.
- Grade each output against its assertions; save to `grading.json` per run.
- Aggregate via `python -m scripts.aggregate_benchmark <workspace>/iteration-1 --skill-name humanise`.
- Run analyst pass on benchmark.
- Launch eval viewer (`generate_review.py`); Mae reviews qualitative outputs and benchmark side by side.
- Mae writes feedback into the viewer; submission produces `feedback.json`.

### 5. Iterate based on feedback

Read `feedback.json`. Improve SKILL.md (or alternatives.md, or grader) based on the specific problems Mae flagged on specific cases. Generalise where possible — don't overfit to the 8 cases. Re-run as iteration 2 with the same subagent pattern. Repeat until Mae says it's good or the feedback goes empty.

### 6. Description optimization

After SKILL.md is stable, run skill-creator's description-optimization loop against `dev/evals/trigger-eval.json` (already exists; ~20 trigger queries). Note: trigger-eval.json may need refreshing if any of its should-trigger queries assume the old "humanise = rewrite" framing. Spot-check before running.

### 7. Final blind eval

Once iteration plateaus, run a blind eval against the held-out samples — the 5 unused new AI samples (05-craft, 07-stoicism, 08-lisbon, 09-bread, 10-slow) plus the 18 existing `ai-XX` samples. This tests whether the skill generalises beyond the iteration corpus, per the prior plan's "blind-eval gate" requirement.

---

## Sequencing

The hard dependencies (steps 1–3 now closed; preserved here for handoff context):

```
1. SKILL.md review → redraft → approval        [done 2026-04-29]
       ↓
2. alternatives.md authoring   ──┐              [done 2026-04-29]
3. grade.py updates            ──┤              [done 2026-04-29]
                                  ├──→ 4. Iteration 1 → 5. Iterate
                                  ┘              ← we are here
6. Description optimization → 7. Final blind eval
```

---

## Open decisions

These need Mae's input but don't block the next step (drafting alternatives.md and grader updates):

- **Duplicate `grade.py` files.** Discovered during step 3 that `humanise/grade.py` and `dev/evals/grade.py` are two separate copies that drift from each other (already had a 5-line divergence before step 3 began). `dev/evals/test_grade.py` imports from the local `dev/evals/grade.py`; `dev/evals/run_grade_sweep.py` imports from `humanise/grade.py`. For step 3 they were re-synced manually, but the structural problem remains. Cleanest fix: delete `dev/evals/grade.py` and have `test_grade.py` load `humanise/grade.py` via importlib like `run_grade_sweep.py` does. Defer until after iteration 1 unless a sweep test fails because of drift.

- **Iteration set hold-out strategy.** Currently 5 of the new 10 AI samples are in the iteration set; 5 are held out for the blind eval. Should the iteration set rotate samples between iterations to avoid overfitting, or stay fixed for clean before/after deltas?
- **Blind eval pass threshold.** What's the success bar for the final blind eval — pass-rate per case, aggregate score, or qualitative read by Mae?
- **Description optimization model.** Which model ID powers the trigger-eval iteration? Default to whatever model is running this session, but Mae may want to test against a specific target.
- **`references/example.md` survival.** The current example is a Hard-mode rewrite walkthrough using the old vocabulary. Refresh, replace with a Balanced-mode walkthrough, or remove?
- **Existing `ai-XX` samples in the blind eval.** They have YAML frontmatter and are shorter (~700 words). Worth retaining as eval inputs, or do they bias the evaluation toward shorter prose?

---

## Success criteria

From the brainstorm requirements doc plus skill-creator's quality bar:

- The new SKILL.md fits comfortably under ~250 lines (currently 314 — see iteration 1 for trimming).
- A writer can read SKILL.md once and know which action they want.
- Iteration loop converges with each case at ≥80% assertion pass rate (or Mae's qualitative sign-off, whichever is the gating criterion).
- Trigger-eval test score after description optimization is ≥80% on held-out queries.
- Blind eval against held-out corpus shows the skill generalises — pass rates within 10% of iteration-set rates.
- A planner, eval reviewer, or future maintainer can pick up `dev/brainstorms/2026-04-28-humanise-refocus-requirements.md` plus this plan and the codebase, and reconstruct what was decided and why.

---

## Files touched (summary for handoff)

| Path | Status | Note |
|---|---|---|
| `dev/brainstorms/2026-04-28-humanise-refocus-requirements.md` | new | Brainstorm output. |
| `dev/plans/2026-04-28-humanise-implementation.md` | new (this file) | Implementation plan. |
| `dev/plans/2026-04-28-humanise-refocus.md` | superseded | Kept for history. |
| `humanise/SKILL.md` | rewritten and approved | Four-action model, 2-point depth dial (Balanced / All). |
| `humanise/references/alternatives.md` | new | Vetted human alternatives for lexical patterns. |
| `humanise/references/severity-detail.md` | updated | Old Light/Medium/Hard wording replaced with Balanced/All. |
| `humanise/references/patterns.md` | updated | Em-dash guidance reworded for the new depth dial. |
| `humanise/grade.py` | updated | `--depth balanced\|all` flag, `AUDIT_SHAPE_CHECKS` registry, `regrade(text, depth=...)` helper, metadata guidance reworded. |
| `dev/evals/grade.py` | re-synced from `humanise/grade.py` | Duplicate of the active grader; flagged for cleanup (see Open decisions). |
| `dev/evals/test_grade.py` | updated to depth API | All assertions green. |
| `dev/evals/run_grade_sweep.py` | updated to depth API | Emits `depth_results` keys. |
| `dev/evals/evals.json` | rewritten and updated | 8 cases; case 4 retargeted from `rewrite-obvious-tech` to `rewrite-balanced-tech`. |
| `dev/evals/evals.json.bak` | new | Backup of old 14-case evals. |
| `dev/evals/samples/generated-ai/01-10` | new | 10 new AI articles. |
| `dev/skill-workspace/skill-snapshot/` | new | Pre-rewrite skill snapshot for iteration baseline. |
| `README.md` | updated | Grader CLI usage and example output. |
| `dev/TESTING.md` | updated | Grader output description. |
