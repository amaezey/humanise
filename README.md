# human-eyes

A [Claude Code skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) that flags patterns in text that make it sound like AI, and (if asked) suggests fixes or rewrites.

Forked from [blader/humanizer](https://github.com/blader/humanizer), restructured around a deterministic grader, an iteration harness, and a corpus of matched human and AI essays for testing what the grader actually catches.

## Install

### Clone and symlink (preferred)

Get updates with `git pull`. Run from your local checkout.

```bash
git clone https://github.com/amaezey/human-eyes.git ~/.local/share/human-eyes
ln -s ~/.local/share/human-eyes/human-eyes ~/.claude/skills/human-eyes
```

### Claude Code CLI

```bash
npx skills@latest add amaezey/human-eyes/human-eyes
```

### Codex and Claude Code desktop

Download the latest release zip from <https://github.com/amaezey/human-eyes/releases/latest>.

## Why this exists

People are increasingly expected to use AI for workplace writing, then left with prose that feels wrong but is hard to diagnose or repair. The damage is usually cumulative: small tells stack across voice, rhythm, structure, and phrasing until the writing reads as synthetic, even when no single sentence is obviously broken.

human-eyes audits a draft against a catalogue of AI-writing patterns drawn from peer-reviewed research, journalism, and craft analysis. The grader is deterministic, so the same input always produces the same audit. The output names each flagged pattern, quotes the phrase from your draft, and points to the source it comes from, so you can read the evidence and decide what to change yourself.

## What it does

The skill runs an **Audit** first: a summary block (counts, severity, signal stacking) plus every flagged pattern with the quoted phrase from your draft. Auto-detected patterns first, then agent-assessed.

The audit ends with a prompt: full coverage report, suggestions, rewrite, or save. Each runs only when asked.

- **Full coverage report**: the same audit plus coverage tables for every check, both auto-detected and agent-assessed.
- **Suggestions**: alternative phrasing for each flag.
- **Rewrite**: rewrites the draft in two modes. Balanced fixes surface and strong patterns. All also reworks structural ones.
- **Write**: a fresh draft to a brief, with the patterns in mind.
- **Save report**: writes the audit or before/after comparison to Markdown.

## Usage

Invoke with `/human-eyes` or ask Claude to "audit this", "human-eyes this", "unsloppify", "strip the AI tells", or "rewrite to sound human". The Audit action runs first. Suggestions, Rewrite, and Write only run when asked.

### Run the grader directly (no LLM)

The grader is a deterministic script. Running it without the skill is useful when you want a reproducible audit with no LLM in the loop and no API cost. The agent-judgement layer is skipped in this mode.

```bash
python3 human-eyes/scripts/grade.py --format markdown --depth balanced <file>
python3 human-eyes/scripts/grade.py --format markdown --depth all <file>
```

`--depth balanced` requires fixing hard-fail and strong-warning patterns. `--depth all` adds context-sensitive ones. Add `--judgement-file <path>` to merge a precomputed agent-judgement reading into the audit. Add `--full-report` for per-category coverage tables and the full phrase list.

## How it works

human-eyes has three layers:

- **Pattern catalogue.** A registry of named AI-writing patterns with severity, sources, and before/after examples. Source of truth is `human-eyes/scripts/patterns.json`; the human-readable view is `human-eyes/references/patterns.md`.
- **Grader.** A deterministic Python script (`human-eyes/scripts/grade.py`) that runs regex and density checks against the draft. No LLM in this layer, so the same input always produces the same audit.
- **Agent-judgement registry.** Structural readings the grader can't do (tonal uniformity, faux specificity, neutrality collapse, structural monotony, generic metaphors, forced synesthesia, even jargon distribution, plus a polymorphic genre slot). Lives in `human-eyes/scripts/judgement.json`. The agent reads each prompt, returns a structured answer, and the grader merges those answers into the final audit before rendering.

When you invoke the skill, it makes the agent-judgement reading, calls the grader with `--judgement-file`, prints the audit verbatim, then asks what you want next.

## Patterns

Patterns are organised by category. Full before/after examples in `human-eyes/references/patterns.md`.

- **Source**: primary external attribution. "Wikipedia (editor consensus)" means the pattern is in the WikiProject AI Cleanup catalogue without an external upstream citation.
- **Check**: how the pattern is detected.
    - `regex` runs against the text deterministically.
    - `agent` runs as a small LLM reading on the whole draft (items defined in `human-eyes/scripts/judgement.json`).
- **Severity**: enforcement tier. One of `hard_fail`, `strong_warning`, or `context_warning`.

| # | Pattern | Source | Check | Severity | Example |
|---|---|---|---|---|---|
| | **Content** | | | | |
| 1 | Significance inflation | Belcher; Juzek & Ward; Sun et al.; Kobak et al.; GPTZero; Grammarly; Kriss/NYT; Wikipedia (editor consensus) | regex | context_warning | "a pivotal moment in the evolution of..." |
| 2 | Notability claims | Wikipedia (editor consensus); Futurism (adjacent, on fabricated bylines) | regex | strong_warning | Listing media mentions as proof of importance |
| 3 | Superficial -ing analyses | Reinhart et al. (PNAS 2025); Belcher; Wikipedia (editor consensus); practitioner guides (aidetectors.io, seoengine.ai, SAGE) | regex | strong_warning | "highlighting...", "underscoring...", "reflecting..." |
| 4 | Promotional language | Wikipedia (editor consensus); Grammarly; Caroll; Rohrer | regex | context_warning | "nestled in the heart of...", "vibrant", "stunning" |
| 5 | Vague attributions | Wikipedia (editor consensus); Shankar; Nature 2025 (adjacent) | regex | strong_warning | "Experts argue...", "Industry reports suggest..." |
| | **Language and grammar** | | | | |
| 7 | AI vocabulary words and phrases | Kobak et al. (Science Advances 2025); Juzek & Ward (ACL 2025; arxiv 2025); Reinhart et al. (PNAS 2025); Merrill et al. (WaPo); Kousha & Thelwall (ISSI 2025); Geng & Trotta (ACL 2025); GPTZero; Grammarly; Nature 2025; Kriss/NYT; Guo; Wikipedia (editor consensus) | regex | strong_warning | "delve", "landscape", "provide a valuable insight" |
| 8 | Copula avoidance | Geng & Trotta (arxiv 2024); Wikipedia (editor consensus) | regex | strong_warning | "serves as", "stands as" instead of "is" |
| 9 | Contrived contrast / negative parallelism | Russell, Karpinska, Iyyer (ACL 2025); Merrill et al. (WaPo); Stockton; Kriss/NYT; Guo; Wikipedia (editor consensus) | regex | strong_warning | "It's not X; it's Y" / "It's Y, not X" |
| 10 | Rule of three | Russell, Karpinska, Iyyer (ACL 2025); Kriss/NYT; Guo; practitioner guides; Wikipedia (editor consensus) | regex | context_warning | Forcing ideas into triads |
| 10a | Triad density | Same source family as #10; matched-genre corpus measurement | regex | context_warning | The density variant of #10 rule of three: three or more triads in a paragraph or short passage. |
| 53 | Vocabulary diversity | Practitioner guides (aidetectors.io, seoengine.ai, SAGE); matched-genre corpus measurement | regex | context_warning | A coarse type-token ratio metric for prose of 150+ words: low ratios suggest narrow vocabulary. |
| | **Style** | | | | |
| 13 | Boldface overuse | Wikipedia (editor consensus); Guo | regex | context_warning | Mechanical bolding of terms that don't need emphasis |
| 14 | Inline-header lists | Wikipedia (editor consensus); Guo; Shankar | regex | strong_warning | Bolded label + colon turning prose into slides |
| 15 | Title case in headings | Russell, Karpinska, Iyyer (ACL 2025); Wikipedia (editor consensus); Grammarly | regex | context_warning | "Strategic Negotiations And Global Partnerships" |
| 16 | Emojis in professional content | Wikipedia (editor consensus); Guo | regex | context_warning | Emoji-led bullet points |
| 17 | Curly quotation marks | Wikipedia (editor consensus); matched-genre corpus measurement | regex | context_warning | "..." instead of "..." |
| 18 | Hyphenated modifier clusters | Wikipedia (editor consensus) | regex | context_warning | 3+ hyphenated compounds in one sentence |
| 49 | Em dashes | Merrill et al. (WaPo); Edwards (Ars Technica); Kriss/NYT; Guo; Wikipedia (editor consensus); Phillips (Ringer dissent); Csutoras (training-corpus mechanism); Bailey (six-model em-dash test); matched-genre corpus measurement | regex | strong_warning | ChatGPT and similar systems use the em dash (`—`) as default mid-sentence punctuation. |
| | **Communication** | | | | |
| 19 | Collaborative artifacts | Wikipedia (editor consensus); OpenAI sycophancy rollback (April 2025); Guo; Caroll | regex | hard_fail | "I hope this helps!", "Let me know if..." |
| 20 | Knowledge-cutoff disclaimers | Wikipedia (editor consensus) | regex | strong_warning | "as of my last training update..." |
| 21 | Sycophantic/servile tone | OpenAI sycophancy rollback (April 2025); Wikipedia (editor consensus); Kriss/NYT; Caroll | regex | hard_fail | "Great question!", "You're absolutely right!" |
| | **Filler and hedging** | | | | |
| 22 | Filler phrases | Wikipedia (editor consensus); Grammarly; Guo; Kriss/NYT (adjacent) | regex | strong_warning | "In today's fast-paced world", "Generally speaking" |
| 23 | Excessive hedging | Wikipedia (editor consensus); Grammarly; Shankar; Abdulhai et al.; Stanford HAI / Liang et al.; Vara (abstraction drift) | regex | context_warning | "It could potentially possibly be argued..." |
| 23a | False balance or concession | Chiang (via Vollmer); Wikipedia (editor consensus); Abdulhai (adjacent) | regex | strong_warning | "While critics argue..., supporters say...", "the truth lies somewhere in the middle" |
| 24 | Generic positive conclusions | Wikipedia (editor consensus); Shankar; Caroll; Guo | regex | hard_fail | "The future looks bright", "Exciting times lie ahead" |
| 25 | Staccato rhythm | Shankar; Wikipedia (editor consensus); Guo; Caroll; matched-genre corpus measurement | regex | context_warning | Short sentences at predictable positions |
| 47 | Soft explainer scaffolding | Vollmer (closing-ritual phrases); matched-genre corpus measurement | regex | strong_warning | "One useful area...", "Another useful area...", "The main strength..." |
| 48 | Dense negation | Stockton (negation series); extends #9 across paragraphs | regex | context_warning | Clusters of "is not", "are not", "does not", "isn't", "aren't"... |
| 50 | Formulaic openers | Grammarly (transitions); Vollmer; Guo | regex | strong_warning | "At its core,", "At a foundational level,", "Beyond this..." |
| | **Sensory and atmospheric** | | | | |
| 26 | Ghost/spectral language | Kriss/NYT; corpus measurement | regex | context_warning | shadows, whispers, echoes, phantoms |
| 27 | Quietness obsession | Kriss/NYT | regex | context_warning | "quiet" 10 times in 759 words about pebbles |
| 28 | Forced synesthesia | Kriss/NYT | agent | context_warning | "grief tasting of metal", "hands humming with colour" |
| | **Structural tells** | | | | |
| 29 | Mid-sentence rhetorical questions | Guo; Kriss/NYT | regex | context_warning | "The solution? It's simpler than you think." |
| 30 | Generic/ungrounded metaphors | Guo; Kriss/NYT; Caroll | agent | strong_warning | Plausible but specific to nobody |
| 31 | Excessive list-making | Guo; Shankar | regex | context_warning | Converting prose to bullets unnecessarily |
| 31a | Decorative Unicode | Guo; Wikipedia (editor consensus); corpus | regex | context_warning | Arrows, checkmarks, stars, ornamental bullets, emoji-style symbols in prose |
| 32 | Dramatic narrative transitions | Guo | regex | context_warning | "Something shifted.", "Everything changed." |
| 38 | Section scaffolding | Wikipedia (editor consensus) | regex | strong_warning | "Let's explore...", "Let's dive into..." |
| 42 | Manufactured insight framing | Guo (performed knowingness); Kriss/NYT; Wikipedia (editor consensus) | regex | strong_warning | "what's really", "the real answer", "here's what's really" |
| 44 | Signposted conclusion | Vollmer (closing rituals); Wikipedia (editor consensus) | regex | context_warning | "In summary,", "In conclusion,", "To summarise,", "To sum up,..." |
| 52 | Sentence rhythm variance | Caroll; Guo; Grammarly; Przystalski/Zaitsu/Bisztray (stylometry); Ju, Blix, Williams (domain syntax); matched-genre corpus measurement | regex | context_warning | A coarse rhythm metric for prose of 100+ words: low variance suggests mechanical pacing. |
| 54 | Structural monotony | Shankar; Guo; practitioner guides | agent | context_warning | Every section follows the same arc: opener, supporting argument, micro-conclusion, repeat. |
| | **Voice and register** | | | | |
| 33 | Countdown negation | Practitioner guides (aidetectors.io, seoengine.ai, SAGE) | regex | context_warning | "It wasn't X. It wasn't Y. It was Z." |
| 34 | Per-paragraph miniature conclusions | Shankar; practitioner guides | regex | context_warning | Every paragraph wraps up neatly |
| 35 | Tonal uniformity / register lock | Practitioner guides; Caroll; Guo | agent | strong_warning | One register throughout, no human drift |
| 35a | Vague 'this/that' starts | Shankar; Vollmer | regex | context_warning | "This highlights...", "This underscores...", "That speaks to..." |
| 35b | Repeated 'This...' chains | Shankar (via Vollmer); chain-form variant of #35a | regex | context_warning | Three or more consecutive sentences beginning with "This [verb]": "This shows... This suggests... This means..." |
| 36 | Faux specificity | Practitioner guides; Caroll; Guo; Preston (collapse of context / missing concrete particular); Vara (strategic vagueness) | agent | strong_warning | "The smell of coffee on a Sunday morning", specific to nobody |
| 37 | Neutrality collapse | Abdulhai et al. (arxiv 2603.18161) | agent | strong_warning | Stripping the author's stance, defaulting to balanced |
| 39 | Placeholder residue | Gmelius (via Vollmer) | regex | hard_fail | `{client_name}`, `[Company Name]`, `[insert date]`, "Hi {name}" |
| 40 | Rubric echoing | Vollmer | regex | context_warning | "the author creates a tone", "I can tell because", "this quote shows that" |
| 41 | Genre-specific manual checks | Walsh (arxiv 2024; poetry); Aranya/Poetly (poetry); Clarke/Clarkesworld (fiction); Germain (fiction); Dhillon et al. (MFA fiction); Waltzer et al. (Wiley 2023; student writing); Hsu (student writing); Hastewire (student detection); Jiang & Hyland (SAGE 2025; academic); Murray & Tersigni (JALT 2024; academic); Bailey (Plagiarism Today; em-dash forensics); Gmelius (email); Bynder (marketing); Copy Posse (LinkedIn / business); AI for Lifelong Learners (essay shape); Futurism / PBS NewsHour (journalism); Vollmer (synthesis) | agent | context_warning | Genre-aware self-audit (academic / student essay / poetry / fiction). |
| 43 | Corporate AI-speak | Vollmer (inflated verbs); Grammarly (buzzwords); practitioner guides | regex | strong_warning | "delivering impact", "measurable outcomes", "scalable, production-grade" |
| 45 | Nonliteral land/surface phrasing | Hard-mode calibration pass against matched-genre corpus | regex | strong_warning | "the argument lands", "the idea lands", "your point lands" |
| 46 | Bland critical template | Caroll (tonal uniformity); Vollmer (model-specific fingerprints); Rudnicka (chatbot-specific styles); matched-genre corpus measurement | regex | strong_warning | "the kind of contemporary novel/film/book/album/show that..." |
| 51 | Mechanical repeated sentence starts | Caroll; Guo; Grammarly; matched-genre corpus measurement | regex | context_warning | Three or more consecutive sentences whose first word matches: "The X… The Y… The Z…" |
| 55 | Even jargon distribution | Practitioner guides (aidetectors.io, seoengine.ai, SAGE) | agent | context_warning | Jargon spreads uniformly across the text instead of clumping where the writer knows things. |
| | **Signal stacking** | | | | |
| | Signal stacking from stacked AI tells | Kobak et al. (corpus-level logic); composite of components #9, #19, #24, #34, #38, #42, #46, #47, #50 | regex | context_warning | Stacked weak signals reaching the threshold (e.g., "headings in prose, assistant residue, generic conclusion") |

Density and stacking matter more than any single occurrence. The grader's `overall-signal-stacking` check fires when several weaker patterns appear together; that is usually a stronger signal than any individual flag.

## Representative output

Default audit on `dev/evals/samples/generated-ai/ai-12-better-emails.md`:

```text
**Audit summary**
Auto-detected: 6 of 48 flagged · Agent-assessed: 0 of 0 flagged
Severity: 1 hard fail · 1 strong warning · 4 context warning
Signal stacking triggered: 8 of 4 threshold (contrived contrast framing, paragraph length uniformity, headings in prose, assistant residue)

**Auto-detected**

x Assistant residue: "let me know if"
! Contrived contrast: "are not clear about the purpose, the reader probably will not"
? Mechanical repeated sentence starts: "If you need a reply, say so.", "If you need approval, say what is being approved.", "If no action is needed, say that too."
? Headings in prose: "# How to Write Better Emails", "# How to Write Better Emails"
? Paragraph length uniformity: paragraph length variation 0.13 across 13 paragraphs (target above 0.18)
? Triad density: "people communicate at work, school, and in everyday administration", "email can save time, reduce confusion, and make it more likely", "confirming details, sending a document, or following up on a" (+6 more)

**Agent-assessed**

No agent-assessed reading was supplied.

**Next steps**

Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?
```

Re-running with `--full-report` keeps the same audit body and inserts a brief note plus per-category coverage tables under each mini-header. The full phrase list also drops the `(+N more)` cap. Excerpt of what's added under `**Auto-detected**`:

```text
Checks the script runs against the text directly.

**Content patterns**: 5/5 clear

**Language and grammar**: 2 flagged of 6

| Pattern | Severity | Result | Detail |
| --- | --- | --- | --- |
| Clustered AI vocabulary | strong warning | Clear |  |
| Contrived contrast | strong warning | Flagged | Fix contrived reframes at Balanced and All; recommend preserving only purposeful contrast at Balanced. |
| Avoiding plain 'is' | strong warning | Clear |  |
| Decorative three-part lists | context warning | Clear |  |
| Vocabulary diversity | context warning | Clear |  |
| Triad density | context warning | Flagged | Fix density-driven triads; recommend preserving if lists are structural or rhetorical. |

[... seven more category sub-tables in patterns.md heading order ...]
```

Rewrite workflows include the rewritten draft, a structural self-check, and the post-check report.

## Performance

Each iteration runs the skill against an eval suite. The block below is auto-generated.

<!-- performance:start -->
**iteration-7** (2026-05-03T12:27:19Z)

- Mean pass rate: 99.1% across 18 evals
- Human-vs-ai_fresh flag gap: total -5% / strong +11%
- Human-vs-ai_rewrite flag gap: total -20% / strong +44%
- Regressions vs prev iteration: 0

[Full report](dev/skill-workspace/iteration-7/performance-report.md)
<!-- performance:end -->

The "human-vs-ai gap" lines are the load-bearing claim. Humans should trigger fewer flags than AI in matched-genre comparisons. In long-form essay register, the gap is small on totals and inverted on strong signals. The numbers come from the most recent eval suite; the iteration harness rewrites the block on each run.

## What testing showed

### Some patterns work

A handful of patterns are genuinely AI-correlated when they appear at high density: em dashes, AI vocabulary clustering ("delve", "navigate", "underscore"), manufactured insight ("the real X is..."), formulaic openers ("In today's fast-paced world..."), and section scaffolding ("Let's explore..."). These also fire on human writing, just at much lower density. The signal lives in the stack: density and co-occurrence carry it.

### Many patterns are register-coded, not authorship-coded

A controlled comparison on long-form first-person essay (5 human originals, 5 AI fresh-writes from matched briefs, 5 AI rewrites of the human originals) shows the grader's "strong AI signal" patterns firing on humans and AI roughly equally. Triads, anaphora, contrived contrast, em dashes are all valid rhetorical moves that good writers use. AI uses them too, often badly. The grader catches them because AI overuses them as a blunt instrument; it cannot tell the difference between a writer who has earned a triad and one who is filling a slot. A flag prompts re-examination of the prose; it cannot decide authorship.

### Body statistics separate the two more reliably than patterns

Sentence-length variance is the cleanest signal in matched-genre, matched-topic comparisons:

| Group | Sentence length mean | Sentence length stdev | Paragraph length stdev |
|---|---|---|---|
| Human (n=5) | 23 words | **17** | 37 |
| AI fresh-write (n=5) | 13 words | **7** | 23 |
| AI rewrite of human (n=5) | 14 words | **7** | 21 |

Humans cluster around longer sentences with much higher variance. AI clusters tight around 13-word sentences regardless of register. This is not currently a grader check; the iteration report surfaces it instead.

### AI rewriting *increases* strong-signal density

Asking AI to rewrite a human essay produces output with **more** strong-pattern density than the human original (about 44% more in matched comparison). The rewrite trades context-sensitive richness for stronger pattern-matching. This is why the skill's own rewrite step stays conservative even on patterns humans use legitimately: AI does them badly.

## Where to be careful

- **Genre matters.** Persuasive how-to, business memo, literary essay, and journalistic reportage all use patterns this skill flags. Audit output is calibrated to spot AI overuse; legitimate technique is not the target. Treat each flag as something to review.
- **Patterns drift.** AI vocabulary lists go stale ("delve" peaked in 2023 to 2024). The catalogue needs periodic refresh.
- **The skill itself is an LLM.** It can introduce the patterns it is trying to catch (neutrality collapse, pronoun depletion, generic substitution). The semantic-preservation step in the rewrite flow mitigates this but cannot eliminate it.
- **Detection is asymmetric.** The skill catches AI doing patterns badly. It can also wrongly flag humans doing the same patterns well. The audit voice tries to make this distinction visible; the user has to apply judgement.
- **Sample sizes are small.** Findings here are based on a matched corpus of human, AI fresh-write, and AI rewrite samples (n=5 per group). Treat them as directional at this sample size.

## What's next

Active work, with open questions tracked in `dev/hypotheses.md`:

- Calibrating thresholds by register (literary essay vs corporate doc vs news copy).
- Adding sentence-length mean as a grader signal (variance is in; mean is the cleaner separator in matched-genre comparisons).
- Demoting pattern checks that do not separate humans from AI in matched genres (em dashes and manufactured insight may belong in softer categories).
- Growing the matched corpus past n=5 per group, with bootstrap confidence intervals so weak-signal patterns demote automatically.
- Calibrating severities on the agent-judgement items against the corpus rather than curated guesses.
- Verifying the rewrite step doesn't itself flatten the writer's stance (Abdulhai-style semantic preservation).
- Catching performative-direct fragments ("Direct. Punchy. Inevitable.") as a candidate pattern.
- Closing grader-integrity gaps: catalogued patterns without programmatic checks, and grader checks without catalogued patterns.

## File structure

```
human-eyes/                          Skill (this is what gets installed)
├── SKILL.md                       Main skill instructions
├── scripts/                       Grader and registry loaders
│   ├── grade.py                   Grading script
│   ├── registries.py              Loaders for the three JSON registries
│   ├── patterns.json              Pattern catalogue (severity, category, report text)
│   ├── judgement.json             Agent-judgement registry
│   ├── vocabulary.json            Severity and action labels, depth consequences
│   └── contracts/                 Audit JSON contract schema
└── references/                    Patterns, alternatives, severity, voice, process

dev/                               Development only (not installed)
├── evals/                         Eval suite, samples, harness
│   ├── evals.json                 Eval cases (audit / suggest / rewrite / write)
│   ├── corpus.json                Genre-paired comparative-baseline corpus
│   ├── run_skill_creator_iteration.py
│   └── samples/{human-sourced,generated-ai}/
├── research/                      Findings and source-pattern analysis
├── tools/                         Generators (render_patterns_md.py, render_audit_html.py)
└── skill-workspace/iteration-N/   Iteration outputs (benchmark.json, review.html, audit-fidelity.html)
```

## Sources

**Foundation:**
- [@blader](https://github.com/blader), [humanizer](https://github.com/blader/humanizer) (original skill)
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (WikiProject AI Cleanup catalogue; full per-pattern citation extraction in `dev/research/wikipedia-signs-of-ai-writing.md`)
- Matthew Vollmer, ["I Asked the Machine to Tell on Itself"](https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself) (pedagogical field guide; full per-section citation extraction in `dev/research/vollmer.md`)

**Academic research (vocabulary and grammatical signals):**
- [Kobak, González-Márquez, Horvát, Lause, "Delving into LLM-assisted writing in biomedical publications through excess vocabulary"](https://www.science.org/doi/10.1126/sciadv.adt3813) (Science Advances 2025; 900-row excess-vocabulary corpus, [GitHub](https://github.com/berenslab/llm-excess-vocab))
- [Juzek & Ward, "Why Does ChatGPT 'Delve' So Much?"](https://aclanthology.org/2025.coling-main.426.pdf) (ACL 2025; lexical overrepresentation traced to RLHF)
- [Juzek & Ward, "Word Overuse and Alignment in Large Language Models"](https://arxiv.org/pdf/2508.01930) (arxiv 2025; alignment-driven word overuse)
- [Reinhart et al., "Do LLMs write like humans? Variation in grammatical and rhetorical styles"](https://pnas.org/doi/10.1073/pnas.2422455122) (PNAS 2025; grammatical and rhetorical style variation)
- [Geng & Trotta, "Human-LLM Coevolution: Evidence from Academic Writing"](https://aclanthology.org/2025.findings-acl.657.pdf) (ACL 2025)
- [Geng & Trotta, "Is ChatGPT Transforming Academics' Writing Style?"](https://arxiv.org/abs/2404.08627) (arxiv 2024; documents 10%+ decline in "is/are" usage post-ChatGPT)
- [Kousha & Thelwall, "How much are LLMs changing the language of academic papers after ChatGPT?"](https://arxiv.org/pdf/2509.09596) (ISSI 2025)
- [Sun, Yin, Xu, Koller, Liu, "Idiosyncrasies in Large Language Models"](https://arxiv.org/abs/2502.12150v2) (arxiv 2025)
- [Ju, Blix, Williams, "Domain Regeneration: How well do LLMs match syntactic properties of text domains?"](https://aclanthology.org/2025.findings-acl.120) (ACL 2025)

**Academic research (behavioural and cognitive effects):**
- [Abdulhai et al., "How LLMs Distort Our Written Language"](https://arxiv.org/abs/2603.18161) (neutrality collapse, pronoun depletion, semantic drift in minimal edits)
- [Russell, Karpinska, Iyyer, "People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text"](https://aclanthology.org/2025.acl-long.267/) (ACL 2025)
- [Nature, "Signs of AI-generated text found in 14% of biomedical abstracts"](https://www.nature.com/articles/d41586-025-02097-6)

**Academic research (stylometry):**
- [Przystalski et al., "Stylometry recognizes human and LLM-generated texts"](https://arxiv.org/abs/2507.00838) (arxiv 2025)
- [Zaitsu et al., "Stylometry can reveal AI authorship"](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369) (PLOS ONE 2025)
- [Bisztray et al., "I Know Which LLM Wrote Your Code Last Summer"](https://arxiv.org/abs/2506.17323) (ACM AISec 2025; code stylometry)

**Academic research (domain-specific):**
- [Walsh et al., "AI poetry computational analysis"](https://arxiv.org/abs/2410.15299) (arxiv 2024; 5,700 ChatGPT poems vs 3,700 human poems)
- Neil Clarke (Clarkesworld editor), ["A Concerning Trend"](https://neil-clarke.com/a-concerning-trend/) (Feb 2023; closed submissions after 500/1200 AI submissions in a single week; "bad in ways no human has been bad before")
- [Waltzer et al., "Can teachers detect AI-generated student essays?"](https://onlinelibrary.wiley.com/doi/full/10.1111/bjet.13362) (Wiley 2023; 69 teachers, 140 students)
- [Murray & Tersigni, "Can instructors detect AI-generated papers?"](https://journals.sfu.ca/jalt/index.php/jalt/article/view/1895) (JALT 2024)
- [Jiang & Hyland, "Engagement markers in ChatGPT-generated argumentative essays"](https://journals.sagepub.com/) (SAGE 2025)
- [Dhillon et al., "MFA students vs LLMs fiction"](https://arxiv.org/abs/2510.13939) (arxiv 2025)
- [Spero & Emi, "Technical Report on the Pangram AI-Generated Text Classifier"](https://arxiv.org/abs/2402.14873)

**Academic research (detection bias and limits):**
- [Liang et al., "GPT detectors are biased against non-native English writers"](https://www.cell.com/patterns/fulltext/S2666-3899(23)00130-7) (Stanford HAI / Patterns 2023; 61.3% misclassification of TOEFL essays)

**Journalism and trade press:**
- Sam Kriss, ["Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html) (NYT Magazine 2025)
- Jeremy B. Merrill, Szu Yu Chen, Emma Kumer, ["What are the clues that ChatGPT wrote something?"](https://www.washingtonpost.com/technology/interactive/2025/how-detect-chatgpt-em-dash/) (Washington Post 2025)
- Benj Edwards, ["Forget AGI — Sam Altman celebrates ChatGPT finally following em dash formatting rules"](https://arstechnica.com/ai/2025/11/forget-agi-sam-altman-celebrates-chatgpt-finally-following-em-dash-formatting-rules/) (Ars Technica 2025)
- Brian Phillips, ["The em-dash defence"](https://www.theringer.com/2025/08/20/pop-culture/em-dash-use-ai-artificial-intelligence-chatgpt-google-gemini) (The Ringer, August 2025; dissenting view)
- Wendy Belcher, ["10 Ways AI Is Ruining Your Students' Writing"](https://www.chronicle.com/article/10-ways-ai-is-ruining-your-students-writing) (Chronicle of Higher Education 2025)
- Hua Hsu, ["What college students lose when ChatGPT writes their essays"](https://www.wnyc.org/story/what-students-lose-when-chatgpt-writes-their-essays/) (New Yorker / WNYC Brian Lehrer)
- Karolina Rudnicka, ["Each AI chatbot has its own, distinctive writing style"](https://www.scientificamerican.com/article/chatgpt-and-gemini-ai-have-uniquely-different-writing-styles) (Scientific American 2025)
- [Slate, "ChatGPT, AI shaming, and the paranoia of writing"](https://slate.com/technology/2025/08/chatgpt-artificial-intelligence-shaming-paranoia-writing.html) (August 2025; paranoia-spiral coverage of writers introducing typos to signal humanity)
- Jonathan Bailey, ["Em dashes, hyphens, and spotting AI writing"](https://www.plagiarismtoday.com/2025/06/26/em-dashes-hyphens-and-spotting-ai-writing/) (Plagiarism Today, June 2025; six-model em-dash test across ChatGPT, Copilot, Deepseek, Claude, Gemini, Meta.ai)
- PBS NewsHour / [Futurism](https://futurism.com/sports-illustrated-ai-generated-writers): CNET (77 AI finance articles, 2023) and Sports Illustrated (AI bylines, AI headshots)

**Practitioner essays and writer blogs:**
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (experiential vacancy, "warm fuzzies")
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (rhetorical questions, metaphors, list-making, transitions; coined "AI slop")
- Shreya Shankar, ["AI Writing"](https://sh-reya.com/blog/ai-writing/) (orphaned demonstratives, bullet-point fetish)
- Blake Stockton, ["Don't Write Like AI" series](https://blakestockton.com/dont-write-like-ai-1-101-negation) (negative parallelism)
- Vauhini Vara, ["Confessions of a Viral AI Writer"](https://www.wired.com/story/confessions-of-a-viral-ai-writer-llms/) (Wired 2023); *Searches: Selfhood in the Digital Age* (Pantheon 2025)
- Laura Preston, ["HUMAN_FALLBACK"](https://www.nplusonemag.com/issue-44/essays/human_fallback/) (n+1 Issue 44, 2022) and ["An Age of Hyperabundance"](https://www.nplusonemag.com/issue-47/essays/an-age-of-hyperabundance/) (n+1 Issue 47, 2024; "collapse of context")
- Ted Chiang, ["ChatGPT Is a Blurry JPEG of the Web"](https://www.newyorker.com/tech/annals-of-technology/chatgpt-is-a-blurry-jpeg-of-the-web) (New Yorker 2023); ["Why A.I. Isn't Going to Make Art"](https://www.newyorker.com/culture/the-weekend-essay/why-ai-isnt-going-to-make-art) (New Yorker 2024)
- Robin Sloan, [robinsloan.com](https://www.robinsloan.com/) (partnership framing for human-AI writing)
- Sean Trott, [seantrott.substack.com](https://seantrott.substack.com) (LLM signature analysis)
- Aranya, [Poetly](https://poetly.substack.com) (Substack; AI poetry tells beyond Walsh)
- David J. Germain, ["Writing dialog with ChatGPT"](https://medium.com/@dave.germain.79/writing-dialog-with-chatgpt-bd8024a69eb3) (Medium; parenthetical stage-directions in GPT-3.5 dialogue)
- Brent Csutoras, ["The em-dash dilemma"](https://medium.com/@brentcsutoras/the-em-dash-dilemma-how-a-punctuation-mark-became-ais-stubborn-signature-684fbcc9f559) (Medium; em-dash training-corpus mechanism)
- Fred Rohrer, [blog.frohrer.com](https://blog.frohrer.com/) (promotional register, n-gram analysis)

**Vendor and first-party:**
- OpenAI: [GPT-4 System Card](https://cdn.openai.com/papers/gpt-4-system-card.pdf); April 2025 [sycophancy rollback](https://openai.com/index/sycophancy-in-gpt-4o/); GPT-5.1 em-dash suppression
- Anthropic: [Claude Sonnet system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts)
- [GPTZero](https://gptzero.me/ai-vocabulary) (AI Vocabulary list; perplexity and burstiness model)
- [Grammarly](https://www.grammarly.com/blog/ai/common-ai-words/) (31 indicator words and phrases)
- [Gmelius](https://gmelius.com/blog/can-customers-tell-an-email-is-written-using-generative-ai) (catalogue of "AI-isms" in email)
- Bynder (2024 consumer study; 55% of US consumers correctly identify AI marketing; referenced through [Copy Posse](https://copyposse.com/blog/5-signs-your-email-was-written-by-ai-and-how-to-write-emails-that-sound-like-a-human/))
- Pangram ([Spero & Emi 2024](https://arxiv.org/abs/2402.14873)), [Copyleaks](https://copyleaks.com/ai-content-detector), [ZeroGPT](https://www.zerogpt.com/), [Originality.AI](https://originality.ai/), NetusAI, [Turnitin](https://www.turnitin.com/products/features/ai-writing-detection) (commercial detector landscape, referenced for context; human-eyes is not a detector)

**Practitioner guides referenced for detection thresholds:**
- [AI Detectors: How to tell if text is AI written](https://www.aidetectors.io/blog/how-to-tell-if-text-is-ai-written)
- [SEO Engine: Signs of AI writing](https://seoengine.ai/blog/signs-of-ai-writing)
- [SAGE: AI detection for peer reviewers](https://www.sagepub.com/explore-our-content/blogs/posts/sage-perspectives/2025/06/11/ai-detection-for-peer-reviewers-look-out-for-red-flags)
- [Hastewire, "How teachers spot ChatGPT use"](https://hastewire.com/blog/how-teachers-spot-chatgpt-use-key-signs-revealed) (student writing detection signals)
- [Copy Posse, "5 signs your email was written by AI"](https://copyposse.com/blog/5-signs-your-email-was-written-by-ai-and-how-to-write-emails-that-sound-like-a-human/) (LinkedIn tricolon armature; business-email tells)
- [AI for Lifelong Learners, "Tells beyond the em-dash"](https://aiforlifelonglearners.substack.com/p/tells-beyond-the-em-dash) (Substack; five-paragraph-essay shape, machine cleanliness)

## Licence

[MIT](LICENCE)
