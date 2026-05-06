# Grammarly: Common AI words and phrases
## Metadata
- **URL:** https://www.grammarly.com/blog/ai/common-ai-words/
- **Author / owner:** Grammarly
- **Published:** Updated 2025-04-09
- **Extracted:** 2026-05-05
- **Source type:** Vendor writing guide
- **Evidence tier:** Vendor / detector pages
- **Extraction status:** second-pass reviewed from Grammarly page on 2026-05-05

## Summary
Cited for common AI indicator words and phrases. It is a tentative phrase-list source.

## Main insights
- Useful as weak corroboration.
- Vendor list should not define severity alone.
- Needs extraction and deduplication.

## Evidence and claims to extract
- Direct source reviewed: Grammarly blog page.
- Grammarly frames common AI words as clues because LLMs predict likely next words from learned patterns.
- The page groups signals into high-frequency words, transition/structured phrases, qualifiers/softening words, and analytical/academic words.
- Named examples include "delve into", "underscore", "pivotal", "realm", "harness", "illuminate", "that being said", "at its core", "to put it simply", "a key takeaway is", "generally speaking", "typically", "tends to", and "arguably".
- Grammarly's examples are prescriptive writing advice with alternatives, not an empirical detector study.

## Skill-use audit
- **Good use:** Weakly backs #7, #22, #23, and #50 as practitioner/vendor corroboration for common AI-ish phrasing.
- **Misuse / overclaim:** It should not define severity or prove AI generation. The page says terms can offer clues, not verdicts.
- **Unsupported use:** Compared with Kobak/Juzek/GPTZero, this is a less rigorous source for vocabulary frequency.
- **Underused evidence:** It supports separating lexical substitutions from structural rewrites: many examples are direct replacement candidates for `alternatives.md`.
- **Patterns left on the table:** "Analytical and academic words" may overlap with #47 soft explainer scaffolding and #43 corporate AI-speak, but should be deduplicated before adding anything.

## Matched patterns / rules
- #7 AI vocabulary words and phrases
- #22 filler phrases
- #50 formulaic openers

## Associated hypotheses
- H7 five-check gating plus advisory catalogue

## Questions / follow-up
- Which Grammarly examples are already covered by `patterns.json` and `alternatives.md`?
- Should Grammarly stay citation-only in alternatives rather than pattern severity?
