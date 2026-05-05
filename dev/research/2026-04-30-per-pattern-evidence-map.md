# Per-pattern evidence map (internal)

Date: 2026-04-30
Status: working artefact for refining the app; gitignored, not for the public README.

## Known issues with this draft

Raw collation of 7 parallel subagent slices. The following issues are NOT yet fixed and are tracked as follow-up tasks:

1. **Wikipedia source gap.** [Resolved: U1c built `dev/research/wikipedia-signs-of-ai-writing.md` with full per-pattern citation extraction via Wikipedia API. Wikipedia turned out to be a literature synthesis citing 19 named upstream sources; per-pattern entries in this evidence map now surface those upstream sources where Wikipedia cites them, and explicitly mark "(editor consensus, no upstream source)" where Wikipedia is unsourced. 18 entries got the editor-consensus marker; 8 entries gained substantive upstream academic attribution (Reinhart PNAS, Russell ACL, Merrill Washington Post, Edwards Ars Technica, Sun et al., Kousha & Thelwall, Geng & Trotta, Belcher Chronicle of Higher Education).]
2. **Other source gaps.** [Largely resolved by U1c.] Wikipedia synthesis (`dev/research/wikipedia-signs-of-ai-writing.md`) grounded Kobak, Juzek/Ward (both papers), Reinhart, Russell, Merrill, Edwards, Sun et al., Kousha & Thelwall, Geng & Trotta, Belcher. Vollmer synthesis (`dev/research/vollmer.md`) grounded Shankar (via Vollmer), Walsh (poetry, primary paper), Clarke (Clarkesworld), Stanford HAI / Liang et al. (via Vollmer), plus added Stockton (negation series), Vara (vagueness), Chiang (false concession), Preston (collapse of context), Aranya (poetry), Germain (fiction), Dhillon et al. (MFA fiction), Waltzer et al. (student writing), Jiang & Hyland (academic), Gmelius (email), Bynder (marketing), and ~30 other practitioner and journalism sources. Remaining genuine gaps: GPTZero (Vollmer cites their docs but doesn't extract; would benefit from a focused fetch), OpenAI sycophancy rollback (a primary event, not a research source — could be acknowledged as event-evidence rather than synthesised), Futurism (covered by Vollmer's journalism section but no dedicated per-source file).
3. **"web-survey-2026" mis-cited as a source.** [Resolved: U1b grep pass found no live mis-citations — slice agents named the primary sources directly (Nature 2025, Przystalski/Zaitsu/Bisztray, practitioner guides, Abdulhai). Likely cleaned during slice work.]
4. **"patterns.md '2026 operating stance'" mis-cited as a source.** [Resolved: U1b dropped patterns.md self-citations from entries #39, #40, and the paragraph-length-variance grader check. patterns.md is a derivative description of patterns, not a source. Real provenance recovered for #39 (Gmelius via Vollmer) and #40 (Vollmer's own observation, "I Asked the Machine to Tell on Itself") by reading the 2026-04-27 Codex session that introduced both patterns. Paragraph-length-variance retains practitioner guides + Guo + Corpus.]
5. **Formatting inconsistencies across slices.** Slices vary in field naming, source list format, and citation style. Need a single normalised template applied uniformly.
6. **Severity not yet looked up.** Each pattern needs its severity (`hard_fail` / `strong_warning` / `context_warning`) looked up from `human-eyes/grade.py` and added.

---

## Method

Two analytical fields per pattern.

**How AI uses it.**
- `frequency-coded` — sources claim AI uses the pattern more often than humans (density signal).
- `appropriate-use-coded` — sources claim humans use the pattern legitimately; AI uses it inappropriately (filler, performance, reaching for depth).
- `both` — sources make both claims.
- `unclear-from-sources` — sources do not speak to the distinction.

**Evidence basis.**
- `corpus-measured` — measured directly in `dev/research/2026-04-29-genre-paired-corpus-findings.md` (N=5 per group, matched personal-essay register).
- `external-only` — catalogued from external sources; not measured in the corpus.
- `both` — both apply.
- `no-direct-evidence` — neither external source nor corpus measurement; pattern catalogued without grounded provenance. Should be rare; flag for revisit.

---

## Content patterns (1-6)

### 1. Significance inflation

**Sources:** Belcher (Chronicle of Higher Education 2025); Juzek & Ward (ACL 2025); Sun et al. (arxiv 2025); Kobak et al. (Science Advances 2025); Wikipedia "Signs of AI writing"; GPTZero AI Vocabulary list; Grammarly; Kriss/NYT

**Why it's in the skill:** Multiple catalogues independently flag the same phrase family ("pivotal moment", "indelible mark", "underscore the importance", "mark a turning point") as AI-frequent inflation language. Wikipedia treats this as a distinct sign and cites Belcher's Chronicle essay, Juzek & Ward on lexical overrepresentation, and Sun et al. on LLM idiosyncrasies; the pattern combines a vocabulary density tell with a content-level move that claims importance instead of explaining it.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Belcher ("10 Ways AI Is Ruining Your Students' Writing", Chronicle of Higher Education, 16 Sep 2025; cited by Wikipedia for significance inflation): names the importance-without-evidence move in AI student writing.
- Juzek & Ward ("Why Does ChatGPT 'Delve' So Much?", ACL 2025, arxiv:2412.11385; cited by Wikipedia for lexical overrepresentation): traces specific high-significance words ("pivotal", "underscore") to LLM lexical inflation.
- Sun, Yin, Xu, Koller, Liu ("Idiosyncrasies in Large Language Models", arxiv:2502.12150; cited by Wikipedia): documents LLM stylistic idiosyncrasies including significance-inflation phrasing.
- Wikipedia "Signs of AI writing" (citing Belcher, Juzek, Sun et al.): catalogues "stands/serves as", "is a testament", "vital/significant/crucial/pivotal/key role", "underscores its importance", "evolving landscape", "indelible mark". Frames as inflating importance without explaining why anyone should care.
- GPTZero AI Vocabulary list: phrase overlap on "play a pivotal role", "a pivotal moment", "leave an indelible mark", "underscore the importance", "mark a turning point", "a significant milestone", "pave the way for the future".
- Kobak et al. (`llm-excess-vocab`): style-annotated rows in the 900-row excess-vocabulary set support several lexical items as post-2023 frequency lifts.
- Grammarly: lists "pivotal", "underscore", "this underscores the importance of".
- Kriss/NYT: names "underscore", "highlight", "showcase" plus "intricate" and "tapestry" as post-ChatGPT academic word cluster.

**Notes:** Not directly fired in the corpus; manufactured-insight is the closest proxy and inverts (humans 2/5, AI fresh 1/5, AI rewrite 0/5).

### 2. Notability claims

**Sources:** Wikipedia "Signs of AI writing"; Futurism (adjacent)

**Why it's in the skill:** WikiProject AI Cleanup catalogues a recurring AI move where the article asserts notability by listing outlets or follower counts as if the mention itself is the story; Futurism's reporting on fabricated bylines and bios sits alongside as a provenance tell.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): "independent coverage", "local/regional/national media outlets", "written by a leading expert", "active social media presence". Asserts notability by listing sources without context.
- Futurism: documents fake bylines, fake bios, AI headshots, byline laundering as provenance artefacts.

