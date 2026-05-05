# GPTZero: AI Vocabulary
## Metadata
- **URL:** https://gptzero.me/ai-vocabulary
- **Author / owner:** GPTZero
- **Published:** Living page; list updated 2026-05
- **Extracted:** 2026-05-05
- **Source type:** Vendor vocabulary guide
- **Evidence tier:** Vendor / detector pages
- **Extraction status:** second-pass reviewed from GPTZero page on 2026-05-05

## Summary
Provides a public list of AI-associated words and phrases. human-eyes uses it as a clustering signal, not a score.

## Main insights
- Useful phrase list.
- Vendor detector framing should not be imported.
- Keep vocabulary scanning separate from probability claims.

## Evidence and claims to extract
- Direct source reviewed: GPTZero AI Vocabulary page.
- GPTZero says its AI Vocabulary feature detects frequent words and phrases used by ChatGPT, Gemini, Claude, and other models in its dataset.
- The page says the top-50 list is ranked from research over 3.3 million texts and compares AI documents against human documents.
- GPTZero says listed terms are used by AI at least 2-3x more than by humans, with top-50 terms ranging from 10x to 200x+.
- Critical limitation from source: GPTZero explicitly says the vocabulary tool is not equivalent to its AI probability score, and a fully human text can still include AI-frequent vocabulary.

## Skill-use audit
- **Good use:** Backs #7 as a vendor phrase-list and supports vocabulary as an advisory clustering signal.
- **Misuse / overclaim:** The source itself warns against treating vocabulary hits as AI probability. Any hard-fail or authorship claim based on GPTZero vocabulary would misuse the source.
- **Weakly backed by this source:** GPTZero's page is vendor-maintained and does not expose the full dataset or method enough to define severity alone.
- **Underused evidence:** The explicit "not probability" caveat should be reflected in human-eyes vocabulary guidance and signal-stacking language.
- **Patterns left on the table:** GPTZero names perplexity, burstiness, and generic/repetitive style as detector factors. Human-eyes already has sentence rhythm and vocabulary diversity hypotheses, but should not import the proprietary detector frame.

## Matched patterns / rules
- #7 AI vocabulary words and phrases
- overall-signal-stacking

## Associated hypotheses
- H1 calibrated register-distance score
- H7 five-check gating plus advisory catalogue

## Questions / follow-up
- Should the GPTZero-derived phrase list be visually separated from peer-reviewed vocabulary evidence?
- Does the audit need a note when vocabulary is the only signal source?
