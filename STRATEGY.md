---
name: humanise
last_updated: 2026-05-03
---

# humanise Strategy

## Target problem

People are increasingly expected to use AI for workplace writing, then left with prose that feels wrong but is hard to diagnose or repair. The hard part is that the damage is usually cumulative: small tells stack across voice, rhythm, structure, and phrasing until the writing reads as synthetic, even when no single sentence is obviously broken.

## Our approach

humanise treats the signs of AI writing as craft patterns a writer can inspect. It combines deterministic checks with agent judgement grounded in research, examples, and eval evidence. It uses that evidence to show what is happening in the draft, why the accumulated effect matters, and what to change without sanding off the writer's voice.

## Who it's for

**Primary:** People editing AI-assisted writing. They're using humanise to find the patterns that make a draft feel synthetic, judge which ones actually weaken the piece, and revise without flattening the writer's voice.

## Key metrics

- **Rewrite quality** - Post-rewrite text has fewer high-severity flags without introducing new AI-writing tells; measured in benchmark runs and review samples.
- **False-positive rate on human writing** - Strong human prose should not be flattened into "AI-looking" failure just because it uses valid rhetorical moves; measured against matched human corpus samples and review fixtures.
- **Human-vs-AI signal gap** - Matched AI samples trigger meaningfully more pressure than matched human samples; measured in the eval suite.
- **Regression rate** - Benchmark runs do not lose coverage on known failure cases; measured in iteration reports.
- **Report usefulness / actionability** - Users can tell what to change from the audit without needing extra explanation; aspirational while humanise is a skill, measurable if it later becomes a plugin with feedback capture.

## Tracks

### Validate the pattern catalogue

Ground AI-writing tells in research, examples, and corpus evidence.

_Why it serves the approach:_ The skill only works if the patterns are inspectable and defensible rather than vibes dressed up as detection.

### Improve deterministic checks

Make regex, density, and pressure checks catch real patterns without over-flagging human prose.

_Why it serves the approach:_ Deterministic checks give the audit structure, repeatability, and a way to measure change across rewrites and evals.

### Clarify judgement and reports

Make both the agent judgement layer and the final audit output understandable, evidence-led, and useful to someone deciding what to change.

_Why it serves the approach:_ The report is where pattern evidence becomes an editing decision, so it has to be readable without hiding uncertainty.

### Protect rewrite quality

Revise flagged prose without flattening voice or adding new AI tells.

_Why it serves the approach:_ The product should help writers repair the draft in front of them, not replace it with another synthetic voice.