**Notes:** Wikipedia portion is editor consensus, not externally sourced.

### 3. Superficial -ing analyses

**Sources:** Reinhart et al. (PNAS 2025); Belcher (Chronicle of Higher Education 2025); Wikipedia "Signs of AI writing"; practitioner guides (aidetectors.io, seoengine.ai, SAGE)

**Why it's in the skill:** Wikipedia catalogues the present-participle tail ("highlighting…", "ensuring…", "reflecting…") as an AI move that simulates analytical depth, citing Reinhart et al.'s PNAS study on LLM grammatical and rhetorical variation; practitioner guides give the frequency claim — instruction-tuned models use "main clause + comma + -ing phrase" at 2 to 5 times the human rate.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Reinhart, Markey, Laudenbach, Pantusen, Yurko, Weinberg, Brown ("Do LLMs write like humans? Variation in grammatical and rhetorical styles", PNAS 122(8), 2025, doi:10.1073/pnas.2422455122; cited by Wikipedia for the participle-tail pattern): documents grammatical and rhetorical style variation including participial-construction frequency.
- Belcher ("10 Ways AI Is Ruining Your Students' Writing", Chronicle of Higher Education, 16 Sep 2025; cited by Wikipedia): names the participle-tail pattern in AI student writing.
- Wikipedia "Signs of AI writing" (citing Reinhart, Belcher): "highlighting", "underscoring", "emphasizing", "ensuring", "reflecting", "symbolizing", "contributing to", "cultivating", "fostering", "encompassing", "showcasing".
- Practitioner guides: present participial constructions at 2 to 5× human rate.

### 4. Promotional language

**Sources:** Wikipedia "Signs of AI writing"; Grammarly; Caroll

**Why it's in the skill:** Wikipedia flags a tourism-marketing register that AI defaults to ("nestled", "vibrant", "stunning", "must-visit"); Grammarly's buzzword list overlaps on the corporate edge; Caroll's "warm fuzzies" framing names the underlying bias toward pleasant, emotionally safe language.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus on trigger list, no upstream source for the specific phrases): "boasts a", "vibrant", "rich" (figurative), "profound", "showcasing", "nestled", "in the heart of", "groundbreaking", "renowned", "breathtaking", "must-visit", "stunning".
- Grammarly: "revolutionize", "innovative", "cutting-edge", "game-changing", "transformative", "seamless integration", "scalable solution".
- Caroll: "warm fuzzies" — AI default to pleasant, emotionally safe framing. "ChatGPT gets away with it because it's writing warm fuzzies not lectures."

### 5. Vague attributions

**Sources:** Wikipedia "Signs of AI writing"; Shankar (adjacent); Nature 2025 (adjacent)

**Why it's in the skill:** Wikipedia catalogues the move where AI attributes opinions to vague authorities ("Industry reports", "Observers have cited") to manufacture consensus; Shankar's craft critique reinforces the underlying problem; Nature's findings sit alongside as quantitative evidence that AI use correlates with more factual mistakes.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): "Industry reports", "Observers have cited", "Experts argue", "Some critics argue".
- Shankar: vagueness and fluency-without-understanding as core AI-writing failures.
- Nature 2025: ~55% increase in objective mistakes in NeurIPS submissions 2021-2025, correlated with rising AI use.

### 6. Formulaic challenges sections

**Sources:** Wikipedia "Signs of AI writing"; GPTZero AI Vocabulary list

**Why it's in the skill:** Wikipedia catalogues a recurring section template ("Despite its... faces several challenges...") that acknowledges a problem and immediately reassures the reader; GPTZero's phrase list independently includes "despite the challenge" and "despite the face".

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): "Despite its... faces several challenges", "Despite these challenges", "Challenges and Legacy", "Future Outlook".
- GPTZero list: "despite the challenge" and "despite the face".

---

## Language and grammar (7-12)

### 7. AI vocabulary words and phrases

**Sources:** Kobak et al. (Science Advances 2025); Juzek & Ward (ACL 2025; "Word Overuse and Alignment", arxiv 2025); Reinhart et al. (PNAS 2025); Merrill, Chen, Kumer (Washington Post 2025); Kousha & Thelwall (ISSI 2025); Geng & Trotta (ACL 2025); GPTZero AI Vocabulary; Grammarly; Nature 2025; Kriss/NYT; Guo; Wikipedia "Signs of AI writing"; Corpus

**Why it's in the skill:** Most heavily evidence-backed pattern in the catalogue. Multiple peer-reviewed studies (Kobak; Juzek & Ward x2; Reinhart; Kousha; Geng) show specific words ("delve", "underscore", "intricate", "tapestry", "pivotal", "meticulous", "unparalleled", "invaluable") spike sharply in post-2023 text relative to human baselines, with measurable frequency decline tracked into 2025 (Merrill).

