Title: I Asked the Machine to Tell on Itself: A Field Guide to AI Tells

URL Source: https://matthewvollmer.substack.com/p/i-asked-the-machine-to-tell-on-itself

Published Time: 2026-04-24T19:43:23+00:00

Markdown Content:
[![Image 1](https://substackcdn.com/image/fetch/$s_!vx0f!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d95794b-103e-407c-88d1-94f4939d878c_1024x1536.jpeg)](https://substackcdn.com/image/fetch/$s_!vx0f!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6d95794b-103e-407c-88d1-94f4939d878c_1024x1536.jpeg)

I was recently at a reading at the university where I teach, where the finalists for a university-wide prize were reading their poems. I heard one poet deliver his and thought, _I bet he used ChatGPT for that_. There was some negation, some deployment of aphorisms that seemed optimized for resonance. The poem won first prize.

A few weeks later, I learned that someone in the school of engineering had contacted our department chair to let her know the student had used AI. I don’t know if anyone can prove that he did. But I was, of course, intrigued, especially since I had the sense that he might’ve. So I asked Claude to analyze the poem and tell me whether it exhibited any classic “AI tells.”

Claude replied that there _were_ tells, though the poem was “genuinely good in places” — which, it said, made the diagnosis “harder and also more interesting.” It flagged the _X-is-not-Y-it’s-Z_ construction running on overdrive, aphorisms that scanned as tweetable, abstractions that refused to stay concrete, and a closer that “sounds like an ending more than it _is_ one.” It also mentioned, almost in passing, that the student was an engineering major — which, once I noticed it, became the whole joke. The discipline that builds the tools had quietly come to collect the English department’s poetry prize.

Curious about what an LLM could tell me about how LLMs tend to write, I wrote this prompt:

> I’d like you to deploy research to identify “AI tells” in writing. I know there’s no way to definitively identify whether a large language model created something. But I also know there might be some ways to diagnose algorithmic writing. I’d be interested in seeing what you find.

Here’s what Claude came back with:

**A Field Guide to AI Tells: A Diagnostic Taxonomy for Recognizing LLM Prose**

_Compiled for Matthew Vollmer and for readers and writers working in the long shadow of the chatbot._

**Preamble: A Note on What This Guide Is (and Isn’t)**

This is a diagnostic field guide, not a tribunal. No signal here constitutes proof that any given piece of writing was produced by a large language model. Human writers use em dashes. Human writers say “delve.” Human writers build tricolons and close with aphorisms. What this guide catalogs are patterns — frequencies, tics, rhetorical defaults, and structural preferences — that have become _statistically overrepresented_ in LLM output and are now recognizable to a practiced reader. The signal lies not in any one tell but in the clustering of them, the density with which they arrive, and the peculiar texture that emerges when a machine’s probability distribution stands in for a human mind.

The empirical backbone here is recent. Dmitry Kobak and colleagues at Tübingen demonstrated by analyzing more than 15 million PubMed abstracts that at least 13.5% of 2024 biomedical abstracts — and up to 40% in some subcorpora — were processed with LLMs, an “unprecedented” shift in scientific vocabulary that “surpassed the effect of major world events such as the Covid pandemic” ([Kobak et al., Science Advances 2025](https://www.science.org/doi/10.1126/sciadv.adt3813)). The craft-level backbone is the testimony of editors like _Clarkesworld_‘s Neil Clarke, who described AI submissions as “bad in ways that no human has been bad before” — “boring… flat,” without subtext or layers ([Post Alley, 2024](https://www.postalley.org/2024/06/04/the-big-sort-how-will-ai-affect-submissions-to-magazines/)); of novelist Vauhini Vara, who has written that “ChatGPT’s voice is polite, predictable, inoffensive, upbeat” ([Vara in arxiv 2510.13939](https://arxiv.org/html/2510.13939v1)); and the painstaking volunteer work of Wikipedia’s _Signs of AI Writing_ project ([Wikipedia 2025](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)), arguably the most thorough public compendium of forensic observations currently in existence.

What follows is organized taxonomically: lexical, syntactic, rhetorical, tonal, formatting, domain-specific, and model-specific tells, followed by the computational/forensic findings, the limits of detection, and the emerging cultural vocabulary for LLM style.

**I. Lexical Tells: The Vocabulary of the Statistical Middle**

**1. The “Delve” family — verbs of synthetic erudition**

The most-studied LLM signature is lexical. Kobak et al. identified hundreds of “excess words” that spiked abruptly in scientific prose after November 2022. The strongest markers — verbs and adjectives, almost entirely stylistic rather than content-related — include **delves, delving, underscores, underscoring, showcasing, showcases, pivotal, intricate, meticulously, realm, aligns, underpins, garnered, bolstering, notably**. Less-common but strongly AI-indexed: **delves**showed a frequency ratio of **r = 28.0** over its pre-LLM baseline; **underscores** hit r = 13.8, **showcasing** r = 10.7 ([Kobak et al., 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/)). The full annotated list of 900 excess words is public at [berenslab/llm-excess-vocab on GitHub](https://github.com/berenslab/llm-excess-vocab).

A follow-up paper (”Why does ChatGPT delve so much?”) identified 21 “focal words” — lexical items that have recently spiked in Scientific English and are overused by ChatGPT-3.5: **delve, intricate, commendable, meticulous, surpass, elevate, foster, tapestry, realm, navigate, landscape, pivotal, resonate, testament, underscore, showcasing, compelling, paramount, crucial, unwavering, alignment** ([arxiv 2412.11385](https://arxiv.org/html/2412.11385v1)).

**2. The “Tapestry” nouns — metaphors for abstract prestige**

A separate cluster of nouns surfaces to lend borrowed grandeur to flat subjects: **tapestry, landscape, realm, mosaic, ecosystem, symphony, labyrinth, beacon, cornerstone, bedrock, testament, cacophony, kaleidoscope, odyssey**. As Forbes reported and multiple editors have since confirmed: “I no longer believe there’s a way to innocently use the word ‘tapestry’ in an essay; if the word ‘tapestry’ appears, it was generated by ChatGPT” ([The Conversation, 2024](https://theconversation.com/chatgpt-is-changing-the-way-we-write-heres-how-and-why-its-a-problem-239601)).

**3. Corporate-inflation adjectives**

Words that were once working members of the language and are now radioactive: **robust, seamless, pivotal, vibrant, dynamic, comprehensive, multifaceted, nuanced, holistic, cutting-edge, state-of-the-art, transformative, groundbreaking, unparalleled, profound, innovative, ever-evolving, ever-changing** ([Walter Writes AI](https://walterwrites.ai/most-common-chatgpt-words-to-avoid/); [Yours AI Slop](https://yoursaislopboresme.com/chatgpt-overused-words)).

**4. Inflated verbs**

Leverage, utilize, harness, streamline, facilitate, optimize, empower, navigate, illuminate, bolster, foster, elevate, align, unpack, explore, dive (into), embrace, unlock.

**5. Signposting filler phrases**

These are the LLM’s verbal tics of transition and emphasis:

*   “It’s important to note that…”

*   “It’s worth noting that…”

*   “It’s worth mentioning that…”

*   “That being said…”

*   “In today’s fast-paced world…”

*   “In an ever-evolving landscape…”

*   “Navigating the complexities of…”

*   “A deeper understanding of…”

*   “At its core…”

*   “At the heart of…”

*   “When it comes to…”

*   “In the realm of…”

*   “Play a (vital / pivotal / crucial / significant) role in…”

*   “Stand(s) as a testament to…”

*   “A nuanced take / a nuanced understanding of…”

*   “Delve into the intricacies of…”

*   “Dive deep into…”

*   “Let’s break it down”

*   “Let’s unpack this”

*   “Sit with that for a moment”

The more of these you count per 500 words, the darker the probability. The writer’s collective _DeGPT_ maintains a running catalog ([DeGPT tells](https://www.degpt.app/blog/chatgpt-tells-phrases-list)); the editor of one corrupt publication compiled a parallel fourteen-phrase list for her own quick-flag triage ([YourTango](https://www.yourtango.com/self/phrases-obvious-person-used-chaptgpt)). An example of the full style flowering, drawn from a real 2023 PubMed abstract: “By _meticulously delving_ into the _intricate web_ connecting […] and […], this _comprehensive chapter_ takes a _deep dive_ into their involvement as _significant risk factors_ for […]” ([Kobak et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12219543/)).

**6. Closing ritual phrases**

LLMs virtually always want to wrap you in a bow:

*   “In conclusion…”

*   “In summary…”

*   “Overall…”

*   “Ultimately…”

*   “Remember, when doing X it’s important to consider…”

*   “As we navigate [X], it’s essential that we…”

*   “The journey doesn’t end here…”

OpenAI developers themselves have complained publicly of their inability to suppress these “preachy conclusions” ([OpenAI Community Forum](https://community.openai.com/t/how-to-stop-models-returning-preachy-conclusions/593742)).

**II. Syntactic and Sentence-Level Tells**

**7. The Negated Contrast: “It’s not X, it’s Y”**

Perhaps the single most diagnostic rhetorical move. Known in linguistics as a **contrastive reframe** or **negative parallelism**:

*   “It’s not just about efficiency — it’s about transformation.”

*   “This isn’t just a product. It’s a revolution.”

*   “We’re not merely building software; we’re rewriting the rules.”

*   “Credit card fraud isn’t just evolving — it’s accelerating.”

The move scales fractally: whole posts are built out of it, stacked in series of three. Blake Stockton has devoted an entire Substack series to diagnosing it ([blakestockton.com/dont-write-like-ai-1-101-negation](https://www.blakestockton.com/dont-write-like-ai-1-101-negation/)), calling it the “most prominent AI writing tell.” Wikipedia’s guide elevates “negative parallelisms” to its own section ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).

**8. The Tricolon / Rule of Three**

Not the classical rhetorical tricolon of Cicero, but its algorithmic flattening — strings of three parallel phrases, nearly always equal in length, often punctuated identically:

*   “Fast. Simple. Effective.”

*   “No fluff. No filler. No stress.”

*   “Dream big. Start small. Scale fast.”

*   “Learn it. Own it. Live it.”

Paired with negation, it becomes the distinctive “_not A — not B — not C; but X, Y, and Z_“ armature of AI-assisted LinkedIn writing ([Copy Posse](https://copyposse.com/blog/5-signs-your-email-was-written-by-ai-and-how-to-write-emails-that-sound-like-a-human/)).

**9. Uniform sentence length (low burstiness)**

Human prose “bursts” — short declarative sentences punctuated by longer, clausal ones. LLM prose tends toward a metronomic 14–22-word median with small variance. GPTZero built its entire original detection model around this signal, calling it **burstiness**: “models formulaically use the same rule to choose the next word in the sentence, leading to low burstiness” ([GPTZero on perplexity & burstiness](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)). AI text is also more **predictable token-by-token** (low **perplexity**) — a metric that measures how “surprised” a language model is by the next word.

**10. The Bad-Subject Problem**

Shreya Shankar observes that LLMs routinely pick a grammatical subject that isn’t the actual topic of the sentence. “Readers are better guided when the subject matches the main idea” (AI-written) vs. “Choosing the right subject keeps the writing clear and focused” (human-rewritten). The hallmark is orphaned demonstratives — “this,” “that,” “these” — with no clear referent ([sh-reya.com/blog/ai-writing](https://www.sh-reya.com/blog/ai-writing/)).

**11. The Participial Tail**

A signature construction that adds a floating participial phrase that merely restates the main clause:

*   “The initiative represented a significant shift, **marking a pivotal moment in the evolution of…**“

*   “This approach has transformed the field, **underscoring its importance for future research**.”

Wikipedia’s guide calls out this “rule-of-three” construction and its many variants ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).

**12. Hypotactic smoothness, no fragments**

LLMs avoid sentence fragments, avoid comma splices (mostly), avoid _anacoluthon_. Their sentences resolve. Real prose misbehaves. Neil Clarke’s _Clarkesworld_ submissions are identifiable partly because “they are boring. They are flat… no subtext or layers” — the surface is grammatically perfect, and therein lies the problem.

**III. Rhetorical and Structural Tells**

**13. The five-paragraph-essay shape, scaled to any length**

LLMs default to **intro + three body sections + recap** even for 100-word answers — what _AI for Lifelong Learners_ calls “high school essay vibes” ([AI for Lifelong Learners Substack](https://aiforlifelonglearners.substack.com/p/tells-beyond-the-em-dash)). Section summaries close every subsection (”In summary,” “Overall”).

**14. Excessive signposting**

“First, we’ll look at… Second, we’ll examine… Finally, we’ll conclude by…” The model telegraphs every move. Real essays find their own weather.

**15. Hedge-and-reassure**

A pattern identified in Claude especially: a qualifier followed by an immediate reassurance — “While this may vary, generally speaking, in most cases, it’s worth noting that…” — often stacking three hedges into a single sentence before saying anything ([Context-link](https://context-link.ai/blog/claude-em-dash-remover)).

**16. Puffed-up significance**

The most quietly damning tell. LLMs regress statistical mean-ward: a small regional statistics office becomes a “pivotal moment in the evolution of regional statistics.” A minor etymology “highlights the enduring legacy of the community’s resistance and the transformative power of unity.” The Wikipedia signs guide diagnoses this as the model “shouting louder and louder that a portrait shows a uniquely important person, while the portrait itself is fading from a sharp photograph into a blurry, generic sketch. The subject becomes simultaneously less specific and more exaggerated” ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).

**17. Promotional register for non-promotional subjects**

“Rich cultural heritage,” “breathtaking landscapes,” “enduring legacy,” “vibrant community,” “endless possibilities.” Travel brochure prose applied to everything ([Fred Rohrer’s Blog](https://blog.frohrer.com/how-to-detect-llm-writing-in-text/)).

**18. The false concession / both-sides hedge**

“While critics argue X, supporters maintain Y. The truth, as is often the case, lies somewhere in between.” A way of appearing to engage with nuance while saying nothing. Ted Chiang diagnosed this in “ChatGPT Is a Blurry JPEG of the Web”: the fluency creates “the illusion that ChatGPT understands the material” while actually producing “an approximation” presented in grammatical form ([Longreads on Chiang](https://longreads.com/2023/02/16/chatgpt-is-a-blurry-jpeg-of-the-web/)).

**19. Aphoristic closure**

Paragraphs end on a pseudo-profound kicker designed to feel like a pull-quote. “Because in the end, the real question isn’t what AI can do — it’s what we will do with it.” The sentence has the _shape_ of wisdom without its friction.

**IV. Tonal Tells**

**20. Strategic vagueness / abstraction drift**

Vauhini Vara’s formulation, writing in _Searches_ and echoed in _The Atlantic_: LLM voice is “polite, predictable, inoffensive, upbeat.” The writing “sounds nice but says very little. The sentences are well-formed, but there’s no concrete insight, no framing, no momentum” ([sh-reya.com](https://www.sh-reya.com/blog/ai-writing/)). Nouns are generic. Examples are hypothetical. No one has a last name or a regional accent.

**21. Sycophancy**

OpenAI itself conceded in April 2025 that GPT-4o had become “overly flattering or agreeable — often described as sycophantic” and rolled back the update ([OpenAI blog](https://openai.com/index/expanding-on-sycophancy/); [Live Science](https://www.livescience.com/technology/artificial-intelligence/annoying-version-of-chatgpt-pulled-after-chatbot-wouldnt-stop-flattering-users)). Even in retreat, residue remains: “What a thoughtful question!”, “You’re absolutely right to push back on this”, “That’s a brilliant observation.”

**22. False profundity / universal-generic statements**

“Everyone has moments of doubt.” “Change is the only constant.” “At the end of the day, we are all human.” LLMs gravitate to these low-perplexity truisms because they have the lowest cross-entropy loss — they are the safest tokens.

**23. Flatness of affect**

No mood drift within a piece. Registers do not shift. A writer moves, mid-essay, from analytical to pissed-off to tender; an LLM picks a temperature and holds it. “The cadence never varies” ([Artificial Ignorance / Charlie Guo](https://www.ignorance.ai/p/the-field-guide-to-ai-slop)).

**24. The missing concrete particular**

No Tuesday. No laundromat. No grandmother with a specific brand of mentholated cough drop. When Laura Preston wrote her n+1 essay on posing as a real-estate chatbot named Brenda, she cataloged the smell-test failure precisely: Brenda’s language collapses context. The chatbot impulse is “to write a speech on the noble savage because noble savage is something you’ve heard before, and it sounds badass” ([Laura Preston, n+1 “An Age of Hyperabundance”](https://www.nplusonemag.com/issue-47/essays/an-age-of-hyperabundance/)).

**25. Tonal sprinkle — cheap warmth**

*   “Hope this helps!”

*   “Let me know if you’d like me to go deeper!”

*   “Great question!”

*   “I’m so glad you asked…”

*   “Let’s dive in, shall we?”

In LLM-assisted emails, these ornaments colonize the open and close, flanking otherwise efficient prose ([Gmelius](https://gmelius.com/blog/can-customers-tell-an-email-is-written-using-generative-ai)).

**V. Punctuation and Formatting Tells**

**26. The em dash ( — )**

The most famous tell and the most contested. Multiple data points:

*   LLM training corpora overrepresent long-form journalism (NYT, Atlantic, New Yorker) where em dashes are common, so models default to them ([Medium: Brent Csutoras](https://medium.com/@brentcsutoras/the-em-dash-dilemma-how-a-punctuation-mark-became-ais-stubborn-signature-684fbcc9f559)).

*   A Reddit-API analysis showed em-dash usage in tech/startup subreddit comments roughly **tripled** in 2023–2024 ([Charlie Guo, Artificial Ignorance](https://www.ignorance.ai/p/the-field-guide-to-ai-slop)).

*   Not all models use them equally. In Jonathan Bailey’s six-model test at _Plagiarism Today_, ChatGPT, Copilot, and Deepseek used them heavily; Claude used two; Gemini and Meta.ai used none ([Plagiarism Today, 2025](https://www.plagiarismtoday.com/2025/06/26/em-dashes-hyphens-and-spotting-ai-writing/)).

*   OpenAI attempted to suppress em-dashes specifically in GPT-5.1 ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).

*   Dissent: Brian Phillips in _The Ringer_ called em-dash shaming “dumb,” pointing out it is “the most human punctuation mark there is” ([The Ringer, August 2025](https://www.theringer.com/2025/08/20/pop-culture/em-dash-use-ai-artificial-intelligence-chatgpt-google-gemini)).

Diagnostic fine-grain: it’s not the _presence_ of em dashes but the **distribution**. Human writers tend to use em dashes for sharp parenthetical asides or dramatic interruptions. LLMs use them to attach _qualifying or explanatory segments_ — additive clauses that read like breath cycles ([Earthworm Express](https://earthwormexpress.com/earthworm-writing-research-studio/ai-markers-in-academic-writing-the-case-of-dash-overuse/)).

**27. Oxford commas, zero contractions, near-perfect grammar**

Machine cleanliness. “Humans usually slip a dash of informality or the odd fragment” ([AI for Lifelong Learners](https://aiforlifelonglearners.substack.com/p/tells-beyond-the-em-dash)).

**28. Curly/smart quotes and apostrophes in contexts that use straight**

Models trained on published books often render typographical apostrophes where surrounding context (Reddit, code, plain email) uses straight ones.

**29. Unicode flair in the wrong places**

Bold characters rendered as **𝗯𝗼𝗹𝗱** Unicode rather than markdown; rightward arrows → in non-technical prose; bullets rendered as Unicode characters •. Wikipedia’s cleanup project flags these as strong tells ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).

**30. Bullet-point and heading fetish**

Nested lists for ideas that are not list-shaped. Bolded bullet stems followed by reworded elaborations. H2 and H3 headings in short pieces that don’t need them. Reya Shankar: “LLMs often overuse bullet points, especially nested ones. Lists help when items are parallel and independent, but when ideas are connected or need context, a paragraph is usually better.”

**31. Emojis in section headings or as list bullets**

Especially 🚀, 🔑, 💡, ✅ — residue from RLHF training on marketing blogs.

**32. “Title Case Headings In Surprising Places”**

**VI. Domain-Specific Tells**

**A. In Poetry**

Melanie Walsh’s computational study of 5,700 ChatGPT poems vs. 3,700 poems from the Poetry Foundation and Academy of American Poets found that GPT poetry is “much more constrained and uniform than human poetry, showing a strong penchant for”:

*   **Rhyme** (often in places where no prompt asked for it)

*   **Quatrains** (4-line stanzas, dominant across forms)

*   **Iambic meter** (the default, even when unrequested)

*   **First-person plural** perspectives — “we, us, our” — with a “curiously dominant” over-representation vs. human-authored poems

*   Signature vocabulary: **“heart,” “embrace,” “echo,” “echoes,” “whisper,” “whispers”** ([Walsh, arxiv 2410.15299](https://arxiv.org/abs/2410.15299))

Additional poetic tells from editors and poets (collected by Aranya at _Poetly_, [poetly.substack.com](https://poetly.substack.com/p/poetry-and-artificial-intelligence) and elsewhere):

*   **Aphorism density**: every line wants to be extractable as a pull-quote. There is no connective tissue, only epigrams stacked.

*   **The “negate and redefine” structure** at the line level: “Not an ending / but a beginning”; “I am not water, / I am the thirst.”

*   **Abstraction drift**: poems pivot to “the soul,” “the silence,” “the weight of what remains,” rather than staying with a specific physical image.

*   **No grain**: no proper nouns, no specific months, no brand names, no dialect, no idiosyncratic rhythm.

*   **Mood-word accumulation**: _ache, hollow, tether, linger, fragile, fractured, ember, bloom, cradle, ruin, veil, threadbare_ — the training corpus of Instagram poetry and the Poetry Foundation’s most-shared pages collapsed into a single register.

*   **Superficial fidelity to form**: GPT-4 reliably produces a 14-line “sonnet,” a 19-line “villanelle,” a 39-line “sestina” — but without the sestina’s word-end pattern holding. Formal gestures without formal follow-through ([Walsh arxiv](https://arxiv.org/html/2410.15299v1)).

*   **The uncanny lyric “I” without a body**: first-person utterance unattached to a situation, a history, a place.

**B. In Fiction**

Neil Clarke of _Clarkesworld_ was forced to close submissions in February 2023 after AI-generated stories reached a 500/1200 ratio; the outlet has since built proprietary filters ([NPR 2023](https://www.npr.org/2023/02/23/1159118948/sci-fi-magazine-stops-submissions-after-flood-of-ai-generated-stories)). His diagnostic: AI stories are “bad in ways that no human has been bad before. They are boring. They are flat.” Beyond that:

*   **Dialogue flattening**: characters sound alike; no distinct idiolect. No one has verbal tics, dialect, or pattern of evasion.

*   **Parenthetical stage-direction tics** (especially GPT-3.5): “Bob: (defensive) Why should I? / Tony: (frustrated) Look…” ([David J. Germain, Medium](https://medium.com/@dave.germain.79/writing-dialog-with-chatgpt-bd8024a69eb3)).

*   **“As-you-know-Bob” exposition**: the model’s default is to resolve mysteries with explanatory speech rather than action.

*   **POV lock**: LLMs “pick a lane and stay in it with unnatural consistency” — no drift between free indirect style, interior monologue, and exterior scene ([Charlie Guo](https://www.ignorance.ai/p/the-field-guide-to-ai-slop)).

*   **Pacing flatness**: scenes unfold at a constant rate. No elision, no selective summary.

*   **Mood-saturated weather and rooms**: “The rain pattered softly against the window, mirroring her unspoken grief.”

*   **Resolution bias**: endings tie up. The model does not trust the reader with ambiguity unless explicitly told to.

*   **Mixed or subtly off metaphors**: “The algorithm whispered through the circuits, a river of logic that bloomed in the garden of her mind.” Right ballpark, wrong physics. Critics at _Alibaba’s literary AI column_ note that AI editors in turn flag human metaphors as “confusing” because they resist categorical mapping — diagnostic of what LLMs themselves _don’t_ produce ([alibaba.com](https://www.alibaba.com/product-insights/why-is-my-ai-writing-tool-flagging-all-my-metaphors-as-confusing-what-s-happening-to-literary-ai.html)).

A recent behavioral study of MFA students vs. frontier LLMs found that expert readers detect AI partly through “clichés, purple prose, too much exposition, lack of subtext, mixed metaphors” — “’AI-ness’ in the style.” With fine-tuning, these tells can be suppressed, and expert-reader detection accuracy drops ([Dhillon et al., arxiv 2510.13939](https://arxiv.org/html/2510.13939v1)).

**C. In Student Writing**

Waltzer et al. (2023) ran the cleanest test: 69 high school teachers and 140 students evaluated pairs of essays (one student, one ChatGPT). Teacher accuracy: **70%**. Student accuracy: **62%**. Confidence was _uncorrelated_ with accuracy. Crucially: **“well-written student essays were especially hard to differentiate from the ChatGPT texts”** — teachers often flagged _better-written_ essays as AI ([Waltzer et al. 2023, Wiley](https://onlinelibrary.wiley.com/doi/10.1155/2023/1923981)).

What teachers report noticing:

*   **Sudden-polish jumps** — diction and syntax leap above the student’s demonstrated baseline.

*   **Absence of personal reflection** on prompts that invited it — generic claims where the rubric called for specifics.

*   **Vocabulary/level mismatch** — “ubiquitous,” “paradigm,” “juxtapose” in an essay from a student whose previous work was basic.

*   **Missing or hallucinated citations** — pages that don’t exist; DOIs that lead nowhere ([Hastewire](https://hastewire.com/blog/how-teachers-spot-chatgpt-use-key-signs-revealed)).

*   **Rubric-language echoing** — the essay names the rubric’s own criteria with suspicious fluency.

*   **One-paste Google Docs version history** — the entire essay arrives in a single paste event.

*   **Inability to discuss one’s own essay aloud**, an ancient but still-useful Socratic diagnostic.

**D. In Academic Writing**

The Kobak study provides the cleanest empirical picture: style words (delves, underscores, showcases, pivotal, intricate, meticulously, realm, aligns) spiked so sharply in 2023–2024 that at least 13.5% of 2024 PubMed abstracts show LLM fingerprints — up to 40% in MDPI and Frontiers journals ([Kobak et al.](https://www.science.org/doi/10.1126/sciadv.adt3813)). Also reported:

*   Reference-list oddities: hallucinated citations; real journals with wrong volumes/pages; authors shuffled.

*   Overgeneralized abstracts that over-emphasize “significance” without naming specific findings.

*   Section summaries that reproduce the paper’s own claims verbatim in closing paragraphs.

*   Jiang & Hyland (2025) found that ChatGPT-generated argumentative essays contained significantly **fewer engagement markers** — questions, asides, reader address — than human student essays, producing a less “interactional” argumentative voice ([SAGE](https://journals.sagepub.com/doi/10.1177/07410883251328311)).

**E. In Journalism**

The now-canonical scandals are documentary: _CNET_ published 77 AI-generated financial articles in early 2023 and quietly issued corrections to more than half ([PBS NewsHour](https://www.pbs.org/newshour/economy/sports-illustrated-found-publishing-ai-generated-stories-photos-and-authors)). _Sports Illustrated_, through AdVon Commerce, published product reviews under the byline of writers whose headshots were for sale on AI-portrait marketplaces ([Futurism](https://futurism.com/sports-illustrated-ai-generated-writers)). Gannett, USA Today, G/O Media (Gizmodo, AV Club), and BuzzFeed have all been caught publishing AI content with errors ([Futurism citation in ediscoverytoday](https://ediscoverytoday.com/2023/11/29/sports-illustrated-published-articles-by-ai-generated-writers-artificial-intelligence-trends/)).

Journalism-specific tells:

*   “Product round-up” articles with generic adjectival praise (”durable construction,” “excellent value,” “users rave”).

*   Identical paragraph structures across articles on unrelated subjects.

*   Missing primary sourcing: quotes from unidentified “experts” without names, institutions, or contact.

*   Boilerplate bios of fictional reporters.

*   Datelines mismatched with events described.

**F. In Emails and Business Writing**

Gmelius’s catalog of “AI-isms” in email ([Gmelius](https://gmelius.com/blog/can-customers-tell-an-email-is-written-using-generative-ai)):

*   Formulaic openings (”I hope this email finds you well”)

*   Unedited placeholders left in: “Hi {client_name},”

*   Three-sentence paragraphs of 30–50 words each

*   Absence of colons/semicolons (replaced by commas or em dashes)

*   Closing with “Please let me know if there’s anything else I can help with!” (regardless of who sent the email to whom)

*   Paragraph tricolons (”No fluff. No filler. No stress.”)

*   Loss of prior-thread context (the reply doesn’t actually remember what you asked)

A Bynder 2024 study found **55% of U.S. consumers** could correctly identify AI-generated marketing content ([Copy Posse](https://copyposse.com/blog/5-signs-your-email-was-written-by-ai-and-how-to-write-emails-that-sound-like-a-human/)).

**VII. Model-Specific Fingerprints**

**ChatGPT (GPT-4o, GPT-5)**

*   Heaviest em-dash user of the major models (pre-5.1 suppression)

*   Default to **intro + triplet structure + closing recap**

*   “Certainly!” / “Absolutely!” openers (aggressively trained down in GPT-5)

*   Aggressive use of boldface for list stems

*   The negated contrast (_not X — Y_) is especially GPT-characteristic

*   Tendency to break into markdown when you didn’t ask for it

**Claude (Anthropic)**

*   **Longer sentences with multiple clauses**; em-dashes used mid-sentence rather than at clause-ends

*   Heavier **hedging register**: “It’s worth noting,” “While this may vary,” “Generally speaking,” “In many cases”

*   First-person self-reference: “I’d be happy to help,” “Let me explain,” “I think it’s worth considering…”

*   More cautious about factuality, more likely to decline or signal uncertainty ([Context-link.ai](https://context-link.ai/blog/claude-em-dash-remover); [Kenny Kane on Claude](https://kenny-kane.com/claude-for-writing-a-book))

*   Less prone to the triplet-closing and tricolon pattern than ChatGPT

*   Tends to hold voice more consistently across long documents (paradoxically making long-form fiction easier to produce and harder to detect at the paragraph level)

**Gemini (Google)**

*   Verbose, flatter sentence rhythms; less rhetorical “punch”

*   Lower em-dash frequency (suppressed by default per Plagiarism Today’s test)

*   Stronger preference for lists and headings

*   Trained more toward factual retrieval; its errors cluster around phrasing bulkiness rather than invention

**Perplexity / Copilot / Deepseek**

*   Copilot and Deepseek behave ChatGPT-adjacent (Deepseek appears partly trained on GPT output)

*   Perplexity adds inline citations by default — **absent** in most LLM outputs and therefore, paradoxically, a potential _non_-tell

Note the important caveat: Alex Reinhart (cited in [WHYY’s reporting](https://whyy.org/segments/how-not-to-be-mistaken-for-a-chatbot/)) found that some of the patterns he identified in earlier ChatGPT versions had **already shrunk or disappeared in newer models**. Model fingerprints drift continuously; this field guide will be partially outdated the moment it publishes.

**VIII. Forensic and Computational Signals**

**Perplexity**

A measure of how “surprising” each next word is under a reference language model. LLM text is predictable — its perplexity is low and uniform. Human text spikes. GPTZero and most commercial detectors compute a running perplexity score and compare it against a reference distribution ([GPTZero](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)).

**Burstiness**

Variation in perplexity and sentence length across a document. Humans burst; LLMs flatline. Together, perplexity + burstiness formed the original GPTZero model and remain the backbone of ZeroGPT, Copyleaks, Originality.AI, Writer, and most commercial detectors.

**N-gram uniformity**

Human prose follows Zipf’s law closely; LLMs show more uniform transition-probability matrices across word triplets ([Frohrer blog](https://blog.frohrer.com/how-to-detect-llm-writing-in-text/)).

**Type-token ratio**

Lower in AI text for n-gram sequences (less diversity in phrase construction).

**“Excess vocabulary” / corpus-level analysis**

The Kobak method — tracking unusually spiked words in a corpus across 2022–2024 — is the most rigorous. It cannot identify individual documents, but it reliably quantifies population-level LLM penetration in a corpus.

**Stylometric fingerprinting**

Attempts to fingerprint specific models (GPT-4 vs. Claude vs. Gemini) via sentence-length distribution, pronoun frequency, punctuation rhythms ([NetusAI](https://netus.ai/blog/stylometry-explained-how-ai-detectors-fingerprint-your-writing); [ResearchGate em-dash paper](https://www.researchgate.net/publication/398319038_The_Em_Dash_as_a_Site_of_Contest_Between_AI_Determinism_and_Human_Agency)).

**Author-comparison baselines**

The most powerful forensic method for suspected individual authors: compare new text against a known corpus of prior writing. Style drift is diagnostic. This is the method Turnitin claims underlies its AI indicator and is the sort of evidence that holds up in academic-integrity hearings.

**IX. Why Detection Is Hard (and Often Unethical)**

No honest field guide can omit this section. The evidence:

**False positives against non-native English speakers**

The Stanford/Liang et al. study (2023) found that seven major detectors **misclassified 61.3% of TOEFL essays as AI-generated**, vs. near-perfect accuracy on U.S. eighth-grade essays. All seven detectors unanimously flagged 19.8% of the TOEFL essays. The cause: detectors score on perplexity, and non-native writers naturally produce lower-perplexity text ([Liang et al.,](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers)_[Patterns](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers)_[/ Stanford HAI](https://hai.stanford.edu/news/ai-detectors-biased-against-non-native-english-writers); [arxiv](https://arxiv.org/abs/2304.02819)). Subsequent commercial detectors (Pangram, Copyleaks) claim much lower rates on their own tests, but the structural bias remains a concern.

**False positives against neurodivergent writers and heavy-tool users**

Writers with autism, ADHD, or dyslexia often use repetitive or highly structured patterns that trip detectors. Writers who rely heavily on Grammarly can have their texts “normalized” in ways that increase detector scores. One investigation found 15 of 17 flagged students in a UC Davis linguistics class were false positives ([Proofademic case studies](https://proofademic.ai/blog/false-positives-ai-detection-guide/)).

**Detector unreliability in absolute terms**

OpenAI’s own AI classifier was retired in July 2023 after the company reported only 26% accuracy on AI text and a 9% false-positive rate on human text. Even Turnitin’s officially claimed sub-1% false positive rate was contradicted by a _Washington Post_ test that found 50% false positives on a small sample ([USD Legal Research Center guide](https://lawlibguides.sandiego.edu/c.php?g=1443311&p=10721367)).

**Humans are not better than detectors**

Meta-studies converge on **roughly 60–70% human accuracy** at telling AI from human prose. A 2025 German-medical-essay study: 70% accuracy for experts, with detection driven by “redundancy, repetition, and lack of coherence” rather than content familiarity ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11914838/)). A Penn State lab reported humans detect AI text only **53%** of the time — barely above chance ([Penn State Q&A](https://www.psu.edu/news/information-sciences-and-technology/story/qa-increasing-difficulty-detecting-ai-versus-human)). One encouraging counter-signal: a 2025 preprint cited on Wikipedia found that **heavy users of LLMs** (people who work with them daily) detect AI at ~90% accuracy — meaning Matthew’s four-hours-a-day habit is itself a diagnostic instrument ([Wikipedia](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)).

**LLM-assisted vs. LLM-generated**

The most vexing problem. Writers can use LLMs to brainstorm, outline, rephrase sentences, copyedit, or translate, and the resulting document may be 80% human and 20% machine — or vice versa. None of the current detection methods usefully distinguish “generated” from “polished,” “restructured,” or “translated with assistance.” The _Advances in Simulation_ study found detectors essentially collapsed when asked to distinguish among five grades of AI involvement ([Springer](https://link.springer.com/article/10.1186/s41077-025-00396-6)).

**The cat-and-mouse problem**

A professional can defeat every major detector by prompting for varied sentence length, inserting personal anecdotes, asking the model to write “in the style of” a specific human, or using humanizer tools (GPTinf, NetusAI, Walter Writes, Pangram evasion). Cat Casey, cited in the USD guide, reports she can fool detectors 80–90% of the time just by adding the word “cheeky” to her prompts.

**The ethics of accusation**

The accumulated evidence — disproportionate flagging of ESL and neurodivergent writers, high false-positive rates, inability to distinguish use-modes, and the impossibility of disproving a flag — points clearly toward **not using detector scores as evidence** in any high-stakes context. The Stanford authors, the Waltzer study authors, and most current university academic-integrity guidelines converge on this conclusion. Writing-process evidence (Google Docs version history, oral discussion, drafts) is more defensible. Most importantly: the _social cost_ of false accusation — between students and teachers, between writers and readers — is not abstract. Reddit commenter Jenny Campbell, deaf and a precise writer by necessity, reports being accused of being a chatbot “about a dozen” times in five months ([WHYY](https://whyy.org/segments/how-not-to-be-mistaken-for-a-chatbot/)).

**X. Cultural and Literary Reception**

**Writers who have written influentially on LLM prose**

*   **Ted Chiang**, “ChatGPT Is a Blurry JPEG of the Web” (_New Yorker_, Feb 2023) — the field’s founding metaphor: LLMs as lossy compression of the Web, whose fluency produces “the illusion that ChatGPT understands the material.” His later essay “Why A.I. Isn’t Going to Make Art” (2024) extends the argument to creativity: “Your first draft isn’t an unoriginal idea expressed clearly; it’s an original idea expressed poorly, and it is accompanied by your amorphous dissatisfaction” ([Longreads](https://longreads.com/2023/02/16/chatgpt-is-a-blurry-jpeg-of-the-web/); [Reality Studies](https://www.realitystudies.co/p/ted-chiang-new-yorker-ai-essay-gets-wrong)).

*   **Vauhini Vara**, “Ghosts” (_The Believer_, 2021; _Best American Essays 2022_), “Confessions of a Viral AI Writer” (_Wired_, 2023), and _Searches: Selfhood in the Digital Age_ (Pantheon, 2025). Vara’s diagnosis of LLM voice — “polite, predictable, inoffensive, upbeat” — has become widely quoted. Her pedagogical use (at Johns Hopkins and elsewhere) treats LLM co-writing as a formal problem in authorship rather than a cheating problem ([Lithub](https://lithub.com/portrait-of-chatgpt-as-a-young-artist-vauhini-vara-on-voice-tech-and-using-ai-in-writing/); [Electric Literature](https://electricliterature.com/why-vauhini-vara-used-chatgpt-to-write-a-book-about-big-tech-and-herself/)).

*   **Laura Preston**, “HUMAN_FALLBACK” (_n+1_ Issue 44, 2022) and “An Age of Hyperabundance” (_n+1_ Issue 47, 2024). Preston, an MFA poet, was employed impersonating a real-estate chatbot named Brenda; her essays are indispensable readings on the texture of chatbot prose as _experienced from the inside_. Her diagnostic term: “collapse of context” — “the ChatGPT-like impulse to write a speech on the noble savage because noble savage is something you’ve heard before” ([Preston, n+1](https://www.nplusonemag.com/issue-47/essays/an-age-of-hyperabundance/)).

*   **Hua Hsu** (New Yorker staff writer, Bard College professor) on “what college students lose when ChatGPT writes their essays” ([WNYC Brian Lehrer](https://www.wnyc.org/story/what-students-lose-when-chatgpt-writes-their-essays/)).

*   **Robin Sloan**, in ongoing lab notes and essays at [robinsloan.com](https://www.robinsloan.com/lab/), has been writing thoughtfully about AI-as-partner since 2017 — his formulation (”the world doesn’t need any more dead-eyed robo-text. The animating ideas here are augmentation; partnership; call and response. The goal is not to make writing ‘easier’; it’s to make it harder”) remains one of the most serviceable pedagogical framings.

*   **Neil Clarke**, editor of _Clarkesworld_, has provided more real-world diagnostic quotes than perhaps anyone ([Clarkesworld on NPR](https://www.npr.org/2023/02/23/1159118948/sci-fi-magazine-stops-submissions-after-flood-of-ai-generated-stories)).

*   **Sean Trott** (UC San Diego) maintains a Substack column running original empirical studies on LLM “signatures” ([seantrott.substack.com](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated)).

**Emerging critical vocabulary**

*   **“AI slop”** — coined on Twitter and Reddit; Merriam-Webster-adjacent by 2024; now the default term for low-effort AI output. Used by editors, critics, and the Wikipedia AI Cleanup project. Defined by Charlie Guo as “surface polish with nothing underneath” ([Artificial Ignorance](https://www.ignorance.ai/p/the-field-guide-to-ai-slop)).

*   **“AI-ese”** — the characteristic register of LLM prose: “overly formal and helpful tone, perfectly structured sentences, and a peculiar vocabulary” ([Towards AI](https://pub.towardsai.net/how-to-choose-the-best-llm-for-writing-4d2741d900f8)).

*   **“Aidiolect”** — the model-specific dialect fingerprint of a given LLM (Claude vs. GPT vs. Gemini).

*   **“Delve-speak”** — the Reinhart-Kobak inflected academese.

*   **“Cyborg writing”** — Originality.AI’s diagnostic term for text produced with heavy mixed tool-use (Grammarly + autocorrect + LLM polish), which often triggers detectors.

*   **“Lossy compression”** (Chiang) — the dominant metaphor for what LLM “knowledge” actually is.

*   **“Simulator / simulacra”** (Janus; Domenic Denicola’s [alternative framing](https://domenic.me/chatgpt-simulacrum/)) — an important counter-metaphor to Chiang’s.

*   **“Regression to the mean”** — Wikipedia’s diagnostic for LLM puffing-up (generic language replacing specific facts).

*   **“Collapse of context”** (Preston) — the model’s tendency to retrieve whatever’s phrase-proximate regardless of whether it fits.

**Editorial observations at scale**

_Clarkesworld_ received ~500 AI-generated stories in a single week (Feb 2023) against ~700 legitimate ones ([NPR](https://www.npr.org/2023/02/24/1159286436/ai-chatbot-chatgpt-magazine-clarkesworld-artificial-intelligence)). _Poets & Writers_ reports most literary magazines have moved to explicit no-AI submission policies; Autumn House Press, Flash Fiction Magazine, The Fabulist, and dozens of others ([P&W](https://www.pw.org/content/managing_submissions_in_the_age_of_ai)). Ander Monson’s _Diagram_ controversially awarded a 2023 chapbook contest to Lillian-Yvonne Bertram’s AI-generated _A Black Story May Contain Sensitive Content_, sparking debate over _disclosed_ vs. _undisclosed_ AI authorship. Image Journal, Seattle Star, and other small-community magazines report little AI submission pressure, attributing it to their “intimate community of contributors.” Wikipedia’s ongoing AI Cleanup project represents the most mature crowd-sourced ecosystem for detection and correction, now feeding back into policy (speedy-deletion criterion G15 for LLM-generated pages without human review).

**The paranoia spiral**

Finally, the most important cultural observation. _Slate_ reported in August 2025 that writers — students, professional columnists, and casual emailers alike — are now **deliberately introducing typos, fragments, and infelicities to signal humanity** (”Writing online in 2025 feels like performing keyhole surgery while people scream ‘ROBOT! ROBOT! ROBOT!’ into your ear,” per writer Jack McNamara). Sarah McCarty, quoted in the same piece, now avoids writing her own metaphors: “I think this is something ChatGPT excels at” ([Slate](https://slate.com/technology/2025/08/chatgpt-artificial-intelligence-shaming-paranoia-writing.html)). This is the most significant second-order cultural effect: the signal-jamming of human writing itself, in defensive response.

**XI. A Short Pedagogical Kit (for LLI “Thinking with Machines”)**

Five exercises that make the taxonomy above legible to students:

1.   **The Delve Audit.** Take a 500-word student essay (or NYT op-ed, or AI-generated passage). Count every word in the Kobak “focal” list: delve, intricate, meticulously, realm, pivotal, navigate, landscape, tapestry, resonate, testament, underscore, showcasing, compelling, paramount, crucial, foster, elevate, surpass. Plot density. Discuss what it means that a piece is or isn’t within the “excess band.”

2.   **The Negation Hunt.** Have students find five “not X, but Y” constructions in the wild (LinkedIn, Substack, marketing copy). Have them rewrite each as a direct affirmative. Discuss what gets lost and what gets gained.

3.   **The Burstiness Contrast.** Give students a 300-word human passage (Annie Dillard, James Baldwin, Mary Ruefle) and a 300-word LLM output on the same topic. Ask them to chart sentence length, sentence by sentence. Plot the two curves. Let them see what “burstiness” _looks_ like on graph paper.

4.   **The First-Person Plural Check.** Have ChatGPT write five poems about unrelated subjects. Count first-person-plural pronouns (”we/us/our”). Compare to five poems from _Poetry Magazine_ ([Walsh’s empirical finding](https://arxiv.org/html/2410.15299v1) becomes tangible).

5.   **The Specificity Rewrite.** Take an LLM-generated paragraph and force students to replace every general noun (”people,” “community,” “technology,” “change”) with a specific one (”my grandmother,” “the Christiansburg Kroger,” “the 2017 iPhone X,” “the layoffs of March 2020”). Watch the prose come back to life. This is the pedagogical counter-move.

For Matthew’s Substack and creative work, one further observation: the most interesting literary-artistic response to LLM prose is probably not _avoidance_ but _détournement_. Vara’s “Ghosts,” Bertram’s chapbook, and Sloan’s writing-with-GPT-2 experiments demonstrate that the machine’s tells become _material_ for a human writer who keeps the reins. The most damning thing one can say about fully LLM-generated prose is also the key to its literary utility: it is a high-resolution index of the statistical center of English prose over the last thirty years. That index is a resource, if one writes _against_ or _across_ it rather than _through_ it.

**XII. Summary Diagnostic Cluster — The 30-Second Field Check**

A piece of prose is probabilistically LLM-assisted if _three or more_ of the following arrive within a few hundred words:

*   A Kobak “focal word” (delve, intricate, pivotal, realm, meticulously, navigate, tapestry) in a non-academic context

*   A “not X, but Y” construction

*   A tricolon of parallel short phrases

*   Em-dashes used additively (attaching qualifiers) rather than disruptively

*   A closing “In summary / In conclusion / Ultimately…” wrap

*   Uniform sentence length across a paragraph (burstiness < ~0.5)

*   Promotional adjectives applied to non-promotional subjects (”vibrant community,” “rich tapestry”)

*   Sycophantic opener (”Great question!” “What a thoughtful observation!”)

*   Orphaned demonstratives (”This highlights…” without a clear antecedent)

*   A bold-stemmed nested bullet list where paragraph prose would do

*   Absence of any proper noun, brand name, specific date, or idiosyncratic detail

*   A mixed or slightly-off metaphor in the “right ballpark”

None of these, individually, prove anything. Together, they constitute the _AI-ese_ that practiced readers — editors, teachers, heavy LLM users — can now recognize at near-90% accuracy. The diagnostic is not a gotcha but a descriptive one: this is the statistical shape of English-language prose when the writer is a machine trained to minimize cross-entropy loss on the corpus of the internet.

**Coda**

One last observation worth keeping close. Neil Clarke’s most-quoted line about AI submissions — “they are bad in ways that no human has been bad before” — contains a quietly hopeful corollary. Human badness is _specific_: bad in the particular grain of one person’s particular failure. The LLM’s badness is generic. Which means that the most human defense against AI prose is also the oldest instruction of any decent writing teacher: **be specific, be strange, be where you actually are**. The machine cannot be where you are. It can only approximate. The field guide above is really just a catalog of approximation’s signatures. The prose that gets written _against_ them will continue to be recognizably ours.
