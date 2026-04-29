## Action: Audit

### Summary
7 of 43 checks were flagged for AI-style writing patterns.

### Confidence
**Medium.** Several signs of AI-like writing appeared, but the evidence is pattern-based and should be read in context.
**Basis:** 2 strong AI-writing signals; 5 context-sensitive signals.
*Note: This is a confidence assessment about AI-writing signs, not an authorship verdict. Several flags here look like genre artefacts of a long literary essay republished from a magazine source (em dashes as authorial style, curly quotes from source HTML, triads inflated by triadic book titles like "Faith, Future, and America's Final Frontier").*

### AI-pressure explanation
AI-pressure looks for accumulation: weaker patterns that may be harmless alone but become more meaningful when they appear together. Here the stacked signals were headings in prose, plus 1 point from clustered AI vocabulary. The pressure score was 3/4, so this combined check stayed clear — the piece did not cross the threshold where weak signals fuse into machine-packaged rhythm.

### Main issues found

- **Em dashes:** Flagged. Found 20 em dashes. Em dashes are a strong style fingerprint in current generated prose, especially as default punctuation. *Severity: em dash.* Recommended action: Preserve in Light only with disclosure. Fix in Medium and Hard.
- **Curly quotes:** Flagged. Found 147 curly quotation marks. Not proof of AI, but matters when output is expected to be plain cleaned text. *Severity: context warning.* Recommended action: Preserve in Light if purposeful (disclose). Fix in Medium and Hard. *Likely a source-copy artefact rather than a generated tell.*
- **Generic promotional language:** Flagged. Found "breathtaking" ("they are breathtaking" — describing IMAX moon footage). Stock hype weakens credibility. *Severity: context warning.* Recommended action: Preserve in Light if purposeful (disclose). Fix in Medium and Hard.
- **Avoiding plain 'is':** Flagged. Found 1: "features" (the top-grossing films "disproportionately features big-budget…"). Inflated replacements turn simple claims into pseudo-analysis. *Severity: strong warning.* Recommended action: Fix in Light, Medium, and Hard.
- **Headings in prose:** Flagged. Found 3 headings ("# First Men and Original Sins", "### Faith and the American Space Program", "# First Men and Original Sins"). Headings can make prose feel assistant-packaged. *Severity: context warning.* Recommended action: Preserve in Light if purposeful (disclose). Fix in Medium and Hard. *These are magazine-article packaging (title and review-block headers), not section scaffolding inside the essay.*
- **Vocabulary diversity:** Flagged. Type-token ratio 0.379 (1,469 unique / 3,876 total; target > 0.40). Low variety can make long prose feel mechanical. *Severity: context warning.* Recommended action: Preserve in Light if purposeful (disclose). Fix in Medium and Hard. *Marginal miss, partly driven by recurring proper nouns (Apollo, NASA, Bonestell, von Braun, Newell, Oliver, Armstrong) over a 3,876-word essay.*
- **Triad density:** Flagged. Found 24 triads, including "the sacred, the profane, the american space program", "faith, future, america", "engineering, technology, materialism". *Severity: context warning.* Recommended action: Preserve in Light if purposeful (disclose). Fix in Medium and Hard. *Several triads come from quoted book subtitles; others are authentic rhetorical cadence in a literary register.*