**How AI uses it:** frequency-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Kobak, González-Márquez, Horvát, Lause ("Delving into LLM-assisted writing in biomedical publications through excess vocabulary", Science Advances 11(27), 2025, doi:10.1126/sciadv.adt3813; cited by Wikipedia as primary academic source): 900-row excess-vocabulary set; supports lexical spike detection at corpus level.
- Juzek & Ward ("Why Does ChatGPT 'Delve' So Much?", ACL 2025, arxiv:2412.11385; cited by Wikipedia): "delve" measurably overrepresented post-ChatGPT in scientific abstracts; attributes mechanism to RLHF.
- Juzek & Ward ("Word Overuse and Alignment in Large Language Models: The Influence of Learning from Human Feedback", arxiv:2508.01930; cited by Wikipedia): extends the analysis to alignment-driven word overuse.
- Reinhart, Markey, Laudenbach, Pantusen, Yurko, Weinberg, Brown ("Do LLMs write like humans?", PNAS 122(8), 2025, doi:10.1073/pnas.2422455122; cited by Wikipedia for several specific words including "intricate", "vibrant", "tapestry"): documents grammatical and rhetorical style variation, including LLM word-frequency idiosyncrasies.
- Merrill, Chen, Kumer ("What are the clues that ChatGPT wrote something? We analyzed its style.", Washington Post, 13 Nov 2025; cited by Wikipedia): tracks "delve" peaking in 2023, declining through 2024, dropping sharply by 2025.
- Kousha & Thelwall ("How much are LLMs changing the language of academic papers after ChatGPT?", ISSI 2025, arxiv:2509.09596; cited by Wikipedia): multi-database co-occurrence analysis of post-ChatGPT vocabulary shifts.
- Geng & Trotta ("Human-LLM Coevolution: Evidence from Academic Writing", ACL 2025; "Is ChatGPT Transforming Academics' Writing Style?", arxiv:2404.08627; cited by Wikipedia): word-frequency and is/are usage shifts in academic writing post-ChatGPT.
- GPTZero AI Vocabulary: 100 public phrase rows from 3.3M texts.
- Grammarly: 31 indicator words/phrases — "delve into", "underscore", "pivotal", "realm", "harness", "illuminate", "facilitate", "bolster", "streamline", plus transitions "that being said", "at its core", "to put it simply".
- Nature 2025: ~200,000 of 1.5M PubMed abstracts in 2024 contained LLM-characteristic vocabulary (~1 in 7); up to 22% of CS papers; "unparalleled" and "invaluable" flagged. Vocabulary fingerprints shift across model versions (GPT-4: tapestry, pivotal, meticulous; GPT-4o: align with, enhance, showcasing).
- Kriss/NYT: "delve" frequency rose ~2,700% in PubMed abstracts 2022-2024; mechanism partly traced to RLHF labellers in Nigeria/Kenya.
- Guo: academic vocabulary as yellow flag; problem is density and lack of purpose.
- Wikipedia "Signs of AI writing" (citing Kobak, Juzek, Juzek2, Reinhart, Merrill, Kousha, Geng, Kriss): consolidated phrase list; per-word attributions vary across the academic sources above.
- Corpus: vocabulary-diversity check fired 3/5 human, 2/5 AI fresh, 0/5 AI rewrite, but is read as length-driven not AI-specific in this register.

**Notes:** Strongest empirical pattern. Skill stance: vocabulary contributes points to a composite, only fails when combined.

### 8. Copula avoidance

**Sources:** Geng & Trotta (arxiv 2024); Wikipedia "Signs of AI writing"

**Why it's in the skill:** AI substitutes elaborate verb constructions ("serves as", "stands as", "boasts", "features") for simple "is", "are", or "has". Geng & Trotta documented an over-10% decrease in usage of "is"/"are" in academic writing in 2023, the year ChatGPT became widely accessible.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Geng & Trotta ("Is ChatGPT Transforming Academics' Writing Style?", arxiv:2404.08627; cited by Wikipedia for the copula-avoidance claim): documented over 10% decrease in usage of "is"/"are" in academic writing in 2023.
- Wikipedia "Signs of AI writing" (citing Geng & Trotta): "serves as / stands as / marks / represents" and "boasts / features / offers" as substitutions.

**Notes:** No corpus measurement.

### 9. Contrived contrast / negative parallelism

**Sources:** Russell, Karpinska, Iyyer (ACL 2025); Merrill, Chen, Kumer (Washington Post 2025); Kriss/NYT; Guo; Wikipedia "Signs of AI writing"; Corpus (adjacent)

**Why it's in the skill:** "It's not X, it's Y" and its variants are one of the most-cited AI fingerprints. The skill treats it as a rhetorical move: the tell is the inflated reveal where a flat interpretation is rejected so a grander, more abstract idea arrives with fake depth.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Russell, Karpinska, Iyyer ("People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text", ACL 2025, arxiv:2501.15654; cited by Wikipedia for negative-parallelism patterns): identifies the contrast-structure family as a tell heavy LLM users reliably detect.
- Merrill, Chen, Kumer (Washington Post, 13 Nov 2025; cited by Wikipedia): documents the "Not just X, but Y" structure as one of the analyzed style markers.
- Kriss/NYT: "one of the most obvious and widespread AI tells"; used to create false profundity.
- Guo: "Parallelism itself isn't the issue, it's a perfectly legitimate rhetorical device. But AI uses it constantly, reflexively." Cites ukulele post: "It's not just about the music, it's about the joy of creativity."
- Wikipedia "Signs of AI writing" (citing Russell, Merrill): catalogues "not X but Y" / "less X than Y" / "more Y than X" / "beyond X, it is Y" family.
- Corpus (manufactured-insight, adjacent): humans 2/5, AI fresh 1/5, AI rewrite 0/5. Fires more on humans than AI in personal-essay register.

**Notes:** Corpus result reinforces tolerance note: register-typical move that the matcher may pick up on legitimate first-person framing.

### 10. Rule of three

**Sources:** Russell, Karpinska, Iyyer (ACL 2025); Kriss/NYT; Guo; practitioner guides (aidetectors.io, seoengine.ai, SAGE); Wikipedia "Signs of AI writing"; Corpus

**Why it's in the skill:** Multiple sources flag triads as default AI cadence. Tolerance note explicit: triads are common in human rhetoric, comedy, speeches; AI tell only when triads cluster densely or feel interchangeable.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Russell, Karpinska, Iyyer (ACL 2025, arxiv:2501.15654; cited by Wikipedia for the triad pattern): identifies three-item lists as a tell that heavy LLM users detect reliably.
- Kriss/NYT (cited by Wikipedia): "ideas forced into groups of three to appear comprehensive."
- Guo: "Snappy triads: 'Fast, efficient, and reliable.' 'Think bigger. Act bolder. Move faster.'" Calls out "awkward, incremental, but unmistakably alive" inside ukulele example.
- Practitioner guides: "Tricolon obsession: AI groups ideas in threes compulsively. Human writers break this constantly."
- Wikipedia "Signs of AI writing" (citing Russell, Kriss): catalogues triads as AI default cadence.
- Corpus: forced-triads fires 3/5 humans, 0/5 AI fresh, 1/5 AI rewrite; triad-density fires 5/5 across all groups. Triads universal in long-form first-person essay; pattern inverted in this register.

