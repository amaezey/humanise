# Przystalski et al.: Stylometry recognizes human and LLM-generated texts
## Metadata
- **URL:** https://arxiv.org/abs/2507.00838
- **Author / owner:** Karol Przystalski, Jan K. Argasiński, Iwona Grabska-Gradzińska, and Jeremi K. Ochab
- **Published:** 2025-07-01 submitted; revised 2025-07-15; journal reference Expert Systems with Applications 296 (2026)
- **Extracted:** 2026-05-05
- **Source type:** Academic preprint / accepted journal article
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Stylometry study distinguishing human-written and LLM-generated short Wikipedia-style samples. It builds a benchmark of human term summaries, pure LLM outputs, summarized outputs, and rephrased outputs, then classifies 10-sentence texts using StyloMetrix and n-gram stylometric features.

## Main insights
- Supports calibrated feature comparison in a well-defined text type, not broad authorship verdicts.
- Feature families include lexical, grammatical, syntactic, and punctuation patterns.
- The abstract names individual overused words and greater grammatical standardisation of LLMs relative to human texts, which aligns with vocabulary and regularity checks.

## Evidence and claims to extract
- Dataset: Wikipedia-based benchmark with human summaries; LLM outputs from GPT-3.5/4, LLaMa 2/3, Orca, and Falcon; outputs processed through T5, BART, Gensim, and Sumy summarizers; and rephrasing via Dipper and T5.
- Classifiers/features: decision trees and LightGBM over StyloMetrix and n-gram features.
- Reported results: up to .87 Matthews correlation coefficient in a seven-class multiclass scenario; binary accuracy between .79 and 1.0; Wikipedia versus GPT-4 up to .98 accuracy on a balanced dataset.
- Explanations: encyclopaedic text-type features, overused words, and greater grammatical standardisation.

## Skill-use audit
- **Good use:** Back H1/H2 comparison framing and #52/#53 as stylometric feature families.
- **Misuse / overclaim:** Do not cite this as evidence for general web prose, fiction, email, or student essays; the abstract's strong claim is limited to a well-defined text type.
- **Unsupported use:** Specific regex-level rules unless the full feature table is extracted.
- **Underused evidence:** The paper's Wikipedia-like reference baseline argues for genre-specific comparison baselines instead of universal prose thresholds.
- **Patterns left on the table:** Grammatical standardisation may deserve its own structural pattern rather than being split between #52 and #53.

## Matched patterns / rules
- #52 sentence rhythm variance
- #53 vocabulary diversity
- #7 AI vocabulary words and phrases (overused-word context)
- grammatical standardisation / structural regularity

## Associated hypotheses
- H1 calibrated register-distance score
- H2 comparison-engine product reframe

## Questions / follow-up
- Which StyloMetrix features are interpretable enough to map into human-eyes guidance?
- Should Wikipedia-like reference prose have a separate baseline from general expository prose?
