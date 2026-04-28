# Humanise: Three-action restructure

## Why

The current SKILL.md frames audit-first in the description but pre-classifies *mode* (Light/Medium/Hard) before the audit even runs. That's wrong on two counts:

1. **Mode is a rewrite parameter, not an audit parameter.** The 43 checks pass or fail based on the text, not the mode. Severity (hard fail / strong warning / context warning / preserve-if-purposeful) is intrinsic to the pattern. Choosing a mode before auditing forces the user to pre-commit to a rewrite intensity for a question they haven't asked yet, and creates routing collisions (e.g. "humanise this" maps to Medium-rewrite in Step 1 and to audit-only in Operating Model 1).
2. **The skill is also for *writing* new content that avoids AI patterns, not just auditing/rewriting existing content.** The current structure has no place for "help me draft this without sounding AI" — both Audit and Rewrite assume input text exists to be analysed.

The five operating models in the current doc are an attempt to handle the first issue and they don't address the second at all. Three actions is the right count.

## Goals

- Make audit always run with no mode pre-classification.
- Reduce five operating models to three actions plus orthogonal modifiers.
- Add a Write action so the skill works on briefs, not just existing text.
- Resolve the routing collisions (findings 4 and 5 from ce-doc-review).
- Reduce SKILL.md cognitive load (find 12 from product-lens).
- Keep the deterministic grader (43 checks, severity classes, plain-English copy, `human_report` contract) unchanged.

## Three actions

### 1. Audit

**Trigger:** any input text where the user wants analysis, or any ambiguous text-only input (default).

**Behaviour:** run the grader with no mode constraint. Show all 43 results, classified by severity. Explain in plain English. Stop and ask what's next.

**No mode question.** No Light/Medium/Hard up-front.

### 2. Rewrite

**Trigger:** user explicitly asks to rewrite, fix, clean up, de-AI, strip tells, or confirms after an audit.

**Behaviour:** run the audit first (always). Then ask Light/Medium/Hard if not specified. Then rewrite at that mode. Then run the structural self-check, semantic preservation, and post-check.

**Mode applies here.**

### 3. Write

**Trigger:** user asks for new content. "Write me an essay on X", "draft a blog post about Y", "help me compose Z without sounding AI".

**Behaviour:** ask Light/Medium/Hard if not specified. Draft the content under the chosen mode's constraints (avoid hard failures, strong warnings; treat context warnings per mode). Run the post-check on the draft. Optionally iterate.

