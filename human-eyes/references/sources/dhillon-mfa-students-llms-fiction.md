# Dhillon et al.: MFA students vs LLMs fiction
## Metadata
- **URL:** https://arxiv.org/abs/2510.13939
- **Author / owner:** Tuhin Chakrabarty, Jane C. Ginsburg, and Paramveer Dhillon
- **Published:** 2025-10-15 submitted; revised 2026-03-17
- **Extracted:** 2026-05-05
- **Source type:** Academic preprint
- **Evidence tier:** Peer-reviewed / academic empirical (preprint)
- **Extraction status:** second-pass reviewed from arXiv abstract

## Summary
Preregistered literary-style emulation study comparing MFA-trained expert writers with ChatGPT, Claude, and Gemini writing up to 450-word excerpts in the styles of 50 award-winning authors. The reviewed abstract focuses on reader preferences, style fidelity, detector behavior, and the effect of author-specific fine-tuning.

## Main insights
- Fiction evidence needs a separate path from generic prose rules.
- MFA readers strongly disfavored in-context AI outputs for both fidelity and quality, while general readers showed no fidelity preference and favored AI quality.
- Fine-tuning changed the result: both MFA and general readers preferred fine-tuned AI outputs, and detectors rarely flagged those outputs as AI-generated.
- This is evidence that surface detectability and perceived literary quality can diverge sharply.

## Evidence and claims to extract
- Study design: blind pairwise evaluations by 28 MFA-trained readers and 516 college-educated general readers.
- In-context AI results: MFA readers disfavored AI for stylistic fidelity (OR=0.16) and quality (OR=0.13); general readers had no fidelity preference (OR=1.06) and favored AI for quality (OR=1.82).
- Fine-tuned AI results: MFA readers favored AI for fidelity (OR=8.16) and quality (OR=1.87); general readers favored it more strongly.
- Detector result: fine-tuned outputs were rarely flagged as AI-generated, 3% versus 97% for prompting.

## Skill-use audit
- **Good use:** Back fiction-specific caution about reader expertise, style fidelity, and detector limitations.
- **Misuse / overclaim:** Do not cite the abstract for specific craft tells such as generic metaphors or structural monotony; the reviewed abstract does not list them.
- **Weakly backed by this source:** #30 and #54 need full-text extraction before direct pattern support.
- **Underused evidence:** The fine-tuning result is a strong warning that detector flags and literary-quality judgements can diverge.
- **Patterns left on the table:** A fiction branch should distinguish expert-reader quality/fidelity judgements from detector-like surface tells.

## Matched patterns / rules
- #30 generic/ungrounded metaphors (not directly backed by reviewed abstract)
- #41 genre-specific manual checks: fiction
- #54 structural monotony (not directly backed by reviewed abstract)
- detector limitation / fine-tuning evasion context

## Associated hypotheses
- H12 genre-aware threshold calibration

## Questions / follow-up
- Does the full paper contain qualitative coding of the "AI quirks" that penalized in-context outputs?
- Should human-eyes represent fiction checks as expert-craft review prompts rather than deterministic source claims?
