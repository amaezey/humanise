`★ Insight ─────────────────────────────────────`
- The grader is a *signal* detector, not an authorship verdict. Every flag below should be read with the purpose test: is the device doing real work, or is it autopilot?
- This is Virginia Woolf, 1929 — a literary essay famous for cadenced repetition, triadic rhythm, and atmospheric verbs. Several flags here are exactly the signature features the grader is built to catch in *AI* prose, which is why this sample is part of the false-positive audit corpus. The flags are correctly *firing*; the call on whether they are AI-style is contextual.
- "Hard action: Fix" in the script's column reflects what hard mode would *do* about each finding, not whether the device is bad. In an audit (mode-agnostic), the severity-tiered recommendation is what matters.
`─────────────────────────────────────────────────`

## Action: Audit

### Audit report

**Summary:** 7 of 43 checks were flagged for AI-style writing patterns.

**Confidence:** Medium. Several signs of AI-like writing appeared, but the evidence is pattern-based and should be read in context. Basis: 1 strong-warning-class signal and 6 context-sensitive signals. This is a confidence assessment about AI-writing signs, not an authorship verdict.

**AI-pressure explanation:** AI-pressure looks for accumulation — weaker patterns that are harmless alone but more meaningful when they stack into machine-packaged rhythm or structure. This text did not stack enough weak signals to trigger that pressure check (score 0/4). The flags are mostly individual stylistic devices rather than a stacked pattern.

### Main issues found

- **Mechanical repeated sentence starts** — *Severity: context warning.* Found 3 consecutive sentences starting with "No" ("No need to hurry. No need to sparkle. No need to be anybody but oneself."). Mechanical repeated openings can read like template rhythm, but in this passage it is deliberate anaphora performing the after-lunch ease the narrator is describing. **Recommended action:** Preserve in Light if purposeful (disclose). Fix in Medium and Hard.

- **Generic promotional language** — *Severity: context warning.* Found "profound" once, in "the more profound, subtle and subterranean glow which is the rich yellow flame of rational intercourse." Not promotional in context — it is a triadic adjective stack describing mood, not selling anything. **Recommended action:** Preserve in Light if purposeful (disclose). Fix in Medium and Hard.

- **Filler phrases** — *Severity: context warning.* Found 1: "in order to". Period-standard 1929 phrasing; flagging it on a single occurrence is borderline. **Recommended action:** Fix in Medium and Hard; defensible to preserve in Light given the era.

- **Ghost/spectral atmosphere** — *Severity: context warning.* Found 4 ghost/spectral words: "whisper", "whispers", "echo", "echoes". Most appear inside quoted Tennyson and Christina Rossetti ("the lily whispers, 'I wait'") and in the literal architectural metaphor "Never will I wake those echoes". This is not the AI-stock spectral atmosphere the check targets. **Recommended action:** Preserve in Light if purposeful (disclose). Fix in Medium and Hard.

- **Generic quiet/still mood** — *Severity: context warning.* Found 4 quietness words (1.1 per 1000 words) — the Oxbridge-quadrangle sequence is doing actual atmospheric work; the quiet is the argument (the cloistered hush of male privilege). **Recommended action:** Preserve in Light if purposeful (disclose). Fix in Medium and Hard.

- **Vocabulary diversity** — *Severity: context warning.* Type-token ratio 0.331 (target >0.40) on 3,532 words. Woolf uses repetition as a structural device (the "Mary Beton, Mary Seton, Mary Carmichael" refrain; the recurring "women and fiction"; the looped "before the war"). The low TTR is a signature, not slop. **Recommended action:** Preserve in Light if purposeful (disclose). Fix in Medium and Hard.

- **Triad density** — *Severity: context warning.* Found 27 triads, including "Mary Beton, Mary Seton, Mary Carmichael", "the limitations, the prejudices, the idiosyncrasies", "to level, to ditch, to dig and to drain". Triadic rhythm is a load-bearing rhetorical device in Woolf's prose. The grader is right to count them; the count is high because the device is the style. **Recommended action:** Preserve in Light if purposeful (disclose). Fix in Medium and Hard.

