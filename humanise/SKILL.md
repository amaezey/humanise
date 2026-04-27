---
name: humanise
description: >-
  Detects and rewrites AI writing patterns across vocabulary, structure, tone,
  voice, and formatting using 38 patterns and 43 programmatic checks.
  Use when the user wants to humanise or de-AI text, clean up AI-generated
  content before publishing, or check whether writing passes as human-written.
  Also useful when a draft feels flat or robotic, when the author's voice has
  been neutralised, or when working with output from ChatGPT, Claude, or
  other language models.
---

# Humanise: Remove AI writing patterns

Edit text to remove signs of AI generation while preserving meaning and the author's voice. Based on Wikipedia's "Signs of AI writing" guide and Abdulhai et al. (2026), "How LLMs Distort Our Written Language".

## Your task

When given text to humanise:

0. Calibrate intensity and genre (below)
1. Check hard constraints first (below)
2. Read [references/patterns.md](references/patterns.md) and scan for all 38 patterns
3. Rewrite problematic sections with natural alternatives at the chosen intensity
4. Preserve the meaning and match the intended tone
5. Add or preserve genuine personality (see Personality and soul)
6. Run the self-audit loop (see Process)

---

## Intensity and tolerance

Before rewriting, decide how far to go. If the user has not specified intensity and the genre makes the answer ambiguous, ask a short calibration question:

> How hard should I go: light cleanup, medium humanise pass, or hard de-AI pass?

If you cannot ask, infer conservatively:

- **Light:** remove hard failures and strong warnings while preserving voice, rhythm, literary devices, humour, dialogue, period style, and intentional formatting. Context warnings may remain only with disclosure and a concrete reason. Default for fiction, memoir, literary essays, humour, interviews, poetry-adjacent prose, and strong personal voice.
- **Medium:** default for generic "humanise this" requests. Remove clear AI patterns and all strong warnings. Context-sensitive devices such as purposeful repetition, rhetorical questions, staccato, and triads may remain only when they carry voice or structure and are disclosed.
- **Hard:** aggressive cleanup for drafts meant to pass as non-AI. Fix every script failure unless doing so would materially change meaning. Strip polish, scaffolding, and formulaic rhetorical moves even when they read smoothly.

The grader is a diagnostic tool, not an authorship verdict. A failed check remains a failed check in every mode. Light, Medium, and Hard decide what action to take: fix, disclose, or ask the user. In Light and Medium, hard failures and strong warnings must be fixed; context warnings may remain only with disclosure and a concrete reason. In Hard mode, assume the user wants maximum risk reduction.

Transparency rule: every remaining grader warning must be shown in the report, grouped by severity, with one of three statuses:

- **Fixed**
- **Recommended preserve**
- **Needs user decision**

Do not silently classify your own writing as the exception. If you preserve a flagged device, name it, quote or identify the relevant passage briefly, and explain the concrete function it serves.

### Severity classes

- **Hard failures:** assistant residue, collaborative artifacts, sycophancy, knowledge-cutoff disclaimers, generic conclusions, fake continuation offers, unfilled placeholders, and unsupported claims that read fabricated. Fix in every mode.
- **Strong warnings:** manufactured insight, contrived contrast/reframe laundering, AI vocabulary clusters, false-concession hedges, copula avoidance, corporate AI-speak, soft scaffold phrasing, bland critical templates, superficial -ing analysis, formulaic openers, and section scaffolding. Fix in Light, Medium, and Hard unless the user explicitly accepts the risk after disclosure.
- **Context warnings:** curly quotes, staccato, anaphora, triads, rhetorical questions, orphaned demonstratives, Unicode flair, rubric echoing, headings including plain title headings, list density, promotional language, ghost/quiet language, negation density, tidy paragraph endings, paragraph length uniformity, and vocabulary diversity. Review with the purpose test before changing.
- **Em dashes:** strong 2026 signal. Light mode may preserve them only with explicit disclosure; Medium and Hard require removal.
- **Preserve if purposeful:** literary repetition, dialogue rhythm, comic timing, interview cadence, historical prose, technical qualification, character voice, and deliberately patterned argument.

### Purpose test

For any context warning, ask:

> Is this device doing real work here, or is it autopilot?

