Action: Audit

**Audit Report**

Summary: 9 of 43 checks were flagged for AI-style writing patterns.

Confidence: High. Multiple structural or style signals fired, but this is confidence about AI-style signals, not proof of authorship. In this draft, several flags look like genre/publishing conventions from a practitioner blog post rather than strong evidence of machine writing.

AI-pressure explanation: The draft triggers accumulated pressure because weaker signals stack: visible headings, manufactured-insight phrasing, repeated triad/list rhythm, and some vocabulary repetition. Alone, these are explainable. Together, they can make the piece look more packaged than conversational.

**Main Issues Found**

- **AI pressure from stacked signals**: The system found accumulated structure signals, mainly headings plus manufactured-insight phrasing. This matters because several weak signals together can create a machine-packaged feel. Severity: Context-sensitive signal. Recommended action: Preserve in Light if purposeful; fix in Medium and Hard.
- **Manufactured insight framing**: Found repeated “but here’s” phrasing. This can sound like performed revelation if overused. Severity: Strong AI-writing signal. Recommended action: Fix in Light, Medium, and Hard unless explicitly preserved.
- **Generic staccato emphasis**: Found a run of four short sentences. In this piece, some of that rhythm feels authorial and blog-native, but it still registers as a tell. Severity: Context-sensitive signal. Recommended action: Preserve in Light if purposeful; fix in Medium and Hard.
- **Inflated significance**: Flagged “crucial.” This is mild here and tied to the essay’s argument. Severity: Context-sensitive signal. Recommended action: Preserve in Light if purposeful; fix in Medium and Hard.
- **Decorative three-part lists / triad density**: Found several three-part rhythms, including “improvisation, sparring, discussion.” This can create generated cadence when frequent. Severity: Context-sensitive signal. Recommended action: Preserve in Light if purposeful; fix in Medium and Hard.
- **Signposted conclusion and headings**: The markdown headings and “Conclusion” label were flagged. For a blog post, these are normal article scaffolding, so I would treat this as a likely false positive unless the goal is seamless essay prose. Severity: Context-sensitive signal. Recommended action: Preserve in Light if purposeful; fix in Medium and Hard.
- **Vocabulary diversity**: Type-token ratio was low for a long text. In this case, repeated terms like workshop, client, consultant, clarity, and work are central to the topic, so this is probably partly topical repetition. Severity: Context-sensitive signal. Recommended action: Preserve in Light if purposeful; fix in Medium and Hard.

**Full Check Table**

