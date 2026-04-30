# TODO: Grader integrity gaps — Group A and Group B

**Status:** open todo. Captured for follow-up; not actioned in the 2026-04-30 README rewrite plan. Mae will hand off to another agent.
**Surfaced during:** U1d severity-lookup pass over the per-pattern evidence map.
**Date:** 2026-04-30.

---

## Summary

Two symmetric integrity gaps between `humanise/references/patterns.md` and `humanise/grade.py`:

- **Group A: described but unenforced.** 17 numbered patterns in patterns.md have no programmatic check.
- **Group B: enforced but undocumented.** 8 programmatic checks in grade.py have no numbered pattern in patterns.md.

Both compromise the skill's transparency claim. Group B is the more concerning of the two: the grader fires on user prose using a check the user cannot read about in the catalogue.

---

## Group A — patterns described in patterns.md, no programmatic check

### Intrinsically manual (sensible — these are not regex shapes)

- #28 Forced synesthesia
- #30 Generic / ungrounded metaphors
- #35 Tonal uniformity / register lock
- #36 Faux specificity
- #41 Genre-specific manual checks

These belong in the catalogue as self-audit prompts. They cannot be programmatic without false-positive explosion.

### Could be programmatic but never were

- #2 Notability claims
- #5 Vague attributions
- #11 Synonym cycling
- #12 False ranges
- #13 Boldface overuse
- #14 Inline-header lists
- #15 Title case in headings — may already fold into `no-markdown-headings`; needs verification
- #16 Emojis
- #18 Hyphenated compound modifier overuse
- #20 Knowledge-cutoff disclaimers — may already fold into `no-collaborative-artifacts`; needs verification
- #21 Sycophantic / servile tone — may already fold into `no-collaborative-artifacts`; needs verification
- #37 Neutrality collapse

### Origin

`git log -S` returns commit `618c723` ("refactor: separate skill files from dev files for clean installs", 2026-04-08) for almost all of them — but that's a file-move refactor, not the original introduction. The strings existed in patterns.md before that. No single introducing commit; these are "always been described but never enforced" rather than a regression.

---

## Group B — programmatic checks in grade.py, no numbered pattern

### Inventory

| Check | Severity | First introducing commit |
|---|---|---|
| `check_manufactured_insight` | strong_warning | `618c723` (2026-04-08 refactor) |
| `check_corporate_ai_speak` | strong_warning | `618c723` (2026-04-08 refactor) |
| `check_signposted_conclusions` | context_warning | `618c723` (2026-04-08 refactor) |
| `check_nonliteral_land_surface` | strong_warning | `1422bad` ("fix: calibrate hard-mode writing signals", 2026-04-27) |
| `check_bland_critical_template` | strong_warning | `9ce1cec` ("feat: expand AI writing signal framework", 2026-04-27) |
| `check_soft_scaffolding` | strong_warning | `9ce1cec` (2026-04-27) |
| `check_negation_density` | context_warning | `9ce1cec` (2026-04-27) |
| `check_overall_signal_pressure` | context_warning | `9ce1cec` (2026-04-27) |

### Diagnostic detail: the 9ce1cec asymmetry

Commit `9ce1cec` was the Vollmer-driven 2026-04-27 source-review session. That session **did update patterns.md** when it added the new checks for #35a (orphaned demonstratives), #23a (false concession), #31a (Unicode flair), #39 (placeholders), and #40 (rubric echoing). It just chose not to enumerate four other checks (`check_bland_critical_template`, `check_soft_scaffolding`, `check_negation_density`, `check_overall_signal_pressure`) in the catalogue.

That isn't a refactor artefact. It's an asymmetric edit: the session knew how to update both files and only did it for some of the additions. Whoever drove that session either did not surface these four to patterns.md deliberately or did not register them as new patterns at all.

### Origin context for Group B

- `618c723` (April 8): the file-move refactor. Three checks (`manufactured_insight`, `corporate_ai_speak`, `signposted_conclusions`) appear in the moved location for the first time. Their original introduction is earlier than April 8; the move commit just happens to be where `git log -S` lands. They are likely from the structural-AI-detection PR (#4) merged earlier on the `refs/tags/latest` history line.
- `1422bad` ("fix: calibrate hard-mode writing signals", April 27): added `check_nonliteral_land_surface` during a calibration pass, not a feature pass.
- `9ce1cec` ("feat: expand AI writing signal framework", April 27): added the four checks above.

---

## Why this matters

The skill's public framing (in README, SKILL.md, and the per-pattern catalogue) is that every grader check has a documented basis. Group B violates that directly: a user whose prose triggers `no-bland-critical-template` or `no-soft-scaffolding` cannot read about that pattern in patterns.md. The check fires from a black box.

Group A is a softer integrity issue: the catalogue claims more than the grader does. A user reading patterns.md sees a 41-pattern catalogue and assumes commensurate grader coverage; in fact 17 of those entries are catalogue-only. Some of that is correct design (the manual-only ones); some of it is unfinished work.

---

## Proposed handling

Out of scope for the 2026-04-30 README rewrite plan. Resolution requires its own plan. Sketch of what that plan would do:

**For Group A — for each "could be programmatic" entry:**
- Decide write-check vs declare-manual.
- For the "may already fold into X" entries, verify and either remove the standalone catalogue entry or note the fold explicitly.

**For Group B — for each undocumented check:**
- Read the check implementation.
- Either write a numbered patterns.md entry with sources and rationale, or remove the check on the basis that an undocumented enforcement is worse than no enforcement.
- For the four checks from `9ce1cec`, surface the asymmetry in the catalogue as a known gap until resolved.

---

## Cross-references

- Per-pattern evidence map (internal, gitignored): `dev/research/2026-04-30-per-pattern-evidence-map.md`.
- 2026-04-30 README rewrite plan (where U1d surfaced this): `dev/plans/2026-04-30-readme-rewrite-and-hypothesis-log.md`.
- Hypothesis log: `dev/hypotheses.md` — consider adding two entries (one per group) when this is picked up.