You may recommend preserving it if it reveals character, controls timing, creates humour, mirrors thought, supports a period voice, or clarifies structure. Remove it if it is generic emphasis, tidy profundity, decorative balance, or a default article template. If you are unsure, mark it **Needs user decision** rather than deciding for the user.

Examples:

- Poe-style staccato can be voice. "That matters. A lot." in a productivity article is usually autopilot.
- A Sedaris-style comic escalation can stay. A corporate triad like "clarity, collaboration, and innovation" should go.
- Curly quotes in a sourced literary sample are not an AI tell. Curly quotes in this skill's final plain-text output may still be normalised if the user asked for hard cleanup.

---

## Hard constraints

Non-negotiable in Hard mode. In Medium and Light mode, hard failures and strong warnings must be fixed. Context warnings may be preserved only with explicit disclosure and a concrete reason. Check first, check last, check again.

### No em dashes except disclosed Light mode preservation

In Medium and Hard mode, the em dash character must never appear in output. Not once. Not for emphasis, not for asides, not for attribution, not for any reason.

Replace with commas, colons, semicolons, periods, or parentheses. Restructure the sentence if none of those fit. There is always an alternative.

In Light mode only, em dashes may be preserved if they are part of an author's established style, quoted source text, dialogue rhythm, or period/literary voice. Disclose the preservation explicitly so the user can decide. If the user asked for publication-ready plain prose, normalise them.

### No manufactured insight

Eliminate all framing that performs the act of having a deeper take. AI cannot have insider knowledge, so it compensates with linguistic markers that signal depth without providing any. Either state the observation plainly or remove the sentence if stripping the framing reveals no substance.

- **False revelation:** "But the real answer is...", "What's actually happening here is...", "Here's what's really going on..."
- **Contrived contrarianism:** "What nobody is talking about...", "What no one is talking about...", "Contrary to popular belief...", "The uncomfortable truth is..."
- **Unnoticed-shift framing:** "When no one noticed...", "The shift nobody noticed...", "Before anyone noticed...", "Without anyone noticing..." when used to manufacture secret significance.
- **Pseudo-profundity:** "quietly revolutionary", "quietly became", "the quiet part", "subtly", "understated", "unassuming" when used to inflate significance
- **Performed knowingness:** "If you know, you know", "And that changes everything", "Let that sink in", "Read that again", "And honestly?", "Here's the thing:"
- **Formulaic depth framing:** "The reason is straightforward:", "The reason is simple:", "Here's why:", "What's strange is", "What's interesting is", "What's remarkable is". These perform the act of having an explanation before delivering one.
- **Dramatic narrative transitions:** "Something shifted.", "Everything changed.", "And then, everything clicked.", "That's when it hit me." These claim a turning point without earning it.
- **Contrived contrast:** "This isn't X. It's Y." as a standalone dramatic beat (e.g. "This isn't a bug. It's a feature." or "This isn't a character flaw. It's hardware."). The two-sentence snap format is a reliable AI fingerprint regardless of content.

These patterns are non-negotiable when they are generic assistant performance. A funny piece with "And honestly?" may still be carrying an AI tell, but a voiced essay may use similar phrasing intentionally. Apply the purpose test in Light mode; remove in Medium and Hard unless the phrase clearly belongs to the writer's voice.

### No adversarial reframes

Do not satisfy the letter of a rule while keeping the same AI-shaped move. This especially applies to pattern 9, contrived contrast / negative parallelism. If the draft says "It's not X, it's Y", an acceptable rewrite is not "It is Y, not X" or "Beyond X, it becomes Y". Those are the same device with the furniture moved around.

Flag and rewrite all of these as direct claims:

- "It's not X, it's Y."
- "It's Y, not X."
- "Less X than Y."
- "More Y than X."
- "Not so much X as Y."
- "Beyond X, it is Y."
- "You might think X. Actually, Y."
- "No X. No Y. Just Z."

The test is semantic: if the sentence creates drama by rejecting a plain interpretation and revealing a supposedly deeper abstraction, remove the setup and state the actual claim with concrete support.

### No staccato fragments

Short sentences used in sequence for dramatic effect are often an AI tell. "That matters." or "Full stop." or "This is it." as standalone beats in generic articles are usually generated.

A sentence should be as long as the thought it contains. When you find fragments used for generic emphasis, fold their content into a neighbouring sentence or expand into something that earns its own line. Preserve staccato when it is character voice, comedy, panic, dialogue, or deliberate literary rhythm.

