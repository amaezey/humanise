# Outstanding issues (post-PR #1)

Issues remaining after the grader bugfix/expansion merge. Cross-referenced against ISSUES.md.

---

## Resolved in this branch

### 1. TESTING.md stale references (was issue 1, 7)

Line 18 said "16-check script", key findings said "21 script checks cover 30 of 32 patterns". Both updated to reflect the current 31-check grader.

### 2. AI vocabulary sync between SKILL.md and grade.py (was issue 2)

Added `seamless` to `AI_VOCABULARY`. Added context-sensitive regex patterns to `AI_VOCABULARY_REGEX` for `actually` (filler intensifier), `land/lands` (reception metaphor), and `hidden` (significance inflation). These avoid false positives on common English usage.

### 3. Broken eval file paths (was issue 4)

Updated all 5 original eval file paths from non-existent `eval-harris-free-will/ai_output/essay.md` to the actual files in `evals/samples/`.

### 4. Missing eval definitions (was issue 3)

Added 8 format-diversity sample evals plus 1 pass-through eval to `evals.json` (evals 5-13). Total: 14 evals, up from 5.

### 5. Short-form text false positive (was issue 5, part 1)

`sentence-length-variance` now skips texts under 100 words with fewer than 6 sentences. Fixes the false positive on the 4-sentence email (8-email-decline.md: 24/26 -> 26/27).

### 6. Passive hedging density (was issue 5, part 2)

Implemented `no-excessive-hedging` check. Detects impersonal passive hedging at density (4+ per text). Cooking blog now correctly caught (6 constructions). Human passthrough scores 0.

### 7. No pass-through test (from ISSUES.md broader testing gaps)

Added `9-passthrough-human.md`: human-written personal essay with named people, specific memories, and personal voice. Scores 26/27 (only fails staccato). Wired into evals.json as eval 13.

### 8. Vocabulary list reconciliation (was MEDIUM)

All flagged items (`fostering`, `showcasing`, `unparalleled`, `invaluable`, `bolstered`, `meticulous`) are already in grade.py's `AI_VOCABULARY`. Resolved in prior PRs.

### 9. Structural monotony detection (was LOW)

Two new grader checks (`no-triad-density`, `no-section-scaffolding`), one extended check (`no-countdown-negation` with pronoun variants). SKILL.md process restructured with mandatory structural self-audit. Resolution density deferred as not programmatically tractable.

---

## Still outstanding

### HIGH: Subtraction framing and skill restructure (from April 2026 research)

Abdulhai et al. (2026) show LLMs subtract meaning (~70% neutrality increase, 50% pronoun depletion), not just add patterns. The skill's architecture is almost entirely additive detection.

**Resolved (prior PR #3):**
- ~~Restructure "Personality and soul" to lead with the subtraction framing~~
- ~~Add semantic preservation warning to the Process section~~
- ~~Add 5 new patterns (33–37): countdown negation, miniature conclusions, tonal uniformity, faux specificity, neutrality collapse~~
- ~~New "Voice and register" category (8th)~~
- ~~Add new programmatic checks: countdown negation regex, type-token ratio, vocabulary items~~

**Resolved (this branch):**
- ~~Expand self-audit with Abdulhai-informed questions~~ — SKILL.md process restructured with mandatory structural self-audit

**Still outstanding:**
- Semantic preservation testing (verify the rewriting step doesn't itself neutralise stance)
- Subtraction-oriented evals (see LOW item below)

### MEDIUM: No regression test for original 10/10 results

TESTING.md notes the original 10 humanised outputs need re-running against the 31-check grader. Requires the original output files (still in Obsidian vault, not version-controlled).

### LOW: Wire new checks into evals.json eval assertions

The 2 new grader checks (`no-triad-density`, `no-section-scaffolding`) and the extended `no-countdown-negation` (pronoun variants) need corresponding `expect_fail` / `expect_pass` assertions wired into the eval definitions in `evals.json`.

### LOW: No cross-model samples

No GPT/Gemini/Llama samples to verify checks work across models. Stylometry research (Zaitsu et al. 2025) confirms most commercial LLMs cluster together stylistically — only Llama 3.1 was distinct. This validates the current approach of targeting shared patterns but cross-model samples would confirm.

### LOW: No CI or regression tracking

No automated pipeline. A SKILL.md edit could regress quality silently.

### LOW: Subtraction-oriented evals

Current evals test "did the AI tells get removed?" (additive). No evals test "did the author's stance survive?" (subtractive). Consider: take opinionated input, humanise it, check the opinion survived. Different eval type from current approach.