### Full check table

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Em dashes | Clear | Em dash punctuation as a strong current AI signal. | No issue found. | Em dashes are now a strong AI fingerprint. | — | None |
| Clustered AI vocabulary | Clear | Generic AI-associated words clustering together. | No issue found. | Clusters are more suspicious than scattered words. | — | None |
| Nonliteral land/surface phrasing | Clear | Abstract uses of land/surface. | No issue found. | Makes ordinary ideas sound packaged. | — | None |
| AI pressure from stacked signals | Clear | Several weaker signals appearing together. | No issue found. | Stacked weak signals can read machine-packaged. | — | None |
| Manufactured insight framing | Clear | Phrases that perform hidden depth without earning it. | No issue found. | Performs depth without evidence. | — | None |
| Generic staccato emphasis | Clear | Repeated short dramatic sentences as generic emphasis. | No issue found. | Reads as generated rather than naturally paced. | — | None |
| Mechanical repeated sentence starts | Flagged | Repeated sentence openings reading like template rhythm. | 3 consecutive sentences starting with "No". | Can signal template rhythm rather than intentional rhetoric. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Assistant residue | Clear | Chatbot collaboration phrases or follow-up offers. | No issue found. | Looks like chat output rather than prose. | — | None |
| Curly quotes | Clear | Curly quotation marks when plain output is expected. | No issue found. | Matters when output should be plain text. | — | None |
| Sentence rhythm variance | Clear | Uniform sentence lengths across longer prose. | No issue found. | Low variance reads mechanical. | — | None |
| Generic promotional language | Flagged | Stock hype and sales-like adjectives. | Found "profound". | Stock hype weakens credibility. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Inflated significance | Clear | Language making ordinary claims sound historic. | No issue found. | Makes claims artificially momentous. | — | None |
| Contrived contrast | Clear | not-X-but-Y, beyond-X, less-X-than-Y reveal structures. | No issue found. | Creates a fake reveal. | — | None |
| Avoiding plain 'is' | Clear | Inflated replacements like serves as / functions as. | No issue found. | Turns simple claims into pseudo-analysis. | — | None |
| Filler phrases | Flagged | Stock padding such as "in order to" / "it is worth noting". | Found 1: "in order to". | Adds polish without information. | Context warning | Fix in Medium and Hard; defensible to preserve in Light given the period. |
| Generic conclusion | Clear | Empty endings such as "the future looks bright". | No issue found. | Templated and interchangeable endings. | — | None |
| False balance or concession | Clear | Fake both-sides framing. | No issue found. | Hides the writer's position. | — | None |
| Placeholder residue | Clear | Unfilled template markers. | No issue found. | Unfinished generated text. | — | None |
| Soft explainer scaffolding | Clear | Phrases that announce structure rather than make a point. | No issue found. | Announces structure rather than writing. | — | None |
| Vague 'this/that' starts | Clear | Repeated vague subjects like "This highlights". | No issue found. | Blurs the actual subject. | — | None |
| Decorative three-part lists | Clear | Forced triads as rhythm rather than substance. | No issue found at the cluster level. | Artificial rhythm without substance. | — | None |
| Tacked-on -ing analysis | Clear | Trailing -ing clauses pretending to analyse. | No issue found. | Pretends to analyse without adding meaning. | — | None |
| Ghost/spectral atmosphere | Flagged | Clichéd ghost/shadow/whisper/echo language. | 4 words: "whisper", "whispers", "echo", "echoes" (mostly inside quoted Tennyson/Rossetti and a literal architectural metaphor). | Stock spectral language can feel borrowed. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Generic quiet/still mood | Flagged | Overused quiet/still/soft/hushed atmosphere. | 4 quietness words (1.1 per 1000). | Generic literary atmosphere. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Template rhetorical questions | Clear | Article-style questions followed by obvious answers. | No issue found. | Simulates engagement without inquiry. | — | None |
| Excessive list formatting | Clear | Prose over-converted to bullets. | No issue found. | Reads like generated notes. | — | None |
| Decorative Unicode | Clear | Decorative symbols and punctuation. | No issue found. | Looks like generated formatting. | — | None |
| Unearned dramatic transitions | Clear | Generic turning points like "everything changed". | No issue found. | Claims drama not built. | — | None |
| Formulaic openers | Clear | Generated openings like "at its core". | No issue found. | Assembled-from-templates feel. | — | None |
| Signposted conclusion | Clear | Explicit conclusion labels. | No issue found. | Flattens endings into summary. | — | None |
| Headings in prose | Clear | Markdown or plain-title headings inside prose. | No issue found. | Looks packaged by an assistant. | — | None |
| Corporate AI-speak | Clear | Vague delivery/alignment/outcomes clichés. | No issue found. | Hides specifics behind operational vagueness. | — | None |
| Repeated 'This...' chains | Clear | Several consecutive vague-This sentences. | No issue found. | Generic analysis, weak subject control. | — | None |
| Excessive hedging | Clear | Evasive qualification. | No issue found. | Weakens stance. | — | None |
| Countdown negation | Clear | Repeated no/not/cannot building to a reveal. | No issue found. | Synthetic reveal structure. | — | None |
| Dense negation | Clear | Unusually dense negation markers. | No issue found. | Over-frames around what something is not. | — | None |
| Paragraph length uniformity | Clear | Suspiciously similar paragraph lengths. | No issue found. | Signals generated structure. | — | None |
| Tidy paragraph endings | Clear | Repeated miniature conclusions at paragraph ends. | No issue found. | Over-resolved, templated paragraphs. | — | None |
| Bland critical template | Clear | Generic review language. | No issue found. | Portable review phrasing instead of judgment. | — | None |
| Rubric echoing | Clear | Assignment or rubric phrasing leaking in. | No issue found. | Sounds like rubric compliance. | — | None |
| Vocabulary diversity | Flagged | Unusually repetitive vocabulary in longer text. | TTR 0.331 (1169/3532, target >0.40). | Repetitive vocabulary can feel mechanical in long prose. | Context warning | Preserve in Light if purposeful (disclose) — Woolf uses the "Mary Beton/Seton/Carmichael" refrain and recurrent "women and fiction" as structural devices. Fix in Medium and Hard. |
| Triad density | Flagged | Three-part list structures used pervasively. | 27 triads, including "Mary Beton, Mary Seton, Mary Carmichael", "the limitations, the prejudices, the idiosyncrasies", "to level, to ditch, to dig and to drain". | Pervasive triads create generated cadence. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Repeated section scaffolding | Clear | Repeated section labels or templates. | No issue found. | Feels assembled from a template. | — | None |

