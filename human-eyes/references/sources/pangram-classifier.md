# Pangram AI content detector
## Metadata
- **URL:** https://arxiv.org/abs/2402.14873
- **Author / owner:** Bradley Emi and Max Spero
- **Published:** 2024-02-21 submitted; revised 2024-07-29
- **Extracted:** 2026-05-05
- **Source type:** Vendor classifier technical report
- **Evidence tier:** Vendor / detector pages
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Technical report for Pangram Text, a transformer-based classifier trained to distinguish LLM-written text from human-written text. The abstract reports evaluation across 10 domains and eight open- and closed-source models.

## Main insights
- Useful for detector-landscape and calibration context, not direct human-eyes prose pattern evidence.
- The benchmark domains named in the abstract overlap many human-eyes registers: student writing, creative writing, scientific writing, books, encyclopedias, news, email, scientific papers, and short-form Q&A.
- The report's false-positive and nonnative-speaker claims are relevant to user-facing caution, but human-eyes should avoid becoming a detector.

## Evidence and claims to extract
- Reported classifier claim: Pangram Text outperforms DetectGPT and leading commercial AI detection tools with over 38 times lower error rates on the benchmark.
- Training method named in abstract: hard negative mining with synthetic mirrors.
- Claims: orders-of-magnitude lower false positive rates on high-data domains such as reviews; not biased against nonnative English speakers; generalizes to unseen domains and models.

## Skill-use audit
- **Good use:** Back H3/H4 architecture cautions around calibration, domain coverage, and false-positive handling.
- **Misuse / overclaim:** Do not cite this for any specific visible prose tell; it is classifier documentation, not a rule-source list.
- **Unsupported use:** Manual pattern checks, unless the full report exposes interpretable features.
- **Underused evidence:** Domain coverage and false-positive framing can guide evaluation design, but the classifier-performance claim should stay separate from human-eyes rule severity.
- **Patterns left on the table:** Domain coverage should inform source-card metadata and benchmark planning, not the pattern inventory directly.

## Matched patterns / rules
- Audit architecture context; no direct prose pattern.
- detector limitation / calibration context

## Associated hypotheses
- H3 drop detection framing
- H4 JSON audit contract

## Questions / follow-up
- Should this card be merged with `spero-emi-pangram-classifier.md`, or kept as a duplicate because README names both Pangram and Spero/Emi?
