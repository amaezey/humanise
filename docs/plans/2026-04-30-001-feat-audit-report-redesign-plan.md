---
title: "feat: Audit report redesign — dual-layer output, registry-backed architecture"
type: feat
status: completed
date: 2026-04-30
deepened: 2026-05-01
refreshed: 2026-05-02
origin: docs/ideation/2026-04-30-audit-report-redesign-ideation.md
---

# feat: Audit report redesign — dual-layer output, registry-backed architecture

## Summary

Redesign the user-facing humanise audit report. Replace the current per-pattern-blocks output (called unreadable when dogfooded) with a two-layer response — orientation block with severity-glyph per-pattern findings, then a coverage receipt of eight per-category sub-tables with a per-row Action column — plus a parallel agent-judgement block carrying the seven semantic checks regex cannot perform. The redesign rests on a no-op architectural refactor that moves pattern metadata into `humanise/patterns.yaml`, agent-judgement metadata into `humanise/judgement.yaml`, all user-facing strings and prose templates into `humanise/vocabulary.yml`, and pins the audit data shape behind a stable JSON contract at `humanise/contracts/audit-format-v1.json`. Phase 1 resolves the catalogue ↔ checks integrity gaps that block severity recalibration, creates `judgement.yaml` so the new agent-judgement step on the Audit action has a canonical home, and propagates severity into `patterns.md`. Phase 2 lands the architecture as a verbatim-output refactor with a JSON-equivalence diff gate. Phase 3 switches the renderer to the new layout.

---

## Problem Frame

The current audit output renders 43 checks as a single 6-column 43-row Markdown table with a per-pattern block above it. Dogfooding showed two failure modes: density (everything has equal weight) and ordering (the most-flagged pattern can be in the middle of the table). The "what to do next" signal is buried — severity is shown as a tier label without saying what the agent will do with it.

Two integrity gaps in the catalogue ↔ check map (`docs/todos/grader-integrity-gaps.md`) make severity recalibration impossible — 17 patterns in `humanise/references/patterns.md` have no programmatic check, and 8 programmatic checks have no numbered pattern.

The skill also has two epistemologies that the current output conflates: deterministic regex/density checks, and the seven semantic items the agent must read for. SKILL.md's Audit action does not currently fire the seven semantic items as a structured step. The redesign establishes that step with a canonical registry.

See origin: `docs/ideation/2026-04-30-audit-report-redesign-ideation.md`.

---

## Requirements

