# humanise

A [Claude Code skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) that audits text for signs of AI-style writing, explains what was flagged, and optionally rewrites after the user chooses a cleanup strategy. Detects 38 patterns across 8 categories with 43 programmatic checks.

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

Invoke with `/humanise` or ask Claude to audit, check, humanise, de-AI, clean up, strip AI tells, or save a Markdown report.

## What it does

Give it text and it can follow five workflows:

1. **Audit only:** report what was flagged and why, without rewriting.
2. **Audit plus recommendation:** report findings and recommend Balanced or All cleanup.
3. **Audit, agree, then rewrite:** ask before changing text when intent or genre is ambiguous.
4. **Rewrite and verify:** rewrite only when requested, then run the post-check.
5. **Save report:** write the audit or before/after report to Markdown.

The script still keeps lower-level diagnostic fields for debugging, but the user-facing path uses `python3 grade.py --format markdown --depth <balanced|all> <file>` so reports start in plain English.

## Representative report output

Excerpt from `python3 humanise/grade.py --format markdown --depth all dev/evals/samples/generated-ai/ai-08-feedback-education.md`. Rewrite workflows also include the rewrite, structural self-check, post-check report, and the full 43-row table before and after rewriting.

```text
Initial assessment
Summary: 5 of 43 checks were flagged for AI-style writing patterns.

Confidence: Medium. Several signs of AI-like writing appeared, but the evidence is pattern-based and should be read in context.
Basis: 5 context-sensitive signal(s); AI pressure score reached 4/4.
Note: This is a confidence assessment about AI-writing signs, not an authorship verdict.

AI-pressure explanation: AI-pressure looks for accumulation: weaker patterns that may be harmless alone but become more meaningful when they appear together. Here the stacked signals were paragraph length uniformity, headings in prose. That means the draft looked machine-packaged, with too much visible structure and too little natural variation. Score: 4/4, so this check was flagged.

Main issues found
- AI pressure from stacked signals: Flagged. What it looks for: Looks for several weaker AI-writing signals appearing together, which can make a draft feel machine-packaged even when no single signal is decisive. What happened here: Stacked weak signals: paragraph length uniformity, headings in prose. Score: 4/4. This points to machine-packaged structure rather than one isolated wording choice. Why this matters: Several weak signals appearing together can make a draft feel machine-packaged even when each signal alone is explainable. All action: Fix.
- Headings in prose: Flagged. What it looks for: Checks for markdown headings and plain title headings when prose should flow. What happened here: Found 2 heading(s): "# Why Feedback Matters in Learning", "# Why Feedback Matters in Learning". Why this matters: Headings can make prose feel packaged by an assistant rather than written as a continuous piece. All action: Fix.

Full check table excerpt

| Check | Status | What it looks for | What happened here | Why this matters | All action |
|---|---|---|---|---|---|
| Em dashes | Clear | Checks for em dash punctuation, a strong current AI-style signal in this skill. | No issue found in this text. | Em dashes are now a strong style fingerprint in generated prose, especially when they appear as default punctuation. | None |
| AI pressure from stacked signals | Flagged | Looks for several weaker AI-writing signals appearing together, which can make a draft feel machine-packaged even when no single signal is decisive. | Stacked weak signals: paragraph length uniformity, headings in prose. Score: 4/4. This points to machine-packaged structure rather than one isolated wording choice. | Several weak signals appearing together can make a draft feel machine-packaged even when each signal alone is explainable. | Fix |
| Headings in prose | Flagged | Checks for markdown headings and plain title headings when prose should flow. | Found 2 heading(s): "# Why Feedback Matters in Learning", "# Why Feedback Matters in Learning". | Headings can make prose feel packaged by an assistant rather than written as a continuous piece. | Fix |
```

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
| 7 | AI vocabulary words and phrases | "delve", "landscape", "provide a valuable insight", GPTZero 100, Kobak excess-vocab pressure |
| 8 | Copula avoidance | "serves as", "stands as" instead of "is" |
| 9 | Contrived contrast / negative parallelism | "It's not X; it's Y" / "It's Y, not X" |
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
├── grade.py                       43-check grading script
└── references/patterns.md         38 patterns with before/after examples

