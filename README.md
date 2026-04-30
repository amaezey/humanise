# humanise

A [Claude Code skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) that flags patterns in prose that often look like AI did it, explains what each pattern is, and — if asked — suggests fixes or rewrites.

Forked from [blader/humanizer](https://github.com/blader/humanizer), restructured around a programmatic grader, an iteration harness, and a corpus of human and AI essays we use to test what the grader actually catches.

## Why this exists

People can usually tell when something was written by AI. They often can't explain why. The patterns are real — there's a body of research on stylometric markers (Kobak, Przystalski, Zaitsu, Abdulhai), a larger body of practitioner anecdata (the Wikipedia AI Cleanup project, GPTZero, Grammarly, NYT, Substack writers), and a small industry of detectors that mostly don't work.

We pulled what was credible from both, turned it into 43 programmatic checks across 38 patterns, ran it on a corpus of human and AI writing, learned which checks actually distinguish the two, refined what we kept, and noted where the patterns are register-coded rather than authorship-coded. This README is an honest account of what we found, what works, where the limits are, and what's next.

## What it does

Give it text and the skill can:

1. **Audit** — list flagged patterns, quoting the input, with a one-line "why" for each.
2. **Suggestions** — for each flag, propose a concrete alternative phrasing.
3. **Rewrite** — Balanced (fix surface and strong tells, leave structural patterns) or All (also rework structural ones).
4. **Write** — produce a fresh draft to a brief, with the patterns held in mind.
5. **Save report** — write the audit or before/after comparison to Markdown.

The audit always comes first. Suggestions and rewrites only happen when asked.

## Install

```bash
# Claude Code CLI
npx skills@latest add amaezey/humanise/humanise

# Or clone and symlink (updates on git pull)
git clone https://github.com/amaezey/humanise.git ~/.local/share/humanise
ln -s ~/.local/share/humanise/humanise ~/.claude/skills/humanise

# Claude Code desktop: download the latest release zip from
# https://github.com/amaezey/humanise/releases/latest
```

## Usage

Invoke with `/humanise` or ask Claude to audit, check, humanise, de-AI, clean up, strip AI tells, or save a Markdown report. Run the grader directly with:

```bash
python3 humanise/grade.py --format markdown --depth balanced <file>
python3 humanise/grade.py --format markdown --depth all <file>
```

`--depth balanced` requires fixing hard-fail and strong-warning patterns; `--depth all` adds context-sensitive ones.

## What we found

Honest version, not the marketing version.

### Some patterns work

A handful of patterns *are* genuinely AI-correlated when applied at high density: em dashes, AI vocabulary clustering ("delve", "navigate", "underscore"), manufactured insight ("the real X is..."), formulaic openers ("In today's fast-paced world..."), and section scaffolding ("Let's explore..."). These also fire on human writing — but at much lower density. The signal is the *stack*, not any one occurrence.

### Many patterns are register-coded, not authorship-coded

In a controlled comparison on long-form first-person essay (5 human originals, 5 AI fresh-writes from matched briefs, 5 AI rewrites of the human originals), the grader's "strong AI signal" patterns fired on humans and AI roughly equally. Triads, anaphora, contrived contrast, em dashes — all are valid rhetorical moves that good writers use. AI uses them too, often badly. The grader catches them because AI overuses them as a blunt instrument; it can't tell the difference between a writer who's earned a triad and one who's filling a slot. So the flag means *re-examine this* — not *this is AI*.

### Body statistics separate the two more reliably than patterns

Sentence-length variance is the cleanest signal we found. In matched-genre, matched-topic comparisons:

| Group | Sentence length mean | Sentence length stdev | Paragraph length stdev |
|---|---|---|---|
| Human (n=5) | 23 words | **17** | 37 |
| AI fresh-write (n=5) | 13 words | **7** | 23 |
| AI rewrite of human (n=5) | 14 words | **7** | 21 |

Humans cluster around longer sentences with much higher variance. AI clusters tight around 13-word sentences regardless of register. This isn't currently a grader check; we surface it in the iteration report.

### AI rewriting *increases* strong-signal density

Asking AI to rewrite a human essay produces output with **more** strong-tell patterns than the human original — about 44% more in our matched comparison. The rewrite trades context-sensitive richness for stronger pattern-matching tells. This is why the skill's own rewrite step is conservative even on patterns humans use legitimately: AI does them badly.

### Two audiences, two rules

The findings above shape how the skill talks:

- **To a human writer**: flagged patterns are review priorities, not verdicts. Keep them if you've earned them.
- **To itself, when rewriting**: still strip them by default. AI does these patterns badly even when humans don't have to.

## Performance

Each iteration runs the skill against an eval suite. The block below is auto-generated.

<!-- performance:start -->
**iteration-4** (2026-04-29T12:55:01Z)

- Mean pass rate: 95.5% across 18 evals
- Human-vs-ai_fresh flag gap: total +5% / strong +11%
- Human-vs-ai_rewrite flag gap: total -12% / strong +44%
- Regressions vs prev iteration: 0

[Full report](dev/skill-workspace/iteration-4/performance-report.md)
<!-- performance:end -->

The "human-vs-ai gap" lines are the load-bearing claim — humans should trigger fewer flags than AI in matched-genre comparisons. In long-form essay register, the gap is small on totals and inverted on strong signals. That's the finding the rest of this README is built around.

## Representative output

Excerpt from `python3 humanise/grade.py --format markdown --depth all dev/evals/samples/generated-ai/ai-08-feedback-education.md`:

```text
Initial assessment
Summary: 5 of 43 checks were flagged for AI-style writing patterns.

Confidence: Medium. Several signs of AI-like writing appeared, but the
evidence is pattern-based and should be read in context.
Basis: 5 context-sensitive signal(s); AI pressure score reached 4/4.
Note: This is a confidence assessment about AI-writing signs, not an
authorship verdict.

Main issues found
- AI pressure from stacked signals: Flagged. Stacked weak signals:
  paragraph length uniformity, headings in prose. Score: 4/4.
- Headings in prose: Flagged. Found 2 heading(s).
```

Rewrite workflows include the rewritten draft, a structural self-check, and the post-check report.

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
| 7 | AI vocabulary words and phrases | "delve", "landscape", "provide a valuable insight" |
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
| 17 | Curly quotation marks | "..." instead of "..." |
| 18 | Hyphenated modifier clusters | 3+ hyphenated compounds in one sentence |
| | **Communication** | |
| 19 | Collaborative artifacts | "I hope this helps!", "Let me know if..." |
| 20 | Knowledge-cutoff disclaimers | "as of my last training update..." |
| 21 | Sycophantic/servile tone | "Great question!", "You're absolutely right!" |
| | **Filler and hedging** | |
| 22 | Filler phrases | "In today's fast-paced world", "Generally speaking" |
| 23 | Excessive hedging | "It could potentially possibly be argued..." |
| 24 | Generic positive conclusions | "The future looks bright", "Exciting times lie ahead" |
| 25 | Staccato rhythm | Short sentences at predictable positions |
| | **Sensory and atmospheric** | |
| 26 | Ghost/spectral language | shadows, whispers, echoes, phantoms |
| 27 | Quietness obsession | "quiet" 10 times in 759 words about pebbles |
| 28 | Forced synesthesia | "grief tasting of metal", "hands humming with colour" |
| | **Structural tells** | |
| 29 | Mid-sentence rhetorical questions | "The solution? It's simpler than you think." |
| 30 | Generic/ungrounded metaphors | Plausible but specific to nobody |
| 31 | Excessive list-making | Converting prose to bullets unnecessarily |
| 32 | Dramatic narrative transitions | "Something shifted.", "Everything changed." |
| | **Voice and register** | |
| 33 | Countdown negation | "It wasn't X. It wasn't Y. It was Z." |
| 34 | Per-paragraph miniature conclusions | Every paragraph wraps up neatly |
| 35 | Tonal uniformity / register lock | One register throughout, no human drift |
| 36 | Faux specificity | "The smell of coffee on a Sunday morning", specific to nobody |
| 37 | Neutrality collapse | Stripping the author's stance, defaulting to balanced |
| 38 | Section scaffolding | "Let's explore...", "Let's dive into..." |

Density and stacking matter more than any single occurrence. The grader's `overall-ai-signal-pressure` check fires when several weaker patterns appear together — that's usually a stronger signal than any individual flag.

## Where to be careful

- **Genre matters.** Persuasive how-to, business memo, literary essay, and journalistic reportage all use patterns this skill flags. Audit output is calibrated to spot AI overuse, not to police legitimate technique. Read flags as priorities, not verdicts.
- **Patterns drift.** AI vocabulary lists go stale ("delve" peaked in 2023–24). The catalogue needs periodic refresh.
- **The skill itself is an LLM.** It can introduce the patterns it's trying to catch — neutrality collapse, pronoun depletion, generic substitution. The semantic-preservation step in the rewrite flow mitigates this but can't eliminate it.
- **Detection is asymmetric.** The skill catches AI doing patterns badly. It can also wrongly flag humans doing the same patterns well. The audit voice tries to make this distinction visible; the user has to apply judgement.
- **Sample sizes are small.** Findings here are based on a 15-sample matched corpus (5 human + 5 AI fresh + 5 AI rewrite). Directional, not definitive.

## What's next

Active work on:

- Reframing the audit voice so flagged patterns read as *review priorities* rather than verdicts.
- Calibrating thresholds by register (literary essay vs corporate doc vs news copy).
- Adding new candidate signals (sentence-length mean, ghost-spectral density, negation density, unicode flair) where evidence supports.
- Demoting pattern checks that don't separate humans from AI in matched genres (em dashes, manufactured insight, triad density may belong in softer categories).
- Growing the matched corpus past N=5 per group.

## File structure

```
humanise/                          Skill (this is what gets installed)
├── SKILL.md                       Main skill instructions
├── grade.py                       43-check grading script
└── references/                    Pattern catalogue, alternatives, process

dev/                               Development only (not installed)
├── evals/                         Eval suite, samples, harness
│   ├── evals.json                 18 eval cases (audit / suggest / rewrite / write)
│   ├── corpus.json                Genre-paired comparative-baseline corpus
│   ├── run_skill_creator_iteration.py
│   └── samples/{human-sourced,generated-ai}/
├── research/                      Findings and source-pattern analysis
└── skill-workspace/iteration-N/   Iteration outputs and review viewers
```

## Sources

**Foundation:**
- [@blader](https://github.com/blader), [humanizer](https://github.com/blader/humanizer) (original skill)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup, patterns 1–25)

**Pattern research:**
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (experiential vacancy)
- Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html) (NYT — ghost language, quietness, synesthesia)
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (rhetorical questions, metaphors, list-making, transitions)
- [Grammarly](https://www.grammarly.com/blog/ai/common-ai-words/) and [GPTZero](https://gptzero.me/ai-vocabulary) (vocabulary lists)
- [Kobak et al., `llm-excess-vocab`](https://github.com/berenslab/llm-excess-vocab) (annotated PubMed excess-vocabulary list)
- Matthew Vollmer, ["I Asked the Machine to Tell on Itself"](https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself)
- Shreya Shankar, ["AI Writing"](https://sh-reya.com/blog/ai-writing/)

**Academic research:**
- [Abdulhai et al., "How LLMs Distort Our Written Language"](https://arxiv.org/abs/2603.18161) (subtraction framing: neutrality collapse, pronoun depletion)
- [Nature, "Signs of AI-generated text found in 14% of biomedical abstracts"](https://www.nature.com/articles/d41586-025-02097-6)
- [Przystalski et al., "Stylometry recognizes human and LLM-generated texts"](https://arxiv.org/abs/2507.00838)
- [Zaitsu et al., "Stylometry can reveal AI authorship"](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) (PLOS ONE)
- [Bisztray et al., "I Know Which LLM Wrote Your Code Last Summer"](https://arxiv.org/abs/2506.17323) (ACM AISec)

**Practitioner guides:**
- [AI Detectors: How to tell if text is AI written](https://www.aidetectors.io/blog/how-to-tell-if-text-is-ai-written)
- [SEO Engine: Signs of AI writing](https://seoengine.ai/blog/signs-of-ai-writing)
- [SAGE: AI detection for peer reviewers](https://www.sagepub.com/explore-our-content/blogs/posts/sage-perspectives/2025/06/11/ai-detection-for-peer-reviewers-look-out-for-red-flags)

## Licence

[MIT](LICENCE)
