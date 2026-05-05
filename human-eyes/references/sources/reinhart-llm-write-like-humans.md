# Reinhart et al.: Do LLMs write like humans?
## Metadata
- **URL:** https://pnas.org/doi/10.1073/pnas.2422455122
- **Author / owner:** Alex Reinhart, Ben Markey, Michael Laudenbach, Kachatad Pantusen, Ronald Yurko, Gordon Weinberg, and David West Brown
- **Published:** 2025-02-18 online; PNAS issue 2025-02-25
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from PMC open-access full text on 2026-05-05

## Summary
Examines grammatical and rhetorical variation in LLM writing. The repo uses it for vocabulary, rhetorical-style, and model-drift context.

## Main insights
- Supports drift-aware pattern maintenance.
- Useful for grammar/rhetoric changes rather than one-off phrase bans.
- Needs mapping to exact checks before stronger claims.

## Evidence and claims to extract
- Direct source reviewed: PMC open-access copy of the PNAS article.
- Study setup: parallel human and LLM corpora using GPT-4o, GPT-4o Mini, and Llama 3 variants prompted from human text chunks across multiple genres/registers.
- Main claim: instruction-tuned models have a distinct noun-heavy, informationally dense style and struggle to match human stylistic variation.
- Quantified example: GPT-4o overused present participial clauses, "that" clauses as subjects, nominalizations, and phrasal coordination relative to humans.
- The paper's features are linguistic/rhetorical variables, not surface phrase lists.

## Skill-use audit
- **Good use:** Strongly backs H1 and H12, plus the general need for register-aware structural/rhetorical features.
- **Misuse / overclaim:** It should not be cited mainly as vocabulary evidence. Its stronger contribution is grammatical/rhetorical style variation and genre mismatch.
- **Weakly backed by this source:** The direct source does not specifically validate current regex phrases for #3 or #7 without additional mapping.
- **Underused evidence:** Present participial clauses directly support revisiting #3 superficial -ing analyses, but the source frames them as part of an informationally dense style, not simply vague analysis.
- **Patterns left on the table:** Nominalization density, noun-heavy style, "that" subject clauses, and phrasal coordination could become future structural/rhetorical features.

## Matched patterns / rules
- #3 superficial -ing analyses
- #52 sentence rhythm variance / structural style context
- Future nominalization and noun-heavy-style checks
- model drift context

## Associated hypotheses
- H1 calibrated register-distance score
- H7 five-check gating plus advisory catalogue
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should #3 be narrowed from generic -ing phrases to present-participial-clause overuse with context?
- Are Biber-style features feasible in the deterministic grader?
