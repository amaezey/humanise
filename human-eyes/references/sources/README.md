# Source references
These files track the sources cited by human-eyes and how each one currently relates to the skill catalogue.

Each source file uses the same shape: metadata, summary, main insights, evidence and claims to extract, skill-use audit, matched patterns/rules, associated hypotheses, and follow-up questions. Use [TEMPLATE.md](TEMPLATE.md) for new source files.

Use [pattern-opportunities.md](pattern-opportunities.md) to track source claims promoted into pattern additions, hypotheses, process guidance, metadata conventions, or explicit non-promotions.

First-pass extracted: 2026-05-05.
Second-pass reviewed: 2026-05-05. All 72 source cards now include source notes, evidence-tier metadata, a skill-use audit, pattern/rule mappings, associated hypotheses, and follow-up questions. New source cards should include extraction date and, when relevant, model family, model version, corpus date range, or source-page update date so time-sensitive AI tells do not become stale blacklists.

## Evidence tiers
- **Peer-reviewed / academic empirical:** strongest for pattern evidence, usually still aggregate, register-scoped, or corpus-scoped rather than proof for a single document.
- **First-party model docs:** useful for model behavior, capability, policy, and version-drift context; not prose-pattern proof unless the document names the behavior directly.
- **Journalism / reported cases:** useful for incidents, public salience, provenance, harms, and social context; weaker for reusable pattern thresholds.
- **Practitioner / teacher / editor essays:** useful for manual review prompts, genre branches, craft language, and examples; weaker for hard severity or detector claims.
- **Vendor / detector pages:** useful for product framing, uncertainty UX, and candidate features; weak for pattern validity unless independently corroborated.
- **Conduit / catalogue sources:** Wikipedia, Vollmer, and the original skill are discovery maps. Prefer their upstream sources for evidence and cite the conduit only for provenance.

Second-pass sources whose exact pages were found but whose inherited mappings need caution:
- [AI for Lifelong Learners: Tells beyond the em-dash](ai-lifelong-learners-em-dash.md) - exact post reviewed from screenshot sequence supplied 2026-05-05; useful practitioner evidence, but not a detector-threshold source.
- [Aranya / Poetly: AI poetry and process](aranya-poetly-ai-poetry.md) - exact post reviewed; source came from `README.md` and `dev/research/vollmer.md`; it supports poetry-process questions more than the inherited aphorism-density / negate-and-redefine / mood-word-accumulation mapping.
- [Sean Trott: LLM signature analysis](trott-llm-signature-analysis.md) - exact post reviewed; source came from `README.md` and `dev/research/vollmer.md`; it supports predictability and calibration cautions, not surface-tell shortcuts.
- [SEO Engine: Signs of AI writing](seoengine-ai-writing-signs.md) - exact article reviewed from local clipping supplied 2026-05-05; it is useful as a vendor/practitioner checklist, but its numeric detector, model-frequency, and ranking-impact claims need upstream corroboration.

Deep extraction exists for:
- [Wikipedia: Signs of AI writing](../../../dev/research/wikipedia-signs-of-ai-writing.md)
- [Matthew Vollmer: I Asked the Machine to Tell on Itself](../../../dev/research/vollmer.md)

## Foundation
- [blader/humanizer](blader-humanizer.md)
- [Wikipedia: Signs of AI writing](wikipedia-signs-of-ai-writing.md)
- [Matthew Vollmer: I Asked the Machine to Tell on Itself](vollmer-machine-tell-on-itself.md)

