# Humanise: skill refocus plan

> **Superseded by [`dev/plans/2026-04-28-humanise-implementation.md`](2026-04-28-humanise-implementation.md).** This plan is the earlier exploratory pass; the implementation plan is the canonical record of executed and remaining work. Decisions in this file (3-mode depth dial, "Light" intensity, open identity placeholders) have been resolved or revised in the implementation plan — read that plan first.

The current SKILL.md is patchwork. Iterative cleanup hasn't fixed the foundational confusion. This plan steps back to first principles, then proposes a clean structure.

---

## Part 1 — Intent

### What this skill is

A Claude Code skill that helps writers reduce the patterns that make text sound AI-generated. It does three things on demand:

- **Audit** an existing draft and explain what's flagged.
- **Rewrite** an existing draft to remove flagged patterns at a chosen intensity.
- **Write** new content from a brief while avoiding flagged patterns.

The detection layer is a Python script (`grade.py`) running 43 programmatic checks. The action layer is the agent following SKILL.md.

### Who it's for

Writers who use Claude (or another LLM) as a drafting aid and want to know what's machine-flavoured before they ship. Three concrete user shapes:

1. **Writer with a touched-up draft.** They wrote it, fed it to AI for a polish, now they're not sure what's still theirs. They want an audit.
2. **Writer with AI-generated content.** They asked AI to write something, want to remove the tells before publishing. They want a rewrite.
3. **Writer drafting from scratch.** They want help composing without the patterns. They want write.

All three share a need: see what AI tells look like in their actual text, decide what to do.

### What it deliberately doesn't do

- **It does not make writing "good".** Hard mode = no detectable AI signals. That is not the same as voice, structure, depth, or interesting prose. A draft can pass every check and still be sterile.
- **It does not issue authorship verdicts.** It surfaces patterns; the writer interprets.
- **It does not auto-rewrite.** Audit is the default action. Rewriting and writing only fire when the user asks. This is by design — most users want to see indicators before approving changes.
- **It does not enforce judgement on context warnings.** Some flagged patterns are legitimate when used with intent (literary staccato, voiced triads, rhetorical questions in interviews). The skill flags them; the writer decides.

### Why it exists in the world

There are two existing tool categories: AI detectors (GPTZero etc., score-based, no rewriting) and AI rewriters (QuillBot, Undetectable.ai, designed to evade detection). This skill sits between them: detection-first, rewriting optional, transparent about what it found and why. It is not optimised for evasion; it's optimised for the writer to understand.

---

## Part 2 — Architecture

### Components

```
humanise/
├── SKILL.md                          The operating contract (~200 lines target)
├── grade.py                          43 checks, severity-classified, plain-English report
├── references/
│   ├── patterns.md                   38-pattern catalogue (words, examples)
│   ├── severity-detail.md            Deep-dive on 4 most distinctive AI tells
│   ├── voice.md                      Voice-craft guidance for Rewrite/Write
│   └── example.md                    Worked rewrite end-to-end
└── (links to dev/evals/* for testing, blind eval harness)
```

### Numbers and what they mean

- **43 programmatic checks** in `grade.py`. Each one is a function in `ALL_CHECKS` with metadata (severity, what to look for) in `CHECK_METADATA`. This is the canonical count for "what the skill detects".
- **38 patterns** in `references/patterns.md`. The catalogue version of the checks, organised by category (content, language, style, communication, filler, sensory, structural, voice). 5 of the 43 checks (the statistical ones — `overall-ai-signal-pressure`, `paragraph-length-uniformity`, `vocabulary-diversity`, `sentence-length-variance`, plus one more) don't have catalogue entries because they're aggregation/density checks not lexical patterns.
- **3 severity classes** (in `CHECK_METADATA`): `hard_fail` (3 checks), `strong_warning` (14), `context_warning` (26). **There is no fourth class.** The doc has been inventing "hard constraint" as if it were a fourth class — it is not.

### Severity → action by mode

This is the critical mapping. Severity is intrinsic to the pattern; mode is the user's chosen intensity.

| Severity         | Light                          | Balanced (default)              | All                              |
|------------------|--------------------------------|---------------------------------|----------------------------------|
| Hard fail (×3)   | Fix                            | Fix                             | Fix                              |
| Strong warning (×14) | Fix (disclose if preserved) | Fix (disclose if preserved)    | Fix                              |
| Context warning (×26) | Preserve if purposeful (disclose) | Fix unless purposeful | Fix                              |

That table is the entire intensity logic. Everything else (genre rules, voice considerations) is guidance on top.

### What the agent reads

