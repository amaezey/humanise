# PR #6 README — proposed changes to resolve

Status: deferred. The audit-report worktree session on 2026-05-01 produced proposed README updates. These are NOT in PR #6's merge. They need exhaustive review against `main`'s README state before being accepted.

## Why this is post-merge work

`main` diverges from `docs/audit-report` by 78 lines on README.md (63 insertions, 15 deletions across `d76d585`, `fadeee1`, `3dbdc97` plus uncommitted edits at the time of the carve-out). The proposals below were made against the older `docs/audit-report` README — they predate the `main`-side work and cannot be merged blindly.

## What was proposed

Three structural updates, all driven by the orphan-check resolution in `13b4e9d`:

1. **Check-count strings updated** at two places (introduction paragraph and the "Patterns" section heading). `48 numbered + 3 sub-letter` → `53 numbered + 5 sub-letter`. The `49 programmatic checks` figure is unchanged — no check_id was added or removed.
2. **Pattern table extended** with `#10a` (Triad density), `#35b` (Repeated 'This …' chains), `#49` (Em dashes), `#50` (Formulaic openers), `#51` (Mechanical repeated sentence starts), `#52` (Sentence length variance), `#53` (Vocabulary diversity). Plus a candour-cluster note appended to `#42`'s example column ("the honest answer is" added as performed candour).
3. **"What's next" bullet removed** — the bullet about promoting the seven unnumbered checks is done work after `13b4e9d`.

## Open issues to address while reconciling

