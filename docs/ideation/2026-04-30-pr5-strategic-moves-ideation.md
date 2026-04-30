---
date: 2026-04-30
topic: pr5-strategic-moves
focus: dev/reviews/2026-04-30-pr5-review-findings.md — strategic next moves for the humanise project
mode: repo-grounded
---

# Ideation: Strategic next moves after PR #5 review

## Codebase context

Python + Markdown Claude Code skill. Two-tier layout: `humanise/` (installable: SKILL.md, grade.py 2765 LOC, references/) vs `dev/` (evals harness, research, plans, brainstorms, reviews, iteration workspaces 1-4). 43-check grader, 38 patterns / 8 categories. README has a marker-bounded auto-rewritten performance block — every harness run touches the user-facing pitch. Plan accretion in `dev/plans/`. No AGENTS.md / CLAUDE.md. No `docs/solutions/`.

PR #5 review surfaced ~60 deduped findings across 14 reviewers. Three strategic decisions the document raised: (1) signals work and the +44% headline stands vs signals don't generalise to register; (2) land the audit-voice sweep across 32+ sites or hold the README; (3) architecture-first vs interleave substance work.

Five queued substance items in the research findings doc — audit-voice reframe, demote/recategorise patterns, body-stats checks, genre-aware thresholds, mean-sentence-length check — sit downstream of these decisions.

## Grounding from external research

- **Sadasivan et al. 2023 (arXiv:2303.11156)** — detection AUROC mathematically bounded by total variation distance between human and AI text distributions. As LLMs improve, the bound shrinks. **Detection framing is unsustainable on first principles**, independent of N=5 data.
- **Stanford HAI 2023 / TOEFL** — 61% of non-native English essays misclassified as AI by perplexity-based detectors. Mechanism: register features misread as authorship features. The humanise corpus finding is the field's documented failure mode.
- **GhostBuster (NAACL 2024)** — average human accuracy at distinguishing human from AI prose was 59% (max 80%, min 34%). External warrant for "audit priority for human review" voice.
- **RAID (ACL 2024)** — 6.2M generations across 11 models / 8 domains / 11 attacks. Length normalisation methodology is *under-specified* in the field — no canonical pattern to borrow.
- **Turnitin precedent** — kept detection feature, foregrounded Draft Coach / Feedback Studio quality-improvement positioning. Did not abandon, layered.
- **Tool-design space** — Hemingway: surface without explain. Vale: rule author writes message. proselint: explain via cited authority. Grammarly: prescriptive with short rationale. **None do context-sensitive explanation of *why* a pattern correlates with AI text.** Market opening.
- **Promptfoo / Anthropic eval guidance** — pin judge model version, alert on mean score shift > 0.1, prefer binary or 3-point scales, version judge prompt as code, calibrate against human golden set, "read the transcripts".

## Past learnings

None — `docs/solutions/` doesn't exist. Worth treating as a finding: this PR raised ~9 generalisable patterns (cross-iter determinism, audit-voice, small-N stats, vocab-sweep coordination, genre-paired corpus methodology) with no capture location.

---

## Ranked Ideas

### 1. Single-source vocabulary registry + JSON audit-format contract

**Description:** One canonical structured source (`humanise/vocabulary.yaml` or `.json`) keyed by pattern_id with fields `audit_voice`, `prescriptive_voice`, `severity`, `audit_priority`, `evidence_summary`, `corpus_separation`, `last_calibrated`, `references[]`. SKILL.md, references/severity-detail.md, references/alternatives.md, evals.json prompts, and `grade.py`'s CHECK_REPORT_TEXT all *render* from it via a thin generator. Pair with promoting the `**Audit**` / `**Suggestions**` / `**Rewrite**` / `**Draft**` section format from prose convention to a versioned JSON schema in `humanise/contracts/audit-format-v1.json`, parsed by a single shared parser used by both the iteration runner and the grader.

**Warrant:** `direct:` PR review documents 32+ "AI tell" sites needing coordinated reframing (P0-DOC-02, P1-DOC-12). P1-CODE-26 documents two parallel section parsers that can disagree on lowercase headers. P0-CODE-04 introduces seven `check_audit_shape_*` functions that exist *because there is no contract document*. P3-CODE-53 flags that the iteration runner pokes `GRADE.split_sentences`, `GRADE.CHECK_REPORT_TEXT`, etc. with no `__all__` boundary. Three independent reviewers point at the same shape: pattern metadata and audit format are duplicated across surfaces. `external:` Vale's rule-author-writes-message architecture is the closest production analogue and the grounding's tool-design review identifies it as the structurally cleanest of the prose-linter ecosystem.

