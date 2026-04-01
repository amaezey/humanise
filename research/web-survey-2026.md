# Web Survey: Signs of AI Writing (April 2026)

**Method:** Web search across academic, journalistic, and practitioner sources
**Date:** 1 April 2026
**Focus:** Identifying patterns not already captured in existing humanise research

---

## Source 1: Nature — "Signs of AI-generated text found in 14% of biomedical abstracts"

**Source:** https://www.nature.com/articles/d41586-025-02097-6
**Published:** 2025
**Type:** Science journalism (reporting on peer-reviewed research)

### Key findings

- ~200,000 out of 1.5 million PubMed-indexed abstracts in 2024 contained LLM-characteristic vocabulary. That's roughly **1 in 7** biomedical abstracts.
- Up to **22% of computer science papers** show signs of LLM input.
- Telltale words in abstracts include **"unparalleled"** and **"invaluable"** — words that are common in LLM output but statistically rare in human academic writing.
- Researchers using generative AI are publishing more papers, but there's been a **~55% increase in objective mistakes** in NeurIPS submissions between 2021 and 2025.
- Different LLM versions leave distinct vocabulary traces over time:
  - GPT-4 era: "tapestry", "pivotal", "meticulous", "testament"
  - GPT-4o era: "align with", "enhance", "showcasing"
  - "Delve" peaked in 2023–early 2024, declined through 2024, dropped sharply by 2025

### New patterns for humanise

| Pattern | Status vs existing list |
|---|---|
| "Unparalleled" and "invaluable" as AI vocabulary | **New vocabulary items** — not in current 37+ list |
| Vocabulary shifts across model versions (temporal fingerprinting) | **New concept** — models have era-specific tells |
| Increased factual error rate correlated with AI use | Reinforces existing "vague attributions" pattern but adds quantitative evidence |

---

## Source 2: Stylometry research — multiple papers on LLM fingerprinting

**Sources:**
- https://arxiv.org/abs/2507.00838 — "Stylometry recognizes human and LLM-generated texts in short samples" (Przystalski et al., 2025)
- https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0335369 — "Stylometry can reveal AI authorship" (Zaitsu et al., PLOS ONE, 2025)
- https://arxiv.org/abs/2506.17323 — "I Know Which LLM Wrote Your Code Last Summer" (Bisztray et al., ACM AISec, 2025)

**Type:** Peer-reviewed / preprint academic research

### Key findings

- **Stylometric features reliably distinguish LLM text from human text** even in short (10-sentence) samples: up to .87 MCC in 7-class attribution, .98 accuracy in binary classification.
- The Japanese study (Zaitsu et al.) achieved **perfect discrimination** between human and LLM text using three integrated stylometric features: phrase patterns, part-of-speech bigrams, and function word unigrams.
- Only **Llama 3.1 showed distinct characteristics** compared with the other six LLMs tested — most commercial models cluster together stylistically.
- In code stylometry, **removing comments dropped accuracy from 92.65% to 85.45%**, showing comment phrasing is the richest stylometric feature for model attribution.
- Researchers propose the concept of **stylometric watermarks**: models consistently favouring unusual sentence structures or specific synonyms, creating differences too subtle for readers but statistically detectable.

### New patterns for humanise

| Pattern | Status vs existing list |
|---|---|
| Function word distribution (the, of, and, etc.) differs between AI and human text | **New signal** — not surface vocabulary but statistical distribution |
| Part-of-speech bigram patterns (e.g., adjective-noun frequency) | **New signal** — grammatical sequencing differs |
| Most commercial LLMs cluster together stylistically (except Llama) | **New insight** — detection may work better as human-vs-AI than model-vs-model |
| Comment/aside phrasing is the richest attribution signal in code | **New insight** — relevant if humanise is ever applied to technical writing |

---

## Source 3: Cross-source consensus from practitioner guides (2025–2026)

