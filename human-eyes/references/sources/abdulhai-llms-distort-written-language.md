# Abdulhai et al.: How LLMs Distort Our Written Language
## Metadata
- **URL:** https://arxiv.org/abs/2603.18161
- **Author / owner:** Marwa Abdulhai, Isadora White, Yanming Wan, Ibrahim Qureshi, Joel Leibo, Max Kleiman-Weiner, and Natasha Jaques
- **Published:** 2026-03-18 submitted
- **Extracted:** 2026-05-05
- **Source type:** Academic preprint
- **Evidence tier:** Peer-reviewed / academic empirical (preprint)
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Studies how LLM assistance changes human writing. The abstract reports that LLMs alter voice, tone, and intended meaning, and that extensive LLM use produced a nearly 70% increase in essays that stayed neutral on the topic question.

## Main insights
- Strong support for stance-preservation and semantic-preservation checks in Rewrite/Write workflows.
- Heavy LLM users reported their writing was less creative and less in their own voice.
- The reviewed abstract also links LLM-generated scientific peer reviews with less weight on clarity and significance and scores about one point higher on average.

## Evidence and claims to extract
- Evidence types in abstract: human user study; pre-LLM 2021 human-written essay dataset with expert feedback; wild LLM-generated scientific peer reviews.
- Concrete findings in abstract: nearly 70% increase in neutral essays under extensive LLM use; grammar-edit prompts still significantly alter semantic meaning; LLM-generated peer reviews in the cited setting were 21% of reviews and scored about one point higher on average.
- Limitation for pattern mapping: the abstract supports meaning/voice/stance drift more directly than any specific surface regex.

## Skill-use audit
- **Good use:** Back agent-judgement checks about neutrality collapse, voice loss, semantic drift, and review-score inflation.
- **Misuse / overclaim:** Do not cite this as direct evidence for pronoun depletion unless the full paper is extracted and confirms it.
- **Weakly backed by this source:** Surface punctuation, vocabulary, or sentence-shape checks.
- **Underused evidence:** This belongs in rewrite safety as much as detection: even grammar-edit prompts can change meaning, stance, and voice.
- **Patterns left on the table:** Add a rewrite-specific "meaning changed despite grammar-only request" follow-up check.

## Matched patterns / rules
- #37 neutrality collapse
- #35 tonal uniformity / register lock
- Rewrite semantic-preservation process
- peer-review judgement calibration

## Associated hypotheses
- H8 audience-aware voice
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should human-eyes expose semantic drift as a first-class rewrite risk separate from AI-writing detection?
- Does the full paper support a measurable stance-change feature, or should this remain agent judgement?
