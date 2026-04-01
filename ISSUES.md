# Known issues, proposals, and technical learnings

Living document. Updated as issues are found.

---

## Grader bugs (fixed)

These were bugs in existing checks that caused false passes on obvious AI text. All fixed and covered by `test_grade.py`.

### 1. COPULA_AVOIDANCE only matched singular verb forms

`"serves as"` caught "The library serves as" but missed "Libraries serve as". Same for `functions as`, `stands as`, etc. Fixed by changing to `serves? as`, `functions? as`, etc.

### 2. AI_VOCABULARY substring match missed inflected multi-word phrases

`"align with"` is checked via `if w in text_lower`. This misses "aligns with" because the `s` between "align" and " with" breaks the substring match. `"align with"` is NOT a substring of `"aligns with"`.

This is the bug that let the cover letter score 21/21. Fixed by adding a separate `AI_VOCABULARY_REGEX` list for multi-word phrases that need inflection handling.

**Technical gotcha:** Python substring matching (`"align with" in "aligns with"`) returns `False` because the characters don't appear consecutively. Any new multi-word AI vocabulary entries need to go in the regex list, not the simple substring list, if the first word can be inflected.

### 3. no-negative-parallelisms only matched within a single sentence

The regex `r"not just\b.*?\bbut\b"` works for "not just X but Y" in one sentence. But AI commonly splits this across sentences: "Learning to cook is not about becoming a chef. It is about reclaiming a fundamental capability."

Fixed by adding cross-sentence patterns: `r"not (?:about|just about) [\w\s]+\.\s+it is (?:about|a\b)"`.

**Technical gotcha:** `count_pattern_matches` lowercases text first, so cross-sentence patterns matching "It is" need to be written as `"it is"` (lowercase). The `re.split` sentence splitter removes this context, which is why the original single-sentence regex couldn't catch it — the check operates on full text, not split sentences.

### 4. COLLABORATIVE_ARTIFACTS missed soft variants

Caught "I hope this helps" but missed "If needed, the explanation can be reframed for a policy audience" — a textbook offer-to-continue. Also missed "feel free to" and "don't hesitate to".

### 5. FILLER_PHRASES too specific

Had "it is worth noting" but not "it is worth recognising/mentioning/emphasising". Missed "is often framed as", a ubiquitous AI hedging opener. Fixed with regex alternation.

### 6. no-forced-triads suffix list too narrow

Only matched -ing, -tion, -ment, -ness, -ity. Missed -ence (resilience), -ance (tolerance), -sion (expression), -cy (democracy), -ism (optimism). Many abstract triads use these suffixes.

### 7. no-rhetorical-questions missed bare "It"

Pattern had `It's` in the alternation for answer-openers but not `It`. A rhetorical question answered with "It depends on the project." was missed.

---

## Grader gaps (implemented)

These were patterns the grader had no check for. Now implemented and covered by `test_grade.py`.

- **`no-formulaic-openers`** — "At a foundational level,", "Beyond X,", "At its core,", "There is also a...", "From a [noun] perspective", etc. Caught in 6/8 original slop samples.
- **`no-signposted-conclusions`** — "In summary,", "In conclusion,", "Conclusion" headings. Caught in 7/13 samples.
- **`no-markdown-headings`** — `#` and `##` heading syntax in prose. Caught in all 5 essay-topic samples.
- **`no-corporate-ai-speak`** — "deliver impact", "measurable outcomes", "end-to-end development", etc. Finally catches the cover letter (was 21/21, now 25/26).
- **`no-this-chains`** — 3+ consecutive "This [verb]" sentences in a paragraph.

## Grader gaps (not yet implemented)

### ~~MEDIUM: Short-form text handling~~ (FIXED)

The 4-sentence email failed `sentence-length-variance` (stdev 3.1 vs target >4). Fixed: `sentence-length-variance` now skips texts under 100 words with fewer than 6 sentences. Email sample improved from 24/26 to 25/26.

### ~~LOW: Passive impersonal hedging density~~ (IMPLEMENTED)

Added `no-excessive-hedging` check. Detects impersonal passive hedging constructions ("is often framed as", "is contingent on", "cannot be overstated", "is overstated", "is less about...more about", "a common assumption is", etc.) and flags at 4+ across the whole text. Cooking blog correctly caught with 6 hedging constructions. Human passthrough scores 0.

### LOW: Structural monotony

Every paragraph in AI samples follows the same template: topic sentence → elaboration → restatement. Human writing varies paragraph structure. Hard to check programmatically.

**Proposed check: `no-paragraph-template`** — measure paragraph length variance. If all paragraphs are within a narrow band (e.g. all 3-5 sentences), flag.

---

## Broader testing gaps

### No short-form evals

All 5 original evals are long-form essays. People actually humanise emails, cover letters, product descriptions, LinkedIn posts, blog intros. The 8 samples in `evals/samples/` cover some of these but aren't wired into `evals.json`.

