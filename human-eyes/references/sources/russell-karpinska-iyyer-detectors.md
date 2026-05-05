# Russell, Karpinska, and Iyyer: Frequent ChatGPT users as detectors
## Metadata
- **URL:** https://aclanthology.org/2025.acl-long.267/
- **Author / owner:** Jenna Russell, Marzena Karpinska, and Mohit Iyyer
- **Published:** 2025-07
- **Extracted:** 2026-05-05
- **Source type:** Academic empirical research
- **Evidence tier:** Peer-reviewed / academic empirical
- **Extraction status:** second-pass reviewed from ACL Anthology page on 2026-05-05

## Summary
Cited for user ability to identify AI-generated text and for several Wikipedia-backed pattern families. It is useful context but must be separated from prose-rule evidence.

## Main insights
- Detection ability is not the same as a safe product verdict.
- Some cues may eventually support contrast, triad, or heading-style rules, but only if the full paper's qualitative coding names those cues directly.
- Use to frame uncertainty and user review.

## Evidence and claims to extract
- Direct source reviewed: ACL Anthology metadata and abstract.
- Study setup: annotators read 300 non-fiction English articles, label each as human-written or AI-generated, and provide paragraph-length explanations.
- Main quantified finding from abstract: majority vote among five frequent-LLM-writing users misclassified only 1 of 300 articles.
- The abstract says expert annotators relied heavily on AI vocabulary but also on harder-to-automate qualities such as formality, originality, and clarity.
- Limit: the paper studies human detection of generated non-fiction articles; it does not directly validate human-eyes severity tiers.

## Skill-use audit
- **Good use:** Supports the idea that experienced humans use lexical and higher-level style cues together.
- **Misuse / overclaim:** It should not be used to make human-eyes a detector or to imply ordinary users can reliably classify authorship. Its strong result is for selected frequent users and a specific corpus.
- **Weakly backed by this source:** The abstract does not directly back #9, #10, or #15 unless the full paper's qualitative coding names those cues.
- **Underused evidence:** Formality, originality, and clarity may belong in agent-judgement or field-guide disambiguation rather than regex.
- **Current README treatment:** Cited only as selected-user detection context for #9, #10, and #15 until the full qualitative coding is mapped.
- **Patterns left on the table:** "Originality" and "clarity" are not current pattern families; they could become explanatory dimensions in a comparison engine, not standalone failures.

## Matched patterns / rules
- #9 contrived contrast
- #10 rule of three
- #15 title case in headings
- detection-background context

## Associated hypotheses
- H3 drop detection framing
- H7 five-check gating plus advisory catalogue

## Questions / follow-up
- Does the full paper's qualitative coding explicitly identify triads, title case, or contrast structures?
- Should this source be moved from per-pattern evidence into evaluation-method evidence?
