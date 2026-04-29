# Humanise Rewrite and Write Process

This file is required for Rewrite and Write actions. Use it as the operating
procedure after the audit has identified patterns and before returning prose.

## Step A: Structural Pass

Do this before changing surface wording.

1. Identify the current paragraph rhythm.
   - Count paragraphs.
   - Notice whether most paragraphs are similar length.
   - Notice whether paragraphs end with tidy summaries.
   - Notice whether sections follow the same arc: setup, explanation, moral.

2. Break repeated arcs.
   - Turn one explanatory paragraph into a short direct paragraph.
   - Merge two thin paragraphs when they repeat the same movement.
   - Split a long paragraph when it contains a turn, example, or qualification.
   - Let some paragraphs end on concrete detail rather than a summary sentence.

3. Vary sentence rhythm.
   - Keep some short sentences if they carry stance or timing.
   - Add longer sentences only when they carry specific detail, not padding.
   - Avoid several paragraphs with the same medium-length explanatory cadence.

4. Reduce list cadence.
   - Cut decorative triads.
   - Break long inventories into prose when the list is only rhythm.
   - Preserve lists when accumulation is the point, but say so in the self-check.

5. Remove reframe laundering.
   - Replace "not X but Y", "less X than Y", "beyond X", and similar reveal
     structures with direct claims.
   - Keep ordinary factual contrast when it is needed for meaning.

## Step B: Surface Pass

After structure is fixed, remove required surface tells for the chosen depth.

Balanced must fix hard failures and strong warnings:
- assistant residue
- generic conclusions
- placeholder residue
- manufactured insight
- false concession hedges
- formulaic openers
- signposted conclusions
- contrived contrast
- AI vocabulary clusters
- soft scaffolding
- excessive hedging
- em dashes unless preserving them is explicitly justified by voice

All must also fix context warnings unless meaning would materially change.

Use `references/alternatives.md` for lexical substitutions when the issue is a
word or stock phrase. Do not use substitutions for structural problems; rewrite
the sentence or paragraph instead.

## Step C: Structural Self-Check

Before returning, answer the eight self-check fields in the output template.
Be concrete. Do not claim a pattern was fixed unless the draft changed in a way
the reader can see.

1. Section arcs: count how many paragraphs or sections still follow the same arc.
2. Resolution density: count tidy summary endings that remain.
3. Register breaks: name at least one place where rhythm, register, or sentence
   shape breaks the default smoothness.
4. Triads: count obvious three-part lists and state what was cut or preserved.
5. Reframe laundering: state whether contrived contrast remains.
6. Purposeful devices preserved: list devices kept because they serve meaning.
7. Stance: state whether the rewrite preserved, weakened, or strengthened stance.
8. Remaining tells: list remaining failed checks, or say none.

## Step D: Semantic Preservation

Compare the rewrite or draft against the brief or source before returning.

For Rewrite:
- Preserve the source argument, examples, stance, and genre.
- Preserve factual claims unless the original claim is unclear or unsupported.
- Do not make a writer more neutral just to sound clean.
- Do not remove a distinctive device if removing it would flatten the voice;
  disclose the preservation instead.

For Write:
- Answer the brief directly.
- Include concrete sensory, practical, or argumentative detail.
- Avoid generic essay structure unless the user asked for it.

## Step E: Re-Grade and Revise

Run the grader or equivalent check after the final draft.

If the chosen depth has required failures:
1. Revise the draft before returning.
2. Re-grade after the revision.
3. Repeat up to two revision passes.

Stop with residual issues only when:
- the issue is deliberately preserved for voice or meaning, or
- removing it would materially change the source, or
- two revision passes have failed to clear it.

When residual issues remain, name them plainly in the post-check. Do not say
"none identified" if the grader still reports required failures.