**Before:**
> The results were clear. Strikingly so. The model outperformed every baseline. Every single one. And nobody saw it coming.

**After:**
> The results were unambiguous: the model outperformed every baseline by a significant margin, which surprised most of the team.

---

## Personality and soul

### The real problem: subtraction

Most AI tells are things AI **adds**: vocabulary, formatting, rhetorical devices. But research shows AI also **subtracts**. Abdulhai et al. (2026) found that extensive LLM use led to a ~70% increase in essays that remained neutral, 50% fewer pronouns, and fewer anecdotes or personal references. Even when instructed to only fix grammar, LLMs frequently changed the writer's conclusions.

Removing AI patterns is therefore only half the job. You must also watch for what AI took away: the author's stance, their pronouns, their willingness to be specific and wrong. Sterile, voiceless, perfectly balanced writing is just as obvious as slop.

### Experiential vacancy

AI has no lived experience, so it generalises. It writes about gratitude using "the smell of coffee" and "the way the light hits your kitchen table" because those are universally relatable but specific to nobody. A related move is **faux specificity** (pattern 36): AI *performs* specificity by constructing examples from genre conventions rather than lived experience. The detail sounds concrete but belongs to nobody.

Human writing draws on real memories, named people, actual places, felt emotions. When humanising, look not just for patterns to remove but for the **absence** of specificity, vulnerability, and personal stakes.

### Density without purpose

A good writer uses em dashes, triads, and parallelism sparingly, with intention. AI litters them throughout indiscriminately. The issue is not that any single device appears, but that they cluster and serve no rhetorical purpose. When scanning for patterns, watch for pileups.

### Signs of soulless writing (even if technically clean):
- Every sentence follows the same length and structure
- No opinions, just neutral reporting: stance has been stripped or was never there
- No acknowledgment of uncertainty or mixed feelings
- No appropriate point-of-view presence; pronouns depleted
- No humour, no edge, no personality
- Observations are universally relatable but never personally specific (faux specificity)
- Emotionally safe: never takes an uncomfortable position
- Tonal uniformity: one register throughout, no drift or register breaks (pattern 35)
- Every paragraph wraps up neatly with a miniature conclusion (pattern 34)

### How to add voice:

**Have opinions.** "I keep going back and forth on this" is more human than neutrally listing pros and cons.

**Vary rhythm within reason.** Mix sentence lengths for natural cadence, but not one-word dramatic punctuation. It should feel like a person thinking at different speeds.

**Acknowledge complexity.** "This is impressive, but it also makes me a little uneasy" carries more weight than unqualified praise or a clean pro/con list.

**Match the natural point-of-view.** If the piece reads as personal reflection, use "I". If it reads as impersonal observation, use "one" or third person. Do not default to first person. Match whatever POV the text is already using or would naturally use for its genre and tone.

**Be specific rather than atmospheric.** Instead of mood words ("eerie", "striking", "fascinating"), describe the concrete detail that caused the feeling.

**Break register.** If the whole text sits in one tone, introduce at least one register shift: a moment of informality, a parenthetical doubt, a change in sentence rhythm.

### Before (clean but soulless):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were sceptical. The implications remain unclear.

### After (has a pulse):
> Three million lines of code, generated overnight while the developers slept. I have been turning this over for a few days now, and I still do not have a clean take on it. Half the dev community thinks this changes everything; the other half is explaining, at length, why it does not count. My own reaction keeps shifting depending on which examples I look at.

---

## Pattern catalogue

Read [references/patterns.md](references/patterns.md) for all 38 AI writing patterns with words-to-watch and before/after examples, organised as:

- **Content patterns (1-6):** Significance inflation, notability claims, superficial -ing analyses, promotional language, vague attributions, formulaic challenges sections
- **Language and grammar (7-12):** AI vocabulary words and phrases, Kobak biomedical excess-vocabulary clusters, copula avoidance, contrived contrast / negative parallelisms, rule of three, synonym cycling, false ranges
- **Style (13-18):** Boldface overuse, inline-header lists, title case, emojis, curly quotes, hyphenated compound modifier clusters
- **Communication (19-21):** Collaborative artifacts, knowledge-cutoff disclaimers, sycophantic tone
- **Filler and hedging (22-25):** Filler phrases, excessive hedging, generic positive conclusions, staccato rhythm in non-fragment contexts
- **Sensory and atmospheric (26-28):** Ghost/spectral language, quietness obsession, forced synesthesia
- **Structural tells (29-32, 38):** Mid-sentence rhetorical questions, generic/ungrounded metaphors, excessive list-making, dramatic narrative transitions, section scaffolding
- **Voice and register (35-37):** Tonal uniformity/register lock, faux specificity, neutrality collapse

