# Source Evidence Triage: Promoted Claims and Non-Promotions

This file tracks useful source-card evidence from the source-card pass and where it was promoted or deliberately not promoted.

Dispositions:
- **Promoted:** added to a named subcheck, #41 genre branch, source note, report/process wording, source metadata convention, or `dev/hypotheses.md`.
- **Hypothesis:** tracked in `dev/hypotheses.md`; needs design or validation before implementation.
- **Process guidance:** added to rewrite/audit/report guidance rather than the pattern catalogue.
- **Do not promote:** kept as context only; it should not become pattern evidence.

## Promoted Additions

| Candidate | Proposed home | Source cards | Why |
|---|---|---|---|
| Source-grounding, fact-checking, and claim verification | #41 journalism/academic manual checks; report guidance | [Bailey](bailey-em-dash-hyphens.md), [Chiang blurry JPEG](chiang-blurry-jpeg.md), [PBS/CNET](pbs-cnet-ai-finance-articles.md), [Futurism](futurism-sports-illustrated-ai-writers.md), [SAGE peer review](sage-ai-detection-peer-reviewers.md), [AI Detectors](aidetectors-ai-writing-signs.md), [Rohrer](rohrer-promotional-register.md), [Wikipedia cleanup guide](wikipedia-signs-of-ai-writing.md) | Several sources point to factual errors, fake bylines, bad citations, broken links, wrong DOIs, missing sources, and platform artifacts as more concrete than surface prose tells. |
| Student-writing argument/evidence quality | #41 student/academic branch | [Belcher](belcher-ai-ruining-student-writing.md), [Murray and Tersigni](murray-tersigni-ai-generated-papers.md), [Hsu](hsu-students-lose-chatgpt.md), [Hastewire](hastewire-teachers-spot-chatgpt.md), [Waltzer](waltzer-teachers-detect-ai-essays.md) | Current #41 names student writing, but these cards support explicit checks for banal thesis, weak evidence, student-level mismatch, abrupt tone/complexity shifts, surface polish masking weak argument, draft ownership, and false-positive caution. |
| Academic engagement-marker depletion | #41 academic/student branch; possible future agent check | [Jiang and Hyland](jiang-hyland-engagement-markers.md) | Stronger than broad neutrality collapse: the source specifically names reduced questions, personal asides, and engagement markers in argumentative essays. |
| Poetry-specific manual checks | #41 poetry branch | [Walsh](walsh-ai-poetry.md), [Poetly](aranya-poetly-ai-poetry.md) | Walsh supports default quatrains, rhyme density, first-person plural clustering, and form compliance without variation; Poetly supports archive comparison, process trace, and revision depth. |
| Fiction dialogue and style-fidelity review | #41 fiction branch | [Germain](germain-chatgpt-dialog.md), [Dhillon](dhillon-mfa-students-llms-fiction.md), [Clarke](clarke-clarkesworld-concerning-trend.md) | Germain gives direct fiction-dialogue cues; Dhillon supports expert-reader/fidelity caution; Clarke supports provenance and editorial-burden checks rather than disclosed style tells. |
| Email/marketing specificity checks | #41 email/marketing branch | [Gmelius](gmelius-email-ai-isms.md), [Copy Posse](copyposse-email-ai-signs.md), [Bynder](bynder-ai-marketing-study.md) | Stronger current evidence is missing personalization, generic subject lines, weak domain understanding, exaggerated transformation claims, and empty hype verbs. |
| Preserve deliberate punctuation and avoid anti-AI camouflage | Rewrite/report guidance; #49 caveat | [Phillips](phillips-ringer-em-dash.md), [Slate](slate-ai-shaming-paranoia.md), [Csutoras](csutoras-em-dash-dilemma.md), [AI for Lifelong Learners](ai-lifelong-learners-em-dash.md) | The em-dash evidence needs an explicit counterweight: preserve deliberate punctuation and do not push writers toward unnatural "humanizing" performance. |
| Detector-output caveat wording | Audit/report guidance | [Turnitin](turnitin-ai-writing-detection.md), [Copyleaks](copyleaks-detector.md), [Liang](liang-detector-bias.md), [NetusAI](netusai-stylometry.md), [GPTZero vocabulary](gptzero-ai-vocabulary.md), [Zaitsu](zaitsu-stylometry.md) | Sources repeatedly support "single data point, not a definitive answer", minimum-length/confidence caveats, and false-positive warnings. |
| Source date/model metadata on imported examples | Source metadata convention | [Merrill/WaPo](merrill-wapo-chatgpt-clues.md), [Geng and Trotta](geng-trotta-human-llm-coevolution.md), [Sun](sun-idiosyncrasies-llms.md), [Rudnicka](rudnicka-chatbot-writing-style.md), [OpenAI GPT-4 System Card](openai-gpt-4-system-card.md), [Edwards](edwards-ars-em-dash.md), [Trott](trott-llm-signature-analysis.md) | Model family, corpus date range, public-tell drift, and version updates affect whether a tell is current or stale. |

