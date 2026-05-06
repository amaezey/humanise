# Geng and Trotta: Is ChatGPT Transforming Academics' Writing Style?
## Metadata
- **URL:** https://arxiv.org/abs/2404.08627
- **Author / owner:** Mingmeng Geng and Roberto Trotta
- **Published:** Submitted 2024-04-12; revised 2024-11-08
- **Extracted:** 2026-05-05
- **Source type:** Academic preprint
- **Evidence tier:** Peer-reviewed / academic empirical (preprint)
- **Extraction status:** reviewed from saved full-text arXiv PDF snapshot on 2026-05-05

## Summary
Academic writing-style transformation paper using arXiv abstracts. The saved full text supports an adaptive word-frequency model and explicitly reports decreased "is" and "are" frequency after ChatGPT.

## Main insights
- Supports the idea that LLM use changes academic abstract style.
- Best used in academic-register notes.
- The saved full text supports copula-frequency decline in arXiv abstracts; keep the claim corpus-scoped.

## Evidence and claims to extract
- Direct source reviewed: arXiv abstract page.
- Corpus: one million arXiv papers submitted from May 2018 to January 2024.
- Method: statistical analysis of word-frequency changes in abstracts, calibrated and validated on mixed real and ChatGPT-modified abstracts.
- Main abstract-level claim: LLM-style abstracts are increasingly visible in arXiv abstracts, especially computer science; with a GPT-3.5 "revise the following sentences" baseline, the estimated fraction is approximately 35%.
- Full-text verification: the PDF reports that "is" and "are" decrease after ChatGPT, with table values showing more than 10% drops in the analysed arXiv-abstract corpus.

## Skill-use audit
- **Good use:** Backs academic-register style shift, H12 calibration work, and #8 as a corpus-level word-frequency decrease.
- **Misuse / overclaim:** Do not turn the corpus-level "is/are" decrease into a universal ban on copulas.
- **Underused evidence:** Stronger fit for register-specific density calibration than for a single grammar rule.
- **Patterns left on the table:** Adaptive word-frequency decreases as well as increases may matter for future register-distance scoring.

## Matched patterns / rules
- #7 AI vocabulary words and phrases
- Academic-register style shift
- #8 copula avoidance in arXiv-abstract corpus frequency drift

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Where exactly does the repo's "10%+ decline in is/are" claim come from?
- Should #8 cite a different source if the full text does not support it?
