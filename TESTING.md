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

4. **Grade programmatically.** 16-check script (`evals/grade.py`) tests for em dashes, AI vocabulary clustering, manufactured insight, staccato sequences, anaphora, and 11 other patterns.

5. **Compare to originals.** Read the humanised output alongside the original human text to check voice, meaning, and plausibility.

6. **Fix failures and re-run.** When Wong's piece kept "And honestly?" because the agent thought it served the humour, we tightened the hard constraints and re-ran until it passed.

All final outputs passed 16/16 programmatic checks across all iterations.

## Grading script

```bash
# Grade a single file against all 16 checks
python3 evals/grade.py path/to/text.md

# Grade against specific checks only
python3 evals/grade.py path/to/text.md no-em-dashes,no-manufactured-insight
```

Outputs JSON with pass/fail and evidence per check.

## Key findings

- **Experiential vacancy was the most useful addition.** Every humaniser agent used it as their primary diagnostic: "this essay contains no named people, no real places, no specific memories." That framing pushes toward replacement with something specific, not just removal of bad patterns.
- **Vague prohibition doesn't work on smart models.** Saying "no manufactured insight" wasn't enough. The model rationalised exceptions. Saying "non-negotiable even in casual, humorous, or conversational writing" with explicit examples closed the loophole.
- **Claude doesn't produce the same slop as ChatGPT.** The sensory/atmospheric patterns (ghost language, quietness, synesthesia) rarely appeared in Claude output even with lazy prompts. The skill's new patterns are more relevant to ChatGPT-generated text.
- **Programmatic grading catches about 60% of tells.** The grading script tests lexical and structural patterns. Subtler issues (experiential vacancy, generic metaphors, emotional risk aversion) need human judgment.