When `/humanise` fires, the agent loads `SKILL.md`. SKILL.md contains the operating contract — three actions, intensity rules, severity logic, output shape. It points to `references/` for catalogues and detail. The agent only reads references when the action calls for it (e.g. read `voice.md` during Rewrite/Write Step 5).

---

## Part 3 — Workflow

### Action 1: Audit (default)

Triggered by any input where the user is asking the skill to look at text without an explicit rewrite/write instruction.

1. Save input to a unique temp file (`mktemp`).
2. Run `grade.py` and render the user-facing report.
3. Ask: rewrite this, save the report, or done?
4. Stop unless the user picks rewrite.

The audit is mode-agnostic. The 43 checks pass or fail based on the text, not the user's intensity choice.

### Action 2: Rewrite

Triggered by an explicit rewrite instruction (rewrite, fix, clean up, de-AI, strip tells, humanise as a verb on text), or by the user picking rewrite after an audit.

1. Run audit (skip if just done in the same turn).
2. Ask intensity if not specified. Default to balanced.
3. Rewrite, addressing structural patterns first, then surface patterns. Read `references/voice.md` for voice-preservation logic. Read `references/severity-detail.md` for the four most-detailed patterns.
4. Run structural self-check (8 questions).
5. Run semantic preservation check (compare stance pre/post).
6. Run post-check by re-grading the rewrite at the chosen intensity.
7. Iterate up to 2 re-runs if intensity is "all" and failures remain. Report unresolved issues rather than looping.
8. Report before/after.

### Action 3: Write

Triggered by an explicit composition request (write, draft, compose, "help me write…").

1. Ask intensity if not specified. Default to balanced.
2. Read `references/voice.md` to avoid the most common AI subtraction failures (no opinions, no register breaks, faux specificity).
3. Draft, addressing patterns prospectively at the chosen intensity.
4. Run structural self-check on the draft.
5. Run post-check by grading the draft.
6. Iterate up to 2 re-runs if intensity is "all".
7. Report.

### Modifiers

- **Recommendation** — after an audit, optionally state a one-sentence intensity suggestion tied to the genre.
- **Save** — wrap any action's output in a Markdown file at `<input-stem>.humanise-<action>.md` next to the input, or `./humanise-<action>.md` if no input file. Append `-2`, `-3` rather than overwriting.

### What the agent should NOT do

- Pre-classify mode before the audit.
- Rewrite or compose without explicit user direction.
- Issue authorship verdicts.
- Treat the audit's recommended-action column as commitments — they're guidance.
- Loop the post-check indefinitely.
- Hide context-warning preservation decisions; always disclose.

---

## Part 4 — SKILL.md structure (target ~200 lines)

```
1. Frontmatter (~8 lines)
   - name: humanise
   - description: one paragraph, three actions, no citations

2. # Humanise + What this skill is (~25 lines)
   - Identity statement (the prose at the bottom of this plan)
   - The hard-mode caveat (intensity ≠ quality)
   - What this skill doesn't do

3. ## Three actions (~50 lines)
   - Audit (default): when, what to do, output shape
   - Rewrite: when, steps, output shape
   - Write: when, steps, output shape
   - Modifiers: recommendation, save (one paragraph each)

4. ## Intensity (~20 lines)
   - Light / Balanced / All, in user-facing language
   - One-line genre suggestions per intensity (not exhaustive)
   - Hard-mode caveat repeated here for emphasis
   - Default: balanced

5. ## Severity (~25 lines)
   - 3 classes (hard fail, strong warning, context warning)
   - The 3×3 table mapping severity to action by mode
   - One-line definition of each class
   - Pointer to references/severity-detail.md for the 4 most distinctive patterns

6. ## Output (~50 lines)
   - Audit template (compact, severity column, recommended-action column)
   - Rewrite template (audit + rewrite + self-check + post-check)
   - Write template (draft + self-check + post-check)
   - Save modifier wrapper

7. ## References (~10 lines)
   - patterns.md — 38-pattern catalogue
   - severity-detail.md — 4 deep-dive patterns
   - voice.md — voice-craft guidance
   - example.md — worked rewrite

8. ## Sources (~12 lines)
   - The Wikipedia, Abdulhai, Kobak etc. citations live here, not in the body
```

### What gets deleted from the current SKILL.md

