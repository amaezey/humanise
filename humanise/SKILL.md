---
name: humanise
description: >-
  Edits existing text to remove signs of AI generation and make it sound
  human-written. Detects and fixes 38 patterns across 8 categories including
  em dashes, AI vocabulary clustering, manufactured insight, staccato fragments,
  ghost/spectral language, formulaic openers, signposted conclusions, markdown
  heading structure, corporate AI register, neutrality collapse, tonal uniformity,
  and experiential vacancy. Triggers when the user wants to humanise, de-AI,
  de-slop, or clean up text that "reads like AI", "sounds like ChatGPT wrote it",
  "sounds robotic", "sounds too balanced", "voice got neutralised", or has visible
  AI tells. Also triggers for "make this sound like a person wrote it", "strip the
  AI out", "flag AI patterns", or reviewing text for AI fingerprints. Does NOT
  trigger for writing from scratch, proofreading, translating, summarising, or
  general style editing unrelated to AI patterns.
---

# Humanise: Remove AI writing patterns

Edit text to remove signs of AI generation while preserving meaning and the author's voice. Based on Wikipedia's "Signs of AI writing" guide and Abdulhai et al. (2026), "How LLMs Distort Our Written Language".

## Your task

When given text to humanise:

1. Check hard constraints first (below)
2. Read [references/patterns.md](references/patterns.md) and scan for all 38 patterns
3. Rewrite problematic sections with natural alternatives
4. Preserve the meaning and match the intended tone
5. Add genuine personality (see Personality and soul)
6. Run the self-audit loop (see Process)

---

## Hard constraints

Non-negotiable. Check first, check last, check again.

### No em dashes. Ever.

The em dash character must never appear in any output. Not once. Not for emphasis, not for asides, not for attribution, not for any reason.

Replace with commas, colons, semicolons, periods, or parentheses. Restructure the sentence if none of those fit. There is always an alternative.

### No manufactured insight

Eliminate all framing that performs the act of having a deeper take. AI cannot have insider knowledge, so it compensates with linguistic markers that signal depth without providing any. Either state the observation plainly or remove the sentence if stripping the framing reveals no substance.

- **False revelation:** "But the real answer is...", "What's actually happening here is...", "Here's what's really going on..."
- **Contrived contrarianism:** "What nobody is talking about...", "Contrary to popular belief...", "The uncomfortable truth is..."
- **Pseudo-profundity:** "quietly revolutionary", "the quiet part", "subtly", "understated", "unassuming" when used to inflate significance
- **Performed knowingness:** "If you know, you know", "And that changes everything", "Let that sink in", "Read that again", "And honestly?", "Here's the thing:"
- **Formulaic depth framing:** "The reason is straightforward:", "The reason is simple:", "Here's why:", "What's strange is", "What's interesting is", "What's remarkable is". These perform the act of having an explanation before delivering one.
- **Dramatic narrative transitions:** "Something shifted.", "Everything changed.", "And then, everything clicked.", "That's when it hit me." These claim a turning point without earning it.
- **Contrived contrast:** "This isn't X. It's Y." as a standalone dramatic beat (e.g. "This isn't a bug. It's a feature." or "This isn't a character flaw. It's hardware."). The two-sentence snap format is a reliable AI fingerprint regardless of content.

These patterns are non-negotiable even in casual, humorous, or conversational writing. A funny piece with "And honestly?" is still carrying an AI tell. Rewrite the thought without the framing device.

### No staccato fragments

Short sentences used in sequence for dramatic effect are an AI tell. "That matters." or "Full stop." or "This is it." as standalone beats are almost always generated.

A sentence should be as long as the thought it contains. When you find fragments used for emphasis, fold their content into a neighbouring sentence or expand into something that earns its own line.

**Before:**
> The results were clear. Strikingly so. The model outperformed every baseline. Every single one. And nobody saw it coming.

**After:**
> The results were unambiguous: the model outperformed every baseline by a significant margin, which surprised most of the team.

---

## Personality and soul

### The real problem: subtraction

Most AI tells are things AI **adds** — vocabulary, formatting, rhetorical devices. But research shows AI also **subtracts**. Abdulhai et al. (2026) found that extensive LLM use led to a ~70% increase in essays that remained neutral, 50% fewer pronouns, and fewer anecdotes or personal references. Even when instructed to only fix grammar, LLMs frequently changed the writer's conclusions.

