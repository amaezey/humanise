## Action: Audit

### Summary
**7 of 43 checks flagged.** This is a personal-philosophy blog post, a voice-sensitive genre, so several context warnings are likely doing real rhetorical work. Read the issues with the purpose test in mind.

### Confidence
**High.** Multiple structural signals fired together, so this is a high-confidence diagnosis of AI-style *patterns* — not a verdict on authorship. (Independent context: this draft is human-authored, 2019, predating widespread LLM influence on prose. Several flags here will land as false positives once the purpose test is applied.)
**Basis:** 1 strong AI-writing signal, 6 context-sensitive signals, AI-pressure score reached 4/4.

### AI-pressure explanation
AI-pressure looks for accumulation: weaker patterns that may be harmless alone but become more meaningful when stacked. Here the stacked signals are **contrived contrast framing** + **headings in prose**. Score: 4/4 (flagged). In an AI-suspect draft this would suggest machine-packaged structure; in a known-human personal essay it suggests the writer leans on rhetorical contrast and a single H1 title.

### Main issues found

- **AI pressure from stacked signals** — Strong warning. *What happened:* contrived contrast framing + headings in prose stacked to 4/4. *Why this matters:* multiple weak signals combined can read machine-packaged. *Recommended action:* fix in Light/Medium/Hard unless explicitly preserved with disclosure. *Purpose test:* the H1 is article packaging from the source site; the contrast is rhetorical scaffolding for the central thesis. Both are explicable as genre conventions.

- **Mechanical repeated sentence starts** — Context warning. *What happened:* 3 consecutive sentences starting with "you" ("You love yourself enough to include yourself…" / "You love your life too much…" / "You have the courage…"). *Why this matters:* repeated openings can read as template rhythm. *Recommended action:* preserve in Light if purposeful (disclose); fix in Medium and Hard. *Purpose test:* this is deliberate anaphora — a known rhetorical device for second-person address in personal philosophy. Reads as intentional rhetoric, not autopilot.

- **Curly quotes** — Context warning. *What happened:* 38 curly quotes. *Why this matters:* not proof of AI, but matters when plain output is expected. *Recommended action:* preserve in Light; fix in Medium and Hard if the output should be plain text. *Purpose test:* these are smart quotes from the published web source (Forte Labs blog), not an AI tell. Safe to preserve unless cleaning for plain-text use.

- **Contrived contrast** — Strong warning. *What happened:* 1 not-X-but-Y/beyond-X/less-X-than-Y/correction structure. *Why this matters:* fake-reveal framing instead of direct claim. *Recommended action:* fix in Light/Medium/Hard unless explicitly preserved with disclosure. *Purpose test:* the script flagged one instance — at this density it reads as ordinary rhetorical contrast, not laundered reframing. Single instance is borderline; review the specific phrase before changing.

- **Decorative three-part lists** — Context warning. *What happened:* abstract triad "belonging, intimacy, connection" (also "needs for safety, belonging, intimacy, and connection"). *Why this matters:* abstract triads can create rhythm without substance. *Recommended action:* preserve in Light if purposeful (disclose); fix in Medium and Hard. *Purpose test:* these are Maslow-adjacent need terms; in a self-help/philosophy register they're conventional. Borderline — could be tightened to two terms or made concrete.

- **Headings in prose** — Context warning. *What happened:* 2 detected (the H1 title appears twice in the file because of frontmatter + heading). *Why this matters:* headings can make prose feel assistant-packaged. *Recommended action:* preserve in Light (web article packaging); fix in Medium and Hard if the output is meant to flow as continuous prose. *Purpose test:* this is the article's published title. Genuine packaging artefact, not AI scaffolding.

- **Triad density** — Context warning. *What happened:* 6 triads, including "leads to unnecessary sacrifice, martyrdom, even self-destruction"; "these two principles, service, pleasure"; "belonging, intimacy, connection have been met"; plus 3 more. *Why this matters:* heavy triad use creates a recognisable cadence. *Recommended action:* preserve in Light if purposeful (disclose); fix in Medium and Hard. *Purpose test:* triads are a Forte-voice signature — this is an actual stylistic habit, not generated cadence. Same caveat: if redrafting in Medium/Hard, redistribute some as pairs.

