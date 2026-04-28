# Humanise Skill: Current Collaboration Issue

## What I Understand The Problem To Be

The current `humanise` skill is drifting toward a one-shot rewrite workflow:

1. receive text,
2. run checks,
3. rewrite the text,
4. report that the rewrite passes.

That is too narrow. It makes the skill behave like a generic rewriting assistant, when the actual purpose is broader and more useful: the skill should primarily help users understand signs of AI-style writing in a draft, then support different follow-up actions depending on what the user wants.

The skill should not assume the user wants a rewrite. A user may want only an audit. They may want a diagnosis before deciding what to change. They may want to compare Light, Medium, and Hard approaches. They may want a Markdown report saved for review. They may want a rewrite only after agreeing on a target.

Right now the workflow is not transparent enough about those choices.

## The Core Misalignment

The skill is being treated as if it is mainly a writing skill. It should be treated first as an AI-writing audit and detection skill.

Rewriting is one possible output, not the default identity of the tool.

The current report language also exposes too much implementation logic. Phrases like "one of the 43 checks" or "internal pressure score" explain why the checker is technically counted a certain way, but they do not help an end user understand what is wrong with the writing.

The user does not need the tool to defend its architecture. The user needs the tool to explain:

- what pattern was detected,
- what that pattern means in normal writing terms,
- where it appeared,
- why it may read as AI-style writing,
- how serious the issue is,
- what options the user has next.

## The Missing Operating Models

The skill needs explicit modes of use. At minimum, it should support these workflows:

### 1. Audit Only

Use when the user asks:

- "Does this sound AI?"
- "Check this for AI writing."
- "Audit this."
- "What is wrong with this?"

Expected output:

- overall summary,
- confidence assessment,
- full check table,
- explanation of flagged patterns in plain English,
- no rewrite unless the user asks for one.

### 2. Audit Plus Recommendation

Use when the user wants help deciding what to do.

Expected output:

- audit report,
- severity of each issue,
- recommended next action,
- suggested Light / Medium / Hard approach,
- a direct question asking what outcome the user wants.

### 3. Audit, Agree, Then Rewrite

Use when the request is ambiguous or the text has meaningful voice, literary style, humour, dialogue, or genre-specific features.

Expected flow:

1. run audit,
2. explain findings,
3. recommend an approach,
4. ask the user to choose Light, Medium, Hard, or audit-only,
5. only then rewrite.

### 4. Rewrite And Verify

Use when the user explicitly asks for rewriting or says to proceed.

Expected output:

- initial audit,
- selected mode and rationale,
- rewrite,
- structural self-audit,
- post-check report,
- list of remaining issues or confirmation that checks are clear.

### 5. Save A Report

Use when the user wants artifacts for review, sharing, or regression testing.

Expected output:

- save an `.md` report containing the audit, findings, check table, and recommended actions,
- optionally include before/after text if a rewrite was performed,
- state the file path.

## What The Skill Should Ask

When the user has not clearly requested a rewrite, the skill should ask a short question before changing text:

> Do you want an audit only, a recommended plan, or a rewrite after the audit?

If the user asks for a rewrite but the mode is unclear:

> How hard should I go: Light cleanup, Medium humanise pass, or Hard de-AI pass?

If the genre is voice-sensitive:

> This looks voice-sensitive. Should I preserve style even if some context warnings remain, or should I prioritise removing all flags?

## Report Language Requirements

The report should be written for the end user, not for the checker implementation.

Avoid:

- "internal pressure score",
- "one of the 43 checks",
- "context_warning",
- "failure mode",
- "shows signs" without explanation,
- implementation-first justifications.

Prefer:

- "Flagged",
- "Clear",
- "What it looks for",
- "What happened here",
- "Why this matters",
- "Recommended action".

For AI pressure, explain it as accumulation:

> This check looks for weaker AI-writing patterns stacking together. One weak signal may not matter, but several at once can make a draft feel machine-packaged. In this text, the stacked signals were paragraph length uniformity and headings in prose, which made the piece feel over-structured and less naturally varied.

## What Needs To Change

The skill should be refactored around protocol, not only output formatting.

Needed changes:

1. Reframe the skill description as an AI-writing audit skill with optional rewriting.
2. Add explicit workflow models: audit-only, audit-plus-recommendation, audit-agree-rewrite, rewrite-verify, save-report.
3. Make audit-only the default when intent is unclear.
4. Require a clarifying question before rewriting if the user did not clearly ask for rewriting.
5. Change report rows to explain checks in user-facing terms.
6. Add a "why this matters" field or sentence for flagged checks.
7. Remove architecture-defensive language from user-facing reports.
8. Keep JSON diagnostics available for testing/debugging, but do not make them the conceptual model of the skill.
9. Update tests to verify the report is understandable to an end user, not just structurally complete.
10. Run blind-agent tests across at least audit-only and rewrite-verify workflows.

## Success Criteria

The improved skill should make it obvious to a user:

- whether the tool is auditing, recommending, rewriting, or verifying,
- why each flagged pattern matters,
- what choices the user has,
- what the model did and did not change,
- what evidence supports the confidence assessment,
- where the report has been saved if an artifact was requested.

The user should never feel that the tool is making hidden decisions about acceptable AI-style writing. The tool should surface the evidence clearly, recommend next actions, and let the user decide how far to go unless the user has already given a clear instruction.
