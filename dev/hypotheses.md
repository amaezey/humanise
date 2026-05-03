# Hypotheses

Hypotheses to test in future iterations of the humanise project. Each entry stays here until capacity allows a test, or until something cheaper or stronger replaces it.

Each hypothesis includes status, source, statement, test, and impact.

## 1. Continuous calibrated register-distance score per pattern

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` survivor #4. External: Sadasivan et al. 2023 (arXiv:2303.11156) on bounded AUROC; GhostBuster (NAACL 2024) on uncertainty as first-class output.

**Statement:** Each pattern emits a continuous z-score against a register-specific human-corpus distribution rather than a binary fire / no-fire. The four-action vocabulary becomes a display layer applied to the underlying distance. Each pattern carries a reliability curve (firing density on AI vs human in matched register, with bootstrap CI).

**Test:**
- Compute per-pattern density on the existing N=5 corpus and on whatever growth comes next.
- Bootstrap CIs for each pattern's human density and AI density.
- Render a reliability diagram for the most-fired patterns.
- Check whether the diagram surfaces the same demotion signals the current binary thresholds do.

**Impact:** The grader's internal output and the README's headline both shift from raw counts to calibrated densities with CIs. Demotion of weak patterns becomes automatic via wide CIs rather than a per-pattern argument.

## 2. Comparison-engine product reframe

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` worth-revisiting #2.

**Statement:** Input is two pieces of prose; output is divergence on register-distance dimensions ("Doc B sits 1.4σ further from human-cluster than Doc A on these dimensions"). Single-document audit becomes a degenerate case where the second input is the human-corpus centroid.

**Test:**
- Spec a comparator interface that takes two documents.
- Implement on top of the per-pattern density data the grader already produces.
- Run on matched human / AI pairs from the corpus.
- Check whether the divergence output is more useful than the current single-document audit for the kinds of decisions the skill is invoked for.

**Impact:** The skill's framing shifts from "does this read like AI" to "how does this differ from this other thing". Absolute claims become structurally impossible. Aligns with Turnitin's converged design (similarity is always between texts).

## 3. Drop detection framing entirely

**Status:** open

**Source:** Internal: meta-question raised during this session's ideation and review of the README. Current positioning kept for now.

**Statement:** Reposition humanise as a vocabulary tool, a register-feature explainer, or a writing aid, not as anything that detects AI. The current detection framing inherits unsustainable epistemic claims (Sadasivan AUROC bound; Stanford HAI bias finding on non-native English writers).

**Test:**
- Draft three alternative framings (vocabulary tool, register explainer, comparison engine).
- Run each past intended users and check which one the user can actually use without misinterpreting the output.
- Check whether dropping detection framing changes which patterns the catalogue keeps.

**Impact:** The README pitch, the SKILL.md description, and the audit voice all change. The patterns table reframes around register features rather than AI-correlation. The skill positioning moves out of a category where AUROC bounds make claims fragile.

## 4. Single-source vocabulary registry plus JSON audit-format contract

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` survivor #1.

**Statement:** One canonical structured source (`humanise/vocabulary.yaml` keyed by pattern_id with audit_voice, prescriptive_voice, severity, audit_priority, evidence_summary, corpus_separation, references). SKILL.md, severity-detail.md, alternatives.md, evals.json prompts, and grade.py's CHECK_REPORT_TEXT all render from it via a thin generator. Pair with promoting the audit format from prose convention to a versioned JSON schema in `humanise/contracts/audit-format-v1.json`.

**Test:**
- Spec the registry schema.
- Write a generator that produces the current artefacts from the registry.
- Verify byte-equivalence between generated and current artefacts on a no-op run.
- Pick one reframe (e.g., "AI tell" replacement) and check that it lands as a single registry edit plus regenerate, not a coordinated commit across many files.

**Impact:** Cross-surface vocabulary drift becomes structurally impossible. Future reframes collapse from days of coordinated edits to a single field flip. Replaces the seven untested check_audit_shape_* functions with JSON-schema validation.

## 5. Editorial gate on the README

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` survivor #2.

**Statement:** Tear README.md into two artefacts. README.md is a slow-changing narrative pitch with no auto-blocks and no harness data. dev/dashboards/latest-performance.md is auto-rewritten by the harness with corpus statistics, per-pattern density, and iteration deltas. Promotion of any dashboard claim into README copy becomes a deliberate edit, never a side-effect of running evals.