### ~~No pass-through test~~ (ADDED)

Added `9-passthrough-human.md`: a human-written personal essay with named people, specific memories, and personal voice. Scores 26/27 (only fails staccato, which is a known acceptable false positive on short conversational sentences). Wired into `evals.json` as eval 13.

### No cross-model samples

TESTING.md notes "Claude doesn't produce the same slop as ChatGPT" but there are no GPT/Gemini/Llama samples to verify the checks work across models. Claude slop tends to be subtler — it avoids the sensory/atmospheric patterns but still does formulaic openers, hedging, and structural monotony.

### No regression tracking

No CI, no historical scores. A SKILL.md edit could regress quality silently. The `test_grade.py` self-tests protect the grader's correctness but not the skill's output quality.

### Original eval text files not in repo

The 5 original human-written texts and their AI-generated + humanised versions are in an Obsidian vault, not version-controlled. This means the grader bugfixes can't be regression-tested against the original 10/10 pass results without manual effort.

---

## Technical gotchas for future check development

1. **Substring vs regex for multi-word vocab.** `"align with" in "aligns with"` is `False` in Python. Any multi-word phrase where the first word can be inflected (pluralised, conjugated) needs regex, not substring matching. This applies to: "align with", "shed light on" (sheds/shedding), "serve as" (serves/served).

2. **`count_pattern_matches` lowercases text.** All regex patterns in the pattern lists must be lowercase. If you write `r"It is"` it won't match because the text is lowercased before matching.

3. **Cross-sentence patterns need full-text matching.** The `split_sentences` utility splits on `[.!?]\s+`, which destroys the boundary between sentences. Checks that need to match across sentence boundaries (like cross-sentence negative parallelisms) must operate on the full text, not split sentences.

4. **Anaphora check excludes common words.** The words "i", "a", "the", "it's", "it" are excluded from anaphora detection. This means "This" as a sentence starter won't trigger anaphora (it starts with a different word each time the underlying subject changes). If "This" chains become a check, it needs its own logic.

5. **The forced triads check only matches abstract nouns by suffix.** Concrete triads like "apples, bread, and milk" correctly pass. But abstract nouns with unusual suffixes (e.g. "speed", "trust", "hope") also pass. The suffix list is a reasonable heuristic but will miss some abstract triads.

6. **`features` in copula avoidance has a film/movie exception.** The regex `r"features?\b(?! film| movie| documentary)"` avoids flagging "the film features..." — but the exception is fragile. Other legitimate uses of "features" (e.g. "software features") could false-positive.

---

## Slop sample inventory

All scores below are against the current 27-check grader.

### Essay-topic samples (matching original 5 evals)

| File | Topic | Score | Key failures |
|------|-------|-------|--------------|
| `harris-free-will.md` | Free will is an illusion | 21/27 | em dashes, promotional, significance inflation, formulaic openers, signposted conclusions, markdown headings |
| `murray-doctors-die.md` | How doctors choose to die | 20/27 | em dashes, manufactured insight, anaphora, promotional, significance inflation, signposted conclusions, markdown headings |
| `woolf-moth.md` | Moth struggling against window | 21/27 | em dashes, manufactured insight, promotional, copula avoidance, signposted conclusions, markdown headings |
| `wong-monkeysphere.md` | Dunbar's number explains everything | 22/27 | em dashes, anaphora, significance inflation, signposted conclusions, markdown headings |
| `orwell-why-write.md` | Motivations for writing | 22/27 | em dashes, promotional, negative parallelisms, signposted conclusions, markdown headings |

### Format-diversity samples

| File | Type | Score | Key failures |
|------|------|-------|--------------|
| `1-essay-libraries.md` | Long-form essay | 21/27 | em dashes, AI vocab, copula avoidance, triads, formulaic openers, signposted conclusions |
| `2-blog-cooking.md` | Blog post | 22/27 | em dashes, negative parallelisms, filler, formulaic openers, excessive hedging |
| `3-listicle-remote.md` | Listicle | 21/27 | em dashes, anaphora, negative parallelisms, triads, signposted conclusions, corporate AI speak |
| `4-reflection-travel.md` | Personal reflection | 22/27 | em dashes, negative parallelisms, filler, triads, signposted conclusions |
| `5-explainer-quantum.md` | Technical explainer | 25/27 | em dashes, collaborative artifacts |
| `6-cover-letter.md` | Cover letter | 26/27 | corporate AI speak |
| `7-hotel-description.md` | Product copy | 25/27 | em dashes, copula avoidance |
| `8-email-decline.md` | Short email | 26/27 | em dashes |

### Pass-through sample

| File | Type | Score | Key failures |
|------|------|-------|--------------|
| `9-passthrough-human.md` | Human-written personal essay | 26/27 | staccato (false positive on short human sentences) |