**Rationale:** The next reframe — and the audit-voice question is unresolved, so there *will* be one — collapses from a 32-site coordinated commit (with test breakage and threshold-table re-baselining) to a single YAML edit + regenerate. The current "AI tell" / "review priority" mismatch becomes structurally impossible because both phrasings live on the same record. Demotion of `manufactured-insight` becomes one field flip + regen, not a planning negotiation. Two-parser drift (P1-CODE-26) collapses by construction. The seven untested `check_audit_shape_*` functions get replaced by JSON-schema validation.

**Downsides:** One-shot architectural sweep — touches every surface that currently hardcodes pattern metadata. Cannot land incrementally without temporarily having both old and new sources of truth. Risk of bike-shedding the schema before any consumer code exists.

**Confidence:** 90%
**Complexity:** Medium-High
**Status:** Unexplored

---

### 2. Editorial gate on the README — split into narrative pitch + auto dashboard

**Description:** Tear `README.md` into two artefacts: `README.md` (slow-changing narrative, hand-edited, no auto-blocks, no harness data — it pitches what the skill *is*) and `dev/dashboards/latest-performance.md` (auto-rewritten by the harness with corpus statistics, per-pattern density, iteration deltas — it shows what the skill *finds*). The `update_readme_performance_block` function targets the dashboard, not the README. README links to the dashboard; promotion of any dashboard claim into README copy is a deliberate edit, never a side-effect of running evals.

**Warrant:** `direct:` Adversarial residual risk explicitly named in the findings doc: "*update_readme_performance_block rewrites a marker-bounded section of the published README on every run. Any harness data-quality bug auto-publishes to the user-facing pitch.*" All three strategic decisions in the findings doc pivot on README/research-doc inconsistency (P0-DOC-01, P0-DOC-03, P1-DOC-09, P1-DOC-19). `external:` Tool-design review (Hemingway, Vale, proselint, Grammarly) — none put their evidence base on the front page of their pitch. The pattern is: pitch states what the tool does; methodology and evidence live in linked docs / changelogs / benchmark pages. humanise is the outlier in trying to do both in one surface, and the contradiction is the consequence.

**Rationale:** Resolves strategic decision #1 mechanically — there is no headline number to defend if no headline number ships automatically. Forces the human to consciously elect each claim, which is the right policy for a load-bearing pitch with N=5 evidence. Removes the "harness data-quality bug auto-publishes" hazard structurally rather than by vigilance. Subsequent research findings can land in `dev/research/` and `dev/dashboards/` without "do we update the README?" being a per-iteration debate.

**Downsides:** Loses the "look at the README and see how good the skill is right now" property of the current setup (which is also exactly the property that creates the hazard). Requires the human to remember to update the narrative occasionally — which is a feature, not a bug, but is a behaviour change.

**Confidence:** 85%
**Complexity:** Low-Medium
**Status:** Unexplored

---

### 3. Immutable run records + grader/corpus version stamps

**Description:** Replace the mutable `dev/skill-workspace/iteration-N/` model with `dev/skill-workspace/runs/<run-id>/` (timestamped, never overwritten). Each run has a `manifest.json` with `grader_sha`, `threshold_set_hash` (sha256 of the threshold constants block), `corpus_sha`, `executor`, `model`, `started_at`, `completed_at`, `status`, `failed_evals[]`. `iteration-N/` becomes a symlink to the latest successful run. The harness defaults change: `--reset` is explicit, `--resume` becomes available, `--only NAME[,NAME]` and `--only-failed` are first-class. The comparator refuses cross-version compares without `--cross-version-compare`, in which case it prints a threshold-diff explaining what changed. SIGINT installs a signal-aware supervisor. Progress goes to stderr; stdout is reserved for machine output.

**Warrant:** `direct:` Five separate findings describe operations on shared mutable state that should be append-only: P1-CODE-20 (default reset wipes prior work), P1-CODE-22 (always-zero exit hides failures), P1-CODE-25 (silent fallback to full output as rewrite), P2-CODE-29 (non-atomic writes corrupt JSONs), P2-CODE-36 (no grader-version stamp invalidates cross-iteration comparisons). P1-CODE-24 documents the SIGINT gap separately. `external:` Promptfoo and Anthropic eval guidance (grounding) — pin judge model version explicitly, alert on mean score shift > 0.1, version judge prompt as code, calibrate continuously. Anthropic Skill Creator 2.0 separates executor / grader / comparator / analyzer as distinct axes.

