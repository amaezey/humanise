---
title: "feat: Add structural AI detection and depth-aware rewriting"
type: feat
status: completed
date: 2026-04-01
---

# feat: Add structural AI detection and depth-aware rewriting

## Overview

The humaniser scores 28/29 on AI-generated text that still obviously reads as AI. Two problems combine: the grader misses structural patterns (repeated templates, triad density, countdown negation variants), and the skill's process treats structural rewriting as an optional afterthought behind "pass the grader."

The grader-as-quality-gate dynamic is the root cause. Adding more checks extends the grader's reach but doesn't change the dynamic — the agent will always optimise for passing with minimal effort. The primary intervention in this plan is therefore the **skill process restructuring**: mandatory structural self-audit with auditable answers, structural-first ordering in Step 2, and an output format that makes the agent's structural work visible to the user. The grader checks (2 new, 1 extended, bringing the total from 29 to 31) are secondary — they extend coverage for specific patterns but they are not what makes the skill robust. The process change is.

The plan validates robustness by testing across multiple AI genres, not just the single failure case that motivated it.

**Count reconciliation after this work:** 31 programmatic checks in grade.py, 38 documented patterns in patterns.md. 6 patterns are fully manual-only (28 forced synesthesia, 30 generic metaphors, 34 miniature conclusions, 35 tonal uniformity, 36 faux specificity, 37 neutrality collapse). Pattern 10 (rule of three) is partially covered by two programmatic checks: `no-forced-triads` (abstract-noun triads, zero-tolerance) and `no-triad-density` (all triads at density threshold 4+); concrete-noun triads below the density threshold remain manual-only. Note: patterns.md header currently says "32 patterns" but actually contains 37 (patterns 33-37 were added in PR #3 without updating the header). This plan adds pattern 38 and fixes the header to 38.

## Problem Frame

Real-world test: a 2000-word digital transformation article run through the humaniser. The grader went from 22/29 to 28/29, but the text still reads as AI because:

1. **7 triads** in the text ("skills, mindset, or autonomy", "training, coaching, and peer learning") — the grader's `no-forced-triads` only catches abstract-noun triads (words ending in -tion, -ment, -ness), missing all concrete-noun lists
2. **4 consecutive "You can't" sentences** — same rhetorical pattern as countdown negation but with a different pronoun/verb. The grader only catches "It wasn't X. It wasn't Y. It was Z."
3. **"How to make this work:" repeated identically 3 times** — cookie-cutter section templates are one of the loudest AI tells and the grader has no check for it
4. **Tonal uniformity, resolution density, register lock** — the skill's process mentions these as secondary "also check" items in Step 2, so the agent prioritises passing the grader and stops. The grader becomes the de facto quality gate, and the agent does word-swaps until it scores clean

The grader's blind spots and the skill's process hierarchy combine to produce text that is technically clean but structurally untouched.

## Requirements Trace

- R1. New grader checks catch the structural patterns identified in the digital transformation failure case
- R2. No new false positives on human text samples — the existing passthrough (personal narrative) plus 2 new samples: an opinion piece with legitimate rhetorical negation, and an instructional piece with repeated section headers
- R3. The skill process makes structural self-audit questions mandatory for all texts, not gated by a depth classification the agent can game
- R4. All new checks follow existing patterns: `check_<name>(text)` function, `ALL_CHECKS` registration, `expect_fail`/`expect_pass` tests
- R5. SKILL.md stays under 500 lines (currently 282)
- R6. New qualitative pattern content goes in `references/patterns.md`, not SKILL.md body
- R7. `ISSUES.md`, `TESTING.md`, and `README.md` are updated to reflect resolved items and current check counts
- R8. The process restructuring is validated against 3+ AI-generated texts in different genres (not just the digital transformation article) to confirm the structural self-audit catches problems that the grader alone would miss
- R9. Success is defined by a qualitative assessment beyond grader score: after humanising, a reviewer should not be able to identify the text as AI-generated from structure alone within the first 3 paragraphs. The grader score is necessary but not sufficient.

## Scope Boundaries

- Resolution density (pattern 34: per-paragraph miniature conclusions) is NOT getting a programmatic check. Analysis showed the signal is content-level, not syntactic — final sentences are conclusions by meaning, not by length or structure. The sentence-length heuristic only catches 4/42 paragraphs. Instead, the skill process is strengthened to make this a more prominent manual check.
- Paragraph structure variance (COVERAGE-ANALYSIS.md's proposed `no-paragraph-template`) is also deferred. Testing showed sentence-count stdev doesn't discriminate between AI and human text (AI: 1.52, human: 1.50).
- No changes to evals.json eval definitions — the new checks will be available in grade.py but wiring them into specific eval assertions can be done in a follow-up once the checks are validated on more samples.
- Tonal uniformity (pattern 35) remains a manual-only check — it requires reading comprehension, not regex.
- **Robustness vs reactivity:** The grader checks (Units 1-3) are reactive — they address specific patterns found in one failure case. The process restructuring (Unit 5) and multi-genre validation (Unit 8) are where robustness comes from. If Unit 8 fails (the process change doesn't generalise across genres), the grader checks alone are insufficient and the approach needs rethinking. The plan is structured so that Unit 8 is a validation gate: it must pass before merging.

## Context & Research

### Relevant Code and Patterns

- `evals/grade.py` — 29 checks following a consistent pattern: module-level constant (pattern list), `check_<name>(text)` function returning `{"text": str, "passed": bool, "evidence": str}`, registration in `ALL_CHECKS` dict
- `evals/test_grade.py` — 87 assertions using `expect_fail(check_name, text, reason)` and `expect_pass(check_name, text, reason)` helpers
- `evals/samples/9-passthrough-human.md` — false-positive anchor; any new check must pass on this text (scores 28/29 currently)
- `SKILL.md` — 282 lines, process is Steps 1-4 (lines 144-198), personality/soul section at lines 73-120
- `references/patterns.md` — 513 lines, 37 patterns across 8 categories; ToC only lists 7 categories (missing Voice and register)
- `ISSUES.md` — tracks outstanding work; structural monotony is LOW priority, subtraction framing is HIGH

### Existing Check Patterns to Follow

**Density checks with thresholds** (the model for new checks):
- `no-ai-vocabulary-clustering`: flags at 3+ AI words per paragraph
- `no-ghost-spectral-density`: flags at 3+ ghost words per text
- `no-quietness-obsession`: flags at 4+ quietness words
- `no-excessive-hedging`: flags at 4+ hedging constructions
- All have explicit `expect_pass` tests for clean human text

**Regex-based pattern detection** (for countdown negation extension):
- `check_countdown_negation`: uses a single complex regex matching 2+ negation sentences followed by affirmative
- `MANUFACTURED_INSIGHT`: list of regex patterns checked via `count_pattern_matches()`

### Calibration Data

Human passthrough sample scores:
- 0 triads (all forms)
- 0 repeated section labels
- 0 "You can't/won't/don't" negation sequences
- Sentence count stdev: 1.50 (comparable to AI text at 1.52 — confirms sentence-count variance is not a useful discriminator)

Digital transformation humanised text scores:
- 7 triads (concrete-noun form)
- 3 repeated "How to make this work:" labels
- 4 consecutive "You can't" sentences

## Key Technical Decisions

- **Rename vs extend `no-forced-triads`:** Create a new `no-triad-density` check rather than modifying the existing `no-forced-triads`. Reason: the existing check catches abstract-noun triads (a specific, high-signal pattern). The new check catches overall triad density (a broader, threshold-based pattern). They test different things and should fail independently. Keep both.

- **Threshold for triad density: 4+ per text (>300 words):** The human passthrough has 0 triads, the AI text has 7. A threshold of 4 provides margin against false positives while catching triad-heavy short texts (e.g., a 476-word listicle with 5 triads would be caught). For texts under 300 words, skip the check. Lower floor than `vocabulary-diversity` (150 words) because triads can be dense even in shorter pieces.

- **Countdown negation extension approach: broaden the existing check with two branches.** Rather than creating a separate check, modify `check_countdown_negation` to also catch pronoun-negation patterns ("You/We/They can't/won't/don't"). Reason: it's the same rhetorical device. **Key design difference:** The existing branch requires 2+ negation sentences followed by an affirmative reveal ("It wasn't X. It wasn't Y. It was Z."). The new pronoun-variant branch does NOT require an affirmative reveal — 3+ consecutive same-subject negation sentences are sufficient ("You can't X. You can't Y. You can't Z."). Threshold is 3 (not 2) because 2 consecutive "You don't" sentences are legitimate in opinion and advice writing. The digital transformation failure case has 4, so it's still caught. The regex needs two branches: original (negation + reveal, threshold 2) and new (consecutive same-subject negation only, threshold 3).

- **Section scaffolding detection: repeated identical subheading-like labels.** Check for lines that appear 3+ times with the same text (case-insensitive, stripped of leading/trailing whitespace). This catches the obvious case ("How to make this work:" repeated 3 times) but is trivially defeated by minor label variation ("How to make this work in practice:" vs "How to make this work for your team:"). This is acknowledged and acceptable: the check is a **signal**, not a gate. Its real value is that when it fires, it forces the agent to confront the structural repetition. The SKILL.md process restructuring (mandatory self-audit: "Do all sections follow the same arc?") is what actually drives structural rewriting. The check and the process change work together — neither is sufficient alone. Not attempting to detect structural template similarity (too hard, too many false positives).

- **Resolution density stays manual:** Explored a sentence-length heuristic (final sentence shorter than 80% of paragraph average) — only caught 4/42 paragraphs. The problem is content-level: AI conclusions summarise or restate, which can be long sentences. Strengthen the SKILL.md self-audit instead.

- **Mandatory structural self-audit over depth classification gate:** The process change is the most impactful part of this plan. Rather than adding a "Step 0: Assess depth" that the agent could game (it has an incentive to classify as "surface-AI" to do less work), make the structural self-audit questions mandatory for ALL texts. The depth assessment can remain as lightweight context ("this text was probably generated from scratch") without gating whether structural fixes are required. The concrete, countable questions ("Count the triads", "Do all sections follow the same arc?") drive structural work regardless of classification.

## Open Questions

### Resolved During Planning

- **Should triad density count "X, Y, or Z" as well as "X, Y, and Z"?** Yes — both are the same AI pattern. The digital transformation text uses both ("skills, mindset, or autonomy" and "training, coaching, and peer learning").
- **Should section scaffolding check be content-aware (detecting similar section arcs) or string-matching (detecting repeated labels)?** String-matching only. Content-aware arc detection requires NLP-level analysis and would be fragile. The string-matching approach catches the most common manifestation (identical action labels).
- **How to handle triads in quoted text or citations?** Count them — the humaniser should address triads in the output regardless of whether they came from citations.

### Deferred to Implementation

- **Exact regex for countdown negation variants.** The pronoun/verb combinations (can't, won't, don't, shouldn't, couldn't) need implementation-time tuning. The design decision (no affirmative reveal required for pronoun variants) is settled; the regex shape is not.
- **Whether `no-triad-density` needs paragraph-scoping or is whole-text.** Start with whole-text count; if false positives emerge in testing, consider paragraph-scoped density.

## Implementation Units

- [ ] **Unit 1: Add `no-triad-density` check**

**Goal:** Detect high density of three-item lists ("X, Y, and/or Z") regardless of word type, catching the pattern that `no-forced-triads` misses on concrete nouns.

**Requirements:** R1, R2, R4

**Dependencies:** None

**Files:**
- Modify: `evals/grade.py`
- Modify: `evals/test_grade.py`

**Approach:**
- Add a `check_triad_density(text)` function that counts all "X, Y, and Z" and "X, Y, or Z" patterns using a regex that matches comma-separated three-item lists where each item can be 1-4 words (to catch multi-word items like "peer learning", "decision-making structures"). Regex shape: each item position should match `\w+(?:\s+\w+){0,3}` or similar, e.g. `(\w+(?:\s+\w+){0,3}),\s+(\w+(?:\s+\w+){0,3}),?\s+(?:and|or)\s+(\w+(?:\s+\w+){0,3})`. This must catch the motivating examples: "skills, mindset, or autonomy" and "training, coaching, and peer learning".
- Skip texts under 300 words
- Flag at 4+ triads per text
- Register as `"no-triad-density"` in `ALL_CHECKS`
- Add `expect_fail` test with the digital transformation text's triad-heavy paragraphs
- Add `expect_pass` test with clean prose containing 0-2 triads

**Patterns to follow:**
- `check_type_token_ratio` for the short-text skip pattern
- `check_ghost_spectral` for the density-threshold-with-evidence pattern

**Test scenarios:**
- Happy path: text with 5 triads in 400 words fails the check, evidence lists count
- Happy path: text with 1 triad passes
- Edge case: text under 300 words with 5 triads is skipped (passes)
- Edge case: "X, Y, and Z" and "X, Y, or Z" both count
- Edge case: triads inside quoted text still count
- Error path: empty text passes without error

**Verification:**
- `python3 evals/test_grade.py` passes with no failures
- Human passthrough sample still scores 28/29 (or better)
- Digital transformation humanised text fails this new check

---

- [ ] **Unit 2: Extend countdown negation to catch pronoun variants**

**Goal:** Broaden the existing `check_countdown_negation` to catch "You can't X. You can't Y. You can't Z." and similar patterns, not just "It wasn't X. It wasn't Y. It was Z."

**Requirements:** R1, R2, R4

**Dependencies:** None

**Files:**
- Modify: `evals/grade.py`
- Modify: `evals/test_grade.py`

**Approach:**
- Add a second detection branch alongside the existing regex
- **Branch 1 (existing, preserved):** "It/this/that wasn't/isn't X. [repeat 2+] It/this/that was/is Z." — negation followed by affirmative reveal
- **Branch 2 (new):** 3+ consecutive sentences with the same subject ("you", "we", "they", "people") and a negated verb ("can't", "won't", "don't", "shouldn't", "couldn't", "cannot", "will not", "do not"). No affirmative reveal required. Threshold is 3 (not 2) because 2 consecutive "You don't" sentences are common in legitimate opinion and advice writing ("You don't owe your employer loyalty. You don't owe them overtime."). Three consecutive same-subject negations is the AI tell.
- Either branch triggering causes the check to fail
- Update the function docstring

**Patterns to follow:**
- The existing `check_countdown_negation` regex structure for Branch 1
- `check_anaphora` for the consecutive-sentence detection approach (Branch 2)

**Test scenarios:**
- Happy path: "You can't X. You can't Y. You can't Z." fails (Branch 2, 3 consecutive)
- Happy path: "It wasn't X. It wasn't Y. It was Z." still fails (Branch 1, regression)
- Happy path: single negation sentence passes
- Happy path: two "You can't" sentences passes — below the 3-sentence threshold for Branch 2 (legitimate rhetorical use: "You don't owe loyalty. You don't owe overtime.")
- Edge case: "You can't X. You can't Y. You can't Z. You can do W." also fails (Branch 2 fires on the three negations; the affirmative is irrelevant)
- Edge case: mixed pronouns ("You can't X. We can't Y. They can't Z.") passes — different subjects break the sequence
- Edge case: "cannot" (full form) also triggers

**Verification:**
- `python3 evals/test_grade.py` passes with no failures
- Human passthrough sample still scores 28/29
- Digital transformation text fails this check on the "You can't" sequence

---

- [ ] **Unit 3: Add `no-section-scaffolding` check**

**Goal:** Detect when a text reuses identical structural labels (like "How to make this work:") 3+ times, indicating a cookie-cutter section template.

**Requirements:** R1, R2, R4, R6

**Dependencies:** None

**Files:**
- Modify: `evals/grade.py`
- Modify: `evals/test_grade.py`
- Modify: `references/patterns.md`

**Approach:**
- Add a `check_section_scaffolding(text)` function
- Split text into lines, strip whitespace, normalise case
- Exclude empty lines and lines consisting only of punctuation or markdown markers (`#`, `##`, etc.)
- Strip leading markdown heading markers before comparison so `### How to make this work:` matches `How to make this work:`
- Count occurrences of each normalised line that appears 3+ times and is under 60 characters (to target label-like lines, not repeated prose sentences)
- Known limitation: trivially varied labels ("How to make this work in practice:" vs "How to make this work for your team:") will NOT be caught — only exact matches after normalisation. This is acceptable for a first implementation; fuzzy matching is a future improvement.
- Register as `"no-section-scaffolding"` in `ALL_CHECKS`
- Add pattern 38 ("Section scaffolding") to the "Structural tells" section of `references/patterns.md`

**Patterns to follow:**
- `check_formulaic_openers` for the line-by-line scanning approach
- Pattern entries 33-37 in `references/patterns.md` for the "Words to watch / Before / After" format

**Test scenarios:**
- Happy path: text with "How to make this work:" appearing 3 times fails
- Happy path: text with unique section labels passes
- Edge case: repeated label appearing only 2 times passes (below threshold)
- Edge case: long repeated sentences (>60 chars) are ignored — they're prose, not labels
- Edge case: case-insensitive matching ("How To Make This Work:" and "How to make this work:" count as the same)

**Verification:**
- `python3 evals/test_grade.py` passes with no failures
- Human passthrough sample still scores 28/29
- Digital transformation text fails this check on the repeated "How to make this work:" label
- Pattern 38 is added to `references/patterns.md` with before/after example

---

- [ ] **Unit 4: Update patterns.md metadata**

**Goal:** Fix stale metadata in patterns.md: update header count from 32 to 38, add "Voice and register" to the ToC, verify pattern numbering is consistent.

**Requirements:** R6

**Dependencies:** Unit 3 (pattern 38 added)

**Files:**
- Modify: `references/patterns.md`

**Approach:**
- Line 1: change "32 patterns" to "38 patterns"
- ToC: add `- [Voice and register (33-37)](#voice-and-register)` and update "Structural tells" to `(29-32, 38)` or renumber as appropriate
- Verify all 38 pattern headings are present and correctly numbered

**Test expectation: none -- metadata-only changes, no behavioral impact**

**Verification:**
- Pattern count in header matches actual H3 count
- ToC lists all 8 categories
- All pattern numbers 1-38 are present

---

- [ ] **Unit 5: Restructure SKILL.md process for mandatory structural self-audit**

**Goal:** Make the structural self-audit questions mandatory for all texts and elevate structural fixes from secondary "also check" items to primary requirements.

**Requirements:** R3, R5

**Dependencies:** Units 1-3 (new checks exist so the grader references are accurate)

**Files:**
- Modify: `SKILL.md`

**Approach:**

**Remove the depth classification gate.** The original plan proposed a "Step 0: Assess depth" where the agent classifies text as surface-AI or core-AI and only does structural work for core-AI. This creates a branch point the agent has an incentive to game (classifying as "surface-AI" means less work). Instead:

- Keep depth as lightweight context in Step 1 (a note: "If the grader pre-check shows multiple structural failures, the text is likely AI-generated from scratch and will need structural rewriting, not just word-swaps")
- Do NOT gate any work on depth classification

**Restructure Step 2: Fix** to have structural patterns first, not "also":
- Move the current "also check" items (structural monotony, tonal uniformity, resolution density, faux specificity, neutrality collapse, jargon distribution) to the top of Step 2 as primary items
- Surface fixes (vocabulary, formatting, manufactured insight, staccato) come second
- Remove the word "also" from all structural pattern references

**Make Step 3: Self-audit questions concrete, mandatory, and auditable:**
- "Do all sections follow the same arc? (problem -> evidence -> anecdote -> advice) If yes, restructure at least one."
- "Count paragraphs that end with a summary sentence. If more than half do, rewrite some to leave threads open."
- "Is there at least one register break — a moment of doubt, informality, or tonal shift?"
- "Count the triads. If there are more than 4, redistribute some as pairs or longer lists."
- These are concrete, countable questions that drive structural work regardless of text classification

**Enforcement mechanism:** The agent must SHOW its self-audit answers in the output (Step 3 of the output format already includes "What makes this so obviously AI generated?"). Update the output format to require the agent to answer each structural question with its actual count/finding, not just a pass/fail claim. Example: "Sections following same arc: 3/3 — restructured section 2 to lead with the anecdote. Triads: 7 → reduced to 3." This makes the self-audit auditable by the user even though it cannot be enforced programmatically. The grader checks (triad density, section scaffolding) provide partial enforcement for the questions that have programmatic backing; the output-format requirement provides transparency for the rest.

**Update check count references** from 29 to 31 throughout SKILL.md. **Also update pattern count references:** SKILL.md line 27 says "scan for all 32 patterns" (stale — should be 38), and the frontmatter says "37 patterns" (should be 38). Both need updating.

Keep changes focused and within the 500-line limit. Current SKILL.md is 282 lines, ~218 lines of headroom. Target: under 340 lines.

**Patterns to follow:**
- Existing Step 2 structure (numbered substeps)
- "Personality and soul" section tone (direct, example-driven)

**Test scenarios:**
- Happy path: SKILL.md is valid markdown with no broken links
- Edge case: stays under 500 lines
- Edge case: pattern catalogue reference still points to patterns.md correctly
- Edge case: grader command examples still reference grade.py correctly

**Verification:**
- `wc -l SKILL.md` is under 500
- All internal references to patterns.md and grade.py are correct
- The word "also check" no longer appears in Step 2 as a qualifier for structural patterns
- Self-audit contains all 4 mandatory structural questions
- Check count references updated from 29 to 31

---

- [ ] **Unit 6: Update documentation files**

**Goal:** Mark resolved items in ISSUES.md, update check counts across all files that reference them.

**Requirements:** R7

**Dependencies:** Units 1-5

**Files:**
- Modify: `ISSUES.md`
- Modify: `TESTING.md`
- Modify: `README.md`

**Approach:**
- **ISSUES.md:** Move "Structural monotony detection" from "Still outstanding LOW" to a new "Resolved" entry, noting: 2 new grader checks added (triad density, section scaffolding), 1 check extended (countdown negation), resolution density deferred as not programmatically tractable, skill process restructured with mandatory structural self-audit. Update the HIGH "Subtraction framing and skill restructure" item: mark the skill restructure portion as resolved, note that semantic preservation and subtraction-oriented evals remain outstanding. Mark "Vocabulary list reconciliation" as already resolved (all items are already in grade.py). Add new follow-up item: wire new checks into evals.json eval assertions.
- **TESTING.md:** Update all references from "29-check grader" to "31-check grader". Update stale assertion count (currently says "66-assertion" but actual is 87+ after new tests). Update coverage claim from "29 script checks cover 37 patterns" to "31 script checks cover 38 patterns".
- **README.md:** Update check count references from 29 to 31; update pattern count from 37 to 38

**Test expectation: none -- documentation-only changes**

**Verification:**
- No stale references to check counts in any file
- Resolved items clearly state what was done
- Outstanding items reflect actual remaining work
- `grep -rn "29.check\|29 checks\|29 programmatic\|All 29" TESTING.md README.md ISSUES.md SKILL.md` returns no stale check count references (do not grep bare "29" — it matches pattern numbers like "pattern 29")

---

- [ ] **Unit 7: Write human-authored false-positive test samples**

**Goal:** Broaden false-positive coverage beyond one personal narrative. The existing passthrough (a 4-paragraph accountant essay) has 0 triads, 0 section labels, 0 negation sequences — it doesn't stress-test the new checks. Add human-written samples in the genres most likely to trigger false positives.

**Requirements:** R2

**Dependencies:** None (can be done in parallel with Units 1-3)

**Files:**
- Create: `evals/samples/10-human-opinion.md`
- Create: `evals/samples/11-human-instructional.md`
- Modify: `evals/test_grade.py` (add passthrough assertions for new samples)

**Approach:**
- **Opinion piece** (~300-500 words): Write a genuine opinion/advice piece that uses 2 consecutive "You don't" sentences (legitimate rhetorical negation), some enumeration (2-3 triads), and a clear argumentative stance. This sample should PASS all checks including the new ones. It tests the boundary between legitimate rhetorical patterns and AI tells.
- **Instructional piece** (~400-600 words): Write a genuine how-to or tutorial that uses repeated structural labels (e.g., "Step 1:", "Step 2:", "Step 3:" — but NOT the same label 3 times), numbered sections, and some triads for legitimate enumeration. This sample should PASS the section scaffolding check (different labels) and triad density check (below threshold).
- Both samples must be genuinely human-written, not AI-generated. They should have natural register variation, imperfect structure, and authorial voice.
- Add `expect_pass` assertions for both samples against all new checks in test_grade.py.

**Patterns to follow:**
- `evals/samples/9-passthrough-human.md` for the existing human sample format

**Test scenarios:**
- Happy path: opinion piece passes all 31 checks (or fails only staccato, like the existing passthrough)
- Happy path: instructional piece passes all 31 checks
- Edge case: opinion piece with 2 consecutive "You don't" sentences passes countdown negation (below 3-sentence threshold)
- Edge case: instructional piece with repeated "Step N:" labels passes section scaffolding (labels differ by number)

**Verification:**
- Both samples pass all new checks
- Both samples are genuinely human-written (not AI-generated)
- `python3 evals/test_grade.py` passes with no failures

---

- [ ] **Unit 8: Multi-genre AI text validation**

**Goal:** Validate that the process restructuring (not just the grader checks) makes the skill robust across different AI-generated text genres. This is the primary robustness validation for the entire plan. Without it, the plan only proves it fixes one article's failure modes.

**Requirements:** R8, R9

**Dependencies:** Units 1-5 (grader checks and skill process must be complete)

**Files:**
- Create: `evals/samples/12-ai-tutorial.md` (AI-generated technical tutorial)
- Create: `evals/samples/13-ai-product-review.md` (AI-generated product review)
- Create: `evals/samples/14-ai-personal-reflection.md` (AI-generated personal reflection)

**Approach:**

Generate 3 AI texts in different genres using the current model (or collect existing AI outputs). Each should be 400-800 words and exhibit structural AI patterns — but NOT necessarily the same patterns as the digital transformation article. The point is to test whether the humaniser's structural self-audit catches genre-specific structural problems, not just triads and repeated labels.

For each text:
1. Run the grader pre-check (grade.py) — record what the grader catches
2. Run the humaniser skill with the restructured process
3. Check whether the self-audit answers show substantive structural engagement (not "I checked and it's fine")
4. Run the grader post-check — record the score
5. **Qualitative assessment (R9):** Read the first 3 paragraphs of the humanised output. Can you tell it was AI-generated from structure alone? If yes, the process failed for this genre.

**What success looks like:**
- The grader catches SOME patterns in each genre (not zero — the grader should have broad coverage)
- The structural self-audit identifies additional patterns the grader misses (this is the process change working)
- The self-audit answers are specific and countable, not vague ("Triads: 5 → 2", not "I reduced AI patterns")
- At least 2 of 3 texts pass the qualitative assessment (first 3 paragraphs don't read as structurally AI)

**What failure looks like:**
- The grader catches patterns in only the digital transformation genre — the checks are overfit
- The self-audit produces vague, unverifiable claims — the process change didn't work
- Humanised texts still read as AI from structure — the whole approach needs rethinking

This unit is a **validation gate**, not a code change. If it fails, the plan needs revision before merging.

**Test expectation: qualitative assessment — see success criteria above**

**Verification:**
- 3 AI-generated samples in different genres exist in evals/samples/
- Each sample has been run through the grader and humaniser
- Self-audit answers for each are specific and countable
- At least 2 of 3 pass the qualitative structural assessment (R9)

## System-Wide Impact

- **Grader score inflation:** Existing texts that scored 28/29 or 29/29 will now score lower if they contain structural patterns. This is intentional and correct — the previous scores were giving false confidence.
- **Skill process change affects agent behavior:** The mandatory structural self-audit and structural-first ordering in Step 2 will make the humaniser produce more heavily rewritten outputs for AI-generated text. This is the goal but means existing "light touch" expectations will change.
- **Check count references:** TESTING.md, README.md, SKILL.md, and ISSUES.md all reference the current check count (29). All need updating to 31. Note: `no-section-scaffolding` and `no-markdown-headings` may both fire on text with repeated markdown headings — the evidence strings should differentiate (headings-exist vs repeated-labels).
- **evals.json not updated in this work:** New checks will appear in grading output but are not wired into specific eval assertions. Follow-up item tracked in ISSUES.md.
- **No backward compatibility concern:** The grader is a standalone script, not a library. Adding checks doesn't break existing callers — they just get more expectations in the output.
- **Unit 8 is a validation gate:** It must pass before merging. If the qualitative assessment fails on 2+ of 3 genres, the plan's approach (grader checks + process restructuring) is insufficient for the stated goal of a robust skill, and needs revision.

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| Triad density false positives on human text with legitimate lists | Threshold of 4+ with 300-word floor provides margin. Human passthrough has 0 triads. Run against all 14 eval samples before merging. |
| Countdown negation extension catches non-AI patterns (e.g., rhetorical writing that uses repeated "You can't") | Require 3+ consecutive sentences with the same subject-verb pattern (threshold raised from 2 because 2 is legitimate in opinion writing). Test against human passthrough + new opinion piece sample. |
| Section scaffolding check flags legitimate repeated headers (e.g., recipe "Ingredients:" / "Instructions:") | 60-character line-length cap focuses on label-like lines. Threshold of 3+ identical lines. Recipes typically don't repeat the same label 3 times. |
| Mandatory structural self-audit adds work for all texts, including ones that don't need it | The structural questions are concrete and quick to answer ("Count the triads" — if the answer is 1, move on). The cost of always asking is low; the cost of not asking on core-AI text is the failure mode that motivated this plan. |
| Grader checks are overfit to one failure case (digital transformation article) | Unit 8 validates across 3 AI genres. If the grader catches patterns in only one genre, the checks need broadening. The process restructuring (Unit 5) is genre-independent and provides coverage where the grader doesn't. |
| The grader-as-quality-gate dynamic doesn't change — agent still optimises for score | The auditable self-audit (Unit 5) breaks this by requiring the agent to show its structural work, not just pass checks. The qualitative success criterion (R9) validates that the output actually reads as human, not just that it scores well. If Unit 8's qualitative assessment fails, the approach needs rethinking. |
| Section scaffolding check is trivially defeated by label variation | Acknowledged. The check's value is as a diagnostic signal during pre-check, not a quality gate. It works in concert with the self-audit question "Do all sections follow the same arc?" — the check catches the obvious case, the self-audit catches the rest. The check is the least important of the three grader additions. |

## Sources & References

- Related code: `evals/grade.py`, `evals/test_grade.py`, `SKILL.md`, `references/patterns.md`
- Related issue tracker: `ISSUES.md` (items: structural monotony LOW, subtraction framing HIGH)
- Prior analysis: `COVERAGE-ANALYSIS.md` (proposed `no-paragraph-template` check at line 159)
- Triggering failure case: digital transformation article humanised output scoring 28/29 but still reading as AI
