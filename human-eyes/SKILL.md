---
name: human-eyes
description: >-
  Audits prose for AI fingerprints and explains each one in plain English.
  Optionally hands back alternative phrasings for each flagged tell, redrafts
  the prose at a chosen intensity, or composes new prose from a brief while
  avoiding AI patterns. Use this skill for content writing, editing and review. Triggers on
  phrases like "audit this for AI", "human-eyes this", "unsloppify", "this
  reads like ChatGPT", "strip the AI tells", "rewrite to sound human", and
  "help me write something that doesn't sound AI".
---

# Human-eyes

The skill helps writers see what marks their prose as machine-flavoured by surfacing patterns and explaining them. Removing or replacing them is opt-in.

Three principles cut across the skill:

1. **The writer decides what to do.** The audit shows every flagged pattern with its location and a short explanation. There is no filter and no ranking. The writer reads the audit and chooses whether to act, and how.
2. **The writer chooses the depth when the skill generates new prose.** Audit and Suggestions return everything regardless of depth. Rewrite and Write run at a depth the writer picks (Balanced or All).
3. **Every interaction with text starts with an audit.** "Human-eyes this" reads as Audit alone, not Rewrite. Direct rewrite requests still audit first; the findings are part of the Rewrite output. The audit teaches the writer to spot the pattern; whatever happens after is the writer's call.

The skill does not score the draft or classify authorship. It does not modify the writer's source file. After an audit, it asks what the writer wants next.

---

## Action selection

Four actions:

| Action | When to fire | Output |
|---|---|---|
| **Audit** *(default)* | The writer hands the agent a draft and asks the skill to look at it, or hands over a draft with no action specified. Triggers: "audit this", "check this for AI", "does this sound AI", "human-eyes this", "what's flagged". | Every flagged pattern with its location in the prose and a short explanation. |
| **Suggestions** | The writer asks for replacements after seeing an audit. Triggers: "give me suggestions", "what should I change", "show me alternatives", "list the fixes". | One suggestion per flagged tell. |
| **Rewrite** | The writer asks for a redrafted version, or confirms a rewrite after an audit. Triggers: "rewrite this", "fix it", "clean it up", "strip the AI tells", "audit and rewrite at <depth>". | An audit followed by a rewrite at the chosen depth. |
| **Write** | The writer hands the agent a brief and no draft. Triggers: "write a 500-word post on X", "draft an opening paragraph about Y", "compose a blog post on Z without sounding AI". | A new draft at the chosen depth. |

If the writer's intent is genuinely ambiguous and the agent can ask, ask whether the writer wants an audit or a rewrite, or whether they're handing over a brief for a new draft. If the agent can't ask (headless invocation, no human turn), default to Audit only.

---

## Action 1: Audit (default)

### Audit steps

1. Save the input to a temp file: `INPUT_PATH=$(mktemp /tmp/human-eyes-input-XXXXXX.md)`. Write the draft to it.
2. **Run the agent-judgement reading and write it to a JSON file.** Read `human-eyes/scripts/judgement.json` for the canonical eight-item registry (seven semantic items plus one polymorphic genre slot) with their prompts and answer schemas. For each item, decide its `status` (`flagged` or `clear`) and the `answer` shape required by the item's `answer_schema`. The genre slot first detects the genre (academic, student_essay, poetry, fiction, or default), then runs the matching `sub_records[<genre>].watchlist` — currently empty for non-default genres, in which case `watchlist_findings` stays empty. These items cover what the regex grader cannot: structural monotony, tonal uniformity, faux specificity, neutrality collapse, even jargon distribution, forced synesthesia, generic metaphors, and the genre-specific watchlist.

   Write the eight items to a JSON file matching the contract's `agent_judgement` slot:

   ```bash
   JUDGEMENT_PATH=$(mktemp /tmp/human-eyes-judgement-XXXXXX.json)
   ```

   ```json
   {
     "agent_judgement": [
       {"id": "tonal_uniformity", "status": "flagged", "answer": "register holds without breaks", "evidence": {}},
       {"id": "faux_specificity", "status": "clear", "answer": [], "evidence": {}}
     ]
   }
   ```

   Per-item fields:
   - `id` — the registry id from `judgement.json` (e.g. `tonal_uniformity`, `genre_specific`).
   - `status` — `clear` or `flagged`, decided by the item's `flagged_when` rule.
   - `answer` — the value matching the item's `answer_schema.type`: a single string for `state` / `trichotomy`, a list of `{phrase, why_*}` objects for `list`, an object with `genre_detected` + `watchlist_findings` for `composite`.
   - `evidence` — an object; `{}` is fine when no extra evidence is captured.
   - `severity` — optional. Omit it and `grade.py` defaults to the registry's curated value. Override only when the writer's draft genuinely shifts the severity for that item.