### Read of the audit

Every flag here is a context warning except *filler phrases* (one occurrence). No hard failures, no strong warnings, no AI-pressure stacking. The grader is correctly detecting Woolf's stylistic signatures — anaphora, triadic rhythm, repeated proper-noun refrain, period-appropriate "in order to", literary atmosphere — and would (correctly) tell you to remove them in Hard mode if you asked it to. In an audit on a 1929 literary essay, those flags are evidence of voice, not of AI generation. The aggregate pattern (low pressure score, no hard fails, no strong warnings, the structural-failure cluster from the "depth signal" entirely absent) is what a known-human literary text should look like through this grader.

`★ Insight ─────────────────────────────────────`
- The grader does not know what year a text was written. "In order to", "profound", and quiet/still vocabulary are penalised because they cluster heavily in current AI prose; in pre-WWII essay prose they are unmarked. This is exactly why the audit is mode-agnostic and the *purpose test* lives at the human review layer.
- The "depth signal" the skill flags for likely-AI structure (triad density + section scaffolding + countdown negation + paragraph uniformity + soft scaffolding + orphaned demonstratives + tidy endings) requires a *cluster* of structural failures. Here only triad density fires. That isolation is itself a signal that the prose is structurally human-shaped even though one device is heavily used.
`─────────────────────────────────────────────────`

Do you want a rewrite, a recommended intensity, or a saved Markdown report?