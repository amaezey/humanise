## Action: Audit

### Audit report

**Summary:** 6 of 43 checks were flagged for AI-style writing patterns.

**Confidence:** Medium. Several signs of AI-like writing appeared, but the evidence is pattern-based and should be read in context.
**Basis:** 1 strong AI-writing signal; 5 context-sensitive signals.
*Note: this is a confidence assessment about AI-writing signs, not an authorship verdict.*

**AI-pressure explanation:** AI-pressure looks for accumulation — weaker patterns that may be harmless alone but become more meaningful when they appear together. Here the stacked signals were contrived contrast framing. The accumulation score landed at 2/4, so this check stayed clear: the signals did not stack into a machine-packaged feel.

**Source caveat (worth flagging before reading the table):** the input contains extraction artifacts from the web page — three paragraphs repeat verbatim three times each ("Who is your everyone? Chess masters scarcely surround themselves..."; "However many more people come, your time and its passions..."; "Most humans who were ever alive lived inside a single culture..."). These are publishing/scraping artifacts, not part of Dillard's prose, and they materially inflate the triad count, the anaphora count ("However" run), and the type-token ratio. Several of the flags below are partly an artefact of those duplicated blocks rather than the writing itself.

### Main issues found

- **Contrived contrast — Strong warning.** What it looks for: not-X-but-Y, beyond-X, less-X-than-Y, and related reveal structures. What happened here: 4 contrived contrast / reframe patterns. Why this matters: contrived contrast can create a fake reveal instead of making a direct, supported claim. Recommended action: fix in Light, Medium, and Hard unless explicitly preserved with disclosure. *Likely-purposeful note:* in Dillard the reveal structures are doing real rhetorical work (climbing-the-beanstalk reframes, "not just there, but here"); the purpose test would lean toward preserve in a Light pass on a literary essay.
- **Generic staccato emphasis — Context warning.** What it looks for: repeated short dramatic sentences used as generic emphasis. What happened here: a sequence of 5 consecutive short sentences. Why this matters: repeated short emphasis beats can make prose sound generated rather than naturally paced. Recommended action: preserve in Light if purposeful (disclose); fix in Medium and Hard. *Likely-purposeful note:* the staccato run ("Not a funeral. Forget funeral. A big birthday party.") is comic timing inside an inventory of ambitions, characteristic literary cadence.
- **Mechanical repeated sentence starts — Context warning.** What it looks for: repeated sentence openings that read like template rhythm. What happened here: 5 consecutive sentences starting with "however". Why this matters: mechanical repeated openings can signal template rhythm instead of intentional rhetoric. Recommended action: preserve in Light if purposeful (disclose); fix in Medium and Hard. *Likely-purposeful note:* this is the "However hypnotized... However dead... However many more people come..." passage — deliberate anaphora — and is also amplified by the duplicated-paragraph extraction artifact.
- **Curly quotes — Context warning.** What it looks for: curly quotation marks when plain output is expected. What happened here: 18 curly quotes. Why this matters: curly quotes are not proof of AI, but they matter when the output is expected to be plain cleaned text. Recommended action: preserve in Light if purposeful (disclose); fix in Medium and Hard. *Likely-purposeful note:* this is published literary prose; curly quotes are correct typography, not an AI tell.
- **Vocabulary diversity — Context warning.** What it looks for: unusually repetitive vocabulary in longer text. What happened here: type-token ratio 0.372 (689 unique / 1851 total; target > 0.40). Why this matters: low vocabulary variety can make longer prose feel repetitive and mechanically produced. Recommended action: preserve in Light if purposeful (disclose); fix in Medium and Hard. *Likely-purposeful note:* the score is dragged down by the three repeated paragraphs in the source extraction. The actual essay leans on a tight motif vocabulary (weave, warp, weft, fabric, peoples, time) by design.
- **Triad density — Context warning.** What it looks for: whether three-part list structures are overused across the piece. What happened here: 23 triads, including "hopes, dreams, values", "restaurants and their staffs, drive the best car, vacation on Tenerife", "to spear the seal, intimidate the enemy, be a big man", plus 20 more. Why this matters: too many three-part lists create a recognisable generated cadence. Recommended action: preserve in Light if purposeful (disclose); fix in Medium and Hard. *Likely-purposeful note:* Dillard is cataloguing the spread of human ambition across cultures — the lists are an intentional inventory device, not decorative balance. A clean count after removing the extraction-duplicated paragraphs would be lower.

