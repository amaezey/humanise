# Geng and Trotta: Human-LLM Coevolution
## Metadata
- **URL:** https://aclanthology.org/2025.findings-acl.657/
- **Author / owner:** Mingmeng Geng and Roberto Trotta
- **Published:** 2025-07
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** reviewed from saved full-text ACL Anthology PDF snapshot

## Summary
Analyzes arXiv abstracts and reports coevolution between LLM outputs and academic authors' behavior. The saved full text says several public ChatGPT-overuse tells dropped after public attention, while other favored words kept increasing, and it identifies declining "is" and "are" frequency as a subtle LLM-impact example.

## Main insights
- The source supports time-sensitive vocabulary drift: once a tell becomes public, users may select around it or edit it out.
- It supports continued aggregate word-frequency analysis, but with attention to already-common words and words that decrease because LLMs disfavor them.
- It makes detection harder in real-world settings because humans and LLMs adapt together.

## Evidence and claims to extract
- Corpus described in the abstract: arXiv paper abstracts.
- Direct examples: "delve" drops after being singled out in early 2024; "significant" keeps increasing.
- Copula evidence: the saved full text states that declining "is" and "are" frequency in arXiv abstracts is an example of a subtle and increasing LLM-impact trend.
- Stated implication: human selection and modification of LLM outputs introduces additional challenges for machine-text detection.

## Skill-use audit
- **Good use:** Cite as evidence that academic vocabulary signals are temporally unstable and need extraction dates, source dates, and register-aware baselines.
- **Misuse / overclaim:** Do not treat it as a stable list of bad words. Its central point is that visible tells can decay or mutate.
- **Supported scope:** #8 copula avoidance is supported for arXiv-abstract corpus frequency drift, not as a universal sentence-level rule.
- **Underused evidence:** Public attention can make a tell fade or invert, so each vocabulary source needs corpus date range and extraction date in addition to publication date.
- **Patterns left on the table:** Add a rule-note concept for "publicly known tells may invert or fade"; use it to prevent stale blacklist behavior.

## Matched patterns / rules
- #7 AI vocabulary words and phrases
- academic-register context
- detector limitation / model-drift context
- #8 copula avoidance in arXiv-abstract corpus frequency drift

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should rule evidence store the date range of the corpus, not just source publication date?
- Does the full paper list disfavored words that matter for negative evidence or baseline shifts?
