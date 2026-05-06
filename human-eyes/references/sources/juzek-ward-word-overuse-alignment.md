# Juzek and Ward: Word Overuse and Alignment in Large Language Models
## Metadata
- **URL:** https://arxiv.org/abs/2508.01930
- **Author / owner:** Tom S. Juzek and Zina B. Ward
- **Published:** 2025-08-03 submitted; accepted for BIAS 2025 at ECML PKDD
- **Extracted:** 2026-05-05
- **Source type:** Academic preprint
- **Evidence tier:** Peer-reviewed / academic empirical (preprint)
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Studies whether learning from human feedback contributes to LLM lexical overuse. The abstract says LLMs overuse terms such as "delve" and "intricate", proposes a procedure for detecting potentially LHF-induced lexical preferences, and experimentally emulates the feedback procedure to show that participants systematically prefer variants containing certain words.

## Main insights
- This is mechanism evidence for why some lexical spikes can happen, not per-document evidence that a given prose sample is AI-written.
- The paper frames some overuse as a possible misalignment between what feedback workers prefer and what end users expect.
- It reinforces that alignment and preference optimization can change surface vocabulary, so pattern thresholds need model/version/register context.

## Evidence and claims to extract
- Source examples named in the abstract: "delve" and "intricate".
- Evidence described in the abstract: Meta Llama case study plus an experimental emulation of the LHF procedure where participants prefer text variants containing certain words.
- Limitation for this repo: the abstract does not provide a general-purpose list of words and does not validate any human-facing authorship detector.

## Skill-use audit
- **Good use:** Cite as mechanism context for #7 and for why vocabulary lists drift with alignment and feedback processes.
- **Misuse / overclaim:** Do not cite it as proof that individual occurrences of "delve", "intricate", or similar words are AI evidence.
- **Unsupported use:** Any fixed blacklist, severity score, or claim that all aligned models share the same lexical profile.
- **Underused evidence:** The mechanism distinction matters: separate observed corpus spikes from alignment-induced candidate words and from practitioner phrase-list anecdotes.
- **Patterns left on the table:** A future source-note field for "mechanism class" could distinguish corpus-observed words, alignment-induced candidates, and practitioner anecdotes.

## Matched patterns / rules
- #7 AI vocabulary words and phrases (mechanism context)
- model/version drift context

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Does the full paper name additional LHF-induced lexical preferences worth adding as tentative candidates, or only validate the mechanism?
- Should #7 split "observed corpus spike" from "plausible alignment-induced overuse" in its evidence notes?