3. Render the audit in a single deterministic call:

   ```bash
   python3 human-eyes/scripts/grade.py --format markdown --depth <balanced|all> --judgement-file "$JUDGEMENT_PATH" "$INPUT_PATH"
   ```

   The script merges the agent-judgement file into the contract before rendering, so this one call produces the full audit — summary lines, both flagged-items blocks, and the next-step prompt. **Print the script's output verbatim.** Do not paraphrase, summarise, normalise quotes, lower-case anything, or re-render any block. The script's quoted phrases are guaranteed to substring-match the input; rephrasing them breaks the audit's contract with the grader.
4. Stop without proceeding to a rewrite or coverage report unless asked.

The default audit emits the summary block + mini-headers + flagged items + next-step. When the writer asks for the full coverage report (per the next-step prompt), re-run with `--full-report` (keep the `--judgement-file` flag): the script keeps the same audit body and inserts brief notes + coverage tables under each mini-header. Both modes share the same audit body shape — full-report mode adds depth (brief notes + coverage tables and the full unbounded phrase list per flagged item).

If you also need the structured findings (e.g. for Suggestions or Rewrite drill-in), run `python3 grade.py --format json --judgement-file "$JUDGEMENT_PATH" "$INPUT_PATH"` separately. The pattern name in any rendered output is the human-readable `short_name` from `human-eyes/scripts/patterns.json` (e.g., "Em dashes", "Triad density") — never the internal check ID (`no-em-dashes`, `no-triad-density`).

### Audit output

The default audit shape (`grade.py --format markdown`):

```
**Audit summary**
Auto-detected: <auto_flagged> of <auto_total> flagged · Agent-assessed: <agent_flagged> of <agent_total> flagged
Severity: <hard_fail count> hard fail · <strong_warning count> strong warning · <context_warning count> context warning
Signal stacking: clear (...)   |   Signal stacking triggered: <score> of <threshold> threshold (<components>)

**Auto-detected**

<severity glyph> <pattern short_name>: "<quoted phrase>"
<severity glyph> <pattern short_name>

**Agent-assessed**

<severity glyph> <agent item label>: <state value>
<severity glyph> <agent item label>
  - "<phrase>": <why>
  - "<phrase>": <why>
<severity glyph> <genre slot label>: <genre> genre detected
  - "<phrase>": <why>

**Next steps**

Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?
```

Auto-detected flagged items appear under the `**Auto-detected**` mini-header; agent-assessed flagged items appear under `**Agent-assessed**`. Within each block, items render in severity-descending order (`x` first, then `!`, then `?`). Both blocks share the same `<glyph> <short_name>` opener (pattern names render unbold); the suffix shape varies per item type:

