# Matthew Vollmer — "I Asked the Machine to Tell on Itself"

**Source:** https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself
**Type:** Long-form essay / pedagogical field guide; functions as a literature synthesis with ~100 micro-patterns drawn from ~60 external sources.
**Fetched:** 2026-04-30 (structured per-section per-citation extraction).

---

## Why this matters for the skill

Vollmer's essay was the source review that drove the 2026-04-27 expansion of `human-eyes/references/patterns.md` and `human-eyes/grade.py` (commit `9ce1cec`). It is the conduit for several patterns currently in the catalogue (#23a False concession, #31a Unicode flair, #35a Orphaned demonstratives, #39 Template/placeholder residue, #40 Rubric echoing). It is also a literature synthesis: most of its patterns trace back to 5–7 core empirical sources (Kobak, GPTZero, Clarke, Shankar, Chiang, Wikipedia) plus specialist studies for domain-specific tells (Walsh for poetry, Waltzer for student writing, Jiang & Hyland for academic).

For evidence-map purposes, Vollmer attribution should follow the upstream-first principle: where Vollmer cites Smith for X, attribute X to Smith with Vollmer as conduit. Where Vollmer presents an observation as his own (synthesis, taxonomy, or no external source), attribute to Vollmer directly.

---

## Article structure (10 sections)

I. Lexical tells
II. Syntactic and sentence-level tells
III. Rhetorical and structural tells
IV. Tonal tells
V. Punctuation and formatting tells
VI. Domain-specific tells (poetry, fiction, student writing, academic, journalism, email/business)
VII. Model-specific fingerprints
VIII. Forensic and computational signals
IX. Why detection is hard (and often unethical)
X. Cultural and literary reception

---

## Upstream sources Vollmer cites

Grouped by source type. Each entry gives Vollmer's citation in full bibliographic detail and notes the patterns Vollmer attributes to that source.

### Academic research

- **Kobak, Dmitry et al.** (Tübingen). "Delving into LLM-assisted writing in biomedical publications through excess vocabulary." *Science Advances*, 2025. Analysed 15M PubMed abstracts; identified excess-vocabulary signal. r-values: delve=28.0, underscores=13.8, showcasing=10.7. GitHub: berenslab/llm-excess-vocab. **Vollmer attributes:** focal vocabulary (Section I.1), academic writing fingerprints (VI.D — 13.5% of 2024 PubMed abstracts; up to 40% in MDPI/Frontiers), excess-vocabulary corpus method (VIII).
- **Juzek, Tom S. & Ward, Zina B.** "Why Does ChatGPT 'Delve' So Much?" arxiv:2412.11385. **Vollmer attributes:** focal vocabulary expansion to 21 focal words.
- **Reinhart, Alex et al.** Cited in *WHYY* reporting (Vollmer didn't directly cite the PNAS paper but referenced Reinhart's analysis of model-fingerprint drift). **Vollmer attributes:** "patterns identified in earlier ChatGPT versions had already shrunk or disappeared in newer models" (Section VII).
- **Walsh, Melanie.** Computational study of AI poetry. arxiv:2410.15299. 5,700 ChatGPT poems vs. 3,700 from Poetry Foundation and Academy of American Poets. **Vollmer attributes:** poetry tells (VI.A) — constrained uniformity, rhyme/quatrain default, first-person plural overuse, mood-word accumulation.
- **Waltzer et al.** (2023). *Wiley.* Study of 69 high school teachers and 140 students. Teacher accuracy 70%; student accuracy 62%; confidence uncorrelated with accuracy. **Vollmer attributes:** student writing detection difficulty (VI.C).
- **Jiang & Hyland** (2025). *SAGE.* ChatGPT-generated argumentative essays contained significantly fewer engagement markers (questions, asides, reader address) than human student essays. **Vollmer attributes:** academic-writing engagement-marker depletion (VI.D).
- **Liang et al.** (Stanford / HAI, 2023). *Patterns* journal. Seven major detectors misclassified 61.3% of TOEFL essays as AI-generated vs. near-perfect on U.S. 8th-grade essays; 19.8% unanimously flagged. **Vollmer attributes:** false-positive bias against non-native English speakers (IX).
- **Dhillon et al.** arxiv:2510.13939. MFA students vs. LLMs study; expert readers detect AI via clichés, purple prose, exposition, lack of subtext, mixed metaphors. **Vollmer attributes:** fiction tells (VI.B).
- **Chiang, Ted.** "ChatGPT Is a Blurry JPEG of the Web." *New Yorker*, Feb 2023 (also discussed at *Longreads*). "Why A.I. Isn't Going to Make Art." 2024. **Vollmer attributes:** false concession / both-sides hedge (III.18); founding lossy-compression metaphor (X).
- **Vara, Vauhini.** "Ghosts" (*The Believer* 2021); "Confessions of a Viral AI Writer" (*Wired* 2023); *Searches: Selfhood in the Digital Age* (Pantheon 2025). **Vollmer attributes:** strategic vagueness / abstraction drift (IV.20) — "polite, predictable, inoffensive, upbeat".
- **Preston, Laura.** "HUMAN_FALLBACK" (*n+1* Issue 44, 2022); "An Age of Hyperabundance" (*n+1* Issue 47, 2024). **Vollmer attributes:** missing concrete particular (IV.24); "collapse of context" framing.
- **Murray & Tersigni** (2024). *Journal of Applied Learning & Teaching* 7(2). doi:10.37074/jalt.2024.7.2.12. (Vollmer indirect via student-writing detection coverage.)

