# Kousha and Thelwall: How much are LLMs changing academic papers after ChatGPT?
## Metadata
- **URL:** https://arxiv.org/abs/2509.09596
- **Author / owner:** Kayvan Kousha and Mike Thelwall
- **Published:** 2025-09-11 submitted; revised 2026-03-11
- **Extracted:** 2026-05-05
- **Source type:** Academic preprint; later version of record in Scientometrics
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Large-scale academic-language drift study tracking 12 LLM-associated terms across Scopus, Web of Science, PubMed, PubMed Central, Dimensions, and OpenAlex from 2015 to 2024, plus full-text analysis of more than 2.4 million PMC open-access papers from 2021 through July 2025.

## Main insights
- Strong aggregate evidence that specific LLM-associated terms rose sharply in academic publishing after ChatGPT.
- The biggest reported 2022-2024 increases in the abstract are "delve", "underscore", and "intricate"; full-text repeated-use increases are especially large for "underscore", "intricate", and "meticulous".
- Co-occurrence matters: papers using one LLM-associated term became much more likely to use other terms, which supports signal stacking over single-word hits.
- The authors frame LLM support for scholarly publishing as potentially reducing language barriers for non-English speakers, so the source should not be used punitively.

## Evidence and claims to extract
- Abstract metrics: "delve" +1,500%, "underscore" +1,000%, "intricate" +700% from 2022 to 2024 across databases.
- PMC full-text repeated-use metric: papers using "underscore" six or more times increased by over 10,000% from 2022 to 2025; "intricate" +5,400%; "meticulous" +2,800%.
- Co-occurrence metric: in 2024, "underscore" correlated with "pivotal" at 0.449 and "delve" at 0.311, compared with much weaker 2022 associations.

## Skill-use audit
- **Good use:** Strong backing for academic-register #7 vocabulary drift and for co-occurrence/signal-stacking logic.
- **Misuse / overclaim:** Do not generalize the exact term frequencies to fiction, email, web copy, or non-academic prose.
- **Weakly backed by this source:** Per-document authorship classification; the abstract reports aggregate database and full-text shifts.
- **Underused evidence:** Repeated-use and co-occurrence metrics are stronger than single-token hits and should inform scoring or examples.
- **Patterns left on the table:** #7 should preserve co-occurrence evidence, repeated-use evidence, and field/register specificity rather than flattening to a word list.

## Matched patterns / rules
- #7 AI vocabulary words and phrases
- overall signal stacking / co-occurrence
- academic-register context

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Does the full paper's 12-term list align with the current #7 vocabulary inventory?
- Should the skill treat repeated use of a term differently from a single occurrence in academic prose?
