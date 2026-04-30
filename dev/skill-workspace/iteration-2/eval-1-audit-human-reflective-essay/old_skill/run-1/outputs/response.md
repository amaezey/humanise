**Action: Audit**

**Summary:** 6 of 43 checks were flagged for AI-style writing patterns.

**Confidence:** Medium. This is confidence about AI-writing signs, not an authorship verdict. The flags are pattern-based, and several are likely explained by literary rhetoric or by duplicated extraction text rather than generated prose.

**Main read:** this does **not** read like a typical AI draft. The strongest signals come from repetition, list rhythm, and contrast framing, but in this piece those are mostly part of the essay’s compressed, rhetorical style. The more practical issue is that the file appears to contain repeated passages and page-share/footer residue, which can make a detector overreact.

**Main Issues**

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Generic staccato emphasis | Flagged | Repeated short dramatic sentences used as generic emphasis. | Found a sequence of 5 consecutive short sentences. | Can sound generated when the short beats are empty emphasis. Here, much of it is literary cadence. | Context warning | Preserve if purposeful; fix only duplicated/noisy text. |
| Mechanical repeated sentence starts | Flagged | Repeated sentence openings that read like template rhythm. | Found 5 consecutive sentences starting with “However.” | Repeated openings can look templated, but here the anaphora is doing rhetorical work. | Context warning | Preserve if intentional; remove accidental duplicate passages. |
| Curly quotes | Flagged | Curly quotation marks when plain cleaned text is expected. | Found 18 curly quote marks. | Not an AI tell in a sourced literary essay. | Context warning | Preserve. |
| Contrived contrast | Flagged | “Not X but Y,” “beyond X,” and similar reveal structures. | Found 4 contrast/reframe patterns. | In generic prose, this can fake insight. Here, some contrast belongs to the essay’s argumentative movement. | Strong warning | Review manually; do not treat as authorship evidence by itself. |
| Vocabulary diversity | Flagged | Unusually repetitive vocabulary in longer text. | Type-token ratio: 0.372, below the target of 0.40. | Repetition can sound mechanical, but literary repetition and duplicated extraction text both lower the score. | Context warning | Fix duplicate extraction artifacts, not the authorial cadence. |
| Triad density | Flagged | Heavy use of three-part lists. | Found 23 triads, including “hopes, dreams, values.” | Too many triads can create generated cadence, but this essay deliberately accumulates examples. | Context warning | Preserve where rhetorical; trim only accidental or editorial additions. |

**Full Check Table**

| Check | Status | What happened here | Severity | Recommended action |
|---|---|---|---|---|
| Em dashes | Clear | No issue found. | — | None |
| Clustered AI vocabulary | Clear | No issue found. | — | None |
| Nonliteral land/surface phrasing | Clear | No issue found. | — | None |
| AI pressure from stacked signals | Clear | Score stayed below the concern threshold. | — | None |
| Manufactured insight framing | Clear | No issue found. | — | None |
| Generic staccato emphasis | Flagged | Found 5 consecutive short sentences. | Context warning | Preserve if purposeful. |
| Mechanical repeated sentence starts | Flagged | Found repeated “However” openings. | Context warning | Preserve if rhetorical; remove accidental duplicates. |
| Assistant residue | Clear | No chat-like residue found. | — | None |
| Curly quotes | Flagged | Found 18 curly quotes. | Context warning | Preserve in this literary context. |
| Sentence rhythm variance | Clear | Sentence lengths vary enough. | — | None |
| Generic promotional language | Clear | No stock hype found. | — | None |
| Inflated significance | Clear | No artificial importance inflation found. | — | None |
| Contrived contrast | Flagged | Found 4 contrast/reframe patterns. | Strong warning | Review manually; preserve if earned. |
| Avoiding plain “is” | Clear | No inflated copula avoidance found. | — | None |
| Filler phrases | Clear | No stock padding found. | — | None |
| Generic conclusion | Clear | No templated ending found. | — | None |
| False balance or concession | Clear | No fake both-sides framing found. | — | None |
| Placeholder residue | Clear | No template placeholders found. | — | None |
| Soft explainer scaffolding | Clear | No structure-announcing filler found. | — | None |
| Vague “this/that” starts | Clear | No repeated vague openings found. | — | None |
| Decorative three-part lists | Clear | Triads were detected elsewhere as density, not decorative filler. | — | None |
| Tacked-on -ing analysis | Clear | No issue found. | — | None |
| Ghost/spectral atmosphere | Clear | No stock spectral language found. | — | None |
| Generic quiet/still mood | Clear | No overused quiet/still mood language found. | — | None |
| Template rhetorical questions | Clear | Questions here are substantive, not article-template prompts. | — | None |
| Excessive list formatting | Clear | No bullet/list over-formatting found. | — | None |
| Decorative Unicode | Clear | No decorative symbols found. | — | None |
| Unearned dramatic transitions | Clear | No generic turning-point language found. | — | None |
| Formulaic openers | Clear | No generated-style openers found. | — | None |
| Signposted conclusion | Clear | No explicit conclusion signpost found. | — | None |
| Headings in prose | Clear | No prose-disrupting headings found. | — | None |
| Corporate AI-speak | Clear | No operational cliché language found. | — | None |
| Repeated “This...” chains | Clear | No vague “This...” chain found. | — | None |
| Excessive hedging | Clear | No evasive qualification pattern found. | — | None |
| Countdown negation | Clear | No synthetic negation buildup found. | — | None |
| Dense negation | Clear | Negation density is not unusual. | — | None |
| Paragraph length uniformity | Clear | Paragraph lengths vary naturally. | — | None |
| Tidy paragraph endings | Clear | No repeated miniature conclusions found. | — | None |
| Bland critical template | Clear | No generic review-template language found. | — | None |
| Rubric echoing | Clear | No assignment/rubric phrasing found. | — | None |
| Vocabulary diversity | Flagged | Repetition score was below target. | Context warning | Check duplicate text before editing style. |
| Triad density | Flagged | Found 23 three-part list structures. | Context warning | Preserve if rhetorical. |
| Repeated section scaffolding | Clear | No repeated heading/template structure found. | — | None |

**Practical Next Step**

I would not rewrite this as “AI-sounding.” I would clean the file: remove duplicated paragraphs and the share/footer material, then re-run the audit on the essay text alone.