### Full check table

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Em dashes | Flagged | Em dash punctuation, a strong current AI-style signal. | Found 20 em dashes. | Em dashes are a strong fingerprint of generated prose when used as default punctuation. | Em dash | Preserve in Light only with disclosure. Fix in Medium and Hard. |
| Clustered AI vocabulary | Clear | Whether generic AI-associated words and phrases cluster together. | No issue found. | Generic AI words become more suspicious when clustered. | — | None |
| Nonliteral land/surface phrasing | Clear | Abstract uses such as ideas landing or concerns surfacing. | No issue found. | Abstract land/surface phrasing makes ideas sound artificially packaged. | — | None |
| AI pressure from stacked signals | Clear | Several weaker AI signals appearing together. | No issue found. | Stacked weak signals can make a draft feel machine-packaged. | — | None |
| Manufactured insight framing | Clear | Phrases performing hidden depth or secret significance. | No issue found. | Performs depth without earning it. | — | None |
| Generic staccato emphasis | Clear | Repeated short dramatic sentences as emphasis. | No issue found. | Generated rhythm rather than natural pacing. | — | None |
| Mechanical repeated sentence starts | Clear | Repeated sentence openings reading like template rhythm. | No issue found. | Signals template rhythm. | — | None |
| Assistant residue | Clear | Assistant-like collaboration phrases or chat residue. | No issue found. | Makes text look like chat output. | — | None |
| Curly quotes | Flagged | Curly quotation marks when plain output is expected. | Found 147 curly quotes. | Matters when output is expected to be plain text. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Sentence rhythm variance | Clear | Whether sentence lengths are too uniform. | No issue found. | Low variation feels mechanical. | — | None |
| Generic promotional language | Flagged | Stock hype and sales-like adjectives. | Found: "breathtaking". | Stock hype weakens credibility. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Inflated significance | Clear | Language making ordinary claims sound historically important. | No issue found. | Makes ordinary claims sound momentous. | — | None |
| Contrived contrast | Clear | not-X-but-Y, beyond-X, less-X-than-Y reveal structures. | No issue found. | Creates a fake reveal. | — | None |
| Avoiding plain 'is' | Flagged | Inflated replacements such as serves as, functions as, features. | Found 1: "features". | Turns simple claims into pseudo-analysis. | Strong warning | Fix in Light, Medium, and Hard. Disclose only if explicitly preserved. |
| Filler phrases | Clear | Stock padding such as in order to, it is worth noting. | No issue found. | Adds polish without information. | — | None |
| Generic conclusion | Clear | Empty endings such as the future looks bright. | No issue found. | Templated ending. | — | None |
| False balance or concession | Clear | Fake both-sides framing. | No issue found. | Hides the writer's actual position. | — | None |
| Placeholder residue | Clear | Unfilled template markers. | No issue found. | Signals unfinished generation. | — | None |
| Soft explainer scaffolding | Clear | Phrases announcing structure instead of making a point. | No issue found. | Announces structure instead of doing the work. | — | None |
| Vague 'this/that' starts | Clear | Repeated vague subjects such as This highlights. | No issue found. | Blurs the actual subject. | — | None |
| Decorative three-part lists | Clear | Forced triads used for rhythm rather than substance. | No issue found. | Artificial rhythm. | — | None |
| Tacked-on -ing analysis | Clear | Trailing -ing clauses pretending to analyse. | No issue found. | Pretends analysis while adding little. | — | None |
| Ghost/spectral atmosphere | Clear | Clichéd ghost, shadow, whisper language. | No issue found. | Borrowed atmosphere. | — | None |
| Generic quiet/still mood | Clear | Overused quiet, still, soft, hushed atmosphere. | No issue found. | Generic literary atmosphere. | — | None |
| Template rhetorical questions | Clear | Article-style questions followed by obvious answers. | No issue found. | Simulates engagement without inquiry. | — | None |
| Excessive list formatting | Clear | Prose over-converted into bullets or numbered lists. | No issue found. | Feels like generated notes. | — | None |
| Decorative Unicode | Clear | Symbols and decorative punctuation. | No issue found. | Looks like generated formatting. | — | None |
| Unearned dramatic transitions | Clear | Generic turning points such as something shifted. | No issue found. | Claims drama not built. | — | None |
| Formulaic openers | Clear | Generated openings such as at its core. | No issue found. | Templated paragraphs. | — | None |
| Signposted conclusion | Clear | Explicit conclusion labels and summary signposts. | No issue found. | Flattens endings into summary. | — | None |
| Headings in prose | Flagged | Markdown headings or plain title headings when prose should flow. | Found 3 headings: "# First Men and Original Sins", "### Faith and the American Space Program", "# First Men and Original Sins". | Headings make prose feel assistant-packaged. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Corporate AI-speak | Clear | Vague delivery, alignment, outcomes, cross-functional clichés. | No issue found. | Hides specific work behind operational language. | — | None |
| Repeated 'This...' chains | Clear | Several consecutive sentences beginning with vague This. | No issue found. | Generic analysis. | — | None |
| Excessive hedging | Clear | Evasive qualification and impersonal uncertainty. | No issue found. | Weakens stance. | — | None |
| Countdown negation | Clear | Repeated no/not/cannot setups building to a reveal. | No issue found. | Synthetic reveal. | — | None |
| Dense negation | Clear | Whether negation markers are unusually dense. | No issue found. | Over-framed around what it is not. | — | None |
| Paragraph length uniformity | Clear | Whether paragraphs are suspiciously similar in length. | No issue found. | Signals generated structure. | — | None |
| Tidy paragraph endings | Clear | Repeated miniature conclusions at paragraph ends. | No issue found. | Over-resolved paragraphs. | — | None |
| Bland critical template | Clear | Generic review language instead of concrete claims. | No issue found. | Replaces judgment with portable review phrases. | — | None |
| Rubric echoing | Clear | Assignment or rubric phrasing leaking into prose. | No issue found. | Sounds like assignment compliance. | — | None |
| Vocabulary diversity | Flagged | Unusually repetitive vocabulary in longer text. | Type-token ratio: 0.379 (1,469 unique / 3,876 total; target >0.40). | Low variety can feel repetitive. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Triad density | Flagged | Whether three-part list structures are overused. | Found 24 triads, including "the sacred, the profane, the american space program", "faith, future, america", "engineering, technology, materialism", plus 21 more. | Too many three-part lists create a generated cadence. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Repeated section scaffolding | Clear | Repeated section labels or structural templates. | No issue found. | Templated piece. | — | None |

---

Do you want a rewrite, a recommendation on intensity, or a saved Markdown report?