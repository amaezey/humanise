---
title: "feat: Audit output redesign"
type: feat
status: active
date: 2026-05-03
origin: dev/brainstorms/2026-05-03-audit-output-redesign-requirements.md
---

# feat: Audit output redesign

## Summary

Implement the audit-output redesign in nine reviewable units: schema (severity on agent-judgement items), vocabulary (signal-stacking rename + new templates), measurement lock (audit-shape checks + harness fixtures), three renderer steps (summary lines → flagged-items shape → full-report disclosure), CLI architecture (`--judgement-file` flag plus SKILL.md flow), audit-fidelity HTML viewer, and a close-out iteration. All nine units land on a single feature branch (`audit-output/redesign`) with one commit per unit; one PR opens at the end of U9.

---

## Problem Frame

The current audit (post-PR-#15) has the right architecture for the auto-detected side — script renders from a contract — but the agent-assessed side is still rendered by hand, the two halves don't share shape conventions, the summary line only counts severity (not check volume), and "pressure" is undefined jargon. The brainstorm establishes the target shape; this plan walks it down to nine atomic implementation units that can each be reviewed and reverted on their own. (See origin: `dev/brainstorms/2026-05-03-audit-output-redesign-requirements.md`.)

---

## Requirements

The plan must deliver R1–R22 from the origin requirements doc.

- R1. Counts line: `Auto-detected: X of Y flagged · Agent-assessed: A of B flagged`
- R2. Severity line: `Severity: N hard fail · M strong warning · P context warning` (space-separated lowercase)
- R3. Signal-stacking line with inline definition (clear / triggered + threshold)
- R4. "Signal stacking" replaces "pressure" on user-facing surfaces; internal field names unchanged
- R5. Default audit shape: header → counts/severity/signal-stacking → flagged items both blocks → next-step
- R6. Auto-detected flagged items: glyph + bold name + phrase, no Action
- R7. Agent-assessed flagged items: glyph + bold name + sub-bullets per finding
- R8. Next-step prompt: "Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?"
- R9. No all-clear collapse — full default shape always
- R10. Calibration ("even human text can fail some checks") lives in the rewrite depth question, not in the audit body
- R11. Full coverage report opens with the same content as the default, then per-block sections, then next-step
- R12. Each per-block section: header → brief note → coverage table(s)
- R13. Auto-detected coverage: 8 sub-category tables in patterns.md heading order
- R14. Agent-assessed coverage: one flat 8-row table
- R15. Both coverage tables: `Pattern | Severity | Result | Detail`; detail source defined per row category
- R16. `humanise/scripts/judgement.json` items gain a `severity` field
- R17. Same severity × depth → action mapping for both blocks
- R18. Action column removed from coverage tables
- R19. Script renders all visible audit shapes; agent supplies structured input + prints verbatim
- R20. Agent supplies the agent-judgement findings as a structured contract
- R21. All user-facing strings live in `humanise/scripts/vocabulary.json`
- R22. Brief-note copy drafted during implementation, reviewed by Mae

**Origin actors:** A1 (Writer), A2 (Agent), A3 (Script).
**Origin flows:** F1 (Default audit), F2 (Full coverage report on request).
**Origin acceptance examples:** AE1 (R5, R9 — clean draft default render), AE2 (R6 — phrase + structural mix), AE3 (R7 — multi-finding agent item), AE4 (R15 — table cells across clear/flagged), AE5 (R10, R17 — calibration in depth question, not audit body).

---

## Scope Boundaries

- Per-pattern rewrite recipes — out of scope (system stays at severity × depth granularity).
- Severity values per agent-judgement item — chosen during U1 implementation, not pre-decided here.
- Brief-note copy for each block — drafted in U6, not pre-decided here.
- Suggestions / Rewrite / Write action output shapes — downstream actions consume the audit but their own outputs don't change in this plan.
- Per-pattern guidance prose updates — out of scope; existing `guidance` field text stays.

### Deferred to Follow-Up Work

- Severity × depth → action mapping doc updates beyond what U6 already needs in SKILL.md — if the depth-dial section needs broader rewriting, that's a separate plan.

---

## Context & Research

### Relevant Code and Patterns

- `humanise/scripts/grade.py` — renderer entry points (`format_two_layer`, `format_agent_judgement`), audit-shape checks (`check_audit_shape_*`), section regexes (`AUDIT_HEADER_RE`, `TOP_LEVEL_SECTION_HEADER_RE`, `LAYER_1_BLOCK_RE`), severity × depth mapping (`_action_for_check`), contract emission (`human_report`).
- `humanise/scripts/registries.py` — JSON loaders + accessor API (`string_for`, `severity_label`, `pattern_for`, `judgement_for`, `_validate_judgement`).
- `humanise/scripts/contracts/audit-format-v1.json` — contract schema; `agent_judgement[]` slot already exists, U1 extends item shape with `severity`.
- `humanise/scripts/{vocabulary,patterns,judgement}.json` — registry data (post-PR-#16 JSON migration).
- `dev/evals/run_skill_creator_iteration.py` — `catalogue_hits`, `grade_one_assertion`, `build_performance_report`; the eval-runner that wires audit-shape checks into the iteration harness.
- `dev/evals/diff_renders.py` + `dev/evals/diff_baseline/` — JSON-equivalence diff gate (11 frozen baselines).
- `dev/tools/render_patterns_md.py` — precedent for U8 (single-file generator that turns structured registry data into a human-viewable artefact).
- `dev/skill-workspace/iteration-6/` — most recent iteration; `review.html` is the existing viewer pattern U8 sits parallel to.

### Institutional Learnings

- **catalogue_hits substring bug** (PR #15): the iteration harness substring-matched pattern names against the entire response, which broke under U11's two-layer renderer because section tables now list every pattern in coverage rows. The fix counts only Layer-1 flag blocks. U3 must extend this counter for the new flagged-items shape — measurement locks before renderer changes.
- **`_section_text` truncated on nested bold lines**: PR #15 added `TOP_LEVEL_SECTION_HEADER_RE` to whitelist top-level headers. U6's full-report sections must verify the boundary regex covers their entry/exit headers — the brainstorm's deferred Q on this is exactly this risk.
- **Verbatim-quote determinism** (PR #15): regex-driven checks must emit `m.group(0)` from the original text, not lowercased + joined captures. Quoted phrases in flagged-items sections feed `every_flag_block_contains_input_substring`; munging case or connectors breaks the audit-shape check.
- **JSON-equivalence diff gate** (Phase 2 / U10b): `dev/evals/diff_renders.py` + `dev/evals/diff_baseline/` is the merge gate for renderer-touching refactors. U1's contract change regenerates baselines explicitly in the same commit; U4–U7 renderer-only commits must show zero diff against the regenerated baselines.
- **Audit-shape check four-step convention** (PR #5 review P0-CODE-04): every new check in `AUDIT_SHAPE_CHECKS` needs (a) function in `grade.py`, (b) registry registration, (c) call site in `run_skill_creator_iteration.py:310-329`, (d) `expect_pass` + `expect_fail` + edge-case tests in `test_grade.py` using the custom `expect_*` helpers. Skipping (d) was the failure mode in Phase 3.
- **String rename sweep discipline** (PR #5 review P1-DOC-12): partial renames are worse than no rename. U2 sweeps user-facing pressure → signal stacking surfaces in one commit (vocabulary.json, SKILL.md, patterns.md, example.md); internal field names stay.

### External References

None for this plan. Local patterns and the existing renderer pipeline are sufficient.

---

## Key Technical Decisions

- **CLI shape: `--judgement-file <path>` flag on `grade.py` main()**. Resolved in this plan from origin's deferred Q1. Matches existing `--format` and `--depth` parser shape; minimal new surface; agent writes a JSON file, calls grade.py once, prints output verbatim. Other candidates (stdin pipe, two-call sequence) work but cost more SKILL.md complexity for no gain.
- **Audit-fidelity HTML viewer is local: `dev/tools/render_audit_html.py`** — not an extension to the cross-repo skill-creator plugin. Follows the `dev/tools/render_patterns_md.py` precedent. Keeps the redesign self-contained; no roadmap coupling to a different repo's owner.
- **Renderer broken into three units (U4 / U5 / U6)** rather than a single big change. Each unit is a reviewable, revertible step: summary lines first, then flagged-items shape, then progressive disclosure. The renderer is the load-bearing surface; small steps prevent a single bad merge from rolling back everything.
- **Measurement-lock unit (U3) lands before any renderer change.** Audit-shape checks for the new shape and a fixture in `test_iteration_harness_measurement.py` go in red, then go green as U4–U7 each land. This is the catalogue_hits-bug pattern: lock measurement before changing the thing being measured.
- **Severity × depth → action mapping is reused, not re-implemented.** `_action_for_check` already returns the right answer for auto-detected checks; once U1 adds `severity` to agent-judgement items, the same function applies. No second mapping lives anywhere.
- **`schema_version: "1"` stays.** U1's `severity` addition is additive (new field on existing record / item shape); no version bump needed.

---

## Open Questions

### Resolved During Planning

- CLI shape for agent → script data flow: `--judgement-file <path>`.
- HTML viewer location: `dev/tools/render_audit_html.py` (local, single-file generator).
- Plan structure: 9 units, three-unit renderer batch, measurement-lock unit before renderer.

### Deferred to Implementation

- Severity values per agent-judgement item (8 items): chosen during U1 implementation, reviewed with Mae before commit.
- Brief-note copy for each block: drafted during U6 implementation, reviewed with Mae before commit.
- Specific HTML viewer layout (per-test side-by-side vs accordion vs other): U8 implementation produces a sketch first; reviewed before completing the unit.

---

## Implementation Units

- U1. **Schema: severity on agent-judgement items**

**Goal:** Add a `severity` field (`hard_fail` / `strong_warning` / `context_warning`) to each of the 8 records in `humanise/scripts/judgement.json`. Extend `audit-format-v1.json` so `agent_judgement[]` items carry severity. Validation enforces the field. Diff-baselines regenerate to absorb the contract change.

**Requirements:** R16, R17.

**Dependencies:** None.

**Files:**
- Modify: `humanise/scripts/judgement.json`
- Modify: `humanise/scripts/contracts/audit-format-v1.json`
- Modify: `humanise/scripts/registries.py` (`REQUIRED_JUDGEMENT_FIELDS`, `_validate_judgement`)
- Regenerate: `dev/evals/diff_baseline/*.json` (all 11)
- Test: `dev/evals/test_judgement_yaml.py`, `dev/evals/test_audit_contract.py`, `dev/evals/test_registries.py`

**Approach:**
- Severity values per item proposed by the implementer; reviewed with Mae before commit. Tonal uniformity, neutrality collapse, faux specificity, and generic metaphors plausibly cluster around `strong_warning`; structural monotony, even jargon distribution, forced synesthesia, and the genre slot plausibly cluster around `context_warning` — but final assignments are the review point.
- Schema version stays at "1" — new field is additive on an existing record/item shape.
- Diff-baseline regen is part of *this* commit, not a separate pass. Commit message documents the regeneration explicitly so reviewers don't have to infer why all 11 files moved.

**Patterns to follow:**
- `patterns.json` records already carry a `severity` field — mirror the same value space.
- `_validate_judgement`'s existing field-required loop is the pattern for enforcement.

**Test scenarios:**
- Happy path: each of the 8 records loads cleanly; `judgement_for(item_id)["severity"]` returns the expected value.
- Error path: a record missing `severity` raises validation error naming the missing field and the record id.
- Error path: a record with an invalid severity value (e.g. `"medium"`) raises validation error naming the value and the allowed set.
- Integration: `humanise/scripts/grade.py` running `--format json` on a real input includes severity on every entry in the contract's `agent_judgement[]` (when populated).
- Integration: `dev/evals/diff_renders.py` shows zero diff between freshly-regenerated baselines and the contract output produced by this commit's grade.py — i.e. the regen captures only the new severity field, no other contract drift.

**Verification:**
- All test files green.
- `python3 humanise/scripts/grade.py --format json <sample>` emits valid contract with severity in every agent-judgement item (when populated).
- Manual check: each severity assignment makes sense given the item's prompt and `flagged_when` rule. Reviewed with Mae before commit.

---

- U2. **Vocabulary: signal-stacking rename + new templates + severity label values**

**Goal:** Rename "pressure" → "signal stacking" on user-facing surfaces only. Add the new vocabulary templates U4–U7 will read. Switch severity labels to space-separated lowercase ("hard fail", "strong warning", "context warning").

**Requirements:** R2, R3, R4, R21.

**Dependencies:** None — additive registry edits.

**Files:**
- Modify: `humanise/scripts/vocabulary.json` — add: `templates.detected_patterns_heading`, `templates.agent_assessed_heading`, `templates.brief_note_auto_detected` (placeholder), `templates.brief_note_agent_assessed` (placeholder), `templates.signal_stacking_clear`, `templates.signal_stacking_triggered`, `templates.flagged_pattern_block_no_action` (the new R6 shape), `templates.agent_assessed_flagged_block` (the new R7 shape), `templates.next_step_prompt_with_full_report` (R8 wording). Rename: `pressure_status.*` → `signal_stacking_status.*`. Update: `severity_labels.{hard_fail,strong_warning,context_warning}` to "hard fail" / "strong warning" / "context warning".
- Modify: `humanise/SKILL.md` — sweep "pressure" mentions to "signal stacking" (7 occurrences per learnings research).
- Modify: `humanise/references/patterns.md` — sweep "pressure" mentions on user-facing prose.
- Modify: `humanise/references/example.md` — sweep "pressure" mentions in worked example.
- Modify: `dev/evals/test_vocabulary.py` — update `LEGACY_LITERALS` to forbid "pressure" on user-facing surfaces; add byte-equivalence pins for the new templates.

**Approach:**
- `grade.py`'s 56 internal field-name occurrences (`ai_pressure`, `pressure_status`, `_short_pressure_explanation`, etc.) **stay unchanged** in this unit. Internal renames are deliberately deferred to avoid bloating the user-facing rename.
- Brief-note templates land as placeholders; U6 fills the actual copy after Mae review.
- Single commit covers all user-facing surfaces — partial renames are the failure mode (PR #5 P1-DOC-12).

**Patterns to follow:**
- Template byte-equivalence pinning convention from `test_vocabulary.py:328-360` (each template has an `expected_*` constant).
- `LEGACY_LITERALS` guard at `test_vocabulary.py:338` — forbid old strings on user-facing surfaces.

**Test scenarios:**
- Happy path: `string_for("templates.detected_patterns_heading")` returns the expected literal.
- Happy path: `severity_label("hard_fail")` returns "hard fail" (space, lowercase).
- Happy path: `string_for("signal_stacking_status.clear")` returns the renamed key's value.
- Error path: `LEGACY_LITERALS` test fails when "pressure" appears in any of vocabulary.json (user-facing), SKILL.md, patterns.md, example.md.
- Edge case: `LEGACY_LITERALS` does NOT fail on `grade.py` mentions of `ai_pressure` etc. — the guard is scoped to user-facing surfaces only.

**Verification:**
- `python3 dev/evals/test_vocabulary.py` green.
- Manual grep: `rg -i pressure humanise/SKILL.md humanise/references/ humanise/scripts/vocabulary.json` returns zero hits.
- Manual grep: `rg -i pressure humanise/scripts/grade.py` still returns the 56 internal-field-name occurrences (unchanged).

---

- U3. **Lock measurement: audit-shape checks + harness fixtures (intentionally red)**

**Goal:** Land the audit-shape check stubs and harness fixtures for the new shape, before any renderer change. Tests fail intentionally — they go green as U4–U7 each land. This locks measurement before the thing being measured changes.

**Requirements:** R1–R10 (the audit-shape requirements).

**Dependencies:** U2 (vocabulary keys exist for the templates the tests assert against).

**Files:**
- Modify: `humanise/scripts/grade.py` — add stub `check_audit_shape_*` functions: counts-line shape, severity-line shape, signal-stacking-line shape, glyph-flagged-shape (both blocks), severity-in-coverage-table, no-action-column. Register in `AUDIT_SHAPE_CHECKS`. Each stub returns failure until the renderer ships its piece.
- Modify: `dev/evals/run_skill_creator_iteration.py` — wire new check names into `grade_one_assertion` dispatch (lines 310-329 area).
- Modify: `dev/evals/evals.json` — add new assertion entries to existing eval cases that exercise these shapes.
- Modify: `dev/evals/test_grade.py` — `expect_pass` + `expect_fail` + missing-section + vacuously-true fixtures per check, using the custom `expect_*` helpers at lines 35-88.
- Modify: `dev/evals/test_iteration_harness_measurement.py` — add fixture for the new flagged-items shape (`<glyph> **<name>**` opener) so the harness's `catalogue_hits` extractor handles both old and new shapes during the transition.

**Approach:**
- Four-step convention per check (function + registration + call-site + tests). Skipping any of the four reintroduces the PR #5 P0-CODE-04 failure.
- Stubs are deliberate red — running `python3 dev/evals/test_grade.py` after this unit lands shows the new audit-shape tests failing on synthetic-correct fixtures, because the renderer hasn't shipped yet. The iteration harness shows the same. This is the locked baseline.
- The harness fixture for the new flagged-items shape is the catalogue_hits-bug-style guardrail: when U4–U6 ship, the new shape will substring-match correctly because we added the fixture *before* changing the extractor.

**Patterns to follow:**
- `check_every_flag_block_has_explanation` (`grade.py:2796`) shape for new checks: take output_text + input_text, extract the block, predicate, return `{text, passed, evidence}`.
- `_FLAG_BLOCK_CANDIDATE_RE` is the precedent for a broader regex that catches malformed blocks for the explanation check.

**Test scenarios:**
- Happy path: each new check's `expect_pass` fixture matches the synthetic-correct shape and returns passed=True.
- Error path: each new check's `expect_fail` fixture matches a synthetic-wrong shape and returns passed=False with evidence naming what's wrong.
- Edge case: missing audit section returns vacuously-true (no audit section, nothing to check).
- Edge case: no flag blocks returns vacuously-true (nothing to check).
- Integration: running the iteration harness against iteration-6's frozen response.md files (old shape) shows the new audit-shape checks failing — that's the locked red baseline.

**Verification:**
- `python3 dev/evals/test_grade.py` runs the new tests, with `expect_pass` fixtures green and `expect_fail` fixtures green (each fails for the right reason).
- `python3 dev/evals/test_iteration_harness_measurement.py` green.
- Iteration harness on iteration-6's existing outputs shows the new audit-shape assertions failing — confirming the lock is working.

---

- U4. **Renderer: new summary lines (counts + severity + signal stacking) and 4-column coverage tables**

**Goal:** `format_two_layer` emits the three-line summary block from R1–R3 with the new vocabulary keys. Coverage tables drop the Action column and gain Severity (already in pattern records) + Detail (sourced per R15). Signal-stacking inline definition reads from the renamed template.

**Requirements:** R1, R2, R3, R15, R18.

**Dependencies:** U1 (severity field exists on agent-judgement items in contract), U2 (vocabulary keys present), U3 (audit-shape checks ready to flip green).

**Files:**
- Modify: `humanise/scripts/grade.py` — `_format_layer_1` emits counts line + severity line + signal-stacking line instead of a single severity line. `_format_layer_2` and `_layer_2_section` and `_layer_2_row` switch to `Pattern | Severity | Result | Detail`. `_short_pressure_explanation` renames to `_short_signal_stacking_explanation` (and updates its registry-key references).
- Test: `dev/evals/test_two_layer_render.py` — assertions for the new summary-line shape and the 4-column table shape.
- Test: `dev/evals/test_audit_contract.py` — confirm contract still validates (unchanged contract on this unit).

**Approach:**
- The Detail column source per R15: pattern's `guidance` field (auto-detected flagged), empty (auto-detected clear). Agent-assessed Detail handling lands in U5 since the agent-assessed-side renderer needs the new flagged-items shape there.
- Severity column reads `pattern_for(check_id)["severity"]` and maps via `severity_label()` to the renamed labels.
- Signal-stacking line: clear = `Signal stacking: clear (weaker AI signals are not accumulating)`. Triggered = `Signal stacking: triggered — N of T threshold (<contributing-component-list>)`. Threshold and components come from the existing pressure-aggregation contract data — only the rendering changes.

**Patterns to follow:**
- `_format_layer_1` (`grade.py:2161`) for the summary-block composition pattern.
- `_layer_2_row` (`grade.py:2267`) for table-row composition; extend to include severity + detail columns.

**Test scenarios:**
- Happy path: summary block on a draft with 1 strong-warning auto-detected flag and 1 strong-warning agent-assessed flag emits `Auto-detected: 1 of N flagged · Agent-assessed: 1 of M flagged`, `Severity: 0 hard fail · 2 strong warning · 0 context warning`, `Signal stacking: clear (...)`.
- Happy path: signal-stacking triggered case emits `Signal stacking: triggered — 5 of 4 threshold (<components>)`.
- Edge case: zero-flag draft emits the same three-line shape with all zeros — no all-clear collapse (R9).
- Edge case: agent-judgement contract empty (regex-only invocation) — counts line shows `Agent-assessed: 0 of 0 flagged` and severity line aggregates only programmatic counts.
- Integration: `Covers AE1.` clean draft — verified end-to-end against AE1 in origin.
- Integration: `Covers AE2.` mix of phrase-carrying and structural patterns — auto-detected flagged-items render correctly when only summary lines + flagged items exist.

**Verification:**
- `python3 dev/evals/test_two_layer_render.py` green.
- Audit-shape checks for counts-line, severity-line, signal-stacking-line, and severity-in-coverage-table flip from red to green when run against the new renderer output.
- Iteration harness pass-rate on the audit-only evals matches iteration-6's pre-rework numbers (no regressions on auto-detected-only flows).

---

- U5. **Renderer: glyph + sub-bullet flagged-items shape (both blocks)**

**Goal:** Both blocks emit flagged items with consistent glyph shape. Auto-detected: `! **Pattern** — "phrase"` (Action gone). Agent-assessed: `! **Item**\n  - "phrase" — why` (state, list, and composite types converge on this shape). `_action_for_check` now applies to agent-assessed items via the severity field added in U1.

**Requirements:** R6, R7.

**Dependencies:** U1 (severity on agent items so `_action_for_check` works), U4 (summary block + 4-col tables already render).

**Files:**
- Modify: `humanise/scripts/grade.py` — `_layer_1_pattern_block` drops the Action clause. `_render_judgement_item` / `_render_judgement_list_item` / `_render_judgement_composite_item` converge on the glyph-prefixed multi-line shape.
- Modify: `humanise/scripts/grade.py` — `_action_for_check` is unchanged, but its agent-assessed call sites now read severity off the contract record.
- Test: `dev/evals/test_agent_judgement_render.py` — fixtures for state, list, and composite items in the new shape (single-finding state, multi-finding list, composite genre + watchlist).
- Test: `dev/evals/test_two_layer_render.py` — auto-detected flagged-items shape.

**Approach:**
- Single-finding state items: `<glyph> **<label>** — <state value>`. Single line, no sub-bullets.
- Multi-finding list items: `<glyph> **<label>**\n  - "<phrase>" — <why>` per finding. Header + sub-bullets.
- Composite (genre slot): `<glyph> **<label>** — Genre detected: <genre>` + watchlist findings as sub-bullets if present.
- Agent-assessed Detail column for U4-shipped coverage tables now resolves: clear → answer/value text, flagged → `(see above)` pointing at the bullet block.
- Severity glyph mapping reuses `severity_glyphs` registry — same glyph values for both blocks.

**Patterns to follow:**
- The existing dispatch on `record["answer_schema"]["type"]` in `_render_judgement_item` is preserved; only the rendered shape changes.
- `_format_quoted_phrases` (`grade.py:2204`) for the auto-detected phrase formatting (cap at 3, "+N more" overflow).

**Test scenarios:**
- Happy path: auto-detected flagged item renders `! **Em dashes** — "—"`. No "Action:" suffix, no `—` between phrase and Action (Action gone).
- Happy path: agent-assessed state-type flagged (Tonal uniformity, "register holds without breaks") renders `! **Tonal uniformity** — register holds without breaks`.
- Happy path: agent-assessed list-type flagged with 2 findings (Faux specificity) renders `! **Faux specificity**\n  - "phrase 1" — why 1\n  - "phrase 2" — why 2`.
- Happy path: agent-assessed composite (Genre specific, flagged with watchlist findings) renders `! **Genre specific** — Genre detected: academic\n  - "phrase" — why`.
- Edge case: auto-detected structural pattern (no quotable phrase) renders `! **Mechanical repeated sentence starts**` — no `— "phrase"` clause.
- Edge case: phrase list of 5 caps at 3 with `(+2 more)` suffix.
- Integration: `Covers AE3.` from origin — multi-finding faux specificity matches the AE3 expectation.
- Integration: `_action_for_check` returns "Fix" for an agent-assessed strong_warning flagged item at Balanced depth, and "Disclose or ask before preserving" for a context_warning at Balanced — same as auto-detected.

**Verification:**
- `python3 dev/evals/test_agent_judgement_render.py` green.
- `python3 dev/evals/test_two_layer_render.py` green.
- Audit-shape checks for glyph-flagged-shape (both blocks) flip from red to green.
- Iteration harness shows full audit shape (both blocks rendered to spec) on every eval case.

---

- U6. **Renderer: full coverage report on request (Detected patterns / Agent-assessed patterns sections)**

**Goal:** `format_two_layer` learns a `mode` parameter (or a separate `format_full_report` function) that emits the full-report shape: default content at top, then per-block sections with brief notes + coverage tables, then next-step. Brief-note copy lands as actual text (reviewed with Mae). Default mode keeps the U4/U5 shape (summary + flagged items + next-step). `TOP_LEVEL_SECTION_HEADER_RE` is verified to cover any new top-level headers.

**Requirements:** R5, R8, R10, R11, R12, R13, R14.

**Dependencies:** U4, U5.

**Files:**
- Modify: `humanise/scripts/grade.py` — new mode parameter or new function for full-report rendering. Verify `TOP_LEVEL_SECTION_HEADER_RE` still covers section boundaries in both modes; extend whitelist if any new top-level header is introduced.
- Modify: `humanise/scripts/vocabulary.json` — replace placeholder brief-note templates with reviewed copy (Mae).
- Modify: `humanise/SKILL.md` — Audit step instructions describe default vs full-report flow; next-step prompt copy updated to R8 wording.
- Modify: `humanise/references/example.md` — show both default and full-report shapes end-to-end.
- Test: `dev/evals/test_two_layer_render.py` — full-report mode shape assertions (per-block sections, brief notes present, coverage tables present, next-step prompt at end).

**Approach:**
- Default audit prints summary + flagged items + next-step. Full-report prints default content + per-block sections + next-step.
- Per-block section: `**<Block name>** — <count> of <total> flagged` heading, brief note line, coverage table (auto-detected gets the 8 sub-category tables; agent-assessed gets one flat table).
- The brief-note placeholders from U2 are filled with actual copy here. Drafted by the implementer, reviewed with Mae before commit.
- `TOP_LEVEL_SECTION_HEADER_RE` currently covers `Audit`, `Agent-judgement reading`, `Suggestions`, `Rewrite`, `Draft`, `Next step`. The brainstorm's R12 introduces per-block headers `**Auto-detected patterns**` and `**Agent-assessed patterns**` (replacing `Agent-judgement reading`); update the whitelist to match.

**Patterns to follow:**
- Existing Layer 2's per-category sub-table rendering (`_layer_2_section`, `grade.py:2249`) is the precedent for the auto-detected coverage tables.
- The `category_collapse` template ("**Category** — N/N clear") for fully-clear sub-categories.

**Test scenarios:**
- Happy path: default-mode render on a draft with mixed flags shows summary + flagged items both blocks + next-step. Coverage tables NOT present.
- Happy path: full-report-mode render shows everything in default + per-block headers + brief notes + 8 sub-category coverage tables (auto-detected) + 1 flat coverage table (agent-assessed) + next-step.
- Happy path: zero-flag draft in default-mode shows the three summary lines + (no flagged items) + next-step. No collapse.
- Happy path: zero-flag draft in full-report-mode shows summary + per-block headers (with `0 of N flagged` counts) + brief notes + coverage tables with all rows Clear + next-step.
- Edge case: agent-assessed all-flagged draft — coverage table shows all rows `Flagged` with severity from contract.
- Edge case: composite genre slot with empty watchlist renders the row with `Watchlist coverage pending.` in the Detail column.
- Integration: `_audit_section` (which depends on `TOP_LEVEL_SECTION_HEADER_RE`) extracts the audit body cleanly when both per-block headers are present in full-report-mode.
- Integration: full-report and default modes share the next-step prompt verbatim.

**Verification:**
- `python3 dev/evals/test_two_layer_render.py` green.
- Audit-shape checks for the full-report-mode flip green; default-mode checks already green from U5.
- Manual: render a real iteration-6 sample in both modes, eyeball that brief notes read sensibly and per-block sections aren't truncated.
- Iteration harness uses default-mode by default; full-report-mode is exercised via a new eval assertion or a separate test fixture.

---

- U7. **Architecture: `--judgement-file` CLI + agent contract production**

**Goal:** `grade.py main()` accepts `--judgement-file <path>`. The script reads that JSON, validates against the audit-format-v1 contract's `agent_judgement[]` slot, merges it into the contract before rendering. SKILL.md updated: agent's job is produce structured judgement findings as JSON, call grade.py once, print verbatim. The agent stops writing the agent-judgement block by hand.

**Requirements:** R19, R20.

**Dependencies:** U1 (contract item shape includes severity), U4–U6 (renderer reads agent-judgement contract data and renders both modes).

**Files:**
- Modify: `humanise/scripts/grade.py` — `main()` parses `--judgement-file <path>`. Loads the JSON, validates each item against the contract's `agent_judgement[]` schema, merges into the contract before `format_two_layer` (or full-report mode) runs.
- Modify: `humanise/SKILL.md` — Audit step instructions: (1) agent reads judgement.json for prompts and answer schemas, (2) for each item, agent decides status + answer/findings + severity inferred from registry + writes a JSON file matching the contract's agent_judgement[] item shape, (3) agent calls `grade.py --format markdown --depth <d> --judgement-file <path>` and prints output verbatim. Replaces the current "agent renders the block by hand".
- Modify: `humanise/references/example.md` — show the full agent-supplied JSON and the script's rendered output side by side.
- Test: `dev/evals/test_grade.py` — CLI-mode tests that exercise `--judgement-file` with valid/invalid JSON, missing fields, malformed items.

**Approach:**
- `main()` parser stays hand-rolled. New flag follows the existing `--format` / `--depth` parsing pattern at lines 3053+.
- Validation: the agent-supplied JSON must match the contract's `agent_judgement[]` item shape. Severity defaults to the registry's value if the agent omits it (defensive); ID, status, answer remain agent-supplied.
- SKILL.md changes are the load-bearing user-facing piece. The agent's prompt-following discipline is what makes the architecture work — without it, the audit block drifts.
- The brainstorm's agent-judgement reading is unchanged (still uses judgement.json prompts); only the rendering surface moves from prose-by-agent to JSON-by-agent + markdown-by-script.

**Patterns to follow:**
- Existing `--format` / `--depth` parsing (`grade.py:3053`).
- `_validate_judgement` in registries.py for the validation pattern.

**Test scenarios:**
- Happy path: `grade.py --format markdown --judgement-file <valid.json>` reads the file, merges, renders the agent-assessed block correctly.
- Error path: `--judgement-file <missing.json>` exits with a clear error naming the missing path.
- Error path: `--judgement-file <malformed.json>` exits with a JSON-parse error.
- Error path: `--judgement-file` JSON missing a required item field (e.g. status) exits with validation error naming the item id and the missing field.
- Edge case: `--judgement-file` JSON with extra fields (additionalProperties) — depending on contract strictness, either accepted or rejected. Behavior decided in implementation; documented in commit.
- Edge case: `--judgement-file` JSON with all 8 items present but all clear — script renders the all-items-clear shape (per R9, no collapse).
- Integration: SKILL.md instruction round-trip — an agent following the new instructions produces a valid JSON file and pipes it through grade.py to produce the expected default-mode audit.

**Verification:**
- `python3 dev/evals/test_grade.py` green.
- Iteration harness: a sample iteration with the agent following the new SKILL.md instructions produces audit output that matches the new shape end-to-end.
- Manual: replay one iteration-6 audit through the new flow (manually crafting the agent-judgement JSON from the existing iteration-6 outputs) and compare to the expected new shape.

---

- U8. **Audit-fidelity HTML viewer**

**Goal:** A single-file generator at `dev/tools/render_audit_html.py` that consumes a corpus of audit response.md files (a workspace iteration's outputs) and emits a single static HTML file rendering each audit's output as a writer would see it (markdown rendered with glyphs, bold, tables) alongside the test's pass/fail summary. The iteration runner emits this artefact at the workspace root.

**Requirements:** Mae's added planning constraint #2.

**Dependencies:** U7 (so the audits being rendered are in the new shape).

**Files:**
- Create: `dev/tools/render_audit_html.py` — single-file Python generator.
- Modify: `dev/evals/run_skill_creator_iteration.py` — invoke `render_audit_html.py` at the end of each iteration to emit `audit-fidelity.html` in the workspace root.
- Modify: `README.md` (or `AGENTS.md` per Mae review) — document the new artefact and where to find it.
- Test: `dev/tools/test_render_audit_html.py` — single-file smoke test (input fixture → output HTML contains expected sections).

**Approach:**
- Static HTML, self-contained (CSS inlined, no external deps).
- Per-eval section showing: (a) the rendered audit (markdown converted to HTML — glyphs survive as plain UTF-8, bold renders, tables render), (b) the assertion list with pass/fail, (c) the input draft snippet for context.
- Markdown rendering: use Python's `markdown` library if available, else minimal hand-rolled (the audit's markdown surface is small — bold, tables, glyphs).
- Layout: per-test side-by-side: rendered audit on the left, assertion summary on the right. Reviewed with Mae before completing the unit (specific layout sketch lands during implementation).
- One-shot static — no long-running viewer process. Avoids the PR #5 P3-CODE-51 detached-Popen-leak class of issue.

**Patterns to follow:**
- `dev/tools/render_patterns_md.py` is the precedent — single-file generator, structured-data-in / human-artefact-out, no runtime dependencies beyond stdlib.
- The skill-creator's `eval-viewer/generate_review.py` `--static` mode for the conceptual shape (single-file static HTML), without taking a cross-repo dependency.

**Test scenarios:**
- Happy path: generator on iteration-6 outputs (or a fixture mimicking them) produces HTML that contains: a section per eval, the rendered audit per section, a pass/fail summary per section.
- Happy path: rendered HTML contains visible glyphs (`x` / `!` / `?`) and proper bold/table rendering when opened in a browser.
- Edge case: an eval with zero flagged items renders the all-clear three-line summary in the audit section.
- Edge case: an eval with the runaway-flag pattern (high agent-judgement count) renders all 8 agent-assessed rows in the coverage table.
- Edge case: an iteration with one eval missing a response.md (failed run) renders a placeholder or skips the eval gracefully.
- Integration: iteration runner produces `audit-fidelity.html` at the workspace root after a full iteration finishes; opening it in a browser shows all evals.

**Verification:**
- `python3 dev/tools/test_render_audit_html.py` green.
- Manual: open the generated `audit-fidelity.html` in a browser, confirm the rendered audit looks right (glyphs, bold, tables, severity column visible).
- Iteration harness on a small subset (`--only` flag) produces the artefact in <30 seconds beyond the existing iteration time.

---

- U9. **Final iteration + baseline regen + plan close-out**

**Goal:** Run a full iteration on the final shape (iteration-7 or whatever the next number). Confirm performance numbers hold or improve vs iteration-6. Regenerate `dev/evals/diff_baseline/` only if any contract field shifted (it shouldn't have between U1 and U9 — U1 already regen'd). Close the plan: frontmatter `status: completed`. Update README's auto-block to reflect the new iteration.

**Requirements:** all origin success criteria.

**Dependencies:** U1–U8.

**Files:**
- Generated: `dev/skill-workspace/iteration-N/` (full iteration outputs).
- Generated (or unchanged): `dev/evals/diff_baseline/*.json` (regen only if drift detected; expected to be unchanged from U1's regen).
- Modify: `README.md` (auto-updated `<!-- performance:start -->` block by `build_performance_report` → `update_readme_performance_block`).
- Modify: `humanise/references/example.md` — fix the rendered worked-example glyph + severity for Structural monotony (rendered as `!` / "strong warning" in the audit body and full-report coverage table; registry value is `context_warning`, so the correct glyph is `?` and the table cell is "context warning"). Pre-U7 inconsistency surfaced during U7 implementation; bundled into close-out so the worked example matches the registry the script actually reads.
- Modify: `docs/plans/2026-05-03-001-feat-audit-output-redesign-plan.md` — frontmatter `status: completed`. Also rewrite the **Documentation / Operational Notes** entry "Each unit lands on its own feature branch + PR" to describe the actual convention used: single feature branch (`audit-output/redesign`) with one commit per unit and one PR at the end of U9. This is what the U1–U8 commits actually followed; the original wording is stale post-decision.

**Approach:**
- Run the iteration harness end-to-end with the canonical settings (codex executor, 4 workers, static viewer per the Phase-3 settled pattern).
- `audit-fidelity.html` from U8 is part of the iteration output. Confirm it renders correctly on a real iteration.
- Check `dev/evals/diff_baseline/` against fresh contract output via `dev/evals/diff_renders.py` — expected: zero diff (U1 already aligned).
- README block auto-updates via the existing `update_readme_performance_block` machinery.
- The two example.md / plan-doc fixes above land as small commits before the close-out commit so the PR diff stays clean and reviewable.

**Patterns to follow:**
- Iteration close-out matches PR #15 pattern — full iteration green, README auto-block updated, plan marked completed.

**Test scenarios:**
- Happy path: iteration harness completes; mean pass-rate ≥ iteration-6's number; no regressions flagged in the regression-vs-previous block.
- Happy path: `dev/evals/diff_renders.py` confirms zero baseline drift.
- Happy path: README's `<!-- performance:start -->` block reflects the new iteration number, mean pass-rate, and corpus gaps.
- Edge case: any individual eval that regressed (>5%) is investigated before the plan closes — root cause documented in commit message; either a shape issue (fix), a data-shift artefact (acknowledge), or an audit-shape check tightening (extend).
- Integration: a writer running `python3 humanise/scripts/grade.py --format markdown --depth balanced <draft>` end-to-end gets the new-shape audit output. SKILL.md instructions produce the same output via the agent flow.

**Verification:**
- Iteration mean pass-rate ≥ iteration-6's.
- Audit-shape checks all green across the eval suite.
- `audit-fidelity.html` renders correctly in a browser.
- README block auto-updated.
- Plan frontmatter set to `status: completed`.

---

## System-Wide Impact

- **Renderer pipeline (`grade.py`)** — the load-bearing surface for U4–U7. Three reviewable steps prevent a single bad merge from rolling back the whole rework.
- **Contract (`audit-format-v1.json`)** — additive change in U1 (severity on agent_judgement[] items). Schema version unchanged. Diff baselines regenerate in the same commit.
- **Vocabulary registry (`vocabulary.json`)** — central rename surface. U2 sweeps user-facing strings; internal field names stay.
- **SKILL.md** — load-bearing for U7. The agent's contract-production discipline depends on the SKILL.md instructions being explicit and consistent. PR-#15-style sweep convention applies.
- **Iteration harness (`run_skill_creator_iteration.py`)** — wires audit-shape checks into eval grading. Each new check needs a call-site here in lockstep with the renderer.
- **diff_baseline + diff_renders.py** — JSON-equivalence gate. Baseline regen happens in U1 only; U2–U9 must show zero diff.
- **HTML viewer surface (U8)** — new artefact. Sits at the workspace root per iteration; documented in repo conventions.
- **Unchanged invariants:** `humanise/scripts/patterns.json` schema, `human_report` contract shape (except the U1 severity addition), the four-action skill model (Audit / Suggestions / Rewrite / Write), the depth-dial section in SKILL.md, the corpus-paired evals at `dev/evals/corpus.json`.

---

## Risks & Dependencies

| Risk | Mitigation |
|---|---|
| `_section_text` boundary regex truncates new full-report sections (the brainstorm's deferred Q3) | U6 explicitly verifies `TOP_LEVEL_SECTION_HEADER_RE` covers `**Auto-detected patterns**` and `**Agent-assessed patterns**` headers. Dedicated test fixture confirms section boundaries hold. |
| catalogue_hits-style measurement drift on the new flagged-items shape | U3 lands the harness fixture for the new `<glyph> **<name>**` opener before U4–U7 ship. The fixture in `dev/evals/test_iteration_harness_measurement.py` is the canonical regression check. |
| Partial pressure → signal stacking sweep (PR #5 P1-DOC-12 pattern) | U2 sweeps all user-facing surfaces in one commit. `LEGACY_LITERALS` test fails on any "pressure" reappearance in vocabulary.json / SKILL.md / patterns.md / example.md. |
| Severity assignments per agent-judgement item don't reflect intent | Mae reviews proposed assignments before U1's commit lands; severity values are not pre-decided in this plan. |
| Brief-note copy reads as filler or jargon | Mae reviews drafted copy before U6's commit lands; placeholders ship in U2. |
| `--judgement-file` validation is too strict and breaks valid agent output | U7 starts with permissive validation (extra fields allowed); strictness can tighten in a follow-up unit if drift becomes a problem. |
| HTML viewer (U8) starts simple, layout doesn't fit Mae's review style | U8 produces a layout sketch first, reviewed with Mae before completing; iteration is part of the unit, not a follow-up. |
| Renderer split into 3 units leaves an intermediate state where partial new-shape and partial old-shape co-exist | Each renderer unit is reviewable on its own. Audit-shape checks gate green-ness per unit; harness tests catch any half-rendered output. |
| Diff-baseline drift between U1 and U9 | U2–U9 required to show zero diff against U1's regenerated baselines. Caught at every PR by `dev/evals/diff_renders.py`. |

---

## Documentation / Operational Notes

- **All nine units land on a single feature branch (`audit-output/redesign`) with one commit per unit; one PR opens at the end of U9.** Per-unit commit messages follow `audit-output: U<N> — <descriptive name>`. This replaces the per-unit-PR convention the plan was originally drafted against — keeping the redesign reviewable as a coherent whole avoided cross-unit churn (each renderer step depends on the previous; per-unit PRs would have fragmented review).
- **The iteration harness must run green per commit** (mean pass-rate not below iteration-6's; no regressions in the regression-vs-previous block). Mae and the implementer review the eval-suite outputs at the close of U9 before the single PR opens.
- **diff_baseline regen is documented explicitly in the commit message** for U1 (the contract-change unit). U2–U9 must show zero diff.
- **U2's "pressure" rename sweep is one commit, not many.** Partial sweeps are the failure mode (PR #5 P1-DOC-12).
- **U6's brief-note copy and U1's severity assignments are review checkpoints.** Each draft is presented to Mae before the unit's commit lands. The brainstorm explicitly defers both to implementation.
- **U7's SKILL.md change is the load-bearing user-facing piece of the architecture rework.** The agent's prompt-following discipline depends on the instructions being explicit; review carefully.
- **Plan close-out** (U9) updates the plan's frontmatter status and adds a `docs(plan): mark audit-output redesign completed` follow-up commit.

---

## Sources & References

- **Origin document:** [dev/brainstorms/2026-05-03-audit-output-redesign-requirements.md](dev/brainstorms/2026-05-03-audit-output-redesign-requirements.md)
- **Prior plan (foundation):** [docs/plans/2026-04-30-001-feat-audit-report-redesign-plan.md](docs/plans/2026-04-30-001-feat-audit-report-redesign-plan.md) (Phase 3 / U11–U13 ships the two-layer renderer + agent-judgement parallel block this plan extends)
- **Recent PRs that establish convention:** #14 (Phase 3 SKILL.md template), #15 (iteration-harness measurement + Layer-1 quote determinism), #16 (yaml→json registry migration), #17 (this brainstorm doc)
- **Code references:** `humanise/scripts/grade.py` (renderer + audit-shape checks), `humanise/scripts/registries.py` (registry API), `humanise/scripts/contracts/audit-format-v1.json` (contract schema), `humanise/scripts/{vocabulary,patterns,judgement}.json` (registry data), `dev/evals/run_skill_creator_iteration.py` (iteration harness), `dev/evals/diff_renders.py` + `dev/evals/diff_baseline/` (JSON-equivalence gate), `dev/tools/render_patterns_md.py` (U8 precedent).