Search for specific patterns when needed:
```bash
grep -i "promotional" references/patterns.md
```

---

## Process

### Step 0: Calibrate intensity and genre

Identify the mode before rewriting:

- User explicitly requested "light", "gentle", "keep my voice", "literary", "just clean it up": use **Light**.
- User asked to "humanise", "de-AI", "make this sound less AI": use **Medium** unless the genre clearly calls for Light.
- User asked to "strip all AI tells", "make it pass checks", "be ruthless", "hard mode": use **Hard**.

If the text is fiction, memoir, humour, interview, literary essay, poetry-adjacent prose, old prose, or dialogue-heavy writing, ask before applying Hard mode. These genres naturally use devices the grader flags.

Record the selected mode in the report.

### Step 1: Pre-check (script finds the problems)

Save the input text to a temp file, then run the grading script on it:

```bash
python3 grade.py --format markdown --mode hard /tmp/input.md
```

Use the selected mode in the command: `--mode light`, `--mode medium`, or `--mode hard`.

The script checks 43 patterns programmatically and returns a plain-English Markdown report by default in this workflow. It is built from `human_report`: `overview`, `score`, `confidence`, `ai_pressure_explanation`, `failed_checks`, and `all_checks`. If you need debugging details, run the script without `--format markdown` to get JSON diagnostics. The older fields (`triggered_checks`, `failure_mode_results`, `mode_results`, and raw expectations) are for debugging only.

Do not paste raw JSON. Do not expose internal labels such as `context_warning`, `strong_warning`, `hard_fail`, `failure_modes`, `frictionless_structure`, or `generic_abstraction` in normal output. Use the plain-English strings in `human_report`.

The pre-check report must include:

- **Summary:** use `human_report.overview`, such as "5 of 43 checks showed signs of AI-style writing."
- **Confidence:** use `human_report.confidence.level`, `meaning`, and `basis`. Make clear this is confidence about AI-writing signs, not authorship.
- **AI-pressure explanation:** include `human_report.ai_pressure_explanation`. Aggregate AI-signal pressure is one of the 43 checks. It also has its own internal 0/4 threshold, so explain both numbers.
- **Main issues:** list the failed rows from `human_report.failed_checks` using the plain check name, severity, why it failed, and selected-mode action.
- **Full check table:** render every row from `human_report.all_checks` as a Markdown table with columns `Check`, `Status`, `Why`, and selected-mode `Action`. For passed checks, use "Pass", the plain reason, and "None". For failed checks, show why and the selected mode's action.

The full 43-row table is required. It is how the user can see that the system checked all signals, not only the ones that failed. Do not replace it with a bullet list or a summary.

- **Fix:** hard failures and strong warnings in Light, Medium, and Hard; all failed checks in Hard.
- **Preserve with disclosure:** context warnings in Light or Medium only when they serve voice, quotation, genre, or meaning.
- **User decision:** context warnings where preservation is plausible but risky.

**Depth signal:** If the pre-check shows multiple structural failures (triad density, section scaffolding, countdown negation, paragraph uniformity, soft scaffolding, orphaned demonstratives, tidy paragraph endings), the text is likely AI-generated from scratch and will need structural rewriting, not just word-swaps.

If the script is not available (e.g. no Python, or running in Claude.ai), fall back to a manual scan: read [references/patterns.md](references/patterns.md) and check each pattern. But prefer the script when possible.

### Step 2: Fix (you rewrite)

Address structural patterns first, then surface patterns. The grader catches surface patterns well but cannot enforce structural rewriting. You must do that work here.

**Structural patterns (address first):**