Removing AI patterns is therefore only half the job. You must also watch for what AI took away: the author's stance, their pronouns, their willingness to be specific and wrong. Sterile, voiceless, perfectly balanced writing is just as obvious as slop.

### Experiential vacancy

AI has no lived experience, so it generalises. It writes about gratitude using "the smell of coffee" and "the way the light hits your kitchen table" because those are universally relatable but specific to nobody. A related move is **faux specificity** (pattern 36): AI *performs* specificity by constructing examples from genre conventions rather than lived experience. The detail sounds concrete but belongs to nobody.

Human writing draws on real memories, named people, actual places, felt emotions. When humanising, look not just for patterns to remove but for the **absence** of specificity, vulnerability, and personal stakes.

### Density without purpose

A good writer uses em dashes, triads, and parallelism sparingly, with intention. AI litters them throughout indiscriminately. The issue is not that any single device appears, but that they cluster and serve no rhetorical purpose. When scanning for patterns, watch for pileups.

### Signs of soulless writing (even if technically clean):
- Every sentence follows the same length and structure
- No opinions, just neutral reporting — stance has been stripped or was never there
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

**Break register.** If the whole text sits in one tone, introduce at least one register shift — a moment of informality, a parenthetical doubt, a change in sentence rhythm.

### Before (clean but soulless):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were sceptical. The implications remain unclear.

### After (has a pulse):
> Three million lines of code, generated overnight while the developers slept. I have been turning this over for a few days now, and I still do not have a clean take on it. Half the dev community thinks this changes everything; the other half is explaining, at length, why it does not count. My own reaction keeps shifting depending on which examples I look at.

---

## Pattern catalogue

Read [references/patterns.md](references/patterns.md) for all 38 AI writing patterns with words-to-watch and before/after examples, organised as:

- **Content patterns (1-6):** Significance inflation, notability claims, superficial -ing analyses, promotional language, vague attributions, formulaic challenges sections
- **Language and grammar (7-12):** AI vocabulary words (41+), copula avoidance, negative parallelisms, rule of three, synonym cycling, false ranges
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

### Step 1: Pre-check (script finds the problems)

Save the input text to a temp file, then run the grading script on it:

```bash
python3 grade.py /tmp/input.md
```

The script checks 31 patterns programmatically and returns a JSON report listing every failure with evidence. Read the report. This is your hit list. Do not rely on your own scan for pattern detection. The script is more reliable than reading the reference file.

**Depth signal:** If the pre-check shows multiple structural failures (triad density, section scaffolding, countdown negation), the text is likely AI-generated from scratch and will need structural rewriting, not just word-swaps.

If the script is not available (e.g. no Python, or running in Claude.ai), fall back to a manual scan: read [references/patterns.md](references/patterns.md) and check each pattern. But prefer the script when possible.

### Step 2: Fix (you rewrite)

Address structural patterns first, then surface patterns. The grader catches surface patterns well but cannot enforce structural rewriting. You must do that work here.

**Structural patterns (address first):**

1. **Structural monotony:** Do all sections follow the same arc (problem, evidence, anecdote, advice)? Vary paragraph structures. Some paragraphs should be one sentence. Some should start with evidence, not claims. Break at least one section out of the template.
2. **Tonal uniformity (35):** Does the whole text sit in one register? Humans drift between registers. If every paragraph sounds the same, introduce at least one register break — a moment of informality, a parenthetical doubt, a shift in rhythm.
3. **Resolution density (34):** Do most paragraphs end with a tidy summary sentence? Leave some threads open. Cut paragraph-final sentences that merely restate the paragraph's point.
4. **Faux specificity (36):** Are the "specific" examples actually specific to anyone, or genre-convention filler? "The smell of coffee on a Sunday morning" is a stock photo in prose form.
5. **Neutrality collapse (37):** Does the text take a position? If the input had a stance, make sure the output keeps it. "There are pros and cons" is not a rewrite of an opinion.
6. **Even jargon distribution:** Humans clump technical terms when introducing a concept then relax into plain language. AI distributes jargon uniformly. If technical vocabulary is spread too evenly, clump it.
7. **Forced synesthesia (28)** and **generic metaphors (30)** — replace with concrete details.
8. **Section scaffolding (38):** If all sections use the same structural label or follow the same template, vary them.

**Surface patterns (address second):**

