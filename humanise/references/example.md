# Worked example: AI-sounding draft → audit → rewrite

End-to-end demonstration on a single AI-generated essay: the audit it produces in default and full-report modes, then a rewrite at All depth with structural self-check and revised rewrite. Use as a reference for what a real Audit and Rewrite action's outputs look like.

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

## Agent-judgement file

The agent reads `humanise/scripts/judgement.json` for the eight-item registry, decides each item's status and answer against the draft, and writes a JSON file matching the contract's `agent_judgement` slot. Severity is omitted so `grade.py` defaults each item to its registry value. The file:

```json
{
  "agent_judgement": [
    {"id": "structural_monotony", "status": "flagged", "answer": "every section follows the same arc", "evidence": {}},
    {"id": "tonal_uniformity", "status": "flagged", "answer": "register holds without breaks", "evidence": {}},
    {"id": "faux_specificity", "status": "clear", "answer": [], "evidence": {}},
    {"id": "neutrality_collapse", "status": "flagged", "answer": "hedges its position", "evidence": {}},
    {"id": "even_jargon_distribution", "status": "clear", "answer": "jargon clumps where the writer knows things", "evidence": {}},
    {"id": "forced_synesthesia", "status": "clear", "answer": [], "evidence": {}},
    {"id": "generic_metaphors", "status": "clear", "answer": [], "evidence": {}},
    {"id": "genre_specific", "status": "clear", "answer": {"genre_detected": "default", "watchlist_findings": []}, "evidence": {}}
  ]
}
```

`grade.py --judgement-file <path>` merges this file into the contract before rendering, so a single call produces the full audit shown below. The agent does not re-render the agent-assessed block by hand.

## Audit (default mode)

`python3 humanise/scripts/grade.py --format markdown --depth balanced --judgement-file <agent-judgement.json>` produces the summary block + flagged items from both blocks + the next-step prompt. Severity glyphs: `x` hard_fail, `!` strong_warning, `?` context_warning. Auto-detected flagged items render first; agent-assessed flagged items follow. Clear items don't appear in the default body — they show up in the full-report-mode coverage tables.

```
Audit
Auto-detected: 13 of 48 flagged · Agent-assessed: 3 of 8 flagged
Severity: 2 hard fail · 10 strong warning · 4 context warning
Signal stacking: triggered — 9 of 4 threshold (formulaic openings, assistant residue, generic conclusion endings)

! **Clustered AI vocabulary** — "enduring", "landscape", "pivotal" (+4 more)
x **Assistant residue** — "i hope this helps", "great question", "let me know if"
? **Generic promotional language** — "nestled", "groundbreaking"
? **Inflated significance** — "pivotal", "vital role", "testament"
! **Avoiding plain 'is'** — "serves as", "serves as", "stands as" (+1 more)
! **Filler phrases** — "in order to"
x **Generic conclusion** — "the future looks bright", "exciting times", "continue this journey"
! **Tacked-on -ing analysis**
! **Formulaic openers** — "At its core, the value proposition is clear: streamlining pr"
? **Signposted conclusion** — "In conclusion, the future looks bright. Exciting times lie a"
! **Corporate AI-speak** — "cross-functional"
! **Vague attributions** — "observers have noted"
! **Knowledge-cutoff disclaimers** — "based on available information", "while specific details are limited"
? **Structural monotony** — every section follows the same arc
! **Tonal uniformity** — register holds without breaks
! **Neutrality collapse** — hedges its position

**Next step**

Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?
```

A zero-flag draft renders the same shape — the summary block carries all-zero counts and there are no flagged items between the summary and the next-step prompt. There's no all-clear single-line shortcut.

## Audit (full-report mode)

When the writer asks for the full coverage report, re-run with `--full-report` (keep the `--judgement-file` flag). The script appends two per-block sections — `**Auto-detected patterns**` (with the eight category sub-tables in `humanise/references/patterns.md` heading order) and `**Agent-assessed patterns**` (a flat eight-row table in `humanise/scripts/judgement.json` registry order) — between the audit body and the next-step prompt. Each per-block section opens with a brief note explaining what's in the block. Coverage tables are 4-column: `Pattern | Severity | Result | Detail`. Detail carries the per-pattern guidance text on flagged auto-detected rows (empty when clear), and `(see above)` for flagged agent-assessed rows (pointing back at the inline bullet block) with the answer/value text on clear rows.

```
[default audit body, exactly as above, including all flagged items]

**Auto-detected patterns** — 13 flagged of 48

Checks the script runs against the text directly.

**Content patterns** — 4 flagged of 5

| Pattern | Severity | Result | Detail |
| --- | --- | --- | --- |
| Generic promotional language | context warning | Flagged | Fix generic hype; recommend preserving quoted marketing copy or voiced enthusiasm. |
| Inflated significance | context warning | Flagged | Fix inflated importance unless the source genuinely argues significance. |
| Tacked-on -ing analysis | strong warning | Flagged | Fix tacked-on analysis clauses unless they carry precise causal meaning. |
| Notability claims | strong warning | Clear |  |
| Vague attributions | strong warning | Flagged | Fix at Balanced and All; replace unnamed authorities with a named source, study, or quote. |

[... seven more category sub-tables in patterns.md heading order; categories where every check is clear collapse to a single `**<Category>** — N/N clear` line. The full output includes Language and grammar, Style, Communication, Filler and hedging, Sensory and atmospheric, Structural tells, and Voice and register.]

**Agent-assessed patterns** — 3 flagged of 8

Checks that are judged by an LLM based on reading the whole draft.

| Pattern | Severity | Result | Detail |
| --- | --- | --- | --- |
| Structural monotony | context warning | Flagged | (see above) |
| Tonal uniformity | strong warning | Flagged | (see above) |
| Faux specificity | strong warning | Clear |  |
| Neutrality collapse | strong warning | Flagged | (see above) |
| Even jargon distribution | context warning | Clear | jargon clumps where the writer knows things |
| Forced synesthesia | context warning | Clear |  |
| Generic metaphors | context warning | Clear |  |
| Genre specific | context warning | Clear | Genre detected: default; watchlist coverage pending |

**Next step**

Want suggestions for edits, a full rewrite, or to save this audit as a file?
```

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
