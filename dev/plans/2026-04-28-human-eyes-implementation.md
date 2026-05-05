---
date: 2026-04-28
topic: human-eyes-implementation
supersedes: dev/plans/2026-04-28-human-eyes-refocus.md
informed-by: dev/brainstorms/2026-04-28-human-eyes-refocus-requirements.md
---

# Human-eyes: implementation plan

The brainstorm at `dev/brainstorms/2026-04-28-human-eyes-refocus-requirements.md` produced the user-facing model. This plan captures what's been done since, what's left, and the sequencing from here to a shippable skill backed by passing evals.

The plan is being executed via `/skill-creator:skill-creator` (chosen in lieu of `/ce-plan` because the iteration-loop framework is purpose-built for skill development with parallel with-skill / baseline runs, eval grading, and a review viewer).

---

## Status as of 2026-04-29

### Done

- **Brainstorm complete.** Requirements doc at `dev/brainstorms/2026-04-28-human-eyes-refocus-requirements.md`. Resolves the four-action model (Audit / Suggestions / Rewrite / Write), the depth dial scope (generative actions only), the depth scale (originally Obvious / Balanced / All; collapsed to Balanced / All on 2026-04-29 — see Decisions below), and the introduction of `references/alternatives.md`.
- **AI sample corpus expanded.** 10 new article-shaped AI samples (1100–1800 words each) added at `dev/evals/samples/generated-ai/01-10`. Topics: personal essay, cultural commentary, tech, science explainer, design craft, wellbeing, ideas/Stoicism, travel, hobby, opinion. Existing 18 shorter `ai-XX` samples retained; iteration set draws from the new 10.
- **`dev/evals/evals.json` rewritten and updated.** 8 cases covering all four actions. Case 4 (`rewrite-balanced-tech`) was originally `rewrite-obvious-tech` and got retargeted when Obvious was dropped. Old 14-case evals backed up to `evals.json.bak`.
- **`human-eyes/SKILL.md` rewritten and approved (2026-04-29).** Four-action model. Frontmatter description updated for richer triggering. Audit-as-default with optional Suggestions/Rewrite/Write. Depth dial (Balanced / All) only on generative actions. Audit findings shown alongside Rewrite/Suggestions output. Em-dash special-casing folded into strong warnings. References block points at `alternatives.md`.
- **`human-eyes/references/alternatives.md` authored.** Vetted human alternatives for the lexical patterns flagged by the grader. Used by the Suggestions action and by Rewrite/Write during the surface pass. ~350 lines.
- **`human-eyes/grade.py` updated.** Depth flag rename (`--mode light|medium|hard` → `--depth balanced|all`), audit-shape assertion registry (`AUDIT_SHAPE_CHECKS` with the seven shape checks the eval cases need), and a `regrade(text, depth=...)` helper for re-grading rewrite/draft outputs at a chosen depth. `dev/evals/test_grade.py`, `dev/evals/run_grade_sweep.py`, `README.md`, `dev/TESTING.md`, and the references files all updated to the new depth API. Test suite green.
- **Pre-rewrite snapshot** of `human-eyes/` saved at `dev/skill-workspace/skill-snapshot/` so iteration 1's baseline runs can compare against the prior version.
- **Iteration loop 1 completed.** `dev/skill-workspace/iteration-1/` contains the first skill-creator-style benchmark run: 8 current-skill outputs plus 8 old-skill baseline outputs, graded and aggregated. Current skill scored 88.4% mean pass rate against 77.1% for the old snapshot. The strongest remaining failures were the All-depth science rewrite's structural variance and the weak human guardrail fixtures.
- **Iteration loop 2 completed after focused fixes.** `dev/skill-workspace/iteration-2/` contains the rerun after retargeting the two human guardrails to real repo corpus samples, adding `human-eyes/references/process.md`, tightening Rewrite/Write re-grade instructions, and improving the benchmark harness. Iteration 2 ran the current skill on all 8 evals and the old snapshot only on the two human guardrails. Current skill scored 86.6% mean pass rate; old-skill aggregate is partial-baseline context only. Balanced tech now passes 7/7. Remaining failures are mostly the All-depth science rewrite's structural variance, anaphora, and triad density, plus strict flag-count expectations on expressive human prose.

### Decisions made beyond the brainstorm

These were resolved during implementation and are recorded here so they're captured outside the SKILL.md and evals.json:

