---
date: 2026-04-28
topic: humanise-skill-refocus
---

# Humanise — skill refocus requirements

## Problem Frame

The `humanise` skill audits writing for AI fingerprints and (optionally) helps the writer remove them. Today's `humanise/SKILL.md` is 461 lines of patchwork from iterative cleanup. The most recent attempt to fix it, `dev/plans/2026-04-28-humanise-refocus.md`, locked in a structure (three actions, "severity × intensity" mode/severity matrix) that conflates two unrelated things: how confidently a pattern is an AI tell (intrinsic to the pattern) and how aggressively the user wants to clean it up (user choice).

This brainstorm reframes the user-facing model around a single observation: **the dial only applies to generative outputs.** The audit is full information — it shows every detected tell, no filter. The dial sits on the response side, when the user asks the skill to produce new prose.

The deliverable from the planning phase that follows is a clean SKILL.md and a grader contract that match this model, replacing the existing patchwork.

---

## Actors

- A1. **Writer** — supplies a draft (existing text) or a brief (no draft yet). Reads the audit, decides whether to ask for an intervention, and applies any suggestions or rewrites in their own editor.
- A2. **Agent** — Claude Code invoking the `humanise` skill. Runs the grader, presents flags in the agreed shape, and offers interventions when the writer asks.

---

## Key Flows

- F1. **Audit an existing draft**
  - **Trigger:** Writer hands the agent text and asks the skill to look at it (or invokes the skill on a file).
  - **Actors:** A1, A2.
  - **Steps:** Agent runs the grader. Agent renders the audit (every detected tell, located + explained, no filter). Agent asks: suggestions, rewrite, or done?
  - **Outcome:** Writer sees what's machine-flavoured in their draft, in enough detail to learn the patterns. Writer chooses next step.
  - **Covered by:** R1, R3, R4, R5, R6.

- F2. **Get a list of suggestions after an audit**
  - **Trigger:** Writer picks "suggestions" after F1.
  - **Actors:** A1, A2.
  - **Steps:** Agent generates one suggestion or replacement per flagged tell. Agent presents the full list. Writer applies what they want, ignores the rest.
  - **Outcome:** Writer has concrete alternative phrasings to copy back into their draft, but the draft itself is unchanged by the skill.
  - **Covered by:** R7, R8.

- F3. **Get a full rewrite after an audit**
  - **Trigger:** Writer picks "rewrite" after F1.
  - **Actors:** A1, A2.
  - **Steps:** Agent asks for the depth setting (default applies if not specified). Agent rewrites the draft at the chosen depth. Agent reports before/after.
  - **Outcome:** Writer has a rewritten draft to compare against the original.
  - **Covered by:** R9, R10, R11, R12.

- F4. **Write new text from a brief**
  - **Trigger:** Writer asks the skill to compose new text and supplies a brief (no input draft).
  - **Actors:** A1, A2.
  - **Steps:** Agent asks for the depth setting (default applies if not specified). Agent drafts new text at the chosen depth, avoiding AI patterns prospectively.
  - **Outcome:** Writer has a draft tuned to the chosen depth of human-pattern adherence.
  - **Covered by:** R13, R14, R15, R16.

---

## Requirements

**Identity and scope**

- R1. The skill has one primary action (Audit) and three secondary actions (Suggestions, Rewrite, Write). Audit is the default when the writer supplies text. Write is invoked when the writer supplies a brief instead of a draft. Suggestions and Rewrite are opt-in after an audit.
- R2. The skill never issues an authorship verdict. It surfaces detected patterns and explains them; the writer interprets.

**Audit (informational, no dial)**

- R3. The audit surfaces every detected AI tell. There is no depth filter on the audit — full information is the contract.
- R4. Each flagged tell is presented with the pattern name, the offending sentence or phrase quoted from the writer's text, and a brief explanation of why this pattern reads as machine-touched.
- R5. The audit does not include a suggested fix per flag. Suggested fixes belong to the Suggestions action.
- R6. After presenting the audit, the agent asks the writer whether to proceed with Suggestions, Rewrite, or stop.

**Suggestions (informational, no dial)**

- R7. Triggered only by the writer choosing it after an audit.
- R8. Output is a full list — one suggestion or replacement per flagged tell from the audit. The list is not filtered by depth or severity.
- R8a. Suggestions for lexical patterns (e.g., `delve`, `hedging`, em-dashes, formulaic depth phrases) are drawn from a curated reference file `humanise/references/alternatives.md` so that the alternatives are vetted human options, not freshly generated text that may itself read as AI.
- R8b. Suggestions for structural patterns (e.g., paragraph-length uniformity, anaphoric scaffolding) are produced contextually by the agent because the replacement is rewriting, not substitution. The `alternatives.md` file does not need to cover these.