- Auto-detected lexical pattern: `<glyph> <name>: "<phrase>"` (caps at three phrases in default mode with `(+N more)` overflow; full-report mode renders all phrases).
- Auto-detected structural pattern: `<glyph> <name>` (no quoted phrase).
- Agent-assessed `state` / `trichotomy` flagged item: `<glyph> <label>: <state value>` (single line).
- Agent-assessed `list` flagged item: `<glyph> <label>` header followed by nested `  - "<phrase>": <why>` sub-bullets per finding.
- Agent-assessed `composite` (genre slot) flagged item: `<glyph> <label>: <genre> genre detected` header, then nested watchlist sub-bullets if any.

The `**Next steps**` heading and prompt are emitted by the script — print them verbatim. The audit format itself contains no em dashes — em dash overuse is one of the patterns the skill flags, so the audit itself avoids them.

The full-report shape (`grade.py --format markdown --full-report`) keeps the same audit body and adds a brief note + coverage tables under each mini-header, before the `**Next steps**` heading:

```
[default audit body: **Audit summary** + summary lines + **Auto-detected** + flagged items]

Checks the script runs against the text directly.

**<Category>**: <clear>/<total> clear

**<Category>**: <flagged> flagged of <total>

| Pattern | Severity | Result | Detail |
| --- | --- | --- | --- |
| <pattern short_name> | <severity> | <Flagged | Clear> | <guidance text when flagged, empty when clear> |
| ... | ... | ... | ... |

(eight category sub-tables in `human-eyes/references/patterns.md` heading order: Content patterns, Language and grammar, Style, Communication, Filler and hedging, Sensory and atmospheric, Structural tells, Voice and register. Categories where every check is clear collapse to a one-liner; categories with at least one flag render the full sub-table including the clear rows for coverage.)

**Agent-assessed**

[agent-assessed flagged items]

Checks that are judged by an LLM based on reading the whole draft.

| Pattern | Severity | Result | Detail |
| --- | --- | --- | --- |
| <Item label> | <severity> | <Flagged | Clear> | <(see above) when flagged, answer/value text when clear> |
| ... | ... | ... | ... |

(one flat eight-row table in `human-eyes/scripts/judgement.json` registry order. Flagged rows point back at the inline list via `(see above)` in Detail; clear rows carry the answer enum or genre detection in Detail.)

**Next steps**

Want suggestions for edits, a full rewrite, or to save this audit as a file?
```

In full-report mode the next-step prompt drops the "full coverage report" option, since the writer has just read it.

A zero-flag draft renders the same shape — the summary block carries all-zero counts, the mini-headers still appear with no items beneath them, and the per-block coverage tables (in full-report mode) show every category collapsed to clear / every agent row clear. There's no all-clear single-line shortcut.

### Rendering rules

- **Severity glyphs** in flagged-item blocks (both auto-detected and agent-assessed): `x` for hard_fail, `!` for strong_warning, `?` for context_warning. No glyphs in coverage tables.
- **Pattern names** are the human-readable `short_name` from `human-eyes/scripts/patterns.json` (e.g., "Em dashes", "Triad density", "Assistant residue"). Pattern names render unbold in flagged-item blocks (the only bold elements in the audit body are the headings: `**Audit summary**`, `**Auto-detected**`, `**Agent-assessed**`, `**Next steps**`). Never use the internal check ID (`no-em-dashes`, `no-triad-density`); check IDs are assertion names, not user-facing labels. Agent-judgement labels are computed mechanically from the registry id (`structural_monotony` → "Structural monotony").
- **Lexical patterns** carry a quoted phrase in their flagged-item block: `<glyph> <name>: "<phrase>"`. The phrase list caps at three with a `(+N more)` overflow suffix in default mode; full-report mode renders every captured phrase.
- **Structural patterns** (paragraph-length uniformity, anaphoric scaffolding, section scaffolding, sentence-length variance) carry no quoted phrase — they render as `<glyph> <name>`. The pattern's "where" lives in the grader's evidence object, not in the rendered prose.
- **Category collapse** in full-report-mode coverage tables: a category with every check clear renders as one line — `**<Category>**: <N>/<N> clear`. A category with at least one flagged check renders the full sub-table including the clear rows so coverage stays visible.
- **Agent-assessed coverage** is one flat eight-row table in full-report mode (no per-category grouping). Detail column carries `(see above)` for flagged rows (points at the inline bullet block) and the answer/value text for clear rows.
- **Signal stacking** is suppressed from flagged-item blocks and coverage tables — its signal lives in the third summary line. The summary-line severity counts aggregate auto-detected + agent-assessed flagged severities; the signal-stacking meta-check itself never inflates them.
- **No "Why this matters" or "What it looks for" prose** in the audit output. Per-pattern explanations live in `human-eyes/references/patterns.md` and are read on drill-in for Suggestions or Rewrite — not in the audit itself.
- Keep explanations concrete and avoid jargon. The point is to teach the writer how to recognise the pattern rather than display the catalogue.

