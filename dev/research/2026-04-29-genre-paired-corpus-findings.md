# Genre-paired corpus findings — long-form first-person essay

Date: 2026-04-29
Status: documented for follow-up after iteration 3

A genre-controlled comparison run on 5 human + 5 AI-fresh-write + 5 AI-rewritten essays, all in the long-form first-person essay register (literary review, practitioner blog, business memo, personal philosophy, confessional memoir).

The fresh-writes were generated from prompts mirroring the human essay topics; the rewrites were AI-rewrites of the human originals. Matched-pair design.

## Corpus

| Slug | Topic | Human source | AI fresh | AI rewrite |
|---|---|---|---|---|
| belonging-superpower | Workshop write-up on decentralised organising | `21c-opencoop-belonging-superpower` | `21c-ai-belonging-superpower` | `21c-ai-rewrite-belonging-superpower` |
| workshops-as-portals | Practitioner essay on selling workshops | `21c-critchlow-workshops` | `21c-ai-workshops-as-portals` | `21c-ai-rewrite-workshops-as-portals` |
| servant-hedonism | Personal-philosophy blog post | `21c-fortelabs-servant-hedonism` | `21c-ai-servant-hedonism` | `21c-ai-rewrite-servant-hedonism` |
| first-men-original-sins | Literary review-essay (faith + spaceflight) | `21c-image-first-men-original-sins` | `21c-ai-first-men-original-sins` | `21c-ai-rewrite-first-men-original-sins` |
| mdma-therapy | Confessional memoir on MDMA-assisted therapy | `21c-tuckermax-mdma-therapy` | `21c-ai-mdma-therapy` | `21c-ai-rewrite-mdma-therapy` |

Prompts used: `dev/evals/genre-paired-personal-essay-prompts.md`.

## Headline finding

**The grader's existing strong-signal patterns do not distinguish humans from AI in this genre.**

| Group | Mean total flags | Mean strong | Mean context |
|---|---|---|---|
| Humans (n=5) | 8.0 | **1.8** | 6.2 |
| AI fresh-write (n=5) | 8.4 | **2.0** | 6.4 |
| AI rewrite (n=5) | 7.0 | **2.6** | 4.4 |

AI rewrites trigger *more* strong-signal hits than humans (2.6 vs 1.8). The "strong AI signal" classification is calibrated to the obvious tells of unsophisticated AI prose; on careful long-form essay output it gives the same readings as on humans writing in the same register.

## Mae's reframe (load-bearing)

> The strong stuff is actually things that have become culturally 'AI' tells because they are valid forms of writing but when applied by AI as a blunt instrument they come off as AI. They're fine when done well, but glaringly bad when not. Reframe the narrative around that — these are things to **re-examine as a priority**.

This reframes the skill's voice from *"this is AI, fix it"* to *"this is a high-risk pattern; verify it's working in your context."* It changes:

- **Audit output**: replace "AI tell" with "high-risk pattern" or "review priority"
- **Patterns documentation**: each strong pattern needs framing as "valid technique that breaks when overused / under-grounded"
- **Severity model**: maybe collapse the strong-vs-context distinction into "review priority" + "context flag" with the priority bar based on density and grounding, not pattern membership

### Important corollary: rewrite policy is NOT the same as audit framing

The reframe applies to how the *audit* speaks to a human writer. **It does not loosen the rewrite policy.** Even though humans can use these patterns well, AI can't do them well — when the skill itself is rewriting (Balanced or All depth), it should still limit their use to compensate for AI's tendency to overuse.

Two audiences, two instructions:

1. **Audit voice to human writer**: "Review these as priorities — they're valid moves, but easy to do badly. Keep them only if you've earned them."
2. **Rewrite policy when AI executes**: "Still strip / reduce these by default. AI does these badly. The Balanced rewrite should remain conservative on em dashes, triads, manufactured insight, etc., even though a human writer using the same patterns would be fine."

This split keeps the audit honest (humans don't get scolded for using legitimate techniques) without giving the AI rewriter permission to mimic them (because it'll get them wrong).

## What actually separates humans from AI in this corpus

Body-level statistics produce the cleanest signal. Means across each group of 5:

| Metric | Human | AI fresh | AI rewrite |
|---|---|---|---|
| Word count | 3,568 | 1,849 | 1,126 |
| Sentence length, mean (words) | **23.3** | 13.2 | 14.0 |
| Sentence length, stdev | **17.0** | 7.3 | 7.5 |
| Paragraph length, stdev (words) | **37.3** | 23.2 | 21.4 |
| Type-token ratio | 0.33 | 0.40 | 0.50 |
| Em dashes (count) | 15.0 | 11.8 | 11.2 |
| Curly quotes | 105.6 | 48.4 | 29.8 |

