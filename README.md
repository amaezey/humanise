# humanise

A [Claude Code skill](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills) that flags patterns in prose that often look like AI did it, explains what each pattern is, and (if asked) suggests fixes or rewrites.

Forked from [blader/humanizer](https://github.com/blader/humanizer), restructured around a programmatic grader, an iteration harness, and a corpus of matched human and AI essays for testing what the grader actually catches.

## Why this exists

People can usually tell when something was written by AI, even if they can't articulate why. The patterns behind that intuition are real, documented across peer-reviewed research and craft-level analysis (see Sources). Commercial detectors like GPTZero, Pangram, Copyleaks, Originality.AI, and Turnitin cover this territory with variable accuracy.

This skill turns those patterns into a regex/density grader (49 programmatic checks across 58 catalogued patterns and one aggregate meta-check) plus an eight-item agent-judgement registry, then runs them against a matched corpus of human and AI writing to see which checks separate the two.

## What it does

Give it text and the skill can:

1. **Audit**: list flagged patterns, quoting the input, with a one-line "why" for each.
2. **Suggestions**: for each flag, propose a concrete alternative phrasing.
3. **Rewrite**: Balanced (fix surface and strong patterns, leave structural ones) or All (also rework structural ones).
4. **Write**: produce a fresh draft to a brief, with the patterns held in mind.
5. **Save report**: write the audit or before/after comparison to Markdown.

The audit always comes first; suggestions and rewrites only happen when asked.

The audit returns three sections. The first two come from a deterministic grader (regex and density checks); the third is the agent reading the text directly.

- **Summary**: a verdict line counting flags by severity, then each flagged pattern with the quoted phrase from the input and the recommended action.
- **Detected patterns**: a per-category coverage list, so what passed and what was flagged are both visible.
- **Agent judgement**: eight readings of voice, register, and grounding.

When every check is clear and pressure has not triggered, the audit collapses to a single line.

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

Invoke with `/humanise` or ask Claude to audit, check, humanise, de-AI, clean up, strip AI patterns, or save a Markdown report. Run the grader directly with:

```bash
python3 humanise/scripts/grade.py --format markdown --depth balanced <file>
python3 humanise/scripts/grade.py --format markdown --depth all <file>
```

`--depth balanced` requires fixing hard-fail and strong-warning patterns; `--depth all` adds context-sensitive ones.

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

### How the skill applies the findings

The findings above shape how the skill talks:

- **To a human writer:** flagged patterns mark review priorities. Keep them where they have been earned.
- **To itself, when rewriting:** strip them by default. AI does these patterns badly even when humans do not have to.

## Performance

Each iteration runs the skill against an eval suite. The block below is auto-generated.

<!-- performance:start -->
**iteration-6** (2026-05-02T15:19:52Z)

- Mean pass rate: 98.3% across 18 evals
- Human-vs-ai_fresh flag gap: total -5% / strong +11%
- Human-vs-ai_rewrite flag gap: total -20% / strong +44%
- Regressions vs prev iteration: 0

[Full report](dev/skill-workspace/iteration-6/performance-report.md)
<!-- performance:end -->

The "human-vs-ai gap" lines are the load-bearing claim. Humans should trigger fewer flags than AI in matched-genre comparisons. In long-form essay register, the gap is small on totals and inverted on strong signals. The numbers come from the most recent eval suite; the iteration harness rewrites the block on each run.

## Representative output

Excerpt from `python3 humanise/scripts/grade.py --format markdown --depth all dev/evals/samples/generated-ai/ai-12-better-emails.md`:

```text
Audit
Severity: 1 hard_fail · 1 strong_warning · 4 context_warning · pressure: triggered
Pressure triggered: weaker AI-writing signals stacked to 8 of the 4-point threshold (contrived contrast framing, paragraph length uniformity, headings in prose, assistant residue).

? **Mechanical repeated sentence starts** — Action: Fix
x **Assistant residue** — "let me know if" — Action: Fix
! **Contrived contrast** — Action: Fix
? **Headings in prose** — "# How to Write Better Emails", "# How to Write Better Emails" — Action: Fix
? **Paragraph length uniformity** — Action: Fix
? **Triad density** — "people communicate at work, school, and in everyday administration", "email can save time, reduce confusion, and make it more likely", "confirming details, sending a document, or following up on a" (+6 more) — Action: Fix

---

**Content patterns** — 5/5 clear

**Language and grammar** — 2 flagged of 6

| Pattern | Result | Action |
| --- | --- | --- |
| Clustered AI vocabulary | Clear |  |
| Contrived contrast | Flagged | Fix |
| Avoiding plain 'is' | Clear |  |
| Decorative three-part lists | Clear |  |
| Vocabulary diversity | Clear |  |
| Triad density | Flagged | Fix |

[...]
```

Rewrite workflows include the rewritten draft, a structural self-check, and the post-check report.

## Patterns

53 numbered patterns, five sub-letter variants, and one aggregate meta-check across 8 categories. Full before/after examples in `humanise/references/patterns.md`. The Source column names the primary external attribution; "Wikipedia (editor consensus)" indicates the pattern is in the WikiProject AI Cleanup catalogue without an external upstream citation. The Severity column reports the grader's enforcement tier (`hard_fail`, `strong_warning`, `context_warning`); blank cells are catalogued patterns without their own programmatic check (covered by the agent-judgement readings, folded into a parent check, or pending Source curation).

| # | Pattern | Source | Severity | Example |
|---|---|---|---|---|
| | **Content** | | | |
| 1 | Significance inflation | Belcher; Juzek & Ward; Sun et al. (via Wikipedia) | context_warning | "a pivotal moment in the evolution of..." |
| 2 | Notability claims | Wikipedia (editor consensus); Futurism | strong_warning | Listing media mentions as proof of importance |
| 3 | Superficial -ing analyses | Reinhart et al. (PNAS 2025); Belcher | strong_warning | "highlighting...", "underscoring...", "reflecting..." |
| 4 | Promotional language | Wikipedia (editor consensus); Grammarly; Caroll | context_warning | "nestled in the heart of...", "vibrant", "stunning" |
| 5 | Vague attributions | Wikipedia (editor consensus); Shankar | strong_warning | "Experts argue...", "Industry reports suggest..." |
| 6 | Formulaic challenges sections | Wikipedia (editor consensus) |  | "Despite these challenges... continues to thrive" |
| | **Language and grammar** | | | |
| 7 | AI vocabulary words and phrases | Kobak et al. (Science Advances 2025); Juzek & Ward; Reinhart; Merrill (WaPo) | strong_warning | "delve", "landscape", "provide a valuable insight" |
| 8 | Copula avoidance | Geng & Trotta (arxiv 2024) | strong_warning | "serves as", "stands as" instead of "is" |
| 9 | Contrived contrast / negative parallelism | Russell, Karpinska, Iyyer (ACL 2025); Stockton; Kriss/NYT | strong_warning | "It's not X; it's Y" / "It's Y, not X" |
| 10 | Rule of three | Russell; Kriss/NYT; Guo | context_warning | Forcing ideas into triads |
| 10a | Triad density |  | context_warning | The density variant of #10 rule of three: three or more triads in a paragraph or short passage. |
| 11 | Synonym cycling | Belcher (Chronicle); stylometry research |  | "the protagonist... the main character... the central figure" |
| 12 | False ranges | Wikipedia (editor consensus) |  | "from X to Y, from A to B" |
| 53 | Vocabulary diversity |  | context_warning | A coarse type-token ratio metric for prose of 150+ words: low ratios suggest narrow vocabulary. |
| | **Style** | | | |
| 13 | Boldface overuse | Wikipedia (editor consensus); Guo | context_warning | Mechanical bolding of terms that don't need emphasis |
| 14 | Inline-header lists | Wikipedia (editor consensus); Guo; Shankar | strong_warning | Bolded label + colon turning prose into slides |
| 15 | Title case in headings | Russell, Karpinska, Iyyer (ACL 2025); Grammarly | context_warning | "Strategic Negotiations And Global Partnerships" |
| 16 | Emojis in professional content | Wikipedia (editor consensus); Guo | context_warning | Emoji-led bullet points |
| 17 | Curly quotation marks | Wikipedia (editor consensus) | context_warning | "..." instead of "..." |
| 18 | Hyphenated modifier clusters | Wikipedia (editor consensus) | context_warning | 3+ hyphenated compounds in one sentence |
| 49 | Em dashes |  | strong_warning | ChatGPT and similar systems use the em dash (`—`) as default mid-sentence punctuation. |
| | **Communication** | | | |
| 19 | Collaborative artifacts | Wikipedia (editor consensus); OpenAI sycophancy rollback; Guo | hard_fail | "I hope this helps!", "Let me know if..." |
| 20 | Knowledge-cutoff disclaimers | Wikipedia (editor consensus) | strong_warning | "as of my last training update..." |
| 21 | Sycophantic/servile tone | OpenAI sycophancy rollback (April 2025); Kriss/NYT | hard_fail | "Great question!", "You're absolutely right!" |
| | **Filler and hedging** | | | |
| 22 | Filler phrases | Wikipedia (editor consensus); Grammarly; Guo | strong_warning | "In today's fast-paced world", "Generally speaking" |
| 23 | Excessive hedging | Wikipedia (editor consensus); Grammarly; Stanford HAI / Liang et al. | context_warning | "It could potentially possibly be argued..." |
| 23a | False balance or concession | Chiang (via Vollmer); Wikipedia (editor consensus); Abdulhai (adjacent) | strong_warning | "While critics argue..., supporters say...", "the truth lies somewhere in the middle" |
| 24 | Generic positive conclusions | Wikipedia (editor consensus); Shankar; Caroll | hard_fail | "The future looks bright", "Exciting times lie ahead" |
| 25 | Staccato rhythm | Shankar; Guo; Caroll | context_warning | Short sentences at predictable positions |
| 47 | Soft explainer scaffolding |  | strong_warning | "One useful area...", "Another useful area...", "The main strength..." |
| 48 | Dense negation |  | context_warning | Clusters of "is not", "are not", "does not", "isn't", "aren't"... |
| 50 | Formulaic openers |  | strong_warning | "At its core,", "At a foundational level,", "Beyond this..." |
| | **Sensory and atmospheric** | | | |
| 26 | Ghost/spectral language | Kriss/NYT; corpus measurement | context_warning | shadows, whispers, echoes, phantoms |
| 27 | Quietness obsession | Kriss/NYT | context_warning | "quiet" 10 times in 759 words about pebbles |
| 28 | Forced synesthesia | Kriss/NYT |  | "grief tasting of metal", "hands humming with colour" |
| | **Structural tells** | | | |
| 29 | Mid-sentence rhetorical questions | Guo; Kriss/NYT | context_warning | "The solution? It's simpler than you think." |
| 30 | Generic/ungrounded metaphors | Guo; Kriss/NYT; Caroll |  | Plausible but specific to nobody |
| 31 | Excessive list-making | Guo; Shankar | context_warning | Converting prose to bullets unnecessarily |
| 31a | Decorative Unicode | Guo; Wikipedia (editor consensus); corpus | context_warning | Arrows, checkmarks, stars, ornamental bullets, emoji-style symbols in prose |
| 32 | Dramatic narrative transitions | Guo | context_warning | "Something shifted.", "Everything changed." |
| 38 | Section scaffolding | Wikipedia (editor consensus) | strong_warning | "Let's explore...", "Let's dive into..." |
| 42 | Manufactured insight framing |  | strong_warning | "what's really", "the real answer", "here's what's really" |
| 44 | Signposted conclusion |  | context_warning | "In summary,", "In conclusion,", "To summarise,", "To sum up,..." |
| 52 | Sentence rhythm variance |  | context_warning | A coarse rhythm metric for prose of 100+ words: low variance suggests mechanical pacing. |
| | **Voice and register** | | | |
| 33 | Countdown negation | Practitioner guides (aidetectors.io, seoengine.ai, SAGE) | context_warning | "It wasn't X. It wasn't Y. It was Z." |
| 34 | Per-paragraph miniature conclusions | Shankar; practitioner guides | context_warning | Every paragraph wraps up neatly |
| 35 | Tonal uniformity / register lock | Practitioner guides; Caroll; Guo |  | One register throughout, no human drift |
| 35a | Vague 'this/that' starts | Shankar; Vollmer | context_warning | "This highlights...", "This underscores...", "That speaks to..." |
| 35b | Repeated 'This...' chains |  | context_warning | Three or more consecutive sentences beginning with "This [verb]": "This shows... This suggests... This means..." |
| 36 | Faux specificity | Practitioner guides; Caroll; Guo |  | "The smell of coffee on a Sunday morning", specific to nobody |
| 37 | Neutrality collapse | Abdulhai et al. (arxiv 2603.18161) |  | Stripping the author's stance, defaulting to balanced |
| 39 | Placeholder residue | Gmelius (via Vollmer) | hard_fail | `{client_name}`, `[Company Name]`, `[insert date]`, "Hi {name}" |
| 40 | Rubric echoing | Vollmer | context_warning | "the author creates a tone", "I can tell because", "this quote shows that" |
| 41 | Genre-specific manual checks | Walsh (arxiv 2024); Clarke/Clarkesworld; Vollmer; genre-survey synthesis |  | Genre-aware self-audit (academic / student essay / poetry / fiction). |
| 43 | Corporate AI-speak |  | strong_warning | "delivering impact", "measurable outcomes", "scalable, production-grade" |
| 45 | Nonliteral land/surface phrasing |  | strong_warning | "the argument lands", "the idea lands", "your point lands" |
| 46 | Bland critical template |  | strong_warning | "the kind of contemporary novel/film/book/album/show that..." |
| 51 | Mechanical repeated sentence starts |  | context_warning | Three or more consecutive sentences whose first word matches: "The X… The Y… The Z…" |
| | **Aggregate AI-signal pressure** | | | |
| | AI pressure from stacked signals | | context_warning | Stacked weak signals reaching the threshold (e.g., "headings in prose, assistant residue, generic conclusion") |

Density and stacking matter more than any single occurrence. The grader's `overall-ai-signal-pressure` check fires when several weaker patterns appear together; that is usually a stronger signal than any individual flag.

## Agent-judgement readings

Eight semantic items the regex grader cannot see. The Audit action runs each one as a small reading and returns a binary status. Source: `humanise/scripts/judgement.json`.

| Item | Pattern ref | Schema |
| --- | --- | --- |
| Structural monotony |  | trichotomy |
| Tonal uniformity | #35 | state |
| Faux specificity | #36 | list |
| Neutrality collapse | #37 | trichotomy |
| Even jargon distribution |  | trichotomy |
| Forced synesthesia | #28 | list |
| Generic metaphors | #30 | list |
| Genre-specific watchlist | #41 | composite |

## Where to be careful

- **Genre matters.** Persuasive how-to, business memo, literary essay, and journalistic reportage all use patterns this skill flags. Audit output is calibrated to spot AI overuse; legitimate technique is not the target. Treat each flag as something to review.
- **Patterns drift.** AI vocabulary lists go stale ("delve" peaked in 2023–24). The catalogue needs periodic refresh.
- **The skill itself is an LLM.** It can introduce the patterns it is trying to catch (neutrality collapse, pronoun depletion, generic substitution). The semantic-preservation step in the rewrite flow mitigates this but cannot eliminate it.
- **Detection is asymmetric.** The skill catches AI doing patterns badly. It can also wrongly flag humans doing the same patterns well. The audit voice tries to make this distinction visible; the user has to apply judgement.
- **Sample sizes are small.** Findings here are based on a 15-sample matched corpus (5 human + 5 AI fresh + 5 AI rewrite). Treat them as directional at this sample size.

## What's next

The grader reads from a registry, the audit pairs eight agent-judgement readings with the regex pass, and the report renders in two layers. Active work, with open questions tracked in `dev/hypotheses.md`:

- Reframing the audit voice so flagged patterns read as *review priorities* rather than verdicts.
- Calibrating thresholds by register (literary essay vs corporate doc vs news copy).
- Adding new candidate signals (sentence-length mean, ghost-spectral density, negation density, unicode flair) where evidence supports them.
- Demoting pattern checks that do not separate humans from AI in matched genres (em dashes, manufactured insight, and triad density may belong in softer categories).
- Growing the matched corpus past N=5 per group.
- Closing two grader-integrity gaps catalogued in `docs/todos/grader-integrity-gaps.md`: 17 catalogued patterns without programmatic checks (Group A) and 8 grader checks without catalogued patterns (Group B).

## File structure

```
humanise/                          Skill (this is what gets installed)
├── SKILL.md                       Main skill instructions
├── scripts/                       Grader + registry loaders
│   ├── grade.py                   Grading script (49 checks)
│   ├── registries.py              Loaders for the three JSON registries
│   ├── patterns.json              Pattern catalogue (severity, category, report text)
│   ├── judgement.json             Eight-item agent-judgement registry
│   ├── vocabulary.json            Severity / action labels and depth consequences
│   └── contracts/                 Audit JSON contract schema
└── references/                    Patterns, alternatives, severity, voice, process

dev/                               Development only (not installed)
├── evals/                         Eval suite, samples, harness
│   ├── evals.json                 18 eval cases (audit / suggest / rewrite / write)
│   ├── corpus.json                Genre-paired comparative-baseline corpus
│   ├── run_skill_creator_iteration.py
│   └── samples/{human-sourced,generated-ai}/
├── research/                      Findings and source-pattern analysis
├── tools/                         Generators (e.g., render_patterns_md.py)
└── skill-workspace/iteration-N/   Iteration outputs and review viewers
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
- Brian Phillips, ["The em-dash defence"](https://www.theringer.com/) (The Ringer 2025; dissenting view)
- Wendy Belcher, ["10 Ways AI Is Ruining Your Students' Writing"](https://www.chronicle.com/article/10-ways-ai-is-ruining-your-students-writing) (Chronicle of Higher Education 2025)
- Hua Hsu, ["What college students lose when ChatGPT writes their essays"](https://www.newyorker.com/) (New Yorker; WNYC Brian Lehrer)
- Karolina Rudnicka, ["Each AI chatbot has its own, distinctive writing style"](https://www.scientificamerican.com/article/chatgpt-and-gemini-ai-have-uniquely-different-writing-styles) (Scientific American 2025)
- Slate (2025): paranoia-spiral coverage of writers introducing typos to signal humanity
- Jonathan Bailey, "Plagiarism Today" (2025): six-model em-dash test
- PBS NewsHour / Futurism: CNET (77 AI finance articles, 2023) and Sports Illustrated (AI bylines, AI headshots)

**Practitioner essays and writer blogs:**
- Linda Caroll, ["Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (experiential vacancy, "warm fuzzies")
- Charlie Guo, ["The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (rhetorical questions, metaphors, list-making, transitions; coined "AI slop")
- Shreya Shankar, ["AI Writing"](https://sh-reya.com/blog/ai-writing/) (orphaned demonstratives, bullet-point fetish)
- Blake Stockton, ["Don't Write Like AI" series](https://blakestockton.com/dont-write-like-ai-1-101-negation) (negative parallelism)
- Vauhini Vara, ["Confessions of a Viral AI Writer"](https://www.wired.com/story/confessions-of-a-viral-ai-writer-llms/) (Wired 2023); *Searches: Selfhood in the Digital Age* (Pantheon 2025)
- Laura Preston, ["HUMAN_FALLBACK"](https://www.nplusonemag.com/issue-44/essays/human_fallback/) and ["An Age of Hyperabundance"](https://www.nplusonemag.com/) (n+1; "collapse of context")
- Ted Chiang, ["ChatGPT Is a Blurry JPEG of the Web"](https://www.newyorker.com/tech/annals-of-technology/chatgpt-is-a-blurry-jpeg-of-the-web) (New Yorker 2023); ["Why A.I. Isn't Going to Make Art"](https://www.newyorker.com/) (2024)
- Robin Sloan, [robinsloan.com](https://www.robinsloan.com/) (partnership framing for human-AI writing)
- Sean Trott, [seantrott.substack.com](https://seantrott.substack.com) (LLM signature analysis)
- Aranya, ["Poetly"](https://poetly.substack.com) (Substack; AI poetry tells beyond Walsh)
- David J. Germain, [Medium](https://medium.com/) (parenthetical stage-directions in GPT-3.5 dialogue)
- Brent Csutoras, [Medium](https://medium.com/) (em-dash training-corpus mechanism)
- Fred Rohrer, [blog.frohrer.com](https://blog.frohrer.com/) (promotional register, n-gram analysis)

**Vendor and first-party:**
- OpenAI: [GPT-4 System Card](https://cdn.openai.com/papers/gpt-4-system-card.pdf); April 2025 [sycophancy rollback](https://openai.com/index/sycophancy-in-gpt-4o/); GPT-5.1 em-dash suppression
- Anthropic: [Claude Sonnet system prompts](https://platform.claude.com/docs/en/release-notes/system-prompts)
- [GPTZero](https://gptzero.me/ai-vocabulary) (AI Vocabulary list; perplexity and burstiness model)
- [Grammarly](https://www.grammarly.com/blog/ai/common-ai-words/) (31 indicator words and phrases)
- [Gmelius](https://gmelius.com/blog/can-customers-tell-an-email-is-written-using-generative-ai) (catalogue of "AI-isms" in email)
- Bynder (2024 consumer study; 55% of US consumers correctly identify AI marketing)
- Pangram, Copyleaks, ZeroGPT, Originality.AI, NetusAI, Turnitin (commercial detector landscape, referenced for context; humanise is not a detector)

**Practitioner guides referenced for detection thresholds:**
- [AI Detectors: How to tell if text is AI written](https://www.aidetectors.io/blog/how-to-tell-if-text-is-ai-written)
- [SEO Engine: Signs of AI writing](https://seoengine.ai/blog/signs-of-ai-writing)
- [SAGE: AI detection for peer reviewers](https://www.sagepub.com/explore-our-content/blogs/posts/sage-perspectives/2025/06/11/ai-detection-for-peer-reviewers-look-out-for-red-flags)
- Hastewire (student writing detection signals)
- Copy Posse (LinkedIn tricolon armature; business-email tells)
- AI for Lifelong Learners (Substack; five-paragraph-essay shape, machine cleanliness)

## Licence

[MIT](LICENCE)