**Sources:**
- https://www.aidetectors.io/blog/how-to-tell-if-text-is-ai-written (2026)
- https://seoengine.ai/blog/signs-of-ai-writing (2025–2026)
- https://www.sagepub.com/explore-our-content/blogs/posts/sage-perspectives/2025/06/11/ai-detection-for-peer-reviewers-look-out-for-red-flags (SAGE, 2025)

**Type:** Practitioner/industry guides

### Key findings

- **Tricolon obsession** — AI groups ideas in threes compulsively ("Clear, concise, and actionable"). Human writers break this constantly, using two, four, or seven items. This reinforces existing pattern #10 (rule of three) but the "nearly every enumeration" framing makes it more specific.
- **Low type-token ratio** — AI recycles high-probability terms, producing measurably lower vocabulary diversity than human writers. Psycholinguists track this as unique-words ÷ total-words.
- **Even jargon distribution** — humans clump technical jargon in one paragraph then switch to plain English. AI disperses jargon uniformly throughout.
- **Tonal uniformity** — AI picks a register (professional-casual, academic-accessible) and stays there. Human writers drift between registers, get colloquial, throw in jokes that don't land. The consistency is the tell.
- **Faux specificity** — AI provides examples that feel specific without actually being specific. It "gestures at the specific while remaining safely abstract, constructing plausible-sounding examples from genre conventions rather than lived experience."
- **Present participial constructions** — instruction-tuned models use "main clause + comma + -ing verb phrase" at **2–5× the rate** of human writing.
- **Miniature conclusions per paragraph** — every paragraph ends with a summary that hands off perfectly to the next. Humans occasionally jump, digress, or foreshadow clumsily.
- **Dramatic countdown negation** — AI negates two or more things before revealing the actual point, creating false suspense: "It wasn't the data. It wasn't the model. It was the prompt."
- **Heavy AI users spot AI text ~90% of the time**; light users do barely better than a coin flip.
- **3+ converging indicators** is the practical threshold for suspicion — no single sign is reliable alone.
- **15% of Reddit posts** are now estimated to be AI-generated.
- **21% of ICLR 2026 reviews** were written entirely by AI.

### New patterns for humanise

| Pattern | Status vs existing list |
|---|---|
| Even jargon distribution (vs human clumping) | **New** — structural pattern not in current list |
| Low type-token ratio / vocabulary recycling | **New** — measurable signal, not currently tracked |
| Tonal uniformity / locked register | **New** — related to but distinct from existing "sycophantic tone" |
| Faux specificity ("gestures at the specific") | **Reinforces** existing "experiential vacancy" but names the mechanism more precisely |
| Participial construction overuse (2–5× rate) | **Partially covered** by pattern #3 (superficial -ing analyses) but broader |
| Per-paragraph miniature conclusions | **New** — structural pattern not in current list |
| Dramatic countdown negation | **New** — rhetorical pattern not in current list |
| "Unparalleled", "invaluable", "bolstered", "fostering", "showcasing" as AI vocabulary | **New vocabulary items** for the word list |

---

## Summary: Strongest candidates for new patterns

Patterns that are genuinely new (not reinforcing existing ones) and have strong cross-source support:

