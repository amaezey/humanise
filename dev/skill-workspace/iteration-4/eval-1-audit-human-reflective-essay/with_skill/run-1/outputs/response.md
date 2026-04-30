`★ Insight ─────────────────────────────────────`
- The grader runs as a pattern detector, not a verdict machine. Several flags here are almost certainly *deliberate* literary devices (Dillard's anaphora, her dense triads, her contrast structures), but the audit's job is to surface every match and let the writer decide. That's the design.
- A few signals are inflated by source-page artefacts: this scrape contains three copy-paste repetitions of the same paragraph, which is what makes "However" appear five times in a row at the sentence level.
`─────────────────────────────────────────────────`

**Audit, 6 AI tells found**

Contrived contrast (4 instances)
  - "Not a funeral. Forget funeral. A big birthday party."
  - "Beyond those things our culture may place a special focus on money, on celebrity, on physical beauty."
  - "Popular culture deals not in its distant past, or any other past, or any other culture."
  - "Not just there, but here."
  Why: not-X-but-Y, beyond-X, and similar reveal structures package a claim as a turn rather than stating it directly. The grader treats these as a strong signal because LLMs lean on them as default rhythm; in literary prose they can still be deliberate.

Mechanical repeated sentence starts (5 consecutive)
  - "However hypnotized you and your people are…"
  - "However dead you are, more people will come."
  - "However many more people come, your time and its passions…" (×3)
  Why: five sentences in a row begin with "However". Three of those five are the same sentence repeated verbatim — almost certainly a scraping artefact from the source page rather than Dillard's draft. Even setting the duplication aside, the underlying anaphora is intentional rhetorical patterning, but the detector can't distinguish craft from template.

Generic staccato emphasis (5 consecutive short sentences)
  - "Fewer golf courses? What's wrong with golf? Nothing at all. Equality of wealth? Sure; how?"
  Why: a run of clipped sentences used as emphasis. Reads as deliberate cadence here (a Q&A volley with the reader), but the same shape is a common AI tell when it's used as default punctuation.

Triad density (23 instances)
  - "hopes, dreams, values"
  - "land is value, or labor is value, or learning is value"
  - "to spear the seal, intimidate the enemy, and be a big man"
  - "cow, cross, mountain"
  - …plus ~19 more, including three copies of "many more people come, your time, its passions" and three copies of "or wasted from disease, then or now" (those duplicates again)
  Why: comma-separated three-part lists are one of the most recognisable AI cadences when overused. This essay leans on them heavily as a stylistic spine — partly substantive cataloguing, partly rhetorical music. The duplication artefact also pads the count.

Vocabulary diversity (type-token ratio 0.372; target >0.40)
  Where: across the whole 1,851-word piece, only 689 unique words. The grader flags TTR below 0.40 for long prose.
  Why: low lexical variety can read as mechanical, but the guidance explicitly notes that older prose, repeated rhetorical motifs, and incantatory writing fail this legitimately. Dillard's deliberate refrain ("Then what?", "what else is there", "the fabric") drags the ratio down on purpose.

Curly quotes (18 instances)
  Where: throughout — typographic ' and " around quoted speech, Mary Oliver's question, "Plato's Cave", and so on.
  Why: this isn't an AI signal in itself. It only matters when the requested output is plain text that should normalise punctuation. For a literary scrape this is expected and harmless.

**Confidence**

- Level: Medium
- Meaning: Several signs of AI-like writing appeared, but the evidence is pattern-based and should be read in context.
- Basis: 1 strong AI-writing signal (contrived contrast); 5 context-sensitive signals (anaphora, staccato, triads, vocab diversity, curly quotes).
- Caveat: This is a confidence assessment about AI-writing signs, not an authorship verdict.

A note worth flagging: three paragraphs in this scrape appear to be pasted in twice or three times verbatim ("Who is your everyone?…", "Most humans who were ever alive…", "However many more people come…"). That source-page glitch is what's pushing several of the rhythm and density numbers; the underlying essay is cleaner than the score implies.

**Next step**

Want Suggestions for per-flag replacements, a Rewrite at a chosen depth, or to save this audit as a Markdown file?