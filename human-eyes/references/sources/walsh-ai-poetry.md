# Walsh et al.: AI poetry computational analysis
## Metadata
- **URL:** https://arxiv.org/abs/2410.15299
- **Author / owner:** Melanie Walsh, Anna Preus, and Elizabeth Gronski
- **Published:** Submitted 2024-10-20; revised 2024-10-30
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from arXiv abstract on 2026-05-05

## Summary
Compares AI and human poetry corpora. human-eyes uses it for poetry-specific manual checks rather than general prose rules.

## Main insights
- Poetry needs domain-specific watchlists.
- Uniformity, rhyme defaults, and mood clusters should not become global regex checks.
- Good fit for genre_specific agent judgement.

## Evidence and claims to extract
- Direct source reviewed: arXiv abstract page.
- Study setup: 5.7k GPT-generated poems from GPT-3.5 and GPT-4 across 24 poetic forms/styles, about 40 subjects, and 3 prompt templates, compared with 3.7k human poems from the Poetry Foundation and Academy of American Poets.
- Main claim: GPT poetry can satisfy superficial form constraints but is more constrained and uniform than human poetry.
- Named style tendencies: rhyme, quatrains, iambic meter, first-person plural perspectives, and vocabulary such as "heart", "embrace", "echo", and "whisper".
- Limit: poetry-specific evidence should not be generalized to prose.

## Skill-use audit
- **Good use:** Strongly backs poetry branch of #41 and supports genre-specific agent judgement.
- **Misuse / overclaim:** Do not generalize rhyme/quatrain/default meter findings to essays, business prose, or fiction.
- **Weakly backed by this source:** This does not support the general ghost/spectral language rule by itself, though "echo" and "whisper" overlap with #26 in poetry context.
- **Underused evidence:** First-person plural overuse and form-default behavior could be explicit poetry-watchlist items.
- **Patterns left on the table:** Poetry-specific checks for default quatrains, rhyme density, first-person plural clustering, and form-compliance without variation.

## Matched patterns / rules
- #41 genre-specific manual checks: poetry

## Associated hypotheses
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should #41's poetry branch name Walsh's concrete tendencies rather than staying generic?
- Should #26 ghost/spectral language exclude poetry unless the genre-specific branch confirms it is formulaic?
