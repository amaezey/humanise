# Failure Mode Consolidation Plan

Date: 2026-04-27

## Current Git State

Branch: `main`, tracking `origin/main`.

Committed checkpoint before consolidation:

- `9ce1cec feat: expand AI writing signal framework`

Current worktree is intentionally dirty with behavior-preserving consolidation work after that checkpoint. This plan was originally written against the pre-commit worktree; this progress note records the new base so the source trail does not get lost.

Current changed areas:

- `human-eyes/grade.py` and `dev/evals/grade.py`: 43-check grader, severity metadata, mode summaries, vocabulary pressure, GPTZero 100 phrase list, Kobak excess-vocabulary loading, aggregate signal pressure.
- `dev/evals/test_grade.py`: assertion tests for new and existing checks, including Light/Medium/Hard behavior and aggregate pressure calibration.
- `human-eyes/SKILL.md`: mode architecture, transparency report, hard/medium/light behavior, semantic preservation, structural self-audit.
- `human-eyes/references/patterns.md`: pattern catalogue, evidence hierarchy, full GPTZero 100 list, Kobak methodology notes, genre-specific manual checks.
- `dev/evals/grade-sweep-report.json`: regenerated sweep over existing, human-sourced, and generated-AI samples.
- `dev/evals/samples/human-sourced/` and `dev/evals/samples/generated-ai/`: expanded evaluation corpus.
- `human-eyes/references/kobak-excess-words.csv`: 900-row Kobak et al. excess-vocabulary source file.

Latest verification before this plan:

- `python3 dev/evals/test_grade.py` passed.
- `git diff --check` passed.
- Sweep report showed `overall-ai-signal-pressure` hits: existing `7/19`, human-sourced `8/47`, generated AI `13/18`.

Progress after checkpoint:

- Phase 1 complete: every registered check has `failure_modes` and `evidence_role` metadata; tests fail if a check disappears or lacks metadata.
- Phase 2 reporting skeleton complete: CLI JSON now includes `failure_mode_results` while keeping legacy `mode_results` and `expectations` intact.
- No checks were removed, no severity was changed, and no pass/fail thresholds were changed.

## Problem

The ruleset has grown by source and symptom:

- Wikipedia AI-cleanup signs.
- Practitioner lists and field observations.
- User-observed pet peeves.
- GPTZero's 100 high-ratio phrases.
- Kobak et al.'s PubMed excess-vocabulary dataset.
- Shreya Shankar's craft critique.
- Genre-specific editorial observations.

That is valuable, but the current presentation can look like cherry-picking because the top-level taxonomy is still a mixed bag: some checks are provenance residue, some are rhetorical moves, some are punctuation preferences, some are corpus-derived vocabulary pressure, and some are genre warnings.

The next improvement should not add more regex first. It should reorganize the skill around a coherent model of AI-writing failure modes while preserving the working checks and source trail.

## Target Model

Reframe the skill around six failure modes.

### 1. Provenance Residue

Text leaks its production workflow.

Examples:

- Assistant residue: "I hope this helps", "great question", "let me know".
- Template residue: `{client_name}`, `[insert date]`.
- Fake continuation offers.
- Fake citations, fake bylines, fake bios, and provenance oddities.

Severity:

- Mostly `hard_fail`.
- Reason: these are not style; they are residue.

Current checks:

- `no-collaborative-artifacts`
- `no-placeholder-residue`
- parts of `no-generic-conclusions`
- manual citation/provenance checks

### 2. Synthetic Significance

The prose performs depth, revelation, or importance without earning it.

Examples:

- "What no one is talking about..."
- "This is not X, it is Y."
- "A pivotal moment."
- "A stark reminder."
- "What surfaces is..."
- "The argument landed..."
- "Quietly revolutionary."

Severity:

- Usually `strong_warning`.
- Light may preserve voiced or quoted exceptions with disclosure.
- Medium and Hard should remove generic uses.

Current checks:

- `no-manufactured-insight`
- `no-negative-parallelisms`
- `no-countdown-negation`
- `no-significance-inflation`
- nonliteral `land/landed` and `surface/surfaced` vocabulary regexes
- parts of `no-ai-vocabulary-clustering`

