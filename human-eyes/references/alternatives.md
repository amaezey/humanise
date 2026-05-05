# Vetted human alternatives

Replacements the Suggestions action draws from when a flagged tell is lexical. Also used by Rewrite and Write when picking replacements during the surface pass.

## Scope

This file covers lexical patterns: patterns where a specific word or phrase can be swapped for a plain-English alternative. Structural patterns (paragraph-length uniformity, anaphoric scaffolding, sentence-length variance, tonal uniformity) do not appear here. Suggestions writes contextual rewriting instructions for those.

A few patterns that look lexical (contrived contrast, false-concession, bland critical templates) get entries below, but their middle column names what the construction usually *means* rather than offering a phrase to swap. Substitution does not work for those; the construction itself is the problem.

## What "vetted" means

Each alternative has been reviewed for AI flavour. The right replacement is rarely a lower-temperature synonym ("dig into" for "delve"); it is the plain word that names what the writer actually meant. If the AI word usually means one of three or four specific things, the writer's job is to pick which and use that. Where the most natural fix is to cut the word, the entry says so. Not every flagged word has a defensible replacement.

## Contents

- [Em dashes](#em-dashes)
- [AI vocabulary words](#ai-vocabulary-words)
- [Significance inflation](#significance-inflation)
- [Copula avoidance](#copula-avoidance)
- [Hedging clusters](#hedging-clusters)
- [Filler phrases](#filler-phrases)
- [Formulaic openers](#formulaic-openers)
- [Signposted-conclusion openers](#signposted-conclusion-openers)
- [Generic positive conclusions](#generic-positive-conclusions)
- [Soft scaffold phrases](#soft-scaffold-phrases)
- [Manufactured-insight phrasings](#manufactured-insight-phrasings)
- [Sycophantic / collaborative artifacts](#sycophantic--collaborative-artifacts)
- [Knowledge-cutoff disclaimers](#knowledge-cutoff-disclaimers)
- [Contrived contrast / negative parallelism](#contrived-contrast--negative-parallelism)
- [False-concession constructions](#false-concession-constructions)
- [Bland critical templates](#bland-critical-templates)

---

## Em dashes

In publication-ready plain prose, em dashes are now a strong AI signal. Density is the giveaway: a writer using one or two intentionally is fine; a piece with em dashes in every other paragraph reads as machine-flavoured even when each individual use is grammatical.

Most em dashes are doing the job of a different punctuation mark. The right replacement depends on what the dash was actually doing.

| AI tell | What it usually means | Notes |
|---|---|---|
| Em dash between two independent clauses | A period or semicolon | Period if both halves carry weight. Semicolon if the two clauses are independent and the relationship is real. |
| Em dash setting off an aside | A comma or parentheses | Parentheses if the aside could be cut without losing the sentence. Comma if it could not. |
| Em dash introducing a list or explanation | A colon | "X, and here is what X means" is colon work. |
| Em dash separating a beat or shift | A comma | The most common case. Try the comma first. |
| Em dash that fits none of the above | A sentence with bad structure | Rewrite. |

---

## AI vocabulary words

Words that appear far more frequently in post-2023 LLM output than in human writing. No single word is proof. The tell is density: three or more in one paragraph reads as AI even when each word is individually defensible.

The vocabulary clusters by semantic function: verbs of intellectual work, inflation verbs, action-flavoured corporate verbs, and abstract scenery nouns. The middle column names what the AI word usually stands in for. The writer picks the meaning that fits and uses that word, or cuts the verb if none of the meanings apply.

For long-tail vocabulary (the Kobak 900-word list, the GPTZero 100-phrase list), Suggestions does not look up individual entries here. It uses the cluster guidance below to draft a rewrite appropriate to the flagged occurrence.

### Verbs of intellectual work

| AI word | What it usually means | Notes |
|---|---|---|
| delve / delve into | analyse, investigate, research, study, get into the detail | Pick the verb that names what you are actually doing. If none fit, the sentence does not need the verb. |
| explore | try, test, investigate, look at possibilities | Fine when the genuine meaning is *consider possibilities*. AI-flavoured when it stands in for any verb of inquiry. |
| examine | check, read, study, test | Often the sentence works without it. "Examine the data" usually wants to be "the data shows…". |
| navigate (figurative) | manage, handle, work out | Drop entirely when the object is concrete. "Navigate the system" wants to be "use the system". |
| unpack | explain, work out, take apart | Now AI-flavoured despite colloquial origin. |

### Inflation verbs

These words promise analytical work the sentence does not do. The plain alternatives are usually shorter and more honest.

| AI word | What it usually means | Notes |
|---|---|---|
| underscore(s) | shows, says, repeats | If the sentence already shows the thing, cut the verb entirely. |
| highlight(s) | shows, picks out, names | A sign the writer has not done the work of saying *what* it shows. |
| emphasise(s) | stresses, repeats, focuses on | Often empty when the next clause is already doing the emphasis. |
| illustrate(s) | shows, gives an example of | The next sentence should be the example. The verb is doing nothing. |
| reflect(s) (figurative) | shows, comes from, follows from | Drop entirely when the connection is already explicit. |

### Action-flavoured corporate verbs

| AI word | What it usually means | Notes |
|---|---|---|
| leverage | use, apply, draw on | "Use" is almost always right. "Leverage" carries no extra information. |
| harness | use, take advantage of | Almost always means "use". |
| foster | encourage, build, support | If the subject cannot actually foster (an abstraction "fostering" something), rewrite. |
| facilitate | run, host, lead, let, help | Almost always means "do" or "let happen". Say which. |
| enable | let, allow | Fine occasionally. Flag when it stacks with other corporate verbs. |
| streamline | simplify, cut, shorten, speed up | Name what was cut. |

### Abstract scenery nouns

| AI word | What it usually means | Notes |
|---|---|---|
| landscape (figurative) | the field, the topic, the situation, or just cut | "The funding landscape" wants to be "funding". "The political landscape" wants to be "politics". |
| tapestry | a mix, a list of named things | Almost never lands. Replace with a concrete plural such as "traditions" or "histories". |
| realm | the field, the area, or just cut | "The realm of X" wants to be "X". |
| interplay | how X and Y work together | Fine in academic writing about specific dynamics. AI-flavoured when it stands in for "the thing". |
| mosaic of / tapestry of | mix of, list of, range of | Often a wrapper around a plural noun. Drop it. |

### Cluster-level fix

When a paragraph trips the AI-vocabulary density check (three or more in one paragraph), single-word substitution rarely fixes it. Rewrite the paragraph around its concrete claim, with concrete verbs in place of the abstract ones and no scenery nouns.

---

## Significance inflation

Constructions that claim symbolic weight for ordinary things: "stands as a testament", "marks a pivotal moment", "plays a crucial role", "represents a shift". The construction promises significance without supplying evidence.

| AI tell | What it usually means | Notes |
|---|---|---|
| stands as a testament to | shows, is evidence for, proves | Often the sentence already says it. Cut the construction. |
| marks a pivotal moment in | started, changed, was the first | Pick the verb that names what actually happened. |
| plays a crucial role in | matters for, is part of, helps | Cut "crucial role" and name the role. |
| represents a (shift / turning point) | started, changed, ended | The construction promises drama. Just say what changed. |
| reflects (broader / wider / deeper) | comes from, is part of, is one example of | Drop the inflation adjective; name the specific connection. |
| sets the stage for | started, made possible, came before | Almost always padding. Cut. |
| has left an indelible mark | shaped, changed, influenced | If the mark is real, it can be named. |
| paves the way for | leads to, comes before, makes possible | Cliché. Pick the plain verb. |

---

## Copula avoidance

Constructions that substitute elaborate verbs for "is", "are", or "has". Often the elaborate verb does nothing the simple copula could not.

| AI tell | What it usually means | Notes |
|---|---|---|
| serves as | is | Almost always. "X serves as the venue for Y" wants to be "X is the venue for Y". |
| stands as | is | Same as serves as. |
| marks | is, was | "X marks the largest Y" wants to be "X is the largest Y". |
| represents (literal) | is, shows | "X represents an attempt to Y" wants to be "X is an attempt to Y". |
| boasts | has | "The town boasts three museums" wants to be "The town has three museums". |
| features | has, includes | "The building features X" wants to be "The building has X". |
| offers | has, gives | "The role offers flexibility" wants to be "The role has flexible hours" (be specific about what). |

---

## Hedging clusters

Stacking three or more qualifiers on a single claim until the sentence commits to nothing. The fix is rarely to find a less hedgy word; it is to drop the hedges and let the claim stand or fall on its own.

| AI tell | What it usually means | Notes |
|---|---|---|
| could potentially possibly | might, could | Pick one qualifier or none. Three is meaningless. |
| It could be argued that | (just argue it) | If the writer thinks X, they should claim X. |
| It might be the case that | maybe, possibly | One word, not five. |
| seems to suggest | suggests, hints at | "Seems to" almost always cuts cleanly. |
| there is some evidence that may indicate | the evidence shows, the evidence is mixed | Either claim it or admit the evidence is mixed. The hedge stack disguises uncertainty as caution. |
| it is worth considering whether | (just consider it) | If it is worth considering, the writer can do the considering on the page. |

---

## Filler phrases

Multi-word constructions that compress to one or two words, or cut entirely. Filler is the easiest tell to remove because the meaning rarely depends on it.

| AI tell | What it usually means | Notes |
|---|---|---|
| in order to | to | Always. "In order to" never adds anything. |
| due to the fact that | because | Always. |
| at this point in time | now, today, currently | Pick the one that fits the tense. |
| in the event that | if | Always. |
| has the ability to | can | Always. |
| it is important to note that | (cut the whole phrase) | The next clause should make its own importance evident. |
| at the end of the day | (cut entirely; or state the actual conclusion) | Adds nothing. |
| from a broader perspective | (cut, or name the perspective) | Vague gesture. Either name the wider context or drop it. |
| generally / broadly speaking | usually, often, mostly | Or cut. |

---

## Formulaic openers

Standard AI-essay opening patterns that signal the piece was generated rather than written. The first sentence often gives the game away.

| AI tell | What it usually means | Notes |
|---|---|---|
| In today's fast-paced world | (cut entirely; start with the actual subject) | The world is not the subject of the piece. |
| As technology continues to evolve | (cut; start with the actual claim) | Time and progress are not arguments. |
| In an era of (X) | (cut; or name a specific year) | Vague historical framing. Pin to a date or remove. |
| In recent years | recently, since (year), in the past (n) years | If recent matters, pick a specific window. |
| Throughout history | (almost always cut) | Rarely true. The claim usually applies to a much narrower window. |
| It is no secret that | (cut entirely) | If everyone knows, the writer has not earned the sentence. |
| Many people believe / It is widely known | (name the people, or drop the claim) | Vague attribution. |
| Imagine a world where | (cut; just describe the situation) | Hypothetical-opener cliché. |

---

## Signposted-conclusion openers

Phrases that announce a conclusion is coming. They tell the reader what to feel rather than letting the conclusion arrive on its own merits.

| AI tell | What it usually means | Notes |
|---|---|---|
| In conclusion | (cut; let the final paragraph stand) | Reading the last paragraph is enough cue. |
| To sum up | (cut) | Same. |
| To summarise | (cut) | Same. |
| Ultimately | (cut, or claim the conclusion directly) | "Ultimately, X" usually works as just "X". |
| In the end | (cut) | Same. |
| All things considered | (cut) | Performs balance the writer has not actually shown. |
| The takeaway is | (cut; just state the takeaway) | The reader does not need a label on it. |
| With that distinction in mind | (cut) | Filler transition. |
| Looking ahead | (cut; or state the specific prediction) | Vague forward-glance. |

---

## Generic positive conclusions

Vague upbeat endings that could be appended to any article. The fix is to replace with a specific fact, observation, or claim.

| AI tell | What it usually means | Notes |
|---|---|---|
| The future looks bright | (replace with a specific plan, statistic, or expectation) | Generic optimism. Name what specifically looks bright and why. |
| Exciting times lie ahead | (replace with a specific upcoming event or development) | Same. |
| This represents a step in the right direction | (claim the specific improvement) | "Right direction" is a placeholder. Say what improved and how. |
| The journey continues | (cut entirely, or name the next stage) | Empty rhetorical close. |
| Only time will tell | (replace with a specific question or test) | Hedged optimism. Name the unresolved question. |
| Continues to thrive | (state the specific evidence of thriving) | Empty without numbers or examples. |

---

## Soft scaffold phrases

Bland labelled-block introductions that mark a generated explainer arranging information into balanced sections. The phrases survive because they are not flashy, which is exactly the problem.

| AI tell | What it usually means | Notes |
|---|---|---|
| One useful area is | (cut; name the area directly) | "One useful area is product design" wants to be "Product design is one example". |
| Another useful area is | (cut; name the area) | Same. |
| The main strength is | (claim the strength directly) | "The main strength is X" wants to be "X". |
| The main risk is | (claim the risk) | Same. |
| Good use usually comes down to | (cut; state what good use looks like) | Vague gesture toward criteria. State them. |
| One thing to consider is | (cut; just consider it) | "One thing to consider is Y" wants to be "Consider Y" or just "Y". |
| It is worth noting that | (cut; note it) | If it is worth noting, just note it. |
| What's interesting is | (cut; state what is interesting) | The writer is announcing rather than showing. |

---

## Manufactured-insight phrasings

Phrases that promise revelation without doing the evidentiary work. They include false revelation ("the real answer is"), contrived contrarianism ("what nobody is talking about"), and privileged perception ("when no one was watching").

| AI tell | What it usually means | Notes |
|---|---|---|
| The real X is | (claim X directly without the "real" frame) | If the writer has the real answer, they can just state it. |
| Here's what's really happening | (state what is happening) | The "really" is doing nothing. |
| What nobody is talking about | (cite a specific source for the silence, or drop) | Almost always false. Many people talk about most things. |
| Contrary to popular belief | (name the belief and source it; or drop) | If the popular belief is real, name it specifically. |
| The uncomfortable truth | (state the truth without the framing) | The framing inflates ordinary claims. |
| What gets lost in the conversation | (state what is missing, with evidence) | Often manufactured. |
| When no one was watching | (cut; the writer probably was not there) | Privileged-perception cliché. |
| Without anyone noticing | (cut) | Same. |
| The shift nobody noticed | (cut, or name the shift and source the silence) | Same. |

---

## Sycophantic / collaborative artifacts

Chatbot turn-taking residue left in published prose. These come from the assistant register and have no business in finished writing.

| AI tell | What it usually means | Notes |
|---|---|---|
| Great question! | (cut entirely) | Never appropriate in published prose. |
| Of course! | (cut) | Same. |
| Certainly! | (cut) | Same. |
| You're absolutely right! | (cut) | Same. |
| I hope this helps! | (cut) | Same. |
| Let me know if you'd like me to expand | (cut) | Same. |
| Here is an overview of | (cut; just give the overview) | Meta-narration that points at the content instead of being it. |
| Would you like | (cut; or rephrase as a direct question to the reader if appropriate) | Chat register. |

---

## Knowledge-cutoff disclaimers

AI hedges about its own training data left in published text. The fix is either to find the actual information or to cut the disclaimer.

| AI tell | What it usually means | Notes |
|---|---|---|
| As of (date) | (cut, or replace with a specific date and source) | Often left over from prompts asking the model what it knows. |
| Up to my last training update | (cut) | Pure model artefact. |
| While specific details are (limited / scarce / not extensively documented) | (find the details, or rewrite the sentence to make a different claim) | If the writer cannot find the detail, the sentence should not pretend to. |
| Based on available information | (cut, or name the source) | Vague hedge. |
| It appears that | (claim it, or hedge with a specific reason) | "It appears that" with no follow-up evidence is empty. |

---

## Contrived contrast / negative parallelism

The "not just X, it's Y" construction and its variants. The problem is structural: a flat interpretation gets dismissed so an inflated abstraction can arrive with fake depth. Substitution does not fix this. The rewrite has to drop the contrast altogether and make a direct claim.

The middle column names what the writer was *trying* to say. The Notes column says how to rewrite.

| AI tell | What it usually means | Notes |
|---|---|---|
| It's not X, it's Y | The writer wants to claim Y but has not supported it | Pick Y, support it with evidence, drop the rejection of X. |
| It's Y, not X | Same as above | Reversing the order does not change the construction. |
| Less X than Y | The writer wants to claim Y but has hedged with the comparison | "Less interesting than important" wants to be "important, because…". |
| More Y than X | Same as Less X than Y | Same construction, opposite framing. |
| Not so much X as Y | Same as above | The "as much" softening adds nothing. |
| Beyond X, it is Y | The writer wants Y to be the subject | "Beyond grief, it becomes a meditation on belonging" wants to be "The film is about how belonging changes after a death." |
| You might think X. Actually, Y | The writer wants to claim Y but has manufactured suspense | Just claim Y. The reader was not thinking X. |
| No X. No Y. Just Z | The writer wants to state Z dramatically | State Z directly. The negation series performs depth without earning it. |

### When the contrast is real

Not every contrast is contrived. A concrete distinction between two specific things ("the laptop is powerful, not cheap") is doing real work. Two named positions in genuine tension ("the problem is not collaboration, the problem is performative attendance") can carry an argument.

The tell is the *inflated reveal*: the second half of the contrast is an abstract noun (meaning, identity, humanity, trust, belonging, connection) that the writer has not actually argued for. If the Y side is concrete and supported, the contrast is probably fine. If the Y side is an abstract payload, rewrite it as a direct claim.

---

## False-concession constructions

Performing balance by staging two generic positions and landing in the middle. Real nuance names the evidence and stakes; false concession just balances abstractions.

The middle column names what the writer was trying to do. Substitution does not work; the rewrite has to drop the staged debate and make a direct claim.

| AI tell | What it usually means | Notes |
|---|---|---|
| While critics argue X, supporters say Y | The writer wants to avoid taking a position | Pick a position, support it. The staged debate is performative. |
| The truth lies somewhere in the middle | The writer has not committed to a claim | Either name the actual middle position with evidence, or drop the framing and pick a side. |
| Both sides have valid points | Same as above | If both sides have valid points, name which points and on what evidence. |
| It depends on context | (when used to dodge) | Acceptable when the dependence is named. Empty when "it depends" is the whole answer. |
| There are merits and drawbacks to both | The writer is dodging | Same as above. List the actual merits and drawbacks. |
| On the one hand X, on the other hand Y | The writer is staging a debate without picking | Pick the side the evidence supports, or admit the question is genuinely open and name what would settle it. |

---

## Bland critical templates

Stock evaluation phrases used in book and film reviews. They sound critical but commit to nothing specific. Common in AI-generated reviews because they are common in the genre's training data.

The middle column says what concrete claim the phrase usually substitutes for. The rewrite has to point at a specific scene, sentence, performance, or formal choice.

| AI tell | What it usually means | Notes |
|---|---|---|
| ambitious in an old-fashioned way | (a specific formal choice the reviewer should name) | What is ambitious about it, and which old-fashioned tradition does it follow? |
| earns its weight | (a specific scene or argument that justifies the length) | Empty without an example. |
| social texture | (specific details about what people do, say, and own in the work) | Replace with the texture itself. |
| emotional range | (the specific emotions the work covers, with examples) | Name two or three of them. |
| field of sympathy | (which characters or positions the work treats with warmth) | Name them. |
| moral strength | (the specific stance the work takes, and on what) | Empty without a position. |
| slow revelation | (what specifically is revealed, and over what time) | Fine when the revelation is named. |
| quietly devastating | (the specific scene or line that does the work) | Cliché unless anchored. |
| richly observed | (the specific observations) | Same. |
| beautifully crafted | (the specific formal choices) | Same. |

---
