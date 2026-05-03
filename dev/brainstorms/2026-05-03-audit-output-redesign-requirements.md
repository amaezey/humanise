---
date: 2026-05-03
topic: audit-output-redesign
---

# Audit output redesign

## Summary

Restructure the humanise audit so the script renders both halves uniformly, the summary tells the reader what was checked and what fired, and per-block content is symmetric on shape and progressive on disclosure. The default audit is a compact summary plus flagged items with examples; the full coverage report is available on request. Severity replaces the action column in coverage tables, agent-judgement items gain a severity field, and "pressure" is renamed to "signal stacking" with an inline definition.

---

## Problem Frame

The current audit (post-Phase 3 two-layer renderer) has accumulated several shape-level inconsistencies that the writer has to absorb to read it:

- The verdict line counts severity, not check volume — the reader can't see "we ran 38 auto-detected checks, 1 fired" or "we ran 8 agent-judgement checks, 0 fired" at a glance.
- The two halves of the audit treat examples differently. Auto-detected items have their matched phrase in the Layer 1 flagged-items block (with the coverage tables showing only Pattern / Result / Action). Agent-judgement items have their phrases tangled inside the same bullet block they appear in, with no separate coverage receipt. Same audit, two different conventions for the same content.
- "Agent-judgement reading" is internal jargon that names how the check runs (LLM judgement) rather than what the reader is looking at.
- "Pressure" is internal jargon. Its meaning (cumulative weight of weaker AI signals stacking up to a threshold) is opaque to anyone who hasn't worked on the grader.
- The agent renders the agent-judgement block by hand using `judgement.json`, while the regex side is fully script-rendered. Two different rendering paths produce two different shapes and let one half drift while the other is locked in.
- The depth dial maps severity × depth → action for auto-detected items via `_action_for_check`, but agent-judgement items have no severity, so the rewrite logic has no rule to apply to them. A flagged agent-judgement item in a Balanced rewrite has no defined treatment.

The cumulative cost is that the writer scanning the audit can't trust shape parity: where examples live, what each block name means, what "pressure" tells them, and how severity translates to action all vary in ways the doc itself doesn't explain.

---

## Actors

- A1. **Writer** — supplies a draft and reads the audit. Decides what to do next: see the full coverage report, ask for suggestions, request a rewrite, or save the audit to a file.
- A2. **Agent** — Claude Code (or another harness) invoking the humanise skill. Calls `grade.py` for the auto-detected pass, produces a structured judgement contract for the agent-assessed pass, and prints the script's rendered output verbatim.
- A3. **Script** — `humanise/scripts/grade.py`. Owns all rendering: the default audit, the full coverage report, the all-states output. The agent supplies data; the script supplies the words.

---

## Key Flows

- F1. **Default audit on a draft**
  - **Trigger:** Writer hands the agent a draft (or invokes humanise on a file).
  - **Actors:** A1, A2, A3.
  - **Steps:** A2 runs the auto-detected grader. A2 produces the agent-judgement findings (status + severity + reasoning per item, plus phrase-level findings for flagged items). A2 passes both into A3's renderer. A3 emits the default audit shape. A2 prints the result verbatim.
  - **Outcome:** Writer sees the global counts, severity breakdown, signal-stacking state, and flagged items in both blocks (with examples and reasoning), plus the next-step prompt.
  - **Covered by:** R1, R2, R3, R4, R5, R6, R7, R8, R9, R10.

- F2. **Full coverage report on request**
  - **Trigger:** Writer picks "full coverage report" at the next-step prompt.
  - **Actors:** A1, A2, A3.
  - **Steps:** A3 emits the full coverage report shape, which carries everything from the default audit at top, then the per-block coverage tables. A2 prints the result verbatim.
  - **Outcome:** Writer sees the complete coverage receipt — every checked pattern in both blocks with severity, result, and per-item detail — alongside the flagged items already shown in the default.
  - **Covered by:** R11, R12, R13, R14, R15.

---

## Requirements

**Summary lines (every audit shape carries these)**

- R1. The script emits a counts line: `Auto-detected: X of Y flagged · Agent-assessed: A of B flagged`. Y is the total auto-detected check count after suppressing internal meta-checks; B is the total agent-judgement item count.
- R2. The script emits a severity line: `Severity: N hard fail · M strong warning · P context warning`. Counts aggregate across both blocks. Severity labels are space-separated lowercase, sourced from the vocabulary registry's `severity_labels`.
- R3. The script emits a signal-stacking line. When clear: `Signal stacking: clear (weaker AI signals are not accumulating)`. When triggered: `Signal stacking: triggered — N of T threshold (<contributing-component-list>)`. The parenthetical / em-dash clause is the inline definition that replaces the separate explanation paragraph.
- R4. Signal stacking renames the concept formerly called "pressure" everywhere it appears in the user-facing audit. Internal data fields and registry keys may keep their existing names.

**Default audit (the compact view)**