- R1. Audit output is two layers separated by `---`: Layer 1 orientation (verdict line + per-flagged-pattern blocks for programmatic checks), Layer 2 coverage receipt (eight per-category sub-tables).
- R2. Layer 2 sub-tables map one-to-one with the eight category headings already in `humanise/references/patterns.md` (Content patterns, Language and grammar, Style, Communication, Filler and hedging, Sensory and atmospheric, Structural tells, Voice and register).
- R3. Categories with every check clear collapse to a one-liner (e.g. `Style — 5/5 clear`); no sub-table for that category.
- R4. Sub-tables render three columns: `Pattern | Result | Action`. (Severity is the *driver* of the Action column but is not itself rendered as a column — see R22.)
- R5. Per-flagged-pattern blocks carry severity glyph + pattern name + quoted phrase(s) + one-verb action. They do NOT carry "why this matters" prose; that lives in `humanise/references/patterns.md` and is reachable on drill-in only.
- R6. A parallel **agent-judgement** block follows the programmatic block, also separated by `---`. It carries the seven fixed items plus one polymorphic genre slot (#41), with binary `flagged` / `clear` status — no severity column, no `mixed` state.
- R7. The agent-judgement block uses per-item answer schemas (counted observations, presence checks, list judgements, trichotomies as appropriate), not a single uniform record shape.
- R8. Zero-flagged + zero agent-judgement renders as a single line carrying severity counts (which will all be zero), pressure status, and a next-step prompt; no tables, no confidence label.
- R9. The agent-judgement step fires on the Audit action (new step — the seven items have no canonical implementation today).
- R10. All pattern metadata moves out of `humanise/grade.py` (`CHECK_REPORT_TEXT`, `CHECK_METADATA` including `severity` / `failure_modes` / `evidence_role` / `guidance`, `CHECK_WHY_IT_MATTERS`) and out of `humanise/references/severity-detail.md` and `humanise/references/alternatives.md` into a single registry at `humanise/patterns.yaml`, keyed by `check_id`. Severity and `failure_modes` are required fields. The `guidance` field is audited against `why_it_matters` during U7; if redundant, it folds.
- R11. Agent-judgement metadata lives in `humanise/judgement.yaml` with one record per item plus the polymorphic genre slot, each with a per-item `answer_schema`.
- R12. All user-facing strings (severity tier labels, status labels, action verbs, headline templates, all-clear copy, next-step prompt template, AI-pressure explanation template, drill-in frame strings) live in `humanise/vocabulary.yml`. Per-pattern `why_it_matters` prose stays in `patterns.yaml` (per-pattern, not generic); only the *frame* it renders into lives in vocabulary.
- R13. The audit data shape is pinned by a stable JSON Schema at `humanise/contracts/audit-format-v1.json` with two top-level item arrays (`programmatic_checks`, `agent_judgement`) plus `aggregates` and `metadata`. The contract carries **structured data only** — no pre-formatted English prose. The renderer composes prose by filling vocabulary.yml templates with structured contract fields. The renderer reads only the contract.
- R14. Confidence as a labelled level (Low / Medium / High) is removed. Severity counts in the verdict line plus the AI-pressure boolean carry the necessary signal without a verdict wrapper. `confidence_assessment()` is removed; `aggregates.by_severity` and `aggregates.ai_pressure` carry its inputs forward.
- R15. Every numbered pattern in `humanise/references/patterns.md` either has a programmatic check, is folded into another check (with the fold documented), or is explicitly declared manual / agent-judgement.
- R16. Every entry in `ALL_CHECKS` in `humanise/grade.py` maps to a numbered pattern in `humanise/references/patterns.md` (with sources and rationale) or is removed.
- R17. Severity is declared in `humanise/patterns.yaml` (the source) and propagated to `humanise/references/patterns.md` (a generated view — see R21b).
- R18. Audit-shape evals in `dev/evals/run_skill_creator_iteration.py` assert that every Audit response contains both a programmatic block and an agent-judgement block (or the all-clear single-line case).
- R19. README reflects the dual-layer audit shape and the resolved patterns ↔ checks map.
- R20. Phase 2 produces today's JSON contract output verbatim (excluding `metadata.timestamp` and `run_id`). A JSON-equivalence diff harness on a fixed corpus is the merge gate.
- R21. Phase 3 changes the renderer only. The JSON contract from Phase 2 does not change in Phase 3.
- R21b. `humanise/references/patterns.md` is generated from `humanise/patterns.yaml`. A CI check asserts the on-disk file equals the regenerated output. Patterns.yaml is the master; patterns.md is a generated transparency artefact.
- R22. The audit output surfaces *what severity does* (action consequences at Balanced depth — Fix / Disclose or ask before preserving), not just *what severity is named* (tier labels). Layer 2 carries an Action column derived from severity; severity tier counts remain in the verdict line.
---

## Scope Boundaries

- The audience-aware voice work (PR5 ideation #6 — twin `audit_voice` / `prescriptive_voice` fields per pattern) is NOT in scope. This plan establishes the registry split that would later host that twin-field work.
- The continuous calibrated register-distance score (PR5 ideation #4) is NOT in scope. Severity stays categorical.
- The 5-check gating + 38-pattern advisory cull (PR5 ideation #5) is NOT in scope. All 43 checks remain gating.
- The README split into narrative pitch + auto dashboard (PR5 ideation #2) is NOT in scope here; this plan only updates the README's audit-output description.
- The immutable run records / version stamps (PR5 ideation #3) is NOT in scope.
- The operator-surface conventions (PR5 ideation #7 — AGENTS.md, STATUS.md, `docs/solutions/`) is NOT in scope.
- UI machinery (collapse/expand toggles, drill-in modals) is NOT possible — skills are text-only.

### Deferred to Follow-Up Work

- **Genre-specific watchlist data for #41**: U14 in Phase 1 creates the polymorphic slot in `humanise/judgement.yaml` with the canonical genre list. Populating per-genre watchlist content (academic citations, student-rubric phrases, default poetry quatrains, fiction "as you know" dialogue) lands in a follow-up PR — too large to bundle and not blocking the layout. The runner returns "Genre detected: <genre>. Watchlist coverage pending." until follow-up data lands.

---

## Context & Research

### Relevant Code and Patterns

- `humanise/SKILL.md` (291 lines) — Audit action at line 42; output template at line 53; ends ~line 125. Rewrite action at line 180. SKILL.md:50 already mentions Phase 3 (U11/U12) introducing the all-clear collapse and Layer 1/Layer 2 split — partial groundwork laid.
- `humanise/grade.py` (2763 LOC after Phase 2 — under the 2900 split threshold). Phase 2 migrations:
  - `CHECK_REPORT_TEXT`, `CHECK_WHY_IT_MATTERS`, `CHECK_METADATA` — migrated to `humanise/patterns.yaml` in U7. Accessor: `registries.pattern_for(id)` and helpers `metadata_for`, `report_text_for`, `why_it_matters_for`.
  - `FAILURE_MODE_METADATA`, `SEVERITY_LABELS`, `ACTION_LABELS`, depth-consequence strings, depth-summary strings, every renderer template — migrated to `humanise/vocabulary.yml` in U9. Accessor: `registries.string_for(dotted_key, **placeholders)` plus `severity_label`, `action_label`, `status_label`, `pressure_status`, `failure_mode_metadata`, `depth_consequence_text`.
  - `confidence_assessment()` — removed in U8 per R14.
  - `markdown_checks_table()` — removed in U8; replaced by `_markdown_table_from_contract()` (line 2208) reading from the JSON contract.
- `humanise/grade.py:1852` — `annotate_result()` reads `guidance` via the registry.
- `humanise/grade.py:2033` — `human_report()` returns the audit-format-v1 contract shape.
- `humanise/grade.py:2073` — `format_human_report()`. Replaced by `format_two_layer()` in U11.
- `humanise/grade.py:2198` — `_action_for_check()`. Maps severity + depth → action key (`fix` or `preserve_with_disclosure_or_user_decision`). U11's Action column reads from this.
- `humanise/grade.py:2208` — `_markdown_table_from_contract()`. The 6-column table U11 replaces.
- `humanise/grade.py:2305` — `failure_mode_results()` reads `failure_modes` via the registry.
- `humanise/grade.py:2477-2665` — `check_audit_shape_*` family (ten functions including U5 additions) plus `AUDIT_SHAPE_CHECKS` registry and `check_audit_shape()` dispatcher.
- `humanise/grade.py:2677` — `regrade()`.
- `humanise/references/patterns.md` — eight `## ` category headings (lines 48, 129, 344, 421, 461, 528, 572, 656). Numbered patterns 1-41 plus 23a/31a/35a sub-letters. After R21b, this file becomes a generated view of `patterns.yaml`. The preamble currently says "38 patterns" — stale; U1 fixes this.
- `humanise/references/severity-detail.md` — deep-dive prose for the four most distinctive AI tells.
- `humanise/references/alternatives.md` — vetted alternatives. Migrates into `patterns.yaml` in U7.
- `dev/evals/run_skill_creator_iteration.py:310-329` — `GRADE.check_audit_shape("…", output, input_text)` call sites for audit-shape assertions. New checks land here in U5.
- `dev/evals/run_skill_creator_iteration.py:893-894` — `README_PERFORMANCE_START` / `README_PERFORMANCE_END` markers. The auto-rewritten README block.
- `dev/evals/test_grade.py:35-88` — custom test helpers (`expect_pass`, `expect_fail`, etc.). New test files in this plan follow this convention, not pytest.
- `dev/skill-workspace/iteration-{1..4}/eval-0-audit-ai-cultural/with_skill/run-1/outputs/response.md` — captured outputs (agent-rendered, not `grade.py --format markdown`). Useful as design-space reference, NOT as the U10 baseline (see U10 below).

### Institutional Learnings

None — `docs/solutions/` does not exist in this repo. The PR5 ideation flags this as itself a finding (PR5 idea #7), out of scope here.

### External References

- Vale's rule-author-writes-message architecture is the closest production analogue to the `patterns.yaml` registry shape — pattern metadata is data, not code.
- ESLint / Vale-style common evidence envelope (`{matches, locations, counts, raw}`) is the analogue for U8's evidence shape — a stable contract for the parts the renderer reads, with an opaque `raw` field for per-check oddities.

---

## Key Technical Decisions

- **PR5 ideation #1 is realised by this plan, not duplicated.** PR5 #1 proposed a single `humanise/vocabulary.yaml` keyed by `pattern_id` with twin voice fields. This plan splits that into three files with sharper concerns: `patterns.yaml` (per-pattern data: severity, failure_modes, evidence_role, alternatives, why_it_matters, references), `judgement.yaml` (per-item agent-judgement data: prompt, answer_schema, pattern_ref), `vocabulary.yml` (tone-decision strings and prose templates). PR5 #1's twin `audit_voice` / `prescriptive_voice` fields are explicitly out of scope (PR5 #6 territory).
- **JSON contract carries structured data only — no pre-formatted prose.** The renderer composes prose by merging vocabulary.yml templates (`"X of Y checks were flagged for AI-style writing patterns."`) with structured contract data (counts, IDs, statuses). vocabulary.yml is the genuine source of truth for user-facing strings; changing tone is a vocabulary edit, not a code edit.
- **Phase 2 is a no-op refactor with a JSON-equivalence diff gate.** U10's gate compares `grade.py --format json` output before/after Phase 2 (excluding `metadata.timestamp` and `run_id`). Locking the JSON contract is what proves Phase 2 doesn't change the user-facing path — the agent reads JSON and renders prose; the JSON is the boundary.
- **Severity is propagated, not reconciled.** Severity already lives in `CHECK_METADATA[id]["severity"]` (the only source). The plan propagates it from there to `patterns.yaml` (via U7 migration) and onward to `patterns.md` (via the U15 generator). The previous "two sources to reconcile" framing was wrong.
- **Confidence as a labelled level is removed.** Severity counts plus the AI-pressure boolean already carry the signal; the verdict wrapper (Low/Medium/High) was unkindled categorical claim on bounded-AUROC data and added little beyond relabelling severity composition. The verdict line is now severity counts + pressure status only.
- **Severity surfaces as Action, not as a tier label, in Layer 2.** The writer's actual question is "what does the agent do with this?" The Action column answers that directly: `Fix` (hard_fail or strong_warning at Balanced) or `Disclose or ask before preserving` (context_warning at Balanced). Severity tier counts remain in the verdict line.
- **`agent_judgement[]` is populated by the agent at response-render time.** `grade.py` emits `programmatic_checks` + `aggregates` + `metadata` only. The agent (the LLM running the Audit action) reads `judgement.yaml` for prompts and answer schemas, runs the seven semantic items + polymorphic genre slot itself, and writes `agent_judgement[]` into the same JSON contract before rendering the response. Two writers to the contract; one schema validates both halves.
- **Common evidence envelope on `programmatic_checks[].evidence`.** Every check populates `{quoted_phrases, locations, counts, raw}`. Renderer reads the common fields; per-check oddities live in `raw` (opaque). Replaces the loose `additionalProperties: true` design.
- **Binary status on agent-judgement.** No severity column, no `mixed` state. Sort order within the agent-judgement block is `judgement.yaml` registry order.
- **Polymorphic genre slot is one record, not eight.** `humanise/judgement.yaml` carries a single `id: genre_specific` record with sub-records per genre.
- **`patterns.yaml` is the master; `patterns.md` is generated.** The U15 generator renders `patterns.md` from `patterns.yaml`. Mae edits `patterns.yaml` when adding/modifying patterns; a CI check enforces that `patterns.md` on disk equals the regenerated output.
- **`humanise/grade.py` size budget.** Today 2765 LOC. The registry migration removes ~350 LOC of metadata constants and adds loader call sites + JSON-schema validation. Net should be down. If it crosses ~2900 LOC, split (e.g. `humanise/render.py`).

---

## Open Questions

### Resolved During Planning

- **#37 Neutrality collapse handling**: agent-judgement only. Surface false-balance phrasing stays under `check_false_concession`. Expanding regex coverage is a separate Group A decision in U1.
- **#41 Genre-specific shape**: one polymorphic slot in `humanise/judgement.yaml`. Sub-records per genre.
- **Severity for agent-judgement**: none. Binary status.
- **Layer-2 sub-table columns**: three (`Pattern | Result | Action`). Severity drives the Action column but is not itself a column.
- **Confidence verdict**: removed (R14).
- **All-clear collapse**: single line "X of X clear · agent reading clean · pressure: clear." plus next-step. No tables, no level label.
- **alternatives.md**: migrates into `patterns.yaml` in U7 (no longer a separate flat file at runtime).
- **`agent_judgement[]` writer**: the agent at response-render time. `grade.py` emits the programmatic half only.
- **`patterns.md` source of truth**: generated from `patterns.yaml` (R21b, U15).
- **U6 README update placement**: deferred entirely to Phase 3 (folded into U13). The original Phase-1 placement was wrong — the README will get touched again in Phase 3 anyway when the renderer changes shape, and Phase 2 might shift severities or rename categories that re-invalidate any earlier README work. The README isn't load-bearing for users (it's project marketing), so stale numbers through Phase 2/3 are fine. U13 handles counts, pattern table, and dual-layer description in one pass. Worktree commit `471a460` (the original U6 work) is now narratively orphaned — PR #6 reviewer decides whether to revert it before merge.
- **Reconciling main's humanised README rewrite**: not a plan concern. Mae commits main's uncommitted humanise edits independently on `main` whenever she chooses. U13 will take whatever `main`'s `README.md` is at that point as its base.
- **Pre-existing P1 + P2 fixes already shipped**: P1 (seven unnumbered checks) resolved by `13b4e9d` before this plan update was authored — the unit I drafted as "U16" was a phantom, removed. P2 (unanchored `ALL_CLEAR_LINE_RE`) resolved by `f671cc4` (anchors regex + enforces shape mutex). Both captured in Risks; no plan units needed.

### Resolved by Phase 2 (2026-05-02)

- **Exact `vocabulary.yml` key names**: resolved in U9 — schema lives in `humanise/vocabulary.yml` (sections: `severity_labels`, `action_labels`, `status_labels`, `pressure_status`, `failure_modes`, `depth_consequence`, `depth_summary`, `section_headings`, `inline_labels`, `templates`, `pressure_explanation`).
- **Whether `guidance` is redundant with `why_it_matters` and folds**: resolved in U7 — both kept. Guidance is depth-aware action advice; why_it_matters is rationale.
- **`FAILURE_MODE_METADATA` destination**: resolved in U9 — folded into `vocabulary.yml` under `failure_modes` with `label` and `summary` per entry.
- **Diff-harness corpus for U10**: resolved before U10a — 11 baselines committed under `dev/evals/diff_baseline/` covering 4 cultural/tech/science/wellbeing samples, 3 comparative pairs (Darwin, Woolf, Alamut), 2 synthetic edges (all-clear, hard-fail-only), 1 iteration capture, 1 opinion sample.
- **PyYAML dependency**: resolved in U7 — accepted as required dep.
- **Whether `jsonschema` is added in U8**: resolved — hand-rolled validation in `registries.py`. No library dep added.

### Deferred to Implementation

- *No outstanding items as of 2026-05-02. Phase 3 begins from a settled architecture.*

---

## Output Structure

New files this plan introduces, relative to repo root:

    humanise/
    ├── contracts/
    │   └── audit-format-v1.json          # JSON Schema, pinned contract (U8)
    ├── patterns.yaml                     # per-pattern registry — master (U7)
    ├── judgement.yaml                    # agent-judgement registry (U14, Phase 1)
    ├── vocabulary.yml                    # user-facing strings + prose templates (U9)
    └── registries.py                     # loader + validation (U7)

    dev/tools/
    └── render_patterns_md.py             # generator: patterns.yaml → patterns.md (U15)

    dev/evals/
    ├── diff_renders.py                   # JSON-equivalence verification (U10b)
    ├── diff_baseline/                    # frozen pre-Phase-2 JSON outputs (U10a)
    ├── test_registries.py                # registry loader tests (U7)
    ├── test_audit_contract.py            # JSON contract tests (U8)
    ├── test_vocabulary.py                # vocabulary registry tests (U9)
    ├── test_two_layer_render.py          # Phase 3 layout tests (U11)
    └── test_agent_judgement_render.py    # Phase 3 agent-judgement tests (U12)

The implementer may adjust the structure if implementation reveals a better layout — per-unit `**Files:**` sections remain authoritative.

---

## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification.*

Data flow after Phase 2 lands:

    [input prose]
        │
        ▼
    grade.py
        ├── ALL_CHECKS (programmatic) ─── reads metadata from ─► patterns.yaml
        │
        └── emits ──► audit-format-v1.json (programmatic_checks + aggregates + metadata)
                              │
                              │ ┌─────────────────────────────────────────┐
                              │ │ agent (LLM running Audit action):       │
                              │ │   - reads judgement.yaml (prompts +     │
                              │ │     answer schemas)                     │
                              │ │   - runs the seven semantic items +     │
                              │ │     polymorphic genre slot              │
                              │ │   - writes agent_judgement[] into the   │
                              │ │     same contract                       │
                              │ └─────────────────────────────────────────┘
                              ▼
                         renderer ◄── reads strings from ─── vocabulary.yml
                              │
                              ├── Phase 2 path: format_human_report() (today's text verbatim, U10 JSON gate)
                              └── Phase 3 path: format_two_layer() (Layer 1 + Layer 2 + agent-judgement)

JSON contract shape (illustrative):

    {
      "schema_version": "1",
      "programmatic_checks": [
        { "id": "no-em-dashes",
          "status": "flagged|clear",
          "severity": "hard_fail|strong_warning|context_warning",
          "category": "Style",
          "failure_modes": ["..."],
          "evidence": {
            "quoted_phrases": ["..."],
            "locations": [{"line": 1, "col": 12}],
            "counts": {"total": 3},
            "raw": { /* per-check opaque */ }
          }
        }
      ],
      "agent_judgement": [
        { "id": "tonal_uniformity",
          "status": "flagged|clear",
          "answer": { /* per-item shape */ },
          "evidence": { /* per-item */ }
        }
      ],
      "aggregates": {
        "by_severity": { "hard_fail": 0, "strong_warning": 4, "context_warning": 2 },
        "by_category": { "Style": 2, "Voice and register": 1, ... },
        "ai_pressure": { "triggered": true, "score": 6, "threshold": 4, "components": [...] }
      },
      "metadata": { "run_id": "...", "grader_version": "...", "timestamp": "..." }
    }

No `confidence` block. The verdict line is composed at render time from `aggregates.by_severity` + `aggregates.ai_pressure` using a vocabulary template.

---

## Implementation Units

### Phase 1 — Regression-fix + agent-judgement registry

- U1. **Resolve Group A — patterns described, not enforced**

**Goal:** For each of the 17 entries in Group A of `docs/todos/grader-integrity-gaps.md`, decide one of: (a) write a programmatic check, (b) declare the entry intrinsically manual / agent-judgement and document that, (c) verify the "may already fold into X" hypothesis and either fold or keep standalone. Also refresh the `patterns.md` preamble count (currently says "38 patterns"; actual is 41 numbered + 23a/31a/35a sub-letters).

**Requirements:** R15.

**Dependencies:** None. Reads `docs/todos/grader-integrity-gaps.md`. (Note: that file landed in the worktree via a precursor `chore: track grader-integrity-gaps.md` commit — see Cross-tree note in Risks.)

**Files:**
- Modify: `humanise/references/patterns.md` — annotate each Group A entry with the resolution; refresh preamble count.
- Modify: `humanise/grade.py` — add `check_*` functions for Group A entries decided as programmatic; register in `ALL_CHECKS`; add `CHECK_METADATA` entries.
- Test: `dev/evals/test_grade.py` — one test per new check, following the `expect_pass` / `expect_fail` convention at lines 35-88.

**Approach:**
- Five "intrinsically manual" entries (#28, #30, #35, #36, #41) stay manual; they appear in the agent-judgement registry from U14. Annotate `patterns.md` with the explicit declaration.
- Twelve "could be programmatic" entries (#2, #5, #11, #12, #13, #14, #15, #16, #18, #20, #21, #37) — for each, decide write/fold/manual.
- For #15, #20, #21, verify the "may already fold into X" hypotheses via `grep` in grade.py before deciding.
- For #37, the ideation already resolved as agent-judgement-only; just annotate.

**Patterns to follow:**
- Existing `check_*` functions in `humanise/grade.py` — pure functions returning `{"text": id, "passed": bool, "evidence": str}`.
- `CHECK_METADATA` entries with `severity`, `failure_modes`, `evidence_role`, `guidance`.
- `dev/evals/test_grade.py:35-88` test convention (custom helpers, no pytest).

**Test scenarios:**
- Happy path: each new check fires on its target phrase pattern using a hand-authored fixture.
- Happy path: each new check stays clear on a benign sample.
- Edge case: structural-shape Group A patterns (e.g. #14) tested on multi-paragraph fixtures.
- Edge case: each "may already fold" entry has a verified resolution recorded in `patterns.md`.
- Integration: meta-test reads `patterns.md` and asserts every Group A entry has a resolution marker.

**Verification:**
- All 17 Group A entries have a resolution marker in `patterns.md`; preamble count refreshed.
- New checks pass `test_grade.py`.

---

- U2. **Resolve Group B — checks enforced, not documented**

**Goal:** For each of the 8 entries in Group B of `docs/todos/grader-integrity-gaps.md`, decide one of: (a) write a numbered patterns.md entry, (b) fold into an existing numbered pattern, (c) remove the check.

**Requirements:** R16.

**Dependencies:** None.

**Files:**
- Modify: `humanise/references/patterns.md` — add new numbered entries; mark folds.
- Modify: `humanise/grade.py` — remove dropped checks; rename for fold cases.
- Modify: `humanise/references/severity-detail.md` — extend if a Group B check joins the four-most-distinctive set.
- Test: `dev/evals/test_grade.py` — preserve tests for surviving checks; remove tests for dropped checks.

**Approach:**
- Three (`check_manufactured_insight`, `check_corporate_ai_speak`, `check_signposted_conclusions`) are core 2026 AI tells with established prose evidence — write numbered entries with sources from `dev/research/` and `humanise/references/severity-detail.md`.
- The 9ce1cec asymmetry batch (`bland_critical_template`, `soft_scaffolding`, `negation_density`, `overall_signal_pressure`) — read each implementation and the source-review session notes in `dev/research/`; decide write-entry vs fold vs drop. `check_overall_signal_pressure` is a meta-check (rolls up other signals); likely needs a special-case entry rather than a numbered pattern.
- `check_nonliteral_land_surface` — check whether it folds into existing structural-tells coverage.

**Patterns to follow:**
- Existing numbered patterns in `humanise/references/patterns.md` — header + Words to watch + Before / After + evidence sources.

**Test scenarios:**
- Happy path: every preserved Group B check has a numbered patterns.md entry visible by `grep`.
- Happy path: every Group B check decided as "fold" has a comment in grade.py pointing at the parent pattern.
- Happy path: every Group B check decided as "drop" is removed from `ALL_CHECKS` and its tests deleted.
- Integration: meta-test enumerates `ALL_CHECKS` and asserts every check_id maps to a patterns.md entry.
- Integration: `check_overall_signal_pressure` keeps its existing semantics — corpus run before/after produces the same trigger pattern on iteration-1..4 fixtures.

**Verification:**
- Every check in `ALL_CHECKS` is documented or removed.
- patterns.md has new numbered entries for the surviving Group B set.

---

- U3. **Audit and propagate severity**

**Goal:** Audit the per-check severity already declared in `CHECK_METADATA[id]["severity"]`. Propagate severity into `patterns.md` (currently not carried in the human-readable catalogue). Severity is *one* source of truth — `CHECK_METADATA` — that this unit propagates to a second view, not "two sources to reconcile."

**Requirements:** R17.

**Dependencies:** U1, U2 (need a clean check ↔ pattern map first).

**Files:**
- Modify: `humanise/grade.py` — `CHECK_METADATA` severity fields reviewed end-to-end.
- Modify: `humanise/references/patterns.md` — add a severity line to each numbered pattern. (After U15, this is generated; for the U3 turn, hand-edit and let U15 pick it up.)
- Modify: `humanise/references/severity-detail.md` — reconcile any shifts.
- Test: `dev/evals/test_grade.py` — meta-test asserting `CHECK_METADATA[id]["severity"]` matches the patterns.md severity for the same id (until U15 lands, after which the test asserts the generator preserves it).

**Approach:**
- Walk the catalogue in patterns.md order. For each pattern, decide severity: `hard_fail` (provenance / placeholder residue), `strong_warning` (high-signal AI tell), `context_warning` (cluster-meaningful, tolerable alone). Document rationale in patterns.md.
- Constraint: severity changes are limited to (a) resolving documented mismatches between `CHECK_METADATA` and the catalogue, and (b) explicit recalibrations cleared with Mae *before* the change. Discretionary re-tiering doesn't slip in.
- After any severity change, render every `dev/skill-workspace/iteration-*/eval-*/outputs/response.md` corpus sample and capture confidence-level shifts in a summary file (`dev/research/2026-04-30-severity-shift-summary.md`). Mae reviews before merge.
- Audit existing tests in `dev/evals/test_grade.py:1121-1173` for hardcoded severity expectations; update where U3 changes severity.

**Patterns to follow:**
- Existing severity tiers in `humanise/grade.py:1734-1993` (`CHECK_METADATA`).
- The four most distinctive AI tells (em-dashes, manufactured insight, adversarial reframes, generic staccato) keep their current severities.

**Test scenarios:**
- Happy path: every check_id in `ALL_CHECKS` has a severity in both `CHECK_METADATA` and `patterns.md`, and they match (meta-test).
- Edge case: a recalibration that promotes a check from `context_warning` to `strong_warning` shifts confidence appropriately on existing iteration fixtures; expected shifts reviewed.
- Integration: corpus diff summary documents every shift before and after.

**Verification:**
- Severity declarations reconcile across grade.py and patterns.md.
- Corpus shift summary written and reviewed.

---

- U14. **Create `humanise/judgement.yaml` (agent-judgement registry)**

**Goal:** Create the canonical agent-judgement registry. Eight records: `structural_monotony`, `tonal_uniformity`, `faux_specificity`, `neutrality_collapse`, `even_jargon_distribution`, `forced_synesthesia`, `generic_metaphors`, plus one polymorphic genre slot (`genre_specific`) with sub-records per genre. Each record carries `id`, `pattern_ref` (where applicable), `prompt`, `answer_schema` (per-item shape: state / list / presence / trichotomy).

**Requirements:** R6, R7, R11.

**Dependencies:** None. This file pre-dates U7's loader — it lands as a static YAML the agent reads via SKILL.md (U4). U7 later promotes it to registry-loaded.

**Files:**
- Create: `humanise/judgement.yaml`.
- Test: `dev/evals/test_judgement_yaml.py` — schema/shape tests independent of the U7 loader.

**Approach:**
- Author the eight records. Each `prompt` is the question the agent reads; each `answer_schema` defines the shape of the agent's answer.
- For the polymorphic `genre_specific` slot, sub-records cover at minimum: `academic`, `student_essay`, `poetry`, `fiction`, `default`. Each sub-record carries a `watchlist` field (initially empty for non-default genres — populating these is deferred work).
- YAML lints clean. PyYAML round-trips bytes equal (relevant for U10's diff harness later).

**Patterns to follow:**
- The seven items + polymorphic slot are listed in the ideation; this unit makes them canonical.
- YAML structure mirrors `patterns.yaml`'s shape (designed in U7) so the U7 loader can handle both.

**Test scenarios:**
- Happy path: file parses; eight top-level records present.
- Happy path: each record has `id`, `prompt`, `answer_schema`.
- Edge case: malformed YAML fails lint cleanly.
- Integration: SKILL.md (after U4) references this file by path; the agent reads it as part of running the audit-judgement step.

**Verification:**
- File exists with eight records + the polymorphic genre slot.
- Lints clean; round-trips through PyYAML.

---

- U4. **Add the agent-judgement step to the Audit action**

**Goal:** Add a new step to Action 1 (Audit) in `humanise/SKILL.md` that runs the agent-judgement reading on the input. The step reads `humanise/judgement.yaml` (created in U14) for prompts and answer schemas. This is net-new behaviour — earlier skill iterations referenced semantic items in different forms, but the seven-item + polymorphic-genre shape is established here.

**Requirements:** R9.

**Dependencies:** U14 (`judgement.yaml` must exist and be canonical).

**Files:**
- Modify: `humanise/SKILL.md:42-92` — Audit-output template (line 52 onwards) gains the agent-judgement block; new step in the Audit-steps list calls out reading `judgement.yaml`.
- Modify: `humanise/references/process.md` — Step C clarification (or new step) for the Audit-time agent-judgement reading; distinct from the existing structural self-check on rewrite output.

**Approach:**
- Add a new Audit step: "Run the agent-judgement reading on the input, reading `humanise/judgement.yaml` for the canonical list of items and their answer schemas. For each item, record `flagged` or `clear` with per-item evidence."
- Add the agent-judgement block to the Audit-output template, positioned after the programmatic block and separated by `---`. Phase 3 (U11/U12) will redesign both blocks; this unit re-instates the agent-judgement block in a Phase-1-shape that is forward-compatible with the dual-layer redesign.
- Reference judgement.yaml by path. The agent reads the YAML at audit time.

**Patterns to follow:**
- `humanise/SKILL.md:148-189` Rewrite action's reference to `humanise/references/process.md` Step C.

**Test scenarios:**
- Happy path: SKILL.md Action 1 step list includes "Run the agent-judgement reading."
- Happy path: SKILL.md Action 1 output template includes a labelled agent-judgement block.
- Integration: a sample Audit run via `dev/evals/run_skill_creator_iteration.py` produces a response containing both blocks.

**Verification:**
- SKILL.md edit reviewed.
- Representative iteration run produces an Audit response with an agent-judgement block visible.

---

- U5. **Update audit-shape evals to require both blocks**

**Goal:** Add audit-shape assertions that every Audit response contains both a programmatic block and an agent-judgement block (or the all-clear single-line case).

**Requirements:** R18.

**Dependencies:** U4.

**Files:**
- Modify: `humanise/grade.py:2550-2672` — add new `check_audit_shape_*` functions; register in `AUDIT_SHAPE_CHECKS` (line 2656).
- Modify: `dev/evals/run_skill_creator_iteration.py:310-329` — add assertion calls for the new checks.
- Test: `dev/evals/test_grade.py` — unit tests for each new audit-shape check, following the test convention at lines 35-88.

**Approach:**
- Add `check_audit_shape_has_programmatic_block`.
- Add `check_audit_shape_has_agent_judgement_block`.
- Add `check_audit_shape_all_clear_line_format` — for all-clear runs, verifies the single-line response shape ("X of X clear · agent reading clean · pressure: clear" + next-step). No confidence label.
- Wire all three into `AUDIT_SHAPE_CHECKS` and call sites in `run_skill_creator_iteration.py:310-329`.

**Patterns to follow:**
- Existing `check_audit_shape_*` functions at `humanise/grade.py:2550-2672`.

**Test scenarios:**
- Happy path: an Audit response with both blocks passes all three checks.
- Happy path: an all-clear response passes the all-clear check.
- Edge case: a response missing the agent-judgement separator fails.
- Edge case: a response with only the programmatic block fails.
- Edge case: a response with only the agent-judgement block fails.
- Integration: new checks against captured iteration outputs — fail on iterations predating U4 (expected); pass after U4 lands.

**Verification:**
- New audit-shape checks fire correctly on hand-authored fixtures.
- Iteration runs after U4 + U5 pass all audit-shape assertions.

---

- U6. *Removed 2026-05-01 — deferred entirely to U13. See `docs/todos/pr-6-readme-resolution.md`.*

---

- U16. *Removed 2026-05-01 — already shipped in commit `13b4e9d` before this plan update was authored.*

Commit `13b4e9d fix: resolve 7 orphan checks into numbered/sub-lettered entries` promoted 5 checks to numbered patterns (#49 Em dashes, #50 Formulaic openers, #51 Mechanical repeated sentence starts, #52 Sentence length variance, #53 Vocabulary diversity), folded 2 into sub-letter entries (#10a Triad density, #35b Repeated 'This …' chains), and removed the `Severity for unnumbered checks` subsection from `humanise/references/patterns.md`. The P1 finding from `docs/todos/pr-6-code-review-handoff.md` is closed.

U16's U-ID is preserved as a gap.

---

- U17. *Removed 2026-05-01 — never should have existed.*

I (the agent on 2026-05-01) invented a "README dogfood test" unit and a corresponding R23 requirement. Mae had asked to test the Phase 1 changes; I overshot by inventing a regression target for the README. Removed. The README is project marketing — testing the grader against its own example table is a self-defeating exercise (it always fails because the table contains examples of every pattern by design). The U-ID is preserved as a gap.

---

### Phase 2 — Architecture as no-op refactor

- U10a. **Capture diff baseline (pre-U7)**

**Goal:** Capture pre-Phase-2 JSON output from `grade.py --format json` over the U10 corpus into `dev/evals/diff_baseline/`. Lock as a frozen artefact so U7-U9 changes can be diffed against it.

**Requirements:** R20.

**Dependencies:** None — but lands BEFORE U7 starts, after corpus selection.

**Files:**
- Create: `dev/evals/diff_baseline/` directory.
- Create: `dev/evals/diff_baseline/<sample_id>.json` — one file per corpus sample (canonicalised JSON; `metadata.timestamp` and `run_id` stripped or replaced with sentinel).
- Create: `dev/evals/diff_renders.py` skeleton — the harness script that compares baseline against fresh output. Skeleton runs against unmodified `grade.py` and produces zero diff (sanity gate before U7 starts).

**Approach:**
- Pick the corpus before this unit starts. Candidates: existing `dev/skill-workspace/iteration-{1,4}/eval-0-audit-ai-cultural/with_skill/run-1/outputs/` inputs (the agent's response.md is NOT the baseline; the input prose is). Plus 2-3 hand-authored synthetic inputs covering (a) all-clear, (b) heavy-flagging across all eight categories, (c) hard_fail-only.
- For each input, run `python3 grade.py --format json <input>`, canonicalise (strip timestamp/run_id), save to `diff_baseline/`.
- Sanity-check the harness: re-run against unmodified grade.py and assert zero diff. If non-zero, the canonicalisation is wrong; fix before U7 lands.

**Patterns to follow:**
- Existing `dev/evals/run_grade_sweep.py` for harness shape.

**Test scenarios:**
- Happy path: harness against unmodified grade.py produces zero diff.
- Edge case: changing grade.py output (insert a debug print) causes the harness to fail loudly with input path + line-level diff.

**Verification:**
- Baseline files committed.
- Harness self-check green.

---

- U7. **Pattern registry + loader; promote `judgement.yaml` to registry-loaded**

**Goal:** Create `humanise/patterns.yaml` (per-pattern data). Add `humanise/registries.py` — loader for `patterns.yaml` and `judgement.yaml`, with schema validation and lookup helpers. Migrate `CHECK_REPORT_TEXT`, `CHECK_WHY_IT_MATTERS`, `CHECK_METADATA` (all four sub-fields: severity, failure_modes, evidence_role, guidance), and `humanise/references/alternatives.md` content into `patterns.yaml`. Audit `guidance` against `why_it_matters` during migration; if redundant, fold to single field.

**Requirements:** R10, R11.

**Dependencies:** U3 (severity audit complete); U10a (baseline locked).

**Files:**
- Create: `humanise/patterns.yaml` — one record per check_id.
- Create: `humanise/registries.py` — `load_patterns()`, `load_judgement()`, `pattern_for(check_id)`, `judgement_for(id)`, schema validation.
- Modify: `humanise/grade.py` — remove `CHECK_METADATA`, `CHECK_REPORT_TEXT`, `CHECK_WHY_IT_MATTERS`. Replace direct lookups with `registries.pattern_for(...)`. `annotate_result()` (line 2024) and `failure_mode_results()` (line 2404) read from the registry.
- Migrate: `humanise/references/alternatives.md` content into `patterns.yaml[id].alternatives`. Once migrated, alternatives.md is removed (or kept as a generated convenience file).
- Test: `dev/evals/test_registries.py` — round-trip load tests, schema validation, completeness tests; following `dev/evals/test_grade.py:35-88` convention.

**Approach:**
- Define `patterns.yaml` schema in a `registries.py` docstring. Required fields: `check_id`, `category`, `severity`, `failure_modes`, `short_name`, `why_it_matters`. Optional: `evidence_role`, `alternatives`, `references`, `guidance`, `structural`. (`mode_actions` was considered but not adopted — actions are computed by `_action_for_check()` from severity + depth, not stored per-pattern.)
- Generate `patterns.yaml` from existing constants via a one-shot migration script (`dev/evals/migrate_constants_to_yaml.py`). Hand-edit afterwards for cleanups, including:
  - Per-check `category` assignment (43 decisions; not currently encoded anywhere — derive from `patterns.md` H2 walk + per-check classification for meta-checks like `overall-ai-signal-pressure`).
  - Per-check `structural` boolean.
  - `alternatives.md` content folded per-check.
- Loader fails fast on schema violations with field name + offending check_id.
- Run U10b harness after this unit; assert zero JSON diff against baseline.

**Patterns to follow:**
- PyYAML for loading. Schema validation hand-rolled (no `jsonschema` dep yet — that decision lands in U8).

**Test scenarios:**
- Happy path: `load_patterns()` returns one record per `ALL_CHECKS` entry; `load_judgement()` returns 8 records.
- Happy path: `pattern_for(known_id)` returns the expected record.
- Edge case: `pattern_for(unknown_id)` raises a clear error with known ids.
- Edge case: malformed `patterns.yaml` fails at load with field name + offending record id.
- Edge case: extra entry in `patterns.yaml` with no matching `ALL_CHECKS` entry surfaces a warning at load.
- Integration: `humanise/grade.py`'s JSON output on the U10 corpus is byte-equivalent to baseline (excluding timestamp/run_id). Gated by U10b.

**Verification:**
- All checks have records in `patterns.yaml`.
- Loader test suite passes.
- U10b harness shows zero JSON delta.

---

- U8. **JSON audit contract + emitter (structured data only)**

**Goal:** Pin the audit data shape behind a JSON Schema at `humanise/contracts/audit-format-v1.json`. Refactor `human_report()` to emit a contract-shaped payload carrying **structured data only** — no pre-formatted prose. Common evidence envelope (`{quoted_phrases, locations, counts, raw}`) on every `programmatic_checks[].evidence`. Strip `confidence`, `overview` prose, `ai_pressure_explanation` prose from the payload. Add `aggregates.by_severity`, `aggregates.by_category`, `aggregates.ai_pressure`.

**Requirements:** R13, R14.

**Dependencies:** U7.

**Files:**
- Create: `humanise/contracts/audit-format-v1.json` — JSON Schema.
- Modify: `humanise/grade.py` — `human_report()` returns the contract shape; remove `confidence_assessment()` (line 2130); `format_human_report()` (line 2302) reads contract field paths.
- Test: `dev/evals/test_audit_contract.py` — schema validation tests.

**Approach:**
- Schema captures: `schema_version` (pinned `"1"`), `programmatic_checks[]` (id, status, severity, category, failure_modes, evidence with common envelope), `agent_judgement[]` (id, status, answer with per-item shape, evidence), `aggregates` (by_severity, by_category, ai_pressure), `metadata` (run_id, grader_version, timestamp).
- `programmatic_checks[].evidence` is the common envelope: `quoted_phrases: [str]`, `locations: [{line, col}]`, `counts: {...}`, `raw: {}` (opaque per-check).
- `agent_judgement[].answer` is per-item polymorphic — schema accepts; per-item shape validated against `judgement.yaml` at runtime (registry validation, not JSON-schema validation).
- No `confidence` block. No prose strings in the payload — `overview`, `ai_pressure_explanation`, etc. become vocabulary.yml templates that the renderer fills.
- `additionalProperties: false` at the top level.
- Decide at this unit: hand-roll validation (consistent with no-deps stance — feasible because the schema is small) OR add `jsonschema` dep. Common evidence envelope makes hand-rolling tractable.

**Patterns to follow:**
- Existing `human_report()` field shapes — overview/score/confidence/failed_checks/all_checks. Map structured pieces forward; drop prose; cut confidence.

**Test scenarios:**
- Happy path: representative grade.py output validates against `audit-format-v1.json`.
- Happy path: `schema_version` pinned to `"1"`.
- Happy path: every `programmatic_checks[].id` is a known check_id from the registry.
- Happy path: every `programmatic_checks[].evidence` carries the four common envelope fields (`quoted_phrases`, `locations`, `counts`, `raw`).
- Edge case: missing required field fails validation with field name.
- Edge case: extra unknown top-level key rejected.
- Edge case: contract validates on the all-clear case.
- Edge case: contract carries no prose strings — assert by grep on the emitted payload.
- Integration: U10b harness shows zero JSON delta against baseline (allowing for the contract-shape changes that are the whole point — baseline is recaptured between U7 and U8 if shape changes are deliberate; otherwise gate fails on shape drift).

**Verification:**
- Schema valid JSON Schema.
- Contract validates on representative outputs.
- No prose strings in payload.

---

- U9. **Vocabulary registry + renderer reads templates from it**

**Goal:** Create `humanise/vocabulary.yml` carrying every user-facing string the renderer prints, including prose templates that fill from contract structured data. Refactor the renderer to read severity tier labels, action verbs, headline templates, all-clear copy, next-step prompt, AI-pressure explanation template, drill-in frame strings from `vocabulary.yml`. Per-pattern `why_it_matters` prose stays in `patterns.yaml`; the *frame* it renders into ("Why this matters: {prose}") lives in vocabulary.

**Requirements:** R12.

**Dependencies:** U7, U8.

**Files:**
- Create: `humanise/vocabulary.yml`.
- Modify: `humanise/registries.py` — add `load_vocabulary()` and `string_for(key, **placeholders)`.
- Modify: `humanise/grade.py` — `SEVERITY_LABELS`, `ACTION_LABELS`, AI-pressure explanation, all-clear copy, next-step prompt, and any other string literals returned to the user — all replaced with `string_for(...)` lookups.
- Test: `dev/evals/test_vocabulary.py` — load tests, key-existence tests, placeholder-substitution tests.

**Approach:**
- Inventory every user-facing string in the renderer. Group by purpose: severity labels, action verbs, headline templates, all-clear, next-step, AI-pressure, drill-in frames.
- Build `vocabulary.yml` with one section per group. Use `{name}` placeholders for substitutions.
- `string_for(key, **kwargs)` formats placeholders. Missing key → fail-fast with key name. Missing placeholder → fail-fast with placeholder + template key.
- The renderer composes prose by merging vocabulary templates with structured contract data (e.g. `string_for("overview_template", failed=N, total=43)` → `"N of 43 checks were flagged for AI-style writing patterns."`).
- (Note: R5 says "why this matters" prose is NOT rendered in the audit output. That rule stands. The vocabulary frame for `why_it_matters` is for the Suggestions / Rewrite actions that DO surface drill-in prose, not the Audit action.)

**Patterns to follow:**
- Existing string-literal usage in `humanise/grade.py` rendering functions.

**Test scenarios:**
- Happy path: every user-facing string the renderer prints is sourced from `vocabulary.yml` (audit by grep on the renderer functions).
- Happy path: changing a label in `vocabulary.yml` propagates to rendered output.
- Edge case: missing key → fail-fast with key name.
- Edge case: placeholder mismatch → fail-fast with placeholder + template key.
- Integration: rendered output matches pre-vocabulary version verbatim with the default vocabulary (gated by U10b at the JSON layer; markdown rendering stays byte-equivalent until Phase 3).

**Verification:**
- Vocabulary keys cover every user-facing string.
- U10b harness clean.

---

- U10b. **JSON-equivalence verification gate (post-U9)**

**Goal:** Run the harness from U10a after each of U7, U8, U9. Assert zero JSON delta against baseline (excluding `metadata.timestamp` and `run_id`). Phase 2 is not done until this gate is green after U9 lands.

**Requirements:** R20.

**Dependencies:** U10a, U7, U8, U9.

**Files:**
- Modify: `dev/evals/diff_renders.py` — implement the comparison logic from the U10a skeleton.
- Test: this script *is* the test.

**Approach:**
- After each of U7, U8, U9 lands, run `diff_renders.py` over the corpus. First mismatch fails with input path + structured diff (which key-path differs, expected vs actual).
- If U8 deliberately changes the contract shape (e.g. adding the common evidence envelope), the baseline is regenerated as part of U8 and the gate becomes "shape matches the new baseline." Document the regeneration explicitly in U8's commit message; it is not a free pass.

**Test scenarios:**
- Happy path: post-U7 (registry migration only — no shape change) shows zero diff.
- Happy path: post-U8 shows zero diff against the regenerated baseline (or, if U8 deliberately changes the shape, a documented baseline regeneration commit lands alongside).
- Happy path: post-U9 shows zero diff (vocabulary lookup is internal — JSON shape unchanged).
- Edge case: harness fails loudly with input path, key-path of the first divergence, expected and actual values.

**Verification:**
- Zero-diff gate green after each of U7, U8, U9.

---

- U15. **Generate `patterns.md` from `patterns.yaml`**

**Goal:** Add a generator (`dev/tools/render_patterns_md.py`) that renders `humanise/references/patterns.md` from `humanise/patterns.yaml`. Add a CI check that asserts `patterns.md` on disk equals the regenerated output. After this unit, `patterns.yaml` is the master; `patterns.md` is a generated transparency artefact.

**Requirements:** R21b.

**Dependencies:** U7.

**Files:**
- Create: `dev/tools/render_patterns_md.py` — reads `patterns.yaml`, renders `patterns.md` per a Markdown template.
- Modify: `humanise/references/patterns.md` — becomes a generated artefact. Header note: "This file is generated from `humanise/patterns.yaml`. Edit the YAML."
- Modify: `dev/evals/test_patterns_md_generator.py` (or add CI step) — runs generator and asserts on-disk matches output.

**Approach:**
- Generator template mirrors today's structure: 8 `## ` category headings; per-pattern `### N. <Name>` block with `**Words to watch:**`, `**Severity:**`, `**Before:**` / `**After:**` examples. Words-to-watch and example fields come from `patterns.yaml` per-pattern.
- For pattern fields the YAML doesn't carry yet (commentary paragraphs, sub-categories within a pattern), the YAML schema gains optional fields (`commentary`, `sub_groups`) populated during U7's hand-edit pass.
- CI check runs `render_patterns_md.py --check`; fails if on-disk patterns.md differs from regenerated. Drift fails CI, not silently.

**Patterns to follow:**
- The existing patterns.md structure is the template target.

**Test scenarios:**
- Happy path: generator on the post-U7 patterns.yaml produces patterns.md byte-equivalent to the hand-edited result (after U7's first pass, the first regeneration may show diff — fold the diff into yaml until clean).
- Happy path: changing a `severity` field in patterns.yaml + regenerate updates patterns.md.
- Edge case: missing required field in a pattern yaml record fails generation with field + record id.
- Integration: CI check runs in `test_grade.py` or as a separate test target; merge blocked on drift.

**Verification:**
- Generator produces stable output.
- CI check enforces sync.

---

### Phase 3 — Layout redesign (renderer-only; JSON contract unchanged)

- U11. **Two-layer renderer (Layer 1 orientation + Layer 2 coverage receipt with Action column)**

**Goal:** Implement `format_two_layer()` reading from the JSON contract. Layer 1: verdict line (severity counts + pressure status, no confidence label) + per-flagged-pattern blocks. Layer 2: eight per-category sub-tables with three columns `Pattern | Result | Action`. Per-category collapse to one-liner when all-clear.

**Requirements:** R1, R2, R3, R4, R5, R8, R22.

**Dependencies:** U10b green.

**Files:**
- Modify: `humanise/grade.py` — replace `format_human_report()` (line 2073) with `format_two_layer()`; replace `_markdown_table_from_contract()` (line 2208) with a category-grouped renderer (`markdown_category_subtables()` or similar). Old functions removed.
- Modify: `humanise/vocabulary.yml` — **new keys to add**: severity glyphs (one per tier), category-collapse line template (e.g. `"{category} — {clear}/{total} clear"`), Layer-1 per-flagged-pattern block template, sub-table headers, all-clear single-line template. **Already present** (re-used as-is): `severity_labels`, `action_labels`, `status_labels`, `pressure_status`, `templates.severity_line`. The existing `templates.flagged_row`, `templates.table_header`, `templates.table_separator`, `templates.summary_*` are superseded by U11's templates and removed.
- Test: `dev/evals/test_two_layer_render.py`.

**Approach:**
- Layer 1 verdict line: severity counts (e.g. `1 hard_fail · 4 strong_warning · 2 context_warning`) + pressure status (`pressure: triggered` / `pressure: clear`). No confidence label. Reuses the existing `templates.severity_line` from `vocabulary.yml`.
- Layer 1 per-flagged-pattern blocks: severity-glyph + `short_name` + quoted phrase(s) from `evidence.quoted_phrases` + one-verb action. The action verb comes from `_action_for_check()` (grade.py:2198), which maps severity + depth → action key (`fix` for hard_fail/strong_warning at any depth; `preserve_with_disclosure_or_user_decision` for context_warning at Balanced; everything → `fix` at All depth). The verb string then resolves through `registries.action_label(...)` from `vocabulary.yml`'s `action_labels`. No "why this matters" prose (R5). (Note: there is no `mode_actions` field on patterns.yaml records — earlier plan drafts assumed one; the action is computed, not stored per-pattern.)
- Layer 2: group by `category`. For each of the 8 categories: if every check is `clear`, emit one-liner; otherwise emit sub-table with `Pattern | Result | Action` columns. Action column is derived from severity via the same `_action_for_check()` path: `Fix` (hard_fail or strong_warning at Balanced) or `Disclose or ask before preserving` (context_warning at Balanced). Render order matches `humanise/references/patterns.md`.
- All-clear case: every programmatic check clear AND every agent-judgement clear → R8 single-line response. No tables, no level label.

**Patterns to follow:**
- Existing `_markdown_table_from_contract()` (grade.py:2208) for table-rendering mechanics — same accessors (`registries.pattern_for(check["id"])`, `registries.action_label(...)`, `registries.status_label(...)`), grouped by category.

**Test scenarios:**
- Happy path: a sample with one flagged check in each category produces all 8 sub-tables.
- Happy path: a sample with all of "Style" clear produces the one-liner for Style.
- Happy path: per-flagged-pattern blocks include severity glyph + name + quoted phrase + action; do NOT include "why this matters."
- Happy path: sub-tables have exactly three columns: `Pattern | Result | Action`.
- Edge case: zero flagged → R8 single-line response, no confidence label.
- Edge case: zero programmatic flagged + agent-judgement flagged → Layer 2 collapses; agent-judgement block (U12) carries findings.
- Edge case: every check in a category flagged → sub-table renders all rows.
- Integration: rendered output for a hand-authored fixture matches a hand-authored expected output.

**Verification:**
- Test suite passes.
- Mae reviews three representative renders before merge.

---

- U12. **Agent-judgement parallel block + all-clear case**

**Goal:** Implement `format_agent_judgement()` rendering `agent_judgement[]` from the contract. Block follows the programmatic block, separated by `---`. Each item uses its per-item answer schema; polymorphic genre slot renders as `Genre detected: <genre>. Findings: …` (or "Watchlist coverage pending." until follow-up data lands). Status binary `flagged` / `clear`. No severity column. Sort by `judgement.yaml` registry order.

**Requirements:** R6, R7, R8, R14.

**Dependencies:** U14 (done — `humanise/judgement.yaml` shipped in commit `38d7c29`); U11 (programmatic block exists for ordering).

**Files:**
- Modify: `humanise/grade.py` — add `format_agent_judgement()` reading `agent_judgement[]`; per-item dispatchers based on `answer_schema.type`. Lookup via `registries.judgement_for(id)` (already implemented in `humanise/registries.py`).
- Modify: `humanise/vocabulary.yml` — strings for the agent-judgement block (header, status labels, "agent reading clean" copy, genre tag template, watchlist-pending copy). Reuses existing `status_labels` (`clear`, `flagged`).
- Test: `dev/evals/test_agent_judgement_render.py`.

**Approach:**
- For each item: read `id`, look up registry record via `registries.judgement_for(id)`, dispatch on `answer_schema.type` (the four types defined in `judgement.yaml` today):
  - `state` → render the state value (e.g. `locked`, `has_breaks`, `mixed_intentional`).
  - `list` → render bulleted entries with the per-item fields (e.g. `[phrase, why_unspecific]`); empty list → `clear`.
  - `presence` → render the boolean.
  - `trichotomy` → render the chosen value (e.g. `varied`, `partly_uniform`, `fully_locked`).
- Each record carries a `flagged_when` field that maps the answer to status (`flagged` / `clear`). The renderer uses this to decide block-level status, not the answer value alone.
- Genre slot: special-case dispatcher. Read detected genre. If watchlist for that genre is empty → emit "Genre detected: <genre>. Watchlist coverage pending." Otherwise emit findings.
- Sort by `judgement.yaml` registry order.
- All-clear case: every item clear → single "agent reading clean" line within the block (or block omitted if Layer 2 also clear; R8 single-line response wins).

**Test scenarios:**
- Happy path: 8 items render in registry order.
- Happy path: polymorphic genre slot renders genre + findings.
- Happy path: status binary; no severity column; no `mixed`.
- Edge case: all 8 clear → single line "agent reading clean."
- Edge case: only genre slot fires → single block with genre finding.
- Edge case: list-shape item with zero entries → `clear`, not empty list.
- Edge case: detected genre with empty watchlist → "Watchlist coverage pending."
- Integration: agent-judgement findings do NOT affect verdict-line severity counts (verdict line reads `aggregates.by_severity` from programmatic block only).
- Integration: R8 single-line response takes precedence when both blocks clear.

**Verification:**
- Test suite passes.
- Mae reviews the agent-judgement block on a flagged-genre sample before merge.

---

- U13. **SKILL.md audit template + full README update + cross-corpus sanity check** *(scope extended 2026-05-01 with Mae sign-off — owns all README work; absorbs the deferred U6)*

**Goal:** Update every place the audit's user-facing shape is described — `humanise/SKILL.md` Audit-output template, `humanise/references/example.md`, and `README.md` — so they all match what the new renderer actually emits. README work absorbs U6's original scope (counts, pattern table, "What's next" bullet) **plus** the dual-layer audit description, all in one pass. Run the new renderer over the iteration corpus and confirm output matches the redesign.

**Requirements:** R1-R8, R19 (completes — owns the entire README update), R22 (cross-cutting verification).

**Dependencies:** U11, U12. Independent of any Phase-1 README work (none exists — U6 was deferred here).

**Files:**
- Modify: `humanise/SKILL.md` — Audit output template (Audit section at line 42, output template at line 53, ends ~line 125 in current 291-line file) replaced.
- Modify: `humanise/SKILL.md` Action 2 (Suggestions, line 127) — references to the audit template updated.
- Modify: `humanise/references/example.md` — example output replaced.
- Modify: `humanise/references/process.md` — Step C reference updated if needed.
- Modify: `README.md` — full update in one pass:
  1. **Counts and pattern table:** Replace stale count strings (`38 patterns`, `43 programmatic checks`) with the actual catalogue state at Phase-3-merge time. Extend the pattern table with every numbered/sub-letter heading then in `humanise/references/patterns.md`.
  2. **Dual-layer audit description:** Update "What it does" / "Representative output" / "Performance" sections to describe the orientation block + coverage receipt + parallel agent-judgement block + all-clear single-line case.
  3. **"What's next" bullet:** Drop the "Promote the seven unnumbered checks" bullet (work done in `13b4e9d`).
  4. **Reconcile against `main`:** Take whatever `README.md` exists on `main` at U13-start as the base prose. Apply 1-3 on top.

No README dogfood gate. The README is project marketing, not load-bearing infrastructure; auditing it against the grader is self-defeating because the example/pattern table fires on every pattern by design (see `feedback_session_2026_05_01_failures.md` for the prior session that learned this the hard way).

**Approach:**
- Generate representative renders (one all-clear, one heavy-flagging, one agent-judgement-only) using U11 + U12.
- Update SKILL.md template to match. Preserve the action-selection table.
- Update `humanise/references/example.md` with one representative render.
- Update README in one pass: counts + table + dual-layer description + dropped bullet, all faithful to the renderer. No confidence-level references (R14).

**Test scenarios:**
- Happy path: SKILL.md Action 1 audit template matches U11 + U12 renderer output on a representative input.
- Happy path: `humanise/references/example.md` renders the new shape (no confidence label).
- Happy path: README's audit-output description matches the same renders SKILL.md and example.md describe (template parity check across the three files).
- Happy path: README count strings match `len(ALL_CHECKS)` and the heading count in `patterns.md`.
- Happy path: README pattern table contains a row for every numbered/sub-letter heading in `patterns.md`.
- Integration: a fresh iteration run via `dev/evals/run_skill_creator_iteration.py` passes all audit-shape assertions (existing + new from U5).

**Verification:**
- SKILL.md template, example.md, and README all describe the same shape.
- Counts and pattern table reconcile with the catalogue.
- Mae reviews the README, example.md, and SKILL.md diffs together as one cross-cutting review.
- One full iteration run passes audit-shape assertions end-to-end.

---

## System-Wide Impact

- **Interaction graph:**
  - `humanise/grade.py` is consumed by `humanise/SKILL.md` (subprocess: `python3 grade.py --format json`), by `dev/evals/run_skill_creator_iteration.py` (`import grade as GRADE`), by `dev/evals/run_grade_sweep.py`. The JSON contract from U8 is the boundary.
  - `humanise/SKILL.md` is read by Claude Code at skill-invocation time. The U4 + U13 template changes are observable to every Audit run.
  - `humanise/references/*.md` are read by the agent during action execution. patterns.md is read for "why this matters" prose during Suggestions / Rewrite (drill-in only — R5).
  - `humanise/judgement.yaml` is read by the agent at audit time (U4) for prompts and answer schemas.
- **Error propagation:**
  - Registry load failures (U7) fail at module import time with field/key names.
  - JSON contract validation (U8) fails at emit time.
  - Missing vocabulary keys (U9) fail at render time with the key name.
  - Missing pyyaml (or json, depending on registry-format decision) — grade.py fails at import. SKILL.md's "no Python" fallback does not catch this; document the dep in README.
- **State lifecycle risks:**
  - The diff baseline in `dev/evals/diff_baseline/` is frozen. Any Phase 1 unit that changes JSON output (most likely U3 severity recalibration) requires re-capturing baseline before U10a locks. Sequence: U1 → U2 → U3 → corpus selection → U10a baseline capture → U7+ →… (U10a runs after Phase 1 settles).
  - Phase 1 changes shift the corpus output; iteration outputs become stale.
- **API surface parity:**
  - `grade.py --format json` output gains the new contract shape (no confidence; common evidence envelope; aggregates expanded). Consumers updated in U8.
  - `grade.py --format markdown` output is byte-equivalent through Phase 2 (used only by `format_human_report()`); changes shape in Phase 3.
  - SKILL.md Action 2 (Suggestions) and Action 3 (Rewrite) read grader output and may need template updates after Phase 3 — verified in U13.
- **Integration coverage:**
  - U10b covers Phase 2's no-op claim at the JSON layer.
  - U13's iteration run covers the dual-layer + agent-judgement contract end-to-end.
- **Unchanged invariants:**
  - `grade.py` CLI flags (`--format`, `--depth`, `<file>`, `[assertion list]`).
  - `humanise/references/severity-detail.md` deep-dive prose (only severity numerics may shift in U3).
  - The Save modifier (`humanise/SKILL.md:228-250`).
  - `regrade()` helper at `humanise/grade.py:2679`.
  - The Suggestions action — drill-in to patterns.md remains the read path for "why this matters" prose.

---

## Risks & Dependencies

### Active risks for Phase 3

| Risk | Mitigation |
|------|------------|
| Polymorphic genre slot (#41) ships with no watchlist data. | Plan defers per-genre watchlist content. The runner emits "Genre detected: <genre>. Watchlist coverage pending." until follow-up data lands. |
| Main's uncommitted humanise rewrite of `README.md` is parallel work, not Phase-3 work. | Mae commits these edits independently on `main` whenever she chooses. U13 takes whatever `README.md` exists on `main` at U13-start as the base prose. |
| Phase 3 introduces edge cases (single-line all-clear, agent-judgement-only) the existing harness doesn't cover. | U11 and U12 each add fixture-level test coverage. U13's iteration run is the integration gate. |
| `agent_judgement[]` is populated by the agent, not by `grade.py` — a Python eval harness can't easily assert what the agent writes there. | U5 audit-shape checks operate on the rendered response (the agent's final output), not on grade.py's JSON. Consistent with how the agent's response is the user-facing artefact. |
| U11's new vocabulary keys (severity glyphs, category-collapse template, sub-table headers) drift from the existing template style in `vocabulary.yml`. | Layer-1 verdict line reuses the existing `templates.severity_line`. New keys mirror the dotted-key + placeholder convention already in the file. `test_vocabulary.py` covers schema/placeholder shape. |

### Resolved (Phase 1 / Phase 2)

| Risk | Resolution |
|------|------------|
| Group A / Group B resolution drags on; Phase 1 timebox slips. | Resolved — Phase 1 done in PR #6. |
| Severity recalibration (U3) shifts confidence on existing iteration outputs in unwanted ways. | Resolved — U3 corpus shift reviewed before merge; commit `4303d44`. |
| U10 baseline drifts after capture. | Resolved — baselines committed in `dev/evals/diff_baseline/`; harness reads only, never overwrites. |
| `humanise/grade.py` exceeds size budget after U7-U9. | Resolved — 2763 LOC after U9, under the 2900 split threshold. |
| README update (U6) describes a target shape the live grader doesn't yet emit. | Resolved — U6 deferred to U13. |
| Cross-tree concern: `docs/todos/grader-integrity-gaps.md` was untracked. | Resolved — file is tracked. |
| Worktree commit `471a460 docs: U6 — refresh README` is now narratively orphaned. | Resolved — `471a460` stayed on `docs/audit-report` and was not merged to `main`. PR #6 merged without it. U13 will write the README from scratch. |
| `pr-6-code-review-handoff.md` P1 (seven unnumbered checks) and P2 (`ALL_CLEAR_LINE_RE` unanchored). | Resolved — P1 by `13b4e9d`; P2 by `f671cc4`. |
| PyYAML adds a hard third-party dep. | Resolved — accepted in U7. |
| `additionalProperties: true` at evidence level was the original design. | Resolved — U8 common envelope; meta-test asserts the four common fields. |

---

## Phased Delivery

### Phase 1 — Regression-fix + agent-judgement registry

**Status as of 2026-05-02:** Done. PR #6 merged (commit `49a9be2` on `origin/main`).

| Unit | Status | Commit |
|---|---|---|
| U1 | Done | `d46943b` |
| U2 | Done | `4b9eb84` |
| U3 | Done | `4303d44` |
| U14 | Done | `38d7c29` |
| U4 | Done | `526b865` |
| U5 | Done | `57db888` |
| U6 | **Removed** — deferred to U13 | `471a460` (stayed on `docs/audit-report`, never merged to `main`) |
| U16 | **Removed** — already shipped | `13b4e9d` |

Plus side-fixes that landed without plan units: `1b58968` (extended #42 with candour cluster), `fbbe0ab` (review-handoff fixes), `f671cc4` (anchored `ALL_CLEAR_LINE_RE`).

### Phase 2 — Architecture as no-op refactor

**Status as of 2026-05-02:** Done. U10b harness green (`11/11 baselines match current grade.py output`).

| Unit | Status | Commit |
|---|---|---|
| U10a | Done | `6dd3721` (PR #8) |
| U7 | Done | `14ff9cd` (PR #8) |
| U15 | Done | `b63eaf3` (PR #8) |
| U8 | Done | `5b02b12` + `886ffde` (volatile metadata fix) (PR #9) |
| U9 | Done | `7498814` (on `feat/audit-phase-2-continued`; PR pending) |
| U10b | Green | n/a — verification harness, runs against committed baselines |

Plus side-work: `0ca4150` (`fix(grader): document and validate YAML registries` — on `refactor/audit-phase-2`).

### Phase 3 — Layout redesign

**Status as of 2026-05-02:** Not started. Phase 2 settled; ready to begin.

U11 and U12 can be parallelised. U13 requires both. **U13 owns all README work** (counts, pattern table, dual-layer description) — the entire deferred U6 plus the original U13 scope. SKILL.md template, example.md render, and README description all land together. No README dogfood gate (see U13 Files).

---

## Documentation / Operational Notes

- README update lands entirely in Phase 3 (U13). Through Phase 1 and Phase 2 the README has stale counts and a stale pattern table — acceptable, because the README is project marketing rather than load-bearing infrastructure.
- `humanise/references/example.md` updated in U13 — agents reading this file see the new audit shape.
- `humanise/references/severity-detail.md` shifted during U2/U3 (resolved in Phase 1).
- No external rollout, monitoring, or feature flag — the skill is local.
- Document the PyYAML dep in the README install section as part of U13. (`jsonschema` is not added — validation is hand-rolled in `humanise/registries.py`.)

---

## Sources & References

- **Origin document:** [`docs/ideation/2026-04-30-audit-report-redesign-ideation.md`](../ideation/2026-04-30-audit-report-redesign-ideation.md)
- **Required reading enforced by origin:** [`docs/todos/grader-integrity-gaps.md`](../todos/grader-integrity-gaps.md), [`docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md`](../ideation/2026-04-30-pr5-strategic-moves-ideation.md)
- **2026-05-01 update inputs:**
  - [`docs/todos/pr-6-readme-resolution.md`](../todos/pr-6-readme-resolution.md) — captures the worktree's original U6 README diff (`471a460`) and the post-merge reconciliation problem this update resolves.
  - [`docs/todos/pr-6-code-review-handoff.md`](../todos/pr-6-code-review-handoff.md) — captures the P1 (seven unnumbered checks → U16) and P2 (`ALL_CLEAR_LINE_RE` → already shipped in `f671cc4`) findings.
  - Branch state at update time: `docs/audit-report` 13 commits ahead of `main`, with main carrying uncommitted README edits that humanise the prose without updating counts.
- **Current renderer surface:** `humanise/SKILL.md:42-92`, `humanise/grade.py:2206-2337`, `humanise/grade.py:2550-2672`
- **Severity source:** `humanise/grade.py:1734-1993` (`CHECK_METADATA[id]["severity"]`).
- **Pattern catalogue:** `humanise/references/patterns.md` (8 category H2 headings; 41 numbered patterns + 23a/31a/35a sub-letters).
- **Design space corpus:** `dev/skill-workspace/iteration-{1..4}/eval-0-audit-ai-cultural/with_skill/run-1/outputs/response.md`.
- **Audit-shape harness:** `humanise/grade.py:2550-2672`, `dev/evals/run_skill_creator_iteration.py:310-329`.
- **README auto-rewritten markers:** `dev/evals/run_skill_creator_iteration.py:893-894`.
- **Test convention:** `dev/evals/test_grade.py:35-88`.