## Hypotheses

These are now tracked in `dev/hypotheses.md` as hypotheses 21-28.

| Candidate | Proposed home | Source cards | Why |
|---|---|---|---|
| Low information density / wrong sentence subject | New advisory/agent hypothesis | [Shankar](shankar-ai-writing.md), [Guo](guo-field-guide-ai-slop.md), [Belcher](belcher-ai-ruining-student-writing.md) | Multiple craft sources point to fluent prose that says little, uses the wrong grammatical subject, or summarizes instead of thinking. |
| Long-tail compression / grammatical standardisation | Structural metric hypothesis near #52 | [Ju, Blix, and Williams](ju-blix-williams-domain-regeneration.md), [Przystalski](przystalski-stylometry.md), [GPTZero burstiness](gptzero-perplexity-burstiness.md) | Stronger than average sentence-length rules: the evidence points to compressed variation and reduced long-tail behavior. |
| Nominalization and noun-heavy style | Future structural/rhetorical feature | [Reinhart](reinhart-llm-write-like-humans.md) | Current #3 covers present-participial clauses, but Reinhart also points to nominalization density, noun-heavy style, "that" subject clauses, and phrasal coordination. |
| Register-specific vocabulary density | #7 scoring/hypothesis refinement | [Kobak](kobak-llm-excess-vocabulary.md), [Kousha and Thelwall](kousha-thelwall-academic-papers.md), [Juzek delve](juzek-ward-delve.md), [Juzek alignment](juzek-ward-word-overuse-alignment.md), [Geng and Trotta style shift](geng-trotta-transforming-academic-style.md), [Nature](nature-biomedical-abstracts.md), [Grammarly](grammarly-common-ai-words.md) | The sources support repeated/co-occurring, increasing and decreasing, register-specific vocabulary evidence, not flat one-word blacklists. |
| Model-family versus generic-AI residue | Source metadata and future scoring dimension | [Sun](sun-idiosyncrasies-llms.md), [Rudnicka](rudnicka-chatbot-writing-style.md), [Merrill/WaPo](merrill-wapo-chatgpt-clues.md), [Trott](trott-llm-signature-analysis.md) | Some evidence distinguishes source model or model family rather than AI versus human. |
| Vague-change intros separate from contrastive negation | Pattern split/refinement | [Stockton](stockton-dont-write-like-ai.md), [Vollmer](vollmer-machine-tell-on-itself.md) | Current contrast/negation patterns may be hiding a separate "something changed" B2B/corporate opener pattern. |
| Performative profundity / aphoristic closure | Future advisory pattern | [Vollmer](vollmer-machine-tell-on-itself.md), [Kriss](kriss-nyt-ai-write-like-that.md), [SEO Engine](seoengine-ai-writing-signs.md) | Several practitioner sources point to generic profundity, false profundity, and universal-generic statements. Start advisory, not hard gate. |
| Originality, clarity, and formality as judgement dimensions | Future comparison-engine dimensions | [Russell, Karpinska, and Iyyer](russell-karpinska-iyyer-detectors.md) | The source does not directly validate #9/#10/#15, but it does suggest higher-level dimensions experienced reviewers use when judging generated non-fiction. |

## Process Guidance

These are promoted to `human-eyes/SKILL.md`, `human-eyes/references/process.md`, and `human-eyes/references/voice.md` where they affect current audit, rewrite, and write behavior. Development-only items remain guidance for future fixture/process work.