If the grader is unavailable (no Python, restricted environment), fall back to a manual scan reading `human-eyes/references/patterns.md` and run the agent-judgement reading directly from `human-eyes/scripts/judgement.json`. Disclose the limitation: a manual scan covers surface patterns and cannot replicate the script's structural and density checks.

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

When the user has not chosen a depth, ask which depth they want. Phrase the question to match how the writer usually decides — they want to know what each depth does to the prose, not which label means what:

> Would you like a balanced rewrite that reduces the most distinctive AI patterns while preserving voice, or a full rewrite that removes every flagged pattern? Note: even human text can fail some checks and still read naturally, so Balanced is usually the right call unless you specifically want maximum pattern removal.

Default to Balanced if the writer declines to choose.

The dial only governs Rewrite and Write. It does not apply to Audit or Suggestions. Both of those return the full list of flagged tells regardless.

---

## Action 3: Rewrite

### Rewrite steps

1. Run the audit (as in Action 1) regardless of whether the writer asked directly. The audit findings are part of the Rewrite output, and the writer benefits from seeing what was flagged before reading the rewrite.
2. Pick the depth: ask if you can; default to Balanced. See the depth dial section above.
3. Read `references/voice.md` for voice-craft guidance. LLM rewrites flatten stance and deplete pronouns; neutrality creeps in even on grammar-only passes. Voice-preservation is required during the rewrite.
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
- Score: how many of the grader's checks failed at the chosen depth, plus whether signal stacking triggered or stayed clear.
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

- Same directory as the input file, with the input's stem plus `.human-eyes-audit.md`, `.human-eyes-suggestions.md`, `.human-eyes-rewrite.md`, or `.human-eyes-write.md`.
- Fallback: `./human-eyes-<action>.md` when there is no input path (e.g., pasted text).
- Append `-2`, `-3` rather than overwriting an existing file.

When Save is used:

- The chat output is a one-line summary of the action's verdict, followed by `Saved to: <path>`, followed by the next-step question if one applies.
- The saved file contains the action's full output template, preceded by a short header:

```
# Human-eyes <action> report
- Input: <input path, or "pasted text", or "brief">
- Depth: <Balanced / All, or "n/a" for Audit and Suggestions>
- Date: <ISO 8601>
```

Do not duplicate the full report inline in chat when a saved file exists.

---

## References

- `references/patterns.md`: full catalogue of detected patterns with words to watch and before/after examples. Includes the four most distinctive AI tells (em dashes, manufactured insight, contrived reframes, generic staccato) with their deeper rules and word lists.
- `references/voice.md`: voice-craft for Rewrite and Write. The subtraction problem: LLM rewrites flatten stance and deplete pronouns; neutrality creeps in even on grammar-only passes. Read during the rewrite or draft step.
- `references/alternatives.md`: vetted human alternatives for lexical patterns, used by Suggestions and by Rewrite or Write when picking replacements.
- `references/process.md`: required operating procedure for Rewrite and Write. Steps A through E cover structural changes, surface cleanup, structural self-check, semantic preservation, and re-grade revision loops.
