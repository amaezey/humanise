---
title: Comprehensive human-eyes project work — prose-last sequencing
type: feat
status: active
date: 2026-04-30
---

# Comprehensive human-eyes project work — prose-last sequencing

## Summary

Build a per-pattern evidence map from the corpus and reference research. Capture every SUSPECT item from this session's ideation and analysis in a hypothesis log so that nothing blocks use of the skill. Sweep the skill files (SKILL.md, references, eval prompts) so they speak with the same canonical voice the README will land on. Then rewrite the README in place as the final synthesis, drawing on the evidence map for the strength column, referencing the hypothesis log from "What's next", and propagating the same voice the sweep applied. Prose work happens last so it does not get overwritten by later structural changes.

---

## Problem Frame

This session generated three layers of work on the human-eyes project:

1. Ideation that produced seven ranked survivors plus three worth-revisiting ideas plus rejected-but-warranted items.
2. Mae's running feedback on direction: KNOW vs SUSPECT split, no infrastructure inflation, do not remove functionality, increase transparency, the README must meet human-eyes's own standards, references preserved with per-pattern traceability, iterate structure before drafting prose.
3. Review of the README on origin/main (the "honest narrative" version with 14 em dashes, "we" voice, contrived contrast in load-bearing positions, undefined jargon) plus a merge of the diverged local main with origin/main that resolved on origin's side for all 12 conflicts (commit `d76d585`, local-only).

The earlier draft of this plan was a "fix Mae's last feedback" plan that put prose first and treated the alignment sweep as out of scope. Mae corrected both: prose work goes LAST so later steps do not overwrite it; and the plan must reflect the comprehensive analysis from ideation, not just the immediate-feedback fixes. This version incorporates both corrections.

---

## Requirements

- R1. `dev/research/2026-04-30-per-pattern-evidence-map.md` exists with one row per pattern (38 rows). Each row has a Strength rating (Strong, Register-coded, or Untested) derived from the evidence hierarchy in `human-eyes/references/patterns.md` plus the corpus findings in `dev/research/2026-04-29-genre-paired-corpus-findings.md`. Each row has a Primary Source citation (and Secondary Sources where multiple sources contributed). Rating logic explained in the file's intro.
- R2. `dev/hypotheses.md` exists with at least 19 entries covering every SUSPECT item surfaced in this session's ideation and analysis. Each entry: Status (open / testing / confirmed / refuted), Source (which finding or idea this came from), Statement (what the hypothesis is), Test (what would actually test it), Stakes (what changes if confirmed; what changes if refuted).
- R3. `human-eyes/SKILL.md`, `human-eyes/references/severity-detail.md`, `human-eyes/references/alternatives.md`, `human-eyes/references/example.md`, `human-eyes/references/process.md`, and `dev/evals/evals.json` (prompt strings only) speak with the canonical voice the README will land on. Specifically: zero em dashes in prose; no "we" / "our" / "us" in authorial voice; no contrived contrast in load-bearing positions; no AI vocabulary in voice; Australian spelling. The four-action vocabulary (must-fix / consider / nudge / context-warning) is consistent across surfaces. "AI tell" replaced with the canonical phrasing throughout.
- R4. README on local main rewritten in place. Voice constraints met. Structure follows: tagline; "What human-eyes does" (high-level overview); install and invoke; what it does well; patterns table with Strength + Source columns; what it doesn't do (yet); what testing showed; what's next (links to `dev/hypotheses.md`); sources. Existing sections (Why this exists, Performance auto-block, Representative output, File structure, Licence) preserved with prose fixes rather than removed. Performance auto-block kept with one transparency caveat. Per-pattern Strength + Source columns added to the patterns table using R1's evidence map. Inline evidence on claims; jargon defined before use; references preserved in full.
- R5. `python3 human-eyes/grade.py --format markdown --depth all README.md` runs and shows the README passing its own audit at the gating action level.
- R6. Mae signs off on each unit before commit. No commits without explicit go-ahead.

---

## Scope Boundaries

