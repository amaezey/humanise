# Plan-file cleanup — drop scope-creep, keep substantive subtractions

Status: deferred from 2026-05-01 session.

## Context

The agent that worked on `docs/plans/2026-04-30-001-feat-audit-report-redesign-plan.md` on 2026-05-01 made a mix of legitimate edits and scope creep. The diff is currently uncommitted on `docs/audit-report`. Surgical revert is needed before PR #6 merge — not a full revert.

## Keep (real intent, no rework needed)

- **R23 removed** — was an invented "README dogfood" requirement; correct subtraction.
- **U17 stub** — the paired README-dogfood test unit; correct removal.
- **U16 stub** — work already shipped in `13b4e9d`; correct removal.
- **The U6→U13 deferral reasoning** — the structural argument is sound (touching the README before Phase 3's renderer changes its shape means doing the work twice).
- **Phase 1 status table with commit refs** — useful as a Phase-1 closure record.

## Drop or trim

- **U18 (the new "PR #6 merge-readiness gate" plan unit)** — added unilaterally without sign-off, in direct violation of `feedback_dont_invent_scope.md` ("New requirements (R-IDs) and new units in a plan need explicit user sign-off, not silent insertion"). If a merge checklist is genuinely wanted, put it in `docs/todos/pr-6-merge-readiness.md`, not as a plan unit.
- **9-line essay inside the U6 stub** — trim to one line, e.g. `*Removed 2026-05-01 — deferred entirely to U13 (Phase 3). See plan changelog.*` Multi-paragraph rationalisations of removed units are themselves scope creep.
- **"2026-05-01 update" preamble injected into the Summary section** — belongs in a changelog or commit message body, not the plan's summary section.
- **U13 scope extension absorbing all README work** — the call may be the right one, but it was made unilaterally. Either confirm and keep (with explicit "decision confirmed 2026-05-XX by Mae" annotation), or revert and keep U6 as a Phase-3 unit.
- **Corrupted commit hash in the Phase 1 status table** — U1 row reads `` `d46叶6db` `` with two Chinese characters mixed in. The previous agent's text got mangled. Look up the actual U1 commit (probably `4b9eb84` or earlier, on the `docs/audit-report` branch) and fix.

## How to apply

1. Inspect the current uncommitted diff:
   `git -C .worktrees/docs/audit-report diff docs/plans/2026-04-30-001-feat-audit-report-redesign-plan.md`
2. Apply the trims above. Each is a discrete edit; this is not a wholesale revert.
3. Commit as `docs(plan): surgical cleanup of 2026-05-01 plan edits` (or similar).

## Why not now

Deferred so the Phase 1 verification work (`d43a820`, `45ce36e`, `03e48bc`, `ae9501f`, `2951520`) could land cleanly without coupling unrelated planning-document hygiene to the matcher-fix story.
