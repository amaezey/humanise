# humanise

A Claude Code skill that edits text to remove signs of AI generation. It detects 32 patterns across 7 categories, rewrites problematic sections, and adds genuine voice. Built for anyone who uses AI to draft and needs the output to not read like AI wrote it.

## Install

Copy the `humanise/` folder into your Claude Code skills directory:

```
~/.claude/skills/humanise/
```

Or if you're using a project-level skills directory:

```
your-project/.claude/skills/humanise/
```

The skill registers automatically. Invoke it with `/humanise` or by asking Claude to "humanise this text", "de-AI this", "clean up the AI writing", or similar.

## What it does

Given a piece of text, the skill:

1. Checks three hard constraints (zero em dashes, no manufactured insight framing, no staccato fragment sequences)
2. Scans for 32 patterns organised in 7 categories (content, language, style, communication, filler, sensory/atmospheric, structural)
3. Rewrites problematic sections while preserving meaning
4. Runs a self-audit loop ("What still makes this obviously AI-generated?") and revises until clean
5. Addresses experiential vacancy: the absence of specific details, named people, real places, and personal stakes that makes AI writing feel generic even when technically correct

The skill uses progressive disclosure per Anthropic's best practices: SKILL.md (214 lines) contains the hard constraints, philosophy, process, and a full worked example. The 32-pattern reference catalogue lives in `references/patterns.md` (426 lines) and is loaded only when needed.

## What it catches

| Category | Patterns | Examples |
|---|---|---|
| Content (1-6) | Significance inflation, notability claims, superficial -ing analyses, promotional language, vague attributions, formulaic challenges sections | "a pivotal moment in the evolution of...", "nestled in the heart of..." |
| Language (7-12) | AI vocabulary words (37+), copula avoidance, negative parallelisms, rule of three, synonym cycling, false ranges | "delve", "serves as", "It's not just X; it's Y" |
| Style (13-18) | Boldface overuse, inline-header lists, title case, emojis, curly quotes, hyphenated compound modifier clusters | Emoji-led bullet points, "Strategic Negotiations And Global Partnerships" |
| Communication (19-21) | Collaborative artifacts, knowledge-cutoff disclaimers, sycophantic tone | "I hope this helps!", "as of my last training update" |
| Filler (22-25) | Filler phrases, excessive hedging, generic positive conclusions, staccato rhythm | "In today's fast-paced world", "The future looks bright" |
| Sensory (26-28) | Ghost/spectral language, quietness obsession, forced synesthesia | "carry the ghosts of...", "quiet" 10x in 759 words, "grief tasting of metal" |
| Structural (29-32) | Mid-sentence rhetorical questions, generic metaphors, excessive list-making, dramatic narrative transitions | "But now? You won't believe this.", "Something shifted." |

## How it was developed

### Origin

The original humaniser skill (v3.0.0) was a single-file prompt based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. That guide documents patterns observed across thousands of instances of AI-generated text on Wikipedia.

### Restructuring against best practices

