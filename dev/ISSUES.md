# Known issues and technical notes

Living document. Updated as issues are found.

---

## Grader bugs (all fixed)

These were bugs in existing checks that caused false passes on obvious AI text. All fixed and covered by `test_grade.py`.

1. **COPULA_AVOIDANCE only matched singular verb forms.** `"serves as"` caught "The library serves as" but missed "Libraries serve as". Fixed with `serves? as` etc.
2. **AI_VOCABULARY substring match missed inflected multi-word phrases.** `"align with"` missed "aligns with" because `"align with" in "aligns with"` is `False` in Python. Fixed with a separate `AI_VOCABULARY_REGEX` list.
3. **no-negative-parallelisms only matched within a single sentence.** Fixed by adding cross-sentence patterns: `r"not (?:about|just about) [\w\s]+\.\s+it is (?:about|a\b)"`.
4. **COLLABORATIVE_ARTIFACTS missed soft variants.** Missed "feel free to", "don't hesitate to", soft offer-to-continue patterns. Added.
5. **FILLER_PHRASES too specific.** Had "it is worth noting" but not "it is worth recognising/mentioning/emphasising". Added regex alternation.
6. **no-forced-triads suffix list too narrow.** Missed -ence, -ance, -sion, -cy, -ism. Added.
7. **no-rhetorical-questions missed bare "It".** Had `It's` but not `It` as an answer opener. Fixed.

---

## Implemented since initial release

All of the following were proposed in earlier development and are now complete.

**New checks (31 total, up from original 21):**
- `no-formulaic-openers` (6/8 original samples caught)
- `no-signposted-conclusions` (7/13 samples caught)
- `no-markdown-headings` (all 5 essay-topic samples caught)
- `no-corporate-ai-speak` (finally catches the cover letter)
- `no-this-chains` (3+ consecutive "This [verb]" sentences)
- `no-excessive-hedging` (impersonal passive hedging at density 4+)
- `no-countdown-negation` (serial "It wasn't / It isn't" + affirmative, plus pronoun variants)
- `vocabulary-diversity` (type-token ratio, flags below threshold for texts 150+ words)
- `no-triad-density` (high density of three-item lists in 300+ word texts)
- `no-section-scaffolding` (repeated identical subheadings across sections)

**Patterns 33-38 and Voice and register category:**
Countdown negation, per-paragraph miniature conclusions, tonal uniformity, faux specificity, neutrality collapse, section scaffolding. All added to SKILL.md and references/patterns.md.

**Subtraction framing:**
"Personality and soul" section in SKILL.md now leads with the subtraction framing from Abdulhai et al. (2026). Semantic preservation step (Step 2.5) added. Self-audit restructured as mandatory structural self-audit with Abdulhai-informed questions.

**Vocabulary reconciliation:**
`unparalleled`, `invaluable`, `bolstered`, `meticulous` added to `AI_VOCABULARY`. `fostering` and `showcasing` confirmed present in both patterns.md and grade.py.

**Short-form text handling:**
`sentence-length-variance` now skips texts under 100 words with fewer than 6 sentences.

**Pass-through test:**
`9-passthrough-human.md` added: human-written personal essay, scores high (only fails staccato, a known acceptable false positive). Wired into evals.json as eval 13.

**Eval expansion:**
14 evals total (up from 5): 5 original essay evals, 8 format-diversity evals, 1 pass-through eval.

---

## Still outstanding

### MEDIUM: Semantic preservation testing

Verify the rewriting step doesn't itself neutralise stance (Abdulhai et al. showed LLMs shift meaning even in grammar-only passes).

### MEDIUM: No regression test for original 10/10 results

TESTING.md notes the original 10 humanised outputs need re-running against the 31-check grader. Requires the original output files (still in Obsidian vault, not version-controlled).

### LOW: Wire new checks into evals.json eval assertions

The 2 new grader checks (`no-triad-density`, `no-section-scaffolding`) and the extended `no-countdown-negation` (pronoun variants) need corresponding `expect_fail` / `expect_pass` assertions wired into the eval definitions in `evals.json`.

