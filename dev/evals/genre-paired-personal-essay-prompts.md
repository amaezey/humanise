# Genre-paired corpus: long-form first-person essay

Five human essays and the prompts to generate matched AI versions for the human-vs-AI flag-count comparison.

Genre: long-form first-person essay (literary review, practitioner blog, business memo, personal philosophy, confessional memoir). Heterogeneous within "essay" but all first-person reflective.

Each prompt is a writing brief — no anti-AI-pattern instructions — so the comparison tests what models naturally produce in each register.

---

## 1. Image Journal — First Men and Original Sins

- **Human source:** [`dev/evals/samples/human-sourced/21c-image-first-men-original-sins.md`](samples/human-sourced/21c-image-first-men-original-sins.md)
- **Author:** Adam Roberts
- **URL:** https://imagejournal.org/article/first-men-and-original-sins/
- **Length:** ~4,000 words
- **Planned AI slug:** `21c-ai-first-men-original-sins`

### Prompt

> Write a long-form essay reviewing two books and a film on the American space program: Kendrick Oliver's *To Touch the Face of God: The Sacred, the Profane, and the American Space Program, 1957–1975* (Johns Hopkins, 2013); Catherine L. Newell's *Destined for the Stars: Faith, Future, and America's Final Frontier* (Pittsburgh, 2019); and Damien Chazelle's film *First Man* (2018). Use the texts as a lens for thinking about religious imagination, sin, and frontier mythology in mid-century American spaceflight. Voice: literary-religion-journal essay; scholarly but non-academic; weaves quotation and synthesis; section breaks but no listicle structure. ~4,000 words.

---

## 2. Open.coop — Belonging is a Superpower

- **Human source:** [`dev/evals/samples/human-sourced/21c-opencoop-belonging-superpower.md`](samples/human-sourced/21c-opencoop-belonging-superpower.md)
- **Author:** Oliver Sylvester-Bradley
- **URL:** https://open.coop/2017/09/25/belonging-superpower-patterns-decentralised-organising/
- **Length:** ~1,150 words
- **Planned AI slug:** `21c-ai-belonging-superpower`

### Prompt

> Write a workshop write-up for a co-op / community-organising blog. The workshop was led by the founders of Loomio (decision-making software for non-hierarchical groups) and covered eight patterns for decentralised organising: (1) Intentionally produce counter-culture / "belonging is a superpower"; (2) Systematically distribute care labour (stewards and stewardees); (3) Make explicit norms and boundaries; (4) Keep talking about power; (5) Make decisions asynchronously; (6) Agree how you use tech (the "holy trinity": realtime / async / static); (7) Use rhythm to cut information overload; (8) Generate new patterns together. List the patterns with brief commentary, anchored in your experience attending the workshop. Voice: warm practitioner-blog, first-person + we, mildly informal. ~1,100 words.

---

## 3. Forte Labs — Servant Hedonism

- **Human source:** [`dev/evals/samples/human-sourced/21c-fortelabs-servant-hedonism.md`](samples/human-sourced/21c-fortelabs-servant-hedonism.md)
- **Author:** Tiago Forte
- **URL:** https://fortelabs.com/blog/servant-hedonism-my-life-philosophy/
- **Length:** ~1,300 words
- **Planned AI slug:** `21c-ai-servant-hedonism`

### Prompt

> Write a first-person personal-philosophy blog post titled "Servant Hedonism: My Life Philosophy." Open with realising on a Sunday afternoon that you have a life philosophy. Thesis: service to others and personal pleasure are usually treated as opposites, but they reinforce each other. Service alone leads to martyrdom; pleasure alone leads to self-centredness; together they're "Servant Hedonism." Section breaks for the two halves before bringing them together at the end. Reference adrienne maree brown briefly on not creating freedom for others through your own bondage. Voice: personal-philosophy blog, first-person, productivity-adjacent register. ~1,300 words.

---

## 4. Tom Critchlow — Workshops as Portals

- **Human source:** [`dev/evals/samples/human-sourced/21c-critchlow-workshops.md`](samples/human-sourced/21c-critchlow-workshops.md)
- **Author:** Tom Critchlow
- **URL:** https://tomcritchlow.com/2019/09/23/workshops/
- **Length:** ~2,800 words
- **Planned AI slug:** `21c-ai-workshops-as-portals`

### Prompt

> Write a long-form practitioner essay for consultants. Title: "Workshops as Portals" with subtitle "And how to create clarity in consulting work." Argument: selling a one-day workshop is the best way to bridge the inside/outside problem of consulting — you don't sell it to *solve* something, you sell it to create *clarity*, which is itself valuable and chargeable. Cover: why clarity matters for both client and consultant; structuring workshops for outcomes not happiness; conversation prompts to run effective jam-sessions; not underselling (e.g., $4,000/day); a couple of examples from your own work. Reference *in media res* as a narrative device early on — both client and consultant want a sense of how it'll feel to work together. Voice: practitioner-blog, first-person, business-essay register, pragmatic and warm. ~2,800 words.

---

## 5. Tucker Max — What MDMA Therapy Did For Me

- **Human source:** [`dev/evals/samples/human-sourced/21c-tuckermax-mdma-therapy.md`](samples/human-sourced/21c-tuckermax-mdma-therapy.md)
- **Author:** Tucker Max
- **URL:** https://medium.com/@tuckermax/what-mdma-therapy-did-for-me-41ffe5f15971
- **Length:** ~9,700 words
- **Planned AI slug:** `21c-ai-mdma-therapy`

### Prompt

> Write a long-form first-person confessional essay for Medium titled "What MDMA Therapy Did For Me." You're a writer who's been through MDMA-assisted therapy and want to walk readers through what it did for you. Cover: the lead-up, the stigma you had to push through, what a session actually looks like (set, setting, dose, therapists, integration), the specific things that shifted (childhood trauma, attachment patterns, relationship with parents, current marriage, sense of self), what *didn't* shift, and where you are now. Voice: direct first-person; emotionally disclosing without being precious; occasional profanity; no academic distance. Acknowledge that the substance is illegal in most contexts and that you're not advocating self-medication. ~9,700 words.

---

## What's planned next

1. AI-generated set (5): each prompt above run against a model to produce a fresh AI essay. Save to `dev/evals/samples/generated-ai/`.
2. AI-rewritten set (5): each human essay above passed to an AI agent for rewriting. Save to `dev/evals/samples/generated-ai/` with a `-rewrite` suffix.
3. Total comparison corpus: 5 human + 10 AI (5 fresh + 5 rewrite) for the genre-paired audit suite.