### 3. Frictionless Structure

The prose is packaged too evenly.

Examples:

- Unrequested headings.
- Same-sized paragraphs.
- Tidy paragraph endings.
- Listification.
- Repeated section labels.
- Mechanical triads.

Severity:

- Mostly `context_warning`, because many structures are valid by genre.
- Becomes more serious when combined in `overall-ai-signal-pressure`.

Current checks:

- `no-markdown-headings`
- `paragraph-length-uniformity`
- `no-tidy-paragraph-endings`
- `no-excessive-lists`
- `no-section-scaffolding`
- `no-forced-triads`
- `no-triad-density`
- `sentence-length-variance`

### 4. Generic Abstraction

Concrete claims are replaced by portable abstractions.

Examples:

- `landscape`, `interplay`, `framework`, `nuanced understanding`.
- GPTZero high-ratio phrases.
- Kobak excess style vocabulary.
- Corporate abstraction: `impact`, `outcomes`, `alignment`, `unlock`.

Severity:

- Single terms are not evidence.
- Clusters are `strong_warning` or aggregate pressure.
- Corpus-derived lists are supporting evidence, not verdicts.

Current checks:

- `no-ai-vocabulary-clustering`
- `overall-ai-signal-pressure`
- `no-corporate-ai-speak`
- `vocabulary-diversity`
- `no-filler-phrases`

### 5. Voice Erasure

The text loses stance, specificity, asymmetry, and human pressure.

Examples:

- Neutral both-sides framing where the source had a stance.
- Generic examples that feel specific to nobody.
- No named people, places, moments, or stakes.
- One register throughout.
- Fewer pronouns and less personal commitment after rewriting.

Severity:

- Mostly manual/self-audit, because regex cannot reliably inspect meaning.
- Should be prominent in the workflow before surface cleanup.

Current checks and guidance:

- `no-false-concession-hedges`
- `no-orphaned-demonstratives`
- semantic preservation check
- experiential vacancy guidance
- tonal uniformity / register lock manual check
- faux specificity manual check
- neutrality collapse manual check

### 6. Genre Misfit

A device is legitimate in one genre and suspicious in another.

Examples:

- Em dashes in literary prose vs generic business prose.
- Headings in documentation vs personal essay.
- Rhetorical questions in teaching prose vs thought-leadership filler.
- Staccato in dialogue/comedy vs generic emphasis.
- Rhyme/quatrains in poetry.
- Flat dialogue/exposition in fiction.

Severity:

- Mode and genre dependent.
- Hard mode minimizes risk.
- Light mode can preserve with disclosure.
- Medium removes hard failures and strong warnings, and discloses context warnings.

Current checks:

- `no-em-dashes`
- `no-curly-quotes`
- `no-staccato-sequences`
- `no-anaphora`
- `no-rhetorical-questions`
- `no-quietness-obsession`
- `no-ghost-spectral-density`
- genre-specific manual checks

## Source Governance

Each source should be assigned an evidence role.

### Corpus Evidence

Sources:

- Kobak et al., Science Advances, excess vocabulary.
- GPTZero vocabulary list.
- Juzek/Ward `delve`-style academic vocabulary work.

Use:

- Vocabulary pressure and aggregate reporting.
- Not direct authorship claims.
- Do not make single-word proof rules.

### Craft Evidence

Sources:

- Shreya Shankar.
- Practitioner guides.
- User-observed failure modes.

Use:

- Rewrite guidance.
- Manual/self-audit prompts.
- Regex only when the construction is narrow enough to test.

### Editorial / Provenance Evidence

Sources:

- Clarkesworld reporting.
- Sports Illustrated/Futurism reporting.
- OpenAI sycophancy rollback.

Use:

- Provenance checks.
- Assistant residue checks.
- Genre-specific review prompts.

### Bias / Ethics Evidence

Sources:

- Stanford HAI detector-bias reporting.
- GPTZero 2026 architecture paper.

Use:

- Transparency architecture.
- Mode summaries.
- "Warnings, not accusations" framing.

## Proposed Refactor