**Notes:** Genre-paired finding suggests register-coded; may need genre-aware thresholds.

### 11. Synonym cycling

**Sources:** Belcher (Chronicle of Higher Education 2025); Wikipedia "Signs of AI writing"; stylometry research (Przystalski 2025; Zaitsu 2025; Bisztray 2025)

**Why it's in the skill:** AI cycles through synonyms for a single referent within a short span ("the protagonist... the main character... the central figure... the hero"), an artefact of repetition-penalty decoding. Belcher names the mechanism explicitly in the Chronicle essay; Wikipedia catalogues the pattern citing her.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Belcher ("10 Ways AI Is Ruining Your Students' Writing", Chronicle of Higher Education, 16 Sep 2025; cited by Wikipedia): names the repetition-penalty decoding mechanism that drives synonym cycling ("Generative AI has a repetition-penalty code").
- Wikipedia "Signs of AI writing" (citing Belcher and Guardian editorial style guide): catalogues the pattern; mechanism attributed to repetition-penalty decoding.
- Stylometry research: stylometric watermarks include "models consistently favouring unusual sentence structures or specific synonyms".

**Notes:** Pattern plausible and well-motivated; evidence thinner than for vocabulary or rule of three.

### 12. False ranges

**Sources:** Wikipedia "Signs of AI writing"

**Why it's in the skill:** "From X to Y" constructions used to suggest scope where X and Y don't lie on a meaningful scale.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia: "from X to Y" is fine on a real scale, AI deploys it for false breadth across non-comparable items.

**Notes:** Single-source, no corpus measurement.

---

## Style (13-18)

### 13. Boldface overuse

**Sources:** Wikipedia "Signs of AI writing"; Guo

**Why it's in the skill:** Catalogue sources flag mechanical bolding as a recognisable AI tell, where emphasis is sprayed across phrases that don't need visual weight.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): AI emphasises phrases in boldface mechanically.
- Guo: "random words or sentences are bolded without it being obvious why... The bolding doesn't necessarily emphasize key points, it's just sort of there."

### 14. Inline-header lists

**Sources:** Wikipedia "Signs of AI writing"; Guo; Shankar

**Why it's in the skill:** Sources converge on the bolded-label-plus-colon list form as a recognisable AI artefact: turns flowing prose into a slide deck.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): list items start with bolded headers followed by colons, turning prose into a slide deck.
- Guo: identifies "Lists with bold inline headers" in the field guide; ukulele specimen demonstrates ("Start with songs, not scales.").
- Shankar: names over-bulleting as a craft failure.

### 15. Title case in headings

**Sources:** Russell, Karpinska, Iyyer (ACL 2025); Wikipedia "Signs of AI writing"; Grammarly

**Why it's in the skill:** AI defaults to capitalising main words in headings; reads as stiff and gives generated pieces their predictable formatting feel.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Russell, Karpinska, Iyyer (ACL 2025, arxiv:2501.15654; cited by Wikipedia for title-case headings): identifies title-case headings as a tell heavy LLM users detect.
- Wikipedia "Signs of AI writing" (citing Russell): capitalising all main words in headings reads as formal to the point of stiffness; non-standard for Wikipedia MOS.
- Grammarly: lists "title-case headings, bullet points, polished phrasing" as predictable AI formatting.

### 16. Emojis

**Sources:** Wikipedia "Signs of AI writing"; Guo

**Why it's in the skill:** Decorating headings or bullets with emojis is frequency-coded AI tell in professional contexts: humans rarely format work writing this way, AI does it routinely.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): decorating headings or bullet points with emojis is almost never appropriate.
- Guo: "No sane person I know is regularly formatting their work emails with a list of emoji-led bullet points." Notes GPT-4o produces emoji-led bullets more than predecessors.

### 17. Curly quotation marks

**Sources:** Wikipedia "Signs of AI writing"; Corpus

**Why it's in the skill:** Catalogue sources note ChatGPT defaults to curly quotes where a human writing in plain text would type straight ones. The N=5 corpus inverts this in long-form essay register, hence the explicit tolerance note.

**How AI uses it:** frequency-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): ChatGPT uses curly quotes instead of straight quotes.
- Corpus: humans 105.6 mean vs AI fresh 48.4 vs AI rewrite 29.8. In published long-form essay, humans use curly quotes more than AI.

**Notes:** Corpus reverses the simple direction in essay register; existing tolerance note handles this.

### 18. Hyphenated compound modifier overuse

**Sources:** Wikipedia "Signs of AI writing"

**Why it's in the skill:** Individual hyphenated modifiers usually correct; AI tell is stacking three or more in a single sentence.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): AI stacks four or five compound modifiers in a sentence; threshold of three or more triggers restructure.

---

## Communication (19-21)

### 19. Collaborative artifacts

**Sources:** Wikipedia "Signs of AI writing"; OpenAI sycophancy rollback (adjacent); Guo (adjacent); Caroll (adjacent)

**Why it's in the skill:** Chatbot scaffolding ("I hope this helps", "Let me know if you'd like…") is residue from the assistant-to-user register that humans don't produce in finished prose; when it survives a paste, it's near-categorical evidence the text came straight from a chatbot.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): "I hope this helps", "Of course!", "Certainly!", "You're absolutely right!", "let me know", "here is a…".
- OpenAI sycophancy rollback (April 2025 GPT-4o): documents same family of assistant flattery.
- Guo: notes "surface polish" and AI's tendency to leave conversational scaffolding.
- Caroll: "manual additions break the flow" implies the chatbot register itself is the unbroken signal.

### 20. Knowledge-cutoff disclaimers

**Sources:** Wikipedia "Signs of AI writing"

**Why it's in the skill:** Disclaimers like "as of my last training update" are produced only by language models trying to flag training-data limits; a human writer never has cause to use this exact framing in finished prose.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): "as of [date]", "Up to my last training update", "While specific details are limited/scarce…", "based on available information…".

**Notes:** Treated as a hard tell.

### 21. Sycophantic / servile tone

