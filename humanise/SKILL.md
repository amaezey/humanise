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
3. Parse the grader output. For each detected pattern, extract these fields: the pattern name; the offending phrase or sentence quoted from the input; the severity; and the relevant explanation from `references/patterns.md`. The pattern name is the human-readable heading from `references/patterns.md` (e.g., "Em dashes", "Triad density", "Curly quotes") — never the internal check ID (`no-em-dashes`, `no_triad_density`, etc.). Check IDs are assertion names, not user-facing labels.
4. **Run the agent-judgement reading.** Read `judgement.yaml` for the canonical eight-item registry (seven semantic items plus one polymorphic genre slot) with their prompts and answer schemas. For each item, decide its status (`flagged` or `clear`) and capture per-item evidence following the item's `answer_schema`. The genre slot first detects the genre (academic, student_essay, poetry, fiction, or default), then runs the matching `sub_records[<genre>].watchlist` — currently empty for non-default genres, in which case record `Watchlist coverage pending.` These items cover what the regex grader cannot: structural monotony, tonal uniformity, faux specificity, neutrality collapse, even jargon distribution, forced synesthesia, generic metaphors, and the genre-specific watchlist.
5. Render the audit using the output template below. The programmatic block carries the regex findings as a two-layer surface (Layer 1 orientation + Layer 2 coverage receipt); the agent-judgement block carries the eight-item reading as a parallel block. The renderer collapses to a single line when both halves are clear and aggregate AI-pressure has not triggered.
6. End with the next-step question and stop without proceeding to a rewrite.

### Audit output

The renderer (`humanise/grade.py format_two_layer`) emits one of three shapes depending on what fired. The all-clear case collapses to a single line; everything else composes a programmatic block, an agent-judgement block, or both — separated by `---`.

```
Audit
Severity: <hard_fail count> hard_fail · <strong_warning count> strong_warning · <context_warning count> context_warning · pressure: <triggered | clear>
<one-sentence pressure explanation: triggered or clear, score vs threshold, components and vocabulary points>

<severity glyph> **<pattern short_name>** — "<quoted phrase>" — Action: <Fix | Disclose or ask before preserving>
<severity glyph> **<pattern short_name>** — Action: <action>
...

---

**<Category>** — <clear>/<total> clear

**<Category>** — <flagged> flagged of <total>

| Pattern | Result | Action |
| --- | --- | --- |
| <pattern short_name> | <Flagged | Clear> | <action when flagged, empty when clear> |
| ... | ... | ... |

(eight category sub-tables in `humanise/references/patterns.md` heading order: Content patterns, Language and grammar, Style, Communication, Filler and hedging, Sensory and atmospheric, Structural tells, Voice and register. Categories where every check is clear collapse to a one-liner; categories with at least one flag render the full sub-table including the clear rows for coverage.)

---

**Agent-judgement reading — <flagged> flagged of <total>**

- <Item label> — <Status>: <state or trichotomy value>
- <Item label> — Flagged:
  - "<phrase>" — <why>
- <Item label> — Clear
- Genre specific — <Status>: Genre detected: <genre>.
  - "<phrase>" — <why>

**Next step**

Want Suggestions for per-flag replacements, a Rewrite at a chosen depth, or to save this audit as a Markdown file?
```

If every programmatic check is clear AND every agent-judgement item is clear AND aggregate AI-pressure has not triggered, the renderer collapses everything to a single line:

```
<N> of <N> clear · agent reading clean · pressure: clear.
Next: re-run with --depth all to inspect lower-tier signals.
```

If only one half has anything to surface, the renderer omits the empty side. Programmatic flagged + agent fully clear renders the programmatic block plus a clean-form agent block (`**Agent-judgement reading**` header followed by `agent reading clean`). Programmatic fully clear but agent flagged renders the agent block alone, with no Layer 1 / Layer 2 above it. The `---` separator only appears between blocks that actually render.

### Rendering rules

