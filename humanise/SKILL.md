---
name: humanise
description: >-
  Audits prose for AI fingerprints and explains each one in plain English.
  Optionally hands back alternative phrasings for each flagged tell, redrafts
  the prose at a chosen intensity, or composes new prose from a brief while
  avoiding AI patterns. Use this skill for content writing, editing and review. Triggers on
  phrases like "audit this for AI", "humanise this", "unsloppify", "this
  reads like ChatGPT", "strip the AI tells", "rewrite to sound human", and
  "help me write something that doesn't sound AI".
---

# Humanise

The skill helps writers see what marks their prose as machine-flavoured by surfacing patterns and explaining them. Removing or replacing them is opt-in.

Three principles cut across the skill:

1. **The writer decides what to do.** The audit shows every flagged pattern with its location and a short explanation. There is no filter and no ranking. The writer reads the audit and chooses whether to act, and how.
2. **The writer chooses the depth when the skill generates new prose.** Audit and Suggestions return everything regardless of depth. Rewrite and Write run at a depth the writer picks (Balanced or All).
3. **Every interaction with text starts with an audit.** "Humanise this" reads as Audit alone, not Rewrite. Direct rewrite requests still audit first; the findings are part of the Rewrite output. The audit teaches the writer to spot the pattern; whatever happens after is the writer's call.

The skill does not score the draft or classify authorship. It does not modify the writer's source file. After an audit, it asks what the writer wants next.

---

## Action selection

Four actions:

| Action | When to fire | Output |
|---|---|---|
| **Audit** *(default)* | The writer hands the agent a draft and asks the skill to look at it, or hands over a draft with no action specified. Triggers: "audit this", "check this for AI", "does this sound AI", "humanise this", "what's flagged". | Every flagged pattern with its location in the prose and a short explanation. |
| **Suggestions** | The writer asks for replacements after seeing an audit. Triggers: "give me suggestions", "what should I change", "show me alternatives", "list the fixes". | One suggestion per flagged tell. |
| **Rewrite** | The writer asks for a redrafted version, or confirms a rewrite after an audit. Triggers: "rewrite this", "fix it", "clean it up", "strip the AI tells", "audit and rewrite at <depth>". | An audit followed by a rewrite at the chosen depth. |
| **Write** | The writer hands the agent a brief and no draft. Triggers: "write a 500-word post on X", "draft an opening paragraph about Y", "compose a blog post on Z without sounding AI". | A new draft at the chosen depth. |

If the writer's intent is genuinely ambiguous and the agent can ask, ask whether the writer wants an audit or a rewrite, or whether they're handing over a brief for a new draft. If the agent can't ask (headless invocation, no human turn), default to Audit only.

---

## Action 1: Audit (default)

### Audit steps

1. Save the input to a temp file: `INPUT_PATH=$(mktemp /tmp/humanise-input-XXXXXX.md)`. Write the draft to it.
2. Run the grader: `python3 grade.py --format json "$INPUT_PATH"`.
3. Parse the grader output. For each detected pattern, extract these fields: the pattern name; the offending phrase or sentence quoted from the input; the severity; and the relevant explanation from `references/patterns.md`.
4. Render the audit using the output template below.
5. End with the next-step question and stop without proceeding to a rewrite.

### Audit output

```
**Audit, N AI tells found**

<pattern-name-1> (M instances)
  - "<quoted phrase from input>"
  - "<another quoted phrase>"
  Why: <brief explanation, ~1-2 sentences>

<pattern-name-2> (M instances)
  - "<quoted phrase>"
  Why: <explanation>

<structural-pattern-name>
  Where: <description of where the pattern appears, e.g., "every paragraph in section 2 is 4-5 sentences and ends with a summary line">
  Why: <explanation>

...

**Confidence**

Render four fields from the grader: the level (low / medium / high / very high), the meaning string explaining what the level implies, the basis list summarising why, and a note that this assessment describes AI-writing signs rather than offering a verdict about who wrote the text.

**Next step**

Pick one: Suggestions for per-flag replacements, Rewrite at a chosen depth, or save this audit as a Markdown file.
```

