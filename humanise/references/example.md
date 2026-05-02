# Worked example: AI-sounding draft → audit → rewrite

End-to-end demonstration on a single AI-generated essay: the dual-layer audit it produces, then a rewrite at All depth with structural self-check and revised rewrite. Use as a reference for what a real Audit and Rewrite action's outputs look like.

## Before (AI-sounding)

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

## Audit

Real `python3 humanise/grade.py --format markdown --depth balanced` output on the input above, with a representative agent-judgement block underneath. Severity glyphs in Layer 1: `x` hard_fail, `!` strong_warning, `?` context_warning. Layer 2 collapses categories where every check is clear; expanded sub-tables include the clear rows so coverage stays visible. The agent-judgement block uses the eight-item registry in `humanise/judgement.yaml` and renders status binary (Flagged / Clear) with no severity column.

```
Audit
Severity: 2 hard_fail · 8 strong_warning · 3 context_warning · pressure: triggered
Pressure triggered: weaker AI-writing signals stacked to 9 of the 4-point threshold (formulaic openings, assistant residue, generic conclusion endings, plus 4 clustered AI-vocabulary point(s)).

! **Clustered AI vocabulary** — "enduring", "landscape", "pivotal" (+4 more) — Action: Fix
x **Assistant residue** — "i hope this helps", "great question", "let me know if" — Action: Fix
? **Generic promotional language** — "nestled", "groundbreaking" — Action: Disclose or ask before preserving
? **Inflated significance** — "pivotal", "vital role", "testament" — Action: Disclose or ask before preserving
! **Avoiding plain 'is'** — "serves as", "serves as", "stands as" (+1 more) — Action: Fix
! **Filler phrases** — "in order to" — Action: Fix
x **Generic conclusion** — "the future looks bright", "exciting times", "continue this journey" — Action: Fix
! **Tacked-on -ing analysis** — Action: Fix
! **Formulaic openers** — "At its core, the value proposition is clear: streamlining pr" — Action: Fix
? **Signposted conclusion** — "In conclusion, the future looks bright. Exciting times lie a" — Action: Disclose or ask before preserving
! **Corporate AI-speak** — "cross-functional" — Action: Fix
! **Vague attributions** — "observers have noted" — Action: Fix
! **Knowledge-cutoff disclaimers** — "based on available information", "while specific details are limited" — Action: Fix

---

**Content patterns** — 4 flagged of 5

| Pattern | Result | Action |
| --- | --- | --- |
| Generic promotional language | Flagged | Disclose or ask before preserving |
| Inflated significance | Flagged | Disclose or ask before preserving |
| Tacked-on -ing analysis | Flagged | Fix |
| Notability claims | Clear |  |
| Vague attributions | Flagged | Fix |

**Language and grammar** — 2 flagged of 6

| Pattern | Result | Action |
| --- | --- | --- |
| Clustered AI vocabulary | Flagged | Fix |
| Contrived contrast | Clear |  |
| Avoiding plain 'is' | Flagged | Fix |
| Decorative three-part lists | Clear |  |
| Vocabulary diversity | Clear |  |
| Triad density | Clear |  |

**Style** — 6/6 clear

**Communication** — 2 flagged of 2

| Pattern | Result | Action |
| --- | --- | --- |
| Assistant residue | Flagged | Fix |
| Knowledge-cutoff disclaimers | Flagged | Fix |

**Filler and hedging** — 3 flagged of 8

| Pattern | Result | Action |
| --- | --- | --- |
| Generic staccato emphasis | Clear |  |
| Filler phrases | Flagged | Fix |
| Generic conclusion | Flagged | Fix |
| False balance or concession | Clear |  |
| Soft explainer scaffolding | Clear |  |
| Formulaic openers | Flagged | Fix |
| Excessive hedging | Clear |  |
| Dense negation | Clear |  |

**Sensory and atmospheric** — 2/2 clear

**Structural tells** — 1 flagged of 9

| Pattern | Result | Action |
| --- | --- | --- |
| Manufactured insight framing | Clear |  |
| Sentence rhythm variance | Clear |  |
| Template rhetorical questions | Clear |  |
| Excessive list formatting | Clear |  |
| Decorative Unicode | Clear |  |
| Unearned dramatic transitions | Clear |  |
| Signposted conclusion | Flagged | Disclose or ask before preserving |
| Paragraph length uniformity | Clear |  |
| Repeated section scaffolding | Clear |  |

**Voice and register** — 1 flagged of 10

| Pattern | Result | Action |
| --- | --- | --- |
| Nonliteral land/surface phrasing | Clear |  |
| Mechanical repeated sentence starts | Clear |  |
| Placeholder residue | Clear |  |
| Vague 'this/that' starts | Clear |  |
| Corporate AI-speak | Flagged | Fix |
| Repeated 'This...' chains | Clear |  |
| Countdown negation | Clear |  |
| Tidy paragraph endings | Clear |  |
| Bland critical template | Clear |  |
| Rubric echoing | Clear |  |

---

**Agent-judgement reading — 4 flagged of 8**

- Structural monotony — Flagged: every section follows the same arc
- Tonal uniformity — Flagged: register holds without breaks
- Faux specificity — Clear
- Neutrality collapse — Flagged: hedges its position
- Even jargon distribution — Clear: jargon clumps where the writer knows things
- Forced synesthesia — Clear
- Generic metaphors — Clear
- Genre specific — Flagged: Genre detected: default.

**Next step**

Want suggestions for per-flag replacements, a rewrite at a chosen depth, or to save this audit as a Markdown file?
```

