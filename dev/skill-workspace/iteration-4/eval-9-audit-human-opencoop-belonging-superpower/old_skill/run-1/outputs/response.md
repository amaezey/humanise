## Action: Audit

### Audit report

**Summary:** 4 of 43 checks were flagged for AI-style writing patterns.

**Confidence:** Medium. Several signs of AI-like writing appeared, but the evidence is pattern-based and should be read in context. Basis: 1 strong-warning signal and 3 context-sensitive signals. This is a confidence assessment about AI-writing signs, not an authorship verdict.

**AI-pressure explanation:** AI-pressure looks at accumulation — weaker patterns that can be harmless alone but more meaningful when they appear together. Here only headings-in-prose stacked into the pressure signal, and the score landed at 2/4 (below threshold), so the accumulation check stayed clear. The flagged items are isolated rather than reinforcing each other into a machine-packaged feel.

**Main issues found**

- **Curly quotes** — Flagged. *What it looks for:* curly quotation marks when plain output is expected. *What happened here:* found 42 curly quote(s) (e.g. `you've`, `it's`, the bolded pattern names with curly quotes around them). *Why this matters:* curly quotes are not proof of AI, but they matter when the output is expected to be plain cleaned text. *Severity:* Context warning. *Recommended action:* Preserve in Light if purposeful (disclose). Fix in Medium and Hard. — In this case the source is a published web article where typographic quotes are conventional, so this is almost certainly a publishing artefact rather than an AI tell.
- **Filler phrases** — Flagged. *What it looks for:* stock padding such as "in order to" or "it is worth noting". *What happened here:* found 1 instance: *"in order to avoid any ambiguity"* (Pattern 3 paragraph). *Why this matters:* filler phrases add polish without information. *Severity:* Strong warning. *Recommended action:* Fix in Light, Medium, and Hard. Disclose only if explicitly preserved. — A single "in order to" in a 1,300-word essay is light evidence, but the phrase tightens to "to" with no loss of meaning.
- **Headings in prose** — Flagged. *What it looks for:* markdown headings and plain title headings when prose should flow. *What happened here:* found 1 heading: `# Belonging is a superpower - Patterns for decentralised organising`. *Why this matters:* headings can make prose feel packaged by an assistant rather than written as a continuous piece. *Severity:* Context warning. *Recommended action:* Preserve in Light if purposeful (disclose). Fix in Medium and Hard. — This is the article's own title imported from the source HTML, not assistant scaffolding. Almost certainly a packaging artefact.
- **Triad density** — Flagged. *What it looks for:* whether three-part list structures are overused across the piece. *What happened here:* found 4 triads, including *"non-hierarchical group, with open, inclusive values and aspirations"*, *"worthiness within the group, belonging can crumble, with it goes organisational"*, *"how it works, what it finds acceptable, what it will not"*, plus one more. *Why this matters:* too many three-part lists create a recognisable generated cadence. *Severity:* Context warning. *Recommended action:* Preserve in Light if purposeful (disclose). Fix in Medium and Hard. — In this draft, the triads are tied to specific content (group attributes, escalating consequences, norms enumerated) rather than decorative balance, so they read as substance triads rather than rhythm triads.