dev/                               Development only (not installed)
├── evals/                         Eval suite, samples, unit tests
│   ├── run_grade_sweep.py          Regenerates corpus-wide sweep report
│   ├── grade-sweep-report.json     Current generated/human corpus metrics
│   └── samples/human-sourced/      Comment-cleaned source corpus
├── research/                      Source article analysis
├── ISSUES.md                      Known issues and technical notes
└── TESTING.md                     Eval methodology and coverage
```

## What changed from the original

- Restructured per [Anthropic's skill best practices](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills#best-practices): split into SKILL.md + reference file for progressive disclosure
- Expanded from 25 to 38 patterns using research from [Wikipedia (WikiProject AI Cleanup)](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), [Kriss (NYT)](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html), [Caroll (Substack)](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon), [Guo (Ignorance.ai)](https://www.ignorance.ai/p/the-field-guide-to-ai-slop), [Grammarly](https://www.grammarly.com/blog/ai/common-ai-words/), [GPTZero AI Vocabulary](https://gptzero.me/ai-vocabulary), [Nature](https://www.nature.com/articles/d41586-025-02097-6), [Abdulhai et al. (2026)](https://arxiv.org/abs/2603.18161), [Przystalski et al. (2025)](https://arxiv.org/abs/2507.00838), and [Zaitsu et al. (2025)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369)
- Added experiential vacancy, density-without-purpose, and subtraction framing as structural diagnostics
- Added a 43-check grading script, failure-mode reporting, mode action buckets, and isolation-based eval pipeline
- Added a reproducible corpus sweep runner and comment-cleaned human-source samples for false-positive auditing
- Renamed to `humanise` (Australian English)

## Known limitations

- **Can't reconstruct what was never there.** Removes AI patterns but can't invent an author's real memories or relationships.
- **Claude and ChatGPT produce different slop.** The sensory patterns (ghost language, quietness, synesthesia) show up more in ChatGPT output.
- **Programmatic grading catches many surface and structural tells.** Subtler issues (tonal uniformity, faux specificity, neutrality collapse, citation validity, fiction pacing) need human judgment in the self-check loop.
- **Checks are not authorship verdicts.** Human writing can legitimately trip context warnings. The report shows the evidence and mode action so the user can decide what to preserve.
- **Patterns are transient.** The catalogue will need periodic updates as models evolve. AI vocabulary shifts with model versions, "delve" peaked 2023-24, newer words emerge each generation.
- **The skill can introduce what it detects.** As an LLM rewriting text, it can itself neutralise stance or strip pronouns (Abdulhai et al. 2026). The semantic preservation step (Step 5) mitigates this but requires attention.

## Sources

**Foundation:**
- [@blader](https://github.com/blader), [humanizer](https://github.com/blader/humanizer) (original skill)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup (patterns 1-25)

**Pattern research:**
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (experiential vacancy)
- Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html), NYT Magazine (ghost language, quietness, synesthesia)
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (rhetorical questions, metaphors, list-making, dramatic transitions)
- [Grammarly, "Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/) (expanded vocabulary list)
- [GPTZero, "AI Vocabulary"](https://gptzero.me/ai-vocabulary) (April 2026 high-ratio phrase list; all 100 public table entries used as clustering signals)
- [Kobak et al., `llm-excess-vocab`](https://github.com/berenslab/llm-excess-vocab) (900 annotated PubMed excess-vocabulary rows; used as a biomedical/scientific cluster signal)
- Matthew Vollmer, ["I Asked the Machine to Tell on Itself"](https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself) (cross-source taxonomy and source trail)
- Shreya Shankar, ["AI Writing"](https://sh-reya.com/blog/ai-writing/) (orphaned demonstratives and weak AI prose mechanics)

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
