# Performance report — iteration-4

Run timestamp: 2026-04-29T13:09:33Z
Evals run: 18
Mean pass rate: 95.5%

## Per-eval pass rates

| ID | Name | Pass rate | Runs |
|---|---|---|---|
| 0 | audit-ai-cultural | 100.0% | 1 |
| 1 | audit-human-reflective-essay | 83.3% | 1 |
| 2 | audit-human-literary | 100.0% | 1 |
| 3 | suggestions-ai-wellbeing | 100.0% | 1 |
| 4 | rewrite-balanced-tech | 100.0% | 1 |
| 5 | rewrite-balanced-personal | 100.0% | 1 |
| 6 | rewrite-all-science | 85.7% | 1 |
| 7 | write-balanced-brief | 100.0% | 1 |
| 8 | audit-human-image-first-men-original-sins | 100.0% | 1 |
| 9 | audit-human-opencoop-belonging-superpower | 100.0% | 1 |
| 10 | audit-human-fortelabs-servant-hedonism | 100.0% | 1 |
| 11 | audit-human-critchlow-workshops | 83.3% | 1 |
| 12 | audit-human-tuckermax-mdma-therapy | 100.0% | 1 |
| 13 | audit-ai-fresh-belonging-superpower | 100.0% | 1 |
| 14 | audit-ai-fresh-workshops-as-portals | 83.3% | 1 |
| 15 | audit-ai-fresh-mdma-therapy | 100.0% | 1 |
| 16 | audit-ai-fresh-servant-hedonism | 83.3% | 1 |
| 17 | audit-ai-fresh-first-men-original-sins | 100.0% | 1 |

## Human-vs-AI flag baseline

Grader output on the genre-paired corpus (see `dev/evals/corpus.json`). Three groups: human originals, AI fresh-writes from matched-topic prompts, and AI-rewrites of the human originals. Deterministic — independent of how the skill renders its audit.

| Sample | Group | Total | Strong | Context | AI-pressure |
|---|---|---|---|---|---|
| 21c-image-first-men-original-sins | human | 7 | 2 | 5 | — |
| 21c-opencoop-belonging-superpower | human | 4 | 1 | 3 | — |
| 21c-fortelabs-servant-hedonism | human | 7 | 1 | 6 | triggered |
| 21c-critchlow-workshops | human | 9 | 1 | 8 | triggered |
| 21c-tuckermax-mdma-therapy | human | 13 | 4 | 9 | triggered |
| 21c-ai-belonging-superpower | ai_fresh | 7 | 2 | 5 | — |
| 21c-ai-workshops-as-portals | ai_fresh | 7 | 1 | 6 | — |
| 21c-ai-mdma-therapy | ai_fresh | 9 | 2 | 7 | triggered |
| 21c-ai-servant-hedonism | ai_fresh | 7 | 1 | 6 | — |
| 21c-ai-first-men-original-sins | ai_fresh | 12 | 4 | 8 | triggered |
| 21c-ai-rewrite-belonging-superpower | ai_rewrite | 3 | 1 | 2 | — |
| 21c-ai-rewrite-workshops-as-portals | ai_rewrite | 6 | 1 | 5 | — |
| 21c-ai-rewrite-mdma-therapy | ai_rewrite | 8 | 3 | 5 | — |
| 21c-ai-rewrite-servant-hedonism | ai_rewrite | 9 | 4 | 5 | triggered |
| 21c-ai-rewrite-first-men-original-sins | ai_rewrite | 9 | 4 | 5 | triggered |

**Group means:**

| Group | n | Total | Strong | Context |
|---|---|---|---|---|
| human | 5 | 8.0 | 1.8 | 6.2 |
| ai_fresh | 5 | 8.4 | 2.0 | 6.4 |
| ai_rewrite | 5 | 7.0 | 2.6 | 4.4 |
| Gap (ai_fresh vs human) | | +5% | +11% | +3% |
| Gap (ai_rewrite vs human) | | -12% | +44% | -29% |