- No infrastructure work: no vocabulary registry tooling, no immutable run records, no version stamps, no AGENTS.md / STATUS.md scaffolding files.
- No removal of existing functionality. Depth dial stays. 43-check grader stays. Audit / Suggest / Rewrite / Write / Save modes stay. The Performance auto-block stays in the README.
- No positioning shift. Detection vs review framing stays as currently positioned, per Mae's planning interview.
- The local merge commit (`d76d585`) stays local. Pushing to origin requires Mae's explicit go-ahead and is OUT of scope here.
- `human-eyes/references/voice.md` is NOT touched — it is voice-craft guidance for Rewrite/Write actions, a different artefact from project voice.
- `human-eyes/references/patterns.md` catalogue content is NOT modified except for prose fixes in its intro/header sections if voice issues are present. The 38-pattern catalogue and "Evidence hierarchy from the reference audit" section are read-only inputs to U1.
- `human-eyes/references/kobak-excess-words.csv` is NOT modified (data file).
- `human-eyes/grade.py` is NOT modified — used as a verification tool only.

### Deferred to Follow-Up Work

- Push merged main to origin. Mae's call after reviewing the merged state.
- Bootstrap CIs for corpus claims, corpus growth past N=5 per group, sentence-length-mean as a grader check, calibration golden set, multi-judge ensemble for the eval grader, discrimination metric as a release gate, decoupled corpus repo. All tracked as hypotheses in U2; not actioned in this plan.
- Hypothesis testing for items in `dev/hypotheses.md`: as-and-when capacity allows. Not blocking.

---

## Context & Research

### Relevant Code and Patterns

- `human-eyes/references/patterns.md`: 38-pattern catalogue. Contains an "Evidence hierarchy from the reference audit" section at the top that explicitly categorises sources as Strong empirical backbone vs Useful but tentative style vs Domain and provenance signals. This is the structural input to U1's strength column.
- `human-eyes/references/severity-detail.md`: per-check severity definitions. Touched by U3 sweep for voice fixes.
- `human-eyes/references/alternatives.md`: per-pattern suggested alternative phrasings. Touched by U3 sweep for voice fixes.
- `human-eyes/references/example.md`, `human-eyes/references/process.md`: skill references. Touched by U3 sweep if voice issues are present.
- `human-eyes/references/voice.md`: voice-craft guide for Rewrite and Write actions. NOT modified; different artefact from project voice.
- `human-eyes/SKILL.md`: skill manifest. Touched by U3 sweep.
- `human-eyes/grade.py`: 43-check grader. NOT modified; used as a verification tool (`python3 human-eyes/grade.py --format markdown --depth all README.md`).
- `dev/research/linda-caroll.md`, `dev/research/nyt-chatbot-style.md`, `dev/research/ignorance-ai-field-guide.md`, `dev/research/grammarly-ai-words.md`, `dev/research/web-survey-2026.md`: per-source analyses. Read-only inputs to U1.
- `dev/research/2026-04-29-genre-paired-corpus-findings.md`: corpus-level findings from N=5 testing. Read-only input to U1.
- `dev/research/2026-04-29-readme-research-section-intent.md`: Mae's notes on how the README's research section should work. Read-only input to U4.
- `dev/reviews/2026-04-30-pr5-review-findings.md`: the multi-reviewer review. Source for several U2 hypothesis entries and the README findings this plan addresses (P0-DOC-01, P0-DOC-02, P0-DOC-03, P1-DOC-06, P1-DOC-07, P1-DOC-09, P1-DOC-12, P1-DOC-19).
- `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md`: ideation artefact with seven survivors, worth-revisiting, and rejection summary. Source for most of U2's hypothesis entries.
- `dev/evals/evals.json`: eval prompts. Touched by U3 sweep (prompt strings only, not structure).

### Institutional Learnings

