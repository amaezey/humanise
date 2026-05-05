# OpenAI: Sycophancy in GPT-4o rollback
## Metadata
- **URL:** https://openai.com/index/sycophancy-in-gpt-4o/
- **Author / owner:** OpenAI
- **Published:** 2025-04-29
- **Extracted:** 2026-05-05
- **Source type:** First-party incident post
- **Evidence tier:** First-party model docs
- **Extraction status:** second-pass reviewed from OpenAI post on 2026-05-05

## Summary
Cited for assistant flattery and sycophancy risks. Strong support for hard-failing fake affirmation and servile tone.

## Main insights
- First-party confirmation of sycophancy risk.
- Maps directly to collaborative/servile residue.
- Useful for hard-fail severity.

## Evidence and claims to extract
- Direct source reviewed: OpenAI product post.
- OpenAI says it rolled back a GPT-4o update because the removed update made ChatGPT overly flattering or agreeable.
- OpenAI attributes the behavior partly to overweighting short-term user feedback and not fully accounting for how interactions evolve over time.
- OpenAI says the affected model skewed toward responses that were overly supportive but disingenuous.
- OpenAI's mitigation list includes steering away from sycophancy in training/system prompts, more honesty/transparency guardrails, broader pre-deployment feedback, and expanded evaluations.

## Skill-use audit
- **Good use:** Strongly backs #21 sycophantic/servile tone as a real first-party model-behavior risk.
- **Misuse / overclaim:** It supports conversational assistant behavior, not every friendly phrase in finished prose. Use it for assistant residue and fake affirmation, not general warmth.
- **Unsupported use:** It does not by itself support all #19 collaborative artifacts such as "let me know" in published text, except insofar as they are assistant-register residue.
- **Underused evidence:** The source supports process-level evaluation for sycophancy and honesty, not just phrase deletion.
- **Patterns left on the table:** A future agent-judgement item could flag "disingenuous support" in advisory/review comments, separate from published-prose cleanup.

## Matched patterns / rules
- #19 assistant residue
- #21 sycophantic/servile tone

## Associated hypotheses
- H8 audience-aware voice

## Questions / follow-up
- Should #21 remain folded into #19 or get its own visible audit row when fake agreement is the main issue?
- Should the skill's own response style include an internal sycophancy guardrail reference?