The strongest single separator: **sentence-length variance**. Humans 17.0 stdev vs AI 7.3 — a 2.3× gap. AI clusters tightly around a 13-word mean; humans cluster around 23 words with much wider variance.

**Sentence-length variance is currently a grader check, but in practice it's not catching the gap reliably** — the threshold and computation may need genre-aware tuning. At minimum, *mean* sentence length (not just variance) is worth tracking as its own signal.

## Pattern fire-rate differences (which patterns fire on which group, of 5 each)

Patterns where fire rates differ by ≥2/5 across groups:

| Pattern | Severity | Hum | Fresh | Rewrite | Reading |
|---|---|---|---|---|---|
| no-anaphora | context | 2 | **4** | 3 | AI uses repeated sentence starts more |
| no-em-dashes | strong | 2 | 4 | **5** | AI rewrites lean on em dashes; humans use them too |
| no-forced-triads | context | **3** | 0 | 1 | Triads are a *human* signal in this genre |
| no-ghost-spectral-density | context | 0 | **2** | 0 | AI-fresh-only signal — possible new tell |
| no-manufactured-insight | strong | **2** | 1 | 0 | Currently classed as AI; fires more on humans here |
| no-markdown-headings | context | **5** | 1 | 3 | Inverted — humans use markdown headings (blog convention) |
| no-negation-density | context | 0 | **2** | 0 | AI-fresh-only — possible new tell |
| no-triad-density | context | 5 | 5 | 3 | Universal genre signal, not AI-specific |
| no-unicode-flair | context | 0 | **2** | 0 | AI-fresh-only (e.g., "⸻" separators) — possible new tell |
| vocabulary-diversity | context | 3 | 2 | 0 | Long-form humans repeat words; not AI-specific |

## New tell candidates

1. **Mean sentence length** (~13 vs ~23 words). Humans write longer sentences. Not currently a grader check.
2. **Sentence-length variance** — already a check, but the threshold and computation need genre-aware tuning. The 2.3× gap here isn't being caught reliably.
3. **Paragraph-length variance** — same story. 1.6× gap (37 vs 22).
4. **Ghost/spectral density, negation density, unicode flair** — each fires only on AI-fresh in this corpus. Currently context_warning; might warrant promotion or be combined into a "subtle AI register" composite signal.

## Patterns that should be demoted or recategorised

Based on this genre-paired data, several existing "strong" or universally-firing patterns are not separating humans from AI:

- **Em dashes (strong)** — fires across all three groups; in published long-form essay this is convention, not a tell. Possibly demote to context, or only flag at high density.
- **Manufactured insight (strong)** — fires more on humans (2/5) than AI rewrites (0/5). The pattern matcher may be picking up legitimate first-person insight framing.
- **Forced triads, triad density (context)** — universal in this register. Both human and AI fire 5/5 on triad-density. The pattern itself is genre-typical.
- **Markdown headings (context)** — fires 5/5 on humans, 1/5 on AI fresh. *Inverted* signal in long-form blog/practitioner essay. The check may be calibrated for academic/journalistic prose where headings are AI tells; for this genre it's a human convention.
- **Vocabulary diversity (context)** — long-form humans naturally have lower TTR. The check may be triggering on essay length, not AI authorship.

## Caveats

- n=5 per group. Findings are directional; need larger N before being baked into the grader.
- AI fresh-writes in this corpus are short relative to the human originals (1,849 mean vs 3,568). Some of the variance differences may be partly length-driven.
- "AI rewrite" set was generated by an unspecified model; results may shift with a different rewriter.
- The genre is heterogeneous within "essay" (literary review, business memo, confessional, philosophical, practitioner). Findings are register-level claims, not single-genre claims.

## What's queued

After iteration 3 (which validates the comparative-report harness end-to-end on this corpus), the follow-up work is:

1. **Reframe audit voice** in SKILL.md and grade.py's report templates: "AI tell" → "high-risk pattern" / "review priority" — Mae's takeaway above.
2. **Recalibrate or demote patterns** that don't separate humans from AI in this register: em dashes, manufactured insight, triad density, markdown headings, vocabulary diversity.
3. **Add new checks** for the AI-fresh-only signals: ghost-spectral-density, negation-density, unicode-flair, mean-sentence-length.
4. **Genre-aware thresholds** — possibly let the audit pre-classify the input register (literary essay vs journalism vs technical) and adjust which patterns fire as which severity.
5. **Larger N** — extend the matched-pair corpus to ≥10 per group to strengthen statistical claims.
