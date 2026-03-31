# Outstanding issues

Gaps identified from a full review of the codebase. Ordered by impact.

---

## 1. AI vocabulary list out of sync between SKILL.md and grade.py

**Files:** `SKILL.md:102-104`, `evals/grade.py:13-25`

SKILL.md lists these words in the AI vocabulary section that are missing from the grading script's `AI_VOCABULARY` list:

- `actually` (as filler intensifier)
- `land` / `lands` (as metaphor for "how something is received")
- `hidden` (when used to inflate significance of something ordinary)
- `seamless` (only `seamlessly` is in the script, not `seamless`)

The commit message for the most recent commit ("Add user-observed AI tells: genuinely, actually, land/lands, unspoken, hidden, but here's, the real X?") suggests these were added to the skill but only `genuinely` and `unspoken` made it into `grade.py`.

**Plan:** Add the missing words to `AI_VOCABULARY` in `grade.py`. For `actually`, `land`, `lands`, and `hidden`, consider whether they need context-sensitive matching (these are common English words that are only AI tells in specific usage patterns) or whether simple substring matching will produce too many false positives.

---

## 2. TESTING.md says "16-check script" but the script has 21 checks

**File:** `TESTING.md:18`

Line 18 references a "16-check script" but the rest of the document (including the results table) correctly references 21 checks. This is a stale reference from before the grading script was expanded from 16 to 21 checks (commit `7b86efa`).

**Plan:** Change "16-check script" to "21-check script" on line 18.

---

## 3. Missing eval definitions for 5 of 10 test samples

**File:** `evals/evals.json`

TESTING.md reports results for 10 samples but `evals.json` only defines 5 (Harris, Murray, Woolf, Wong, Orwell). The 5 "slop prompt" samples (Gratitude, Insect, Passion, End of life, Dunbar) have no eval definitions.

**Plan:** Add eval definitions for the 5 slop prompt samples to `evals.json`, with appropriate assertions matching the pattern used for the existing 5.

---

## 4. Eval sample files not committed

**File:** `evals/evals.json` references paths like `eval-harris-free-will/ai_output/essay.md`

The eval definitions reference AI output files that don't exist in the repo. Nobody can reproduce the test results without them.

**Plan:** Decide whether to commit the sample files or document that they are generated on-the-fly and not stored. If the latter, add a note to TESTING.md explaining how to regenerate them.

---

## 5. Automatable patterns missing from grade.py

**File:** `evals/grade.py`

Several patterns documented in `references/patterns.md` could be detected programmatically but have no corresponding check in the grading script:

| Pattern | Detection approach |
|---|---|
| 12. False ranges | Regex for repeated `from X to Y` constructions |
| 15. Title case headings | Check markdown headings for title-cased words |
| 18. Hyphenated modifier clusters | Count hyphenated compounds per sentence, flag at 3+ |
| 11. Synonym cycling | Harder, but could flag known synonym sets within short spans |

Adding these would improve the "30 of 32 patterns" coverage claim and bring the programmatic detection closer to the full 32.

**Plan:** Implement checks for patterns 12, 15, and 18 (all straightforward regex). Pattern 11 (synonym cycling) is harder and may not be worth the false-positive risk.

---

## 6. No check-to-pattern mapping documented

**Files:** `evals/grade.py`, `TESTING.md`

TESTING.md claims "21 programmatic checks covering 30 of 32 patterns" but there's no explicit mapping showing which checks cover which patterns. This makes it hard to verify the claim or identify coverage gaps.

**Plan:** Add a comment block or table to `grade.py` (or a section in TESTING.md) mapping each of the 21 checks to the pattern numbers it covers.

---

## 7. grade.py has potential false positives in common-word matching

**File:** `evals/grade.py:77-81`

The copula avoidance check flags `features` and `represents a` which are extremely common in normal English. The existing exclusion (`features` not followed by film/movie/documentary) is narrow. Similarly, `check_ghost_spectral` flags `hidden` and `lingering` which are ordinary words outside atmospheric contexts.

**Plan:** Review false-positive rates on the existing 10 test samples. If false positives are rare in practice, document the known edge cases. If they're common, add context-sensitive exclusions.

---

## 8. evals.json assertions don't cover all 21 grade.py checks

**File:** `evals/evals.json`

Each eval only lists 7-8 programmatic assertions, but the grading script runs 21 checks. For example, the Harris eval doesn't include `no-promotional-language`, `no-copula-avoidance`, `no-filler-phrases`, `no-forced-triads`, `no-superficial-ing`, `no-ghost-spectral-density`, `no-quietness-obsession`, `no-rhetorical-questions`, `no-excessive-lists`, or `no-dramatic-transitions`.

**Plan:** Either expand each eval's assertions to include all 21 checks, or add a note that the grading script runs all checks regardless (and the eval JSON assertions are a subset for the eval framework).