**Mode applies here.** No initial audit (there's no input text to audit), but the post-check on the output uses the same grader.

## Orthogonal modifiers

- **Recommendation:** after an audit, optionally suggest a rewrite mode. Doesn't change the audit; just adds a sentence at the end.
- **Save:** write the report (audit / rewrite / write) to a Markdown file. Path follows the existing default-path convention (same dir as input, suffixed; or `./humanise-<action>.md` if no input path).

## Why this collapses cleanly

| Old operating model | New action | Notes |
|---|---|---|
| 1. Audit only | Audit | Audit is the default; "only" is implicit. |
| 2. Audit plus recommendation | Audit + Recommendation modifier | Same behaviour; the recommendation is a modifier, not a separate model. |
| 3. Audit, agree, then rewrite | Audit → Rewrite (sequential) | The user agrees between phases; that's just normal interactive flow, not a named model. |
| 4. Rewrite and verify | Rewrite | The "verify" step (post-check) is part of any Rewrite. |
| 5. Save report | Save modifier | Applies to any action. |
| (none) | Write | New action, currently unsupported. |

## Step order

Old:
1. Step 0: Choose workflow
2. Step 1: Calibrate intensity and genre (mode pre-classification)
3. Step 2: Audit
4. Step 3: Decide or ask before rewriting
5. Step 4: Fix
6. Step 5: Semantic preservation check
7. Step 6: Structural self-check
8. Step 7: Post-check

New:
1. Step 1: Pick action (audit / rewrite / write). Default to audit.
2. Step 2: Audit (only for audit and rewrite actions; write actions skip).
3. Step 3: Decide next step (stop / rewrite / save). Audit ends here unless rewrite is chosen.
4. Step 4: Pick mode (Light / Medium / Hard). Only fires for rewrite and write.
5. Step 5: Rewrite or write under mode. Address structural patterns first, surface patterns second.
6. Step 6: Semantic preservation check (rewrite only — write has no original to preserve).
7. Step 7: Structural self-check (rewrite and write).
8. Step 8: Post-check via grader on the output.

## Output format consequences

Old: three named templates (audit-only, audit-plus-recommendation, rewrite-and-verify), with Models 3 and 5 unrendered.

New: three templates, one per action.

- **Audit output:** workflow=audit, summary, confidence, AI-pressure explanation, main issues, full 43-row table with severity-tiered "Recommended action" column (no per-mode action), recommended next step, question.
- **Rewrite output:** workflow=rewrite, mode, initial audit (with severity-tiered actions), rewrite, structural self-check, semantic preservation, post-check at chosen mode.
- **Write output:** workflow=write, mode, draft, structural self-check, post-check at chosen mode. No initial audit.

Save modifier wraps any of these.

## Audit table column change

Old audit table column: `Hard action` (or whatever mode the user picked) — gives one mode's recommended action.

New audit table column: `Severity` + `Recommended action`, where the recommended action is a phrase tied to severity:
- Hard failure → "Fix in any mode"
- Strong warning → "Fix in Light, Medium, Hard (disclose if preserved)"
- Context warning → "Preserve in Light if purposeful; fix in Medium/Hard"
- Em dash → "Preserve in Light with disclosure; fix in Medium/Hard"

The mode-specific action only appears in rewrite and write outputs, not in the standalone audit.

## Code changes

`humanise/grade.py` and `dev/evals/grade.py`:
- `format_human_report` should accept a "no mode" / "audit-only" rendering that shows severity + severity-tiered recommended action instead of one mode's action column.
- `markdown_checks_table` needs a new column shape for the audit-only path: `| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |`.
- The CLI keeps `--mode` for rewrite/write post-checks. Audit-only can run without `--mode` and uses the new severity-tiered column.

`dev/evals/test_grade.py`:
- New assertion that audit-mode rendering uses the severity-tiered column.
- Existing mode-specific assertions stay for rewrite/write paths.

## What stays the same

- 43 checks. No additions, no removals.
- Severity classes: hard failures, strong warnings, context warnings, preserve-if-purposeful, em-dash special.
- Pattern catalogue (`references/patterns.md`).
- `human_report` field shape (`overview`, `confidence`, `ai_pressure_explanation`, `failed_checks`, `all_checks`).
- Hard constraints section (em dashes, manufactured insight, adversarial reframes, staccato).
- Personality and soul (now load-bearing for both Rewrite and Write — no longer scope-bleed).
- Save default path convention.

## What this fixes from ce-doc-review

| Finding | Status after restructure |
|---|---|
| 1. Em-dash classification | Already fixed in walk-through. |
| 2. Step 4 numbering | Already fixed in walk-through. |
| 3. Output gap for Models 3 and 5 | Mostly moot — Models 3, 5 collapse. Save modifier is now explicit. |
| 4. Routing collision on "humanise this" | Resolved. There is no Step-1 mode classification; "humanise this" defaults to audit, and the user is asked about rewrite afterwards. |
| 5. Genre detection load-bearing | Reduced. Genre matters for the *rewrite recommendation* (still does), not for the audit path. |
| 6. Hard-mode unbounded recursion | Still needs fix. Add max-rounds bound. |
| 7. Save-report has no Step | Resolved. Save is a modifier with explicit format. |
| 8. Doc still rewrite-centred | Improved. Audit gets its own action with no rewrite scaffolding required. |
| 9. Personality and soul scope bleed | Resolved. Now load-bearing for Write. |
| 12. Five operating models too many | Resolved. Three actions + two modifiers. |
| 13. Name/identity mismatch | Partially resolved. "Humanise" still includes Rewrite and Write — actions consistent with the verb. Audit becomes the default but the verb's actions are present. |
| 23. Headless contract | Improved. Default to audit (read-only, low-risk) if no clear action keyword. Add explicit "if running headless and no rewrite/write keywords detected, audit + exit" rule. |

Findings still standing after this restructure: 6, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24. Walk through these as a separate pass.

## Blind-agent evaluation

The current test suite (`dev/evals/test_grade.py`) is a unit-test surface for the grader script. It does not test the *skill* — whether an autonomous agent following SKILL.md produces valid, consistent output. This restructure changes both the operating contract and the output shape, so we need an eval that exercises the protocol end-to-end.

### Why blind agents

A blind agent has no prior context: no conversation history, no knowledge of what the previous run decided. Each invocation must independently pick an action, choose a mode, render the report, and stop. If two blind agents disagree on the workflow for the same input, that is a reliability failure of the spec, not a model flake. Blind dispatch is the only way to surface that.

### Harness

Standalone Python script at `dev/evals/blind_eval.py`. Independent of `test_grade.py`.

- Reads samples from `dev/evals/samples/`.
- For each sample, spawns 3 fresh sub-agents via the **Claude Agent SDK**. Each agent loads `humanise/SKILL.md` (mounted as a skill) and is given the sample as input plus a brief prompt that mimics a real user invocation (e.g. `/humanise <input>` or natural-language framing).
- Captures each agent's full output, including the chosen action, chosen mode (if any), full audit table, and any rewrite/write content.
- Spawns separate **reviewer agents** that score each output against the rubric below. Reviewer agents see the input and the output but not SKILL.md — they're scoring against criteria, not against compliance with a doc.
- Outputs a JSON results file plus a Markdown summary report at `dev/evals/blind-eval-report.md`.

### Sample set

- All 18 samples in `dev/evals/samples/generated-ai/` (existing).
- A representative subset of `dev/evals/samples/human-sourced/` (e.g. 6 covering different genres: fiction, memoir, journalism, instructional, opinion, literary essay).
- 4 new **brief** samples for the Write action — short topic prompts like "Write a 300-word essay about hybrid working" or "Draft an opening paragraph for an article about urban heat islands". These need to be added at `dev/evals/samples/briefs/` as part of the migration.

Total: 28 samples × 3 runs = 84 dispatches per eval pass.

### Rubric

Validity — scored per output by a reviewer agent:

- **Action chosen matches input intent.** For ambiguous inputs (no clear rewrite verb), the action must be Audit. For clear rewrite requests, Rewrite. For briefs with no input text, Write. Reviewer agent gets the input and decides what intent should have been; mismatch = fail.
- **Audit table is full 43 rows.** Reviewer counts. < 43 = fail.
- **No implementation-label leakage.** Reviewer scans for the banned-phrase list: `context_warning`, `strong_warning`, `hard_fail`, `failure_mode`, `frictionless_structure`, `generic_abstraction`, `vocabulary_pressure(`, `triggered_checks`, `mode_results`, raw JSON. Any match = fail.
- **Severity classification matches SKILL.md severity classes.** Reviewer cross-references the table's severity column against the canonical severity list. Disagreement on hard failures = fail; ≥ 5% disagreement on strong warnings = fail.
- **Plain-English column shape.** Audit must have `What it looks for / What happened here / Why this matters` columns. Rewrite/Write outputs must include the post-check table with the same shape.
- **For Rewrite outputs:** post-check passes the chosen mode's threshold (Hard: 0 failures; Medium: hard fails + strong warnings = 0; Light: hard fails + strong warnings = 0, context warnings disclosed).
- **For Write outputs:** post-check passes the chosen mode's threshold; the draft addresses the brief.

Consistency — scored across 3 runs per sample:

- **Action consistency = 100%.** All 3 runs must pick the same action. Workflow flip-flop is the most serious reliability failure and has no tolerance.
- **Severity classification consistency ≥ 95%** per-check across runs. (Out of 43 checks × 3 runs = 129 classifications; ≤ 6 disagreements tolerated per sample.)
- **Mode recommendation consistency ≥ 90%** when applicable. Recommendation is more genre-judgement-driven and has more tolerance.
- **Hard-failure detection consistency = 100%.** The hard-fail set must match exactly across runs.

### Pass thresholds

To merge the restructure:

- **Validity:** ≥ 95% of outputs pass all validity criteria. (28 × 3 = 84 outputs; ≤ 4 failures.)
- **Consistency:** ≥ 90% of samples pass all consistency criteria. (28 samples; ≤ 2 failures.)
- **Zero tolerance:** zero implementation-label leaks across all 84 outputs. Any leak = block.

If thresholds fail, iterate on SKILL.md and rerun until they pass. Each iteration writes its results to `dev/evals/runs/YYYY-MM-DD-HHMMSS/` so we can compare across attempts.

### Cost estimate

84 dispatches × ~8K tokens per dispatch (input + output) × Sonnet 4.6 ≈ 670K tokens per run. At Sonnet 4.6 pricing, ~$2 per full eval pass. Affordable to run 5–10 times during iteration.

## Migration

1. Write new SKILL.md operating-models section (3 actions + modifiers).
2. Reorder Process steps (8 steps).
3. Add new Audit output template (no mode column).
4. Add new Write output template.
5. Update `format_human_report` and `markdown_checks_table` for the audit-only severity-tiered column.
6. Update `dev/evals/test_grade.py` for the new audit-mode assertions.
7. Update README.md to describe three actions instead of five operating models.
8. Render a sample Audit, Rewrite, and Write output to confirm.
9. Add 4 brief samples to `dev/evals/samples/briefs/` for the Write path.
10. Build `dev/evals/blind_eval.py` using the Claude Agent SDK; implement the rubric and threshold checks.
11. Run the eval. Iterate on SKILL.md until thresholds pass.
12. Commit only after the eval passes.

## Risks

- **Breaking existing test fixtures.** The current tests assert `Hard action` in the markdown table. New tests need to assert either `Recommended action` (severity-tiered) or the mode-action depending on path. Test surface grows ~10–15 assertions.
- **README example becomes stale.** Need to regenerate.
- **Skill description in frontmatter** needs to mention Write. Currently says "audits writing for AI-style patterns ... or optionally humanise/de-AI text after an audit". Needs a third clause.
- **The Step 1 → Step 2 → Step 3 ordering depends on the agent reading the doc top-to-bottom.** Same risk as today; not new.

## Out of scope

- Headless mode contract gaps (finding 23) beyond the audit-default rule.
- Genre detection rubric (finding 5 second half).
- Counting reliability via script-routed targeted assertions (finding 14).
- Hard-mode max-rounds bound (finding 6) — fix in the same commit if straightforward; otherwise follow-up.
