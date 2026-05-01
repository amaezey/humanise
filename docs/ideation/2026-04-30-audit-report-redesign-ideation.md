---
date: 2026-04-30
topic: audit-report-redesign
focus: redesign the user-facing humanise audit report; the current per-pattern-blocks format was dogfooded and called unreadable
mode: repo-grounded
---

# Ideation: Audit report redesign

## REQUIRED READING — before planning, read these files

The plan for this work cannot be drafted from this ideation alone. The following files contain decisions, scope, and prerequisites that the plan must incorporate. Read each before producing any plan output:

1. **`docs/todos/grader-integrity-gaps.md`** — `MUST READ`. Defines Group A (17 patterns described in `patterns.md` with no programmatic check) and Group B (8 programmatic checks with no numbered pattern). Resolving both is **Phase 1 prerequisite work** that blocks the redesign in this ideation. The plan must include a substep for each Group A pattern (decide: write the check / fold / move to agent-judgement) and each Group B check (decide: add patterns.md entry / fold / remove). Severity recalibration is impossible until these are resolved.
2. **`docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md`** — `MUST READ`. Idea #1 (single-source vocabulary registry + JSON audit-format contract) substantially overlaps with the architecture in #6 below. The plan must reconcile the two rather than treat them as independent proposals.
3. `humanise/SKILL.md` — current Audit / Suggestions / Rewrite / Write action templates. Lines 42-89 are the current Audit output template that the redesign replaces.
4. `humanise/grade.py:2130-2337` — the existing `confidence_assessment()`, `human_report()`, `format_human_report()`, and `markdown_checks_table()` functions that the renderer replaces. Lines 1735+ are `FAILURE_MODE_DETAILS` (the only place severity currently lives).
5. `humanise/references/patterns.md` — the catalogue. The 8 category headings are the basis for the per-category sub-tables in #1. The numbered patterns are the basis for the pattern registry's `check_id` ↔ pattern mapping.
6. `dev/skill-workspace/iteration-{1..4}/eval-0-audit-ai-cultural/{old_skill,with_skill}/run-1/outputs/response.md` — captured user-facing reports across the formats this ideation rejects (per-pattern blocks, table-of-everything) and represents the design space the plan is choosing inside.

If the plan is produced without reading file 1 (`docs/todos/grader-integrity-gaps.md`), the result is incomplete and unsafe to act on.

## Codebase context

Python (2765 LOC grader) + Markdown Claude Code skill. `humanise/` is the installable skill (SKILL.md, grade.py, references/), `dev/` is harness/research/plans/iterations.

Report rendering lives in three places:
- `humanise/SKILL.md:42-89` — agent-facing audit output template (current "per-pattern blocks")
- `humanise/grade.py:2206-2337` — `human_report()` / `format_human_report()` (assembly + rendering)
- `humanise/grade.py:2280-2299` — `markdown_checks_table()` (the 6-column 43-row table)

## Survivors after critique and conversational refinement

### 1. Two-layer audit response shape

