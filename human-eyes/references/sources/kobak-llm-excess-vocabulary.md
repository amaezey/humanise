# Kobak et al.: Delving into LLM-assisted writing in biomedical publications through excess vocabulary
## Metadata
- **URL:** https://www.science.org/doi/10.1126/sciadv.adt3813
- **Author / owner:** Dmitry Kobak, Rita Gonzalez-Marquez, Emoke-Agnes Horvat, and Jan Lause
- **Published:** 2025-07-02 online; Science Advances 11(27), 2025-07-04
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from PMC open-access full text on 2026-05-05

## Summary
Analyzes biomedical publications for excess vocabulary associated with LLM-assisted writing and provides the dataset bundled in human-eyes. The source supports corpus-level lexical signals, not single-word authorship claims.

## Main insights
- Use excess vocabulary as density evidence.
- Keep register scope explicit: biomedical/scientific prose.
- The bundled CSV should remain reference data, not a standalone verdict.

## Evidence and claims to extract
- Direct source reviewed: PMC open-access copy of Science Advances article.
- Corpus: 15.1 million English PubMed abstracts from 2010-2024 after filtering.
- Method: excess-word analysis compares post-ChatGPT word-frequency jumps against pre-LLM baselines rather than using a ground-truth human/LLM classifier.
- Main quantified claim: at least 13.5% of 2024 biomedical abstracts were likely processed with LLMs; some subcorpora reached around 40%.
- Limit: the paper is about biomedical abstracts and style-word frequency shifts. It does not say a single word or phrase proves AI authorship in arbitrary prose.

## Skill-use audit
- **Good use:** Strongly backs #7 and `overall-signal-stacking` when human-eyes treats vocabulary as corpus/register evidence and a density signal.
- **Misuse / overclaim:** Using the Kobak word list as a per-document detector or hard failure would misuse the paper. The paper's logic is aggregate excess vocabulary, not one-token accusation.
- **Unsupported use:** It does not directly support non-academic prose, fiction, marketing copy, em dashes, assistant residue, or structural tells.
- **Underused evidence:** The source supports H1 and H12 more strongly than the current first-pass note implied: it is a model for register-specific baseline comparison.
- **Patterns left on the table:** A future "biomedical/academic register" branch could expose corpus-normalized excess-word density separately from the generic AI vocabulary rule.

## Matched patterns / rules
- #7 AI vocabulary words and phrases
- overall-signal-stacking
- kobak-excess-words.csv

## Associated hypotheses
- H1 calibrated register-distance score
- H7 five-check gating plus advisory catalogue
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should `kobak-excess-words.csv` stay advisory-only outside academic/scientific prose?
- Should the audit name the register limit when Kobak terms drive signal stacking?
