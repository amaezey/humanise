# humanise

A fork of [blader/humanizer](https://github.com/blader/humanizer) by [@blader](https://github.com/blader), restructured, research-expanded, and tested. The original skill drew from [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup). This version adds 8 pattern categories, triples the vocabulary list, introduces an eval pipeline, and incorporates the "subtraction framing" from Abdulhai et al. (2026) — recognising that AI removes stance, pronouns, and specificity, not just adds detectable patterns.

Created by [Billie-Mae Kennedy](https://github.com/amaezey).

## What changed from the original

- Restructured per [Anthropic's skill best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices): split into SKILL.md + reference file for progressive disclosure
- Expanded from 25 to 38 patterns using research from NYT, Substack, Grammarly, Nature, and Abdulhai et al. (2026)
- Added experiential vacancy, density-without-purpose, and subtraction framing (neutrality collapse, faux specificity, tonal uniformity) as structural diagnostics
- Tightened hard constraints after test failures showed agents rationalising exceptions
- Rewrote description to match how people actually ask for this ("reads like AI", "sounds like ChatGPT")
- Added a 31-check grading script and isolation-based eval pipeline
- Renamed to `humanise` (Australian English)

## Install

Copy the folder into your Claude Code skills directory:

```
~/.claude/skills/humanise/
```

Invoke with `/humanise` or ask Claude to "humanise this", "de-AI this", "clean up the AI writing", "strip the AI out", etc.

## What it does

1. Checks three hard constraints: zero em dashes, no manufactured insight framing, no staccato fragment sequences
2. Scans 38 patterns across 8 categories
3. Rewrites problematic sections while keeping meaning intact
4. Runs a self-audit loop and revises until clean
5. Flags experiential vacancy: the absence of specific details and personal stakes that makes AI writing feel generic

## Patterns

38 patterns across 8 categories. Full before/after examples in `references/patterns.md`.

| # | Pattern | Example |
|---|---|---|
| | **Content** | |
| 1 | Significance inflation | "a pivotal moment in the evolution of..." |
| 2 | Notability claims | Listing media mentions as proof of importance |
| 3 | Superficial -ing analyses | "highlighting...", "underscoring...", "reflecting..." |
| 4 | Promotional language | "nestled in the heart of...", "vibrant", "stunning" |
| 5 | Vague attributions | "Experts argue...", "Industry reports suggest..." |
| 6 | Formulaic challenges sections | "Despite these challenges... continues to thrive" |
| | **Language and grammar** | |
| 7 | AI vocabulary words (41+) | "delve", "landscape", "tapestry", "harness", "unparalleled" |
| 8 | Copula avoidance | "serves as", "stands as" instead of "is" |
| 9 | Negative parallelisms | "It's not just X; it's Y" |
| 10 | Rule of three | Forcing ideas into triads |
| 11 | Synonym cycling | "the protagonist... the main character... the central figure" |
| 12 | False ranges | "from X to Y, from A to B" |
| | **Style** | |
| 13 | Boldface overuse | Mechanical bolding of terms that don't need emphasis |
| 14 | Inline-header lists | Bolded label + colon turning prose into slides |
| 15 | Title case in headings | "Strategic Negotiations And Global Partnerships" |
| 16 | Emojis in professional content | Emoji-led bullet points |
| 17 | Curly quotation marks | \u201c...\u201d instead of "..." |
| 18 | Hyphenated modifier clusters | 3+ hyphenated compounds in one sentence |
| | **Communication** | |
| 19 | Collaborative artifacts | "I hope this helps!", "Let me know if..." |
| 20 | Knowledge-cutoff disclaimers | "as of my last training update..." |
| 21 | Sycophantic/servile tone | "Great question!", "You're absolutely right!" |
| | **Filler and hedging** | |
| 22 | Filler phrases | "In today's fast-paced world", "Generally speaking" |
| 23 | Excessive hedging | "It could potentially possibly be argued..." |
| 24 | Generic positive conclusions | "The future looks bright", "Exciting times lie ahead" |
| 25 | Staccato rhythm | Short sentences at predictable positions (hooks, landings) |
| | **Sensory and atmospheric** | |
| 26 | Ghost/spectral language | Everything becomes shadows, whispers, echoes, phantoms |
| 27 | Quietness obsession | "quiet" 10 times in 759 words about pebbles |
| 28 | Forced synesthesia | "grief tasting of metal", "hands humming with colour" |
| | **Structural tells** | |
| 29 | Mid-sentence rhetorical questions | "The solution? It's simpler than you think." |
| 30 | Generic/ungrounded metaphors | Plausible but specific to nobody |
| 31 | Excessive list-making | Converting prose to bullets unnecessarily |
| 32 | Dramatic narrative transitions | "Something shifted.", "Everything changed." |
| | **Voice and register** | |
| 33 | Countdown negation | "It wasn't X. It wasn't Y. It was Z." |
| 34 | Per-paragraph miniature conclusions | Every paragraph wraps up neatly with a summary sentence |
| 35 | Tonal uniformity / register lock | One register throughout, no human drift or breaks |
| 36 | Faux specificity | "The smell of coffee on a Sunday morning" — specific to nobody |
| 37 | Neutrality collapse | Stripping the author's stance, defaulting to balanced/neutral |
| 38 | Section scaffolding | "Let's explore...", "Let's dive into...", "Now let's look at..." |

## File structure

```
humanise/
├── SKILL.md                       Main skill instructions
├── references/patterns.md         38 patterns with before/after examples
├── evals/                         Testing infrastructure (see TESTING.md)
└── research/                      Analysis of source articles and studies
```

## Known limitations

- **Can't reconstruct what was never there.** Removes AI patterns but can't invent an author's real memories or relationships.
- **Claude and ChatGPT produce different slop.** The sensory patterns (ghost language, quietness, synesthesia) show up more in ChatGPT output.
- **Programmatic grading catches about 60% of tells.** Subtler issues (tonal uniformity, faux specificity, neutrality collapse) need human judgment in the self-audit loop.
- **Patterns are transient.** The catalogue will need periodic updates as models evolve. AI vocabulary shifts with model versions — "delve" peaked 2023–24, newer words emerge each generation.
- **The skill can introduce what it detects.** As an LLM rewriting text, it can itself neutralise stance or strip pronouns (Abdulhai et al. 2026). The semantic preservation step (Step 2.5) mitigates this but requires attention.

## Sources

- [@blader](https://github.com/blader), [humanizer](https://github.com/blader/humanizer) (original skill)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon)
- Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html), NYT Magazine
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop)
- [Grammarly, "Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/)
- [Abdulhai et al., "How LLMs Distort Our Written Language"](https://arxiv.org/abs/2603.18161), 2026
- [Nature, "Signs of AI-generated text found in 14% of biomedical abstracts"](https://www.nature.com/articles/d41586-025-02097-6), 2025

## Licence

[MIT](LICENCE)