**Sources:** OpenAI sycophancy rollback (primary); Wikipedia "Signs of AI writing"; Kriss/NYT (adjacent); Caroll (adjacent)

**Why it's in the skill:** Performative agreement and flattery ("Great question!", "You're absolutely right!") was widespread enough in deployed assistants that OpenAI rolled back a GPT-4o release to suppress it.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- OpenAI sycophancy rollback (April 2025): documented sycophancy at scale; rolled back the release.
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): overly positive, people-pleasing language that performs agreement.
- Kriss/NYT: "always slightly wide-eyed, overeager, insipid but also on the verge of some kind of hysteria."
- Caroll: ChatGPT defaults to "warm fuzzies not lectures".

---

## Filler and hedging (22-25, 23a)

### 22. Filler phrases

**Sources:** Wikipedia "Signs of AI writing"; Grammarly; Guo; Kriss/NYT (adjacent)

**Why it's in the skill:** AI pads sentences with phrases that have no informational content ("In order to", "At this point in time", "In today's fast-paced world") because training data rewards length and formality.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): "In order to" → "To", "Due to the fact that" → "Because", "At this point in time" → "Now".
- Grammarly: "Transitions and Structured Phrases" — "That being said…", "At its core…", "From a broader perspective…".
- Guo: "vapid openers and transitions" — "As technology continues to evolve", "In today's fast-paced world", "At the end of the day".
- Kriss/NYT: model "trying to write well" by reaching for surface markers of formality.

### 23. Excessive hedging

**Sources:** Wikipedia "Signs of AI writing"; Grammarly; Shankar (adjacent); Abdulhai (adjacent); Stanford HAI (adjacent)

**Why it's in the skill:** AI stacks qualifiers because hedging is a low-risk default in RLHF; result is sentences that commit to nothing.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): over-qualifying to the point where sentences commit to nothing.
- Grammarly: "Qualifiers and Softening Words" — "Generally speaking", "Typically", "Tends to", "Arguably", "To some extent", "Broadly speaking".
- Shankar: vagueness as core AI craft failure.
- Abdulhai: ~70% increase in essay neutrality under heavy LLM use.
- Stanford HAI: detector-bias warning supports clustering signal not verdict (non-native English writers may also hedge more).

**Notes:** Stanford HAI caveat load-bearing: hedging alone is not proof, only clustering signal.

### 23a. False concession hedges

**Sources:** Chiang (New Yorker / Longreads 2023, via Vollmer); Vollmer ("I Asked the Machine to Tell on Itself", conduit); Wikipedia "Signs of AI writing"; Abdulhai (adjacent)

**Why it's in the skill:** Specific shape of hedging where AI stages two abstract positions ("While critics argue…, supporters say…") and lands in a bland middle. Vollmer flagged this as item 2 of his "Gaps Worth Adding" review during the 2026-04-27 source pass, citing Chiang's lossy-compression framing as the upstream conceptual basis.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Chiang ("ChatGPT Is a Blurry JPEG of the Web", New Yorker / Longreads, Feb 2023; "Why A.I. Isn't Going to Make Art", 2024; cited by Vollmer for the false-concession pattern): diagnoses the appearance of engaging with nuance while saying nothing as a lossy-compression artefact — LLMs approximate the centre of mass of training data, producing the average position rather than a stance.
- Vollmer ("I Asked the Machine to Tell on Itself", https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself, Section III.18; conduit for Chiang): frames the move as "appearing to engage with nuance while saying nothing".
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): tolerance note explicit — "Real nuance names the evidence, stakes, and tradeoffs."
- Abdulhai: LLMs systematically remove content making particular claims, edit essays toward neutral.

### 24. Generic positive conclusions

**Sources:** Wikipedia "Signs of AI writing"; Shankar (adjacent); Caroll (adjacent); Guo (adjacent)

**Why it's in the skill:** AI ends articles with vague upbeat closers ("The future looks bright") that could be appended to any piece on any topic.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): vague upbeat endings appendable to any article.
- Shankar: empty paragraph endings as one of the strongest AI craft tells.
- Caroll: AI defaults to "warm fuzzies not lectures".
- Guo: "surface polish with nothing underneath" is AI's signature.

**Notes:** Distinct from #37 (neutrality collapse, which removes stance). #24 is the *addition* of empty optimism.

### 25. Staccato rhythm in extended contexts

**Sources:** Shankar (primary); Wikipedia "Signs of AI writing"; Guo (adjacent); Caroll (adjacent); Corpus (sentence-length variance)

**Why it's in the skill:** AI clusters short sentences in predictable positions and produces uniformly short, single-clause sentences that flatten rhythm.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Shankar: "flat rhythm" as core AI craft failure.
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): tolerance note — staccato is fine for character voice, panic, comedy.
- Guo: "AI-generated content often has a repetitive structure. Sentences are roughly the same length."
- Caroll: "One 'action' per sentence is easier to follow… simple sentence structure too."
- Corpus: humans 17.0 stdev vs AI 7.3 (fresh) / 7.5 (rewrite), 2.3× gap. Mean: humans 23.3 vs AI ~13.

---

## Sensory and atmospheric (26-28)

### 26. Ghost / spectral language

**Sources:** Kriss/NYT; Corpus

**Why it's in the skill:** Kriss documents AI's defaulting to spectral, ghostly, shadowy imagery whenever it reaches for depth; corpus confirms ghost-spectral density fires on AI fresh-writes but not humans in same register.

**How AI uses it:** both
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Kriss/NYT: "AIs are absolutely obsessed with ghosts. In machine-written fiction, everything is spectral." Pebbles essay, AI-grief metafiction count.
- Corpus: AI fresh 2/5, humans 0/5, AI rewrite 0/5. Clean AI-fresh-only signal.

### 27. Quietness obsession

**Sources:** Kriss/NYT

**Why it's in the skill:** Kriss documents AI inserting quietness, stillness, and soft humming where it doesn't belong, often against scene logic, with measurable density (10 instances of "quiet" in a 759-word pebbles essay).

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Kriss/NYT: "AIs love quietness, and for no obvious reason." 10 uses of "quiet" in 759 words. Seven instances of "quiet"/"hum"/"echo"/"ghosts" in 1,100-word AI-grief metafiction.

### 28. Forced synesthesia

**Sources:** Kriss/NYT