The skill was reviewed against [Anthropic's skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) and restructured to:

- Split into SKILL.md (under 500 lines) + reference file (progressive disclosure)
- Rewrite the description in third person for correct triggering
- Remove duplicate patterns (em dash appeared twice)
- Trim explanatory prose Claude doesn't need
- Add a structured feedback loop to the process
- Clean non-standard frontmatter fields

### Research expansion

Four articles were analysed to identify gaps in the original pattern catalogue:

- [Linda Caroll, "Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (Substack, Feb 2026) -- identified experiential vacancy, emotional risk aversion, and the warm-fuzzy default as structural problems beyond lexical patterns
- [Sam Kriss, "Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html) (NYT Magazine, Dec 2025) -- documented ghost/spectral language, quietness obsession, forced synesthesia, and the overfitting mechanism ("it screams at the top of its voice about how absolutely everything in sight is shadowy, subtle and quiet")
- [Charlie Guo, "The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (Artificial Ignorance, Substack) -- contributed mid-sentence rhetorical questions, excessive list-making, generic metaphors, and the core framing: "a good writer uses these devices sparingly, and with intention. AI litters them throughout its writing indiscriminately"
- [Grammarly, "Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/) (Feb 2026) -- provided 29 additional AI vocabulary words and phrases across 5 categories, filling gaps in transition phrases, hedging qualifiers, and tech buzzwords

Full research notes are in `research/`.

### Testing methodology

The skill was tested using an isolation-based eval pipeline:

1. **Select human-written originals.** Five pre-AI essays spanning different voices and genres:
   - Sam Harris, ["Free will"](https://www.samharris.org/blog/the-illusion-of-free-will) (philosophical argument, 2012)
   - Ken Murray, ["How doctors die"](https://www.zocalopublicsquare.org/2011/11/30/how-doctors-die/ideas/nexus/) (personal medical essay, 2011)
   - Virginia Woolf, ["The Death of the Moth"](https://gutenberg.net.au/ebooks12/1203811h.html) (literary observation, 1942)
   - David Wong, ["What is the Monkeysphere?"](https://www.cracked.com/article_14990_what-monkeysphere.html) (irreverent comedy, 2007)
   - George Orwell, ["Why I write"](https://orwellfoundation.com/george-orwell/by-orwell/essays-and-other-works/why-i-write/) (direct autobiography, 1946)

2. **Generate AI versions via isolated agents.** Each agent received a content brief (key arguments to cover) but never saw the original text or its voice. This produced AI-flavoured rewrites of the same content.

3. **Humanise via isolated agents.** Separate agents applied the skill to the AI output. These agents had no access to the originals, so the humaniser worked blind, exactly as it would in real use.

4. **Grade programmatically.** A 16-check grading script (`evals/grade.py`) tested for em dashes, AI vocabulary clustering, manufactured insight, staccato sequences, anaphora, collaborative artifacts, curly quotes, sentence variance, promotional language, significance inflation, negative parallelisms, copula avoidance, filler phrases, generic conclusions, forced triads, and superficial -ing endings.

5. **Compare to originals qualitatively.** The humanised output was read alongside the original human text to assess voice naturalness, meaning preservation, and whether the output could plausibly have been written by a person.

6. **Iterate.** When tests revealed failures (e.g. the Wong piece retained "And honestly?" because the agent judged it as serving the humorous tone), the skill instructions were tightened and the test re-run until the failure was fixed.

Three iterations were run. The first used carefully crafted content briefs. The third used bare, lazy prompts ("write a beautiful essay about gratitude") to test against genuine slop. All final outputs passed 16/16 programmatic checks.

### Description optimisation

The description was rewritten to match user vocabulary rather than internal pattern names. Trigger phrases like "reads like AI", "sounds like ChatGPT wrote it", and "strip the AI out" were added based on realistic eval queries. An explicit NOT-trigger list was added to prevent false activation on adjacent tasks (proofreading, translating, writing from scratch).

## File structure

```
humanise/
├── README.md                         This file
├── SKILL.md                          Main instructions (214 lines)
├── references/
│   └── patterns.md                   32-pattern catalogue with before/after examples (426 lines)
├── evals/
│   ├── grade.py                      16-check programmatic grading script
│   ├── evals.json                    5 test cases with assertions
│   └── trigger-eval.json             20 trigger/no-trigger queries for description testing
└── research/
    ├── linda-caroll.md               Experiential vacancy analysis
    ├── nyt-chatbot-style.md          Ghost/spectral/synesthesia patterns
    ├── ignorance-ai-field-guide.md   Density/purpose framing
    └── grammarly-ai-words.md         29 additional AI vocabulary words
```

## Running the grading script

```bash
# Grade a single file against all 16 checks
python3 evals/grade.py path/to/text.md

# Grade against specific checks only
python3 evals/grade.py path/to/text.md no-em-dashes,no-manufactured-insight,no-staccato-sequences
```

Output is JSON with pass/fail per assertion and evidence for each.

## Known limitations

- **Can't add what was never there.** The skill removes AI patterns and adds voice cues, but it cannot reconstruct an author's personal connections, real memories, or named relationships. If the AI text mentions "a colleague" generically, the humaniser can flag the vacancy but cannot invent a real person.
- **Claude vs ChatGPT slop profiles differ.** The sensory/atmospheric patterns (ghost language, quietness obsession, forced synesthesia) are more common in ChatGPT output. Claude produces cleaner prose even with lazy prompts, which means the skill has less to fix on Claude-generated input.
- **Programmatic grading catches ~60% of tells.** The grading script tests lexical and structural patterns. Subtler issues (experiential vacancy, emotional risk aversion, generic metaphors) require human judgment during the self-audit loop.
- **Patterns are transient.** As models train on articles documenting these tells, the tells will evolve. The pattern catalogue will need periodic updates.

## Credits

Created by [Billie-Mae Kennedy](https://github.com/amaezey).

- **Foundation:** [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup
- **Research sources:**
  - Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (Substack, 2026)
  - Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html) (NYT Magazine, 2025)
  - Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (Artificial Ignorance, Substack)
  - Grammarly, ["Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/) (2026)
- **Test texts:** Sam Harris, Ken Murray, Virginia Woolf, David Wong (Cracked.com), George Orwell
- **Development methodology:** Built using Anthropic's [skill-creator](https://github.com/anthropics/claude-code-plugins) plugin and [skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)

## Licence

[MIT](LICENCE)
