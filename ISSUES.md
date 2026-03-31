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

## Grader gaps (not yet implemented)

These are patterns the grader has no check for at all. Ordered by priority.

### HIGH: Formulaic paragraph openers

AI text opens paragraphs with a small rotation of transition formulae. Appeared in 6/8 slop samples, triggered zero checks.

Examples:
- "At a foundational level,"
- "Beyond access and curation,"
- "Beyond practicality,"
- "At its core,"
- "There is also a practical dimension"
- "There is a social dimension"
- "It is also worth recognising that"
- "From a [noun] perspective"

**Proposed check: `no-formulaic-openers`** — regex list of paragraph-initial phrases.

### HIGH: Signposted conclusions

AI nearly always labels its conclusion. Human writers rarely do this outside academic papers.

Examples:
- "In summary, public libraries are not legacy institutions"
- "Conclusion" as a section heading
- "In conclusion,"
- "To summarise,"

**Proposed check: `no-signposted-conclusions`** — regex for "In summary,", "In conclusion,", "To summarise,", "To sum up,", and "## Conclusion" / "Conclusion\n" as headings.

### HIGH: H1/H2 heading structure in prose

AI-generated essays almost always use markdown headings (`# Title`, `## Section`). Real essays don't have `##` subheadings. All 5 essay-topic slop samples used H1 + H2 structure. This is trivially detectable and a strong signal.

**Proposed check: `no-markdown-headings`** — flag if text contains `#` heading syntax (with possible exception for documents that legitimately need it).

### MEDIUM: Corporate AI register

The cover letter scored 21/21. None of the existing word lists cover this register.

Examples:
- "deliver impact"
- "measurable outcomes"
- "deliverable outcomes"
- "scalable.*systems"
- "pragmatic approach"
- "drives.*outcomes"
- "cross-functional"
- "end-to-end development"

**Proposed check: `no-corporate-ai-speak`** — word list.

### MEDIUM: Impersonal "This" chains

AI starts consecutive sentences with "This [verb]" to simulate logical progression. The anaphora check doesn't catch it because "this" is implicitly excluded (similar to "the", "it").

Examples:
- "This exposes how much of identity is contingent"
- "This conditions decision-making under constraint"
- "This characteristic is significant."

**Proposed check: `no-this-chains`** — flag 3+ sentences in a paragraph starting with "This [verb]".

**Technical note:** The anaphora check explicitly excludes common starters including "it" and "the". "This" would need to either be removed from that exclusion list or handled in a separate check.

### MEDIUM: Short-form text handling

The 4-sentence email failed `sentence-length-variance` (stdev 3.1 vs target >4). A short email can't have high variance — this is a false positive, not a real AI tell.

**Proposed fix:** Skip `sentence-length-variance` for texts under 100 words or under 6 sentences.

### LOW: Passive impersonal hedging density

AI hedges with impersonal passive constructions at higher density than human writing. Individually these are fine; it's the density that's the tell.

Examples from one sample:
- "is often framed as"
- "is difficult to ignore"
- "is not a compromise but a requirement"
- "is contingent on"

**Proposed check: `no-excessive-hedging`** — count per paragraph, flag above threshold.

### LOW: Structural monotony

Every paragraph in AI samples follows the same template: topic sentence → elaboration → restatement. Human writing varies paragraph structure. Hard to check programmatically.

**Proposed check: `no-paragraph-template`** — measure paragraph length variance. If all paragraphs are within a narrow band (e.g. all 3-5 sentences), flag.

---

## Broader testing gaps

### No short-form evals

All 5 original evals are long-form essays. People actually humanise emails, cover letters, product descriptions, LinkedIn posts, blog intros. The 8 samples in `evals/samples/` cover some of these but aren't wired into `evals.json`.

### No pass-through test

What happens when input is already human-written? The skill should leave it mostly alone. This is untested.

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

### Essay-topic samples (matching original 5 evals)

| File | Topic | Score (fixed grader) | Key failures |
|------|-------|---------------------|--------------|
| `harris-free-will.md` | Free will is an illusion | 18/21 | em dashes, promotional, significance inflation |
| `murray-doctors-die.md` | How doctors choose to die | 16/21 | em dashes, manufactured insight, anaphora, promotional, significance inflation |
| `woolf-moth.md` | Moth struggling against window | 17/21 | em dashes, manufactured insight, promotional, copula avoidance |
| `wong-monkeysphere.md` | Dunbar's number explains everything | 18/21 | em dashes, anaphora, significance inflation |
| `orwell-why-write.md` | Motivations for writing | 18/21 | em dashes, promotional, negative parallelisms |

### Format-diversity samples

| File | Type | Score (fixed grader) | Key failures |
|------|------|---------------------|--------------|
| `1-essay-libraries.md` | Long-form essay | 17/21 | em dashes, AI vocab, copula avoidance, triads |
| `2-blog-cooking.md` | Blog post | 18/21 | em dashes, negative parallelisms, filler |
| `3-listicle-remote.md` | Listicle | 17/21 | em dashes, anaphora, negative parallelisms, triads |
| `4-reflection-travel.md` | Personal reflection | 17/21 | em dashes, negative parallelisms, filler, triads |
| `5-explainer-quantum.md` | Technical explainer | 19/21 | em dashes, collaborative artifacts |
| `6-cover-letter.md` | Cover letter | **21/21** | **nothing — biggest blind spot** |
| `7-hotel-description.md` | Product copy | 19/21 | em dashes, copula avoidance |
| `8-email-decline.md` | Short email | 19/21 | em dashes, sentence variance (false positive on short text) |