### Rendering rules

- Lexical patterns (specific words or phrases) get the `- "<quoted>"` shape.
- Structural patterns (paragraph-length uniformity, anaphoric scaffolding, section scaffolding, sentence-length variance) get a `Where:` line that describes where the pattern shows up and what it looks like in the draft. They have no single quotable instance to point at.
- Keep explanations concrete and avoid jargon. The point is to teach the writer how to recognise the pattern rather than display the catalogue.

If no patterns are detected, say so plainly:

> Audit clean: no AI tells detected. Point me at a specific aspect of the draft if you want a closer look.

If the grader is unavailable (no Python, restricted environment), fall back to a manual scan reading `references/patterns.md`. Disclose the limitation: a manual scan covers surface patterns and cannot replicate the script's structural and density checks.

---

## Action 2: Suggestions

### Suggestion steps

1. If an audit hasn't been run on this draft in this turn, run one first.
2. For each flagged pattern from the audit, produce one suggestion:
   - Lexical patterns (`delve`, hedging phrases, formulaic depth phrases, em dashes, AI vocabulary words): pull from `references/alternatives.md`. Pick the alternative that fits the surrounding sentence.
   - Structural patterns (paragraph-length uniformity, anaphoric scaffolding, sentence-length variance, tonal uniformity): compose a contextual suggestion. Substitution does not work for these patterns; rewriting does. Say what to vary and how.
3. Render the audit findings followed by the suggestions list.
4. Stop without producing a full rewrite.

### Suggestion output

```
[Audit output as in Action 1, but without the trailing question]

**Suggestions, one per flag**

<pattern-name-1>
  - "<quoted phrase from the audit>"
  Try: "<replacement>"

<pattern-name-2>
  - "<another quoted phrase>"
  Try: "<replacement>"

<structural-pattern>
  Try: <contextual rewriting instruction, e.g., "Vary paragraph 3 to be one short sentence, then expand paragraph 4 with two new clauses to break the rhythm.">

...

**Next step**

Pick one: apply these yourself, ask for a Rewrite at a chosen depth, or save this list of suggestions as a Markdown file.
```

The number of suggestions equals the number of flagged tells, with no filtering applied. The writer chooses what to apply.

---

## The depth dial (Rewrite and Write only)

Two settings:

- **Balanced** *(default)*: address surface-level and strong AI tells — lexical tells (such as `delve` and em dashes), formulaic openers, manufactured-insight framing, signposted conclusions, AI vocabulary clustering, contrived contrast, and soft scaffold phrasing. Most context warnings can be preserved if they are doing real work. Structural patterns like paragraph-length uniformity may remain.
- **All**: address every flagged pattern, even the implicit and structural ones a reader wouldn't consciously notice. Voice can take a hit at this depth. The goal is unambiguous human-shape; preserving every flourish comes second.

When the user has not chosen a depth, ask which depth they want. Balanced is the lighter pass; All is the deeper one. Default to Balanced if the writer declines to choose.

The dial only governs Rewrite and Write. It does not apply to Audit or Suggestions. Both of those return the full list of flagged tells regardless.

---

## Action 3: Rewrite

### Rewrite steps

1. Run the audit (as in Action 1) regardless of whether the writer asked directly. The audit findings are part of the Rewrite output, and the writer benefits from seeing what was flagged before reading the rewrite.
2. Pick the depth: ask if you can; default to Balanced. See the depth dial section above.
3. Read `references/voice.md` for voice-craft guidance. Recent research (Abdulhai et al., 2026) showed that LLM rewrites flatten stance and deplete pronouns; neutrality creeps in even on grammar-only passes. Voice-preservation is required during the rewrite.
4. Read `references/process.md` for the process steps used by Rewrite and Write. Address structural patterns first (Step A), then surface patterns (Step B).
5. Run the structural self-check (Step C from `process.md`). Show the answers in the output.
6. Run the semantic preservation check (Step D from `process.md`).
7. Re-grade the rewrite at the chosen depth. If at All depth and failures remain, iterate up to two re-runs and then report unresolved issues. Do not loop indefinitely.
8. Render the audit findings, the rewritten draft, and the post-check.