**Rationale:** Cross-iteration claims (the thing the README and `grade-sweep-report.json` rely on) become structurally trustable. The "iteration 4 vs iteration 3" comparison is now a defined operation: same grader_sha + same corpus_sha = comparable; otherwise the comparator surfaces what changed before computing deltas. The harness becomes resumable, which converts a 45-minute crashed run from "lost work" to "rerun the failed evals". One architectural move retires 5+ findings.

**Downsides:** Run directory grows monotonically — needs a retention policy. Symlink-based "iteration-N" might confuse tooling that expects the directory to be the canonical artifact. Comparator semantics need careful design — the threshold-diff output is essentially a new mini-product.

**Confidence:** 85%
**Complexity:** Medium
**Status:** Unexplored

---

### 4. Continuous calibrated register-distance score with per-pattern reliability curves

**Description:** Reframe the grader's internal output: every pattern emits a continuous register-distance score (z-score against a register-specific human-corpus distribution, or distance from a register centroid in feature space). The four-action vocabulary (must-fix / consider / nudge / context-warning) becomes a *display layer* — one threshold function applied to the underlying distance. Each pattern carries a published reliability curve: "fires at density X per 1k words on AI-rewrite samples in personal-essay register, density Y on human samples, P(AI | flag) ≈ 0.55 with CI 0.32-0.78 (humanise-corpus v0.4, n=5+5)". The README's headline becomes a per-pattern density-gap chart with CI shading, not a single +44%.

**Warrant:** `external:` Sadasivan et al. 2023 — AUROC mathematically bounded; pretending to determinism on bounded-AUROC tasks is a category error. `external:` GhostBuster (NAACL 2024) explicitly exports uncertain LLM-judge outputs (0.4-0.6) to JSONL for human review — uncertainty is first-class, not defect. `external:` Stockfish-style continuous evaluation with display-layer thresholds is the cleanest cross-domain analogue (chess engines decoupled engine from UI for exactly this reason). `external:` Earthquake/weather forecasting calibration — reliability diagrams + Brier scores are the discipline the field developed when categorical claims couldn't be defended on uncertain data. `direct:` README §"What we found" already says "the signal is the *stack*, not any one occurrence" but the headline still uses raw hit-counts. Text and metric contradict; the fix is to make the metric reflect the text.

**Rationale:** Demotion becomes automatic — patterns with wide CIs *are* demoted by the output presentation. No threshold-tuning negotiation; no severity-detail.md edits. Resolves the +44% / "doesn't separate" tension (P0-DOC-03) — the README publishes the reliability diagram, not a single number. Provides the discrimination metric P1-DOC-15 asks for as a release gate (mean Brier score across catalogue, length-normalised gap with bootstrap CI). Solves the determinism cluster (P2-CODE-36) by making cross-iteration comparison a re-rendering of stored continuous scores rather than a re-run with potentially-shifted thresholds.

**Downsides:** Biggest epistemic shift in the set. Requires actually computing per-pattern calibration curves (which needs adequate per-pattern N — currently N=5 per group is barely enough for a single rough estimate per pattern, let alone reliability curves). Some patterns may not separate enough to support a meaningful curve; that's a finding, but it's an uncomfortable one to ship. README chart needs design.

**Confidence:** 70%
**Complexity:** High
**Status:** Unexplored

---

### 5. 5-check gating grader + 38-pattern advisory catalogue

**Description:** Invert the default. The grader's *gating* check set is exactly 5 — the ones the existing corpus shows actually separate human from AI-rewrite at length-normalised density with non-overlapping CIs (likely candidates: sentence-length-mean, sentence-length-variance with corrected threshold, em-dashes density, paragraph-length variance, vocabulary-diversity). The other 38 patterns become an *advisory diagnostic catalogue* — surfaced in audit output as context with their per-pattern density, never gating, never headline. Iteration baselines and threshold-tuning attention concentrate on the 5; the catalogue grows or shrinks without touching the gating contract.