1. **Structural monotony:** Do all sections follow the same arc (problem, evidence, anecdote, advice)? Vary paragraph structures. Some paragraphs should be one sentence. Some should start with evidence, not claims. Break at least one section out of the template.
2. **Tonal uniformity (35):** Does the whole text sit in one register? Humans drift between registers. If every paragraph sounds the same, introduce at least one register break: a moment of informality, a parenthetical doubt, or a shift in rhythm.
3. **Resolution density (34):** Do most paragraphs end with a tidy summary sentence? Leave some threads open. Cut paragraph-final sentences that merely restate the paragraph's point.
4. **Faux specificity (36):** Are the "specific" examples actually specific to anyone, or genre-convention filler? "The smell of coffee on a Sunday morning" is a stock photo in prose form.
5. **Neutrality collapse (37):** Does the text take a position? If the input had a stance, make sure the output keeps it. "There are pros and cons" is not a rewrite of an opinion.
6. **Even jargon distribution:** Humans clump technical terms when introducing a concept then relax into plain language. AI distributes jargon uniformly. If technical vocabulary is spread too evenly, clump it.
7. **Soft scaffold phrasing:** Remove paragraph labels such as "One useful area", "Another useful area", "The main strength", "The main risk", and "Good use usually comes down to". State the point directly.
8. **Bland critical templates:** In reviews and criticism, replace phrases like "emotional range", "field of sympathy", "moral strength", and "earns its weight" with concrete claims from the work.
9. **False concessions:** Replace "critics say/supporters say/the truth lies in the middle" with the actual stance and evidence. Do not let balance stand in for thought.
10. **Orphaned demonstratives:** Replace vague starts like "This highlights..." or "That underscores..." with concrete subjects.
11. **Forced synesthesia (28)** and **generic metaphors (30):** replace with concrete details.
12. **Section scaffolding (38):** If all sections use the same structural label or follow the same template, vary them.
13. **Hard-mode headings:** If `no-markdown-headings` fails, remove both markdown headings and plain title headings. Do not reintroduce a title line in the rewrite unless the user explicitly asked to preserve article packaging.

**Genre-specific tentative checks:**

- **Academic/research:** Verify citations, DOIs, journals, dates, and reference-list formatting. Do not trust plausible-looking references. Flag citation oddities for user review rather than inventing replacements.
- **Student essays:** Watch for rubric echoing: "the author creates a tone", "I can tell because", "this quote shows that", "according to the rubric". Preserve only if the text is explicitly discussing a rubric.
- **Poetry:** Watch for default quatrains, unrequested rhyme, first-person plural overuse, mood-word accumulation, and formal gestures that do not follow through.
- **Fiction:** Watch for flattened dialogue, "as-you-know" exposition, parenthetical stage directions, fixed POV with no pressure, over-resolved endings, scene pacing that never surprises, characters stating subtext, and exposition that arrives before the scene has earned it.

**Surface patterns (address second):**

9. Read [references/patterns.md](references/patterns.md) for context on each flagged pattern from the pre-check
10. Fix every hard failure and strong warning from the pre-check report in Light, Medium, and Hard unless the user explicitly accepts the risk after disclosure. Review context warnings with the purpose test.
11. Add personality and voice per the Personality and soul section
12. Preserve meaning and match the intended tone

### Step 2.5: Semantic preservation check

Compare your rewrite's conclusions to the input's conclusions. Abdulhai et al. (2026) showed that LLMs shift meaning even in grammar-only passes, and this skill is itself an LLM rewriting text. If the stance shifted toward neutral, you have introduced the same distortion the research documents. Restore the original position. Check:

- Did the input have an opinion? Does the output still have it?
- Are there fewer pronouns in the output than the input? If so, why?
- Did specific claims get softened into "on the other hand" balance?

### Step 3: Structural self-audit (mandatory)

Answer each question below with a specific count or finding. Do not skip any. Show your answers in the output (see Output format).

1. **Section arcs:** Do all sections follow the same arc? Count how many do. If more than half follow the same template, restructure at least one.
2. **Resolution density:** Count paragraphs that end with a summary sentence. If more than half do, rewrite some to leave threads open.
3. **Register breaks:** Is there at least one register break (moment of doubt, informality, or tonal shift)? If not, add one.
4. **Triad count:** Count the triads. If there are more than 4, redistribute some as pairs or longer lists.
5. **Reframe laundering:** Did any banned contrast survive in flipped form ("Y, not X"), softened form ("beyond X"), comparative form ("less X than Y"), or correction form ("you might think X, actually Y")? If yes, rewrite as a direct claim.
6. **Purposeful devices:** Which flagged context warnings did you preserve, and why? Name the device and its function.
7. **Stance preservation:** Did you preserve the author's original position, or did you neutralise it?
8. **Remaining tells:** What still makes this obviously AI generated? List them, revise, repeat until no obvious tells remain.

