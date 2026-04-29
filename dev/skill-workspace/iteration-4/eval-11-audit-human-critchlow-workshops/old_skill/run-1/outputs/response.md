**Action:** Audit

## Audit report

**Summary:** 9 of 43 checks were flagged for AI-style writing patterns.

**Confidence:** High. Multiple structural signals fired and AI pressure reached threshold.
- *Basis:* 1 strong AI-writing signal, 8 context-sensitive signals, AI pressure score 5/4.
- *Note:* This is a confidence assessment about AI-writing signs, not an authorship verdict. This piece is a 2019 indie-consultant blog post by Tom Critchlow — several flags are conventional for that genre (headings, conversational triads, "but here's" pivots) and would likely survive a Light-mode review under the purpose test.

**AI-pressure explanation:** AI pressure looks for accumulation — weaker patterns that can be harmless alone but become more meaningful when they appear together. Here the stacked signals were manufactured-insight framing plus heavy heading use, with one extra point from clustered AI vocabulary. The grader read that as machine-packaged structure with too much visible scaffolding. Score: 5/4, so the stack-up check fired. The genre context (a structured how-to blog post) softens this reading.

### Main issues found

- **AI pressure from stacked signals — Flagged.** *What it looks for:* several weaker AI-writing signals appearing together. *What happened here:* manufactured-insight framing + headings in prose + 1 vocabulary point = 5/4. *Why it matters:* stacked weak signals can read as machine-packaged even when each is individually defensible. *Severity:* derived signal (composite). *Recommended action:* address the underlying signals; this score will drop on its own.
- **Manufactured insight framing — Flagged.** *What it looks for:* phrases that perform hidden depth without earning it. *What happened here:* "but here's" appears twice (e.g. "But here's one surprising outcome", "But here's a word of caution"). *Why it matters:* it stages a reveal instead of just making the claim. *Severity:* Strong warning. *Recommended action:* Fix in Light, Medium, and Hard. Disclose only if explicitly preserved.
- **Generic staccato emphasis — Flagged.** *What it looks for:* repeated short dramatic sentences used as emphasis. *What happened here:* a sequence of 4 consecutive short sentences (likely the "Free jazz not pop. Experience not performance. Collaborative not guided." run, plus the "Brand marketing is expensive! It's slow!" beat). *Why it matters:* repeated short emphasis beats can sound generated rather than naturally paced. *Severity:* Context warning (staccato). *Recommended action:* Preserve in Light if purposeful and disclosed (this looks deliberate — a punchy aphoristic riff). Fix in Medium and Hard.
- **Inflated significance — Flagged.** *What it looks for:* language that makes ordinary claims sound historically important. *What happened here:* "crucial" in "clarity is crucial to good work". *Why it matters:* inflated importance words can make ordinary claims feel artificially weighty. *Severity:* Strong warning. *Recommended action:* Fix in Light, Medium, and Hard. (Mild here — likely a false positive given the conversational register, but the grader catches the word as listed.)
- **Decorative three-part lists — Flagged.** *What it looks for:* forced abstract triads used as rhythm. *What happened here:* 1 abstract triad — "improvisation, sparring, discussion". *Why it matters:* abstract triads can create rhythm without substance. *Severity:* Context warning (triads). *Recommended action:* Preserve in Light if purposeful and disclosed; fix in Medium and Hard.
- **Signposted conclusion — Flagged.** *What it looks for:* explicit conclusion labels. *What happened here:* a "## Conclusion" heading. *Why it matters:* labelled endings tend to flatten into generic summaries. *Severity:* Strong warning (section scaffolding). *Recommended action:* Fix in Light, Medium, and Hard. Disclose only if preserved as blog packaging.
- **Headings in prose — Flagged.** *What it looks for:* markdown headings and plain title headings when prose should flow. *What happened here:* 15 headings ("# Workshops as Portals", "## In media res", "## Selling Portal Workshops", and so on). *Why it matters:* dense heading structure can read as assistant packaging. *Severity:* Context warning (headings). *Recommended action:* Preserve in Light if purposeful and disclosed — conventional for a how-to consulting blog post. Fix in Medium and Hard.
- **Vocabulary diversity — Flagged.** *What it looks for:* repetitive vocabulary in longer text. *What happened here:* type-token ratio 0.303 (802 unique / 2644 total; target >0.40). *Why it matters:* low variety can make longer prose feel mechanically produced. *Severity:* Context warning. *Recommended action:* Preserve in Light if purposeful and disclosed (consultancy essays often loop on a few key words — workshop, client, clarity, scope); fix in Medium and Hard.
- **Triad density — Flagged.** *What it looks for:* whether three-part list structures are overused. *What happened here:* 7 triads, including "improvisation, sparring, discussion", "conversation prompts, guides, pointers", "prep work, research, some kind of debrief". *Why it matters:* too many three-parters create a recognisable generated cadence. *Severity:* Context warning. *Recommended action:* Preserve in Light if purposeful and disclosed; fix in Medium and Hard.