### Journalism and trade press

- **Merrill, Jeremy B. et al.** "What are the clues that ChatGPT wrote something?" *Washington Post*, 13 Nov 2025. (Indirect; Vollmer cites GPTZero burstiness work which overlaps Merrill's analysis.)
- **Phillips, Brian.** *The Ringer*, August 2025. Dissenting view: em-dash is "the most human punctuation mark there is". **Vollmer attributes:** em-dash counter-position (V.26).
- **Bailey, Jonathan.** *Plagiarism Today*, 2025. Six-model em-dash test (ChatGPT, Copilot, Deepseek, Claude, Gemini, Meta.ai). **Vollmer attributes:** model-specific em-dash fingerprints (V.26, VII).
- **Hsu, Hua.** *New Yorker* / Bard College. "What college students lose when ChatGPT writes their essays" (*WNYC Brian Lehrer*). **Vollmer attributes:** cultural reception (X).
- **Forbes / The Conversation** (2024). On "tapestry" appearance signalling AI generation. **Vollmer attributes:** tapestry-noun family (I.2).
- **Csutoras, Brent.** *Medium.* LLM training corpora overrepresent long-form journalism where em-dashes are common. **Vollmer attributes:** em-dash mechanism (V.26).
- **Edwards, Benj.** *Ars Technica*, 14 Nov 2025. Documents OpenAI suppressing em-dashes in GPT-5.1. **Vollmer attributes:** em-dashes (V.26).
- ***Slate***, August 2025. "Paranoia spiral" article on writers introducing typos to signal humanity. **Vollmer attributes:** paranoia spiral (X).
- **PBS NewsHour / Futurism.** *CNET* AI-generated finance articles (77 articles, corrections on >50%); *Sports Illustrated* AI bylines and headshots. **Vollmer attributes:** journalism tells (VI.E).
- **Kane, Kenny.** kenny-kane.com/claude-for-writing-a-book. **Vollmer attributes:** Claude fingerprints (VII).
- **Live Science.** Coverage of OpenAI's April 2025 sycophancy rollback. **Vollmer attributes:** sycophancy (IV.21).

### Practitioner guides and writer blogs

- **Stockton, Blake.** Substack series: blakestockton.com/dont-write-like-ai-1-101-negation. Devoted "entire series" to negation patterns. **Vollmer attributes:** negative parallelism (II.7) — "the most prominent AI writing tell".
- **Shankar, Shreya.** sh-reya.com/blog/ai-writing/. **Vollmer attributes:** orphaned demonstratives / bad-subject problem (II.10); bullet-point fetish (V.30); echoes Vara on vagueness.
- **Clarke, Neil.** *Clarkesworld* editor. **Vollmer attributes:** fiction tells (VI.B); editorial observations (X) — closed submissions Feb 2023 after 500/1200 AI submissions; "they are bad in ways no human has been bad before".
- **Guo, Charlie.** *Artificial Ignorance* Substack. **Vollmer attributes:** flatness of affect (IV.23); fiction tells (VI.B); em-dash Reddit-API analysis (V.26); "AI slop" coinage (X).
- **Trott, Sean.** UC San Diego, seantrott.substack.com. **Vollmer attributes:** LLM signature analysis (X).
- **Sloan, Robin.** robinsloan.com lab notes (since 2017). **Vollmer attributes:** partnership framing (X) — "the goal is not to make writing 'easier'; it's to make it harder".
- **Aranya / *Poetly* (Substack).** poetly.substack.com. **Vollmer attributes:** poetry tells beyond Walsh (VI.A) — aphorism density, negate-and-redefine structure, mood-word accumulation.
- **Germain, David J.** *Medium.* **Vollmer attributes:** parenthetical stage-direction tics in GPT-3.5 dialogue (VI.B).
- **Walter Writes AI.** Blog. **Vollmer attributes:** corporate-inflation adjectives (I.3); humanizer-tool category (IX).
- **Yours AI Slop.** Blog. **Vollmer attributes:** corporate-inflation adjectives (I.3).
- **DeGPT writer collective.** **Vollmer attributes:** signposting filler phrases (I.5).
- **YourTango.** **Vollmer attributes:** signposting filler phrases (I.5).
- **Copy Posse.** copyposse.com. **Vollmer attributes:** tricolon armature in LinkedIn writing (II.8); business email tells (VI.F).
- **Earthworm Express.** earthwormexpress.com. **Vollmer attributes:** em-dash distribution (not presence) as the diagnostic (V.26).
- **Frohrer.** blog.frohrer.com. **Vollmer attributes:** promotional register (III.17); n-gram uniformity / Zipf's law (VIII).
- **AI for Lifelong Learners.** Substack. **Vollmer attributes:** five-paragraph-essay shape (III.13); machine cleanliness (V.27).
- **Context-link.ai** (blog/claude-em-dash-remover). **Vollmer attributes:** Claude hedge-and-reassure pattern (III.15, VII).
- **Hastewire.** hastewire.com. **Vollmer attributes:** student writing detection signals (VI.C).
- **Alibaba literary AI column.** alibaba.com. **Vollmer attributes:** AI editors flagging human metaphors (VI.B).

### Vendor / first-party

- **GPTZero.** gptzero.me/news/perplexity-and-burstiness-what-is-it/. **Vollmer attributes:** burstiness and perplexity as detection signals (II.9, VIII); commercial detector backbone.
- **OpenAI.** April 2025 sycophancy rollback blog post; OpenAI Community Forum complaints about closing-ritual phrases; AI classifier retired July 2023 (26% accuracy on AI text, 9% false positives on human text); GPT-5.1 em-dash suppression. **Vollmer attributes:** sycophancy (IV.21); closing rituals (I.6); em-dashes (V.26); detector retirement (IX).
- **Gmelius.** gmelius.com/blog/can-customers-tell-an-email-is-written-using-generative-ai. **Vollmer attributes:** email/business tells (VI.F) — formulaic openings, unedited placeholders, three-sentence paragraphs, missing colons/semicolons.
- **Bynder** (2024 consumer study). **Vollmer attributes:** 55% of U.S. consumers correctly identify AI marketing (VI.F).
- **Pangram, Copyleaks, ZeroGPT, Originality.AI, Writer.** Commercial detector backbone built on burstiness metric. **Vollmer attributes:** detector landscape (VIII, IX).
- **NetusAI.** netus.ai/blog/stylometry-explained-how-ai-detectors-fingerprint-your-writing. **Vollmer attributes:** stylometric fingerprinting (VIII); humanizer tool category (IX).
- **Turnitin.** **Vollmer attributes:** author-comparison baselines as forensic method (VIII).
- **Wikipedia "Signs of AI writing"** / WikiProject AI Cleanup. **Vollmer attributes:** negative parallelism elevation (II.7); puffed-up significance (III.16); Unicode flair (V.29); G15 criterion / cleanup project (X).

### Cultural / literary commentary

- **Monson, Ander.** *Diagram* / chapbook: Lillian-Yvonne Bertram's *A Black Story May Contain Sensitive Content* (AI-generated, disclosed, awarded 2023). **Vollmer attributes:** cultural reception (X).
- **Bertram, Lillian-Yvonne.** *A Black Story May Contain Sensitive Content* (AI-generated chapbook). (Cited via Monson.)
- **McNamara, Jack** (quoted in *Slate* 2025). "Writing online in 2025 feels like performing keyhole surgery while people scream 'ROBOT! ROBOT! ROBOT!' into your ear". **Vollmer attributes:** paranoia spiral (X).
- **McCarty, Sarah** (quoted in *Slate* 2025). "I think this is something ChatGPT excels at" — now avoids metaphors. **Vollmer attributes:** paranoia spiral (X).
- **Janus** and **Domenic Denicola** (domenic.me/chatgpt-simulacrum/). Simulator / simulacra framing. **Vollmer attributes:** critical vocabulary (X).
- **Casey, Cat** (cited in USD guide). Detector evasion (80–90%). **Vollmer attributes:** cat-and-mouse problem (IX).
- **Campbell, Jenny** (Reddit commenter, deaf writer; cited in *WHYY*). Accused of being chatbot "about a dozen" times in five months. **Vollmer attributes:** ethics of accusation (IX).

---

## Patterns Vollmer presents as his own observation (no external attribution)

These are Vollmer's synthesis or independent observations, not sourced from elsewhere:

1. **Inflated verbs** (I.4) — leverage, utilize, harness, streamline, facilitate, optimize, empower, navigate, illuminate, bolster.
2. **Hedge-and-reassure** (III.15) — diagnostic framing is his (Claude attribution is for model behaviour, not the diagnostic).
3. **Puffed-up significance** (III.16) — Wikipedia provides the metaphor, Vollmer's diagnostic framing.
4. **Aphoristic closure** (III.19) — paragraphs ending on pseudo-profound kicker.
5. **False profundity / universal-generic statements** (IV.22) — based on cross-entropy loss framing, no external source.
6. **Curly/smart quotes** (V.28).
7. **Emojis in section headings** (V.31) — characterised as RLHF residue, no external source.
8. **Title case headings in surprising places** (V.32).
9. **Pedagogical exercises** (XI) — "Specificity Rewrite" and other classroom methods.
10. **30-second diagnostic cluster** (XII) — synthesis of the preceding taxonomy.
11. **Coda reframe of Clarke** — counter-argument that human badness is specific, LLM badness generic.

---

## Vollmer's role in the human-eyes catalogue (2026-04-27 review)

The 2026-04-27 Codex session that produced commit `9ce1cec` ran a "Gaps Worth Adding" pass against Vollmer. Items that became numbered patterns:

- **Item 1 (Orphaned demonstratives, citing Shankar via Vollmer)** → #35a in `human-eyes/references/patterns.md`. Catalogue currently cites Shankar; Vollmer is the conduit.
- **Item 2 (False concession / both-sides hedge, citing Chiang via Vollmer)** → #23a. Catalogue currently cites Wikipedia + Abdulhai mechanism; Vollmer is the conduit and Chiang is the upstream.
- **Item 3 (Closing ritual phrases)** → folded into existing `no-signposted-conclusions` and possibly drove `no-soft-scaffolding` (one of the Group B undocumented checks).
- **Item 4 (Unicode flair, citing Wikipedia via Vollmer)** → #31a. Catalogue currently cites Guo + Wikipedia + Corpus.
- **Item 5 (Placeholders, citing Gmelius via Vollmer)** → #39 (already corrected in U1b).
- **Item 6 (Citation oddities)** → folded into manual-only #41 plus reference to Bailey/Plagiarism Today.
- **Item 7 (Rubric echoing, Vollmer's own observation)** → #40 (already corrected in U1b).
- **Item 8 (Poetry, citing Walsh)** → folded into #41.
- **Item 9 (Fiction, citing Clarke)** → folded into #41.
- **Item 10 (Model-specific fingerprints)** → reference-only mention; may relate to Group B's `no-bland-critical-template`.

---

## How this changes the evidence map

Patterns that should gain Vollmer attribution (or correct Vollmer-via-X chain):

- **#23a False concession hedges** — currently cites Wikipedia + Abdulhai. Should add Chiang ("ChatGPT Is a Blurry JPEG of the Web", *New Yorker* 2023) as upstream via Vollmer, plus Stockton (Substack negation series).
- **#31a Unicode flair** — currently cites Guo + Wikipedia + Corpus. Wikipedia is editor consensus on this; Vollmer is the conduit.
- **#35a Orphaned demonstratives** — currently cites Shankar. Should note Vollmer as conduit (Shankar via Vollmer's review) since that's how Shankar got into the catalogue.
- **#9 Contrived contrast** — currently cites Russell + Merrill + Kriss + Guo + Wikipedia + Corpus. Vollmer adds Stockton (negation series) as the most heavily evidence-backed practitioner source on this pattern.
- **#5 Vague attributions** — Vara is the strongest single source per Vollmer and not currently in the evidence map.
- **#19 Collaborative artifacts** — Gmelius via Vollmer is a primary source for the email-template aspect; currently cites Wikipedia + OpenAI + Guo + Caroll.
- **#21 Sycophantic tone** — already cites OpenAI; Vollmer adds Live Science as confirming coverage.
- **Em-dashes density grader check** — already cites Merrill + Edwards + Kriss; Vollmer adds Csutoras (Medium), Bailey (Plagiarism Today), Phillips (Ringer dissent), Earthworm Express (distribution-not-presence).
- **#41 Genre-specific manual checks** — should cite Walsh (poetry) directly; Aranya (Poetly); Germain (Medium fiction); Dhillon et al. (arxiv 2510.13939); Hastewire (student writing); Bynder (business).

Source-gap status: this file partially closes Known Issues #2 of the evidence map for these previously-uncovered sources: Shankar (now grounded via Vollmer's citation chain), Walsh/Preus/Gronski (Walsh is now grounded via the Walsh paper directly), Clarkesworld (Clarke is now grounded via Vollmer's editorial attribution), Futurism (Vollmer's coverage of CNET/Sports Illustrated), Stanford HAI (Liang et al. 2023 now grounded). Still no per-source files for Stanford HAI specifically, GPTZero (Vollmer cites their docs but doesn't synthesise), OpenAI sycophancy rollback as a primary event.

---

## Limitations

- Vollmer is opinionated. His framing is pedagogical (he teaches a writing seminar at Virginia Tech); some patterns are presented as his diagnostic synthesis rather than as research findings. Where he says "this is the most diagnostic move" — that is his claim, not empirical.
- His source list mixes peer-reviewed research, journalistic reporting, vendor documentation, blog posts, and his own observations. The evidence map should preserve those distinctions per source; Vollmer's mention is not equivalent to peer-reviewed support.
- The article is dated by its own model snapshots (GPT-4o vs GPT-5 vs GPT-5.1 references). Patterns Vollmer documents may already have shifted in newer models (Reinhart's drift point).