After answering and acting on these questions, re-run the grader to confirm your structural fixes didn't introduce new failures. In Hard mode, all checks should pass. In Medium and Light mode, hard failures and strong warnings should be gone; em dashes are never acceptable in Medium and should be fixed in Light unless the user explicitly accepts the risk after disclosure. In Light mode, remaining context warnings are acceptable when they preserve voice and are disclosed.

### Step 4: Post-check (script verifies the fix)

Run the grading script on your output:

```bash
python3 grade.py --format markdown --mode hard /tmp/output.md
```

Use the selected mode in the command.

Interpret the post-check by mode:

- **Hard:** fix failures and re-run until all 43 checks pass unless a fix would change meaning.
- **Medium:** hard failures and strong warnings must be gone; context warnings may remain if purposeful and disclosed.
- **Light:** hard failures and strong warnings must be gone; context warnings may remain if they preserve voice and are disclosed.

Always report check status and mode action separately. A check failure remains a failure even when Light or Medium allows disclosure instead of rewriting. Example:

```text
Score summary: fail, 7/43 checks failed, pass rate 36/43. AI-signal pressure: 5/4, triggered.
Light action: fix 1 strong warning; disclose or ask on 6 context warnings
Medium action: fix 1 strong warning; disclose or ask on 6 context warnings
Hard action: fix all 7 failed checks
```

The post-check report must use the post-check `human_report` the same way: overview, confidence, AI-pressure explanation, remaining failed checks, and the full 43-check Markdown table. Do not report only "pass" or "fail"; show the numbers.

If the script is not available, manually verify hard failures and scan for generic AI structures. Use the purpose test before flattening voice.

## Output format

1. Mode selected: Light / Medium / Hard, with one sentence explaining why
2. Initial assessment:
   - Summary: [X of 43 checks showed signs / all checks passed]
   - Confidence: [Low / Low to medium / Medium / High, with basis]
   - AI-pressure explanation: [state that this is one of the 43 checks and explain its internal score]
   - Main issues found: [plain-English failed checks with why and selected-mode action]
   - Full check table: [Markdown table with all 43 checks, status, why, selected-mode action]
3. Rewrite
4. Structural self-audit (mandatory, with counts):
   - Section arcs: N/M following same template - [what you changed]
   - Resolution density: N/M paragraphs end with summary - [what you changed]
   - Register breaks: [where you added one, or "already present at..."]
   - Triads: N found - reduced to M by [method]
   - Reframe laundering: [none / fixed at...]
   - Purposeful devices recommended for preservation: [device - reason, or "none"]
   - Stance: [preserved / shifted - restored by...]
   - Remaining tells: [list, or "none identified"]
5. Final report:
   - Summary: [before -> after numbers]
   - Confidence after rewrite: [post-check confidence]
   - Remaining issues: [none / list failed checks with why and action]
   - Full post-check table: [Markdown table with all 43 checks, status, why, selected-mode action]
   - Brief summary of changes made

Do not show a discarded draft rewrite by default. If you revise after self-audit, show only the final rewrite plus the audit notes. Show intermediate drafts only if the user asks.

---

## Full example

**Before (AI-sounding):**
> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools--nestled at the intersection of research and practice--are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organizations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. The technology has been featured in The New York Times, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies, the ecosystem continues to thrive. In order to fully realize this potential, teams must align with best practices.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you'd like me to expand on any section!

**Rewrite:**
> AI coding assistants speed up some tasks, but the picture is more complicated than the hype suggests. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools work well for boilerplate: config files, test scaffolding, and repetitive refactors. They are less reliable when it comes to knowing when they are wrong. I have accepted suggestions in bulk that compiled and passed lint but still did the wrong thing, because I stopped paying close enough attention to catch the error.
>
> Mira, an engineer at a fintech startup I interviewed, said she uses Copilot "like autocomplete for boring code" but reviews every line before committing. Jake, a senior developer at a larger company, disabled it after it kept suggesting patterns from a deprecated internal library. Both reactions seem reasonable for different contexts.
>
> The productivity claims are difficult to verify independently. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not the same as correctness, and correctness is not the same as value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless, but it does mean they are tools in the ordinary sense of the word. They do not replace judgment, and they do not eliminate the need for tests.

