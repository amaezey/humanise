Title: Identifying signatures of LLM-generated text

URL Source: https://seantrott.substack.com/p/identifying-signatures-of-llm-generated

Published Time: 2025-04-18T20:41:44+00:00

Markdown Content:
_A few months ago, [paying subscribers voted](https://seantrott.substack.com/p/results-from-poll-5) to see a report on a novel empirical study looking at “signatures” of LLM-generated text. It took a while to find a suitable dataset, conduct the analyses, and write it all up, but the initial results are now in. As I mention in the post below, I plan to continue working on this project and expanding the range of texts, analyses, and LLMs under consideration. Thanks for your support!_

It’s no secret that some people use ChatGPT to help with their writing. Some versions of this seem harmless or even positive, like identifying structural weaknesses in an argument so the writer can improve it. Other versions present genuine challenges to society, from cheating on essays to creating spam or even [persuasive propaganda](https://arxiv.org/abs/2412.17128). More generally, I worry about the erosion in trust that comes with a world in which we find it increasingly difficult to identify when or whether we’re encountering the thoughts of another human being. [As I’ve written before](https://seantrott.substack.com/p/human-culture-in-the-age-of-machines?utm_source=publication-search), LLM-mediated communication might even change the nature of how we use language.

Unfortunately, [detecting LLM-generated (or “synthetic”) text is a hard problem](https://seantrott.substack.com/p/detecting-llm-generated-text-is-hard). That doesn’t mean it’s impossible: given a set of LLM-generated texts and a set of human-generated texts, I think it’s plausible that one can find differences between them—or train another language model to distinguish them. And as you’ll see below, it _is_ possible to find relatively interpretable _signatures_ for a particular sample. My concern (as it often is) is more about both the [construct validity](https://seantrott.substack.com/p/you-cant-escape-construct-validity) and the [generalizability](https://seantrott.substack.com/p/llm-ology-and-the-external-validity) of these signatures, particularly across time[1](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-1), across LLMs, and across humans. Is it even coherent to collapse the variety of “human-generated” and “LLM-generated” texts into two categories, both of which (particularly the former!) might contain multitudes?

I’m not sure. More generally I think we should be very cautious about using automated techniques to “classify” a piece of text as LLM-generated: the costs of a false positive (e.g., to a student turning in an essay) can be really high. Ultimately, the solution to this technological problem may not itself be technical in nature. As I mention at the end of this post, these are ultimately human decisions and I think it would be unwise to hand over the responsibility for making them to an automated system.

That’s also why my interest in this is less about immediate practical application to something like synthetic text detection. Rather, I think there might be something interesting we can learn about whether and how current LLMs differ from humans in the mechanisms and processes by which they produce language. Understanding this could also inform ongoing debates and concerns about [how LLMs could change the way we use language](https://seantrott.substack.com/p/could-language-models-change-language).

Below, I first briefly summarize some of the methods people rely on to classify text as synthetic.

I summarized some of what was _then_ the state-of-the-art in [this 2023 post](https://seantrott.substack.com/p/detecting-llm-generated-text-is-hard). At that point, you could divide the field into a couple of approaches. The first was “feature-based” approaches, in which detection was based on relatively interpretable text features (i.e., the frequency of words in a passage). The second relied on “black box” methods, in which another language model was fine-tuned on examples of human-generated and LLM-generated text—allowing that model to learn _implicit_ (though less interpretable) features that distinguished the categories in the sample.

I did a brief survey of the literature for this project, and as far as I can tell, this taxonomy still largely holds up. Perhaps the most interesting development has been the creation of detection tools that use _metrics_ from other language models as inputs to some kind of classifier. In some cases, these approaches also introduce novel algorithms or decision procedures based on empirical observations about these metrics.

For instance, “[DetectGPT](https://proceedings.mlr.press/v202/mitchell23a.html)” relies on a simple but powerful hypothesis:

> This paper poses a simple hypothesis: minor rewrites of model-generated text tend to have lower log probability under the model than the original sample, while minor rewrites of human-written text may have higher or lower log probability than the original sample.

This is a hypothesis about the relative _curvature_ of LLM-generated vs. human-generated text. Namely, the assumption is that LLM-generated text represents a kind of “local maximum”: the sequences of words produced by an LLM tend to be more likely than some other sequence of words you could’ve generated from the same model. From one perspective, this seems quite straightforward: LLMs produce text by sampling from a probability distribution, so it makes sense that the sequences produced by this process will be more likely than other, conceivable sequences.[2](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-2) That is, if I present a language model with the following text…

> He took a sip from his glass of ____

…I can use that language model to obtain a probability distribution over the most likely subsequent words. If I then sample the most likely word from that distribution (let’s say it’s “water”), then the resulting generated sequence (“He took a sip from his glass of **water**”) will definitionally be higher probability than other conceivable sequences. Predictability is baked into the generation process.[3](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-3)

Further, the authors suggest that human-generated text is _less_ likely to follow this pattern. Of course, humans don’t just produce words at random, but perhaps because there’s a larger diversity of forces influencing which words any given human might produce in any given situation, they’re less likely than a language model to produce the “statistically most likely” word in a sequence.

The authors operationalize this assumption in a clever way. They use another language model to _perturb_ the words in a passage—i.e., selectively rewrite it—and then recalculate the probability of the entire sequence. The idea here is that if LLM-generated text truly represents a local maximum, then any rewrites of that text will be at least slightly _less likely_ (according to another language model) than the original text. The same may not be true of human-generated text, for which rewrites might be more or less predictable than the original text. As it turns out, this assumption turns out to be mostly true: rewriting LLM-generated passages using another LLM makes them systematically _less_ likely—and this change is larger than the change observed for human-generated passages. Further, this was true for texts produced by a variety of GPT-based models.

DetectGPT relied on observations (and assumptions) about the _predictability_ of words generated by a language model. Another source of intuition comes from thinking about the underlying _embedding space_. Recall that [language models represent words as large (e.g., 300-dimensional) “vectors” of numbers](https://www.understandingai.org/p/large-language-models-explained-with) (also called “embeddings”). An entire passage of text is thus represented as a bunch of these vectors in sequence. In theory, one might expect the distribution of LLM-generated vectors to be different from the distribution of human-generated vectors. While both sets of vectors will be the same number of dimensions, they might differ in how many of these dimensions are actually _necessary_ to represent the data, i.e., their [“intrinsic dimensionality”](https://en.wikipedia.org/wiki/Intrinsic_dimension).

Working on a similar intuition as the creators of DetectGPT, [another set of authors](https://proceedings.neurips.cc/paper_files/paper/2023/file/7baa48bc166aa2013d78cbdc15010530-Paper-Conference.pdf) argued that one might expect LLM-generated text to have a lower intrinsic dimensionality than human-generated text. That is, LLM-generated texts should be describable in fewer dimensions than human-generated texts.[4](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-4) Using a particular measure of intrinsic dimensionality called _[persistent homology dimension](https://en.wikipedia.org/wiki/Persistent\_homology)_, the authors found that indeed, English texts produced by various LLMs had lower intrinsic dimensionality than texts on analogous topics produced by humans. Another interesting result was that their approach was less likely than other approaches to _misclassify_ text produced by non-native English speakers as synthetic, i.e., it had a lower false positive rate.[5](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-5)

As I mentioned at the top of this section, the field of synthetic text detection is relatively large and relies on a number of different methods and techniques. I haven’t exhaustively surveyed them here; rather, my goal was to present the underlying logic and intuition behind two pretty successful approaches—both of which I drew inspiration from.

My core question was whether there are statistical or geometric signatures that reliably distinguish LLM-generated text from human-generated text.

To answer this, I first needed a suitable dataset. This was probably the hardest step, and also the most vulnerable to criticism. Any sample is subject to limitations: most notably, are the text samples actually _representative_ of the broader “population” of LLM-generated and human-generated texts? If they’re not—either because the wrong LLMs were used, or because they were prompted in inappropriate or unrepresentative ways—then one can’t really draw generalizable conclusions.

As a starting point, I selected the dataset from [this 2023 paper](https://pubmed.ncbi.nlm.nih.gov/37903836/) analyzing argumentative essays written by (mostly) high school students on a fixed number of topics (e.g., “Should students be taught to cooperate or to compete?”).[6](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-6) Using those same topics, the authors of that paper prompted ChatGPT-3 and ChatGPT-4[7](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-7) with the following instructions:

> Write an essay with about 200 words on “[topic]”

The authors carried out a number of analyses on these essays, including a human annotation study. For instance, they found that a separate pool of humans tended to rate the essays generated by the LLMs (particularly ChatGPT-4) as more “logical” and “complex” than those written by the students.[8](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-8)

As I see it, there are two main limitations of this dataset. The first is that the study was done in 2023, so the LLMs used are almost certainly outdated—thus, any inferences we draw have to be limited to ChatGPT-3 and ChatGPT-4. That said, as noted above, the authors _did_ find that the LLM-generated essays nonetheless received higher ratings on a number of dimensions than the human essays—suggesting that relying on these older LLMs didn’t hurt their performance too much. Further, I’m less interested in characterizing their “capabilities” than in identifying specific signatures that mark LLM-generated text.

The other key limitation is that the context (writing an argumentative essay) and topics (**N = 90**) are pretty constrained. [As recent work by my friend Cameron Jones reports](https://arxiv.org/abs/2503.23674), state-of-the-art language models _do_ reliably pass for human in a number of interactive contexts, suggesting that in the right setting, LLM-generated text might resemble human-generated text more closely. (That said, _[other](https://arxiv.org/pdf/2407.08853)_[recent work by Cameron](https://arxiv.org/pdf/2407.08853) suggests that statistical properties of the text from that same study—like curvature—are more reliable predictors!)

My primary interest was in whether a set of interpretable metrics could reliably distinguish LLM-generated from human-generated text. I had a few criteria for selecting these metrics:

*   First, I wanted to use metrics that could be derived from open-source language models, not just the closed models offered by companies like OpenAI or Anthropic. It was also critical to use models _other than_ the models used to generate the text, since it wouldn’t be particularly surprising if GPT-3 found text generated by GPT-3 to be more predictable.

*   Second, I wanted them to be both _meaningful_ and _interpretable_. That is, I didn’t just want to train a black box LLM to classify text as LLM-generated vs. human-generated. Rather, I wanted metrics that might themselves tell us something interesting about how these samples differed (if they did differ).

To satisfy the first criterion, I selected language models from the open-source Pythia suite. One reason I really like the Pythia suite is that the details of the training process (and training data), as well as the final set of weights, have all been made public by EleutherAI. They’ve even released a number of training _checkpoints_ for each model, as well as nine random seeds (i.e., “versions”) of each model size. They’re doing a lot to improve the reproducibility and transparency of LLM-ology. I used four Pythia models, ranging in size from 14M parameters to 410M parameters.

To satisfy the second criterion, I drew inspiration from the related work I summarized above. Specifically, I focused on metrics reflecting either the _predictability_ of text or the _geometry_ of the embeddings representing that text. “Predictability” was measured in a few ways, including the average surprisal (i.e., inverse predictability) of words in a passage, according to the four Pythia models. I also measured the _entropy_ of the probability distribution over subsequent tokens, which reflects the degree to which context constrained (low entropy) or didn’t constrain (high entropy) the specificity of the prediction. “Geometry” was also measured in a few ways, including intrinsic dimensionality (which I assessed using the _[skdim](https://scikit-dimension.readthedocs.io/en/latest/api.html#id-estimators)_[package](https://scikit-dimension.readthedocs.io/en/latest/api.html#id-estimators) in Python) and the average cosine distance between each subsequent embedding.

Again, the intuition here is that we might expect LLM-generated text to be _more_ predictable and also require _fewer dimensions_ to represent it than human-generated text. That’s operating on the assumption that LLMs follow a relatively fixed process when producing tokens that is itself driven by predictability; humans probably do so to some extent too, but the assumption is (again) that they do so less than LLMs. While we can’t observe the process by which humans produce language directly, we _can_ use these empirical metrics to test our intuitions.

I looked at a number of metrics, and in some cases the analyses got pretty complicated, so I’m going to focus here on what I found both most interesting and most surprising. At a high-level, each metric was analyzed the same way, i.e., using a _regression model_ comparing that metric to the underlying condition (i.e., Student vs. ChatGPT-3 vs. ChatGPT-4). In each case, I asked whether there were significant differences in that metric across each pair of conditions _across_ all the Pythia models used to assess the metric—i.e., accounting for the fact that some of the Pythia models might show a bigger effect than others.[9](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-9)

I’ll start with metrics reflecting **predictability**, such as the average surprisal of words in a passage. All of the Pythia models tested showed differences in the average surprisal: specifically, in each case, words written by humans were _less predictable_ (more “surprising”) than words generated by either ChatGPT-3 or ChatGPT-4. This wasn’t necessarily surprising, but it was nice to see my intuition validated—as depicted below, the effect was pretty robust.

More surprising was the finding that words in human essays were also more _variable_ in their predictability. That is, the standard deviation of surprisal was significantly higher for human essays than for ChatGPT-3; when it came to human essay vs. ChatGPT-4, the difference hovered right on the significance threshold—as you can see below, it was most pronounced (and quite clear) for the larger Pythia models.[10](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-10)

[![Image 1](https://substackcdn.com/image/fetch/$s_!a5ct!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bfc7e2b-0907-4b91-8755-8dc12fbf493b_14000x5500.png)](https://substackcdn.com/image/fetch/$s_!a5ct!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6bfc7e2b-0907-4b91-8755-8dc12fbf493b_14000x5500.png)

Left: mean surprisal of words in passages generated by students, ChatGPT-3, and ChatGPT-4. Higher values indicate more “surprising” words overall (i.e., less predictable). Right: standard deviation of surprisal for words in passages across conditions. Here, higher values indicate more _variance_ in the predictability of words.

Turning now to the **geometry** of the embedding spaces: recall that I used a variety of measures, including the average cosine distance between subsequent tokens, as well as two measures of intrinsic dimensionality. For some of these metrics, the effects were much less robust. Contrary to [preliminary analyses of cosine distance](https://x.com/colin_fraser/status/1768781710433395060), I found that in some cases the average cosine distance was _larger_ for texts generated by ChatGPT-4 than for texts generated by students; in fact, different Pythia models showed pretty different results here, so the overall results came out to a wash.

The intrinsic dimensionality results were more promising. Below, you can see the distribution of (z-scored) intrinsic dimensionality scores for each passage type. Particularly for the larger evaluation models (like Pythia-410M), it does seem like the student passages have a consistently higher I.D. score. This was also borne out by the results of a statistical analysis. Interestingly, the difference in I.D. scores also appeared to be modulated by the _layer_ that those scores were calculated for. Each LLM consisted of multiple “layers”, each of which forms different representations of each word in the input. As depicted in the figure below, the gap between the I.D. of student vs. ChatGPT-4 essays seemed particularly large in the later layers of each model.

[![Image 2](https://substackcdn.com/image/fetch/$s_!2OQQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff70f42f1-f35f-48c4-b7aa-bef8db1f8825_14000x5500.png)](https://substackcdn.com/image/fetch/$s_!2OQQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff70f42f1-f35f-48c4-b7aa-bef8db1f8825_14000x5500.png)

Left: distribution of I.D. scores (using the Two-NN algorithm) for each passage type. Scores were z-scored within layer, within model, to account for the effect of anisotropy. Higher scores indicate higher I.D., i.e., more dimensions were needed to represent the passage. Right: average I.D. across passage types for each layer in the model (also z-scored). 

At this point, it was clear that some metrics were reliably distinct, while others were not. Another way to assess this is to take a machine learning approach, in which we fit a _classifier_ using those metrics to predict the label for a category—student, ChatGPT-3, or ChatGPT-4—and ask which metrics lead to the highest accuracy. To do this, I fed each of the predictability features from each Pythia model into a separate random forest classifier and asked how well that classifier predicted the label of “held-out” data it hadn’t seen yet (i.e., using cross-validation). I calculated the accuracy both of using each individual feature (e.g., only average surprisal), as well as combinations of features. Note that there were three evenly distributed labels, so chance performance would be ~33%.

Each Pythia model achieved relatively good performance equipped only with information about the average surprisal of a passage: for instance, Pythia-70M classified passages with **~86% accuracy**.[11](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-11) When I allowed the classifier for each model to use _multiple_ features, accuracy rose to **≥94%** across the board (reaching **~97%** for both 160M and 410M).[12](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-12)

My primary interest with this project was whether there were any meaningful, interpretable _signatures_ that reliably distinguished LLM-generated text from human-generated text. Focusing on a relatively small sample of texts, I found that there were indeed several such metrics. The most interpretable were those relating to predictability: on average, texts written by the humans in the sample had less predictable words than those written by ChatGPT-3 or ChatGPT-4. In some cases, those texts also exhibited more _variability_ in how predictable words were.

Both observations are consistent with the intuition that humans select which word to use in a given context for a variety of reasons—and further, that _different_ humans probably do so differently. If this result is generalizable (see more caveats below), one theoretically and practically relevant insight is this: as people rely more and more on LLMs to produce text for them, we might expect instances of language use to be more and more predictable. This is what I called the _[homogenization hypothesis](https://seantrott.substack.com/p/human-culture-in-the-age-of-machines)_[in a previous post](https://seantrott.substack.com/p/human-culture-in-the-age-of-machines), and it’s something I worry about more generally when it comes to the creation of cultural and communicative artifacts using LLMs.

Of course, there are some pretty clear limitations with my analysis that prevents us from drawing strong conclusions. For one, the sample of passages is very small and constrained: all these results really show is that two LLMs (ChatGPT-3 and ChatGPT-4) produce more predictable passages than high school students when it comes to argumentative essays on certain topics. It’s unclear whether these results generalize to other topics, registers, or other writers (human or LLMs).

In part for this reason, I don’t think it would be wise or ethical to rely on metrics such as these to categorize texts (say, student essays) as LLM-generated. Even a high accuracy rate (on this limited sample) could translate into a relatively high _false positive rate_, which could cause real harm to students. And beyond questions about generalizability, I’m quite wary of handing over the responsibility of making these difficult decisions to some kind of automated or algorithmic tool—and that includes synthetic text detection. Ultimately, I think that humans should remain accountable both for the words we produce and for the decisions we make about the words we encounter.

[2](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-2)

Of course, changing the “temperature” of the sampling process—i.e., the extent to which you sample only the highest-probability words—will determine the extent to which this is true.

[3](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-3)

Again, depending on temperature.

[4](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-4)

More technically: the “real data” might plausibly lie on some lower-dimensional manifold, and the manifold for LLM-generated data will be lower-dimensional than that for human-generated data.

[5](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-5)

This is especially important, as a particularly damaging outcome of deploying synthetic text detection methods “in the wild” would be this kind of false positive.

[6](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-6)

Thanks to Sidney Ma, a former student of mine, for pointing me to this dataset. Sidney’s carried out his own very interesting analysis of the dataset, which you can find [here](https://github.com/sidneytma/gpt_syntax_ngram_classifier).

[7](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-7)

Using the browser version of the tool.

[8](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-8)

The authors argue that these results suggest we should change how writing is taught. From the abstract: “We must re-invent homework and develop teaching concepts that utilize these AI models in the same way as math utilizes the calculator: teach the general concepts first and then use AI tools to free up time for other learning objectives.” I don’t think I agree, particularly for writing—though I’ll note this is fundamentally a point about values than one that can be addressed empirically.

[9](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-9)

This was a design decision that could’ve gone another way: it would’ve also been perfectly defensible to look at whether _any_ of the Pythia models showed an effect for a given metric. The approach I took was slightly more conservative in that it was less likely to find any effect.

[10](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-10)

Here, the difference between human and ChatGPT-4 essays was significant for the larger Pythia models, but not for the smaller ones, which is why the overall difference was only “trending”.

[11](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-11)

The other scores using this metric alone were ~73% (14M), 85% (160M), and 84% (410M).

[12](https://seantrott.substack.com/p/identifying-signatures-of-llm-generated#footnote-anchor-12)

Presumably, accuracy could be further improved by using _all_ the Pythia models in a single classifier (i.e., a “team” of Pythias), but my interest was in evaluating the accuracy of each model independently.