### LOW: Structural monotony detection

Every AI paragraph follows topic sentence, elaboration, restatement. Humans vary paragraph structure. Hardest gap to close programmatically. Documented in SKILL.md Step 2 as a manual check. "Per-paragraph miniature conclusions" (pattern 34) is a related signal.

Proposed: `no-paragraph-template`, measuring paragraph length variance. Needs prototyping to assess false-positive rate.

### LOW: No cross-model samples

No GPT/Gemini/Llama samples. Stylometry research (Zaitsu et al. 2025) confirms most commercial LLMs cluster together stylistically (only Llama 3.1 was distinct), which validates targeting shared patterns, but cross-model samples would confirm.

### LOW: No CI or regression tracking

No automated pipeline. A SKILL.md edit could regress quality silently. `test_grade.py` protects the grader's correctness but not the skill's output quality.

### LOW: Subtraction-oriented evals

Current evals test "did the AI tells get removed?" (additive). No evals test "did the author's stance survive?" (subtractive). Would need: opinionated input, humanise it, verify the opinion survived.

### LOW: Original eval text files not in repo

The 5 original human-written texts and their AI-generated + humanised versions are in an Obsidian vault, not version-controlled. The original 10/10 results were against the 21-check grader and have not been re-run against the current 31-check grader.

---

## Research findings

Full analysis in `research/web-survey-2026.md`.

### Insights not being implemented (documented for context)

**Stylometric classification features (Przystalski et al., Zaitsu et al. 2025):**
Function word unigrams, POS bigrams, and phrase patterns achieve .98 binary accuracy on 10-sentence samples. These are classification features for a detector, not patterns for a rewriting tool. The insight that matters is already captured: commercial LLMs cluster together, validating the skill's approach of targeting shared patterns.

**Code stylometry (Bisztray et al., ACM AISec 2025):**
Comment phrasing is the richest signal for model attribution. The skill targets prose, not code. Relevant if humanise ever expands to code comments or technical documentation.

**Stylometric watermarking proposals:**
Models could embed watermarks via consistent synonym preferences or unusual syntactic structures. Speculative/theoretical; no production watermarking to detect yet. Worth monitoring.

**Temporal vocabulary fingerprints (Nature study):**
GPT-4 era favoured "tapestry", "pivotal", "meticulous", "testament". GPT-4o shifted to "align with", "enhance", "showcasing". "Delve" peaked 2023-24. Useful for periodic maintenance of the vocabulary list, not a detectable pattern in itself.

**Satisfaction paradox (Abdulhai et al.):**
Heavy LLM users reported similar satisfaction despite acknowledging loss of creativity and voice. Context for why AI writing persists, not actionable for the skill.

**Peer review score inflation (Abdulhai et al., ICLR 2026):**
AI reviews assigned scores a full point higher on average. Domain-specific to academic peer review, outside the skill's scope.

---

## SKILL.md best practices compliance