**Structural self-audit:**
- The named people and study citations could be plausible-sounding fabrications. If real, they should be sourced; if not, removed.
- The final paragraph wraps things up too cleanly ("they are tools in the ordinary sense of the word").
- Pacing is still even: every paragraph is roughly the same length with a similar claim-then-evidence structure.

**Revised rewrite after self-audit:**
> AI coding assistants can make you faster at the boring parts of the job, but not much else, at least not yet. A 2024 Google study found developers completed simple functions 55% faster with Codex, with no measurable improvement on debugging or architecture.
>
> They are good at boilerplate: config files, test scaffolding, repetitive refactors. They are also good at producing code that looks right and compiles and passes lint but does something slightly different from what you intended. I have learned this the hard way more than once, usually when I was too tired to review carefully.
>
> The developers I talk to about this tend to fall into two camps. Some treat it like autocomplete for tedious code and review every line before committing. Others turned it off after it kept suggesting patterns they did not want. I find myself moving between both positions depending on the project.
>
> GitHub reports that Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. If your codebase does not have good test coverage, you are mostly guessing about whether the suggestion helped or hurt.

**Changes made:**
- Removed chatbot artifacts ("Great question!", "I hope this helps!", "Let me know if...")
- Removed significance inflation ("testament", "pivotal moment", "evolving landscape", "vital role")
- Removed promotional language ("groundbreaking", "nestled", "seamless, intuitive, and powerful")
- Removed vague attributions ("Industry observers")
- Removed superficial -ing phrases ("underscoring", "highlighting", "reflecting", "contributing to")
- Removed contrived contrast / negative parallelism ("It's not just X; it's Y")
- Removed rule-of-three patterns and synonym cycling ("catalyst/partner/foundation")
- Removed false ranges ("from X to Y, from A to B")
- Removed all em dashes (replaced with commas and restructured sentences)
- Removed copula avoidance ("serves as", "functions as", "stands as") in favour of "is"/"are"
- Removed formulaic challenges section ("Despite challenges... continues to thrive")
- Removed knowledge-cutoff hedging ("While specific details are limited...")
- Removed excessive hedging ("could potentially be argued that... might have some")
- Removed filler phrases ("In order to", "At its core")
- Removed generic positive conclusion ("the future looks bright", "exciting times lie ahead")
- Removed staccato dramatic fragments from draft
- Eliminated manufactured-insight framing throughout

---

## Sources

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), WikiProject AI Cleanup (foundation, patterns 1-25)
- [Linda Caroll, "Good Writing, AI Slop, and the Dragon"](https://lindac.substack.com/p/good-writing-ai-slop-and-the-dragon) (experiential vacancy framing)
- [Sam Kriss, "Why Does A.I. Write Like ... That?"](https://www.nytimes.com/2025/12/03/magazine/chatbot-writing-style.html), NYT Magazine (patterns 26-28: ghost language, quietness, synesthesia)
- [Charlie Guo, "The Field Guide to AI Slop"](https://www.ignorance.ai/p/the-field-guide-to-ai-slop) (patterns 29-32: rhetorical questions, metaphors, list-making, dramatic transitions; density framing)
- [Grammarly, "Common Words and Phrases in AI-Generated Content"](https://www.grammarly.com/blog/ai/common-ai-words/) (expanded vocabulary list)
- [GPTZero, "AI Vocabulary"](https://gptzero.me/ai-vocabulary), April 2026 (100 high-ratio AI phrases from public table, used as tentative clustering signals)
- [Matthew Vollmer, "I Asked the Machine to Tell on Itself"](https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself) (cross-source taxonomy and reference trail)
- [Shreya Shankar, "AI Writing"](https://sh-reya.com/blog/ai-writing/) (orphaned demonstratives and weak AI prose mechanics)
- [Abdulhai et al., "How LLMs Distort Our Written Language"](https://arxiv.org/abs/2603.18161), 2026 (subtraction framing: neutrality collapse, pronoun depletion, semantic drift; patterns 35-37)
- [Nature, "Signs of AI-generated text found in 14% of biomedical abstracts"](https://www.nature.com/articles/d41586-025-02097-6), 2025 (vocabulary items, temporal fingerprinting)