- **Process section** (currently ~165 lines, lines 191–355). Actions section already covers the workflow. Two parallel structures explaining the same thing.
- **Pattern catalogue section** (currently ~20 lines, lines 171–189). The catalogue lives in `references/patterns.md`. SKILL.md just points to it.
- **"Hard constraints (deep-dive)" pointer section** — folds into severity-detail.md reference, which is already done.
- **"Personality and soul" pointer section** — reclaim this title for the identity statement at the top. Voice content stays in voice.md.
- **All trigger lists** ("Use this when the user asks…"). Replaced with a one-line action description.
- **Worked example pointer**. Folds into the references list.
- **Em-dash special-case prose**. Em dashes are a strong warning. Treated like the other 13 strong warnings.
- **All "no mode pre-classification" / "the audit is mode-agnostic" defensive language.**
- **Genre→mode mapping rules.** Reduced to one-line suggestions per intensity.
- **Author-name examples** (Poe, Sedaris). Replaced with genre/principle descriptions.

### What stays

- The 3-severity / 3-mode mapping table — promoted to a primary structure.
- The structural self-check (8 questions) — kept inline because the agent needs it during Rewrite/Write.
- The semantic preservation check — kept inline for Rewrite.
- Output templates — three of them, tight.

---

## Part 5 — The identity statement

Mae's edited version of the opening paragraphs (work in progress, includes open questions in brackets):

> AI-generated text has detectable patterns. After someone uses an LLM to draft, or expand a piece of writing, the prose picks up traces: vocabulary clusters, structural rhythms, formatting tics, voice flattening. These mark the text as machine-touched even when the writer can't see them.
>
> Humanise [what it does] so that humans can identify and remove signs of AI writing. Each of the 43 checks [and what about guidance that isn't programmatic?] in published research; sources in references/evidence.md.

Open questions Mae flagged:

1. **What does Humanise do?** — paragraph 2 has a `[what it does]` placeholder. The verb is the thing.
2. **What about non-programmatic guidance?** — the 43 checks are programmatic. The skill also includes structural self-check questions, semantic preservation checks, and voice-craft guidance that the agent applies, not the script. The identity statement should account for both.

The original draft and the iterated revisions are in the conversation history. Subsequent paragraphs (use case, three actions, detection layer / action layer split, "not for" disclaimers) need to be rewritten — Mae's note: "framed around my critique of your shallow analysis and not the actual identity of the skill". A fresh start is required, not further iteration on the existing prose.

---

## Part 6 — Outstanding decisions before drafting the new SKILL.md

These need user input before I write the new file.

1. **Intensity names.** I've been using "Light / Medium / Hard". Mae suggested user-facing terms in her last feedback ("light touch / balanced / absolutely all"). The plan uses "Light / Balanced / All" but the names are negotiable. Pick.
2. **The grader's `--mode` flag.** Currently the script accepts `--mode light|medium|hard`. The new framing makes intensity a Rewrite/Write parameter, not an audit parameter. Should the audit run without `--mode` and show severity columns? (Yes per the plan; needs grade.py change.) Should the flag be renamed to match new naming? (Optional.)
3. **The 5th non-catalogue check.** I haven't fully nailed down which 5 checks aren't in patterns.md. Worth doing before writing the doc that mentions the discrepancy. Do you want me to confirm exactly which 5 and document it, or just say "43 checks, 38 catalogued patterns, 5 statistical/structural" and move on?
4. **Action 3 ("Write") is new.** The current code has no Write-specific path. The post-check exists. The structural self-check exists. But the workflow ("draft from a brief, then check") needs the agent to do something the script can't validate ahead of time (it has no input to compare against). Are you OK with this being an agent-only path, or do you want grade.py to add a `--write` mode that does some pre-draft validation?
5. **Headless / non-interactive contract.** Mae hasn't spoken on this directly. Default behaviour when no human is present: I've been defaulting to Audit (read-only, low-risk). Is that the right call for headless invocation, or should the skill error out and ask for an explicit action?
6. **Citations and credibility scaffolding.** The Wikipedia + Abdulhai citations currently sit in the description. The plan moves them to a Sources section at the bottom. Confirm.

---

## Part 7 — Migration sequencing (after the plan is approved)

1. Write the new SKILL.md from clean foundations using this plan's structure. Target ~200 lines.
2. Update `grade.py` if needed (audit-mode rendering with severity column).
3. Update `dev/evals/test_grade.py` for the new audit-mode rendering.
4. Update `README.md` for the three-action framing.
5. Add 4 generic Write briefs to `dev/evals/samples/briefs/`.
6. Build `dev/evals/blind_eval.py` per the existing eval plan.
7. Run blind eval. Iterate on SKILL.md until thresholds pass.
8. Commit.

The blind-eval gate from the prior plan still applies. Don't merge until the eval shows consistency thresholds met.