- **Default depth** is **Balanced**. The skill asks if it can; falls back to Balanced otherwise.
- **Depth-setting names** are ~~Obvious / Balanced / All~~ **Balanced / All** (2026-04-29 amendment). The original 3-point dial collapsed to 2 because Obvious and Balanced compiled to identical grader behaviour (both fix `hard_fail` + `strong_warning`, leave `context_warning` for disclosure). Rather than carry a user-facing distinction the grader couldn't enforce, Mae chose to drop Obvious. Balanced now subsumes the lighter pass.
- **Audit findings are always shown** in Rewrite and Suggestions output, not absorbed silently. The reasoning: a rewrite that the writer didn't see flagged isn't teaching them anything; the audit is the educational layer.
- **Suggestions sourcing splits by pattern type.** Lexical patterns (delve, hedging, em dashes, formulaic depth phrases, AI vocabulary) draw replacements from `references/alternatives.md`. Structural patterns (paragraph-length uniformity, anaphoric scaffolding, sentence-length variance) get contextual rewriting suggestions composed by the agent.
- **The 3-point depth dial** is what the user picks; the existing 3 grader severity classes (`hard_fail` / `strong_warning` / `context_warning`) are intrinsic to patterns. The two map roughly — Obvious ≈ hard_fail+strong_warning addressed; Balanced ≈ same plus context_warnings the writer would notice; All ≈ everything including subtle structural patterns — but the mapping is implementation detail the SKILL.md doesn't expose.
- **Old-skill baselines are no longer needed for every eval after the first full comparison.** The harness now defaults to current-skill runs for every eval and old-skill runs only for `audit-human-*` guardrails. Use `--include-old-skill` when a full baseline comparison is intentionally needed.

---

## Remaining work

> Steps 1–4 are now done as of 2026-04-29. Iteration loop 2 is the latest completed benchmark. The next step is to iterate on the remaining failures from iteration 2.

### 4. Iteration loop 1 and 2 (done)

Following skill-creator's process, with a local adapter because the exact skill-creator execution harness was not available in this Codex environment:

- Iteration 1 saved outputs to `dev/skill-workspace/iteration-1/<eval-name>/{with_skill,old_skill}/run-1/outputs/`.
- Iteration 1 captured timing, graded each run into `grading.json`, aggregated benchmark data, and generated review artifacts.
- Iteration 2 saved outputs to `dev/skill-workspace/iteration-2/<eval-name>/...`.
- Iteration 2 used the faster harness defaults: 8 workers, incremental grading, current-skill runs for all evals, and old-skill runs only for human guardrails.
- Static review viewers were generated at `dev/skill-workspace/iteration-1/review.html` and `dev/skill-workspace/iteration-2/review.html`.

### 5. Iterate based on iteration-2 results (next)

Use `dev/skill-workspace/iteration-2/benchmark.json` and the review viewer outputs to improve the remaining failure areas. Generalise where possible — don't overfit to the 8 cases.

Current candidate fixes:

- Revisit the `rewrite-all-science` All-depth process. It still fails stricter structural-variance expectations and re-grade checks (`no-anaphora`, `no-triad-density`).
- Decide whether the `<=3` flag-count assertion is too strict for expressive human prose, or whether audit output should better classify intentional human rhetorical devices as context rather than flags.
- Review `suggestions-ai-wellbeing`, where one current-skill run failed the quote-anchoring assertion for flagged patterns.
- Rerun as iteration 3 after changes. Default command shape: `python3 dev/evals/run_skill_creator_iteration.py --skill-creator-path /tmp/anthropic-skills-skill-creator/skills/skill-creator --iteration 3 --executor codex --workers 8 --static-viewer`.

### 6. Description optimization

After SKILL.md is stable, run skill-creator's description-optimization loop against `dev/evals/trigger-eval.json` (already exists; ~20 trigger queries). Note: trigger-eval.json may need refreshing if any of its should-trigger queries assume the old "human-eyes = rewrite" framing. Spot-check before running.

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
                                  ├──→ 4. Iteration 1/2 [done] → 5. Iterate on remaining failures
                                  ┘                                      ← we are here
