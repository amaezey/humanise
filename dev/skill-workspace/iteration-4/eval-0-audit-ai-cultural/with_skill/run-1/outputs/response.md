`★ Insight ─────────────────────────────────────`
- The grader splits findings into "Strong AI-writing signal" (lexical/structural fingerprints with high specificity, like contrived contrast or `lands` as metaphor) and "Context-sensitive signal" (weaker patterns that matter mainly when they stack — anaphora, triads, staccato, headings).
- The `overall-ai-signal-pressure` check is the meta-detector: it scores 4/4 here because contrived-contrast framing and headings co-occur, signalling machine-packaged structure even before any single sentence is examined.
- Curly quotes (22 of them) aren't proof of AI on their own, but they're a giveaway that the text was pasted from an LLM chat surface that auto-smartens punctuation; flagging them is part of the skill's "plain-output" hygiene.
`─────────────────────────────────────────────────`

**Audit, 10 AI tells found**

Nonliteral land/surface phrasing (1 instance)
  - "That scene lands differently across a life."
  Why: Abstract uses of *land* (ideas landing, scenes landing, work landing on a scale) are a current AI-writing fingerprint. They make ordinary observations sound artificially managed.

Contrived contrast (3 instances)
  - "Not because its meaning changes, exactly, but because the reader's defences do."
  - "Its durability comes not from universality in the abstract, but from the accuracy with which Didion records a specific consciousness under extreme strain."
  - "It should be returned to, not for comfort, but for calibration."
  Why: *Not X, but Y* and its cousins (*beyond X*, *less X than Y*, *not only X. It is Y*) are reveal scaffolds. They simulate insight by cancelling something simpler instead of stating the claim and supporting it.

Filler phrases (1 instance)
  - "is often described as a grief memoir, which is accurate but insufficient"
  Why: *Is often described as* is stock framing that adds polish without information. It also smuggles in the contrived-contrast move that follows.

Generic staccato emphasis
  Where: "She knows what to do. She calls the right people. She signs forms. She keeps functioning." — four consecutive short sentences used for emphasis.
  Why: Repeated short beats applied as a generic dramatic device read as generated cadence rather than naturally paced prose.

Mechanical repeated sentence starts
  Where: Paragraph four, where six consecutive sentences begin with *She* ("She remembers the fire… She reconstructs the event… She seeks the timeline. She wants the medical explanation. She reads the records. She returns to the details…").
  Why: Identical sentence openings in a run read as template rhythm rather than chosen rhetoric. Anaphora can be deliberate, but at six in a row it's pattern-matching for emphasis.

Triad density (10 triads)
  - "medical language, social performance, the collapse of ordinary time"
  - "an anatomy of denial, a critique of competence, and a warning about the stories we tell ourselves"
  - "loss made her wiser, kinder, or more authentic"
  - "curated vulnerability, the language of healing and closure"
  - "specialist language, medical uncertainty and bureaucratic routines"
  - "chronic illness, disability systems or end-of-life care"
  - "the repetitions, returns and abrupt transitions"
  - plus three more
  Why: Three-part lists are a default LLM cadence. At ten, they create a recognisable generated rhythm and start doing the work that specific evidence should do.

Dense negation
  Where: 21 negation markers across roughly 1,560 words (13.5 per 1,000). Concentrated in claims like *does not stage*, *does not turn grief into moral improvement*, *does not claim*, *does not speak for everyone*, *not interested in uplift*, *not decorative flashbacks*, *not only emotional*, *not only missing someone*.
  Why: A piece over-framed around what it *isn't* substitutes refusal for description. Once negation crosses ~10 per 1,000 words, the prose starts feeling defined by its disclaimers.

Headings in prose (1 instance)
  - "# Why The year of magical thinking should be reread every decade"
  Why: A markdown H1 above a continuous essay is a pasted-from-chat signal. Long-form criticism rarely opens with a packaged title heading.

Curly quotes (22 instances)
  Where: All apostrophes and quotation marks throughout (*Didion's*, *book's*, *"magical thinking"*, etc.) are typographic curly characters.
  Why: Not proof of AI authorship, but a hygiene tell: text pasted from a chat surface arrives with smart-quoted punctuation that plain prose typically doesn't have unless deliberately typeset.

AI pressure from stacked signals (4/4, triggered)
  Where: The contrived-contrast framing and the markdown heading combine across the whole piece.
  Why: AI pressure is the accumulation check. None of the stacked signals would be damning alone, but together they make the piece read as machine-packaged: too much visible structure, too little natural variation.

**Confidence**

- Level: High
- Meaning: Multiple strong or structural signals fired. Treat this as a high-confidence style diagnosis, not proof of authorship.
- Basis: 3 strong AI-writing signals; 7 context-sensitive signals; AI-pressure score reached 4/4.
- Note: This is a confidence assessment about AI-writing signs, not an authorship verdict.

**Next step**

Want Suggestions for per-flag replacements, a Rewrite at a chosen depth (Balanced or All), or to save this audit as a Markdown file?