- R5. The default audit emits, in order: the `Audit` header, the counts line (R1), the severity line (R2), the signal-stacking line (R3), the auto-detected flagged items, the agent-assessed flagged items, the next-step prompt.
- R6. Auto-detected flagged items render in glyph shape: `<glyph> **<short_name>** — "<phrase>"`. Glyphs are `x` for hard fail, `!` for strong warning, `?` for context warning. Phrase list caps at three with a `(+N more)` overflow when more phrases are present. Structural patterns with no quotable instance render as `<glyph> **<short_name>**`.
- R7. Agent-assessed flagged items render in glyph + sub-bullet shape:
  ```
  <glyph> **<item label>**
    - "<phrase>" — <why>
  ```
  Multiple findings under one item are sub-bullets under a single header line. Glyph signals severity as in R6. State-type items (where the answer is a state value rather than a phrase, e.g. "register holds without breaks") render the value as the sub-bullet content.
- R8. The next-step prompt for the default audit reads: `**Next step**\nWant the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?` — verbatim string from the registry.
- R9. The default audit retains its full shape even when nothing is flagged and signal stacking is clear. There is no all-clear collapse; the standard summary lines plus the next-step prompt are short enough.
- R10. The default audit contains no calibration text about "human prose can fail some checks" — that calibration lives in the rewrite depth-question, surfaced when the user picks "full rewrite", not in the audit body.

**Full coverage report (on request)**

- R11. The full coverage report opens with the same content the default audit emits (R5–R8), then continues with per-block sections, then the same next-step prompt at the end.
- R12. Each per-block section has the same structure: `**<Block name>** — <count> of <total> flagged` header → one-line brief note explaining what the block checks → coverage table(s).
- R13. The auto-detected coverage uses 8 sub-category tables in the existing patterns.md heading order: Content patterns, Language and grammar, Style, Communication, Filler and hedging, Sensory and atmospheric, Structural tells, Voice and register. Sub-categories where every check is clear collapse to a one-liner; sub-categories with at least one flagged check render the full table including clear rows for coverage.
- R14. The agent-assessed coverage is one flat table covering all eight items.
- R15. Both coverage tables share the column shape: `Pattern | Severity | Result | Detail`. Severity uses the same labels as R2. Result is `Flagged` or `Clear`. Detail is sourced as: pattern `guidance` (auto-detected flagged), empty (auto-detected clear), agent's value/reasoning answer (agent-assessed clear), or `(see above)` (agent-assessed flagged) — pointing back to the flagged-items block already shown earlier.

**Severity model**

- R16. Each agent-judgement item in `judgement.json` carries a severity field (`hard_fail` / `strong_warning` / `context_warning`), assigned during planning per item. The agent populates status (clear / flagged) at runtime; severity is intrinsic to the item.
- R17. Rewrite action selection uses the same severity × depth → action mapping for both blocks. At Balanced depth, hard fail and strong warning → Fix; context warning → Disclose or ask before preserving. At All depth, every severity → Fix. The depth dial documentation (`humanise/SKILL.md` "The depth dial" section) is the canonical statement of this mapping.
- R18. The Action column is removed from coverage tables. The action that applies to any flagged row is read from the depth dial doc, not duplicated per row.

**Architecture**

- R19. The script (`humanise/scripts/grade.py`) renders all visible audit shapes — default, full report, and any future variant. The agent's role for any audit is: produce structured input data, call the script, print the script's output verbatim. The agent does not paraphrase, summarise, lower-case, or re-render any block.
- R20. The agent supplies the agent-judgement findings to the script as a structured contract (status, severity, answer, per-finding phrase + why for list-shape items, genre + watchlist findings for the composite item). The script consumes this contract and renders it with the same template logic that renders the auto-detected side.

**Vocabulary and templates**

- R21. All user-facing strings (block headers, severity labels, signal-stacking copy, next-step prompt, brief notes) live in `humanise/scripts/vocabulary.json` and are looked up via `registries.string_for(...)`. No user-facing strings are hard-coded inside `grade.py` rendering functions.
- R22. Brief-note copy for each block is drafted by the agent during implementation and reviewed by the writer (A1) at that point. The brainstorm captures the requirement to *have* brief notes; the words themselves are deferred.

---

## Acceptance Examples

- AE1. **Covers R5, R9.** Given a draft with zero flagged items in both blocks and signal stacking clear, when the agent renders the default audit, the output contains the `Audit` header, counts line showing `0 of Y flagged` and `0 of B flagged`, severity line showing `0 hard fail · 0 strong warning · 0 context warning`, signal-stacking line showing `Signal stacking: clear (...)`, an empty body (no flagged items), and the next-step prompt.
- AE2. **Covers R6.** Given a draft that triggers two auto-detected flags (one strong warning carrying a quoted phrase, one context warning structural pattern with no quotable instance), the auto-detected flagged-items block renders the first as `! **<name>** — "<phrase>"` and the second as `? **<name>**` (no em-dash, no phrase clause).
- AE3. **Covers R7.** Given an agent-judgement contract where Faux specificity is flagged with two phrases plus reasons, the agent-assessed flagged-items block renders as `! **Faux specificity**` followed by two sub-bullets, each `  - "<phrase>" — <why>`.
- AE4. **Covers R15.** Given the same contract, the agent-assessed coverage table shows the row `| Faux specificity | strong warning | Flagged | (see above) |`. For a clear item like Tonal uniformity with the agent's answer `register holds without breaks`, the row shows `| Tonal uniformity | context warning | Clear | register holds without breaks |`.
- AE5. **Covers R10, R17.** When the writer picks "full rewrite" at the next-step prompt, the agent asks for depth (Balanced or All), and that question carries the calibration line "even human text can fail some checks and still read naturally". The audit body itself does not contain that calibration line.

