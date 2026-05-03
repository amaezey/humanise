# TODO: Add performative-direct fragments to the audit catalogue

**Status:** open todo. Captured during U6 of the audit-output redesign; not actioned in this plan.
**Date:** 2026-05-03.

---

## What

Add a check for **performative-direct fragments**: short, choppy sentence-fragments used to feel punchy and decisive. Examples:

- "Regex can't."
- "Both sides win."
- "Ship it."
- "No filler."
- "End of story."

The fragment is meant to read terse-and-decisive but reads as staccato performance. AI writing leans on this constantly because it sounds punchy without committing to a full thought.

## Why this is an AI tell

Real directness is a complete sentence with no filler. The clipped fragment substitutes performance for substance — there's a verb implied but not written, so the line carries authority without taking a position. AI models reach for this shape because it pattern-matches "confident".

Mae has flagged this multiple times across sessions. It's already in the disliked-phrasings memory; this todo proposes adding it to the audit catalogue so the script can catch it at audit time.

## Where it could live

Two plausible homes — implementer should pick during the unit that adds it:

1. **Auto-detected (`humanise/scripts/patterns.json`)** — a regex/structural check that flags high density of very short sentence-fragments (e.g. ≥2 sentences under 5 words in a row that lack a finite verb). Hard part: distinguishing intentional staccato style from performative-direct AI shape. May produce false positives in human prose with deliberate short rhythm.
2. **Agent-assessed (`humanise/scripts/judgement.json`)** — an LLM-judged tell with a prompt like "Does the draft use short sentence-fragments to feel punchy? List any fragments that read as performative rather than load-bearing." This is the safer home; the model can read intent, regex cannot.

Recommendation: agent-assessed first. If it works well, consider whether a regex prefilter would catch the obvious cases.

## Severity

Likely `strong_warning`. The pattern is high-signal AI when present but isn't a hard fail (some human prose uses fragments deliberately for rhythm).

## Sources

- Mae's session feedback (this session, 2026-05-03): "fragments; clear ai tell ▎ A model reads for these. Regex can't." flagging my own draft of agent-assessed brief-note copy.
- `feedback_disliked_phrasings.md` (auto-memory): performative-direct-fragments entry added in this session.