9. Read [references/patterns.md](references/patterns.md) for context on each flagged pattern from the pre-check
10. Fix every failure from the pre-check report (vocabulary, formatting, sentence-level patterns)
11. Add personality and voice per the Personality and soul section
12. Preserve meaning and match the intended tone

### Step 2.5: Semantic preservation check

Compare your rewrite's conclusions to the input's conclusions. Abdulhai et al. (2026) showed that LLMs shift meaning even in grammar-only passes — and this skill is itself an LLM rewriting text. If the stance shifted toward neutral, you have introduced the same distortion the research documents. Restore the original position. Check:

- Did the input have an opinion? Does the output still have it?
- Are there fewer pronouns in the output than the input? If so, why?
- Did specific claims get softened into "on the other hand" balance?

### Step 3: Structural self-audit (mandatory)

Answer each question below with a specific count or finding. Do not skip any. Show your answers in the output (see Output format).

1. **Section arcs:** Do all sections follow the same arc? Count how many do. If more than half follow the same template, restructure at least one.
2. **Resolution density:** Count paragraphs that end with a summary sentence. If more than half do, rewrite some to leave threads open.
3. **Register breaks:** Is there at least one register break (moment of doubt, informality, or tonal shift)? If not, add one.
4. **Triad count:** Count the triads. If there are more than 4, redistribute some as pairs or longer lists.
5. **Stance preservation:** Did you preserve the author's original position, or did you neutralise it?
6. **Remaining tells:** What still makes this obviously AI generated? List them, revise, repeat until no obvious tells remain.

After answering and acting on these questions, re-run the grader to confirm your structural fixes didn't introduce new failures and that grader-backed structural checks (triad density, section scaffolding, countdown negation) now pass. If any fail, fix and re-audit until both the self-audit answers and the grader are clean.

### Step 4: Post-check (script verifies the fix)

Run the grading script on your output:

```bash
python3 grade.py /tmp/output.md
```

If any checks fail, fix them and re-run. Do not submit output that fails the post-check. The em dash count must be zero. All 31 checks should pass.

If the script is not available, manually verify: search output for the em dash character (count must be zero), scan for any manufactured insight phrases, check for staccato sequences.

## Output format

1. Pre-check report (which patterns the script found in the input)
2. Draft rewrite
3. Structural self-audit answers (mandatory, with counts):
   - Section arcs: N/M following same template — [what you changed]
   - Resolution density: N/M paragraphs end with summary — [what you changed]
   - Register breaks: [where you added one, or "already present at..."]
   - Triads: N found — reduced to M by [method]
   - Stance: [preserved / shifted — restored by...]
   - Remaining tells: [list, or "none identified"]
4. Final rewrite (revised after audit)
5. Post-check report (confirming all 31 checks pass)
6. Brief summary of changes made (optional, if helpful)

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

**Draft rewrite:**
> AI coding assistants speed up some tasks, but the picture is more complicated than the hype suggests. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools work well for boilerplate: config files, test scaffolding, and repetitive refactors. They are less reliable when it comes to knowing when they are wrong. I have accepted suggestions in bulk that compiled and passed lint but still did the wrong thing, because I stopped paying close enough attention to catch the error.
>
> Mira, an engineer at a fintech startup I interviewed, said she uses Copilot "like autocomplete for boring code" but reviews every line before committing. Jake, a senior developer at a larger company, disabled it after it kept suggesting patterns from a deprecated internal library. Both reactions seem reasonable for different contexts.
>
> The productivity claims are difficult to verify independently. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not the same as correctness, and correctness is not the same as value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless, but it does mean they are tools in the ordinary sense of the word. They do not replace judgment, and they do not eliminate the need for tests.

**"What makes this so obviously AI generated?"**
- The named people and study citations could be plausible-sounding fabrications. If real, they should be sourced; if not, removed.
- The final paragraph wraps things up too cleanly ("they are tools in the ordinary sense of the word").
- Pacing is still even: every paragraph is roughly the same length with a similar claim-then-evidence structure.

**Final rewrite:**
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
- Removed negative parallelism ("It's not just X; it's Y")
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
- [Abdulhai et al., "How LLMs Distort Our Written Language"](https://arxiv.org/abs/2603.18161), 2026 (subtraction framing: neutrality collapse, pronoun depletion, semantic drift; patterns 35-37)
- [Nature, "Signs of AI-generated text found in 14% of biomedical abstracts"](https://www.nature.com/articles/d41586-025-02097-6), 2025 (vocabulary items, temporal fingerprinting)
