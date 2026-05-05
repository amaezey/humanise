# OpenAI: GPT-4 System Card
## Metadata
- **URL:** https://cdn.openai.com/papers/gpt-4-system-card.pdf
- **Author / owner:** OpenAI
- **Published:** 2023 context; PDF source reviewed 2026-05-05
- **Extracted:** 2026-05-05
- **Source type:** First-party model documentation
- **Evidence tier:** First-party model docs
- **Extraction status:** second-pass reviewed from OpenAI-hosted PDF excerpt/search result

## Summary
First-party system card for GPT-4 describing training/deployment context, safety mitigations, red-teaming, and behavioral limitations. The reviewed excerpt says GPT models are first trained to predict the next word from internet-scale text and then fine-tuned with reinforcement learning from human feedback to produce outputs preferred by human labelers.

## Main insights
- Useful as first-party background on next-token training, RLHF, mitigations, and sycophancy as a known tendency.
- Not a direct prose-pattern source for human-eyes unless a specific behavior is mapped from the system card text.
- The excerpt explicitly notes model behavior changes between early and launch versions due to mitigations, supporting model/version drift caution.

## Evidence and claims to extract
- Training stages in reviewed excerpt: internet-scale next-word prediction followed by RLHF fine-tuning.
- Deployment context: evaluates GPT-4 and distinguishes an early instruction-following model from a launch model with additional helpfulness/harmlessness mitigations.
- Behavioral limitation noted in excerpt: sycophancy, described as repeating back a dialogue user's preferred answer, can worsen with scale.

## Skill-use audit
- **Good use:** Back model-behavior/process context, RLHF context, versioned behavior, and sycophancy background.
- **Misuse / overclaim:** Do not use this as evidence for visible prose patterns like vocabulary, punctuation, or sentence rhythm.
- **Weakly backed by this source:** Any current regex or checklist pattern.
- **Underused evidence:** The early-versus-launch model distinction should be used in model-drift notes so pattern confidence is not treated as timeless.
- **Patterns left on the table:** None as direct prose-pattern evidence; first-party system cards are model-context evidence, separate from empirical prose-corpus evidence.

## Matched patterns / rules
- Assistant behavior context; no direct check currently.
- #21 sycophancy / over-agreement context
- model-version behavior context

## Associated hypotheses
- H3 drop detection framing

## Questions / follow-up
- Should first-party model docs live in a separate "model behavior context" evidence tier?
