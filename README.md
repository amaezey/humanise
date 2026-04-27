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

1. Calibrates intensity: Light, Medium, or Hard
2. Runs a programmatic pre-check (43 checks via a Python grading script) and scans the input against all 38 patterns
3. Builds a plain-English Markdown report from `human_report`: overview, confidence, AI-pressure explanation, failed checks, and a full 43-check table
4. Rewrites flagged sections: structural patterns first (repetitive section arcs, tonal flatness, neutralised stance), then surface patterns (AI vocabulary, formatting, filler)
5. Checks the rewrite didn't strip the author's stance or voice
6. Runs a non-programmatic structural self-audit covering patterns the script can't detect (tonal uniformity, section monotony, stance preservation, resolution density)
7. Re-runs the grading script and revises according to mode: Hard aims for a clean pass; Medium and Light fix stronger signals and disclose any intentional preserves
8. Returns the rewrite with a readable report: before/after scores, confidence, remaining issues, and the full check table

The script still keeps lower-level diagnostic fields for debugging, but the skill's normal output uses `python3 grade.py --format markdown --mode hard <file>` so the user-facing report starts in plain English. Aggregate AI-signal pressure is one of the 43 checks, not a separate verdict. It counts as one failed check only when its internal 0/4 pressure score reaches the threshold.

## Representative report output

Excerpt from `python3 humanise/grade.py --format markdown --mode hard dev/evals/samples/generated-ai/ai-08-feedback-education.md`. The actual skill output also includes the rewrite, structural self-audit, post-check report, and the full 43-row table before and after rewriting.

```text
Mode: Hard

Initial assessment
Summary: 5 of 43 checks showed signs of AI-style writing.

Confidence: Medium.
Basis: 5 context-sensitive signals; aggregate AI-signal pressure reached 4/4.
Note: This is a confidence assessment about AI-writing signs, not an authorship verdict.

AI-pressure explanation: Aggregate AI-signal pressure is one of the 43 checks, not a separate verdict. It counts as one failed check only when its internal pressure score reaches the threshold. Here it was 4/4 and triggered.

Main issues found
- Aggregate AI-signal pressure: Shows signs. Aggregate pressure was 4/4. It counted weaker signals together: paragraph uniformity, markdown headings. Vocabulary pressure contributed 0 point(s). Hard action: Fix.
- Headings in prose: Shows signs. Found 2 heading(s): "# Why Feedback Matters in Learning", "# Why Feedback Matters in Learning". Hard action: Fix.
- Dense negation: Shows signs. Found 10 negation markers (12.4 per 1000 words). Hard action: Fix.
- Paragraph length uniformity: Shows signs. Paragraph length CV: 0.08 across 10 paragraphs (target: >=0.18). Hard action: Fix.
- Triad density: Shows signs. Found 12 triad(s), including "feedback as a grade, a correction, a short comment written", "quizzes, peer review, short conferences with the", "lab report, presentation, math solution looks like", plus 9 more. Hard action: Fix.

Full check table excerpt

| Check | Status | Why | Hard action |
|---|---|---|---|
| Em dashes | Pass | No sign of this pattern found. | None |
| Clustered AI vocabulary | Pass | No sign of this pattern found. | None |
| Nonliteral land/surface phrasing | Pass | No sign of this pattern found. | None |
| Aggregate AI-signal pressure | Shows signs | Aggregate pressure was 4/4. It counted weaker signals together: paragraph uniformity, markdown headings. Vocabulary pressure contributed 0 point(s). | Fix |
| Manufactured insight framing | Pass | No sign of this pattern found. | None |
| Headings in prose | Shows signs | Found 2 heading(s): "# Why Feedback Matters in Learning", "# Why Feedback Matters in Learning". | Fix |
| Dense negation | Shows signs | Found 10 negation markers (12.4 per 1000 words). | Fix |
| Paragraph length uniformity | Shows signs | Paragraph length CV: 0.08 across 10 paragraphs (target: >=0.18). | Fix |
| Triad density | Shows signs | Found 12 triad(s), including "feedback as a grade, a correction, a short comment written", "quizzes, peer review, short conferences with the", "lab report, presentation, math solution looks like", plus 9 more. | Fix |

Final report
Summary: before 5/43 checks showed signs; after 0/43 checks showed signs.
Confidence after rewrite: Low. No programmatic checks showed AI-writing patterns.
AI-pressure after rewrite: 0/4 and did not trigger.
Remaining issues: none.
Full post-check table: all 43 checks pass.
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
- **Programmatic grading catches many surface and structural tells.** Subtler issues (tonal uniformity, faux specificity, neutrality collapse, citation validity, fiction pacing) need human judgment in the self-audit loop.
- **Checks are not authorship verdicts.** Human writing can legitimately trip context warnings. The report shows the evidence and mode action so the user can decide what to preserve.
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