- **Severity glyphs** in Layer 1's per-flagged-pattern blocks: `x` for hard_fail, `!` for strong_warning, `?` for context_warning. No glyphs in Layer 2 sub-tables or in the agent-judgement block.
- **Pattern names** are the human-readable `short_name` from `humanise/patterns.yaml` (e.g., "Em dashes", "Triad density", "Assistant residue") — never the internal check ID (`no-em-dashes`, `no-triad-density`). Check IDs are assertion names, not user-facing labels. Agent-judgement labels are computed mechanically from the registry id (`structural_monotony` → "Structural monotony").
- **Lexical patterns** (specific words or phrases) carry a quoted phrase in their Layer 1 block: `<glyph> **<name>** — "<phrase>" — Action: ...`. The Layer 1 phrase list caps at three with a `(+N more)` overflow suffix when more phrases are present.
- **Structural patterns** (paragraph-length uniformity, anaphoric scaffolding, section scaffolding, sentence-length variance) carry no quoted phrase — they render as `<glyph> **<name>** — Action: ...` in Layer 1. The pattern's "where" lives in the grader's evidence object, not in the rendered prose.
- **Category collapse**: a Layer 2 category with every check clear renders as one line — `**<Category>** — <N>/<N> clear`. A category with at least one flagged check renders the full Pattern/Result/Action sub-table including the clear rows so coverage stays visible.
- **Agent-judgement per-type rendering**:
    - `state` / `trichotomy` items render as `- <label> — <Status>: <value>` (clear or flagged carries the same shape; the value is one human-readable phrase from the schema).
    - `list` flagged items render as `- <label> — Flagged:` followed by nested `  - "<phrase>" — <why>` bullets. List items with no entries render as `- <label> — Clear`.
    - `composite` (the genre slot only) always shows the detected genre. When the registered watchlist for that genre is empty, the rendering ends with `Watchlist coverage pending.` regardless of status.
- **Aggregate AI-signal pressure** is suppressed from Layer 1 and Layer 2 — its signal lives in the verdict line's `pressure: <triggered | clear>` token. The verdict-line severity counts read from visible programmatic checks only; agent-judgement findings cannot inflate them.
- **No "Why this matters" or "What it looks for" prose** in the audit output. Per-pattern explanations live in `humanise/references/patterns.md` and are read on drill-in for Suggestions or Rewrite — not in the audit itself.
- Keep explanations concrete and avoid jargon. The point is to teach the writer how to recognise the pattern rather than display the catalogue.

If the grader is unavailable (no Python, restricted environment), fall back to a manual scan reading `humanise/references/patterns.md` and run the agent-judgement reading directly from `humanise/judgement.yaml`. Disclose the limitation: a manual scan covers surface patterns and cannot replicate the script's structural and density checks.

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

Want to apply these yourself, ask for a Rewrite at a chosen depth, or save this list of suggestions as a Markdown file?
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
4. Read `references/process.md`; it is required for Rewrite and Write. Address structural patterns first (Step A), then surface patterns (Step B).
5. Run the structural self-check (Step C from `process.md`). Show the answers in the output.
6. Run the semantic preservation check (Step D from `process.md`).
7. Re-grade the rewrite at the chosen depth. If required failures remain for that depth, revise before returning unless removing the issue would materially change meaning or voice. Iterate up to two re-runs and then report unresolved issues. Do not loop indefinitely.
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
3. Read `references/process.md`; it is required for Rewrite and Write. Apply the structural patterns (Step A) prospectively while drafting. Vary paragraph structures and take a stance. Avoid the default section arc.
4. Draft from the brief at the chosen depth.
5. Run the structural self-check (Step C from `process.md`) on the draft.
6. Re-grade the draft at the chosen depth. If required failures remain for that depth, revise before returning unless fixing them would materially change the brief or voice. Iterate up to two re-runs, then report unresolved issues.
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
- `references/process.md`: required operating procedure for Rewrite and Write. Steps A through E cover structural changes, surface cleanup, structural self-check, semantic preservation, and re-grade revision loops.