- `docs/solutions/` does not exist in this repo. Establishing it is captured as a hypothesis in U2 (entry #14), not actioned in this plan.

### External References

- The README's existing Sources section already cites the relevant external research. No additional external research is needed for this plan; the work is editorial fidelity to existing claims plus surfacing the per-pattern evidence map that has been latent in `patterns.md` and the corpus findings.

---

## Key Technical Decisions

- **Sequencing: prose last.** Per Mae's correction, prose work happens after all structural and data work so that later changes do not overwrite the prose. U1 (evidence map), U2 (hypothesis log), and U3 (skill-files sweep) all complete before U4 (README rewrite).
- **Scope includes the alignment sweep.** Without U3, the README's voice would diverge from the skill files it references, and the README becomes incoherent again. The sweep is the structural prerequisite for the README rewrite.
- **Hypothesis log captures the comprehensive analysis.** All 19 SUSPECT items from this session's ideation + analysis are captured in U2, including ideas that Mae's filters cut from action. The hypothesis log is for capture not commitment, so killed-but-still-warranted ideas live here for future revisit.
- **Strength column rating method.** Per-pattern strength is derived from two inputs: (1) source category in `patterns.md` "Evidence hierarchy from the reference audit" — Strong empirical backbone vs Useful but tentative style vs Domain and provenance signals; (2) corpus separation in `dev/research/2026-04-29-genre-paired-corpus-findings.md`. **Strong** when empirical backbone AND corpus separation; **Register-coded** when corpus shows it firing on humans at meaningful density; **Untested** when no direct corpus measurement (most rows).
- **Per-pattern source attribution.** Each row carries a Primary Source citation. Multiple-source patterns name the primary in the cell; full attribution remains in the README's Sources section and in `patterns.md` detail.
- **Project voice spec.** Lives in this plan, applied to both U3 and U4. Constraints: zero em dashes; no "we" / "our" / "us" in authorial voice; no contrived contrast in load-bearing positions; no AI vocabulary; no "Let's explore" section starters; Australian spelling; active voice; varied sentence length.
- **Voice-constraint enforcement via grader self-audit.** After U4, run `python3 human-eyes/grade.py --format markdown --depth all README.md`. Iterate the rewrite until the grader runs clean at the gating action level.
- **README rewrite is surgical.** Existing structure preserved. Section ordering rearranged per R4. Prose rewritten section by section. Performance auto-block kept with a one-line transparency caveat. Representative output section kept (it is the most direct way to show what the skill produces).
- **Iterate structure before drafting prose.** U4 begins with a structural skeleton agreed with Mae before any prose drafting.
- **Hypothesis log format.** Plain markdown. Each hypothesis is an H2 section with five named fields below it (Status, Source, Statement, Test, Stakes). No tooling, no frontmatter system.
- **Local merge commit stays local.** The diverged history was resolved during this session by merging origin/main into local main and resolving 12 conflicts in favour of origin (commit `d76d585`). That commit is local-only; pushing to origin is out of scope here and requires Mae's explicit go-ahead.

---

## Open Questions

### Resolved During Planning

- **Scope: just the README, or wider?** Wider. Per Mae's correction, the alignment sweep and a comprehensive hypothesis log are in scope. The earlier "README + hypothesis log only" framing was the wrong cut.
- **Sequencing.** Prose last. Mae's explicit correction.
- **Should the README split into narrative + auto-dashboard?** No. Mae's "do not remove functionality" plus this plan's "no infrastructure" boundary settle it. Performance auto-block stays in the README with a transparency caveat.
- **Should detection framing be dropped entirely?** No for action; yes for capture. Mae confirmed in interview to keep current positioning. The hypothesis is captured in U2 entry #3 for future revisit.
- **Should the patterns table show grader severity (must-fix / consider / nudge / context-warning) instead of corpus-derived strength?** No. Strength is corpus-derived (what the data shows). Severity is a separate axis (what the grader does on a fire). The README explains both; the table column is strength because that is what the user needs to interpret a flag.
- **Where does the plan live, where does the hypothesis log live?** Plan: `dev/plans/2026-04-30-readme-rewrite-and-hypothesis-log.md` (this file). Hypothesis log: `dev/hypotheses.md`. Mae confirmed.
- **Is `human-eyes/references/voice.md` the canonical project voice spec for the sweep?** No. voice.md is voice-craft for Rewrite/Write actions, a different artefact. Project voice constraints live in this plan and are applied to both U3 and U4.

### Deferred to Implementation

- Exact wording of the "What human-eyes does" high-level paragraph in U4. Drafted during U4; iterated with Mae before commit.
- Specific phrasings to replace each "we" / "our" usage in U3 and U4. Pattern: "the skill" or passive voice where the actor is unimportant; first person singular ("I") only where the agency is genuinely Mae's voice.
- Whether the "Two audiences, two rules" section in the README gets reworded (likely) or removed (possibly). Decision falls out of structural rewrite during U4.
- The exact canonical phrasing that replaces "AI tell" across U3 and U4. Candidates: "review priority", "high-correlation pattern", "AI-correlated pattern". Decision early in U3.
- Whether `human-eyes/references/process.md` and `human-eyes/references/example.md` need voice fixes. Confirmed during U3 file inspection.

---

## Implementation Units

- U1. **Build per-pattern evidence map**

**Goal.** A new file at `dev/research/2026-04-30-per-pattern-evidence-map.md` mapping each of the 38 patterns to (Strength, Primary Source, Secondary Sources). This data is the source the README's Strength column draws from in U4.

**Requirements:** R1

**Dependencies:** None.

**Files:**
- Create: `dev/research/2026-04-30-per-pattern-evidence-map.md`
- Read-only: `human-eyes/references/patterns.md`, `dev/research/2026-04-29-genre-paired-corpus-findings.md`, `dev/research/{linda-caroll, nyt-chatbot-style, ignorance-ai-field-guide, grammarly-ai-words, web-survey-2026}.md`

**Approach:**
1. Read `human-eyes/references/patterns.md` end to end. Extract for each pattern: name, source attribution from inline notes, category in the "Evidence hierarchy from the reference audit" section.
2. Read `dev/research/2026-04-29-genre-paired-corpus-findings.md`. Extract per-pattern corpus separation results where present.
3. For each pattern, derive Strength: **Strong** when empirical backbone in the evidence hierarchy AND not contradicted by corpus, OR clear corpus separation. **Register-coded** when corpus shows the pattern firing on humans at meaningful density (manufactured insight, triads, anaphora, contrived contrast, etc.). **Untested** when no direct corpus measurement.
4. Cross-reference the per-source files in `dev/research/` for source attribution detail where patterns.md does not name a single source.
5. Write the file with: a one-paragraph intro explaining the rating logic; a table with columns # / Pattern / Strength / Primary Source / Secondary Sources / Notes.

**Patterns to follow:** Match the prose style of existing `dev/research/` files. Voice constraints from this plan's Key Technical Decisions.

**Test scenarios:**
- Happy path: file exists at the named path with 38 rows.
- Happy path: each row has Strength (one of Strong / Register-coded / Untested) and Primary Source.
- Edge case: patterns where multiple sources contributed have Secondary Sources populated.
- Edge case: rating logic explained in intro is consistent with what the rows actually show.

**Verification:**
- File present.
- All 38 patterns covered.
- Rating logic in intro matches the per-row ratings.

---

- U2. **Comprehensive hypothesis log**

**Goal.** Create `dev/hypotheses.md` with every SUSPECT item from this session's ideation and analysis. Each entry self-contained and scannable.

**Requirements:** R2

**Dependencies:** None.

**Files:**
- Create: `dev/hypotheses.md`

**Approach:**
1. Define the per-entry shape: H2 section title (the hypothesis name); fields below (Status, Source, Statement, Test, Stakes). Plain markdown. No tooling.
2. Write a one-paragraph intro explaining the format and the principle: hypotheses live here so they do not block use of the skill; testing happens as capacity allows.
3. Write the 19 initial entries:
   1. Continuous calibrated scoring per pattern (was ideation survivor #4)
   2. Comparison-engine product reframe (was W2)
   3. Drop detection framing entirely (was a meta-question; Mae kept current positioning)
   4. Single-source vocabulary registry + JSON audit-format contract (was survivor #1)
   5. Editorial gate on README — split into hand-edited narrative + auto-generated dashboard (was survivor #2)
   6. Immutable run records + grader/corpus version stamps (was survivor #3)
   7. 5-check gating grader + 38-pattern advisory catalogue (was survivor #5)
   8. Audience-aware voice — one engine, two personas via invocation (was survivor #6)
   9. Field-guide voice with explicit similar-species disambiguation per pattern (was W1)
   10. Pharmacovigilance-shape user-reported false-positive intake (was W3)
   11. Register-coded vs rewriter-imports-own-tells interpretation of manufactured insight
   12. Genre-aware threshold calibration
   13. Sentence-length mean as a grader check
   14. AGENTS.md + STATUS.md + active-plan invariant + `docs/solutions/` learnings store (was survivor #7)
   15. Decoupled corpus repo / submodule with SHA-pinned consumption
   16. Multi-judge ensemble for the eval grader, with disagreement surfaced
   17. Calibration golden set (~30 hand-labelled samples) gating any grader change
   18. Discrimination metric as release gate (length-normalised gap with bootstrap CI)
   19. Bootstrap confidence intervals on corpus claims

**Patterns to follow:** Match the prose style of existing `dev/research/` files. Voice constraints from this plan's Key Technical Decisions.

**Test scenarios:**
- Happy path: file exists with at least 19 H2 sections.
- Happy path: each entry has all five fields.
- Edge case: zero em dashes in the file.
- Edge case: no authorial "we" / "our" / "us".

**Verification:**
- File present.
- All 19 entries with five fields each.
- `grep -c '—' dev/hypotheses.md` returns 0.

---

- U3. **Skill-files alignment sweep**

**Goal.** Apply the canonical voice across the skill files so they speak the same language the README will land on.

**Requirements:** R3

**Dependencies:** Decision early in U3 on the canonical phrasing that replaces "AI tell" (likely "review priority"; final choice in U3).

**Files:**
- Modify: `human-eyes/SKILL.md`
- Modify: `human-eyes/references/severity-detail.md`
- Modify: `human-eyes/references/alternatives.md`
- Modify: `human-eyes/references/example.md` (only if voice issues present)
- Modify: `human-eyes/references/process.md` (only if voice issues present)
- Modify: `dev/evals/evals.json` (prompt strings only, not structure)

NOT modified: `human-eyes/references/voice.md`, `human-eyes/references/patterns.md` (catalogue content), `human-eyes/references/kobak-excess-words.csv`.

**Approach:**
1. Decide the canonical phrasing for "AI tell" (likely "review priority" based on Mae's earlier framing).
2. Inspect each file. List the specific change set for each (em dashes, "we" / "our" / "us", contrived contrast, AI vocabulary, undefined jargon, "AI tell" → canonical).
3. Show the change set to Mae before applying. Get sign-off per file or per batch.
4. Apply changes. Verify per-file: `grep -c '—'` returns 0 in modified files; "AI tell" replaced consistently; four-action vocabulary consistent.
5. Mae sign-off before commit.

**Patterns to follow:** Voice constraints from this plan's Key Technical Decisions.

**Test scenarios:**
- Happy path: each modified file has zero em dashes in prose.
- Happy path: "AI tell" replaced with the canonical phrasing throughout.
- Happy path: four-action vocabulary (must-fix / consider / nudge / context-warning) consistent across files.
- Edge case: technical content (variable names, code, frontmatter) untouched.
- Edge case: existing structural content (process steps, severity definitions, eval IDs) preserved.

**Verification:**
- `grep -c '—' human-eyes/SKILL.md human-eyes/references/*.md dev/evals/evals.json` returns 0 across modified files (data files exempt).
- `grep -c "AI tell" human-eyes/SKILL.md human-eyes/references/*.md dev/evals/evals.json` returns 0 (replaced everywhere).
- Mae signs off before commit.

---

- U4. **README rewrite — prose last**

**Goal.** Rewrite `README.md` in place. Voice constraints met. Structure follows R4. Per-pattern Strength + Source columns added from U1 data. References U2 hypothesis log from "What's next". Voice consistent with U3 sweep.

**Requirements:** R4, R5

**Dependencies:** U1 (evidence map), U2 (hypothesis log linked), U3 (skill files in sync so the README's references to skill vocabulary are coherent).

**Files:**
- Modify: `README.md`

**Approach:**
1. Confirm structural skeleton with Mae (one line per section in the agreed order). Get sign-off before drafting prose.
2. Draft section by section. Each section verified against voice constraints before moving on.
3. Add Strength + Source columns to patterns table using U1's evidence map.
4. Reframe Performance auto-block with a one-line transparency caveat. Do not strip the block.
5. Reword "Two audiences, two rules" to remove its contrived-contrast structure.
6. Verify with `python3 human-eyes/grade.py --format markdown --depth all README.md`. Iterate until clean at the gating action level.
7. Hand to Mae for review. Iterate on her feedback.
8. Commit only on Mae's explicit go-ahead.

**Patterns to follow:**
- Voice constraints from this plan's Key Technical Decisions.
- The structural skeleton order in R4.
- Mae's existing prose voice in `dev/research/2026-04-29-genre-paired-corpus-findings.md` as a voice reference.

**Test scenarios:**
- Happy path: `grep -c '—' README.md` returns 0.
- Happy path: `grep -niE '\b(we|our|us)\b' README.md` returns no matches outside URLs, code blocks, and quoted source titles.
- Happy path: `python3 human-eyes/grade.py --format markdown --depth all README.md` runs clean at the gating action level.
- Edge case: every claim with a number (the +44% figure, "23 words", "n=5", "stdev 17") sits in a section that names the source corpus or links to the research doc.
- Edge case: every pattern row in the table has a Strength cell and a Source cell.
- Edge case: the Sources section retains every entry from the pre-rewrite version (≥17 named sources across Foundation / Pattern research / Academic research / Practitioner guides).
- Integration: README's "What's next" links to `dev/hypotheses.md`.

**Verification:**
- `grep` checks confirm zero em dashes and zero "we" / "our" / "us" in authorial voice.
- Grader self-audit runs clean at the gating action level.
- Patterns table has Strength + Source on every row.
- Sources section retains every entry from the pre-rewrite version.
- Mae signs off before commit.

---

## System-Wide Impact

- **Interaction graph:** `README.md` is the public entry point. `human-eyes/SKILL.md` is the skill manifest invoked by Claude Code. Changes to either are highly visible. `dev/hypotheses.md` and `dev/research/2026-04-30-per-pattern-evidence-map.md` are new and have no existing consumers. Modifications to skill references are visible to the skill itself when loaded.
- **Error propagation:** If the grader self-audit fails on the rewritten README, the rewrite must iterate before commit. No external systems depend on the rewrite.
- **State lifecycle risks:** The Performance auto-block in the README is auto-rewritten by the harness on every iteration run. The U4 rewrite preserves the marker comments so the harness keeps writing into them.
- **API surface parity:** All four action levels (must-fix / consider / nudge / context-warning) and the depth dial (`balanced` / `all`) survive in U3 and U4. Functionality is unchanged.
- **Integration coverage:** `human-eyes/grade.py --depth all README.md` is the verification step. No other integration coverage needed since no code is modified.
- **Unchanged invariants:** Skill functionality (audit / suggest / rewrite / write / save), the 43-check grader, the depth dial, the four action levels, and the PR #5 corpus and harness are unchanged. `human-eyes/grade.py`, `human-eyes/references/voice.md`, `human-eyes/references/patterns.md` (catalogue content), and `human-eyes/references/kobak-excess-words.csv` are not touched.

---

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| README rewrite ships before structure agreed; Mae rejects | U4 step 1 explicitly requires structural sign-off before prose drafting. No prose work without that sign-off. |
| Sweep changes a load-bearing prompt or instruction in evals.json or SKILL.md | U3 step 3 shows the change set per file or per batch to Mae before applying. |
| Per-pattern strength rating wrong for some patterns | Rating logic is documented in U1's intro. Corrections are one-cell edits, not structural changes. The strength column is marked as "directional, refines as corpus grows". |
| README still trips its own audit after rewrite | U4 step 6 runs the grader self-audit before handing to Mae. Iterate until clean. |
| Sweep replaces "AI tell" with a canonical phrase Mae later wants to change | The replacement is a single sed-or-find-replace if needed later. Lower cost than skipping the sweep. |
| Local main and origin/main divergence pushed before review | Out of scope. The merge is local-only until Mae's explicit go-ahead. |

---

## Sources & References

- Origin: this session's conversation with Mae. No upstream brainstorm document.
- Code: `human-eyes/references/patterns.md`, `human-eyes/references/severity-detail.md`, `human-eyes/references/alternatives.md`, `human-eyes/references/voice.md`, `human-eyes/references/process.md`, `human-eyes/references/example.md`, `human-eyes/SKILL.md`, `human-eyes/grade.py`, `dev/evals/evals.json`, `dev/research/2026-04-29-genre-paired-corpus-findings.md`, `dev/research/2026-04-29-readme-research-section-intent.md`, `dev/research/{linda-caroll, nyt-chatbot-style, ignorance-ai-field-guide, grammarly-ai-words, web-survey-2026}.md`.
- Review: `dev/reviews/2026-04-30-pr5-review-findings.md`. This plan addresses the README-related findings (P0-DOC-01, P0-DOC-02, P0-DOC-03, P1-DOC-06, P1-DOC-07, P1-DOC-09, P1-DOC-12, P1-DOC-19) plus the SUSPECT items captured in U2.
- Ideation: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md`. Source for U2 hypothesis entries.
- Session-level summary of approved plan: `/Users/mae/.claude/plans/melodic-purring-oasis.md`.
- Mae's stated principles applied throughout: KNOW vs SUSPECT split (R2 via comprehensive `dev/hypotheses.md`); do not remove functionality (Scope Boundaries); no infrastructure inflation (Scope Boundaries); README must meet human-eyes's standards (R4, R5); preserve full references with attribution and per-pattern traceability (R1, R4); iterate structure before drafting prose (U4 step 1); prose work last (sequencing).

---

## Corrections during execution (2026-04-30)

Plan structure as originally written has drifted from execution intent. These corrections apply.

### R1 correction — evidence map is multi-axis per-pattern, not Strength rating

R1 originally specified a Strength rating per pattern (Strong / Register-coded / Untested) feeding the README's strength column. That conflated multiple dimensions and the rating system was broken. Replaced with per-pattern comprehensive evidence summaries containing:

- Sources (every contributing source, multi-source synthesis where applicable)
- Why it's in the skill (1-2 sentence synthesis)
- How AI uses it (frequency-coded / appropriate-use-coded / both / unclear-from-sources) — analytical field
- Evidence basis (corpus-measured / external-only / both) — analytical field
- Severity (`hard_fail` / `strong_warning` / `context_warning`) — looked up from `human-eyes/grade.py`. Operational alignment to the actual audit. NOT must-fix / consider / nudge / context-warning, that vocabulary was invented.
- Source claims (per-source quotes)
- Notes (caveats, register issues, data limits)

The file is internal/gitignored. Does not feed README.

### R4 correction — README patterns table is Source + Severity, not Strength + Source

R4 originally specified a Strength + Source column. Replaced with Source + Severity (severity from grade.py). Internal multi-axis ratings stay internal; the README is plain-English transparency.

### U1 broken into sub-units after slice work

Original U1 was "build the evidence map". Slice work (7 parallel subagents, one per patterns.md TOC category plus non-numbered grader checks) is complete and saved at `dev/research/2026-04-30-per-pattern-evidence-map.md` with known issues flagged. Cleanup is tracked as:

- **U1b. Citation cleanup.** Replace "(web-survey-2026)" mis-citations with the actual primary source (Nature 2025, Przystalski/Zaitsu/Bisztray stylometry, practitioner guides aidetectors.io/seoengine.ai/SAGE, Abdulhai). Drop or rename "patterns.md operating stance" citations — internal commentary, not external source.
- **U1c. Source gap audit.** Create per-source analysis files for load-bearing sources without one: Wikipedia "Signs of AI writing" (priority), Kobak, Shankar, OpenAI sycophancy, GPTZero, Stanford HAI, Juzek/Ward, Vollmer, Walsh/Preus/Gronski, Clarkesworld, Futurism. Or honestly acknowledge the gap.
- **U1d. Severity lookup.** Look up severity per pattern from `human-eyes/grade.py` and add to each entry.
- **U1e. Formatting normalisation.** Apply a single normalised template to every per-pattern entry. Slices used inconsistent field naming and citation style.
- **U1f. Review with Mae.** Sign-off after U1b-e complete. This is the explicit review step Mae called for.

### Severity vocabulary correction

Severity vocabulary in this project is `hard_fail` / `strong_warning` / `context_warning`. Defined per pattern in `human-eyes/grade.py`. Not must-fix / consider / nudge / context-warning, which was invented in earlier turns of this session.

### Per-source files that exist vs source citations used

`dev/research/` per-source files (verified 2026-04-30):
- `linda-caroll.md` — Caroll
- `nyt-chatbot-style.md` — Kriss/NYT
- `ignorance-ai-field-guide.md` — Guo
- `grammarly-ai-words.md` — Grammarly
- `web-survey-2026.md` — aggregator file covering Nature 2025, stylometry research, practitioner guides, Abdulhai. NOT a primary source itself.

Sources referenced in patterns.md but without per-source files: Wikipedia, Kobak, Shankar, OpenAI sycophancy, GPTZero, Stanford HAI, Juzek/Ward, Vollmer, Walsh/Preus/Gronski, Clarkesworld, Futurism. This is the U1c gap.