### Phase 1: Add Failure-Mode Metadata

Add metadata for every check:

```python
"no-manufactured-insight": {
    "severity": "strong_warning",
    "failure_modes": ["synthetic_significance"],
    "evidence_role": "rhetorical_pattern",
    "guidance": "...",
}
```

Keep existing `severity` behavior unchanged.

Acceptance criteria:

- All 43 checks have `failure_modes`.
- Tests fail if metadata is missing.
- CLI JSON includes failure modes.

### Phase 2: Reorganize Reports

Change reports so results are grouped by failure mode first, then severity.

Current report shape:

- severity
- check name
- evidence

Target report shape:

- Provenance residue
- Synthetic significance
- Frictionless structure
- Generic abstraction
- Voice erasure
- Genre misfit

Each group lists:

- failed checks
- evidence snippets
- mode consequence
- whether the agent fixed, preserved, or needs user decision

Acceptance criteria:

- `grade.py` includes `failure_mode_results`.
- `mode_results` remains backward-compatible.
- `dev/evals/test_grade.py` asserts grouping behavior.

### Phase 3: Split Vocabulary Strategy

Keep all current vocabulary sources, but make their role explicit.

Vocabulary sources:

- local curated AI vocab
- GPTZero 100 phrases
- Kobak 900 row CSV
- construction regexes (`landed`, `surface`, `hidden`, `actually`, `aligns with`)

Target behavior:

- `no-ai-vocabulary-clustering` remains as a strong warning for dense local/GPTZero/construction clusters.
- `vocabulary_pressure_profile` remains as aggregate evidence.
- Kobak remains pressure only.
- Source labels appear in evidence output so users can see whether a hit came from GPTZero, Kobak, local list, or construction regex.

Acceptance criteria:

- Evidence distinguishes `local`, `gptzero`, `kobak`, and `construction`.
- Tests cover each source.
- Literal controls for `landed` and `surface` continue to pass.

### Phase 4: Calibrate Aggregate Pressure

Do not tune by intuition. Use the three corpora:

- existing samples
- human-sourced samples
- generated-AI samples

Current aggregate result:

- existing: `7/19`
- human-sourced: `8/47`
- generated-AI: `13/18`

Target:

- Generated-AI coverage remains meaningfully higher than human-sourced coverage.
- Human-sourced hits remain context warnings and are inspectable.
- Any threshold change must include a before/after table.

Acceptance criteria:

- Sweep report includes aggregate hit counts.
- Test suite includes calibration fixtures.
- `dev/TESTING.md` documents expected aggregate behavior.

### Phase 5: Rewrite Documentation Around Failure Modes

Update:

- `README.md`
- `human-eyes/SKILL.md`
- `human-eyes/references/patterns.md`
- `dev/TESTING.md`

Documentation should stop leading with "38 patterns across 8 categories" as the conceptual model. Keep the full pattern catalogue, but introduce failure modes first.

Acceptance criteria:

- README explains the six failure modes.
- SKILL workflow instructs agents to reason by failure mode.
- references/patterns.md maps every pattern to a failure mode.
- Source hierarchy remains intact.

## Risks

### Risk: Losing Useful Specific Checks

Mitigation:

- Do not delete checks during metadata refactor.
- Only move and relabel.
- Keep regression tests for existing check names.

### Risk: Over-abstracting the Skill

Mitigation:

- Failure modes organize the report, but checks still provide concrete evidence.
- Keep examples and before/after rewrites.

### Risk: Aggregate Pressure Becomes a Black Box

Mitigation:

- Output component scores and source labels.
- Keep aggregate pressure as context warning unless the user chooses Hard mode.

### Risk: Genre Misfit Gets Ignored

Mitigation:

- Mode report must show preserved warnings.
- Light mode can preserve with disclosure.
- Medium and Hard remain stricter.

## Immediate Next Step

Implement Phase 1 only:

1. Add `failure_modes` metadata to all checks.
2. Add test coverage that every check has at least one failure mode.
3. Emit failure modes in JSON.
4. Do not change pass/fail behavior yet.

This gives the system a coherent skeleton without destabilizing the working grader.
