# NetusAI: stylometry and AI detectors
## Metadata
- **URL:** https://netus.ai/blog/stylometry-explained-how-ai-detectors-fingerprint-your-writing
- **Author / owner:** Ejaz Ahmad / NetusAI
- **Published:** 2025-07-22
- **Extracted:** 2026-05-05
- **Source type:** Vendor explainer
- **Evidence tier:** Vendor / detector pages
- **Extraction status:** second-pass reviewed from NetusAI article

## Summary
Vendor explainer on stylometry and AI detectors. It describes stylometry as measuring writing style rather than meaning and lists sentence burstiness, lexical density, punctuation/structure, and contextual glue as detector-relevant feature families.

## Main insights
- Weaker than academic stylometry sources, but useful for plain-English feature taxonomy.
- It directly names low burstiness, formal diction, missing colloquial spikes, transition overuse, uniform bullet/list formatting, and perfect grammar as stylometric risk signals.
- Because it markets humanizing/detector-bypass tools, its advice should be treated as vendor/practitioner guidance.

## Evidence and claims to extract
- Feature families named: sentence length/structure variance, filler/formal vocabulary, pronouns/passive voice, comma/dash/semicolon ratios, paragraph openers, bullet/list uniformity, transitions, and grammar cleanliness.
- It explicitly says detectors target patterns, not ideas or accuracy.
- It says traditional clean writing can increase false-positive risk.

## Skill-use audit
- **Good use:** Back #52/#53 feature-family explanations as vendor/plain-English context when paired with academic sources.
- **Misuse / overclaim:** Do not cite as empirical validation for thresholds.
- **Weakly backed by this source:** Exact rule severities.
- **Underused evidence:** The false-positive warning for traditionally clean writing is useful user-facing caveat language.
- **Patterns left on the table:** None as pattern evidence; "detectors target patterns, not prose quality" is promoted only as user-facing caveat language.

## Matched patterns / rules
- #52 sentence rhythm variance (context)
- #53 vocabulary diversity (context)
- #38 section scaffolding / list uniformity
- #39 machine-cleanliness / perfect grammar

## Associated hypotheses
- H1 calibrated register-distance score
- H2 comparison engine

## Questions / follow-up
- Which vendor-explainer terms should be replaced by academic stylometry terminology?
