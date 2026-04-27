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
3. Groups failures by failure mode and severity, then separates check status from Light/Medium/Hard actions
4. Rewrites flagged sections: structural patterns first (repetitive section arcs, tonal flatness, neutralised stance), then surface patterns (AI vocabulary, formatting, filler)
5. Checks the rewrite didn't strip the author's stance or voice
6. Runs a non-programmatic structural self-audit covering patterns the script can't detect (tonal uniformity, section monotony, stance preservation, resolution density)
7. Re-runs the grading script and revises according to mode: Hard aims for clean pass; Medium and Light fix hard failures and strong warnings; context warnings may remain only with disclosure
8. Returns the rewrite with a transparent report of what changed, what remains flagged, and what needs the user's decision

Failure modes currently used in reports: provenance residue, synthetic significance, frictionless structure, generic abstraction, voice erasure, and genre misfit. A failed check remains a failed check in every mode; the mode decides whether to fix it, disclose it, or ask the user.

## Representative report output

Excerpt from a blind-agent Hard-mode run against `dev/evals/samples/generated-ai/ai-08-feedback-education.md`, followed by an independent direct grade of the agent's final rewrite.

```text
Mode selected: Hard. The user requested Hard mode, so every failed check had to be fixed rather than preserved.

Pre-check report
Score summary: fail, 5/43 checks failed, pass rate 38/43. AI-signal pressure: 4/4, triggered. Components: paragraph_uniformity, markdown_headings. Severity counts: context_warning 5.

Triggered checks
- overall-ai-signal-pressure, context_warning. Evidence: Overall AI-signal pressure 4/4 from paragraph_uniformity and markdown_headings; vocabulary pressure 0 points, worst_generic 1, GPTZero matches none, Kobak sample: need, analysis, involves, strategies, valuable. Failure modes: generic_abstraction, frictionless_structure. Hard action: fix.
- no-markdown-headings, context_warning. Evidence: Found 2 heading(s): "# Why Feedback Matters in Learning", "# Why Feedback Matters in Learning". Failure modes: frictionless_structure, genre_misfit. Hard action: fix.
- no-negation-density, context_warning. Evidence: Found 10 negation markers, 12.4 per 1000 words. Failure modes: frictionless_structure, genre_misfit. Hard action: fix.
- paragraph-length-uniformity, context_warning. Evidence: Paragraph length CV 0.08 across 10 paragraphs, target at least 0.18. Failure modes: frictionless_structure. Hard action: fix.
- no-triad-density, context_warning. Evidence: Found 12 triads, including "feedback as a grade, a correction, a short comment written", "learn to seek it, interpret it, use it", and "in time for revision, reflection, goal setting". Failure modes: frictionless_structure, genre_misfit. Hard action: fix.

Failure-mode summary
- generic_abstraction: overall-ai-signal-pressure
- frictionless_structure: overall-ai-signal-pressure, no-markdown-headings, no-negation-density, paragraph-length-uniformity, no-triad-density
- genre_misfit: no-markdown-headings, no-negation-density, no-triad-density

Structural self-audit:
- Section arcs: 8/10 original paragraphs followed the same explainer template. I removed the title packaging, varied paragraph length, and changed several paragraphs from general claim plus explanation into example-led or instruction-led paragraphs.
- Resolution density: 5/10 original paragraphs ended with a tidy mini-conclusion. I cut or loosened several closers, especially around timing, peer feedback, and action.
- Register breaks: Added "At first this can feel artificial. That is fine." and "wastes everybody's time" to break the neutral article register.
- Triads: 12 found in the original, reduced to 6 in the draft, then 2 in the final by turning list structures into pairs or single concrete examples.
- Reframe laundering: none.
- Purposeful devices recommended for preservation: none.
- Stance: preserved. The original argued that feedback should guide improvement, arrive in time to be used, and lead to student action. The rewrite keeps that position.
- Remaining tells: Draft still had too many triads, so I revised again.

Final rewrite:
Feedback helps only when students can do something with it. Too often, it arrives as a score or a sentence in the margin after the work is already over. A student sees 68 percent and knows the essay met part of the standard, but the number does not tell them where the next draft should change.

Useful feedback points to the next move. Instead of writing "needs more detail," a teacher might mark the second paragraph and say, "Add one example here so the claim has something to rest on." That comment gives the student a place to start. It also keeps the problem inside the work, where it belongs.

Timing matters more than teachers sometimes want it to, because late comments are easy for students to file away and forget. Feedback has the best chance of changing learning while the student is still drafting or revising. That might mean a quick note on a plan, a conversation during class, or a low-stakes quiz before the final version is due.

Students also need a clear picture of the target. Rubrics can help, but a rubric full of phrases like "strong analysis" will not carry much by itself. Show students two answers, talk through why one is clearer, and let them try the judgement themselves. The goal is for them to recognise quality before someone else points it out.

The emotional part is real. Even accurate criticism can sting, especially for students who already doubt themselves. Honest feedback still matters; soft praise that hides the problem wastes everybody's time. The trick is to keep the task possible: name something that works, choose the most important issue, then give a step the student can attempt today.

Students can learn to ask better questions about their own work. "Is this good?" usually leads to a vague answer. "Where does my argument become hard to follow?" gives the teacher, or a classmate, something useful to answer.

Peer feedback needs training. Left alone, students often become too blunt or too polite, and both versions are unhelpful. Give them a narrow job, such as finding the strongest sentence and one place where the reader gets lost. At first this can feel artificial. That is fine. The structure is temporary support while students learn what useful comments sound like.

Feedback should end in action. Build in ten minutes for students to revise a paragraph, write a short plan, or correct an error pattern. Without that time, comments become a receipt for work already done.

The larger aim is judgement. Students start to notice the habits in their own writing and problem solving. They learn which mistakes keep returning and which fixes actually help. A grade can report performance. Feedback should teach students how to improve the next attempt.

Post-check report:
Score summary: pass, 0/43 checks failed, pass rate 43/43. AI-signal pressure: 0/4, not triggered. Components: none. Severity counts: none.
Fixed: overall-ai-signal-pressure, no-markdown-headings, no-negation-density, paragraph-length-uniformity, no-triad-density.
Remaining hard failures: none.
Remaining strong warnings: none.
Remaining context warnings: fixed.
Check status: pass, 0/43 checks failed.
Light action: no required fixes, no preserved warnings, no user decisions.
Medium action: no required fixes, no preserved warnings, no user decisions.
Hard action: no required fixes.

Independent direct grade of the final rewrite:
pass_rate: 43/43
failures_by_severity: {}
ai_signal_pressure: 0/4, not triggered
triggered_checks: []
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