**Warrant:** `direct:` README's own honest finding is "the signal is the stack, not any one occurrence". P1-DOC-09 (manufactured-insight overclaim — fires 2/5 humans, 0/5 AI rewrites) and P1-DOC-10 (three of four queued "new candidate signals" already exist as wired-in checks) both point at "we have too many gating signals, most don't separate". P1-CODE-11 (sentence-variance threshold off by ~2.5×) confirms threshold-tuning attention is currently spread across patterns where it doesn't matter. `reasoned:` 43 checks gating with no per-pattern separation evidence is taxonomy theatre. Five gating checks + 38 advisory patterns is the same information with the right epistemic weight. Combined with idea 4 (continuous calibrated score), the catalogue patterns get to keep showing their numbers without making categorical claims.

**Rationale:** Answers the queued "demote/recategorise patterns" item by inverting the default — patterns are advisory unless proven otherwise. Eliminates the manufactured-insight overclaim by structural design, not by per-pattern argument. Reduces threshold-tuning surface area by ~88%. Makes "did iteration N+1 improve?" answerable on the 5 checks that matter. The 38-pattern advisory catalogue retains the vocabulary contribution (which is real value — Hemingway/Vale/proselint each have ~50-100 checks, so the catalogue size is appropriate for the *vocabulary* role, just wrong for the *gating* role).

**Downsides:** Picking the 5 is contested and depends on the corpus state — at N=5 per group, even the survivors have wide CIs. Risks rejecting checks that would separate at higher N (genre-aware, longer samples). Requires a re-baselining of every iteration's "pass rate" claim. The cull-versus-keep argument will be a real conversation, not a one-shot decision.

**Confidence:** 75%
**Complexity:** Medium
**Status:** Unexplored

---

### 6. Audience-aware voice — one engine, two personas via invocation context