### Full check table

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Em dashes | Clear | Em dash punctuation, a strong current AI-style signal. | No issue found. | Em dashes are a strong style fingerprint in generated prose. | — | None |
| Clustered AI vocabulary | Clear | Whether generic AI-associated words and phrases cluster. | No issue found. | Generic AI vocabulary becomes more suspicious when it clusters. | — | None |
| Nonliteral land/surface phrasing | Clear | Abstract uses such as ideas landing, concerns surfacing. | No issue found. | Abstract land/surface phrasing can make ideas sound managed. | — | None |
| AI pressure from stacked signals | Flagged | Several weaker AI-writing signals appearing together. | Stacked: manufactured insight + headings in prose. Score 5/4. +1 from clustered vocabulary. | Several weak signals together can feel machine-packaged. | Composite | Address underlying signals |
| Manufactured insight framing | Flagged | Phrases that perform hidden depth without earning it. | Found 2: "but here's", "but here's". | Performs depth without specific evidence. | Strong warning | Fix in Light, Medium, and Hard. Disclose only if explicitly preserved. |
| Generic staccato emphasis | Flagged | Repeated short dramatic sentences as generic emphasis. | Sequence of 4 consecutive short sentences. | Repeated short beats can sound generated. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Mechanical repeated sentence starts | Clear | Repeated openings that read like template rhythm. | No issue found. | Mechanical openings can signal templates. | — | None |
| Assistant residue | Clear | Assistant-like collaboration phrases or chat residue. | No issue found. | Makes text look like chat output. | — | None |
| Curly quotes | Clear | Curly quotation marks when plain output is expected. | No issue found. | Matters when output is expected to be plain. | — | None |
| Sentence rhythm variance | Clear | Whether sentence lengths are too uniform. | No issue found. | Low variation feels mechanical. | — | None |
| Generic promotional language | Clear | Stock hype and sales-like adjectives. | No issue found. | Stock hype weakens credibility. | — | None |
| Inflated significance | Flagged | Language that makes ordinary claims sound historically important. | Found: "crucial". | Makes ordinary claims artificially momentous. | Strong warning | Fix in Light, Medium, and Hard. Disclose only if explicitly preserved. |
| Contrived contrast | Clear | Not-X-but-Y, beyond-X, less-X-than-Y reveals. | No issue found. | Creates fake reveals instead of direct claims. | — | None |
| Avoiding plain 'is' | Clear | Inflated replacements such as serves as, functions as. | No issue found. | Turns simple claims into pseudo-analysis. | — | None |
| Filler phrases | Clear | Stock padding such as in order to, it is worth noting. | No issue found. | Adds polish without information. | — | None |
| Generic conclusion | Clear | Empty endings such as the future looks bright. | No issue found. | Makes endings feel templated. | — | None |
| False balance or concession | Clear | Fake both-sides framing that avoids taking a position. | No issue found. | Hides the writer's actual position. | — | None |
| Placeholder residue | Clear | Unfilled template markers and instructions. | No issue found. | Signals unfinished generated text. | — | None |
| Soft explainer scaffolding | Clear | Phrases that announce structure instead of making a point. | No issue found. | Announces structure instead of writing. | — | None |
| Vague 'this/that' starts | Clear | Repeated vague subjects such as This highlights. | No issue found. | Blurs the actual subject. | — | None |
| Decorative three-part lists | Flagged | Forced triads used as rhythm rather than substance. | 1 abstract triad: "improvisation, sparring, discussion". | Triads can create rhythm without substance. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Tacked-on -ing analysis | Clear | Trailing -ing clauses that pretend to analyse. | No issue found. | Pretend analysis without meaning. | — | None |
| Ghost/spectral atmosphere | Clear | Clichéd ghost, shadow, whisper, echo language. | No issue found. | Stock spectral language feels borrowed. | — | None |
| Generic quiet/still mood | Clear | Overused quiet, still, soft, hushed atmosphere. | No issue found. | Generic literary atmosphere. | — | None |
| Template rhetorical questions | Clear | Article-style questions followed by obvious answers. | No issue found. | Simulates engagement without inquiry. | — | None |
| Excessive list formatting | Clear | Whether prose has been over-converted into bullets. | No issue found. | Makes prose feel like notes or slides. | — | None |
| Decorative Unicode | Clear | Symbols and decorative punctuation. | No issue found. | Looks like generated formatting. | — | None |
| Unearned dramatic transitions | Clear | Generic turning points such as something shifted. | No issue found. | Claims drama the prose has not built. | — | None |
| Formulaic openers | Clear | Generated openings such as at its core. | No issue found. | Feels assembled from templates. | — | None |
| Signposted conclusion | Flagged | Explicit conclusion labels and summary signposts. | Found 1: "## Conclusion". | Flattens endings into generic summaries. | Strong warning | Fix in Light, Medium, and Hard. Disclose only if explicitly preserved. |
| Headings in prose | Flagged | Markdown headings and plain title headings when prose should flow. | 15 headings ("# Workshops as Portals", "## In media res", "## Selling Portal Workshops", "## Jam Sessions", "## Conversation prompts…"). | Heading density can feel like assistant packaging. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Corporate AI-speak | Clear | Vague delivery, alignment, outcomes, cross-functional clichés. | No issue found. | Hides specific work behind operational language. | — | None |
| Repeated 'This...' chains | Clear | Several consecutive sentences beginning with vague This. | No issue found. | Generic analysis with weak subject control. | — | None |
| Excessive hedging | Clear | Evasive qualification and impersonal uncertainty. | No issue found. | Weakens stance. | — | None |
| Countdown negation | Clear | Repeated no/not/cannot setups building to a reveal. | No issue found. | Synthetic reveal structure. | — | None |
| Dense negation | Clear | Whether negation markers are unusually dense. | No issue found. | Over-frames around what something is not. | — | None |
| Paragraph length uniformity | Clear | Whether paragraphs are suspiciously similar in length. | No issue found. | Signals generated structure. | — | None |
| Tidy paragraph endings | Clear | Repeated miniature conclusions at paragraph ends. | No issue found. | Makes paragraphs feel over-resolved. | — | None |
| Bland critical template | Clear | Generic review language. | No issue found. | Replaces concrete judgment with portable review phrases. | — | None |
| Rubric echoing | Clear | Assignment or rubric phrasing leaking into prose. | No issue found. | Sounds like assignment compliance. | — | None |
| Vocabulary diversity | Flagged | Unusually repetitive vocabulary in longer text. | Type-token ratio 0.303 (802 unique / 2644 total; target >0.40). | Low variety can feel mechanically produced. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Triad density | Flagged | Whether three-part list structures are overused. | 7 triads, including "improvisation, sparring, discussion", "conversation prompts, guides, pointers", "prep work, research, some kind of debrief". | Too many three-parters create generated cadence. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Repeated section scaffolding | Clear | Repeated section labels or templates. | No issue found. | Makes pieces feel assembled from a template. | — | None |

---

**Reading the result:** the high-confidence number is mostly carried by genre conventions (heavy headings, signposted conclusion, low TTR from a tightly looped vocabulary of *workshop / client / clarity*) plus two real strong-warning hits — the doubled "but here's" reveal and the bare word "crucial". A Light-mode review would probably preserve the headings, the staccato run, and most of the triads under the purpose test, and fix the manufactured-insight phrasing.

Do you want a rewrite, a recommendation on intensity, or a saved Markdown report?