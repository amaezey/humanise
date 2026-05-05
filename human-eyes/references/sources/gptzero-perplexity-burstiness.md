# GPTZero: Perplexity and burstiness
## Metadata
- **URL:** https://gptzero.me/news/perplexity-and-burstiness-what-is-it/
- **Author / owner:** GPTZero
- **Published:** 2023-03-01
- **Extracted:** 2026-05-05
- **Source type:** Vendor explainer
- **Evidence tier:** Vendor / detector pages
- **Extraction status:** second-pass reviewed from GPTZero post on 2026-05-05

## Summary
Explains detector concepts such as perplexity and burstiness. human-eyes uses it as architecture/background context.

## Main insights
- Transparent mixed evidence is useful.
- Detector scores are not part of human-eyes.
- May inform full-report language.

## Evidence and claims to extract
- Direct source reviewed: GPTZero post by Edward Tian.
- The post describes perplexity and burstiness as the statistical layer of GPTZero's first detection model.
- It defines sentence-level perplexity as a measure of how likely a language-model-like system would choose the same words in the document.
- It defines burstiness as variation in writing patterns and perplexity across a document, contrasting human variation with lower-variation model output.
- The post says statistical signals are only one layer among several upgraded detector indicators.

## Skill-use audit
- **Good use:** Supports the general idea behind rhythm, diction-variation, and transparent multi-signal reporting.
- **Misuse / overclaim:** It is vendor detector architecture, not evidence that human-eyes should output AI probability or detector scores.
- **Unsupported use:** It does not directly validate any current human-eyes regex pattern.
- **Underused evidence:** Burstiness aligns with #52 sentence rhythm variance and #53 vocabulary/diction diversity, but should be reframed as document-level variation rather than detector probability.
- **Patterns left on the table:** None as direct pattern evidence; perplexity stays out of scope for the deterministic grader and burstiness-style variation is tracked through structural-metric hypotheses.

## Matched patterns / rules
- #52 sentence rhythm variance (conceptual support)
- #53 vocabulary diversity / diction variation as vendor detector-feature framing
- Overall audit architecture; no direct phrase pattern

## Associated hypotheses
- H3 drop detection framing
- H4 single-source registry plus JSON contract

## Questions / follow-up
- Should human-eyes use "variation" language instead of "burstiness" to avoid importing detector framing?
- Should this source remain architecture background?
