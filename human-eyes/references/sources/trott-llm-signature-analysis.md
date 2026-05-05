# Sean Trott: LLM signature analysis
## Metadata
- **URL:** https://seantrott.substack.com/p/identifying-signatures-of-llm-generated
- **Author / owner:** Sean Trott
- **Published:** 2025-04-18
- **Extracted:** 2026-05-05
- **Source type:** Practitioner/research commentary
- **Evidence tier:** Practitioner / teacher / editor essays
- **Extraction status:** second-pass direct-source review

## Summary
Trott reports an empirical analysis of "signatures" that distinguish a small set of human student argumentative essays from ChatGPT-3 and ChatGPT-4 essays. He tests whether open-source Pythia models can expose differences in predictability and representation structure, then uses those features in classifiers. The post is useful for skill development because it argues for interpretable signals, but also explicitly warns against treating detector accuracy on a limited sample as permission to automate authorship judgments.

## Main insights
- Predictability features are the cleanest signal in the post: human essays in the sample used less predictable words than ChatGPT-3 or ChatGPT-4 essays.
- The post treats LLM-written text as potentially more homogenized and lower-variance, but it frames that as a hypothesis requiring broader evidence.
- Trott uses open-source Pythia models to score text rather than relying only on surface word lists.
- Random forest classifiers using Pythia-derived features perform well on the constrained dataset, including strong accuracy from average surprisal alone and higher accuracy from feature combinations.
- The author emphasizes limits: small sample, constrained genre, limited models, uncertain generalization, and real false-positive risk.

## Evidence and claims to extract
- Post title: "Identifying signatures of LLM-generated text."
- Dataset: high school student argumentative essays compared with essays produced by ChatGPT-3 and ChatGPT-4 on related topics.
- Methods include open-source Pythia models, average surprisal, variability in predictability, intrinsic dimensionality, and random forest classifiers.
- Reported classifier result: average surprisal alone was enough for strong classification in the constrained setup; feature combinations improved accuracy further.
- Core caution: even high accuracy in this dataset does not justify automated text-detection decisions because the sample is narrow and false positives are harmful.
- Source origin in this repo: `README.md` lists Sean Trott's Substack for LLM signature analysis; `dev/research/vollmer.md` cites "Sean Trott. UC San Diego, seantrott.substack.com" for LLM signature analysis.

## Skill-use audit
- **Good use:** Support a calibrated, evidence-aware "predictability / homogenization" research note and a warning against binary detector claims.
- **Misuse / overclaim:** Do not convert the reported classifier accuracy into a general-purpose detector promise; the author explicitly disallows that leap.
- **Unsupported use:** Surface tells such as punctuation, AI vocabulary, or generic prose texture are not the point of the analysis.
- **Underused evidence:** Trott is useful as a methodological caution: even model-derived features need genre, model-version, sample-size, and false-positive caveats.
- **Patterns left on the table:** Feature-level signals around surprisal variance, intrinsic dimensionality, genre constraints, and model/version drift.

## Matched patterns / rules
- Model drift / signature context
- Predictability / homogenization research note
- Detector-bias and false-positive caution
- Genre-constrained calibration

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should human-eyes add an explicit "predictability variance" reference note separate from surface phrase tells?
- Can this source be used as a caution label wherever a rule sounds detector-like?
- What equivalent low-cost proxy can the skill use without running model-surprisal analysis?
