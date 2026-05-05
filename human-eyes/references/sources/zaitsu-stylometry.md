# Zaitsu et al.: Stylometry can reveal AI authorship
## Metadata
- **URL:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369
- **Author / owner:** Wataru Zaitsu, Mingzhe Jin, Shunichi Ishihara, Satoru Tsuge, and Mitsuyuki Inaba
- **Published:** 2025-10-27
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from PLOS One full article abstract

## Summary
Japanese-language study with two parts: stylometric detection potential and human detection ability. Study 1 compares 100 human-written public comments with 350 texts from seven LLMs using phrase patterns, part-of-speech bigrams, and function-word unigrams; Study 2 asks 403 Japanese participants to judge AI versus human texts.

## Main insights
- Stylometric feature combinations can distinguish AI and human texts in this setting, but human participants had limited detection ability.
- The abstract reports 99.8% random forest accuracy and perfect discrimination on integrated stylometric MDS dimensions.
- Participants relied on superficial impressions such as phraseology, expression, word endings, conjunctions, and punctuation.
- The language and genre scope matters: Japanese public comments, not English prose generally.

## Evidence and claims to extract
- Study 1 sample: 100 human-written public comments and 350 LLM-generated texts from ChatGPT GPT-4o/o1, Claude 3.5, Gemini, Microsoft Copilot, Llama 3.1, and Perplexity.
- Feature families: phrase patterns, POS bigrams, and function-word unigrams.
- Classifier result: random forest reached 99.8% accuracy.
- Human study: 403 participants; overall human AI-detection ability was limited, and ChatGPT o1 was more likely to mislead participants into judging outputs human-written.

## Skill-use audit
- **Good use:** Back H3 detector-framing caution and H1 feature-comparison framing.
- **Misuse / overclaim:** Do not transfer Japanese-public-comment feature directions to English human-eyes rules without separate evidence.
- **Weakly backed by this source:** #52 and #53 only as broad feature-family context, not specific thresholds.
- **Underused evidence:** The human-study component can support user-facing cautions that surface cues may feel persuasive while still being unreliable for authorship classification.
- **Patterns left on the table:** Human reliance on superficial phrase/punctuation cues is useful as a warning against user-facing certainty.

## Matched patterns / rules
- #52 sentence rhythm variance
- #53 vocabulary diversity
- H3 / detector-framing caution
- punctuation and function-word features (context only)

## Associated hypotheses
- H1 calibrated register-distance score
- H2 comparison-engine product reframe
- H3 drop detection framing

## Questions / follow-up
- Should human-eyes explicitly warn that the cues humans notice are not necessarily the cues that robust classifiers use?
- Are any full-paper feature directions reusable for English, or should this remain language-specific context?
