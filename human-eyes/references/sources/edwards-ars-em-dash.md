# Benj Edwards: OpenAI suppressing em dashes
## Metadata
- **URL:** https://arstechnica.com/ai/2025/11/forget-agi-sam-altman-celebrates-chatgpt-finally-following-em-dash-formatting-rules/
- **Author / owner:** Benj Edwards
- **Published:** 2025-11-14
- **Extracted:** 2026-05-05
- **Source type:** Technology journalism
- **Evidence tier:** Journalism / reported cases
- **Extraction status:** second-pass reviewed from Ars Technica article

## Summary
Reports Sam Altman's November 2025 claim that ChatGPT had started following custom instructions to avoid em dashes. The article frames this as evidence of the public salience of em dashes as an AI tell and of ongoing instruction-following/model-behaviour changes.

## Main insights
- Em-dash behaviour is not stable: provider changes and custom instructions can alter it.
- The article itself notes that humans can overuse em dashes too.
- This supports model-drift notes for #49 more than it supports a detection rule.

## Evidence and claims to extract
- Reported Altman claim: if users tell ChatGPT not to use em dashes in custom instructions, it finally follows the instruction.
- Article context: em dashes are widely perceived as AI-generated text tells, but human writers also use them.
- Limitation: this is secondary reporting of a social post, not a controlled measurement of em-dash frequency.

## Skill-use audit
- **Good use:** Back model-drift and custom-instruction sensitivity for #49.
- **Misuse / overclaim:** Do not cite this as primary first-party OpenAI documentation or as proof that GPT-5.1 suppresses em dashes by default.
- **Unsupported use:** Any claim that em dashes are obsolete as a cue across all models.
- **Underused evidence:** The key value is drift: once users and providers know a tell, prompting and model updates can erase it.
- **Patterns left on the table:** Add "instruction-following can erase a known tell" to source notes.

## Matched patterns / rules
- #49 em dashes
- model drift context

## Associated hypotheses
- H7 five-check gating plus advisory catalogue
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should this become the backing source for the em-dash suppression note instead of the unsupported first-party OpenAI card?