**Why it's in the skill:** Kriss diagnoses AI synesthesia as unanchored: model has no physical experience, sensory vocabulary attaches to immaterial subjects.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Kriss/NYT: "Hands humming with the color of grief." Sorrow tasting of metal. Woolf contrast: "great plateful of blue water" works because Woolf had stood before a view and sat to a meal; AI has done neither.

---

## Structural tells (29-32, 31a, 38)

### 29. Mid-sentence rhetorical questions

**Sources:** Guo; Kriss/NYT

**Why it's in the skill:** Guo identifies short questions dropped mid-paragraph and answered immediately as a distinct AI tic, including "The real X?" reveal patterns.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Guo: "But now? You won't be able to unsee this one." "The solution? It's simpler than you think."
- Kriss/NYT: self-interrupting questions — stopping mid-sentence to ask itself questions.

### 30. Generic / ungrounded metaphors

**Sources:** Guo; Kriss/NYT; Caroll

**Why it's in the skill:** Three sources converge: AI metaphors are plausible but specific to nobody, drawing from the statistical middle.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Guo: "AI metaphors are… plausible. Generic. They gesture toward meaning without quite achieving it."
- Kriss/NYT: AI metaphors unanchored because AI cannot experience the world.
- Caroll: genericness as deeper structural pattern under many surface tells.

### 31. Excessive list-making

**Sources:** Guo; Shankar

**Why it's in the skill:** Guo names list-making as structural tell driven by RLHF training; result is prose converted to bullet points where content doesn't warrant it.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Guo: "ChatGPT loves making lists." Attributes to RLHF: "people are more inclined to be impressed by answers that contain bullet points."
- Shankar: over-bulleting listed among bad-AI-writing markers.

### 31a. Unicode flair

**Sources:** Guo (Artificial Ignorance Substack); Vollmer ("I Asked the Machine to Tell on Itself", conduit); Wikipedia "Signs of AI writing"; Corpus

**Why it's in the skill:** Guo names Unicode bold/italic substitution and decorative arrows as "almost exclusively an AI thing" in essay register. Vollmer flagged the pattern in item 4 of his "Gaps Worth Adding" review (2026-04-27), citing Wikipedia. Corpus confirms.

**How AI uses it:** frequency-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Guo: "most authors aren't going out of their way to grab Unicode arrows or multiplication signs… almost exclusively an AI thing."
- Vollmer ("I Asked the Machine to Tell on Itself", Section V.29; conduit for Wikipedia citation): "Unicode flair in wrong places — bold Unicode characters (𝗯𝗼𝗹𝗱), rightward arrows →, Unicode bullets •". Identified Wikipedia "Signs of AI writing" cleanup project as the source flagging these as strong tells.
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): names "unrequested headings/lists/Unicode flair" as cluster signal.
- Corpus: AI fresh 2/5, humans 0/5, AI rewrite 0/5. Example: "⸻" separators.

### 32. Dramatic narrative transitions

**Sources:** Guo

**Why it's in the skill:** Guo identifies standalone sentences ("Something shifted." "Everything changed.") that claim a narrative turning point without earning it.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Guo: "Serious, narrative-shifting transitions that come out of nowhere." Filed under "unearned profundity".

### 38. Section scaffolding

**Sources:** Wikipedia "Signs of AI writing"

**Why it's in the skill:** AI-generated articles with numbered sections often repeat identical structural labels ("How to make this work:") in each section; repetition itself is the tell.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Wikipedia "Signs of AI writing" (editor consensus, no upstream source): identical subheadings repeated across sections. Repetition is the tell.

---

## Voice and register (33-37, 35a)

### 33. Countdown negation

**Sources:** Practitioner guides (aidetectors.io, seoengine.ai, SAGE)

**Why it's in the skill:** Practitioner detection guides identify a sustained "It wasn't X. It wasn't Y. It was Z." build-up as distinct AI rhetorical move that fakes suspense across multiple sentences.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Practitioner guides: "Dramatic countdown negation — AI negates two or more things before revealing the actual point, creating false suspense."

**Notes:** Distinguished from #9 (negative parallelism) — #9 is single-sentence flip, #33 is multi-sentence dramatic build.

### 34. Per-paragraph miniature conclusions

**Sources:** Shankar; practitioner guides

**Why it's in the skill:** Shankar names "empty paragraph endings" as one of the strongest craft tells; practitioner guides confirm same pattern as miniature wrap-ups handing off perfectly.

**How AI uses it:** both
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Shankar: "empty paragraph endings" listed alongside bad sentence subjects, orphaned demonstratives, over-bulleting.
- Practitioner guides: "every paragraph ends with a summary that hands off perfectly."

**Notes:** Closing-phrase list ("That is why…", "The takeaway is…", "Ultimately…") — three or more = same landing every time. Paragraph-block uniformity (65-85 word blocks) related.

### 35. Tonal uniformity / register lock

**Sources:** Practitioner guides; Caroll; Guo

**Why it's in the skill:** Cross-source consensus describes AI picking one register and never breaking from it; consistency itself is the tell.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Practitioner guides: "AI picks a register (professional-casual, academic-accessible) and stays there. The consistency is the tell."
- Caroll: AI defaults to "warm fuzzies not lectures", uniformly at 5th-6th grade level regardless of audience.
- Guo: "Sentences are roughly the same length. Paragraphs follow the same rhythm." Fixed point-of-view.

**Notes:** Manual self-audit only. Sentence-length variance (17.0 vs 7.3) is related quantitative signal.

### 35a. Orphaned demonstratives

**Sources:** Shankar (sh-reya.com/blog/ai-writing); Vollmer ("I Asked the Machine to Tell on Itself", conduit)

**Why it's in the skill:** Shankar names directly as core craft tell: AI starts sentences with "This highlights…" / "This underscores…" where "this" points vaguely back at a whole previous paragraph. Vollmer surfaced this as item 1 of his "Gaps Worth Adding" review during the 2026-04-27 source pass, citing Shankar; the pattern was added to `human-eyes/references/patterns.md` and `human-eyes/grade.py` (`check_orphaned_demonstratives`, `check_this_chains`) in commit 9ce1cec as a result.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Shankar (sh-reya.com/blog/ai-writing, cited by Vollmer for orphaned demonstratives): "Readers are better guided when the subject matches the main idea". Lists the pattern as a direct craft tell that supports both self-audit and programmatic checks.
- Vollmer ("I Asked the Machine to Tell on Itself", Section II.10 "Bad-Subject Problem"; conduit for Shankar): "Orphaned demonstratives; grammatical subject ≠ actual topic. Sentences leading with 'This' or 'That' with no clear antecedent."