**Test:**
- Split the existing README on this principle.
- Move the marker-bounded auto-block to the dashboard.
- Run a harness iteration and check that README copy is untouched.
- Check whether the README still serves new users without the dashboard front-and-centre.

**Impact:** Removes the "harness data-quality bug auto-publishes to the user-facing pitch" hazard structurally. README claims become deliberate human edits; methodology lives in linked docs. Aligns with the tool-design pattern across Hemingway, Vale, proselint, Grammarly.

## 6. Immutable run records with grader and corpus version stamps

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` survivor #3. External: Promptfoo and Anthropic eval guidance on judge-version pinning and continuous calibration.

**Statement:** Replace the mutable `dev/skill-workspace/iteration-N/` model with `dev/skill-workspace/runs/<run-id>/` (timestamped, never overwritten). Each run carries a `manifest.json` with grader_sha, threshold_set_hash, corpus_sha, executor, model, started_at, completed_at, status, failed_evals. iteration-N becomes a symlink to the latest successful run. Comparator refuses cross-version compares without an explicit flag.

**Test:**
- Implement run-id allocation and manifest writing.
- Re-run an existing iteration and confirm the manifest captures version stamps.
- Try a cross-version comparison and confirm the comparator surfaces the threshold diff.
- Try resuming a crashed run.

**Impact:** Cross-iteration comparison becomes structurally trustable. The harness becomes resumable. Retires the "default reset wipes prior work", "always-zero exit hides failures", "silent fallback to full output as rewrite", "non-atomic writes corrupt JSONs", and "no grader-version stamp invalidates cross-iteration comparison" findings in one architectural move.

## 7. Five-check gating grader plus 38-pattern advisory catalogue

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` survivor #5. Internal: `dev/research/2026-04-29-genre-paired-corpus-findings.md` shows most current gating patterns do not separate human from AI in matched register.

**Statement:** Five checks gate; the rest become advisory diagnostic context. Likely gating candidates from the existing corpus: sentence-length mean, sentence-length variance with corrected threshold, em-dashes density, paragraph-length variance, vocabulary diversity. The 38-pattern catalogue continues to surface densities without making categorical claims.

**Test:**
- Compute per-pattern length-normalised density on the corpus.
- Pick the five with non-overlapping CIs as gating.
- Re-render the audit output with five gating plus 38 advisory.
- Run the grader on a sample of human and AI prose and check whether the gating signal is sharper than the current 43-check version.

**Impact:** Threshold-tuning attention concentrates on five checks. Manufactured-insight overclaim becomes structurally impossible. Iteration baselines re-base on the gating set; the catalogue retains vocabulary-explainer value without taxonomy theatre.

## 8. Audience-aware voice via invocation surface

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` survivor #6. External: Turnitin precedent (Draft Coach for writers, Feedback Studio for instructors).

**Statement:** One engine, one registry, one corpus, one set of patterns. Voice changes by invocation surface. `/humanise audit` (reviewer voice) uses calibrated audit framing: review priority, register-X density, look-alike disambiguator. `/humanise rewrite` (writer voice) uses prescriptive framing: consider replacing with X. The registry holds twin fields and renders the right one for each surface.

**Test:**
- Add audit_voice and prescriptive_voice fields to the registry.
- Wire each surface to its voice.
- Run the same flagged passage through audit and rewrite and check the output reads coherently for the intended reader.

**Impact:** Resolves the audit / prescriptive voice mismatch without choosing one. README continues using audit voice; rewrite surface continues using prescriptive voice. Composes naturally with the single-source registry hypothesis.

## 9. Field-guide voice with similar-species disambiguation per pattern

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` worth-revisiting #1. External: Stanford HAI / TOEFL bias finding on register features misread as authorship.

**Statement:** Every pattern carries a "looks like, but isn't" block. For example, manufactured-insight: "vs legitimate epistemic hedging in academic prose; vs quoted material with attribution". The block disambiguates the pattern from genre-typical look-alikes the writer might actually be doing.

**Test:**
- Draft disambiguation blocks for the most-fired patterns.
- Add them to the audit output.
- Run the audit on prose where the pattern fires legitimately (academic hedging, attributed quotation) and check whether the disambiguator helps the reader make the right call.