| Check | Status | What it looks for | What happened here | Why this matters | Severity | Recommended action |
|---|---|---|---|---|---|---|
| Em dashes | Clear | Em dash punctuation as a current AI-style signal. | No issue found. | Em dashes can be a generated prose fingerprint when overused. | Strong AI-writing signal | None |
| Clustered AI vocabulary | Clear | Generic AI-associated words clustering together. | No issue found. | Generic vocabulary is more suspicious when it clusters. | Strong AI-writing signal | None |
| Nonliteral land/surface phrasing | Clear | Abstract “land,” “surface,” or similar phrasing. | No issue found. | This phrasing can make ordinary ideas sound packaged. | Strong AI-writing signal | None |
| AI pressure from stacked signals | Flagged | Several weaker signals appearing together. | Headings, manufactured insight framing, and vocabulary pressure stacked to 5/4. | Weak signals become more meaningful in combination. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Manufactured insight framing | Flagged | Phrases that perform hidden depth or reveal. | Found 2 uses of “but here’s.” | Can perform insight without earning it. | Strong AI-writing signal | Fix in Light, Medium, and Hard. |
| Generic staccato emphasis | Flagged | Repeated short dramatic sentences. | Found a sequence of 4 short sentences. | Can sound generated when used as generic emphasis. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Mechanical repeated sentence starts | Clear | Template-like repeated openings. | No issue found. | Repeated openings can create mechanical rhythm. | Context-sensitive signal | None |
| Assistant residue | Clear | Chatbot collaboration phrases or follow-up residue. | No issue found. | Would make the text look like assistant output. | Must fix | None |
| Curly quotes | Clear | Curly quotation marks where plain output is expected. | No issue found. | Mostly a formatting signal, not authorship evidence. | Context-sensitive signal | None |
| Sentence rhythm variance | Clear | Overly uniform sentence lengths. | No issue found. | Low variation can feel mechanically produced. | Context-sensitive signal | None |
| Generic promotional language | Clear | Stock hype or sales-like adjectives. | No issue found. | Stock hype weakens credibility. | Context-sensitive signal | None |
| Inflated significance | Flagged | Language that overstates importance. | Found “crucial.” | Can make ordinary claims sound artificially momentous. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Contrived contrast | Clear | Not-X-but-Y or fake reveal structures. | No issue found. | Can simulate depth instead of making a direct claim. | Strong AI-writing signal | None |
| Avoiding plain “is” | Clear | Inflated substitutes such as “serves as.” | No issue found. | Can turn simple claims into pseudo-analysis. | Strong AI-writing signal | None |
| Filler phrases | Clear | Stock padding such as “it is worth noting.” | No issue found. | Adds polish without information. | Strong AI-writing signal | None |
| Generic conclusion | Clear | Empty or interchangeable endings. | No issue found. | Generic endings feel templated. | Must fix | None |
| False balance or concession | Clear | Fake both-sides framing. | No issue found. | Can hide the writer’s stance. | Strong AI-writing signal | None |
| Placeholder residue | Clear | Unfilled template markers. | No issue found. | Signals unfinished generated text. | Must fix | None |
| Soft explainer scaffolding | Clear | Phrases that announce structure instead of making a point. | No issue found. | Can make prose feel assembled. | Strong AI-writing signal | None |
| Vague “this/that” starts | Clear | Repeated vague sentence subjects. | No issue found. | Blurs the actual subject. | Context-sensitive signal | None |
| Decorative three-part lists | Flagged | Forced triads used for rhythm. | Found “improvisation, sparring, discussion.” | Can create artificial cadence. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Tacked-on -ing analysis | Clear | Trailing -ing clauses pretending to analyse. | No issue found. | Often adds vague analysis without substance. | Strong AI-writing signal | None |
| Ghost/spectral atmosphere | Clear | Cliched ghost, shadow, whisper, echo language. | No issue found. | Can make atmosphere feel borrowed. | Context-sensitive signal | None |
| Generic quiet/still mood | Clear | Overused quiet/still/soft atmosphere. | No issue found. | Can create generic literary mood. | Context-sensitive signal | None |
| Template rhetorical questions | Clear | Article-style questions followed by obvious answers. | No issue found. | Can simulate engagement. | Context-sensitive signal | None |
| Excessive list formatting | Clear | Prose over-converted into lists. | No issue found. | Can make writing feel like generated notes. | Context-sensitive signal | None |
| Decorative Unicode | Clear | Decorative symbols or generated-looking formatting. | No issue found. | Can signal generated formatting. | Context-sensitive signal | None |
| Unearned dramatic transitions | Clear | Generic turning points. | No issue found. | Claims drama the prose has not built. | Context-sensitive signal | None |
| Formulaic openers | Clear | Stock openings such as “at its core.” | No issue found. | Makes paragraphs feel templated. | Strong AI-writing signal | None |
| Signposted conclusion | Flagged | Explicit conclusion labels. | Found “## Conclusion.” | Can flatten endings into generic summary. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Headings in prose | Flagged | Markdown/plain title headings in prose. | Found 15 headings. | Can make prose feel packaged. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Corporate AI-speak | Clear | Vague delivery/alignment/outcomes cliches. | No issue found. | Hides specific work behind vague language. | Strong AI-writing signal | None |
| Repeated “This...” chains | Clear | Consecutive vague “This...” constructions. | No issue found. | Creates generic analysis. | Context-sensitive signal | None |
| Excessive hedging | Clear | Evasive qualification. | No issue found. | Weakens stance. | Context-sensitive signal | None |
| Countdown negation | Clear | Repeated no/not/cannot reveal setups. | No issue found. | Creates synthetic reveal structure. | Context-sensitive signal | None |
| Dense negation | Clear | Unusually dense negation markers. | No issue found. | Can over-frame prose around what it is not. | Context-sensitive signal | None |
| Paragraph length uniformity | Clear | Suspiciously similar paragraph lengths. | No issue found. | Can signal generated structure. | Context-sensitive signal | None |
| Tidy paragraph endings | Clear | Repeated miniature conclusions. | No issue found. | Makes paragraphs feel over-resolved. | Context-sensitive signal | None |
| Bland critical template | Clear | Generic review language. | No issue found. | Replaces judgment with portable phrasing. | Strong AI-writing signal | None |
| Rubric echoing | Clear | Assignment or rubric phrasing. | No issue found. | Sounds like compliance rather than thought. | Context-sensitive signal | None |
| Vocabulary diversity | Flagged | Unusually repetitive vocabulary in longer text. | Type-token ratio: 0.303, below target. | Low variety can feel repetitive or mechanical. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Triad density | Flagged | Overuse of three-part list structures. | Found 7 triads. | Too many triads create generated cadence. | Context-sensitive signal | Preserve in Light if purposeful; fix in Medium and Hard. |
| Repeated section scaffolding | Clear | Repeated section labels or templates. | No issue found. | Repeated structure can feel assembled. | Strong AI-writing signal | None |

Question: Do you want a rewrite, a recommendation on intensity, or a saved Markdown report?