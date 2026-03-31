# Test coverage analysis

## Method

Ran 8 AI-generated text samples through `grade.py` — each designed to trigger specific pattern categories. All samples were produced by Claude (Sonnet 4) using simple prompts with no instruction to avoid AI tells.

## Results

| # | Sample | Type | Score | Failures |
|---|--------|------|-------|----------|
| 1 | Public libraries essay | Long-form essay | 18/21 | em dashes, AI vocab clustering, forced triads |
| 2 | Learn to cook blog | Blog post | 20/21 | em dashes |
| 3 | Remote work listicle | Listicle | 18/21 | em dashes, anaphora, forced triads |
| 4 | Travel reflection | Personal reflection | 20/21 | em dashes |
| 5 | Quantum computing explainer | Technical explainer | 20/21 | em dashes |
| 6 | Cover letter | Professional email | **21/21** | **none** |
| 7 | Boutique hotel description | Product copy | 19/21 | em dashes, copula avoidance |
| 8 | Meeting decline email | Short email | 19/21 | em dashes, sentence-length-variance |

**Average score: 19.5/21 (93%).** Every sample is obviously AI-generated. The grader barely notices.

The cover letter — stereotypical AI corporate prose ("With extensive experience designing and delivering scalable, production-grade systems, I bring a pragmatic approach") — scored a perfect 21/21.

## What the grader catches well

- **Em dashes**: caught in 7/8 samples. This is the most reliable signal.
- **Forced triads**: caught abstract "X, Y, and Z" patterns in 2 samples.
- **Copula avoidance**: caught "features" in the hotel description.

## What the grader misses

### 1. Formulaic paragraph openers

AI text opens paragraphs with a small rotation of transition formulae. These appeared across nearly every sample but triggered zero checks.

Examples from the samples:
- "At a foundational level," (libraries)
- "Beyond access and curation," (libraries)
- "Beyond practicality," (cooking)
- "At its core," (cooking)
- "There is also a practical dimension" (cooking)
- "There is a social dimension" (cooking)
- "It is also worth recognising that" (cooking)

**Proposed check: `no-formulaic-openers`** — flag paragraphs starting with "At a foundational level", "Beyond [noun],", "At its core,", "There is also a", "It is also worth", "From a [noun] perspective", "On a [adjective] level".

### 2. Impersonal "This" chains

AI loves starting consecutive sentences with "This [verb]" to simulate logical progression. The anaphora check doesn't catch it because "this" is implicitly excluded (similar to "the", "it").

Examples:
- "This exposes how much of identity is contingent" (travel)
- "This conditions decision-making under constraint" (travel)
- "This characteristic is significant." (libraries)
- "This shifts labour market competition" (remote work)
- "This includes designing APIs" (cover letter)

**Proposed check: `no-this-chains`** — flag 3+ sentences in a paragraph starting with "This [verb]".

### 3. "Not X — it's Y" reframing (manufactured insight variant)

The manufactured insight check catches "here's the thing" and "what's really", but misses the subtler AI move of reframing via negation. This appeared in 4/8 samples.

Examples:
- "Learning to cook is not just about feeding yourself. It is about capability, autonomy, and connection." (cooking)
- "Travel is less about discovering new places than about testing the stability of the self" (travel)
- "Learning to cook is therefore not about becoming a chef. It is about reclaiming a fundamental capability." (cooking)
- "The primary transformation is not technological but managerial" (remote work)
- "These are not personality labels but operational boundaries" (travel)

**Proposed check: extend `no-manufactured-insight`** — add patterns for "is not about X. It is about Y", "is less about X than about Y", "is not X but Y" when X and Y are abstract nouns.

### 4. Passive impersonal hedging density

AI text hedges with impersonal passive constructions at much higher density than human writing. The filler check only catches specific phrases like "in order to" and "it is worth noting". It misses the broader pattern.

Examples from a single sample (cooking):
- "is often framed as"
- "is difficult to ignore"
- "is not a compromise but a requirement"
- "is overstated"

**Proposed check: `no-excessive-hedging`** — count passive impersonal constructions ("is often [verb]ed", "is increasingly [verb]ed", "is not guaranteed", "is contingent on") and flag when density exceeds a threshold per paragraph.

### 5. "In summary" / "In conclusion" closings

AI text almost always signals its conclusion with an explicit label. Human writers rarely do this outside academic papers.

Examples:
- "In summary, public libraries are not legacy institutions" (libraries)
- "Conclusion" as a section heading (travel, remote work)

**Proposed check: `no-signposted-conclusions`** — flag "In summary,", "In conclusion,", "To summarise,", "To sum up,", and "Conclusion" as a heading.