**Rewrite (generative, depth dial)**

- R9. Triggered only by the writer choosing it after an audit.
- R10. Output is a rewritten version of the original draft. The skill does not modify the writer's source file; it returns the rewrite for the writer to compare.
- R11. The rewrite is governed by a 3-point depth dial (see R17).
- R12. The agent reports before/after so the writer can compare.

**Write (generative, depth dial)**

- R13. Triggered when the writer supplies a brief and no input draft, and asks the skill to compose.
- R14. Output is a new draft based on the brief, written to avoid the AI patterns the skill knows about.
- R15. The draft is governed by the same 3-point depth dial as Rewrite (see R17).
- R16. The skill does not run an audit on its own output before returning it. (Whether to add a self-audit step is deferred to planning.)

**Depth dial (applies only to Rewrite and Write)**

- R17. The dial has 3 settings:
  - **Obvious** — only address blatant, surface-level AI tells.
  - **Balanced** — address obvious tells plus the strong ones a careful reader would notice.
  - **All** — address every detected pattern, including the implicit/structural ones a reader wouldn't consciously notice.
- R18. The dial does not apply to Audit or Suggestions. Those actions are full information regardless of depth.
- R19. The agent asks the writer for a depth setting when invoking Rewrite or Write, unless the writer specified one. If the writer declines to choose, a default applies (default value deferred to planning).

---

## Acceptance Examples

- AE1. **Covers R3, R4.** Given a draft containing "I wanted to delve into the topic" and three hedging phrases, when the writer runs an audit, the output includes a `delve` entry showing the quoted sentence and a brief explanation of why "delve" reads as an AI tell, and a `hedging` entry showing all three quoted phrases with a single shared explanation.

- AE2. **Covers R5, R6.** Given the audit in AE1 has just been presented, when the agent finishes the audit output, the agent does not include suggested rewrites for any flag, and asks the writer whether to proceed with Suggestions, Rewrite, or stop.