### 36. Faux specificity

**Sources:** Practitioner guides; Caroll; Guo

**Why it's in the skill:** AI provides examples that feel specific without being specific — constructed from genre conventions rather than lived experience.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Practitioner guides: "Faux specificity — AI gestures at the specific while remaining safely abstract."
- Caroll: "A machine has no stories to tell, so it has to generalize."
- Guo: "Human metaphors tend to be either highly specific or culturally resonant. AI metaphors are… plausible. Generic."

### 37. Neutrality collapse

**Sources:** Abdulhai et al.

**Why it's in the skill:** Headline finding of Abdulhai et al. — strongest empirical evidence to date that LLMs subtract argumentative stance, defaulting to balanced treatment even when writer had a clear position.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Abdulhai: ~70% increase in neutral essays under heavy LLM use; LLMs systematically removed content making particular claims; even when instructed to fix grammar only, frequently changed conclusions. Companion findings: 50% pronoun depletion; semantic drift in minimal edits.

**Notes:** Distinct from #24 — #24 adds bland optimism, #37 strips opinion. ArgRewrite design is matched-pair counterfactual.

---

## Additional (39-41)

### 39. Template and placeholder residue

**Sources:** Gmelius (primary, via Vollmer)

**Why it's in the skill:** Unfilled placeholders like `{client_name}`, `[Company Name]` are unambiguous generation/template residue. Catalogued in Gmelius's "AI-isms in email" list and surfaced for the skill via Vollmer's article during the 2026-04-27 source-review pass.

**How AI uses it:** frequency-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Gmelius (catalog of "AI-isms" in email, cited in Vollmer "I Asked the Machine to Tell on Itself", Section VI.F "In Emails and Business Writing"): "Unedited placeholders left in: 'Hi {client_name},'". Pattern added to human-eyes/references/patterns.md and human-eyes/grade.py on 2026-04-27 (commit 9ce1cec) following review of Vollmer's article.

### 40. Rubric echoing

**Sources:** Vollmer (primary)

**Why it's in the skill:** AI-generated student essays mirror assignment language ("the author creates a tone", "I can tell because") instead of analysing the text. Catalogued from Vollmer's reporting on what teachers notice in AI-generated student work.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**
- Vollmer ("I Asked the Machine to Tell on Itself", https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself, Section VI.C "In Student Writing"): "Rubric-language echoing — the essay names the rubric's own criteria with suspicious fluency." Framed as part of what teachers report noticing; Vollmer presents this as his own observation without crediting an external source. Pattern added to human-eyes/references/patterns.md and human-eyes/grade.py on 2026-04-27 (commit 9ce1cec) following review of Vollmer's article.

**Notes:** Genre-bound — fires in academic submissions.

### 41. Genre-specific manual checks

**Sources:** Walsh (arxiv 2410.15299); Aranya/Poetly (Substack); Clarke (Clarkesworld editor); Germain (Medium); Dhillon et al. (arxiv 2510.13939); Waltzer et al. (Wiley 2023); Hastewire; Jiang & Hyland (SAGE 2025); Gmelius; Bynder (2024); Futurism / PBS NewsHour; Kriss/NYT (adjacent); Vollmer ("I Asked the Machine to Tell on Itself", conduit for several genre sub-patterns)

**Why it's in the skill:** Meta-pattern collecting genre-bound checks too unreliable for regex but essential to self-audit. Vollmer's article (Section VI, "Domain-specific tells") groups these by genre and cites specialist sources for each — the strongest single-article synthesis of genre-specific AI tells available.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** external-only
**Severity:** [pending — U1d]

**Source claims:**

*Poetry (VI.A):*
- Walsh ("AI poetry: a stylistic analysis", arxiv:2410.15299; cited by Vollmer): computational study of 5,700 ChatGPT poems vs 3,700 from Poetry Foundation and Academy of American Poets; AI poetry shows "much more constrained and uniform" form — penchant for rhyme, quatrains, iambic meter, first-person plural ("we/us/our"), and signature vocabulary ("heart", "embrace", "echo", "whisper").
- Aranya (Poetly Substack, poetly.substack.com; cited by Vollmer): aphorism density, negate-and-redefine structure, abstraction drift, mood-word accumulation ("ache, hollow, tether, linger, fragile, fractured, ember, bloom, cradle, ruin, veil, threadbare").
- Kriss/NYT (poetry sub-pattern indirectly): most readers prefer AI poems to Shakespeare/Eliot/Dickinson.

*Fiction (VI.B):*
- Clarke (Clarkesworld editor; cited by Vollmer): closed submissions Feb 2023 after 500/1200 AI submissions in a single week. "Bad in ways no human has been bad before… boring… flat… no subtext or layers… the surface is grammatically perfect, and therein lies the problem."
- Germain (Medium; cited by Vollmer): parenthetical stage-direction tics in GPT-3.5 dialogue ("(defensive)", "(frustrated)").
- Dhillon et al. (arxiv:2510.13939; cited by Vollmer): MFA students vs LLMs study; expert readers detect AI via "clichés, purple prose, too much exposition, lack of subtext, mixed metaphors".

*Student writing (VI.C):*
- Waltzer et al. (Wiley 2023; cited by Vollmer): 69 high school teachers + 140 students; teacher accuracy 70%, student accuracy 62%; "well-written student essays especially hard to differentiate"; confidence uncorrelated with accuracy.
- Hastewire (cited by Vollmer): teachers report vocabulary/level mismatch, missing citations, rubric-language echoing, one-paste Google Docs history.

*Academic (VI.D):*
- Jiang & Hyland (SAGE 2025; cited by Vollmer): ChatGPT-generated argumentative essays contained significantly fewer engagement markers (questions, asides, reader address) than human student essays.

*Journalism (VI.E):*
- Futurism / PBS NewsHour (cited by Vollmer): CNET's 77 AI-generated finance articles (2023, corrections on >50%); Sports Illustrated's AI-generated reviews under AI-generated author headshots.