### Rewrite output

```
[Audit output as in Action 1, but without the trailing question]

**Depth: <Balanced / All>**
Why: <one sentence on why this depth fits the genre or the writer's stated preference>

**Rewrite**

<rewritten draft>

**Structural self-check**
1. Section arcs: <count of similar arcs>/<total>. <What you changed.>
2. Resolution density: <count of summary endings>/<total>. <What you changed.>
3. Register breaks: <where you added one, or "already present at...">
4. Triads: <count> found, reduced to <count> by <method>.
5. Reframe laundering: <none / fixed at...>
6. Purposeful devices preserved: <device: reason, or "none">
7. Stance: <preserved / shifted, restored by...>
8. Remaining tells: <list, or "none identified">

**Post-check at <depth>**
- Score: how many of the grader's checks failed at the chosen depth, plus whether AI-pressure triggered or stayed clear.
- Confidence: the level and meaning string from the grader, with the caveat that this describes AI-writing signs rather than offering an authorship verdict.
- Remaining issues: list the failed checks that remain unaddressed, or state "none" if the rewrite cleared everything.
```

Show only the final rewrite. Intermediate drafts stay hidden unless the writer asks. Do not modify the writer's source file.

---

## Action 4: Write

### Drafting steps

1. Pick the depth: ask if you can; default to Balanced.
2. Read `references/voice.md`. Write produces new prose, so voice-craft is load-bearing. There is no input voice to preserve; the writer fills an absence.
3. Read `references/process.md`. Apply the structural patterns (Step A) prospectively while drafting. Vary paragraph structures and take a stance. Avoid the default section arc.
4. Draft from the brief at the chosen depth.
5. Run the structural self-check (Step C from `process.md`) on the draft.
6. Re-grade the draft at the chosen depth. Iterate up to two re-runs at All depth if failures remain, then report unresolved issues.
7. Render the draft and the post-check.

### Drafting output

```
**Brief: <one-sentence restatement of what the writer asked for>**

**Depth: <Balanced / All>**
Why: <one sentence on why this depth fits the brief>

**Draft**

<drafted text>

**Structural self-check**
[Same eight items as Rewrite]

**Post-check at <depth>**
[Same shape as Rewrite post-check]
```

Write has no audit step because there is no input text to audit. The skill avoids AI patterns prospectively and verifies via the post-check.

---

## The save modifier

Save wraps any of the four actions' output in a Markdown file. Combine freely with any action.

Default save paths:

- Same directory as the input file, with the input's stem plus `.humanise-audit.md`, `.humanise-suggestions.md`, `.humanise-rewrite.md`, or `.humanise-write.md`.
- Fallback: `./humanise-<action>.md` when there is no input path (e.g., pasted text).
- Append `-2`, `-3` rather than overwriting an existing file.

When Save is used:

- The chat output is a one-line summary of the action's verdict, followed by `Saved to: <path>`, followed by the next-step question if one applies.
- The saved file contains the action's full output template, preceded by a short header:

```
# Humanise <action> report
- Input: <input path, or "pasted text", or "brief">
- Depth: <Balanced / All, or "n/a" for Audit and Suggestions>
- Date: <ISO 8601>
```

Do not duplicate the full report inline in chat when a saved file exists.

---

## References

- `references/patterns.md`: full catalogue of detected patterns with words to watch and before/after examples. Includes the four most distinctive AI tells (em dashes, manufactured insight, contrived reframes, generic staccato) with their deeper rules and word lists.
- `references/voice.md`: voice-craft for Rewrite and Write. The subtraction problem (Abdulhai et al., 2026): LLM rewrites flatten stance and deplete pronouns; neutrality creeps in even on grammar-only passes. Read during the rewrite or draft step.
- `references/alternatives.md`: vetted human alternatives for lexical patterns, used by Suggestions and by Rewrite or Write when picking replacements.
- `references/process.md`: Steps A through D for Rewrite and Write. Address structural patterns, address surface patterns, structural self-check, semantic preservation check.
