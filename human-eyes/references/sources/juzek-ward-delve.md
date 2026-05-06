# Juzek and Ward: Why Does ChatGPT Delve So Much?
## Metadata
- **URL:** https://aclanthology.org/2025.coling-main.426/
- **Author / owner:** Tom S. Juzek and Zina B. Ward
- **Published:** 2025-01
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from ACL Anthology page on 2026-05-05

## Summary
Studies lexical overrepresentation, especially the visibility of words such as "delve" in LLM-associated writing. human-eyes uses it to support narrow vocabulary-spike claims.

## Main insights
- Strong for specific excess words.
- Mechanism is more useful than document-level detection framing.
- Best paired with Kobak rather than cited alone.

## Evidence and claims to extract
- Direct source reviewed: ACL Anthology metadata and abstract.
- The paper studies scientific English and finds 21 focal words whose increased occurrence in scientific abstracts is likely due to LLM usage.
- Named focal examples in the abstract include "delve", "intricate", and "underscore".
- The authors test possible causes of lexical overrepresentation and report no evidence that model architecture, algorithm choices, or training data explain it.
- RLHF is treated as a plausible contributor, but the abstract also notes that participant reactions to "delve" may differ from reactions to other focal words.
- Limit: the paper supports lexical overrepresentation in scientific abstracts, not generic authorship detection for all prose.

## Skill-use audit
- **Good use:** Backs #7 as a narrow scientific-abstract vocabulary signal and supports vocabulary clustering in `overall-signal-stacking`.
- **Misuse / overclaim:** The paper should not be used to justify the whole GPTZero-style 100 phrase list, nor to hard-fail arbitrary prose for a word such as "delve".
- **Unsupported use:** It does not directly support structural rules, em dashes, assistant residue, or literary/marketing-register claims.
- **Underused evidence:** The "21 focal words" should be extracted into a source-specific list and compared against `patterns.json` and `kobak-excess-words.csv`.
- **Patterns left on the table:** No new pattern family beyond vocabulary, but the source suggests separating "scientific focal words" from broader practitioner phrase lists.

## Matched patterns / rules
- #7 AI vocabulary words and phrases
- overall-signal-stacking

## Associated hypotheses
- H1 calibrated register-distance score
- H7 five-check gating plus advisory catalogue

## Questions / follow-up
- Which of the 21 focal words are already covered by the current vocabulary rules?
- Should scientific focal words carry different guidance from general AI-slang phrases?