| Candidate | Proposed home | Source cards | Why |
|---|---|---|---|
| Rewrite semantic-preservation check | Rewrite process | [Abdulhai](abdulhai-llms-distort-written-language.md), [Vara](vara-confessions-viral-ai-writer.md), [Hsu](hsu-students-lose-chatgpt.md) | Even grammar-only or emotionally difficult AI assistance can alter meaning, stance, ownership, and voice. |
| Audience, intent, and choice as positive voice criteria | Voice/process guidance | [Caroll](caroll-good-writing-ai-slop.md), [Chiang art essay](chiang-why-ai-isnt-art.md), [Sloan](sloan-human-ai-writing.md), [Preston hyperabundance](preston-hyperabundance.md), [AI for Lifelong Learners](ai-lifelong-learners-em-dash.md) | These sources are stronger as positive guidance: simple language plus lived specificity, harder/stranger work, real audience fit, and intentional choice. |
| Human-fallback/script-break review | Process guidance | [Preston HUMAN_FALLBACK](preston-human-fallback.md) | The source supports identifying places where context, idiom, ambiguity, or emotional stakes require human judgement. |
| Sycophancy and honesty in advisory/review comments | Process or future agent-judgement guidance | [OpenAI sycophancy rollback](openai-sycophancy-rollback.md) | OpenAI supports evaluating disingenuous support and fake agreement as behavior, not just deleting friendly phrases in finished prose. |
| Avoid publishing evasion recipes | Source/process guidance | [Clarke](clarke-clarkesworld-concerning-trend.md), [Trott](trott-llm-signature-analysis.md) | Some sources explicitly warn that overspecified detector details can enable evasion or create false confidence. |
| Evaluation and fixture design | Dev/research guidance | [Pangram](pangram-classifier.md), [Spero and Emi](spero-emi-pangram-classifier.md), [Originality.AI](originality-ai-detector.md) | Domain coverage, synthetic-mirror methods, and use-case surfaces are useful for tests/UX planning, not direct pattern evidence. |
| Migration checklist for inherited behavior | Maintenance checklist | [blader/humanizer](blader-humanizer.md) | The inherited 29-pattern list should be reconciled as retained, renamed, split, or removed. |

## Do Not Promote

| Candidate | Source cards | Reason |
|---|---|---|
| Code-only stylometry as prose evidence | [Bisztray](bisztray-code-stylometry.md) | Adjacent model-attribution context only; not natural-language prose evidence. |
| Product detector scores or thresholds as rule severity | [Copyleaks](copyleaks-detector.md), [ZeroGPT](zerogpt-detector.md), [Originality.AI](originality-ai-detector.md), [Turnitin](turnitin-ai-writing-detection.md), [NetusAI](netusai-stylometry.md), [GPTZero perplexity](gptzero-perplexity-burstiness.md) | Useful for uncertainty UX and contrast, but opaque product metrics should not set human-eyes thresholds. |
| Consumer recognition as pattern evidence | [Bynder](bynder-ai-marketing-study.md) | Useful for stakes and perception framing, but the source does not disclose which textual cues drove recognition. |
| First-party prompts as direct prose-pattern proof | [Anthropic prompts](anthropic-sonnet-prompts.md), [OpenAI GPT-4 System Card](openai-gpt-4-system-card.md) | Model-context evidence unless exact prompt text or behavior is mapped directly. |
| Pure framing essays as pattern evidence | [Chiang art essay](chiang-why-ai-isnt-art.md), [Preston hyperabundance](preston-hyperabundance.md), [Sloan](sloan-human-ai-writing.md) | Useful for rationale/process; not direct pattern support. |

## Suggested Next Patches

1. Keep `human-eyes/scripts/judgement.json`, `human-eyes/scripts/patterns.json`, `human-eyes/SKILL.md`, `human-eyes/references/process.md`, `human-eyes/references/voice.md`, `dev/hypotheses.md`, and `README.md` in sync when source evidence changes.
2. For **Hypotheses**, validate against corpus or qualitative examples before moving anything into active detector behavior.
3. Keep **Do not promote** entries out of rule evidence unless a future direct source changes the evidence tier.
