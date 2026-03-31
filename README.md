# humanise

A fork of [blader/humanizer](https://github.com/blader/humanizer) by [@blader](https://github.com/blader), restructured, research-expanded, and tested. The original skill drew from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup). This version adds 7 new pattern categories, triples the vocabulary list, and introduces an eval pipeline for verifying the skill works.

Created by [Billie-Mae Kennedy](https://github.com/amaezey).

## What changed from the original

- Restructured per [Anthropic's skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): split into SKILL.md + reference file for progressive disclosure
- Expanded from 25 to 32 patterns using research from NYT, Substack, and Grammarly
- Added experiential vacancy and density-without-purpose as structural diagnostics
- Tightened hard constraints after test failures showed agents rationalising exceptions
- Rewrote description to match how people actually ask for this ("reads like AI", "sounds like ChatGPT")
- Added a 16-check grading script and isolation-based eval pipeline
- Renamed to `humanise` (Australian English)

## Install

Copy the folder into your Claude Code skills directory:

```
~/.claude/skills/humanise/
```

Invoke with `/humanise` or ask Claude to "humanise this", "de-AI this", "clean up the AI writing", "strip the AI out", etc.

## What it does

1. Checks three hard constraints: zero em dashes, no manufactured insight framing, no staccato fragment sequences
2. Scans 32 patterns across 7 categories
3. Rewrites problematic sections while keeping meaning intact
4. Runs a self-audit loop and revises until clean
5. Flags experiential vacancy: the absence of specific details and personal stakes that makes AI writing feel generic

## Patterns

| Category | # | Examples |
|---|---|---|
| Content | 1-6 | "a pivotal moment in the evolution of...", "nestled in the heart of..." |
| Language | 7-12 | "delve", "serves as", "It's not just X; it's Y" |
| Style | 13-18 | Emoji-led bullet points, title case headings, curly quotes |
| Communication | 19-21 | "I hope this helps!", "as of my last training update" |
| Filler | 22-25 | "In today's fast-paced world", "The future looks bright" |
| Sensory | 26-28 | Ghost/spectral language, quietness obsession, forced synesthesia |
| Structural | 29-32 | Mid-sentence rhetorical questions, generic metaphors, dramatic transitions |

Full catalogue with before/after examples in `references/patterns.md`.

## File structure

```
humanise/
├── SKILL.md                       Main skill instructions
├── references/patterns.md         32 patterns with before/after examples
├── evals/                         Testing infrastructure (see TESTING.md)
└── research/                      Analysis of 4 source articles
```

## Known limitations

- **Can't reconstruct what was never there.** Removes AI patterns but can't invent an author's real memories or relationships.
- **Claude and ChatGPT produce different slop.** The sensory patterns (ghost language, quietness, synesthesia) show up more in ChatGPT output.
- **Programmatic grading catches about 60% of tells.** Subtler issues need human judgment in the self-audit loop.
- **Patterns are transient.** The catalogue will need periodic updates as models evolve.

## Sources

- [@blader](https://github.com/blader), [humanizer](https://github.com/blader/humanizer) (original skill)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon)
- Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html), NYT Magazine
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop)
- [Grammarly, "Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/)

## Licence

[MIT](LICENCE)
