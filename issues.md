# Outstanding issues (post-PR #1)

Issues remaining after the grader bugfix/expansion merge. Cross-referenced against ISSUES.md.

---

## Resolved in this branch

### 1. TESTING.md stale references (was issue 1, 7)

Line 18 said "16-check script", key findings said "21 script checks cover 30 of 32 patterns". Both updated to reflect the current 26-check grader.

### 2. AI vocabulary sync between SKILL.md and grade.py (was issue 2)

Added `seamless` to `AI_VOCABULARY`. Added context-sensitive regex patterns to `AI_VOCABULARY_REGEX` for `actually` (filler intensifier), `land/lands` (reception metaphor), and `hidden` (significance inflation). These avoid false positives on common English usage.

### 3. Broken eval file paths (was issue 4)

Updated all 5 original eval file paths from non-existent `eval-harris-free-will/ai_output/essay.md` to the actual files in `evals/samples/`.

### 4. Missing eval definitions (was issue 3)

Added 8 format-diversity sample evals to `evals.json` (essays 5-12), each with targeted programmatic assertions matching their content type. Total: 13 evals, up from 5.

### 5. Short-form text false positive (was issue 5, part 1)

`sentence-length-variance` now skips texts under 100 words with fewer than 6 sentences. Fixes the false positive on the 4-sentence email (8-email-decline.md: 24/26 -> 25/26).

---

## Still outstanding

### MEDIUM: Passive impersonal hedging density

From ISSUES.md "not yet implemented". AI hedges with impersonal passive constructions at higher density than human writing. Needs threshold tuning.

### LOW: Structural monotony detection

From ISSUES.md "not yet implemented". Every AI paragraph follows topic sentence -> elaboration -> restatement. Hardest gap to close programmatically.

### MEDIUM: No regression test for original 10/10 results

TESTING.md notes the original 10 humanised outputs need re-running against the 26-check grader. Requires the original output files (still in Obsidian vault, not version-controlled).

### LOW: No pass-through test

What happens when input is already human-written? Untested.

### LOW: No cross-model samples

No GPT/Gemini/Llama samples to verify checks work across models.

### LOW: No CI or regression tracking

No automated pipeline. A SKILL.md edit could regress quality silently.
