**Audit, 13 AI tells found**

Em dashes (55 instances)
  - "changed to protect them — except mine, of course"
  - "it may have been 100% placebo effect — but for a time, it worked well"
  - "my thighs and legs shook for literally hours"
  - "—I got jimmy legs"
  Why: Em dashes are a strong current AI fingerprint, especially when used as default punctuation throughout a piece. Plenty of them here are doing real prose work, but the sheer count makes the page read as machine-cadenced.

Manufactured insight framing (2 instances)
  - "And honestly, that feeling, at least at first, is this weird mix of terrifying and exhilarating."
  - "MDMA is the future of trauma treatment, and honestly, I am really excited about it."
  Why: "And honestly" performs candour without earning it; it's a stock LLM move to flag depth. Mostly readable here because it sits inside actually candid prose, but it's the same wrapper.

Generic staccato emphasis (1 sequence)
  - "Not a cry of sadness. / More a cry of release and a cry of happiness."
  - Other clusters: "Fuck that. No more." / "I'm hiding."
  Why: Repeated short, dramatic, line-broken beats are a classic generated rhythm. They land harder when the surrounding prose is tight, and start sounding template-like when they stack.

Mechanical repeated sentence starts (5-in-a-row)
  - "You CANNOT AVOID processing the trauma… / You WILL do the work either way. / You cannot avoid the processing work though."
  - Earlier: "You don't mind actually… / You can keep your true self back…"
  Why: Five consecutive sentences opening with the same word ("you") read as anaphora-as-template. Used deliberately by humans, but a tell when stacked.

Curly quotes (301 instances)
  - "It was a deeply profound and life-changing experience."
  - "I'm not trying to convince you to do MDMA therapy"
  Why: Curly quotes aren't proof of anything by themselves, but the file is fully smart-quoted. That's a packaging signal in plain Markdown, not a writing one — likely an artefact of how the source was extracted.

Generic promotional language (1 instance)
  - "It was a deeply profound and life-changing experience."
  Why: "Profound" is a stock hype adjective; LLMs reach for it constantly. It sits in the very first beat of the piece, where the writer's specific voice should be loudest.

Contrived contrast / reframe (4 patterns)
  - "Not the love you're thinking about. Not love for other people, or even love for yourself — all of that implies that we are all separate things…"
  - "MDMA is not a psychedelic. It is a totally different class of medicine"
  - "Not in an emotionally dissociated way, and not in a disconnected way."
  - "MDMA is not a treatment for trauma *by itself*."
  Why: "Not X — it's Y" / "not X, but Y" frames create a fake reveal instead of stating Y directly. Some of these (the love passage) are doing real definitional work; others (the dissociated/disconnected pair) read as machine reveal-rhythm.

Decorative three-part lists (2)
  - "sweating, gyrating, and flailing my arms"
  - "patience, vision, and persuasion"
  Why: Triads of abstract nouns or near-synonyms are a generated-sounding cadence — three for rhythm rather than because each item carries new information.

Headings in prose (23 instances)
  - "## Disclaimer"
  - "## 1\. Why I Decided To Do MDMA"
  - "## 5\. The Aftermath of the First Session"
  - "## Sixteen days after Session 1"
  Why: Heavy section scaffolding with numbered headings makes a personal essay feel chapter-divided like an assistant-packaged article. The dated subheads ("Two days after Session 1") read more like field notes and are doing real work; the top-level numbered list is the part that signals packaging.

Triad density (27 instances)
  Where: Triadic phrasing recurs across the piece — "what it was like, how it impacted me, and resources for", "trust the medicine. Surrender to the medicine. Receive what comes up.", "addiction, anger, self-abuse, overachievement", and 24 others. Several triads per major section.
  Why: One triad reads as rhythm; twenty-seven reads as a cadence the writer (or model) keeps reaching for. The "Trust / Surrender / Receive" frame is load-bearing because it's quoted from the book — but the rest stack quickly.

Vocabulary diversity (TTR 0.180)
  Where: 1,436 unique tokens in 7,977 total — well below the 0.40 target. Long pieces always drop, but this drops further than expected.
  Why: Heavy repetition of MDMA, trauma, therapy, session, anger, processing across the piece. Some of that is unavoidable in a focused essay, but it does flatten the vocabulary surface.

Repeated section scaffolding
  Where: The character `[` repeats seven times in a stacked block at the end (the medium.com link/footer artefacts: tag links, sign-in links, follower count).
  Why: A scraped trailing block of repeated bracketed link templates reads as boilerplate scaffolding, not prose. Likely a defuddle artefact rather than authored content — but the grader sees it as packaging.

AI pressure from stacked weak signals
  Where: Manufactured insight framing + contrived contrast + section scaffolding + headings in prose, all firing together. Score 7 against a threshold of 4.
  Why: None of these alone would be damning. Together they make the draft *look* machine-packaged even though the prose underneath is voice-y, profane, and clearly authored.

**Confidence**

- Level: **High**
- Meaning: Multiple strong or structural signals fired. Treat this as a high-confidence style diagnosis, not proof of authorship.
- Basis: 4 strong AI-writing signals, 9 context-sensitive signals, AI-pressure score 7/4.
- Note: This describes AI-writing signs in the surface and structure of the text, not a verdict about who wrote it. A lot of this piece — confessional first-person, profanity, the "Sorry Meditation, it was me, not you" beat, the strip-club anecdote, the Slack-pasted dialogue — is unmistakably human voice. The flags mostly catch packaging (headings, footer artefacts, smart quotes, em-dash density) and a handful of recurring framing tics.

**Next step**

Want Suggestions for per-flag replacements, a Rewrite at a chosen depth, or to save this audit as a Markdown file?