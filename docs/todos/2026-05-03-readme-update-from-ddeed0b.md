# TODO: Update README from ddeed0b prose to current state

**Status:** open. Mae's saved prose is restored to disk. Facts need updating without losing the prose. Mae has not authorised any prose changes; this todo captures the work for the next session.
**Date:** 2026-05-03.
**Hands off from:** session 4678d21a-562b-4fa6-83b0-b8eb84093428.

---

## Current state on disk

`README.md` is the 244-line `ddeed0b` version ("docs: rewrite README with honest narrative and findings", 2026-04-30 07:49). This is Mae's saved prose from before the audit-report-redesign Phase 1-3 work. The previous on-disk state (308 lines from `bfbc1f6`) was retrievable via `git show HEAD:README.md`. The restoration was done in the prior session; Mae did not authorise it. Do not undo it without her explicit instruction.

The plan that drove the rewrite is `dev/plans/2026-04-30-readme-rewrite-and-hypothesis-log.md`. Read it before starting.

---

## What needs updating

The prose stays. The facts below are stale and need correction:

1. **Tagline / "Why this exists" para 2.** Reads "43 programmatic checks across 38 patterns". Current state: 49 programmatic checks across 53 numbered patterns plus 5 sub-letter variants (10a, 23a, 31a, 35a, 35b) plus 1 unnumbered aggregate meta-check (`overall-ai-signal-pressure`). Add the dual-layer framing: regex/density grader + eight-item agent-judgement registry.

2. **"What it does".** The five-action list (Audit, Suggest, Rewrite, Write, Save report) stays. Add a paragraph describing the dual-layer audit render: Layer 1 orientation block (Severity verdict line + per-flag blocks with glyphs `x` `!` `?`), Layer 2 eight per-category coverage sub-tables, parallel agent-judgement block separated by `---`, single-line collapse when all clear and no pressure triggered.

3. **Install.** Add `python3 -m pip install PyYAML` line at the top of the install block, with a one-line comment explaining it is the registry-backed grader's dependency. Phase 2 added this.

4. **Performance block.** Auto-block markers (`<!-- performance:start -->` / `<!-- performance:end -->`) must be preserved — the iteration harness writes between them. Current numbers should be iteration-5 (2026-05-02): 84.9% mean pass rate, 13 regressions vs prev iteration. Optional: add a one-line transparency caveat outside the markers.

5. **Representative output.** The example currently shows the old single-block format. Regenerate with the current grader against a sample from `dev/evals/samples/` to show the new dual-layer format (Severity line, glyph-prefixed flags, `---` separator, eight category sub-tables).

6. **Patterns table.** Currently 38 rows. Expand to 53 numbered + 5 sub-letter variants + 1 meta. Add Source and Severity columns per the plan correction in `dev/plans/2026-04-30-readme-rewrite-and-hypothesis-log.md` ("R4 correction — README patterns table is Source + Severity, not Strength + Source"). Source data: `dev/research/2026-04-30-per-pattern-evidence-map.md`. Severity data: `humanise/grade.py` `CHECK_METADATA` (values: `hard_fail` / `strong_warning` / `context_warning`).

7. **Eight-item agent-judgement registry table.** Missing entirely. Add after the patterns table. Source: `humanise/judgement.yaml`. Columns: Item / Pattern ref / Schema. Items: Structural monotony, Tonal uniformity (#35), Faux specificity (#36), Neutrality collapse (#37), Even jargon distribution, Forced synesthesia (#28), Generic metaphors (#30), Genre-specific watchlist (#41).

8. **"What's next".** Reflect that audit-report-redesign Phase 1-3 has landed (per plan completion commit `8be730b`). Link to `dev/hypotheses.md` (untracked but exists) for the SUSPECT items deferred from this work.

9. **File structure.** Add `judgement.yaml` (eight-item registry, Phase 1), `patterns.yaml` and `vocabulary.yml` (Phase 2 registries), and any other files added in Phase 1-3 that are missing from the current diagram.

---

## Constraints

- **Preserve Mae's prose.** This is the load-bearing constraint. Voice, structure, framing, ordering — all stay. Only correct factual content and add the missing tables / paragraphs called out above. If a fact correction would force a sentence rewrite, surface the rewrite to Mae before making it; do not silently rephrase.
- **Voice spec from the plan applies to any new prose written.** Zero em dashes in newly drafted sentences. No authorial "we" / "our" / "us" in new prose (existing instances stay unless Mae says otherwise). Australian spelling. Severity vocabulary is `hard_fail` / `strong_warning` / `context_warning` — not "must-fix / consider / nudge", which was an earlier invented vocabulary.
- **No commits without Mae's explicit go-ahead.** Per plan R6.
- **Section by section.** Confirm structural skeleton with Mae before drafting. Show each section's diff before moving on.
- **Mae does not currently trust the agent.** Make every change visible before applying. Do not batch.

---

## What not to do

- Do not run any `git checkout`, `git restore`, `git reset`, or `git commit -- README.md` on Mae's behalf without her saying so explicitly in the current session.
- Do not regenerate or "modernise" the prose. The prose is the part she worked hard at. Touch only the listed factual content.
- Do not add sections that did not exist before. Restrict additions to the dual-layer audit paragraph, the agent-judgement registry table, and the PyYAML install line.
- Do not infer permission from ambiguous distressed language. If she is keysmashing or upset, wait for an unambiguous instruction.

---

## Verification before commit (when Mae authorises)

- `python3 humanise/grade.py --format markdown --depth all README.md` runs clean at the gating action level.
- `grep -c '—' README.md` low and intentional (existing em dashes in original prose may stay if Mae wants them).
- Patterns table row count matches the catalogue.
- Eight-item registry table matches `humanise/judgement.yaml`.
- Sources section retains every entry from the pre-restore version.