**Impact:** Closes the proselint gap (no current tool does context-sensitive explanation of why a pattern correlates with AI). Addresses the Stanford HAI bias finding directly by making genre-typical look-alikes a first-class output.

## 10. Pharmacovigilance-shape user-reported false-positive intake

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` worth-revisiting #3. External: ASRS (Aviation Safety Reporting System) non-punitive intake design.

**Statement:** An opt-in `humanise report-fp` flow captures false positives the user encountered, with a non-punitive covenant (the report does not change the user's audit history). Reports grow the corpus from real authoring rather than synthetic generation.

**Test:**
- Spec the report shape (passage, pattern that fired, user's claim, optional context).
- Implement intake.
- Run for a corpus-growth window and check whether reports actually arrive and whether they meaningfully improve per-pattern calibration.

**Impact:** Unblocks corpus growth without solving sourcing or licensing for synthetic samples. Adds a feedback loop the current skill does not have. Premature today (no install path); structural fit is strong enough to revisit later.

## 11. Manufactured insight is register-coded in long-form essay

**Status:** open

**Source:** Internal: `dev/research/2026-04-29-genre-paired-corpus-findings.md` shows manufactured-insight firing 2/5 on humans and 0/5 on AI rewrites, against the pattern's catalogued severity in `humanise/references/patterns.md`.

**Statement:** The "X is not just Y, it's Z" formulation is a rhetorical move humans use deliberately in reflective essay. AI overuses it. In matched-genre corpus, the human signal is stronger than the AI signal.

**Test:**
- Grow corpus to N=15-20 per group.
- Re-run the comparative report.
- Check whether manufactured-insight still fires more on humans than AI rewrites.

**Impact:** Patterns table classification for manufactured-insight in essay register; grader severity for the pattern when document genre is essay.

## 12. Genre-aware threshold calibration

**Status:** open

**Source:** Internal: `dev/research/2026-04-29-genre-paired-corpus-findings.md` shows several patterns inverting or vanishing in long-form personal essay (markdown headings inverted, vocabulary diversity tracking length not authorship, forced-triads firing universally).

**Statement:** Pattern thresholds are register-specific. A single threshold set cannot fit both encyclopaedia register (where the catalogue largely originates) and long-form personal essay register (where the corpus tests them). Genre detection plus a per-genre threshold set is the corrective.

**Test:**
- Identify a small number of register classes (encyclopaedia, journalistic, academic, long-form essay, marketing copy).
- Compute per-pattern density per register where data allows.
- Implement a register classifier (heuristic first, learned later).
- Apply per-register thresholds and check whether the same patterns separate cleanly within their register.

**Impact:** Several currently-strong patterns reclassify per register. The grader's audit output gains a "this looks like personal essay register, applying long-form thresholds" line. Eliminates the "patterns inverted in this register" footnote that currently lives in the corpus findings.

## 13. Sentence-length mean as a grader check

**Status:** open

**Source:** Internal: `dev/research/2026-04-29-genre-paired-corpus-findings.md` reports sentence-length mean of 23.3 words (humans) vs 13.2 (AI fresh) vs 14.0 (AI rewrites), a clean separation that no current grader check captures.

**Statement:** Mean sentence length in long-form prose separates human from AI more cleanly than several current gating checks. It belongs in the grader as a register-aware check (mean-too-low against the register's human distribution).

**Test:**
- Add the check to grade.py with a register-aware threshold.
- Run on the corpus and confirm the separation holds.
- Check whether it adds gating value beyond what sentence-length variance already captures.

**Impact:** New gating check or new advisory check. Possible candidate for the five-check gating set in hypothesis 7. Strengthens the body-stats family alongside existing variance and paragraph checks.

## 14. AGENTS.md, STATUS.md, active-plan invariant, docs/solutions

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` survivor #7. Internal: PR #5 review noted project-standards reviewer returned zero findings due to absent AGENTS.md / CLAUDE.md.

**Statement:** Four conventions established together. AGENTS.md at repo root captures skill conventions (frontmatter rules, humanise vs dev separation, vocabulary source-of-truth, audit-format contract location, eval discipline). dev/STATUS.md is updated by the harness on successful runs and edited manually for strategic state. dev/plans/active.md is the only un-prefixed plan with mechanical supersession. docs/solutions/ captures generalisable learnings.