The all-clear case collapses to a single line — `<N> of <N> clear · agent reading clean · pressure: clear.` followed by the next-step prompt. No tables, no glyphs, no level label.

## Rewrite

> AI coding assistants speed up some tasks, but the picture is more complicated than the hype suggests. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools work well for boilerplate: config files, test scaffolding, and repetitive refactors. They are less reliable when it comes to knowing when they are wrong. I have accepted suggestions in bulk that compiled and passed lint but still did the wrong thing, because I stopped paying close enough attention to catch the error.
>
> Mira, an engineer at a fintech startup I interviewed, said she uses Copilot "like autocomplete for boring code" but reviews every line before committing. Jake, a senior developer at a larger company, disabled it after it kept suggesting patterns from a deprecated internal library. Both reactions seem reasonable for different contexts.
>
> The productivity claims are difficult to verify independently. GitHub says Copilot users "accept 30% of suggestions," but acceptance is not the same as correctness, and correctness is not the same as value. The 2024 Uplevel study found no statistically significant difference in pull-request throughput between teams with and without AI assistants.
>
> None of this means the tools are useless, but it does mean they are tools in the ordinary sense of the word. They do not replace judgment, and they do not eliminate the need for tests.

## Structural self-check

- The named people and study citations could be plausible-sounding fabrications. If real, they should be sourced; if not, removed.
- The final paragraph wraps things up too cleanly ("they are tools in the ordinary sense of the word").
- Pacing is still even: every paragraph is roughly the same length with a similar claim-then-evidence structure.

## Revised rewrite after self-check

> AI coding assistants can make you faster at the boring parts of the job, but not much else, at least not yet. A 2024 Google study found developers completed simple functions 55% faster with Codex, with no measurable improvement on debugging or architecture.
>
> They are good at boilerplate: config files, test scaffolding, repetitive refactors. They are also good at producing code that looks right and compiles and passes lint but does something slightly different from what you intended. I have learned this the hard way more than once, usually when I was too tired to review carefully.
>
> The developers I talk to about this tend to fall into two camps. Some treat it like autocomplete for tedious code and review every line before committing. Others turned it off after it kept suggesting patterns they did not want. I find myself moving between both positions depending on the project.
>
> GitHub reports that Copilot users "accept 30% of suggestions," but acceptance is not correctness, and correctness is not value. If your codebase does not have good test coverage, you are mostly guessing about whether the suggestion helped or hurt.

## Changes made

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
