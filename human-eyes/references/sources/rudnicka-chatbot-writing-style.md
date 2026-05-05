# Karolina Rudnicka: Each AI chatbot has its own distinctive writing style
## Metadata
- **URL:** https://www.scientificamerican.com/article/chatgpt-and-gemini-ai-have-uniquely-different-writing-styles/
- **Author / owner:** Karolina Rudnicka
- **Published:** 2025-07-09
- **Extracted:** 2026-05-05
- **Source type:** Science journalism
- **Evidence tier:** Journalism / reported cases
- **Extraction status:** second-pass reviewed from Scientific American article page/search excerpt

## Summary
Scientific American article by linguist Karolina Rudnicka arguing that different LLM tools can have distinct idiolect-like writing styles. The article compares ChatGPT and Gemini outputs on diabetes texts and discusses lexical, grammatical, and syntactic habits.

## Main insights
- Supports model-specific style variation rather than a single universal AI voice.
- Reported examples contrast ChatGPT's more formal/clinical phrasing, such as "blood glucose levels", with Gemini's more conversational phrasing, such as "high blood sugar".
- The article says LLM idiolects may change across updates or new versions, which matters for stale rules.

## Evidence and claims to extract
- Method described in article: authorship-style comparison using Delta method and frequent word/trigram differences in ChatGPT and Gemini diabetes texts.
- Reported distance examples from excerpt: ChatGPT sample closer to ChatGPT dataset than Gemini; Gemini sample closer to Gemini dataset than ChatGPT.
- Named style contrast: ChatGPT favors formal medical language while Gemini favors simpler accessible phrasing in the diabetes dataset.

## Skill-use audit
- **Good use:** Back model-drift/model-specific-source notes and warnings against overfitting to one model's style.
- **Misuse / overclaim:** Do not use this as support for #46 bland critical template without direct mapping; the reviewed evidence is about model idiolects.
- **Weakly backed by this source:** Universal AI vocabulary claims.
- **Underused evidence:** Model-specific idiolect should be metadata on examples, especially when a source compares named tools in one topic domain.
- **Patterns left on the table:** Add "model-specific wording preference" as a metadata dimension on examples.

## Matched patterns / rules
- #46 bland critical template (not directly backed by reviewed article)
- model drift context
- model-specific idiolect context

## Associated hypotheses
- H1 calibrated register-distance score
- H12 genre-aware threshold calibration

## Questions / follow-up
- Should model/version be recorded next to examples where the source is model-specific?
- Should "glucose" versus "sugar" style contrasts remain illustrative only because the dataset is medical-topic specific?
