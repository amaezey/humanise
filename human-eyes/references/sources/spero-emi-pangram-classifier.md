# Spero and Emi: Pangram AI-generated text classifier technical report
## Metadata
- **URL:** https://arxiv.org/abs/2402.14873
- **Author / owner:** Bradley Emi and Max Spero
- **Published:** 2024-02-21 submitted; revised 2024-07-29
- **Extracted:** 2026-05-05
- **Source type:** Classifier technical report
- **Evidence tier:** Vendor / detector pages
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Technical report for Pangram Text, a transformer-based neural network trained to distinguish LLM-written text from human-written text. This card duplicates `pangram-classifier.md` at the source level because the README listed Pangram and Spero/Emi separately.

## Main insights
- The source is most useful for detector-landscape, domain-coverage, and false-positive design context.
- It should not be used as evidence for user-visible prose patterns unless the full report yields interpretable features.
- Its domain list can help evaluate whether human-eyes examples cover enough registers.

## Evidence and claims to extract
- Benchmark: 10 text domains and eight open-/closed-source LLMs.
- Domains named in abstract: student writing, creative writing, scientific writing, books, encyclopedias, news, email, scientific papers, and short-form Q&A.
- Reported classifier claims: over 38 times lower error rates than DetectGPT and leading commercial tools; hard negative mining with synthetic mirrors; lower false-positive rates; no nonnative-speaker bias; generalization to unseen domains/models.

## Skill-use audit
- **Good use:** Back H3 detector-framing caution and H4 audit-contract thinking.
- **Misuse / overclaim:** Do not translate Pangram classifier performance into confidence for human-eyes manual rules.
- **Unsupported use:** Any specific pattern in the current catalogue.
- **Underused evidence:** The domain list and synthetic-mirror method are more useful for test-fixture design than for end-user pattern claims.
- **Patterns left on the table:** The synthetic mirror method may inspire test-fixture design, not end-user pattern claims.

## Matched patterns / rules
- Audit contract and transparent evidence design; no direct prose pattern yet.
- detector calibration context

## Associated hypotheses
- H3 drop detection framing
- H4 single-source registry plus JSON audit-format contract

## Questions / follow-up
- Should one Pangram card be canonical and the duplicate become an alias?