---

## Success Criteria

- A writer reading any audit can answer, without leaving the audit, three questions: how many checks fired (counts line), how serious they are in aggregate (severity line), and whether weaker signals are stacking up (signal-stacking line). Each question maps to one line; nothing requires hover, expansion, or external lookup.
- The two blocks read parallel: the same shape decisions (counts in header, glyph in flagged items, table columns) apply on both sides. A reader can scan one block, learn the convention, and read the other without re-orienting.
- A downstream agent (or a future humanise contributor) can implement R1–R22 without inventing what each block name means, where examples go, or how severity flows into rewrite. The doc plus the depth-dial section are sufficient.
- The default audit is short enough that a writer with a clean draft can read it in under five seconds and decide what to do next.

---

## Scope Boundaries

- Per-pattern rewrite recipes (e.g. "for em dashes, replace with comma or sentence-break") are out of scope. The system stays at severity × depth granularity. Whether to add per-pattern rewrite tactics is a separate brainstorm.
- The exact severity values for each of the eight agent-judgement items are out of scope. The brainstorm commits to giving each item a severity field; planning assigns the values per item.
- The exact CLI shape that lets the agent pass judgement findings to the script (single call with a `--judgement-file` flag, two calls, stdin pipe, etc.) is out of scope. The brainstorm commits to "script renders both blocks from agent-supplied data"; planning picks the mechanism.
- The brief-note copy for each block is out of scope as content. R22 captures the requirement to have brief notes; the words are drafted during implementation review.
- Suggestions, Rewrite, and Write actions' output shapes are out of scope. The audit redesign affects the audit only; downstream actions still consume the audit but their own outputs are unchanged by this brainstorm.

---

## Key Decisions

- **Block names** are "Auto-detected patterns" and "Agent-assessed patterns". These describe how each block is checked (script-detected vs LLM-assessed), not what's checked. Symmetry pair, no internal jargon.
- **Severity replaces Action in coverage tables** rather than adding a fourth column. Severity is intrinsic to each pattern; action is derived from severity × depth. Showing severity preserves the underlying signal and lets the reader compute action by depth, with the depth-dial doc as canonical.
- **Examples live above the coverage table in both blocks** as a flagged-items block. Coverage tables are coverage receipts only. Resolves the asymmetry where auto-detected examples were in Layer 1 and agent examples were inside the bullet block.
- **"Signal stacking" replaces "pressure"** as the user-facing name for the cumulative-weaker-signals concept. Self-explanatory; doesn't require a glossary.
- **Default audit shows examples; full report adds coverage tables.** Progressive disclosure. The default tells the writer what fired in enough detail to act; the full report adds the coverage receipt.
- **No all-clear collapse.** The default audit's three summary lines plus next-step prompt are short enough that collapsing further saves nothing meaningful.

---

## Dependencies / Assumptions

- The script-rendering architecture depends on the agent producing a structured judgement contract that mirrors the existing `human_report` contract shape used by `format_two_layer`. Planning will resolve the exact CLI / data-flow.
- Adding a `severity` field to each item in `judgement.json` is a schema change. The existing `format_agent_judgement` and downstream test suites consume the contract; both will need updating.
- The vocabulary registry already loads strings via `registries.string_for(...)`. New templates and labels (block names, signal-stacking copy, next-step prompt, severity-label space-separated forms) slot into the existing registry mechanism.

---

## Outstanding Questions

### Resolve Before Planning

(none — all product decisions are captured above.)

### Deferred to Planning

- [Affects R19, R20][Technical] Exact CLI / data-flow shape for the agent passing the judgement contract into the script. Candidates: `--judgement-file <path>` flag, stdin pipe, two-call sequence with the script joining outputs.
- [Affects R16][User decision during implementation] Severity assignment per agent-judgement item. Each of the eight items needs a severity (`hard_fail` / `strong_warning` / `context_warning`); the writer reviews proposed values during implementation.
- [Affects R22][User decision during implementation] Brief-note copy for each block. The words are drafted by the agent and reviewed by the writer at implementation time.
- [Affects R13][Technical] How the existing `_section_text` boundary regex in `humanise/scripts/grade.py` interacts with the new "full coverage report" section (which contains nested bold sub-category headers). Likely already handled by the recent `TOP_LEVEL_SECTION_HEADER_RE` work, but worth re-verifying once the new sections are in place.