### 6. Soft collaborative artifacts

The collaborative artifact check catches "I hope this helps" and "let me know", but misses softer variants where the AI offers to do more work or frames its output as a service.

Example:
- "If needed, the explanation can be reframed for a policy or procurement audience (e.g. implications for encryption, sovereign capability, or investment risk)." (quantum)

**Proposed check: extend `no-collaborative-artifacts`** — add patterns for "if needed,? (?:I can|the .* can be|this can be) (?:reframed|expanded|adjusted|tailored)", "feel free to", "don't hesitate to".

### 7. Short-form text handling

The email (sample 8) failed `sentence-length-variance` (stdev 3.1 vs target >4) — but this is expected for a 4-sentence email. The check penalises short texts unfairly.

**Proposed fix**: skip `sentence-length-variance` for texts under 100 words or under 6 sentences.

### 8. No check for structural monotony

Every paragraph in the AI samples follows the same template: topic sentence, elaboration, implication/restatement. Human writing varies paragraph structure — some are one sentence, some meander, some start with evidence before the claim. This is the hardest gap to close programmatically but is arguably the strongest AI signal.

**Proposed check: `no-paragraph-template`** — measure similarity of paragraph structures (e.g. sentence count per paragraph, variance of paragraph lengths). If all paragraphs are within a narrow band (e.g. 3-5 sentences each), flag it.

### 9. Corporate/LinkedIn register

The cover letter scored 21/21 despite being full of AI corporate speak: "pragmatic approach", "translate ambiguous requirements into clear, deliverable outcomes", "drives measurable outcomes", "deliver impact quickly". None of the existing word lists cover this register.

**Proposed check: `no-corporate-ai-speak`** — word list for "deliver impact", "measurable outcomes", "deliverable outcomes", "scalable.*systems", "pragmatic approach", "drives.*outcomes", "cross-functional", "end-to-end".

## Priority ranking

| Priority | Check | Difficulty | Samples caught |
|----------|-------|------------|----------------|
| **High** | Formulaic paragraph openers | Easy (regex list) | 6/8 |
| **High** | "Not X — it's Y" reframing | Easy (extend existing) | 4/8 |
| **High** | Signposted conclusions | Easy (regex list) | 3/8 |
| **High** | Soft collaborative artifacts | Easy (extend existing) | 1/8 but high-signal |
| **Medium** | Corporate AI register | Easy (word list) | 1/8 but covers a blind spot |
| **Medium** | Impersonal "This" chains | Easy (regex) | 3/8 |
| **Medium** | Short-form text handling | Easy (conditional) | Prevents false positives |
| **Low** | Passive hedging density | Medium (threshold tuning) | 4/8 |
| **Low** | Structural monotony | Hard (statistical) | 6/8 |

## Broader test gaps

Beyond new checks, the testing methodology has gaps:

1. **No short-form evals.** All 5 existing evals are long-form essays. Emails, cover letters, product descriptions, and social posts are what people actually ask to humanise. The 8 samples in `evals/samples/` are a start.

2. **No pass-through test.** What happens when the input is already human-written? The skill should leave it mostly alone. Currently untested.

3. **No grade.py self-tests.** If a regex has a typo or a word list is wrong, nothing catches it. The grading script should have its own unit tests with known-good and known-bad snippets for each check.

4. **No cross-model samples.** TESTING.md notes "Claude doesn't produce the same slop as ChatGPT" but there are no GPT/Gemini/Llama samples in the eval suite to verify the checks work across models.

5. **No regression tracking.** No CI, no historical scores. A SKILL.md edit could regress quality silently.

## Sample files

8 AI-generated samples saved to `evals/samples/` for use in future testing:

| File | Prompt | Patterns targeted |
|------|--------|-------------------|
| `1-essay-libraries.md` | Importance of public libraries | Significance inflation, promotional language |
| `2-blog-cooking.md` | Why everyone should learn to cook | Staccato rhythm, generic conclusions |
| `3-listicle-remote.md` | 7 ways remote work transforms work | Excessive lists, filler phrases |
| `4-reflection-travel.md` | What travel teaches us | Manufactured insight, copula avoidance |
| `5-explainer-quantum.md` | Quantum computing for general audience | AI vocabulary, hedging |
| `6-cover-letter.md` | Senior engineer cover letter | Sycophantic tone, collaborative artifacts |
| `7-hotel-description.md` | Boutique hotel in historic city | Promotional, ghost/spectral language |
| `8-email-decline.md` | Decline meeting, suggest alternative | Collaborative artifacts, filler |