- AE3. **Covers R7, R8, R8a, R8b.** Given the audit in AE1, when the writer picks Suggestions, the output is one suggested replacement for the `delve` instance (drawn from `references/alternatives.md`'s canonical replacements for `delve`) and three suggested replacements for the `hedging` instances (also from the file) — all four shown, regardless of how strong each tell is. If the same audit also flagged `paragraph-length-uniformity` (a structural pattern), the suggestion for that flag is composed contextually by the agent rather than pulled from the file.

- AE4. **Covers R11, R17.** Given the audit in AE1, when the writer picks Rewrite at "Obvious", the rewritten draft addresses `delve` and other surface-level tells but leaves subtle patterns (e.g., paragraph-length uniformity) untouched. When the writer picks Rewrite at "All", the rewritten draft addresses every flagged pattern including the structural ones.

- AE5. **Covers R13, R14, R15.** Given a writer who supplies a brief ("write a 200-word paragraph about my linocut practice") and no draft, when the writer asks the skill to write, the agent asks for a depth setting and then produces a draft tuned to that setting.

---

## Success Criteria

- The new SKILL.md fits comfortably under ~250 lines and a writer can read the whole thing once and know which action they want without trial and error.
- A writer who has seen one audit can describe the output shape from memory ("located + explained per flag"), the four actions, and what the dial does — without reading SKILL.md again.
- An agent invoked with `/humanise` on a draft never proceeds to a rewrite without an explicit user choice. An agent invoked with a brief never silently audits an existing file as a fallback.
- A planner picking up this document and the existing codebase can write the implementation plan without re-deciding any of the four actions, the dial structure, or the audit's output shape.

---

## Scope Boundaries

- The skill does not score the draft or assign an AI-likelihood verdict. It surfaces patterns; it does not classify authorship.
- The skill does not auto-rewrite. Audit is the default when the writer supplies text; Rewrite and Suggestions only fire on explicit opt-in.
- The skill does not optimise for evading AI detectors. The point is helping the writer see and decide, not winning a detection arms race.
- The skill does not modify the writer's source file. Output is returned in the conversation (or saved as a separate file via the existing save modifier, if retained — see Outstanding Questions).
- The skill's catalogue and grader are out of scope as catalogue redesigns. The mapping between the existing 43 grader checks and the 3-point depth dial is a planning question, not a requirements question.

---

## Key Decisions

- **The dial is on generative outputs, not on the audit.** The prior plan put intensity on every action ("the audit is mode-agnostic" was added as a defensive sub-rule). The new model makes the principle structural: informational actions show everything, generative actions need user control over how aggressive to be.
- **Suggestions exists as a distinct action, not as part of the audit.** Suggestions is the writer's middle ground between "show me, I'll do it myself" (Audit) and "do it for me" (Rewrite). Folding suggestions into the audit would force every audit user to receive proposed rewrites whether they wanted them or not.
- **Audit and Suggestions are full lists, not filtered.** Filtering them would force the writer to choose what they care about before they've seen what's there. The dial belongs after the writer has seen the full picture, on the side that produces new prose.
- **Three depth settings, not two or free-form.** Two collapses the middle position writers actually want. Free-form is fuzzier than the contract needs to be and harder to test against the existing grader's tiered checks.
- **Write from a brief stays as an action.** The earlier "smallest version is Audit" answer cut Write only as a minimum-viable check, not as a permanent exclusion. The skill has cohesive coverage of "writing without AI tells" — composing-from-brief belongs in that set.
- **Suggestions are sourced from a curated reference file, not freshly generated.** The risk of agent-generated alternatives being themselves AI-flavoured (e.g., "delve" → "explore", which is also flagged) is real. A curated `references/alternatives.md` bakes in writer judgement and gives the Suggestions action a vetted source of truth. Structural patterns, where there is no canonical replacement, are handled contextually by the agent.

---

## Dependencies / Assumptions

- The existing grader (`humanise/grade.py`, 43 programmatic checks across hard_fail / strong_warning / context_warning severity classes) provides the detection layer the audit calls into. This requirements document assumes the grader stays roughly as-is in capability; how its severity classes map to the new 3-point depth dial is a planning decision.
- The existing references (`humanise/references/patterns.md`, `severity-detail.md`, `voice.md`, `example.md`) are assumed to remain useful as agent-loaded context for the actions that need them. Whether each one survives the rewrite is a planning question.
- A new `humanise/references/alternatives.md` will be created during planning/implementation to provide canonical human alternatives for lexical patterns. Initial scope: at minimum the patterns covered by `severity-detail.md` plus the most common lexical tells from `patterns.md`. Coverage breadth is a planning decision.
- The skill is invoked through Claude Code as a slash command (`/humanise`) or by the agent recognising a humanise-shaped intent. Headless / non-interactive invocation behaviour is unspecified by this document and deferred to planning.
- The existing blind-eval harness in `dev/evals/` is assumed to be the consistency-gate for any SKILL.md change, per the prior plan.

---

## Outstanding Questions

### Resolve Before Planning

- *(none — the brainstorm has converged on the user-facing model. Remaining items below are technical or infra questions appropriate for planning.)*

### Deferred to Planning

- [Affects R19][User decision] What is the default depth value when the writer doesn't specify one? "Balanced" is the obvious candidate but worth confirming during plan review.
- [Affects R3, R4][Technical] What does "located" mean precisely when a pattern is structural rather than lexical (e.g., paragraph-length uniformity)? The audit needs a coherent rendering rule for non-quotable findings.
- [Affects R3][Technical] Does the audit include a one-line summary (e.g., total flag count) or go straight into the list? Tactical formatting question.
- [Affects R8a][Technical] What is the initial coverage of `references/alternatives.md` — every lexical pattern in `patterns.md`, only the 4 patterns in `severity-detail.md`, or somewhere in between? And how many alternatives per pattern?
- [Affects R11, R17][Technical] How do the existing grader's severity classes (hard_fail / strong_warning / context_warning) map onto the 3-point depth dial? E.g., does "Obvious" mean hard_fail only, or hard_fail + strong_warning?
- [Affects R16][Technical] Should Write run a self-audit on its output before returning, and report the results? The earlier plan's "post-check" loop existed for this; whether to keep it is a planning call.
- [Affects R10, R14][Technical] File-save behaviour. The current SKILL.md has a `save` modifier that wraps output to a file next to the input. Does this survive in the new model, and does it apply to all four actions or only the generative ones?
- [Affects all flows][Technical] Headless / programmatic invocation contract. What's the default action when there's no human turn-taking — does the skill error out, run audit only, or refuse?
- [Affects all][Needs research] Whether the existing grader checks all map cleanly to "patterns the writer should learn to spot" — some checks (e.g., overall AI signal pressure) are aggregate scores rather than locatable patterns and may need different rendering.

---

## Next Steps

`-> /ce-plan` for structured implementation planning. The plan should cover:
1. New SKILL.md structure and content (target ~200-250 lines).
2. Grader updates needed to support the audit/suggestions/rewrite/write split.
3. Mapping of existing severity classes to the 3-point depth dial.
4. Migration of existing references (`patterns.md`, `severity-detail.md`, `voice.md`, `example.md`) — keep, rewrite, or remove.
5. Authoring `references/alternatives.md` — initial coverage, format, and per-pattern alternative count.
6. Eval harness updates per `dev/evals/` to gate the rewrite.
7. Sequence of changes that keeps each commit shippable.