### Full check table

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Em dashes | Clear | Em dash punctuation, a strong current AI-style signal. | No issue found. | Em dashes are now a strong style fingerprint in generated prose. | — | None |
| Clustered AI vocabulary | Clear | Generic AI-associated words and phrases clustering together. | No issue found. | Generic AI-associated words become more suspicious when they cluster. | — | None |
| Nonliteral land/surface phrasing | Clear | Abstract uses such as ideas landing or concerns surfacing. | No issue found. | Abstract land/surface phrasing often makes ordinary ideas sound artificially managed. | — | None |
| AI pressure from stacked signals | Clear | Several weaker AI-writing signals appearing together. | No issue found. | Weak signals together can make a draft feel machine-packaged. | — | None |
| Manufactured insight framing | Clear | Phrases that perform hidden depth without earning it. | No issue found. | Manufactured insight performs depth without specifics. | — | None |
| Generic staccato emphasis | Flagged | Repeated short dramatic sentences used as emphasis. | Sequence of 5 consecutive short sentences. | Repeated short beats can sound generated rather than paced. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Mechanical repeated sentence starts | Flagged | Repeated sentence openings that read like template rhythm. | 5 consecutive sentences starting with "however". | Mechanical openings can signal template rhythm. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Assistant residue | Clear | Assistant-like collaboration phrases and chat residue. | No issue found. | Assistant residue makes text look like chat output. | — | None |
| Curly quotes | Flagged | Curly quotation marks when plain output is expected. | 18 curly quotes. | Curly quotes matter when plain cleaned text is expected. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Sentence rhythm variance | Clear | Whether sentence lengths are too uniform. | No issue found. | Low rhythm variation feels mechanical. | — | None |
| Generic promotional language | Clear | Stock hype and sales-like adjectives. | No issue found. | Stock hype weakens credibility. | — | None |
| Inflated significance | Clear | Language that makes ordinary claims sound historically important. | No issue found. | Inflated importance sounds artificially momentous. | — | None |
| Contrived contrast | Flagged | not-X-but-Y, beyond-X, less-X-than-Y, related reveal structures. | 4 contrived contrast/reframe patterns. | Creates a fake reveal instead of a direct claim. | Strong warning | Fix in Light, Medium, and Hard. Disclose only if explicitly preserved. |
| Avoiding plain 'is' | Clear | Inflated replacements such as serves as, functions as. | No issue found. | Avoiding plain 'is' inflates simple claims. | — | None |
| Filler phrases | Clear | Stock padding such as in order to. | No issue found. | Filler adds polish without information. | — | None |
| Generic conclusion | Clear | Empty endings such as the future looks bright. | No issue found. | Generic conclusions feel templated. | — | None |
| False balance or concession | Clear | Fake both-sides framing that avoids a position. | No issue found. | False balance hides the writer's actual position. | — | None |
| Placeholder residue | Clear | Unfilled template markers and placeholder instructions. | No issue found. | Placeholder residue signals unfinished templated text. | — | None |
| Soft explainer scaffolding | Clear | Phrases that announce structure instead of making a point. | No issue found. | Soft scaffolding announces structure instead of doing work. | — | None |
| Vague 'this/that' starts | Clear | Repeated vague subjects such as This highlights. | No issue found. | Vague this/that openings blur the subject. | — | None |
| Decorative three-part lists | Clear | Forced triads used as rhythm rather than substance. | No issue found. | Decorative triads create artificial rhythm. | — | None |
| Tacked-on -ing analysis | Clear | Trailing -ing clauses that pretend to analyse. | No issue found. | Tacked-on -ing clauses pretend to analyse without adding meaning. | — | None |
| Ghost/spectral atmosphere | Clear | Clichéd ghost, shadow, whisper, echo language. | No issue found. | Stock spectral language sounds borrowed. | — | None |
| Generic quiet/still mood | Clear | Overused quiet, still, soft, hushed atmosphere. | No issue found. | Overused quiet/still language is generic. | — | None |
| Template rhetorical questions | Clear | Article-style questions followed by obvious answers. | No issue found. | Template questions simulate engagement without inquiry. | — | None |
| Excessive list formatting | Clear | Whether prose has been over-converted into bullets. | No issue found. | Too much list formatting looks like generated notes. | — | None |
| Decorative Unicode | Clear | Symbols and decorative punctuation. | No issue found. | Decorative symbols look like generated formatting. | — | None |
| Unearned dramatic transitions | Clear | Generic turning points such as something shifted. | No issue found. | Unearned transitions claim drama the prose has not built. | — | None |
| Formulaic openers | Clear | Generated openings such as at its core. | No issue found. | Formulaic openings feel assembled from templates. | — | None |
| Signposted conclusion | Clear | Explicit conclusion labels and summary signposts. | No issue found. | Conclusion signposts flatten the ending. | — | None |
| Headings in prose | Clear | Markdown headings and plain title headings when prose should flow. | No issue found. | Headings make prose feel packaged by an assistant. | — | None |
| Corporate AI-speak | Clear | Vague delivery, alignment, outcomes, cross-functional clichés. | No issue found. | Corporate AI-speak hides specifics behind operational language. | — | None |
| Repeated 'This...' chains | Clear | Several consecutive sentences starting with vague This. | No issue found. | Repeated vague This sentences create generic analysis. | — | None |
| Excessive hedging | Clear | Evasive qualification and impersonal uncertainty. | No issue found. | Too much hedging weakens stance. | — | None |
| Countdown negation | Clear | Repeated no/not/cannot setups building toward a reveal. | No issue found. | Countdown negation creates a synthetic reveal. | — | None |
| Dense negation | Clear | Whether negation markers are unusually dense. | No issue found. | Dense negation over-frames a piece around what it is not. | — | None |
| Paragraph length uniformity | Clear | Whether paragraphs are suspiciously similar in length. | No issue found. | Similar lengths can signal generated structure. | — | None |
| Tidy paragraph endings | Clear | Repeated miniature conclusions at paragraph ends. | No issue found. | Repeated tidy endings feel over-resolved. | — | None |
| Bland critical template | Clear | Generic review language instead of concrete claims. | No issue found. | Bland critical language replaces concrete judgment. | — | None |
| Rubric echoing | Clear | Assignment or rubric phrasing leaking into prose. | No issue found. | Rubric echoing sounds like assignment compliance. | — | None |
| Vocabulary diversity | Flagged | Unusually repetitive vocabulary in longer text. | Type-token ratio 0.372 (689 unique / 1851 total; target > 0.40). | Low variety can make prose feel mechanical. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Triad density | Flagged | Whether three-part list structures are overused. | 23 triads, including "hopes, dreams, values"; "restaurants and their staffs, drive the best car, vacation on Tenerife"; "to spear the seal, intimidate the enemy, be a big man" — plus 20 more. | Too many triads create a recognisable cadence. | Context warning | Preserve in Light if purposeful (disclose). Fix in Medium and Hard. |
| Repeated section scaffolding | Clear | Repeated section labels or structural templates. | No issue found. | Repeated section structure feels assembled from a template. | — | None |

### Reading

The grader did its job: it counted what it counts. But on a literary essay by Annie Dillard, the six flags read like a textbook false-positive case. The contrived-contrast, anaphora, staccato, and triad signals are all firing on devices Dillard is using deliberately — the beanstalk reframes, the "However…" cascade, the comic "Not a funeral. Forget funeral.", the cross-cultural inventories of ambition. The curly quotes are correct typography for published prose. The vocabulary-diversity dip is partly the essay's chosen motif vocabulary and partly the duplicated paragraphs in the scrape. None of the structural-fingerprint checks (paragraph uniformity, scaffolding, soft scaffolding, tidy endings, formulaic openers, signposted conclusion, manufactured insight, generic conclusion) fired, and the AI-pressure stack stayed clear at 2/4.

If a Light-mode rewrite were ever requested on this piece, every flagged item above would be a strong candidate for **Recommended preserve** under the purpose test, with the contrived-contrast strong warning being the only thing worth a closer look case-by-case.

### Question

Do you want a rewrite (and at what intensity), a saved Markdown report, or to stop here?