*Email and business (VI.F):*
- Gmelius (gmelius.com/blog/can-customers-tell-an-email-is-written-using-generative-ai; cited by Vollmer): formulaic openings, unedited placeholders, three-sentence paragraphs, missing colons/semicolons.
- Bynder (2024 consumer study; cited by Vollmer): 55% of U.S. consumers correctly identify AI-generated marketing.

**Notes:** Whole pattern explicitly manual-only. Vollmer's Section VI is the most heavily sourced genre-by-genre synthesis available; per-genre primary sources should be preserved in the README's References section under a "Domain-specific" subsection.

---

## Non-numbered grader checks

### Em-dashes density (`no-em-dashes`)

**Sources:** Merrill, Chen, Kumer (Washington Post 2025); Edwards (Ars Technica 2025); Kriss/NYT; Guo; Caroll (adjacent); Wikipedia "Signs of AI writing"; Corpus

**Why it's in the skill:** Em dashes are now culturally entrenched AI fingerprint because the model was trained to drench prose with them as a quality marker; humans use them legitimately, but at AI's frequencies and in AI's contexts they read as machine-produced. The Washington Post's Merrill et al. quantitative analysis and Ars Technica's reporting on OpenAI suppressing em-dashes in GPT-5.1 confirm the cultural recognition.

**How AI uses it:** both
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Merrill, Chen, Kumer ("What are the clues that ChatGPT wrote something? We analyzed its style.", Washington Post, 13 Nov 2025; cited by Wikipedia for em-dash analysis): quantitative style analysis tracking em-dash frequency.
- Edwards ("Forget AGI — Sam Altman celebrates ChatGPT finally following em dash formatting rules", Ars Technica, 14 Nov 2025; cited by Wikipedia): documents OpenAI's GPT-5.1 attempt to suppress em-dashes in response to user complaints — direct evidence the pattern is recognised as an AI tell.
- Kriss/NYT (cited by Wikipedia): "the em dash is more likely to appear in texts marked as well-formed, high-quality prose, and if this punctuation mark appears with increased frequency in high-quality writing, then one way to produce high-quality writing is to absolutely drench it with the punctuation mark."
- Guo: "Em dashes are something very few humans use in day-to-day writing." Reddit em-dash use tripled in one year across tech/startup subreddits.
- Wikipedia "Signs of AI writing" (citing Merrill, Kriss, Edwards): LLMs use em dashes more frequently than human nonprofessional text, often formulaically.
- Corpus: AI fresh 4/5 fire, AI rewrite 5/5 fire, humans 2/5 fire. Mean count humans 15.0 vs AI fresh 11.8 vs AI rewrite 11.2. Fire rate separates groups, raw counts do not.

**Notes:** Corpus flags recalibration question. In published long-form essay em-dashes are convention.

### Markdown headings density (`no-markdown-headings`)

**Sources:** Grammarly; Corpus

**Why it's in the skill:** Generated articles arrive packaged with `##` section scaffolding and title-case headings, signalling assistant-formatted artefact rather than continuous prose.

**How AI uses it:** appropriate-use-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Grammarly: "predictable formatting (title-case headings, bullet points)" as structural AI tell.
- Corpus: humans 5/5, AI fresh 1/5, AI rewrite 3/5 — **inverted in long-form essay**.

**Notes:** Currently mis-calibrated for long-form essay. Genre-aware thresholding queued.

### Anaphora — repeated sentence openings (`no-anaphora`)

**Sources:** Caroll (adjacent); Guo (adjacent); Grammarly (adjacent); Corpus

**Why it's in the skill:** Three or more consecutive sentences opening with the same word read as template rhythm rather than rhetorical anaphora.

**How AI uses it:** frequency-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Caroll: AI defaults to short, single-clause sentences with recognisable rhythm.
- Guo: "Sentences are roughly the same length. Paragraphs follow the same rhythm. The cadence never varies."
- Grammarly: "repetitive phrasing" as AI text characteristic.
- Corpus: humans 2/5, AI fresh 4/5, AI rewrite 3/5 — clear AI lean.

### Vocabulary diversity / type-token ratio (`vocabulary-diversity`)

**Sources:** Practitioner guides; Corpus

**Why it's in the skill:** AI recycles high-probability terms, producing measurably lower vocabulary diversity than human writers.

**How AI uses it:** frequency-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Practitioner guides: "Low type-token ratio — AI recycles high-probability terms… Psycholinguists track this as unique-words ÷ total-words."
- Corpus: humans TTR 0.33, AI fresh 0.40, AI rewrite 0.50. By fire rate: humans 3/5, AI fresh 2/5, AI rewrite 0/5 — **inverted in long-form**.

**Notes:** Currently mis-thresholded for long-form. Threshold needs genre-aware tuning.

### Sentence-length variance (`sentence-length-variance`)

**Sources:** Caroll; Guo; stylometry research (Przystalski/Zaitsu/Bisztray); Grammarly; Corpus

**Why it's in the skill:** AI clusters tightly around a single sentence-length mean; human prose shows wide variance. Low standard deviation is one of the cleanest measurable rhythm tells.

**How AI uses it:** frequency-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Caroll: short, single-clause sentences contribute to recognisable rhythm.
- Guo: "Sentences are roughly the same length. The cadence never varies."
- Stylometry research: stylometric features reliably distinguish LLM from human in short samples.
- Corpus: humans stdev 17.0 vs AI fresh 7.3 vs AI rewrite 7.5 — 2.3× gap, strongest single separator. Mean: humans 23.3 vs AI 13.2.

**Notes:** Currently mis-thresholded. Grader passes when `sd > 4`, which trips trivially against humans (17.0) and AI (7.3). Threshold needs to move up.

### Paragraph-length variance (`paragraph-length-uniformity`)

**Sources:** practitioner guides; Guo; Corpus

**Why it's in the skill:** AI long-form settles into near-identical paragraph blocks with uniform word counts; humans show uneven pressure across paragraphs.

**How AI uses it:** frequency-coded
**Evidence basis:** both
**Severity:** [pending — U1d]

**Source claims:**
- Practitioner guides: per-paragraph miniature conclusions handing off perfectly.
- Guo: "Paragraphs follow the same rhythm."
- Corpus: humans paragraph-length stdev 37.3 vs AI fresh 23.2 vs AI rewrite 21.4 — 1.6× gap.

**Notes:** Implementation requires 7+ substantial paragraphs (≥25 words); passes when CV ≥ 0.18.
