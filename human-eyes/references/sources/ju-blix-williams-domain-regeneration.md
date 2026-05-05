# Ju, Blix, and Williams: Domain Regeneration
## Metadata
- **URL:** https://aclanthology.org/2025.findings-acl.120/
- **Author / owner:** Da Ju, Hagen Blix, and Adina Williams
- **Published:** 2025-07
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from ACL Anthology abstract

## Summary
Studies how well an open-source LLM can regenerate the syntactic distributions of Wikipedia and news text in a semantically controlled setting. The authors compare properties from sentence length and readability through dependency-tag distribution, parse depth, and parse complexity.

## Main insights
- Strong support for register/domain-specific structural calibration.
- The key finding is distributional: regenerated text usually has shifted means, lower standard deviation, and reduced long-tail behavior compared with human originals.
- This backs variance/long-tail checks more directly than any phrase or vocabulary list.

## Evidence and claims to extract
- Domains: Wikipedia and news text from permissively licensed English sources often found in LLM training data.
- Structural levels: sentence length, readability, dependency tag distribution, parse depth, and parse complexity.
- Main abstract finding: most regenerated distributions show shifted means, lower standard deviation, and reduced long tails versus human originals.

## Skill-use audit
- **Good use:** Back #52 sentence-rhythm variance and broader register-aware structural comparison.
- **Misuse / overclaim:** Do not turn this into a generic "AI sentences are shorter/longer" rule without domain-specific direction and measurement.
- **Weakly backed by this source:** Any vocabulary, punctuation, or phrase-level pattern.
- **Underused evidence:** Reduced long-tail behavior is a stronger structural concept than a simple average sentence-length warning.
- **Patterns left on the table:** Reduced long-tail behavior should be represented as its own structural insight, not folded only into sentence rhythm.

## Matched patterns / rules
- #52 sentence rhythm variance
- register-aware structural checks
- long-tail reduction / variance compression

## Associated hypotheses
- H1 calibrated register-distance score
- H2 comparison-engine product reframe
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should human-eyes add a structural "long-tail compression" hypothesis distinct from rhythm variance?
- Which regenerated domain directions from the full paper map cleanly to current rule thresholds?
