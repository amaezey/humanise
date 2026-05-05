# Fred Rohrer: promotional register and n-gram analysis
## Metadata
- **URL:** https://blog.frohrer.com/how-to-detect-llm-writing-in-text/
- **Author / owner:** Fred Rohrer
- **Published:** 2025-07-28
- **Extracted:** 2026-05-05
- **Source type:** Practitioner analysis
- **Evidence tier:** Practitioner / teacher / editor essays
- **Extraction status:** second-pass reviewed from Fred Rohrer article/search excerpt

## Summary
Practitioner article on detecting LLM writing through linguistic/stylistic recognition and statistical approaches. Rohrer warns detection is not foolproof and varies by model, then lists promotional/emphatic language, editorial voice, structural conventions, typographical/markup indicators, citations, conversational artifacts, placeholders, platform artifacts, entropy/perplexity, Markov chains, n-grams, vocabulary diversity, AUC, and repetition patterns.

## Main insights
- Useful practitioner support for promotional-register and n-gram/vocabulary-diversity claims.
- Weaker than academic stylometry sources; treat it as feature taxonomy and pattern discovery, not validated thresholds.
- Strongly supports keeping model-variation and not-foolproof caveats attached to detector-like claims.

## Evidence and claims to extract
- Direct caveat: LLM text is harder to detect, detection varies between models, and the methods are not foolproof.
- Promotional/emphatic examples: "stands as a testament", "plays a vital role", "underscores its importance", "rich cultural heritage", "breathtaking landscapes", "enduring legacy".
- Editorial voice examples: "it's important to note", "no discussion would be complete without", "defining feature", "powerful tools".
- Structural examples: mechanical connectors such as "moreover", "furthermore", "on the other hand"; section summaries beginning "In summary" or "Overall".
- Technical/provenance examples: markdown artifacts, curly quotes, hallucinated citations, invalid DOIs/ISBNs, chatbot artifacts, placeholders, platform citation bugs, and `utm_source=chatgpt.com`.
- Statistical approaches: entropy/perplexity, Markov transition analysis, n-gram frequency, MTLD, hapax legomena, AUC, and repetition detection.

## Skill-use audit
- **Good use:** Back practitioner descriptions for #4, #22, #49-adjacent typographic artifacts, #52/#53 feature families, citation/provenance anomalies, and platform artifacts.
- **Misuse / overclaim:** Do not treat Rohrer as empirical validation for thresholds or authorial certainty.
- **Weakly backed by this source:** Exact severity assignments.
- **Underused evidence:** Platform artifacts, bad citations, and `utm_source=chatgpt.com` are more concrete than the broad detection framing and could become provenance checks.
- **Patterns left on the table:** Platform-specific artifacts such as broken citation tokens and `utm_source=chatgpt.com` are concrete checks not fully represented in the current catalogue.

## Matched patterns / rules
- #4 promotional language
- #53 vocabulary diversity
- #52 sentence rhythm variance / structural regularity
- #22 filler phrases
- citation/provenance anomalies
- chatbot/platform artifacts
- model-variation/detector-caution context

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Which platform-artifact checks belong in deterministic rules versus manual provenance review?
