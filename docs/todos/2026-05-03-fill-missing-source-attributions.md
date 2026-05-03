# TODO: Fill missing Source attributions in README patterns table

**Status:** open. Captured during the 2026-05-03 README restore session as task #21 in the in-session tracker; persisted here so it survives the session.
**Date:** 2026-05-03.

---

## What needs doing

The README's patterns table at `README.md` covers 53 numbered patterns + 5 sub-letter variants + 1 meta. Source attributions are filled in for the 38 entries Mae had curated earlier, plus 6 of the new entries that the evidence map already covers (23a, 31a, 35a, 39, 40, 41). The remaining new rows have blank Source cells:

- 10a — Triad density
- 35b — Repeated 'This...' chains
- 42 — Manufactured insight framing
- 43 — Corporate AI-speak
- 44 — Signposted conclusion
- 45 — Nonliteral land/surface phrasing
- 46 — Bland critical template
- 47 — Soft explainer scaffolding
- 48 — Dense negation
- 49 — Em dashes
- 50 — Formulaic openers
- 51 — Mechanical repeated sentence starts
- 52 — Sentence rhythm variance
- 53 — Vocabulary diversity
- meta — AI pressure from stacked signals

That is 14 new rows plus the meta with no Source attribution.

---

## Where Source data lives

- `dev/research/2026-04-30-per-pattern-evidence-map.md` — Mae's curated per-pattern evidence map. Currently covers patterns 1–41 plus sub-letters 23a, 31a, 35a, plus 38 (out of order). Does not yet cover 10a, 35b, 42–53, or the meta-check.
- `humanise/scripts/patterns.json` — each entry has a `patterns_md_body` field with inline source mentions (often "**Source:**" or named attributions in prose). Could be parsed or read manually.
- `humanise/references/patterns.md` — generated from `patterns.json`; same source material as `patterns_md_body`.

---

## Two ways to close this

1. **Extend the evidence map** to cover the missing patterns. Add new H3 sections per the existing template (Sources, Why it's in the skill, How AI uses it, Evidence basis, Severity, Source claims, Notes). Then port the Source line into the README table.
2. **Pull from `patterns_md_body` per pattern** as a faster but lower-quality option. The bodies have inline citations. Read them, summarise the primary source(s) per row, paste into the README table cell.

Option 1 is the higher-quality long-term work. Option 2 is good enough for an interim fill.

---

## Constraints

- Voice spec applies to any new prose: zero em dashes in newly drafted sentences; no authorial "we" / "our" / "us" in new prose; Australian spelling; severity vocabulary is `hard_fail` / `strong_warning` / `context_warning`.
- Source attributions in the table follow Mae's existing format: semicolon-separated primary sources, with parenthetical role/year where useful (e.g., "Belcher; Juzek & Ward; Sun et al. (via Wikipedia)").
- Wikipedia (editor consensus) is the canonical attribution for patterns in the WikiProject AI Cleanup catalogue without an external upstream citation. Do not invent a source.

---

## Verification

- Every row in `README.md`'s patterns table has a non-blank Source cell, OR
- Rows that genuinely have no source attribution carry a deliberate marker (e.g., `n/a`) and the README intro paragraph notes that some new rows are pending source curation.
