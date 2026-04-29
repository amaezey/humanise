# README "What we found" section — intent

Date noted: 2026-04-29
Status: deferred — capture the framing now, write the section later (after follow-up iterations on the reframe)

## What goes in this section

A research/findings section in the root README. Sits somewhere between "Performance" (existing auto-populated block) and "Patterns" (the catalogue table) — or replaces / reframes the lead-in to the patterns table.

## Narrative arc

People notice that AI writing has a particular feel — they can't always explain why. There's a body of research on this (linguistics, stylometry, text classification papers) and a much larger body of anecdata (Substack writers, editors, teachers, journalists). We pulled from both, turned the patterns into programmatic indicators, ran them on a corpus, learned which indicators actually distinguish humans from AI in matched-genre comparisons, refined what we kept and dropped, and this is what we ended up with. Here's what we found, where the value lies, where to be careful, and what's next.

## Tone

- **Plain.** No "groundbreaking", "revolutionary", "we discovered that…". Don't inflate.
- **Honest about limits.** Patterns are register-coded. Strong-signal categories don't always separate humans from AI on long-form first-person essay. Sample sizes are small. The grader has gaps.
- **Practitioner voice.** This is a tool that helps writers see AI patterns in their own drafts. Frame findings in terms of what the tool can and can't reliably catch.
- **No claims about authorship.** The skill flags patterns; it doesn't render verdicts about who wrote a piece.

## Substance to include

Drawing from `dev/research/2026-04-29-genre-paired-corpus-findings.md`:

1. **What we built indicators from**
   - Wikipedia AI Cleanup conventions
   - Stylometry research (Kobak excess vocab; Przystalski; Zaitsu)
   - GPTZero / Grammarly / SEO Engine / AIDetectors practitioner lists
   - Practitioner essays (Caroll, Kriss, Guo, Vollmer, Shankar)
   - Academic findings on language drift (Abdulhai et al.)

2. **What we found**
   - Some patterns *are* genuinely AI-correlated when applied at high density (em dashes, AI vocabulary clustering, manufactured insight, formulaic openers).
   - Many patterns coded as "strong AI signals" are actually high-skill rhetorical moves (triads, anaphora, contrived contrast, section scaffolding) — used by good human writers in the same registers AI mimics. They flag because AI overuses them as a blunt instrument, not because they're inherently AI.
   - The clearest non-pattern signal is **sentence-length variance**. Humans cluster around 23-word sentences with stdev ~17; AI clusters around 13-word sentences with stdev ~7. The grader's pattern checks don't catch this; body-level statistics do.
   - **Style-coded vs authorship-coded.** A lot of "AI tells" are really "thin or unconfident writing tells." Strong human writers and strong AI writers in the same register fire the same patterns. The flags become useful when they're dense, ungrounded, or stack across categories.

3. **Where the value lies**
   - As a *review priority list*, not a verdict. The skill surfaces high-risk patterns to re-examine — "have you earned this?" — not "this is AI, fix it."
   - As an audit framework that explains *why* a pattern matters, so the writer learns to spot it next time.
   - As a body-stats baseline (variance, density, vocabulary diversity) that can flag mechanical output even when individual patterns don't trigger.

4. **Where to be careful**
   - Genre matters. Persuasive how-to, business memo, and literary essay all have legitimate uses of patterns this skill flags. The audit is calibrated to spot AI overuse, but a reader has to apply judgement.
   - Patterns drift. AI vocabulary lists go stale (delve peaked in 2023–24). The catalogue needs refreshing.
   - Detection is asymmetric. The skill catches AI doing patterns badly; it can also wrongly flag humans doing the same patterns well. False-positive guard is necessary; the audit voice should reflect this.
   - The skill itself is an LLM. It can introduce the patterns it's trying to catch — neutrality collapse, pronoun depletion, generic substitution. The semantic-preservation step matters.

5. **What's next**
   - Reframe audit voice from "AI tell, fix it" to "review priority — verify this is working."
   - Add genre-aware thresholds (literary essay ≠ corporate doc ≠ news copy).
   - Promote new candidate signals (ghost-spectral density, negation density, unicode flair) where evidence supports.
   - Demote pattern checks that don't actually separate humans from AI in matched genres (some triads, em dashes, manufactured insight may belong in a softer category).
   - Larger N. Iteration corpus will grow.

## Where this section sits in README

Suggested order:

1. Title + intro (existing)
2. Install (existing)
3. Usage (existing)
4. What it does (existing)
5. **Findings — what we learned building this** (new — the section described above)
6. Performance (existing — auto-populated iteration block)
7. Representative report output (existing — example)
8. Patterns table (existing)
9. File structure / Sources / Limitations / Licence (existing)

Putting findings between "What it does" and "Performance" gives readers the *meaning* behind the numbers before the numbers.

## When to write this section

After at least one more iteration of the reframe lands — i.e., after:

- The audit voice is updated in `humanise/SKILL.md` and `humanise/grade.py`'s report templates
- The patterns documentation reflects "review priority" framing
- A subsequent iteration's data confirms the reframed output

Writing it before the reframe ships would document a tool that doesn't exist yet. Writing it after gives an honest account.