### Full check table

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Em dashes | Clear | Em dash punctuation, a strong current AI-style signal. | No issue found. | Em dashes are a strong style fingerprint in generated prose. | Strong warning (em dash class) | None |
| Clustered AI vocabulary | Clear | Whether generic AI-associated words and phrases cluster. | No issue found. | Generic AI words are more suspicious when they cluster. | Strong warning | None |
| Nonliteral land/surface phrasing | Clear | Abstract uses such as ideas landing, concerns surfacing. | No issue found. | Abstract land/surface phrasing sounds artificially managed. | Strong warning | None |
| AI pressure from stacked signals | Flagged | Several weaker signals appearing together. | Stacked: contrived contrast framing + headings in prose. Score 4/4. | Stacked weak signals can feel machine-packaged. | Strong warning | Fix in Light/Medium/Hard unless preserved with disclosure |
| Manufactured insight framing | Clear | Phrases performing hidden depth without earning it. | No issue found. | Performs depth without specific evidence. | Strong warning | None |
| Generic staccato emphasis | Clear | Repeated short dramatic sentences as emphasis. | No issue found. | Sounds generated rather than naturally paced. | Strong warning | None |
| Mechanical repeated sentence starts | Flagged | Repeated openings reading like template rhythm. | 3 consecutive sentences starting with 'you'. | Can signal template rhythm vs intentional rhetoric. | Context warning | Preserve in Light if purposeful (disclose); fix in Medium/Hard |
| Assistant residue | Clear | Assistant-like collaboration phrases. | No issue found. | Looks like chat output. | Hard failure | None |
| Curly quotes | Flagged | Curly quotation marks when plain output is expected. | 38 curly quotes. | Not proof of AI, matters for plain text output. | Context warning | Preserve in Light; fix in Medium/Hard if plain-text output |
| Sentence rhythm variance | Clear | Whether sentence lengths are too uniform. | No issue found. | Low variation feels mechanical. | Context warning | None |
| Generic promotional language | Clear | Stock hype and sales adjectives. | No issue found. | Weakens credibility. | Strong warning | None |
| Inflated significance | Clear | Language making ordinary claims sound momentous. | No issue found. | Sounds artificially momentous. | Strong warning | None |
| Contrived contrast | Flagged | not-X-but-Y, beyond-X, less-X-than-Y reveal structures. | 1 contrived contrast/reframe pattern. | Creates a fake reveal instead of a direct claim. | Strong warning | Fix in Light/Medium/Hard unless preserved with disclosure |
| Avoiding plain 'is' | Clear | Inflated replacements like serves as, functions as. | No issue found. | Turns simple claims into pseudo-analysis. | Strong warning | None |
| Filler phrases | Clear | Stock padding such as in order to. | No issue found. | Adds polish without information. | Strong warning | None |
| Generic conclusion | Clear | Empty endings such as the future looks bright. | No issue found. | Feels templated and interchangeable. | Hard failure | None |
| False balance or concession | Clear | Fake both-sides framing. | No issue found. | Hides the writer's actual position. | Strong warning | None |
| Placeholder residue | Clear | Unfilled template markers. | No issue found. | Signals unfinished generated text. | Hard failure | None |
| Soft explainer scaffolding | Clear | Phrases announcing structure instead of making a point. | No issue found. | Announces structure rather than doing work. | Strong warning | None |
| Vague 'this/that' starts | Clear | Repeated vague subjects such as This highlights. | No issue found. | Blurs the actual subject. | Strong warning | None |
| Decorative three-part lists | Flagged | Forced triads used as rhythm. | 1 abstract triad: "belonging, intimacy, connection". | Can create artificial rhythm without substance. | Context warning | Preserve in Light if purposeful (disclose); fix in Medium/Hard |
| Tacked-on -ing analysis | Clear | Trailing -ing clauses pretending to analyse. | No issue found. | Pretends to analyse while adding little. | Strong warning | None |
| Ghost/spectral atmosphere | Clear | Cliché ghost, shadow, whisper, echo language. | No issue found. | Sounds borrowed. | Context warning | None |
| Generic quiet/still mood | Clear | Overused quiet, still, soft, hushed atmosphere. | No issue found. | Generic literary atmosphere. | Context warning | None |
| Template rhetorical questions | Clear | Article-style questions followed by obvious answers. | No issue found. | Simulates engagement without inquiry. | Context warning | None |
| Excessive list formatting | Clear | Whether prose is over-converted into lists. | No issue found. | Feels like generated notes. | Context warning | None |
| Decorative Unicode | Clear | Symbols and decorative punctuation. | No issue found. | Looks like generated formatting. | Context warning | None |
| Unearned dramatic transitions | Clear | Generic turning points (something shifted). | No issue found. | Claims drama not built. | Context warning | None |
| Formulaic openers | Clear | Generated openings (at its core). | No issue found. | Feels assembled from templates. | Strong warning | None |
| Signposted conclusion | Clear | Explicit conclusion labels. | No issue found. | Flattens the ending. | Context warning | None |
| Headings in prose | Flagged | Markdown headings or plain title headings. | 2 headings (the H1 title, counted twice via frontmatter+heading). | Can feel assistant-packaged. | Context warning | Preserve in Light (article packaging); fix in Medium/Hard |
| Corporate AI-speak | Clear | Vague delivery, alignment, outcomes clichés. | No issue found. | Hides specific work. | Strong warning | None |
| Repeated 'This...' chains | Clear | Several consecutive sentences beginning with vague This. | No issue found. | Generic analysis, weak subject control. | Context warning | None |
| Excessive hedging | Clear | Evasive qualification. | No issue found. | Weakens stance. | Strong warning | None |
| Countdown negation | Clear | Repeated no/not/cannot setups building to a reveal. | No issue found. | Synthetic reveal structure. | Context warning | None |
| Dense negation | Clear | Whether negation markers are unusually dense. | No issue found. | Over-frames around what it is not. | Context warning | None |
| Paragraph length uniformity | Clear | Whether paragraphs are suspiciously similar in length. | No issue found. | Signals generated structure. | Context warning | None |
| Tidy paragraph endings | Clear | Repeated miniature conclusions at paragraph ends. | No issue found. | Feels over-resolved. | Context warning | None |
| Bland critical template | Clear | Generic review language. | No issue found. | Replaces concrete judgment. | Strong warning | None |
| Rubric echoing | Clear | Assignment or rubric phrasing. | No issue found. | Sounds like assignment compliance. | Context warning | None |
| Vocabulary diversity | Clear | Unusually repetitive vocabulary. | No issue found. | Feels mechanically produced. | Context warning | None |
| Triad density | Flagged | Whether three-part lists are overused across the piece. | 6 triads, including "leads to unnecessary sacrifice, martyrdom, even self-destruction"; "these two principles, service, pleasure"; "belonging, intimacy, connection have been met"; plus 3 more. | Too many triads create a recognisable generated cadence. | Context warning | Preserve in Light if purposeful (disclose); fix in Medium/Hard |
| Repeated section scaffolding | Clear | Repeated section labels or templates. | No issue found. | Feels assembled from a template. | Context warning | None |

### Verdict in plain English
The draft fires **one strong warning** (AI-pressure stacking, driven by a single contrived-contrast phrase plus the article H1) and **six context warnings**. In a voice-sensitive personal essay the triads, the "you/you/you" anaphora, and the H1 are defensible as voice and packaging. The contrast structure is a single instance and reads as ordinary rhetoric. The curly quotes are a source artefact, not a signal. Net: this scans as a writer with a triad-heavy, second-person-leaning style — exactly the kind of piece the purpose test is designed to protect.

### Next step
Do you want a rewrite (and at what intensity — Light, Medium, or Hard), an intensity recommendation, or a saved Markdown report?