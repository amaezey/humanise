# Liang et al.: GPT detectors are biased against non-native English writers
## Metadata
- **URL:** https://www.cell.com/patterns/fulltext/S2666-3899(23)00130-7
- **Author / owner:** Weixin Liang, Mert Yuksekgonul, Yining Mao, Eric Wu, and James Zou
- **Published:** 2023-07
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from ScienceDirect/Stanford summaries on 2026-05-05

## Summary
Shows detector false-positive risk for non-native English writers. human-eyes uses it to justify warnings, not accusations.

## Main insights
- User-facing language must avoid authorship verdicts.
- False-positive risk should be part of pattern disambiguation.
- Supports process safeguards.

## Evidence and claims to extract
- Direct source reviewed: ScienceDirect article summary and Stanford SCALE listing.
- Study setup: seven GPT detectors evaluated on 91 TOEFL essays by non-native English writers and 88 US eighth-grade essays.
- Main quantified finding: average false-positive rate on TOEFL essays was 61.3%; all detectors unanimously flagged 19.8% of human TOEFL essays; at least one detector flagged 97.8% of TOEFL essays.
- Mechanism noted in the source: lower perplexity in TOEFL essays contributed to detector misclassification.
- Limit: this source critiques detector fairness; it does not supply a positive pattern catalogue for human-eyes.

## Skill-use audit
- **Good use:** Strongly backs human-eyes avoiding authorship verdicts and using warnings/review framing.
- **Misuse / overclaim:** It should not be cited as evidence that any human-eyes pattern identifies AI writing. It is evidence that detector framing can harm non-native writers.
- **Unsupported use:** No individual pattern should claim support from Liang et al. unless the claim is about false positives, bias, or process safeguards.
- **Underused evidence:** This should be connected to every user-facing place that says "AI generated", "detector", or implies authorship classification.
- **Patterns left on the table:** Not a pattern source; it argues for disambiguation and uncertainty language around all surface/register features.

## Matched patterns / rules
- Overall audit stance
- field-guide disambiguation
- no authorship classification

## Associated hypotheses
- H3 drop detection framing
- H9 similar-species disambiguation

## Questions / follow-up
- Should every source-backed pattern card include a false-positive/look-alike note when used on non-native English prose?
- Should README wording move further from "detects" toward "surfaces register features"?