**Full check table**

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Em dashes | Clear | Em dash punctuation, a strong current AI-style signal. | No issue found. | Em dashes are a strong style fingerprint in generated prose. | Em dash | None |
| Clustered AI vocabulary | Clear | Whether generic AI-associated words and phrases cluster. | No issue found. | Clustering of AI-associated vocabulary is more suspicious than isolated use. | Strong warning | None |
| Nonliteral land/surface phrasing | Clear | Abstract uses such as ideas landing or concerns surfacing. | No issue found. | Abstract land/surface phrasing makes ordinary ideas sound artificially managed. | Strong warning | None |
| AI pressure from stacked signals | Clear | Several weaker signals appearing together. | No issue found. | Stacked weak signals can make a draft feel machine-packaged. | Context warning | None |
| Manufactured insight framing | Clear | Phrases performing hidden depth or secret significance. | No issue found. | Manufactured insight performs depth without earning it. | Strong warning | None |
| Generic staccato emphasis | Clear | Repeated short dramatic sentences as generic emphasis. | No issue found. | Repeated short emphasis beats can sound generated. | Context warning | None |
| Mechanical repeated sentence starts | Clear | Repeated sentence openings that read like template rhythm. | No issue found. | Repeated openings can signal template rhythm. | Context warning | None |
| Assistant residue | Clear | Assistant-like collaboration phrases or chat residue. | No issue found. | Residue makes the text look like chat output. | Hard failure | None |
| Curly quotes | Flagged | Curly quotation marks when plain output is expected. | Found 42 curly quotes. | Matters when plain cleaned text is expected; otherwise a packaging artefact. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Sentence rhythm variance | Clear | Whether sentence lengths are too uniform across longer prose. | No issue found. | Low variation makes paragraphs feel mechanical. | Context warning | None |
| Generic promotional language | Clear | Stock hype and sales-like adjectives. | No issue found. | Stock hype weakens credibility. | Context warning | None |
| Inflated significance | Clear | Language making ordinary claims sound historically important. | No issue found. | Inflation makes ordinary claims sound momentous. | Strong warning | None |
| Contrived contrast | Clear | Not-X-but-Y, beyond-X, less-X-than-Y reveal structures. | No issue found. | Creates a fake reveal instead of a direct claim. | Strong warning | None |
| Avoiding plain 'is' | Clear | Inflated replacements such as serves as or functions as. | No issue found. | Turns simple claims into pseudo-analysis. | Strong warning | None |
| Filler phrases | Flagged | Stock padding such as "in order to" or "it is worth noting". | Found 1: "in order to". | Adds polish without information. | Strong warning | Fix in Light, Medium, and Hard. Disclose only if explicitly preserved. |
| Generic conclusion | Clear | Empty endings such as "the future looks bright". | No issue found. | Makes the ending feel templated. | Hard failure | None |
| False balance or concession | Clear | Fake both-sides framing avoiding a position. | No issue found. | Hides the writer's actual position. | Strong warning | None |
| Placeholder residue | Clear | Unfilled template markers and placeholder instructions. | No issue found. | Signals unfinished generated text. | Hard failure | None |
| Soft explainer scaffolding | Clear | Phrases that announce structure instead of making a point. | No issue found. | Announces structure instead of doing the work. | Strong warning | None |
| Vague 'this/that' starts | Clear | Repeated vague subjects such as "This highlights". | No issue found. | Blurs the actual subject. | Context warning | None |
| Decorative three-part lists | Clear | Forced triads used as rhythm rather than substance. | No issue found. | Decorative triads create artificial rhythm. | Context warning | None |
| Tacked-on -ing analysis | Clear | Trailing -ing clauses pretending to analyse. | No issue found. | Often pretend to analyse while adding little. | Strong warning | None |
| Ghost/spectral atmosphere | Clear | Clichéd ghost, shadow, whisper, echo language. | No issue found. | Stock spectral language can feel borrowed. | Context warning | None |
| Generic quiet/still mood | Clear | Overused quiet/still/soft/hushed atmosphere. | No issue found. | Creates generic literary atmosphere. | Context warning | None |
| Template rhetorical questions | Clear | Article-style questions followed by obvious answers. | No issue found. | Simulates engagement without inquiry. | Context warning | None |
| Excessive list formatting | Clear | Whether prose has been over-converted into bullets. | No issue found. | Too much list formatting feels like notes or slides. | Context warning | None |
| Decorative Unicode | Clear | Symbols and decorative punctuation as generated formatting. | No issue found. | Decorative symbols suggest generated output. | Context warning | None |
| Unearned dramatic transitions | Clear | Generic turning points such as "everything changed". | No issue found. | Claims drama the prose has not built. | Strong warning | None |
| Formulaic openers | Clear | Generated openings such as "at its core". | No issue found. | Makes paragraphs feel assembled from templates. | Strong warning | None |
| Signposted conclusion | Clear | Explicit conclusion labels and summary signposts. | No issue found. | Flattens endings into generic summaries. | Hard failure | None |
| Headings in prose | Flagged | Markdown headings and plain title headings when prose should flow. | Found 1 heading: `# Belonging is a superpower - Patterns for decentr…`. | Headings make prose feel packaged by an assistant. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Corporate AI-speak | Clear | Vague delivery, alignment, outcomes, cross-functional clichés. | No issue found. | Hides specific work behind vague operational language. | Strong warning | None |
| Repeated 'This...' chains | Clear | Several consecutive sentences beginning with vague "This" constructions. | No issue found. | Creates generic analysis and weak subject control. | Context warning | None |
| Excessive hedging | Clear | Evasive qualification and impersonal uncertainty. | No issue found. | Weakens stance and feels machine-neutral. | Strong warning | None |
| Countdown negation | Clear | Repeated no/not/cannot setups building toward a reveal. | No issue found. | Creates a synthetic reveal structure. | Context warning | None |
| Dense negation | Clear | Whether negation markers are unusually dense. | No issue found. | Over-frames around what the piece is not. | Context warning | None |
| Paragraph length uniformity | Clear | Whether paragraphs are suspiciously similar in length. | No issue found. | Similar paragraphs signal generated structure. | Context warning | None |
| Tidy paragraph endings | Clear | Repeated miniature conclusions at paragraph ends. | No issue found. | Makes paragraphs feel over-resolved. | Context warning | None |
| Bland critical template | Clear | Generic review language instead of concrete claims. | No issue found. | Replaces concrete judgment with portable phrases. | Strong warning | None |
| Rubric echoing | Clear | Assignment or rubric phrasing leaking into prose. | No issue found. | Sounds like assignment compliance. | Context warning | None |
| Vocabulary diversity | Clear | Unusually repetitive vocabulary in longer text. | No issue found. | Low variety feels mechanical. | Context warning | None |
| Triad density | Flagged | Whether three-part list structures are overused. | Found 4 triads, including "non-hierarchical group, with open, inclusive values and aspirations"; "worthiness within the group, belonging can crumble, with it goes organisational"; "how it works, what it finds acceptable, what it will not"; plus 1 more. | Too many three-part lists create a recognisable generated cadence. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Repeated section scaffolding | Clear | Repeated section labels or structural templates. | No issue found. | Makes the whole piece feel template-assembled. | Strong warning | None |

**Read in context:** This is a 2017 practitioner essay reporting on a workshop, and three of the four flags (curly quotes, the article-title heading, the substance-bound triads) look like publishing artefacts or genre features rather than AI tells. The single strong-warning hit ("in order to") is a real but minor filler. The piece carries clear voice markers — first-person reactions, dated cultural references, registered opinion ("Brilliant advice which might be hard for some egos to hear") — that the AI-pressure check correctly recognised as keeping the draft below the accumulation threshold.

> Do you want a rewrite, a recommendation on intensity, or a saved Markdown report?