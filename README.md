# humanise

A fork of [blader/humanizer](https://github.com/blader/humanizer) by [@blader](https://github.com/blader), restructured, research-expanded, and tested. The original skill drew from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup). This version adds 7 new pattern categories, triples the vocabulary list, and introduces an eval pipeline for verifying the skill works.

Created by [Billie-Mae Kennedy](https://github.com/amaezey).

## What changed from the original

- Restructured per [Anthropic's skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): split into SKILL.md (215 lines) + reference file (426 lines) for progressive disclosure
- Expanded from 25 to 32 patterns using research from NYT, Substack, and Grammarly (see [Research sources](#research-sources))
- Added experiential vacancy and density-without-purpose as structural diagnostics, not just lexical pattern matching
- Tightened hard constraints after test failures showed agents rationalising exceptions for humorous tone
- Rewrote description to match how people actually ask for this ("reads like AI", "sounds like ChatGPT") instead of internal pattern names
- Added a 16-check grading script and an isolation-based eval pipeline
- Renamed to `humanise` (Australian English)

## Install

Copy the folder into your Claude Code skills directory:

```
~/.claude/skills/humanise/
```

Or project-level:

```
your-project/.claude/skills/humanise/
```

Invoke with `/humanise` or ask Claude to "humanise this", "de-AI this", "clean up the AI writing", "strip the AI out", etc.

## What it does

1. Checks three hard constraints: zero em dashes, no manufactured insight framing, no staccato fragment sequences
2. Scans 32 patterns across 7 categories
3. Rewrites problematic sections while keeping meaning intact
4. Runs a self-audit loop ("What still makes this obviously AI-generated?") and revises until clean
5. Flags experiential vacancy: the absence of specific details, named people, and personal stakes that makes AI writing feel generic even when technically correct

## Patterns

| Category | # | Examples |
|---|---|---|
| Content | 1-6 | "a pivotal moment in the evolution of...", "nestled in the heart of..." |
| Language | 7-12 | "delve", "serves as", "It's not just X; it's Y" |
| Style | 13-18 | Emoji-led bullet points, title case headings, curly quotes |
| Communication | 19-21 | "I hope this helps!", "as of my last training update" |
| Filler | 22-25 | "In today's fast-paced world", "The future looks bright" |
| Sensory | 26-28 | Ghost/spectral language, "quiet" 10x in 759 words, "grief tasting of metal" |
| Structural | 29-32 | "But now? You won't believe this.", "Something shifted." |

Full catalogue with before/after examples in `references/patterns.md`.

## How it was tested

Three rounds of isolation-based testing:

1. **Pick human-written originals.** Five pre-AI essays across different voices:
   - Sam Harris, ["Free will"](https://www.samharris.org/blog/the-illusion-of-free-will) (2012)
   - Ken Murray, ["How doctors die"](https://www.zocalopublicsquare.org/2011/11/30/how-doctors-die/ideas/nexus/) (2011)
   - Virginia Woolf, ["The Death of the Moth"](https://gutenberg.net.au/ebooks12/1203811h.html) (1942)
   - David Wong, ["What is the Monkeysphere?"](https://www.cracked.com/article_14990_what-monkeysphere.html) (2007)
   - George Orwell, ["Why I write"](https://orwellfoundation.com/george-orwell/by-orwell/essays-and-other-works/why-i-write/) (1946)

2. **Generate AI versions with isolated agents.** Each agent got a content brief but never saw the original text. This produced AI-flavoured rewrites of the same content.

3. **Humanise with isolated agents.** Separate agents applied the skill blind (no access to originals), exactly as it works in real use.

4. **Grade programmatically.** 16-check script (`evals/grade.py`) tests for em dashes, AI vocabulary clustering, manufactured insight, staccato sequences, anaphora, and 11 other patterns.

5. **Compare to originals.** Read the humanised output alongside the original human text to check voice, meaning, and plausibility.

6. **Fix failures and re-run.** When Wong's piece kept "And honestly?" because the agent thought it served the humour, we tightened the hard constraints and re-ran until it passed.

All final outputs passed 16/16 programmatic checks across all iterations.

## Grading script

```bash
python3 evals/grade.py path/to/text.md
python3 evals/grade.py path/to/text.md no-em-dashes,no-manufactured-insight
```

Outputs JSON with pass/fail and evidence per check.

## File structure

```
humanise/
├── SKILL.md                       Main skill (215 lines)
├── references/patterns.md         32 patterns with before/after examples
├── evals/
│   ├── grade.py                   16-check grading script
│   ├── evals.json                 5 test cases with assertions
│   └── trigger-eval.json          20 trigger/no-trigger queries
└── research/                      Analysis of 4 source articles
```

## Known limitations

- **Can't reconstruct what was never there.** Removes AI patterns and adds voice cues, but can't invent an author's real memories or named relationships.
- **Claude and ChatGPT produce different slop.** The sensory patterns (ghost language, quietness, synesthesia) show up more in ChatGPT output. Claude writes cleaner even with lazy prompts.
- **Programmatic grading catches about 60% of tells.** Subtler issues (experiential vacancy, generic metaphors) need human judgment in the self-audit loop.
- **Patterns are transient.** Models will train on articles documenting these tells. The catalogue will need updates.

## Research sources

- [@blader](https://github.com/blader), [humanizer](https://github.com/blader/humanizer) (original skill)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup (foundation)
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (experiential vacancy)
- Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html), NYT Magazine (ghost language, synesthesia)
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (density framing, rhetorical questions)
- [Grammarly, "Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/) (expanded vocabulary)

## Licence

[MIT](LICENCE)