**Test:**
- Establish each convention with seed content.
- Run a future PR review and check whether project-standards reviewer returns useful findings.
- Return to the project after a 2-week gap and check whether STATUS.md absorbs the catch-up load.
- Run ce-learnings-researcher on a future ideation and check whether docs/solutions has retrievable corpus.

**Impact:** Future-Mae returning after a gap reads STATUS.md instead of reverse-engineering 11 plan / research / brainstorm docs. Future PR reviews catch convention violations automatically. Future ideations have a learnings corpus. The "which plan is canonical" question becomes a filesystem answer.

## 15. Decoupled corpus repo with SHA-pinned consumption

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` rejection #21 ("overkill at N=5; revisit at N≥50").

**Statement:** Move the corpus to a separate repo or git submodule consumed by humanise via SHA pin. Corpus growth becomes its own discipline with its own review surface. The skill repo tracks a corpus_sha rather than corpus contents.

**Test:**
- Wait until corpus reaches N≥50 per group.
- Spec the corpus repo layout (per-genre, per-source, per-author metadata).
- Migrate the existing corpus.
- Update the harness to consume by SHA.

**Impact:** Corpus and skill version histories decouple. Sourcing, licensing, and per-sample provenance get their own surface. The skill repo stops growing monotonically with corpus additions.

## 16. Multi-judge ensemble for the eval grader, with disagreement surfaced

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` rejection #22 ("premature; needs golden set first"). External: Promptfoo and Anthropic eval guidance on judge variance.

**Statement:** Run each eval through more than one judge model (or the same model with varied seeds). Surface judge disagreement as a first-class signal rather than averaging it away. Cases where judges disagree route to human review.

**Test:**
- Implement multi-judge invocation against an existing eval set.
- Compute pairwise disagreement.
- Sample disagreement cases and check whether human review consistently sides with one judge.
- Decide whether disagreement-flagged cases should gate iteration progress.

**Impact:** Eval-grader confidence becomes a measurable thing rather than an assumption. The "judge model is the oracle" premise weakens; high-disagreement cases route to human attention. Composes with the calibration golden set hypothesis.

## 17. Calibration golden set gating any grader change

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` rejection #19 ("strong but premature").

**Statement:** Maintain a hand-labelled golden set of around 30 samples covering the most contested patterns. Any change to grade.py or its thresholds must reproduce the golden-set labels within a tolerance before it ships. Acts as a regression gate.

**Test:**
- Curate the 30 samples (mix of registers, mix of human / AI authorship, mix of clear and contested cases).
- Hand-label per-pattern.
- Wire grade.py against the golden set as a CI step.
- Try a deliberate threshold change and confirm the gate flags it.

**Impact:** Grader changes stop being silent. Cross-iteration claims become reproducible. Threshold tuning gains a falsifiable acceptance test.

## 18. Discrimination metric as a release gate

**Status:** open

**Source:** Internal: `docs/ideation/2026-04-30-pr5-strategic-moves-ideation.md` rejection #23.

**Statement:** Compute a length-normalised mean discrimination metric across the catalogue, with bootstrap CI. A grader release does not ship unless the metric is at least flat against the prior version on the corpus.

**Test:**
- Define the metric (e.g., mean per-pattern Cohen's d between human and AI samples).
- Compute on the existing corpus.
- Wire as a CI gate.
- Try a release that degrades discrimination and confirm the gate blocks it.

**Impact:** Prevents iteration regressions where threshold edits chase a single metric and silently degrade others. Makes "this iteration is better" a falsifiable claim. Composes with the continuous-calibrated-score hypothesis.

## 19. Bootstrap confidence intervals on corpus claims

**Status:** open

**Source:** Internal: `dev/research/2026-04-29-genre-paired-corpus-findings.md` reports counts and means without CIs at N=5.

**Statement:** Every corpus-derived claim in research docs and in the README ships with a bootstrap CI alongside the point estimate. At N=5 per group, CIs will be wide. The point of shipping them is that the CI width is the most honest single signal of how much weight a claim can bear.

**Test:**
- Write a small bootstrap utility against the corpus statistics.
- Re-render the corpus findings doc with CIs.
- Run the same on README claims.
- Decide which point estimates are robust enough to keep, which need a CI footnote, and which should be removed entirely.

**Impact:** README and research docs gain epistemic honesty per claim. Wide CIs flag claims that should not be load-bearing. Some current headline claims may not survive contact with their own CI.