6. Description optimization → 7. Final blind eval
```

---

## Open decisions

### Resolved 2026-04-29

- ~~**Duplicate `grade.py` files.**~~ **Resolved: removed.** `dev/evals/grade.py` deleted. `dev/evals/test_grade.py` now loads `human-eyes/grade.py` via importlib, matching what `run_grade_sweep.py` already does. Single source of truth restored.
- ~~**Iteration set hold-out strategy.**~~ **Resolved: rotate.** Iteration set rotates samples between iterations to guard against overfitting to a fixed five.
- ~~**Existing `ai-XX` samples in the blind eval.**~~ **Resolved: drop.** The 18 older `ai-XX` samples are dropped from the blind eval. Held-out blind set is the 5 unused new AI samples only (rotated each iteration; the unused-this-iteration set forms the blind pool for that iteration's blind eval).
- ~~**Blind eval pass threshold.**~~ **Resolved: per-case ≥70% AND held-out within 10% of iteration-set pass rate.** Two-part bar — the 70% floor catches "wasn't good enough to begin with"; the within-10% check catches "doesn't generalise". Aggregate scores rejected because they hide one broken case behind several strong ones.
- ~~**Description optimization model.**~~ **Resolved: Opus and Sonnet.** Trigger-eval iteration runs the loop against both Opus 4.7 and Sonnet 4.6, picking a description that triggers reliably across both. Haiku skipped.
- ~~**`references/example.md` survival.**~~ **Resolved: refresh now, re-evaluate after iteration 1.** Heading updated from "Hard-mode rewrite" to "rewrite at All depth"; rest of the example prose is depth-agnostic and untouched. If iteration 1 shows subagents struggling without a Balanced-depth example, author one then.

### Still open

*(none currently)*

---

## Success criteria

From the brainstorm requirements doc plus skill-creator's quality bar:

- The new SKILL.md fits comfortably under ~250 lines (currently 314 — see iteration 1 for trimming).
- A writer can read SKILL.md once and know which action they want.
- Iteration loop converges with each case at ≥80% assertion pass rate (or Mae's qualitative sign-off, whichever is the gating criterion).
- Trigger-eval test score after description optimization is ≥80% on held-out queries.
- Blind eval against held-out corpus shows the skill generalises — pass rates within 10% of iteration-set rates.
- A planner, eval reviewer, or future maintainer can pick up `dev/brainstorms/2026-04-28-human-eyes-refocus-requirements.md` plus this plan and the codebase, and reconstruct what was decided and why.

---

## Files touched (summary for handoff)

| Path | Status | Note |
|---|---|---|
| `dev/brainstorms/2026-04-28-human-eyes-refocus-requirements.md` | new | Brainstorm output. |
| `dev/plans/2026-04-28-human-eyes-implementation.md` | new (this file) | Implementation plan. |
| `dev/plans/2026-04-28-human-eyes-refocus.md` | superseded | Kept for history. |
| `human-eyes/SKILL.md` | rewritten and approved | Four-action model, 2-point depth dial (Balanced / All). |
| `human-eyes/references/alternatives.md` | new | Vetted human alternatives for lexical patterns. |
| `human-eyes/references/process.md` | new | Required Rewrite/Write operating process: structural pass, surface pass, self-check, semantic preservation, re-grade revision loop. |
| `human-eyes/references/severity-detail.md` | updated | Old Light/Medium/Hard wording replaced with Balanced/All. |
| `human-eyes/references/patterns.md` | updated | Em-dash guidance reworded for the new depth dial. |
| `human-eyes/grade.py` | updated | `--depth balanced\|all` flag, `AUDIT_SHAPE_CHECKS` registry, `regrade(text, depth=...)` helper, metadata guidance reworded. |
| `dev/evals/grade.py` | re-synced from `human-eyes/grade.py` | Duplicate of the active grader; flagged for cleanup (see Open decisions). |
| `dev/evals/test_grade.py` | updated to depth API | All assertions green. |
| `dev/evals/run_grade_sweep.py` | updated to depth API | Emits `depth_results` keys. |
| `dev/evals/evals.json` | rewritten and updated | 8 cases; case 4 retargeted from `rewrite-obvious-tech` to `rewrite-balanced-tech`; human guardrails retargeted to real repo corpus samples (`21c-dillard-this-is-the-life.md`, `20c-woolf-room.md`). |
| `dev/evals/run_skill_creator_iteration.py` | new | Local adapter for skill-creator-style execution, grading, aggregation, and review generation. Defaults to 8 workers, incremental grading, and old-skill baseline only for human guardrails. |
| `dev/evals/evals.json.bak` | new | Backup of old 14-case evals. |
| `dev/evals/samples/generated-ai/01-10` | new | 10 new AI articles. |
| `dev/skill-workspace/skill-snapshot/` | new | Pre-rewrite skill snapshot for iteration baseline. |
| `dev/skill-workspace/iteration-1/` | new | First full current-vs-old iteration output, grading, benchmark, and review artifacts. |
| `dev/skill-workspace/iteration-2/` | new | Focused rerun after guardrail/process/harness fixes; current skill all evals, old snapshot only human guardrails. |
| `README.md` | updated | Grader CLI usage and example output. |
| `dev/TESTING.md` | updated | Grader output description. |
