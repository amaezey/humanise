# humanise

A [Claude Code skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) that edits text to remove signs of AI generation. Detects and fixes 38 patterns across 8 categories.

Forked from [blader/humanizer](https://github.com/blader/humanizer) by [@blader](https://github.com/blader), then restructured, expanded, and tested.

## Install

### Claude Code (CLI)

```
npx skills@latest add amaezey/humanise/humanise
```

Or clone and symlink (updates automatically on `git pull`):

```bash
git clone https://github.com/amaezey/humanise.git ~/.local/share/humanise
ln -s ~/.local/share/humanise/humanise ~/.claude/skills/humanise
```

### Claude Code (desktop)

Download the [latest release zip](https://github.com/amaezey/humanise/releases/latest) and upload it in Claude Code desktop settings.

## Usage

Invoke with `/humanise` or ask Claude to "humanise this", "de-AI this", "clean up the AI writing", "strip the AI out", etc.

## What it does

Give it text and it:

1. Runs a programmatic pre-check (31 checks via a Python grading script) and scans the input against all 38 patterns
2. Rewrites flagged sections: structural patterns first (repetitive section arcs, tonal flatness, neutralised stance), then surface patterns (AI vocabulary, formatting, filler)
3. Checks the rewrite didn't strip the author's stance or voice
4. Runs a non-programmatic structural self-audit covering patterns the script can't detect (tonal uniformity, section monotony, stance preservation, resolution density)
5. Re-runs the grading script on its own output and revises until both the script and the self-audit pass
6. Returns the rewrite with a report of what changed

## Patterns

38 patterns across 8 categories. Full before/after examples in `humanise/references/patterns.md`.

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
| 36 | Faux specificity | "The smell of coffee on a Sunday morning", specific to nobody |
| 37 | Neutrality collapse | Stripping the author's stance, defaulting to balanced/neutral |
| 38 | Section scaffolding | "Let's explore...", "Let's dive into...", "Now let's look at..." |

## File structure

```
humanise/                          Skill (this is what gets installed)
├── SKILL.md                       Main skill instructions
├── grade.py                       31-check grading script
└── references/patterns.md         38 patterns with before/after examples

dev/                               Development only (not installed)
├── evals/                         Eval suite, samples, unit tests
├── research/                      Source article analysis
├── ISSUES.md                      Known issues and technical notes
└── TESTING.md                     Eval methodology and coverage
```

## What changed from the original

- Restructured per [Anthropic's skill best practices](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills#best-practices): split into SKILL.md + reference file for progressive disclosure
- Expanded from 25 to 38 patterns using research from [Wikipedia (WikiProject AI Cleanup)][wikipedia], [Kriss (NYT)][kriss], [Caroll (Substack)][caroll], [Guo (Ignorance.ai)][guo], [Grammarly][grammarly], [Nature][nature], [Abdulhai et al. (2026)][abdulhai], [Przystalski et al. (2025)](https://arxiv.org/abs/2507.00838), and [Zaitsu et al. (2025)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369)
- Added experiential vacancy, density-without-purpose, and subtraction framing as structural diagnostics
- Added a 31-check grading script and isolation-based eval pipeline
- Renamed to `humanise` (Australian English)

## Known limitations

- **Can't reconstruct what was never there.** Removes AI patterns but can't invent an author's real memories or relationships.
- **Claude and ChatGPT produce different slop.** The sensory patterns (ghost language, quietness, synesthesia) show up more in ChatGPT output.
- **Programmatic grading catches about 80% of tells.** Subtler issues (tonal uniformity, faux specificity, neutrality collapse) need human judgment in the self-audit loop.
- **Patterns are transient.** The catalogue will need periodic updates as models evolve. AI vocabulary shifts with model versions, "delve" peaked 2023-24, newer words emerge each generation.
- **The skill can introduce what it detects.** As an LLM rewriting text, it can itself neutralise stance or strip pronouns (Abdulhai et al. 2026). The semantic preservation step (Step 2.5) mitigates this but requires attention.

## Sources

**Foundation:**
- [@blader](https://github.com/blader), [humanizer](https://github.com/blader/humanizer) (original skill)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup (patterns 1-25)

**Pattern research:**
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (experiential vacancy)
- Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html), NYT Magazine (ghost language, quietness, synesthesia)
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (rhetorical questions, metaphors, list-making, dramatic transitions)
- [Grammarly, "Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/) (expanded vocabulary list)

**Academic research:**
- [Abdulhai et al., "How LLMs Distort Our Written Language"](https://arxiv.org/abs/2603.18161), 2026 (subtraction framing: neutrality collapse, pronoun depletion, semantic drift)
- [Nature, "Signs of AI-generated text found in 14% of biomedical abstracts"](https://www.nature.com/articles/d41586-025-02097-6), 2025 (vocabulary items, temporal fingerprinting)
- [Przystalski et al., "Stylometry recognizes human and LLM-generated texts in short samples"](https://arxiv.org/abs/2507.00838), 2025
- [Zaitsu et al., "Stylometry can reveal AI authorship"](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369), PLOS ONE, 2025
- [Bisztray et al., "I Know Which LLM Wrote Your Code Last Summer"](https://arxiv.org/abs/2506.17323), ACM AISec, 2025

**Practitioner guides:**
- [AI Detectors, "How to tell if text is AI written"](https://www.aidetectors.io/blog/how-to-tell-if-text-is-ai-written), 2026
- [SEO Engine, "Signs of AI writing"](https://seoengine.ai/blog/signs-of-ai-writing), 2025
- [SAGE, "AI detection for peer reviewers"](https://www.sagepub.com/explore-our-content/blogs/posts/sage-perspectives/2025/06/11/ai-detection-for-peer-reviewers-look-out-for-red-flags), 2025

## Licence

[MIT](LICENCE)