## Body-level statistics

Sentence/paragraph length variance is the strongest non-pattern signal separating humans from AI in long-form essay register (humans cluster around longer, more variable sentences; AI clusters around shorter, more uniform ones). Tracked across iterations to surface drift even when pattern flags don't move.

| Group | n | Words | Sent. mean | Sent. stdev | Para. stdev | TTR |
|---|---|---|---|---|---|---|
| human | 5 | 3568 | 23.3 | 17.1 | 37.3 | 0.33 |
| ai_fresh | 5 | 1849 | 13.2 | 7.3 | 23.2 | 0.40 |
| ai_rewrite | 5 | 1126 | 14.0 | 7.5 | 21.4 | 0.50 |

## Audit fidelity

How faithfully the skill's audit surfaces patterns the grader found. Lower fidelity means the audit is suppressing flags the grader caught.

| Eval | Type | Grader | Audit reported | Fidelity |
|---|---|---|---|---|
| audit-ai-cultural | ai | 10 | 10 | 100% |
| audit-human-reflective-essay | human | 6 | 6 | 100% |
| audit-human-literary | human | 7 | 7 | 100% |
| audit-human-image-first-men-original-sins | human | 7 | 6 | 86% |
| audit-human-opencoop-belonging-superpower | human | 4 | 4 | 100% |
| audit-human-fortelabs-servant-hedonism | human | 7 | 6 | 86% |
| audit-human-critchlow-workshops | human | 9 | 8 | 89% |
| audit-human-tuckermax-mdma-therapy | human | 13 | 12 | 92% |
| audit-ai-fresh-belonging-superpower | ai_fresh | 7 | 7 | 100% |
| audit-ai-fresh-workshops-as-portals | ai_fresh | 7 | 7 | 100% |
| audit-ai-fresh-mdma-therapy | ai_fresh | 9 | 9 | 100% |
| audit-ai-fresh-servant-hedonism | ai_fresh | 7 | 8 | 114% |
| audit-ai-fresh-first-men-original-sins | ai_fresh | 12 | 12 | 100% |

## Regression vs previous iteration

Advisory only — flagged for review when an eval's pass rate dropped >5%.

| Eval | Prev | This | Δ | Regressed? |
|---|---|---|---|---|
| audit-ai-cultural | 83.3% | 100.0% | +16.7% | — |
| audit-human-reflective-essay | 100.0% | 83.3% | -16.7% | yes |
| audit-human-literary | 100.0% | 100.0% | +0.0% | — |
| suggestions-ai-wellbeing | 100.0% | 100.0% | +0.0% | — |
| rewrite-balanced-tech | 100.0% | 100.0% | +0.0% | — |
| rewrite-balanced-personal | 100.0% | 100.0% | +0.0% | — |
| rewrite-all-science | 71.4% | 85.7% | +14.3% | — |
| write-balanced-brief | 100.0% | 100.0% | +0.0% | — |
| audit-human-image-first-men-original-sins | 100.0% | 100.0% | +0.0% | — |
| audit-human-opencoop-belonging-superpower | 100.0% | 100.0% | +0.0% | — |
| audit-human-fortelabs-servant-hedonism | 100.0% | 100.0% | +0.0% | — |
| audit-human-critchlow-workshops | 100.0% | 83.3% | -16.7% | yes |
| audit-human-tuckermax-mdma-therapy | 83.3% | 100.0% | +16.7% | — |
| audit-ai-fresh-belonging-superpower | 100.0% | 100.0% | +0.0% | — |
| audit-ai-fresh-workshops-as-portals | 100.0% | 83.3% | -16.7% | yes |
| audit-ai-fresh-mdma-therapy | 83.3% | 100.0% | +16.7% | — |
| audit-ai-fresh-servant-hedonism | 83.3% | 83.3% | +0.0% | — |
| audit-ai-fresh-first-men-original-sins | 83.3% | 100.0% | +16.7% | — |