1. **Even jargon distribution** — humans clump, AI spreads evenly. Multiple sources confirm.
2. **Per-paragraph miniature conclusions** — every paragraph wraps up neatly and transitions perfectly. Distinct from overall structural rigidity.
3. **Tonal uniformity / register lock** — picking one tone and never breaking from it. Distinct from sycophancy.
4. **Dramatic countdown negation** — "It wasn't X. It wasn't Y. It was Z." Distinct from existing negative parallelism (#9).
5. **Low type-token ratio** — measurable vocabulary recycling. Complements existing synonym cycling (#11) but is the inverse problem (too few unique words rather than too many synonyms for one concept).
6. **Temporal vocabulary fingerprints** — specific AI words rise and fall with model versions. Relevant for keeping the vocabulary list current.

### New vocabulary items to consider adding

- unparalleled
- invaluable
- bolstered
- fostering
- showcasing
- align with
- enhance (in the "enhance X" construction)

---

## Source 4: "How LLMs Distort Our Written Language" (Abdulhai et al., March 2026)

**Source:** https://arxiv.org/abs/2603.18161
**Authors:** Marwa Abdulhai, Isadora White, Yanming Wan, Ibrahim Qureshi, Joel Z. Leibo, Max Kleiman-Weiner, Natasha Jaques (UC Berkeley, UCSD, UW, Google DeepMind)
**Published:** 18 March 2026
**Type:** Peer-reviewed research (arXiv + OpenReview)
**Companion site:** https://sites.google.com/view/llmwritingdistortion/home
**Code:** https://github.com/abdulhaim/llm_writing_distortion

### Study design

Three evaluation settings:

1. **Randomised controlled trial** — participants wrote argumentative essays with or without LLM access
2. **ArgRewrite counterfactual** — 86 human-written essays (collected 2021, pre-ChatGPT) with expert feedback; compared human revisions to revisions by GPT-5-mini, Gemini-2.5-Flash, and Claude-3.5-Haiku
3. **ICLR 2026 review analysis** — 18,000 peer reviews; 21% found to be LLM-generated

### Key findings

**Neutrality collapse**
- Extensive LLM use led to a **~70% increase** in essays that remained neutral rather than taking a for/against position.
- LLMs systematically remove content making particular claims, editing essays to be more neutral or positive.
- Even when instructed to only fix grammar, LLMs frequently changed the writer's conclusions.

**Voice and creativity loss**
- Heavy LLM users reported writing was **less creative** and **not in their voice**.
- Essays had **50% fewer pronouns**, representing a shift toward impersonal language with fewer anecdotes and references to human experiences.
- LLMs use both more emotional *and* more argumentative language than human editors — but paradoxically strip out the author's actual argument.

**The paradox of preferences**
- Users who heavily relied on LLMs reported **similar satisfaction** with their output despite acknowledging it was less creative and less in their voice. People like the polish even as it erases them.

**Semantic distortion even in minimal edits**
- LLM edits meaningfully alter semantics even when tasked with only grammar corrections. The intended meaning shifts, not just the style.
- LLM revisions are structurally very different from how humans revise the same text given the same feedback.

**Peer review distortion (ICLR 2026)**
- 21% of reviews were LLM-generated.
- AI reviews systematically **deprioritised clarity and relevance** while over-emphasising reproducibility and scalability.
- AI reviews assigned scores **a full point higher on average** — an inflationary bias.

### New patterns for humanise

| Pattern | Status vs existing list |
|---|---|
| Neutrality collapse — stripping argumentative stance, defaulting to balanced/neutral | **New** — distinct from "generic positive conclusions" (#24); this is about removing opinion entirely |
| Pronoun depletion — 50% fewer first/second-person pronouns | **New measurable signal** — complements "experiential vacancy" but is quantifiable |
| Semantic drift in minimal edits — meaning changes even in grammar-only passes | **New insight** — relevant to the skill's self-audit loop |
| Satisfaction paradox — users like the output but know it's not them | **Contextual** — not a detection pattern but explains why AI writing persists |
| Peer review score inflation (+1 point average) | **Contextual** — domain-specific but demonstrates systematic bias |
| Impersonal language shift — fewer anecdotes, fewer human experience references | **Reinforces** existing "experiential vacancy" with experimental evidence |

### Why this matters for humanise

This is the strongest empirical evidence yet that LLMs don't just add detectable surface patterns — they **subtract meaning**. The existing humanise skill focuses heavily on what AI *adds* (vocabulary, formatting, rhetorical devices). This paper shows the equally important flip side: what AI *removes* (stance, pronouns, personal experience, argumentative commitment). The neutrality collapse finding is particularly actionable — a humanised text should preserve or restore the author's actual position rather than defaulting to both-sides balance.