**Description:** The skill keeps one engine, one registry, one corpus, one set of patterns. Voice changes by invocation surface. `/humanise audit` (a reviewer or editor invoking on someone else's prose) uses the calibrated audit voice — "review priority", "this pattern fires at register-X density, look-alike disambiguator: ..., your judgement". `/humanise rewrite` (a writer asking for help with their own prose) uses the prescriptive voice — "consider replacing with X". Same flagged patterns; different rhetorical packaging because the reader-prose relationship is different. The audit-voice / prescriptive-voice mismatch (P0-DOC-02) is resolved by *retaining both* in the registry's twin fields and selecting at render time.

**Warrant:** `external:` Turnitin precedent (grounding) — kept the underlying similarity-detection engine; layered Draft Coach (writer-facing, supportive) over Feedback Studio (instructor-facing, evidentiary). The product retired neither voice; it routed by audience. `external:` GhostBuster's 59% human-baseline + Sadasivan's AUROC bound together imply that *neither* voice can claim authority by itself — the audit voice is calibrated humility (correct for reviewers); the prescriptive voice is action-oriented (correct for writers). `direct:` Strategic decision #2 in the findings doc treats the voice question as a forced binary — but the binary only exists if you accept one-voice-per-skill. P0-DOC-01's "identity drift" concern dissolves: there is no identity drift if the identity is "audience-aware register-feature explainer", and the audit/rewrite split is a deliberate routing choice, not a contradiction.

**Rationale:** Strategic decision #2 stops being "land the sweep or hold the README". The sweep ships as a registry change with twin fields; the README continues using audit voice (because users coming to the README are evaluating the tool, not asking it to rewrite their prose); the rewrite surface continues using prescriptive voice (because writers asking for a rewrite want instruction, not calibration). Composes naturally with idea 1 (single-source registry) — the registry is the place the twin fields live.

**Downsides:** New invocation contract — the skill currently doesn't differentiate by invocation surface. Needs design work on what "surface" means in Claude Code (slash command argument? sub-command? frontmatter dispatch?). Risk of confusing the user about which voice they're getting.

**Confidence:** 65%
**Complexity:** Medium
**Status:** Unexplored

---

### 7. Operator-surface compounding — AGENTS.md + STATUS.md + active-plan invariant + docs/solutions/

**Description:** Establish four conventions now while their absence is fresh. (a) `AGENTS.md` at repo root capturing skill frontmatter rules, `humanise/` vs `dev/` separation, no-spaces-in-filenames, vocabulary-source-of-truth location, audit-format contract location, eval-discipline rules (golden-set gate, judge-version pinning). (b) `dev/STATUS.md` updated by the harness on successful runs + manually edited for strategic state — answers "which iteration is active, what's the last green run, what are the open strategic decisions, what's blocked" in 2 minutes. (c) `dev/plans/active.md` is the only un-prefixed file; superseding is `mv active.md archive/YYYY-MM-DD-<slug>.md && mv new-plan.md active.md` wrapped in a `make supersede` command. (d) `docs/solutions/` directory established with the 9 generalisable patterns this PR review surfaced (cross-iteration determinism, audit-voice mismatch, small-N statistical claims, vocabulary sweep coordination, genre-paired corpus methodology, README auto-block hazard, two-parser drift, default-wipes-prior footgun, length-confound).

**Warrant:** `direct:` Project-standards reviewer returned zero findings because no AGENTS.md / CLAUDE.md exists (findings doc § "Reviewer roster"). P2-DOC-44 (space in `examples ai.txt` filename) is exactly the class AGENTS.md catches. Three reviewers (coherence, scope-guardian, adv-doc) independently flagged the missing supersession marker on `humanise-refocus.md` — a textual annotation that should have been mechanical. The findings doc itself opens with "Read this first — three strategic decisions" because the reviewer noticed Mae would lose this context between sessions; STATUS.md is what should have absorbed that load. `direct:` Grounding agent confirmed `docs/solutions/` doesn't exist and the absence "is itself signal — the topics this PR raised are generalisable but uncaptured". `external:` ce-compound and ce-learnings-researcher are designed around the `docs/solutions/` convention; ce-learnings-researcher ran on this PR with no corpus to retrieve from.

**Rationale:** Cheap to establish, compounds across every future PR / ideation / planning session. Future-Mae returning after a 2-week gap reads STATUS.md instead of reverse-engineering state from 11 plan/research/brainstorm docs. Future PR reviews catch convention violations automatically (project-standards reviewer starts returning real findings). Future ideations have a learnings corpus to retrieve from. The "which plan is canonical?" question becomes a filesystem answer.

**Downsides:** Four conventions at once is a lot of new structure for a solo project. Risk of over-formalising a workflow that's currently working informally. STATUS.md needs maintenance — if it goes stale, it's worse than not existing.

**Confidence:** 95%
**Complexity:** Low
**Status:** Unexplored

---

## Worth revisiting (rejected on prioritisation, not warrant)

These had strong warrant but didn't make the top 7 because they're either premature (depend on something earlier in the order) or are big-risk-big-reward bets better surfaced as separate decisions.

| # | Idea | Why surfaced |
|---|------|--------------|
| W1 | **Field-guide voice with explicit similar-species disambiguation** — every pattern carries a "looks like, but isn't" block (e.g., manufactured-insight: "vs legitimate epistemic hedging in academic prose, vs quoted material with attribution"). | Closes the proselint gap (no tool does context-sensitive explanation of why a pattern correlates) and addresses the Stanford HAI / TOEFL bias finding head-on. Cheap, additive — strong candidate for the next PR. |
| W2 | **Pair-comparator product reframe** — input becomes two pieces of prose; output is divergence ("Doc B sits 1.4σ further from human-cluster than Doc A on these dimensions"). Single-document audit becomes a degenerate case. | Most distinctive product reframe; absolute claims become structurally impossible. Echoes Turnitin's converged design (similarity is always *between* texts). High-risk-high-reward; worth a separate brainstorm. |
| W3 | **Pharmacovigilance-shape user-reported intake** — opt-in `humanise report-fp` flow grows the corpus from real authoring (with a non-punitive covenant, ASRS-style). | Unblocks corpus growth without solving sourcing/licensing. Premature today (no install path for it), but the structural fit is strong enough to revisit at iteration 6+. |

## Rejection summary

| # | Idea | Reason rejected |
|---|------|-----------------|
| 1 | F1-1 invert README publish direction | Subsumed by survivor 2 (editorial gate) |
| 2 | F1-2 extract single phrasing module | Subsumed by survivor 1 (single-source registry) |
| 3 | F1-5 grader-as-public-package | Premature refactor; do the cull (survivor 5) first, repackage second |
| 4 | F1-6 split into two skills (audit + rewrite) | Subsumed by survivor 6 (one engine, audience-aware voice) — splitting is more work than templating |
| 5 | F1-7 dev/findings/ as evidence venue | Subsumed by survivors 2 (dashboard) + 7 (docs/solutions/) |
| 6 | F2-1 kill update_readme_performance_block | Subsumed by survivor 2 |
| 7 | F2-2 vocabulary.json | Subsumed by survivor 1 |
| 8 | F2-3 remove depth dial entirely | Tactical; depth removal could survive survivor 6 but is a separate decision |
| 9 | F2-5 make supersede automation | Subsumed by survivor 7 (active-plan invariant) |
| 10 | F2-6 auto reviews → follow-up issues | Premature; review-doc itself is the durable artifact for now |
| 11 | F2-7 remove "What we found" from README | Subsumed by survivor 2 |
| 12 | F2-8 weekly corpus-growth agent | Premature without sourcing/licensing strategy (P1-DOC-14) |
| 13 | F3-2 N=5 forever by design | Strong critique tool, weak design tool — folded into survivor 4's calibration framing |
| 14 | F3-3 pattern co-occurrence as unit | Subsumed by survivor 4 (continuous score IS the joint-distribution unit) |
| 15 | F3-5 interactive corpus-comparison page | Speculative product surface outside install model |
| 16 | F3-6 iterations as 4-axis matrix | Subsumed by survivor 3 (version stamps make this implicit) |
| 17 | F3-8 headline = density gap | Subsumed by survivor 4 |
| 18 | F4-3 pattern-evidence registry as standalone | Subsumed by survivor 1 (registry's evidence field) |
| 19 | F4-4 calibration golden set | Strong but premature — survivors 4 + 3 land first, golden set follows |
| 20 | F4-5 audit-format schema standalone | Subsumed by survivor 1 (JSON contract is part of it) |
| 21 | F4-8 decoupled corpus repo | Overkill at N=5; revisit at N≥50 |
| 22 | F4-9 multi-judge ensemble | Premature; needs golden set first (which comes after survivor 4) |
| 23 | F4-10 discrimination metric as gate | Subsumed by survivor 4 (calibration curves give this) |
| 24 | F5-2 chess engine continuous score | Subsumed by survivor 4 |
| 25 | F5-4 music theory separation | Subsumed by survivor 4 (separating signal from rendering) |
| 26 | F5-5 CVE/GHSA pattern registry | Subsumed by survivor 1 (registry with stable IDs) |
| 27 | F5-6 earthquake reliability curves | Subsumed by survivor 4 |
| 28 | F5-7 aviation ASRS confess flow | Speculative; same family as W3 (kept in worth-revisiting) |
| 29 | F5-8 linguistic corpus annotation scheme | Subsumed by survivors 1 + 3 |
| 30 | F6-1 N=1 dyadic comparator | Subsumed by W2 (pair-comparator) and survivor 4 |
| 31 | F6-2 / F6-9 / F6-10 forcing-function flips | Useful as critique tools, not standalone designs |
| 32 | F6-4 fixed 1000-word input contract | Too restrictive for actual user need |
| 33 | F6-5 single adv-doc reviewer pilot | About review process, not project design |
| 34 | F6-6 100-reviewer theme-clustering | About review process, not project design |
| 35 | F6-7 zero prose docs | Too radical; prose docs serve real purposes |
| 36 | F6-8 JSON-only output contract standalone | Subsumed by survivor 1 |

## Suggested ordering (if all seven proceed)

These compound. If pursuing more than one, an ordering that minimises rework:

1. **Survivor 7 (operator surface)** — first because it's cheap and creates the *places* the other ideas land (AGENTS.md captures conventions the next ideas establish; docs/solutions/ captures learnings from the next ideas as they ship; STATUS.md is where the new architecture's state lives).
2. **Survivor 1 (single-source registry + JSON contract)** — establishes the *source of truth* every later idea references.
3. **Survivor 6 (audience-aware voice)** — uses the twin fields in survivor 1's registry; resolves strategic decision #2 cleanly.
4. **Survivor 2 (editorial gate on README)** — removes the auto-publish hazard before the next iteration can re-trigger it.
5. **Survivor 3 (immutable run records + version stamps)** — required infrastructure for survivor 4's reliability curves to be cross-iteration meaningful.
6. **Survivor 5 (5-check cull + advisory catalogue)** — answers the demote/recategorise question by construction.
7. **Survivor 4 (continuous calibrated score)** — biggest epistemic shift, lands last on top of everything above.

Survivors 1, 2, and 7 are independently shippable in any order. Survivors 3 → 4 are sequential. Survivor 5 can land before or after 3-4 depending on whether the cull is decided on existing data or on calibration curves.