- **Line 11 performative candour.** The current README contains the sentence "This README is an honest account of what we found, what works, where the limits are, and what's next." That sentence matches the disliked-phrasings memory entry on performative honesty AND the candour cluster added to `no-manufactured-insight` (#42) in commit `1b58968`. The README commits the very pattern the skill now catches. Decision needed: delete, replace with a concrete pointer, or preserve with reasoning.
- **U6 README scope.** This todo covers only the 2026-05-01 proposed delta. If U6's existing README work (committed as `471a460`) also needs re-review, capture that as a separate todo or expand the scope here explicitly.
- **`main`-side README work landing on `docs/audit-report`'s successor.** If the proposed updates are still applicable after reviewing `main`'s changes, decide where they land: a follow-up PR off the merged `main`, a docs-only PR, or as part of Phase 2 of the audit-report redesign.

## Proposed diff (against `docs/audit-report` HEAD before commit `9926183`)

```diff
diff --git a/README.md b/README.md
index 7016cfe..224c542 100644
--- a/README.md
+++ b/README.md
@@ -8,7 +8,7 @@ Forked from [blader/humanizer](https://github.com/blader/humanizer), restructure
 
 People can usually tell when something was written by AI. They often can't explain why. The patterns are real — there's a body of research on stylometric markers (Kobak, Przystalski, Zaitsu, Abdulhai), a larger body of practitioner anecdata (the Wikipedia AI Cleanup project, GPTZero, Grammarly, NYT, Substack writers), and a small industry of detectors that mostly don't work.
 
-We pulled what was credible from both, turned it into 49 programmatic checks across 48 numbered patterns plus three sub-letter variants and one unnumbered meta-check, ran it on a corpus of human and AI writing, learned which checks actually distinguish the two, refined what we kept, and noted where the patterns are register-coded rather than authorship-coded. The audit is dual-layer: a deterministic regex/density grader plus an eight-item agent-judgement reading for the semantic territory regex cannot cover (structural monotony, tonal uniformity, faux specificity, neutrality collapse, even jargon distribution, forced synesthesia, generic metaphors, and a polymorphic genre slot). This README is an honest account of what we found, what works, where the limits are, and what's next.
+We pulled what was credible from both, turned it into 49 programmatic checks across 53 numbered patterns plus five sub-letter variants and one unnumbered meta-check, ran it on a corpus of human and AI writing, learned which checks actually distinguish the two, refined what we kept, and noted where the patterns are register-coded rather than authorship-coded. The audit is dual-layer: a deterministic regex/density grader plus an eight-item agent-judgement reading for the semantic territory regex cannot cover (structural monotony, tonal uniformity, faux specificity, neutrality collapse, even jargon distribution, forced synesthesia, generic metaphors, and a polymorphic genre slot). This README is an honest account of what we found, what works, where the limits are, and what's next.
 
 ## What it does
 
@@ -129,7 +129,7 @@ This is the grader's output (the regex/density layer). The agent's full Audit re
 
 ## Patterns
 
-48 numbered patterns across 8 categories, plus three sub-letter variants (23a, 31a, 35a) and one unnumbered aggregate meta-check (`overall-ai-signal-pressure`). Full before/after examples and per-pattern severity in `humanise/references/patterns.md`.
+53 numbered patterns across 8 categories, plus five sub-letter variants (10a, 23a, 31a, 35a, 35b) and one unnumbered aggregate meta-check (`overall-ai-signal-pressure`). Full before/after examples and per-pattern severity in `humanise/references/patterns.md`.
 
 | # | Pattern | Example |
 |---|---|---|
@@ -145,8 +145,10 @@ This is the grader's output (the regex/density layer). The agent's full Audit re
 | 8 | Copula avoidance | "serves as", "stands as" instead of "is" |
 | 9 | Contrived contrast / negative parallelism | "It's not X; it's Y" / "It's Y, not X" |
 | 10 | Rule of three | Forcing ideas into triads |
+| 10a | Triad density | Triad rate across 300+ words ("X, Y, and Z" stacked) |
 | 11 | Synonym cycling | "the protagonist... the main character... the central figure" |
 | 12 | False ranges | "from X to Y, from A to B" |
+| 53 | Vocabulary diversity | Low type-token ratio across 150+ words |
 | | **Style** | |
 | 13 | Boldface overuse | Mechanical bolding of terms that don't need emphasis |
 | 14 | Inline-header lists | Bolded label + colon turning prose into slides |
@@ -154,6 +156,7 @@ This is the grader's output (the regex/density layer). The agent's full Audit re
 | 16 | Emojis in professional content | Emoji-led bullet points |
 | 17 | Curly quotation marks | "..." instead of "..." |
 | 18 | Hyphenated modifier clusters | 3+ hyphenated compounds in one sentence |
+| 49 | Em dashes | "—" used as default mid-sentence punctuation in plain web prose |
 | | **Communication** | |
 | 19 | Collaborative artifacts | "I hope this helps!", "Let me know if..." |
 | 20 | Knowledge-cutoff disclaimers | "as of my last training update..." |
@@ -166,6 +169,7 @@ This is the grader's output (the regex/density layer). The agent's full Audit re
 | 25 | Staccato rhythm | Short sentences at predictable positions |
 | 47 | Soft scaffolding | "One useful area...", "The main strength..." |
 | 48 | Dense negation | Sustained "is not / does not / isn't" density across long prose |
+| 50 | Formulaic openers | "At its core,", "From a broader perspective,", "Perhaps most importantly," |
 | | **Sensory and atmospheric** | |
 | 26 | Ghost/spectral language | shadows, whispers, echoes, phantoms |
 | 27 | Quietness obsession | "quiet" 10 times in 759 words about pebbles |
@@ -177,13 +181,16 @@ This is the grader's output (the regex/density layer). The agent's full Audit re
 | 31a | Unicode flair | Decorative arrows, checkmarks, ornamental bullets |
 | 32 | Dramatic narrative transitions | "Something shifted.", "Everything changed." |
 | 38 | Section scaffolding | Identical subheadings repeated across sections |
-| 42 | Manufactured insight framing | "the real insight", "let that sink in", "what nobody is talking about" |
+| 42 | Manufactured insight framing | "the real insight", "let that sink in", "what nobody is talking about", "the honest answer is" (performed candour) |
 | 44 | Signposted conclusions | "In conclusion,", "Key takeaways:", "Final thoughts:" |
+| 52 | Sentence length variance | Most sentences land in a similar word-count band across longer prose |
 | | **Voice and register** | |
 | 33 | Countdown negation | "It wasn't X. It wasn't Y. It was Z." |
 | 34 | Per-paragraph miniature conclusions | Every paragraph wraps up neatly |
 | 35 | Tonal uniformity / register lock | One register throughout, no human drift |
 | 35a | Orphaned demonstratives | "This highlights...", "That underscores..." |
+| 35b | Repeated 'This …' chains | 3+ consecutive sentences starting with "This [verb]" |
+| 51 | Mechanical repeated sentence starts | 3+ consecutive sentences with the same first word (anaphora without escalation) |
 | 36 | Faux specificity | "The smell of coffee on a Sunday morning", specific to nobody |
 | 37 | Neutrality collapse | Stripping the author's stance, defaulting to balanced |
 | 39 | Template and placeholder residue | `{client_name}`, `[Company Name]`, "Hi {name}" |
@@ -228,7 +235,6 @@ Active work, tracked in `docs/plans/`:
 - **Calibrating thresholds by register** (literary essay vs corporate doc vs news copy).
 - **Demoting pattern checks that don't separate humans from AI** in matched genres (em dashes, manufactured insight, triad density may belong in softer categories — explicitly out of scope for the active plan; tracked separately).
 - **Growing the matched corpus past N=5 per group.**
-- **Promoting the seven unnumbered checks** (`no-em-dashes`, `no-formulaic-openers`, `no-anaphora`, `sentence-length-variance`, `no-this-chains`, `no-triad-density`, `vocabulary-diversity`) to numbered patterns or explicit folds — currently documented in the "Severity for unnumbered checks" subsection of `humanise/references/patterns.md`.
 
 ## File structure
```

## Where the proposed changes live in git

Equivalent diff regenerable from reflog at the time this todo was written:

```bash
git diff 9926183~1..9926183 -- README.md
```

Commit `9926183` is reachable from `docs/audit-report` reflog as of 2026-05-01 16:04. If the reflog is pruned before this todo is resolved, the diff verbatim above is the canonical artifact.

## Acceptance criteria

This todo is resolved when:

- README check counts and pattern table reflect the actual catalogue state (currently 49 checks across 53 numbered + 5 sub-letter entries after `13b4e9d`).
- Line 11 is either deleted, replaced with a concrete pointer, or preserved with explicit reasoning written down.
- `main`-side README work is reconciled with `docs/audit-report`-side work cleanly.
- Any remaining proposed updates land in a follow-up PR or are explicitly dropped.
