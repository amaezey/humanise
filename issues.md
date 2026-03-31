# Outstanding issues (post-PR #1)

Issues remaining after the grader bugfix/expansion merge. Cross-referenced against ISSUES.md.

---

## 1. TESTING.md line 18 still says "16-check script"

**File:** `TESTING.md:18`

The rest of the doc correctly references 26 checks, but line 18 still reads: `16-check script (`evals/grade.py`)`. Should be `26-check script`.

**Severity:** Low (stale copy)
**Fix:** One-line edit.

---

## 2. AI vocabulary words in SKILL.md missing from grade.py

**File:** `SKILL.md:102-104`, `evals/grade.py:13-33`

SKILL.md lists these words that aren't in grade.py's `AI_VOCABULARY` or `AI_VOCABULARY_REGEX`:

- `actually` (as filler intensifier)
- `land` / `lands` (as metaphor for reception)
- `hidden` (when inflating significance)
- `seamless` (only `seamlessly` is present)

These were added to the skill docs in commit `43e882b` but only `genuinely` and `unspoken` made it into the grading script.

**Severity:** Medium (grader misses words the skill says to catch)
**Plan:** Add to `AI_VOCABULARY`. For `actually`, `land`, and `hidden`, consider false-positive risk since they're common English words. May need context-sensitive regex in `AI_VOCABULARY_REGEX` rather than simple substring matching.

---

## 3. evals.json only defines 5 of 10+ test samples

**File:** `evals/evals.json`

- Only 5 evals (Harris, Murray, Woolf, Wong, Orwell)
- The 5 slop prompt samples from the original TESTING.md results aren't defined
- The 8 new format-diversity samples in `evals/samples/` aren't wired in either
- ISSUES.md explicitly notes: "The 8 samples in `evals/samples/` cover some of these but aren't wired into `evals.json`"

**Severity:** Medium (eval infrastructure exists but can't run the full test suite)
**Plan:** Add eval definitions for the 8 format-diversity samples and the 5 slop prompt samples.

---

## 4. Original 5 eval file paths are broken

**File:** `evals/evals.json`

The existing 5 evals reference paths like `eval-harris-free-will/ai_output/essay.md` which don't exist. ISSUES.md notes: "The 5 original human-written texts and their AI-generated + humanised versions are in an Obsidian vault, not version-controlled."

**Severity:** Medium (evals can't be reproduced)
**Plan:** Either commit the files or update paths to point to the samples in `evals/samples/` (which do contain these essays, e.g. `evals/samples/harris-free-will.md`).

---

## 5. ISSUES.md has three "not yet implemented" proposals

**File:** `ISSUES.md`

Three grader gaps are documented but not implemented:

| Proposal | Difficulty | Notes |
|---|---|---|
| Short-form text handling (skip variance for <100 words) | Easy | Prevents false positives on emails |
| Passive impersonal hedging density | Medium | Threshold tuning needed |
| Structural monotony (paragraph template detection) | Hard | Strongest AI signal but hardest to code |

**Severity:** Low-Medium
**Plan:** Implement the short-form text fix (easy win). The other two are lower priority.

---

## 6. No regression test for the original 10/10 results

**File:** `TESTING.md:43`

TESTING.md now notes: "These results were against the original 21-check grader. The grader has since been expanded to 26 checks... The original 10 samples need re-running against the updated grader to confirm they still pass."

**Severity:** Medium (expanded grader may fail previously-passing output)
**Plan:** Re-run the 10 original humanised outputs through the 26-check grader. This requires the original output files (see issue 4).

---

## 7. TESTING.md key findings section is stale

**File:** `TESTING.md:66-72`

The key findings still say "21 script checks cover 30 of 32 patterns" but the grader now has 26 checks. The coverage claim needs updating.

**Severity:** Low (stale copy)
**Fix:** Update to reflect 26 checks and current coverage.