Checked against [Anthropic's skill best practices](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/skills#best-practices).

### Compliant
- Progressive disclosure: SKILL.md -> references/patterns.md (one level deep)
- Reference file has table of contents
- Feedback loop: pre-check -> fix -> self-audit -> post-check
- Workflow with clear steps
- Utility script (grade.py) with explicit error output
- Description includes both what the skill does and when/how to trigger it
- Consistent terminology throughout
- Examples are concrete with before/after pairs
- Trigger terms include natural phrasings ("reads like AI", "sounds too balanced", "voice got neutralised")

### Needs attention
- **SKILL.md line count:** currently manageable, but new qualitative guidance should go in patterns.md, not SKILL.md body, to stay under the 500-line limit.
- **Time-sensitive vocabulary:** the vocabulary list is inherently time-sensitive (words rise and fall with model versions). Consider periodic review against current model output rather than embedding dates.

---

## Technical gotchas for future check development

1. **Substring vs regex for multi-word vocab.** `"align with" in "aligns with"` is `False` in Python. Any multi-word phrase where the first word can be inflected needs regex, not substring matching.

2. **`count_pattern_matches` lowercases text.** All regex patterns must be lowercase.

3. **Cross-sentence patterns need full-text matching.** The `split_sentences` utility splits on `[.!?]\s+`, destroying sentence boundaries. Cross-sentence checks must operate on the full text.

4. **Anaphora check excludes common words.** "i", "a", "the", "it's", "it" are excluded. "This" chains need their own logic (implemented as `no-this-chains`).

5. **Forced triads check only matches abstract nouns by suffix.** Concrete triads correctly pass. Abstract nouns with unusual suffixes ("speed", "trust", "hope") also pass.

6. **`features` in copula avoidance has a film/movie exception.** `r"features?\b(?! film| movie| documentary)"` avoids flagging "the film features..." but other legitimate uses ("software features") could false-positive.

---

## Gaps against Wikipedia's "Signs of AI writing"

Comparison of [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (79 items) against the 32 patterns currently in humanise. Wikipedia-specific signs (wikitext markup, citation bugs, hallucinated templates, DOI/ISBN errors, etc.) are excluded as out of scope.

### Missing vocabulary words

The following words are flagged by Wikipedia and linked studies but absent from `AI_VOCABULARY` in `evals/grade.py` and the word list in `references/patterns.md` pattern 7:

- moreover
- furthermore
- notably
- multifaceted
- nuanced
- encompasses

### Missing patterns worth adding

#### Speculation about gaps (Wikipedia #36)

AI speculates when it lacks data rather than admitting absence. Claims information is "not widely documented" or "limited information is available" then follows with "likely..." or "it is believed that..."

**Example:**
> While specific details about his early life are not widely documented, it is likely that he was influenced by the cultural and intellectual environment of his time.

#### Privacy speculation (Wikipedia #37)

When personal details are simply unknown, AI fabricates an explanation: the person "maintains a low profile" or "values their privacy." The absence of data is reframed as a deliberate choice.

**Example:**
> Little is known about her personal life, as she maintains a low profile and prefers to keep her private affairs out of the public eye.

#### Explicit negation, broadened (Wikipedia #20)

Pattern 9 currently covers "not only...but also" and "not just...but" constructions. Wikipedia identifies a broader explicit-negation pattern: "No X. No Y. Just Z." and "not..., it's..." as a standalone rhetorical device distinct from negative parallelisms.

**Example:**
> No fluff. No filler. Just actionable insights you can use today.

#### Improper list markers (Wikipedia #27)

AI outputs bullet characters (•), hyphens (-), en dashes (--), hashes (#), or emoji as list markers instead of proper formatting for the target medium.

#### Unnecessary small tables (Wikipedia #30)

AI creates small tables (2-4 rows) that would be better represented as prose. The tabular format adds no clarity and reads as a formatting crutch.

#### Mismatched English variety (Wikipedia #63)

AI defaults to American English regardless of context. A topic about a British, Australian, or Indian subject may use American spellings, idioms, or conventions. Already documented in `research/nyt-chatbot-style.md` (the "I rise to speak" example) but never promoted to a numbered pattern.

### Borderline / lower priority

#### Statistical regression to the mean (Wikipedia #3)

AI omits specific, unusual facts and replaces them with generic descriptions. The "experiential vacancy" concept in SKILL.md captures the spirit but this is not a named pattern with detection criteria or a grading check.

#### Subject lines left in output (Wikipedia #32)

AI output sometimes begins with text intended for an email Subject field or a title line. Adjacent to pattern 19 (collaborative artifacts) but not explicitly covered.

#### Phrasal templates (Wikipedia #38)

Fill-in-the-blank templates the user forgot to complete: "[Insert name here]", "[Your company]", "[specific example]".

#### List titles as proper nouns (Wikipedia #15)

AI treats non-proper-name list titles as standalone named entities, capitalising and referencing them as if they were proper nouns.

#### Sudden style shifts (Wikipedia #62)

An abrupt change in prose quality, register, or English variety mid-text, suggesting part of the text was AI-generated and part was human-written.