Single response, two visual sections separated by `---`. No UI machinery (skills can't control collapse/toggles in any harness — this is just text order).

**Layer 1 — orientation, what to do:**
- Verdict line: counts by severity + confidence level
- Per-flagged-pattern blocks for programmatic checks: severity glyph + pattern name + quoted phrase(s) + one-verb action. **No "why this matters" prose** (lives in `references/patterns.md`).

**Layer 2 — coverage receipt:**
- Programmatic checks rendered as **8 sub-tables, one per category** (`Content patterns`, `Language and grammar`, `Style`, `Communication`, `Filler and hedging`, `Sensory and atmospheric`, `Structural tells`, `Voice and register`).
- Categories with all clear collapse to a one-liner (`Style — 5/5 clear`); no table for that category.
- Tables show three columns: `Pattern | Result | Severity`.
- Below the programmatic block, a parallel **Agent-judgement block** (Option A — two epistemologies, both first-class) — see #2.

When zero flagged across both programmatic and agent-judgement layers: single line `43 of 43 patterns clear, agent reading clean. Confidence: Low.` + next-step. No tables.

**Warrant:** `direct:` — grounding flagged that the "unreadable" complaint is about ordering and density, not absence of either component; spec says "Audit returns full information." Categories already exist as 8 prose section headings in `references/patterns.md`. Severity already exists as metadata in `FAILURE_MODE_DETAILS` (grade.py:1735+).

### 2. Agent-judgement layer (parallel block, Option A)

The grader has two epistemologies, both required, never conflated:

- **Programmatic** (43 regex/structural checks) — deterministic, regex/density-based.
- **Agent-judgement** (7 items, see below) — semantic reading the regex grader cannot perform.

Two top-level keys in the audit JSON: `programmatic_checks: [...]` and `agent_judgement: [...]`. Two visual blocks in the response. A reader can tell at a glance whether a finding is regex-true or the agent's read.

The 8 agent-judgement items (7 + 1 polymorphic genre slot):

1. **Structural monotony** — do all sections follow the same arc (problem → evidence → anecdote → advice)?
2. **Tonal uniformity** *(pattern 35)* — does the whole text sit in one register?
3. **Faux specificity** *(pattern 36)* — are the "specific" examples actually specific, or genre-convention filler?
4. **Neutrality collapse** *(pattern 37)* — does the text commit to a position? *(Resolved as agent-only. The surface false-balance phrasing piece is partly covered by existing `check_false_concession`; expanding that on the regex side is a Group A decision, separate from the agent-layer item.)*
5. **Even jargon distribution** — clumped or uniform?
6. **Forced synesthesia** *(pattern 28)*
7. **Generic metaphors** *(pattern 30)*
8. **Genre-specific** *(pattern 41)* — polymorphic slot. Agent first reads the input to determine genre (academic / student essay / poetry / fiction / other), then runs the relevant genre-specific watchlist (citations for academic, rubric phrases for student, default quatrains for poetry, "as-you-know" dialogue for fiction). Reports as one block with genre identified: `Genre detected: fiction. Findings: …`.

Each item has its own answer schema (per-item shapes, not a single uniform record) — counted observations, presence checks, list judgements, trichotomies as appropriate.

**Status vocabulary (binary):** `flagged` or `clear`. No severity column on the agent-judgement layer. No `mixed` state. Agent's confidence in its own judgement is implicit — the layer's job is to surface what regex can't see, not to grade urgency.

**Cut from Mae's original list (have regex equivalents):**
- #34 Resolution density → `check_tidy_paragraph_endings`
- #38 Section scaffolding → `check_section_scaffolding`

### 3. Architecture (#6) — registry + JSON contract + vocabulary split

Three architectural moves bundled:

(a) **Pattern registry** (`humanise/patterns.yaml`) — replaces `CHECK_REPORT_TEXT` dict in grade.py + scattered metadata across `references/patterns.md`, `severity-detail.md`, `alternatives.md`. Keyed by `check_id`. Fields per record:
```yaml
check_id: no-em-dashes
category: punctuation       # the 8 categories from patterns.md
structural: false           # vs lexical
severity: strong_warning
evidence_role: punctuation_signal
short_name: "Em dashes"
mode_actions: { balanced: fix, all: fix }
alternatives: [comma, period, parens]
references: [{ source: '...', url: '...' }]
why_it_matters: "..."       # only shown when user drills in
```

(b) **Agent-judgement registry** (`humanise/judgement.yaml`) — 7 records (possibly +1 for #41), each with its own answer schema (per-item shapes per Q4):
```yaml
- id: tonal_uniformity
  pattern_ref: 35
  prompt: "Does the whole text sit in one register?"
  answer_schema: { type: state, values: [locked, has_breaks, mixed] }
  severity_tier: strong_warning   # depends on Q1 resolution
- id: forced_synesthesia
  pattern_ref: 28
  prompt: "Are there forced cross-modal metaphors?"
  answer_schema: { type: list, items: [{ phrase, why_forced }] }
- ...
```

(c) **JSON audit contract** — stable, versioned, the only thing rendering reads:
```json
{
  "schema_version": "1",
  "programmatic_checks": [
    { "id": "...", "status": "flagged|clear", "severity": "...", "category": "...", "evidence": {...} }
  ],
  "agent_judgement": [
    { "id": "...", "status": "flagged|clear", "answer": {...}, "evidence": {...} }
  ],
  "confidence": { "level": "...", "basis": [...], "caveat": "..." },
  "aggregates": { "by_severity": {...}, "by_category": {...} },
  "metadata": { "run_id": "...", "grader_version": "...", "timestamp": "..." }
}
```

(d) **Vocabulary registry** (`humanise/vocabulary.yml`) — all user-facing strings live here:
- Programmatic severity tier labels (`hard_fail` / `strong_warning` / `context_warning` → display strings)
- Agent-judgement state labels (`flagged` / `clear` → display strings, separate set from programmatic severity)
- Status labels (passed / flagged / mixed for the programmatic block)
- Action verbs
- Confidence level labels and meaning strings
- Headline template strings (with placeholders)
- All-clear copy
- Next-step prompt template

Per-pattern `why_it_matters` prose stays in the pattern registry (it's per-pattern, not generic), but the *frame* it's rendered into (e.g. "Why this matters: {prose}") lives in vocabulary.

**Principle:** if changing a string is a tone/voice decision, vocabulary. If changing the structure is a decision about what to show, renderer.

### 4. Confidence stays programmatic-only

`confidence_assessment()` (grade.py:2130) is a deterministic rollup over severity counts + AI-pressure trigger. After the redesign it reads from the JSON's `programmatic_checks` block only. Agent-judgement findings get their own status block but don't dilute confidence — confidence is "how strong is the regex evidence," not "how confident is the agent."

The level labels (Low / Medium / High) move into `vocabulary.yml`.

## Sequencing

### Phase 1: Regression-fix (must-ship-first, blocks redesign)

This phase is bigger than originally framed — has six substeps:

1. **Resolve Group A** (`docs/todos/grader-integrity-gaps.md`) — for each of the 12 "could be programmatic" patterns, decide: write the check, fold into existing check, or move to agent-judgement.
2. **Resolve Group B** — for each of the 8 undocumented checks: add a numbered patterns.md entry, fold into existing, or remove.
3. **Recalibrate severity** — once the check ↔ pattern map is clean. Currently severity lives only in `FAILURE_MODE_DETAILS` and patterns.md doesn't carry it; cross-reference is impossible.
4. **Re-add agent-judgement items to Audit action** in `humanise/SKILL.md` (currently only fires on Rewrite/Write — accidental regression from `739d8ba`). Update `references/process.md` Step C accordingly.
5. **Update `dev/evals/` audit-shape assertions** — every audit response must contain both programmatic and agent-judgement blocks.
6. **Update README** — reflect dual-layer audit + resolved patterns ↔ checks map.

### Phase 2: Architecture as no-op refactor

Land the pattern registry + agent-judgement registry + JSON contract + vocabulary registry. Renderer must produce **today's output verbatim**. Verify by diffing renders before/after on a fixed corpus.

### Phase 3: Layout redesign

Switch the renderer from "today's output" to the two-layer / 8-sub-tables / agent-judgement-block design. Pure renderer change, JSON contract unchanged.

## Resolved decisions

1. **#37 Neutrality collapse** → agent-judgement only. (Surface false-balance phrasing under `check_false_concession`; expanding regex coverage is a separate Group A decision.)
2. **#41 Genre-specific** → one polymorphic slot in the agent-judgement registry. Agent detects genre, then runs the matching watchlist. Single record in `judgement.yaml` with sub-records per genre.
3. **Severity for agent-judgement** → none. Binary `flagged` / `clear` status only. No tier vocabulary, no severity column. Sort order within the block is by registry order.

## Rejection summary (full)

See `/tmp/compound-engineering/ce-ideate/514b7355/survivors.md` for the 42 rejected candidates and reasons. Notable categories of rejection:
- Variations on "verdict line first" — all absorbed into #1.
- SMS-mode / 5-line ceiling — violate "Audit returns full information."
- Severity-gated drill — violates "depth dial doesn't filter audit."
- Pattern-free output / rewrite-first — violate "audit and rewrite are separate actions."
- Longitudinal ledger — out of scope (different feature).
- Inline annotated draft — high-complexity radical alternative; rejected for now in favour of #1's two-layer approach.
