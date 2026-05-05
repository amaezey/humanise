# Sun et al.: Idiosyncrasies in Large Language Models
## Metadata
- **URL:** https://arxiv.org/abs/2502.12150v2
- **Author / owner:** Mingjie Sun, Yida Yin, Zhiqiu Xu, J. Zico Kolter, and Zhuang Liu
- **Published:** 2025-02-17 submitted; revised 2025-06-16; published at ICML 2025
- **Extracted:** 2026-05-05
- **Source type:** Academic paper
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Studies model-specific idiosyncrasies: output patterns that can distinguish which LLM produced text. The abstract reports 97.1% held-out validation accuracy on a five-way classification problem across ChatGPT, Claude, Grok, Gemini, and DeepSeek, and says the idiosyncrasies are rooted in word-level distributions.

## Main insights
- This source supports model-specific fingerprints, not a universal AI-writing signature.
- The reported patterns persist after rewriting, translation, or summarization by another LLM, suggesting fingerprints can survive surface edits.
- The source is useful for explaining why a single static pattern set will drift across model families and post-processing pipelines.

## Evidence and claims to extract
- Task: given a text output, predict the source LLM.
- Model set named in abstract: ChatGPT, Claude, Grok, Gemini, and DeepSeek.
- Result named in abstract: 97.1% held-out validation accuracy in the five-way classification task.
- Mechanism named in abstract: idiosyncrasies rooted in word-level distributions, with semantic persistence under rewriting/translation/summarization.

## Skill-use audit
- **Good use:** Cite as model-specific drift/fingerprint context and as support for comparing signals by source model or source family where possible.
- **Misuse / overclaim:** Do not use this as evidence that #1 significance inflation or any one word is a universal AI tell; the reviewed abstract does not name "significant".
- **Weakly backed by this source:** Human-readable regex-level rules. The abstract's strongest evidence is embedding-model classification and aggregate word-level distributions.
- **Underused evidence:** The model-family distinction should be represented in source metadata so rules can say whether they are generic AI residue or model-specific fingerprints.
- **Patterns left on the table:** Future metadata could distinguish "AI vs human" checks from "which model family" checks.

## Matched patterns / rules
- #7 AI vocabulary words and phrases (model-specific distribution context)
- model/version drift context

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Does the full paper provide named model-specific word lists that should be tracked as examples rather than general rules?
- Should human-eyes record whether a pattern is meant to catch generic AI residue or model-family residue?
