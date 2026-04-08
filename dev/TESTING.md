# Testing methodology

## Approach

Three rounds of isolation-based testing, where no agent has access to information it shouldn't:

1. **Pick human-written originals.** Five pre-AI essays across different voices:
   - Sam Harris, ["Free will"](https://www.samharris.org/blog/the-illusion-of-free-will) (2012)
   - Ken Murray, ["How doctors die"](https://www.zocalopublicsquare.org/2011/11/30/how-doctors-die/ideas/nexus/) (2011)
   - Virginia Woolf, ["The Death of the Moth"](https://gutenberg.net.au/ebooks12/1203811h.html) (1942)
   - David Wong, ["What is the Monkeysphere?"](https://www.cracked.com/article_14990_what-monkeysphere.html) (2007)
   - George Orwell, ["Why I write"](https://orwellfoundation.com/george-orwell/by-orwell/essays-and-other-works/why-i-write/) (1946)

2. **Generate AI versions with isolated agents.** Each agent got a content brief but never saw the original text. This produced AI-flavoured rewrites of the same content.

3. **Humanise with isolated agents.** Separate agents applied the skill blind (no access to originals), exactly as it works in real use.

4. **Grade programmatically.** 31-check script (`evals/grade.py`) tests for em dashes, AI vocabulary clustering, manufactured insight, staccato sequences, anaphora, hedging density, and 23 other patterns.

5. **Compare to originals.** Read the humanised output alongside the original human text to check voice, meaning, and plausibility.

6. **Fix failures and re-run.** When Wong's piece kept "And honestly?" because the agent thought it served the humour, we tightened the hard constraints and re-ran until it passed.

## Results

### Original run: pre-check/post-check loop, 10 samples, 21 checks

| Sample | Pre-check | Post-check |
|---|---|---|
| Harris (free will) | 20/21 | **21/21** |
| Murray (how doctors die) | 15/21 | **21/21** |
| Woolf (death of the moth) | 20/21 | **21/21** |
| Wong (monkeysphere) | 17/21 | **21/21** |
| Orwell (why I write) | 19/21 | **21/21** |
| Gratitude (slop prompt) | 19/21 | **21/21** |
| Insect (slop prompt) | 20/21 | **21/21** |
| Passion (slop prompt) | 19/21 | **21/21** |
| End of life (slop prompt) | 20/21 | **21/21** |
| Dunbar (slop prompt) | 20/21 | **21/21** |

10/10 clean passes. The pre-check script finds the problems, the model fixes them, the post-check script confirms they're gone.

**Note:** These results were against the original 21-check grader. The grader has since been expanded to 31 checks (fixing 7 bugs in existing checks and adding 8 new checks). The original 10 samples need re-running against the updated grader to confirm they still pass. See [ISSUES.md](ISSUES.md) for details.

## Grading script

31 programmatic checks covering 38 patterns plus structural tells (forced synesthesia and generic metaphors still need human judgment):

```bash
python3 evals/grade.py path/to/text.md
python3 evals/grade.py path/to/text.md no-em-dashes,no-manufactured-insight
```

Outputs JSON with pass/fail and evidence per check.

## Self-tests

104-assertion test suite verifying each check catches known-bad text and passes known-clean text:

```bash
python3 evals/test_grade.py
```

Run this after any change to `grade.py` to prevent silent regex breakage. See [ISSUES.md](ISSUES.md) for technical gotchas (e.g. substring vs regex matching for multi-word phrases, cross-sentence pattern matching).

## Key findings

- **Pre-check/post-check loop is the breakthrough.** Without the script loop, models miss patterns they've been told to catch (Murray's "the reason is straightforward" slipped through in every run without the script). With the loop, 10/10 clean.
- **Experiential vacancy was the most useful conceptual addition.** Every agent used it as their primary diagnostic: "this essay contains no named people, no real places, no specific memories." That framing pushes toward replacement with something specific, not just removal of bad patterns.
- **Vague prohibition doesn't work on smart models.** Saying "no manufactured insight" wasn't enough. The model rationalised exceptions for humorous tone. Explicit examples and "non-negotiable even in casual writing" closed the loophole.
- **Claude doesn't produce the same slop as ChatGPT.** The sensory/atmospheric patterns (ghost language, quietness, synesthesia) rarely appeared in Claude output even with lazy prompts. The skill's new patterns are more relevant to ChatGPT-generated text.
- **Programmatic grading catches about 80% of tells.** 31 script checks cover 38 patterns. Forced synesthesia, generic metaphors, tonal uniformity, faux specificity, and neutrality collapse still need human judgment in the self-audit step.