## Academic vocabulary, grammar, behavior, domains, limits, and stylometry
- [Kobak et al.: Delving into LLM-assisted writing in biomedical publications through excess vocabulary](kobak-llm-excess-vocabulary.md)
- [Juzek and Ward: Why Does ChatGPT Delve So Much?](juzek-ward-delve.md)
- [Juzek and Ward: Word Overuse and Alignment in Large Language Models](juzek-ward-word-overuse-alignment.md)
- [Reinhart et al.: Do LLMs write like humans?](reinhart-llm-write-like-humans.md)
- [Geng and Trotta: Human-LLM Coevolution](geng-trotta-human-llm-coevolution.md)
- [Geng and Trotta: Is ChatGPT Transforming Academics' Writing Style?](geng-trotta-transforming-academic-style.md)
- [Kousha and Thelwall: How much are LLMs changing academic papers after ChatGPT?](kousha-thelwall-academic-papers.md)
- [Sun et al.: Idiosyncrasies in Large Language Models](sun-idiosyncrasies-llms.md)
- [Ju, Blix, and Williams: Domain Regeneration](ju-blix-williams-domain-regeneration.md)
- [Abdulhai et al.: How LLMs Distort Our Written Language](abdulhai-llms-distort-written-language.md)
- [Russell, Karpinska, and Iyyer: Frequent ChatGPT users as detectors](russell-karpinska-iyyer-detectors.md)
- [Nature: Signs of AI-generated text found in biomedical abstracts](nature-biomedical-abstracts.md)
- [Przystalski et al.: Stylometry recognizes human and LLM-generated texts](przystalski-stylometry.md)
- [Zaitsu et al.: Stylometry can reveal AI authorship](zaitsu-stylometry.md)
- [Bisztray et al.: I Know Which LLM Wrote Your Code Last Summer](bisztray-code-stylometry.md)
- [Walsh et al.: AI poetry computational analysis](walsh-ai-poetry.md)
- [Neil Clarke: A Concerning Trend](clarke-clarkesworld-concerning-trend.md)
- [Waltzer et al.: Can teachers detect AI-generated student essays?](waltzer-teachers-detect-ai-essays.md)
- [Murray and Tersigni: Can instructors detect AI-generated papers?](murray-tersigni-ai-generated-papers.md)
- [Jiang and Hyland: Engagement markers in ChatGPT-generated argumentative essays](jiang-hyland-engagement-markers.md)
- [Dhillon et al.: MFA students vs LLMs fiction](dhillon-mfa-students-llms-fiction.md)
- [Spero and Emi: Pangram AI-generated text classifier technical report](spero-emi-pangram-classifier.md)
- [Liang et al.: GPT detectors are biased against non-native English writers](liang-detector-bias.md)

## Journalism and trade press
- [Sam Kriss: Why Does A.I. Write Like ... That?](kriss-nyt-ai-write-like-that.md)
- [Merrill, Chen, and Kumer: What are the clues that ChatGPT wrote something?](merrill-wapo-chatgpt-clues.md)
- [Benj Edwards: OpenAI suppressing em dashes](edwards-ars-em-dash.md)
- [Brian Phillips: the em-dash defense](phillips-ringer-em-dash.md)
- [Wendy Belcher: 10 Ways AI Is Ruining Your Students' Writing](belcher-ai-ruining-student-writing.md)
- [Hua Hsu: What college students lose when ChatGPT writes their essays](hsu-students-lose-chatgpt.md)
- [Karolina Rudnicka: Each AI chatbot has its own distinctive writing style](rudnicka-chatbot-writing-style.md)
- [Slate: ChatGPT, AI shaming, and the paranoia of writing](slate-ai-shaming-paranoia.md)
- [Jonathan Bailey: Em dashes, hyphens, and spotting AI writing](bailey-em-dash-hyphens.md)
- [Futurism: Sports Illustrated published AI-generated writers](futurism-sports-illustrated-ai-writers.md)
- [Gizmodo: CNET AI-generated finance articles](pbs-cnet-ai-finance-articles.md)

## Practitioner essays and writer blogs
- [Linda Caroll: Good Writing, AI Slop, and the Dragon](caroll-good-writing-ai-slop.md)
- [Charlie Guo: The Field Guide to AI Slop](guo-field-guide-ai-slop.md)
- [Shreya Shankar: AI Writing](shankar-ai-writing.md)
- [Blake Stockton: Don't Write Like AI series](stockton-dont-write-like-ai.md)
- [Vauhini Vara: Confessions of a Viral AI Writer](vara-confessions-viral-ai-writer.md)
- [Laura Preston: HUMAN_FALLBACK](preston-human-fallback.md)
- [Laura Preston: An Age of Hyperabundance](preston-hyperabundance.md)
- [Ted Chiang: ChatGPT Is a Blurry JPEG of the Web](chiang-blurry-jpeg.md)
- [Ted Chiang: Why A.I. Isn't Going to Make Art](chiang-why-ai-isnt-art.md)
- [Robin Sloan: human-AI writing notes](sloan-human-ai-writing.md)
- [Sean Trott: LLM signature analysis](trott-llm-signature-analysis.md)
- [Aranya / Poetly: AI poetry and process](aranya-poetly-ai-poetry.md)
- [David J. Germain: Writing dialog with ChatGPT](germain-chatgpt-dialog.md)
- [Brent Csutoras: The em-dash dilemma](csutoras-em-dash-dilemma.md)
- [Fred Rohrer: promotional register and n-gram analysis](rohrer-promotional-register.md)

## Vendor, first-party, and practitioner guides
- [OpenAI: GPT-4 System Card](openai-gpt-4-system-card.md)
- [OpenAI: Sycophancy in GPT-4o rollback](openai-sycophancy-rollback.md)
- [Anthropic: Claude Sonnet system prompts](anthropic-sonnet-prompts.md)
- [GPTZero: AI Vocabulary](gptzero-ai-vocabulary.md)
- [GPTZero: Perplexity and burstiness](gptzero-perplexity-burstiness.md)
- [Grammarly: Common AI words and phrases](grammarly-common-ai-words.md)
- [Gmelius: Can customers tell an email is written using generative AI?](gmelius-email-ai-isms.md)
- [Bynder: AI marketing identification study](bynder-ai-marketing-study.md)
- [Pangram AI content detector](pangram-classifier.md)
- [Copyleaks AI content detector](copyleaks-detector.md)
- [ZeroGPT AI detector](zerogpt-detector.md)
- [Originality.AI detector](originality-ai-detector.md)
- [NetusAI: stylometry and AI detectors](netusai-stylometry.md)
- [Turnitin AI writing detection](turnitin-ai-writing-detection.md)
- [AI Detectors: How to tell if text is AI written](aidetectors-ai-writing-signs.md)
- [SEO Engine: Signs of AI writing](seoengine-ai-writing-signs.md)
- [SAGE: AI detection for peer reviewers](sage-ai-detection-peer-reviewers.md)
- [Hastewire: How teachers spot ChatGPT use](hastewire-teachers-spot-chatgpt.md)
- [Copy Posse: 5 signs your email was written by AI](copyposse-email-ai-signs.md)
- [AI for Lifelong Learners: Tells beyond the em-dash](ai-lifelong-learners-em-dash.md)
