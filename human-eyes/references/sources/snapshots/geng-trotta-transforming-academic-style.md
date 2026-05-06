# Is ChatGPT Transforming Academics Writing Style?

- **Source URL:** https://arxiv.org/pdf/2404.08627
- **Snapshot method:** arXiv PDF text extraction
- **Retrieved:** 2026-05-05

## Article Body

Is ChatGPT Transforming Academics’ Writing Style?

                                        Mingmeng Geng                                                                                   mgeng@sissa.it
                                        International School for Advanced Studies (SISSA), Trieste, Italy.

                                        Roberto Trotta                                                                                  rtrotta@sissa.it
                                        International School for Advanced Studies (SISSA), Trieste, Italy.
                                        Imperial College London, London, UK.

arXiv:2404.08627v2 [cs.CL] 8 Nov 2024
                                                                                            Abstract

                                                Based on one million arXiv papers submitted from May 2018 to January 2024, we assess the
                                                textual density of ChatGPT’s writing style in their abstracts through a statistical analysis
                                                of word frequency changes. Our model is calibrated and validated on a mixture of real
                                                abstracts and ChatGPT-modified abstracts (simulated data) after a careful noise analysis.
                                                The words used for estimation are not fixed but adaptive, including those with decreasing
                                                frequency. We find that large language models (LLMs), represented by ChatGPT, are having
                                                an increasing impact on arXiv abstracts, especially in the field of computer science, where
                                                the fraction of LLM-style abstracts is estimated to be approximately 35%, if we take the
                                                responses of GPT-3.5 to one simple prompt, “revise the following sentences”, as a baseline.
                                                We conclude with an analysis of both positive and negative aspects of the penetration of
                                                LLMs into academics’ writing style.

                                        1    Introduction
                                        Since ChatGPT (Chat Generative Pre-trained Transformer) was released on November 30, 2022, large
                                        language models (LLMs) have started to be widely exploited and therefore affect many aspects of our lives.
                                        In this paper, we are concerned with whether LLMs, represented by ChatGPT, are transforming academic
                                        writing.
                                        Many papers have already explored the advantages and disadvantages of LLMs (Kasneci et al., 2023).
                                        Although they can increase productivity and may help scientific discovery (Noy & Zhang, 2023; AI4Science &
                                        Quantum, 2023), the potential risks of using LLMs in academia cannot be ignored (Lund et al., 2023), such
                                        as generating incorrect references (Walters & Wilder, 2023).
                                        Researchers have been working on machine-generated text detection since a few years ago (Bakhtin et al.,
                                        2019; Gehrmann et al., 2019), which have attracted more attention shortly after ChatGPT appeared (Mitchell
                                        et al., 2023; Guo et al., 2023). At the same time, questions have been raised about the reliability of these
                                        detectors (Sadasivan et al., 2023). Detection and counter-detection of LLM-generated text soon developed
                                        cat-and-mouse games, such as watermarking (Kirchenbauer et al., 2023), paraphrasing (Sadasivan et al.,
                                        2023), and the combination of both (Krishna et al., 2024). Besides, distinguishing between human and LLM
                                        writing samples is also sometimes not easy for human experts (Casal & Kessler, 2023).
                                        While there is already a corpus of current research on using ChatGPT in academia (Casal & Kessler, 2023;
                                        Lingard et al., 2023; Fergus et al., 2023; Lund et al., 2023), to our knowledge only a handful of works have
                                        attempted to quantify its impact on the whole academic community. It was only when the first version of
                                        this paper was completed that two preprints appeared that addressed related questions: one focuses on AI
                                        conferences peer reviews (Liang et al., 2024a) and analyzes scientific papers (Liang et al., 2024b). They claim
                                        that the usage of LLMs is evident in AI conference reviews and scientific writings, especially in computer
                                        science papers.
                                        Within the broad field of academic writing and publishing, we chose the abstracts of articles as the focus of
                                        this work, as they have a relatively uniform format across disciplines, are supposed to condense an entire

                                                                                                 1

research article and thus are often highly polished, and can be considered short articles of pure text, not
involving pictures nor tables.
Of course, LLMs can generate abstracts directly given a suitable prompt (Luo et al., 2023), and studies
have shown that identifying such abstracts is not easy even if they remain unedited by humans (Gao et al.,
2023; Cheng et al., 2023). We have previously discussed methods for detecting LLM-generated text, but the
detection of a mixture of human and machine-generated text is usually much harder (Krishna et al., 2024;
Zhang et al., 2024). Determining whether a given few sentences were generated by LLMs is difficult, but it
is feasible to estimate the extent to which millions of sentences are influenced by LLMs. We analyzed the
fingerprints of LLMs on scientific abstracts as a function of time in order to tease out a statistical signature,
rather than a binary classification.
In fact, that the abstract of a paper shows what we call the “ChatGPT style” or “LLM style” does not
necessarily mean that the authors directly utilized LLM to generate or modify it. It is also possible that the
authors used LLM in another context and that, as a result, their writing habits were influenced by the LLM
style – not a remote possibility.
It is worth considering in this context that reading and writing in English is more difficult for non-native
English academics (Amano et al., 2023). Before ChatGPT was released, the pros and cons of other tools were
discussed, such as Google Translate (Mundt & Groves, 2016) and Grammarly (Fitria, 2021), but ChatGPT
has a much wider range of application scenarios – not to mention, a much higher flexibility.
We have seen similar AI-induced seismic shifts in the past: after AlphaGo (Silver et al., 2017) shocked the
world, professional Go players have begun training with AI, and the sport of Go has been profoundly changed
as a result (Kang et al., 2022). A similar story may be happening with academic writing, especially for
researchers whose first language is not English (Hwang et al., 2023). This paper is a first effort at establishing
whether this is the case.
We also think that analytical rigor is a higher priority than comprehensiveness, and the former is our focus
in this paper. Once the reliability of a single analysis is assured, the comprehensive analysis can be more
convincing. For example, we should use a more adaptive approach to selecting words for estimation, as well
as considering words with decreasing frequency.

2     Data

arXiv dataset The metadata of arXiv papers are provided by Kaggle (arXiv.org submitters, 2024). Because
the abstracts in this dataset are updated when authors submit changes, we used the first version in 2024
(version 161) as well as the last version before the ChatGPT era (version 105). Our observations and analysis
are based on one million arXiv articles submitted from May 2018 to January 2024.

English word frequency Google Ngram dataset is chosen for comparison and reference (Michel et al., 2011).
Specifically, we used the freely available mirrors on Kaggle (http://kaggle.com/datasets/wheelercode/
english-word-frequency-list) covering word frequencies from the 1800s to 2019 as established from
Google Books.

3     Observations and analysis

3.1   Changes in word frequency

We approach the problem by analyzing how the frequency of words changes after ChatGPT has been deployed.
The frequency of some non-specialized words also starts to skyrocket in early 2023, as presented in Figure
1 (1 million abstracts are divided into 100 uneven time-periods, each encompassing 10,000 abstracts). The
number of arXiv articles is getting more and more each month. In general, the larger the sample (the greater
the number of articles), the more accurate the estimate will be. We used a similar number of articles in each
period rather than the same time interval to keep the error in the estimates on the same scale, providing the
same quality of observation and estimation.

                                                        2

(a) Examples of words with rapidly growing frequency in           (b) The words “are” and “is” are decreasing in frequency
arXiv abstracts.                                                  in arXiv abstracts.

Figure 1: Word frequency changes in abstracts. The vertical red dashed line demarcates the first time period
after ChatGPT’s release.

How could the frequencies of words like “significant” grow significantly together? Another striking example
is the frequency change of the words “are" and “is”. The counts in 10,000 abstracts of these two words were
quite stable before 2023. However, the frequency of these two terms has dropped by more than 10% in 2023.
These examples, anecdotal as they are, may represent the tip of the iceberg of a wider and growing phenomenon:
the rapid increase in the usage of ChatGPT or other LLMs. The rise and fall in frequency of specific technical
nouns may well be related to the changing popularity of certain research topics, but that a research trend is
responsible for the change in usage of adjectives appears implausible – even less so for words like “is” and
“are”.

3.2   LLM simulations

We wanted to be more specific about the impact of LLMs on articles from different disciplines, so the arXiv
abstracts from different categories were examined separately. The one million arXiv articles were divided
into 20 periods in this part in order to increase the number of articles per period and reduce estimation
error, which is not the same as the previous part. The identifier numbers of the first and last arXiv articles
corresponding to each period are given in the section A of the Appendix.
The emergence of other LLMs is also inspired or influenced by ChatGPT, and we also assume that other
LLMs have similar but not identical word preferences to ChatGPT. The most recent articles we processed
were submitted in January 2024, when other LLMs should be less utilized. Therefore, we used ChatGPT for
simulations.
Previous studies have shown that ChatGPT has its own linguistic style (AlAfnan & MohdZuki, 2023), and
that likely includes the frequency of some words. Although there is no direct way to investigate ChatGPT’s
word preference, we can ask ChatGPT to polish or rewrite real, pre-2023 abstracts, and use the resulting
simulation data to calculate the estimated frequency change rate r̂ij of word i in category j:

                                                       d     d          d
                                                     q̃ij − qij       q̃ij
                                            r̂ij =       d
                                                                  =    d
                                                                             −1                                        (1)
                                                        qij           qij

where qij
       d
          represents the word frequency of real abstracts in the dataset and q̃ij
                                                                               d
                                                                                  means the frequency after
ChatGPT processing.

                                                              3

What are the prompts used in the real cases are still unclear, and we think simple prompts could better
reflect the inherent word preferences of ChatGPT, as complex prompts may bring more human interference.
So some simple prompts were used to reduce the bias due to prompts, for example,

                                      “Revise the following sentences:”

GPT-3.5 was utilized in our simulations for 10,000 abstracts in period 14 (April 2022 to July 2022), although
it may not have the same word preferences as other LLMs. Many words have different frequencies before
and after ChatGPT processing, such as the words “is”, “are”, and “significant” that we mentioned earlier.
For simplicity, the results of the 4 categories with the highest number of articles are shown in Table 1 and
the rest parts in this paper, namely cs (computer science), math (mathematics), astro (astrophysics), and
cond-mat (condensed matter).

               Table 1: Word frequency (per abstract) before and after ChatGPT processing.

                        words         category     before        after      change rate
                        is, are          cs       2.01, 1.00   1.73, 0.83   -14%, -17%
                        is, are         math      1.78, 0.74   1.61, 0.71     -9%, -5%
                        is, are         astro     2.13, 1.39   1.90, 1.25    -11%, -1%
                        is, are       cond-mat    2.00, 0.92   1.68, 0.80   -16%, -13%
                        significant      cs          0.09         0.18          99%
                        significant     math         0.01         0.03          308%
                        significant     astro        0.17         0.26          53%
                        significant   cond-mat       0.07         0.18          171%

This corroborates the hypothesis, formulated earlier, that the drop in the frequency of these two words
observed in real abstracts in 2023 may have been caused by ChatGPT. Combined with Figure 6 in the
Appendix showing the correlation between changes in simulated and real data, we speculate that ChatGPT
is one of the important reasons, possibly even the main reason, for the recent word frequency change in
abstracts.
Our next step is to start by modeling LLM impact or ChatGPT impact, as well as estimating the impact
based on real data and simulations. In order to minimize the impact of the research topic, different words
should be used for estimation for different paper categories. And it is important to consider not only words
that increase in frequency, but also those that decrease in frequency.

4     LLM impact
4.1   Simple model

Imagine different scenarios of using LLMs in scientific writing: a researcher might simply use it to correct
grammatical errors, another employs it for translating native sentences into English, and yet another one
wants it to polish their draft in English very purposefully. In theory, each of these use cases contributes the
same proportion of LLM usage. But, as is well known, different prompts will lead to different outputs, which
means different word frequency changes. Therefore, we use the more neutral term “LLM impact” instead of
“proportion” in our estimation part. Because the estimates in this paper are based on ChatGPT simulations,
it can also be called “ChatGPT impact”.
We start with a simple model, ignoring noise and variability for this subsection. Suppose that the frequency
of word i for abstracts in subject category j changes from fij∗
                                                                 to f˜ij
                                                                      ∗
                                                                         after being processed by ChatGPT, when
it’s used as a means to polish and improve the abstract (if not to fully generate it). The corresponding word
change rate is defined as
                                                  f˜ij
                                                    ∗      ∗
                                                       − fij  f˜ij
                                                                ∗
                                           r̄ij =       ∗    = ∗ − 1.                                        (2)
                                                       fij    fij

                                                       4

Suppose that f¯ij (t) is the word frequency for word i in category j at time period t, this can be written as:

                    f¯ij (t) = (1 − ηj (t))fij
                                            ∗
                                               (t) + ηj (t)fij
                                                            ∗
                                                               (t)(r̄ij + 1) = fij
                                                                                ∗
                                                                                   (t) + ηj (t)fij
                                                                                                ∗
                                                                                                   (t)r̄ij            (3)

where ηj (t) denotes the proportion of abstracts in category j affected by LLMs, and fij
                                                                                      ∗
                                                                                         (t) represents the
original evolution in word frequency without LLMs.
Unfortunately, we cannot know the true value of fij    ∗
                                                         (t) in the LLM era, but we can replace it with the
            ˆ
estimation fij (t) based on the word frequency before LLM was introduced. As our objective is to identify
             ∗

the words that LLM “likes” (or “dislikes”) to use compared to academic researchers on average, we assume
that the frequencies of these words should remain stable without LLM, i.e., we take the average of the
pre-ChatGPT periods before T0 as following:
                                                1       X
                                   ∗
                                  fij (t) =                    d
                                                             fij (t), if t > T0 .                        (4)
                                            #{t ≤ T0 }
                                                                 t≤T0

For a specified word i, we will have one estimate of ηj (t), as r̄ij and fij
                                                                          ∗
                                                                             (t) could be approximated with Eq. (1)
and Eq. (4). We are also likely to get better results after combining the estimates of different words.
However, this model is highly idealized: we have to additionally consider the effects of noise (such as
randomness inside LLM), uncertainty in word usage evolution without LLM, and the epistemic uncertainty
in how users actually prompt LLMs.

4.2   Noise model

We now consider the noise terms, which might be modeled in many different ways.
For instance, we denote the word frequency for word i in category j by fij
                                                                        d
                                                                           , which represents the word
frequency observed in the data:
                                          d
                                         fij = fij
                                                ∗
                                                   + δij (fij
                                                           ∗
                                                              )                                     (5)
where δij (·) represents noise and word usage variability which are not directly related to the internal parameters
of LLM.
                                                                                                     δ,η
After taking into account the impact of LLMs, we split the word frequencies fij
                                                                             d
                                                                                (t) into two parts, fij  (t) and
 δ,1−η
fij    (t), while they both have corresponding noise terms:
                                   δ,η
                                  fij  (t) = ηj (t)fij
                                                    ∗
                                                       (t) + δij (ηj (t)fij
                                                                         ∗
                                                                            (t))                                      (6)
                                δ,1−η
                               fij    (t) = (1 − ηj (t))fij
                                                         ∗
                                                            (t) + δij ((1 − ηj (t))fij
                                                                                    ∗
                                                                                       (t)) .                         (7)

In this case, the equation corresponding to Eq. (3) is
                                                                            δ,η         δ,1−η             δ,η
           d
          fij (t) = (1 − ηj (t))fij
                                 ∗
                                    (t) + δij ((1 − ηj (t))fij
                                                            ∗
                                                               (t)) + Cij (fij  (t)) = fij    (t) + Cij (fij  (t))    (8)

where the function Cij (·) means the frequency after LLM process.
We assume that the noise in the “real” data and in the simulations due to LLM processing can be represented
as ϵij (·) and ϵsij (·), then Eq. (1) and Eq. (2) are related by

                                     f˜ij
                                       ∗
                                          − ϵij (fij
                                                   ∗
                                                     ) − fij
                                                          ∗      d
                                                               q̃ij − ϵsij (qij
                                                                              d
                                                                                ) − qij
                                                                                     d

                                                 ∗           =              d
                                                                                        .                             (9)
                                               fij                        qij

Therefore,
                                           δ,η         δ,η
                                     Cij (fij  (t)) = fij  (t)(r̂ij + 1 + ϵηij (q, f, t))                            (10)
where
                                                                  δ,η
                                                            ϵij (fij  (t))       ϵsij (qij
                                                                                        d
                                                                                           )
                                         ϵηij (q, f, t) =      δ,η
                                                                             −       d
                                                                                               .                     (11)
                                                              fij  (t)              qij

                                                                 5

Then, Eq. (8) – representing the difference in word frequency before and after LLM processing – can be
rewritten as
                                d
                               fij (t) − fij
                                          ∗
                                             (t) = ηj (t)xij (t) + gij (t) + ξij (t)               (12)
where
                     xij (t) =fij
                               ∗
                                  (t)r̂ij                                                                    (13)
                     gij (t) =ηj (t)fij
                                     ∗
                                        (t)ϵηij (q, f, t)                                                    (14)
                     ξij (t) =(r̂ij + 1 + ϵηij (q, f, t))δij (ηj (t)fij
                                                                     ∗
                                                                        (t)) + δij
                                                                                ′
                                                                                   ((1 − ηj (t))fij
                                                                                                 ∗
                                                                                                    (t)) .   (15)
where δij
        ′
           (·) follows the same distribution as δij (·). It should be noted that gij (t) includes only LLM-related
noise ϵij (·) and ϵsij (·), however ξij (t) contains δij (·) and δij
                                                                  ′
                                                                     (·) that are unrelated to LLM.

4.3     Impact estimation and bias analysis

In many data analysis applications, more data point (in our case, using a larger number of words) means
better estimates. But in our case, the effect of noise is different for each data point (word), and choosing
wisely which words to include can improve our estimates.
For simplicity, we define
                                                    hij (t) = fij
                                                               d
                                                                  (t) − fij
                                                                         ∗
                                                                            (t) .                            (16)
For abstracts in category j, we use the words in the subset Ij (whose determination is discussed below), of
numerosity nj . In order to estimate ηj (t), we can use the quadratic loss function
                                     1 X                              1 X
                      Lj,t (ηj ) =       (hij (t) − ηj (t)xij (t))2 =     (gij (t) + ξij (t))2 .             (17)
                                     nj                               nj
                                        i∈Ij                                        i∈Ij

If we ignored the dependency of gij (t) and ξij (t) on ηj (t), the estimate of LLM impact would simply be given
by Ordinary Least Squares (OLS) as

                                                      i∈Ij hij (t)xij (t)
                                                    P
                                          η̂j (t) =                       .                                (18)
                                                          i∈Ij xij (t)
                                                                 2
                                                       P

However, since gij (t) also depends on ηj (t) and ξij contains ηj (t) as described in Eq. (14) and Eq. (15), we
need to make additional assumptions to progress further.
Case 1: if the effect of ηj (t) on ξij (t) can be ignored compared to other terms, e.g., the following simple
scenario,
                                Var[δij (ηj (t)fij
                                                ∗
                                                   (t))] ≪ ηj (t)fij
                                                                  ∗
                                                                     (t)Var[ϵηij (q, f, t)]               (19)
One can also derive the approximation below:
                                                  δ,η
                                                 fij  (t) ≈ ηj (t)fij
                                                                   ∗
                                                                      (t) + δij (∗)                          (20)
where δij (∗) is a random variable with zero mean and variance much smaller than ηj (t)fij
                                                                                        ∗
                                                                                           (t), and its derivative
with respect to ηj (t) is negligible compared to fij (t).
                                                  ∗

Therefore, the loss function under this assumption is:
                                     1 X                                        1 X 2
                      Lj,t,g (ηj ) =     (hij (t) − ηj (t)xij (t) − gij (t))2 =    ξij (t) .                 (21)
                                     nj                                         nj
                                            i∈Ij                                                i∈Ij

Thus,
                     ∂Lj,t,g (ηj )   2 X                                   2 X
                                   =     ηj (t)x2ij (t) − hij (t)xij (t) +     xij (t)gij (t)
                                                                        
                        ∂ηj          nj                                    nj
                                            i∈Ij                                            i∈Ij
                                                                                                             (22)
                                            2 X ∂gij (t)
                                       −                          (hij (t) − ηj (t)xij (t) − gij (t))
                                            nj          ∂ηj (t)
                                                 i∈Ij

                                                                    6

                                            ∂L          (η )
If we require a minimum by setting j,t,g ∂ηj
                                              j
                                                 = 0, we obtain a new estimate η̂jg (t), which is equal to the OLS
η̂j (t) in Eq. (18) corrected for bias and noise,
                                                X                   X ∂gij (t)
                         (η̂jg (t) − η̂j (t))          x2ij (t) =                    (hij (t) − ηj (t)xij (t))
                                                                           ∂ηj (t)
                                                i∈Ij                i∈Ij
                                                                                                                                (23)
                                                                        X                         X                ∂gij (t)
                                                                    −          xij (t)gij (t) −          gij (t)            .
                                                                                                                   ∂ηj (t)
                                                                        i∈Ij                      i∈Ij

But without knowing the distribution of ϵij (·) and ϵsij (·), we have no way of estimating the value of this bias,
so we assume that ϵij (fij ) ∼ N (0, fij σij,ϵ
                                          2
                                               ) and ϵsij (fij ) ∼ N (0, fij σij,ϵ
                                                                              2
                                                                                   ), e.g., ϵij (1) ∼ N (0, σij,ϵ
                                                                                                             2
                                                                                                                  ), then we can
obtain an expression for ϵηij (q, f, t):

                                                               ϵij (1)          ϵsij (1)
                                ϵηij (q, f, t) = q                            − q                                               (24)
                                                                ∗ (t) + δ (∗)
                                                         ηj (t)fij                    d
                                                                         ij          qij
                                                         ηj (t)fij
                                                                ∗
                                                                   (t)ϵij (1)             ηj (t)fij
                                                                                                 ∗
                                                                                                    (t)ϵs (1)
                                      gij (t) = q                                     −          q ij         .                 (25)
                                                         ηj (t)fij
                                                                ∗ (t) + δ (∗)
                                                                         ij
                                                                                                     d
                                                                                                    qij

After calculations (see appendix), the bias part is expressed as
                                                                h                  i
                                                                         ∂g (t)
                                                               E gij (t) ∂ηijj (t)
                                                        P
                                                         i∈I j
                                   η̂j (t) − η̂jg (t) =                              .                                          (26)
                                                            i∈Ij (fij (t)r̂ij )
                                                                   ∗
                                                          P                     2

Some insights can be gained from the results above. As by definition ηj (t) ≥ 0, the estimate η̂j (t) given by
Eq. (18) tends to be biased high in our model. The value of r̂ij plays a role in the minimization of bias, as it
only appears in the denominator in Eq. (26).
Similarly, if the value of r̂ij is similar for different words, then larger values of qij d
                                                                                            and fij
                                                                                                  ∗
                                                                                                    will reduce the
bias, as seen from Eq. (35) – therefore, we should consider including preferentially in our analysis words
with larger values of qij
                        d
                          , fij
                              ∗
                                and |r̂ij |. Considering that the value of ηj (t) affects the bias as well, which is
not simply linear, we are led to consider adaptive or iterative criteria for word choice, which will in general
depend on the true (and unknown) value of ηj (t).
Case 2: Gaussian distribution for δij (fij ), e.g., δij (fij ) ∼ N (0, fij σij
                                                                            2
                                                                               ), which is inspired by central limit
theorem and justified empirically in the Appendix, Figure 8. As a result,

                             ξij (t) =(r̂ij + ϵηij (q, f, t))δij (ηj (t)fij
                                                                         ∗
                                                                            (t)) + δij
                                                                                    ′
                                                                                       (fij
                                                                                         ∗
                                                                                            (t))
                                      q                                                 q                                       (27)
                                     = ηj (t)fij  ∗ (t)(r̂ + ϵη (q, f, t))δ (1) +            ∗ (t)δ ′ (1)
                                                                                           fij
                                                          ij     ij            ij                  ij

which gives us similar conclusions. (Some calculations are in the Appendix.)
Finding criteria for selecting the words that are included in the frequency change analysis greatly reduces the
computational complexity compared to trying different word combinations. If all combinations of n words
are tried, that complexity rises to O(2n ). When we use word choice criteria to select several groups of words,
the complexity is reduced to O(1). Our analysis of noise models gives some insights into these criteria, such
as qij
    d
       and r̂ij .

4.4   Calibration and test

In order to verify the theoretical and practical validity of our approach, we used calibrations and tests, with
ChatGPT-processed abstracts mixed with real abstracts. Considering that the noise in real data is likely
highly complex, we did not estimate the variance of ϵij (·). Instead, we used ChatGPT to process additional

                                                                           7

abstracts (on top of those used to estimate rij ), and used the resulting frequencies as calibration for the bias
and noise.
As previous analyses have demonstrated, with the goal of reducing bias in estimation, different selected words
are likely to correspond to the different (unknown) ground truth value of ηj (t). Therefore, we construct
N different sets of abstract data for calibration and test, Dn and Tn′ , with its correspond mixed ratio of
ChatGPT-processed abstracts, ηn and ηn′ ′ , as

                           (Dn , ηn ), n ∈ {1, 2, . . . , N };       (Tn′ , ηn′ ), n′ ∈ {1, 2, . . . , N ′ }.        (28)

                                                                                                                r̂ij + 1
And for one pair of (Dn , ηn ) and a specific word choice requirement qk (for example, qij
                                                                                        d
                                                                                           > 0.1 and                 2   <
                                                                                                                   r̂ij
0.1 + 1
        ), the efficiency can be defined as
 0.12
                                           e(Dn , ηn , qk ) = |ηn − η̂n (Dn , qk )|                                  (29)

where η̂n (Dn , qk ) is the estimate of ηn using Eq. (18) and the words set Ij can be derived from qk , denoted
Ij (qk ).
For a given set of qk (examples can be found in the Appendix), we are looking for the best one minimizing
e(Dn , ηn , qk ), denoted q(Dn , ηn ), which is the calibration part. For the test data Tn′ , the estimate of ηn′ is
calculated from Eq. (18) with different Ij , based on different q(Dn , ηn ) obtained in the calibration procedure.
Because of the goal of the calibration, word choice may well actually introduce a new bias to neutralize the
original bias, so that the estimate is not necessarily higher in the test results than the ground truth.

5     Results

5.1   Calibration and test results

To calibrate the choice of set Ij , we use different mixing ratios, in proportion to the value of ηj (t). In addition,
we only consider the 10,000 words with the highest frequency in the Google Ngram dataset.
We continue our simulations based on GPT-3.5. As the training data for GPT-3.5 is up to September 2021,
abstracts submitted later than this time are considered: 20,000 abstracts in period 13 to estimate rij , 10,000
abstracts in period 12 for calibration, and 10,000 abstracts in period 14 for testing.
We used the first 10 periods before ChatGPT was introduced, to estimate fij
                                                                         ∗
                                                                            (t), as they weren’t influenced
by ChatGPT, which means T0 = 10 and #{t ≤ T0 } = 10 in Eq. (4).
We take {ηn } = {0, 0.05, 0.1, . . . , 0.45, 0.5} and m = 1, which means N = #{(Dn , ηn )} = 11. Then the 11 Ij
(with possible repetitions), obtained from mixed data with 11 corresponding ηn of period 12, were used for
ηn′ estimation in the test data (period 14). Other parameters can be found in the Appendix.
The results using the same prompt for generating calibration and test data are shown in Figure 2a, with
injected mixed ratio (i.e., ChatGPT impact) ηn′ from 0 to 0.5. It is clear that when the calibration and test
sets are mixed in the same ratio, word combinations that achieve better estimates on the calibration set
generally work better on the test set, as well.
Unlike in Figure 2a where we normalized the word frequency by the total number of abstracts, we normalized
it by the total number of words for one period in Figure 2b. The trends remain similar, albeit different in
detail.
Because one may use a wide variety of prompts in practical applications, we also evaluated the robustness of
our approach by adopting a different prompt for generating the test data than the one we used for calibration.
The corresponding results in Figure 2c use the following prompt:

                       "Please rewrite the following paragraph from an academic paper:"

                                                                 8

(a) Normalized to the total number     (b) Normalized to the total number     (c) Different prompt for test data
of abstracts.                          of words.                              than used in calibration data.

Figure 2: Test results for simulated admixtures of abstracts in period 14. The error bars represent the
standard deviation of the estimation results, and the red star is the estimated value of ηn′ from test data based
on optimal Ij with the same mixed ratio ηn as in the calibration data. The orange dashed lines correspond
to perfect estimation.

In this example, we add the word “please” and make it clear that this comes from an “academic paper”,
replacing “revise” with “rewrite”. Although the quantitative results of our tests were not as good as before,
the errors were still small at lower mixed ratios, which also illustrates the robustness of our method. This is
understandable because in data generated with different prompts, not all of our previous assumptions hold,
and the estimate of r̂ij on rij in our model may be biased. We can also note that most of our estimates in
Figure 2c are on the high side relative to the ground truth, most likely because we use a more precise prompt
for the test data here, making the frequency change rate of the relevant words higher.

5.2   Estimation from real data

The estimates of ChatGPT impact on the real data are shown in Figure 3a and Figure 3b.

   (a) Normalized to the total number of abstracts.            (b) Normalized to the total number of words.

Figure 3: Estimates of ηj (t) (i.e., ChatGPT impact) from real data. Word frequencies were normalized on the
number of abstracts in each period before the estimation was performed. The error bars represent the standard
deviation of the estimation results, using 11 different word sets Ij obtained in the calibration procedure with
11 different ηn . The points of the triangle represent the average of the 3 estimates, corresponding to the 3
word selection requirements q based on the 3 ηn closest to the mean of the previous 11 estimates.

                                                       9

Based on our calibration results, we chose 11 words set Ij for different injected values of ηn . According to the
results of the first estimation about ηj (t), we found the three values of ηn that were closest to the mean of
the first estimation and used their optimal word set Ij in the calibration procedure for a second estimation,
leading to the triangle points shown in the figures.
Despite mild differences in the estimates under the two different normalizations, the conclusions are essentially
the same. Our estimates on ηj (t) hover around 0 until 2023, which gives reassurance of the reliability of
our methodology. More and more abstracts are being influenced by ChatGPT, especially in the cs category,
starting from December 2022, after the release of ChatGPT.
Our estimate indicates that the density of ChatGPT style texts of the most recent time period in this category
is around 35%, when we use the results of one simple prompt, “revise the following sentences”, as a baseline.
By contrast, we detected a much smaller uptick in ChatGPT impact in math, while astro and cond-mat both
reach values between 10% and 20%, approximately.
It is important to note that our ChatGPT impact or LLM impact here is a relative value that corresponds to
the change in word frequency from the use of simple prompts. More precise prompts, both in reality and in
simulation, could potentially lead to an impact value greater than 1.

6   Conclusions

Is ChatGPT transforming academics’ writing style? An important question before these discussions is the
evaluation of the actual penetration of the usage of ChatGPT in academic writing – without a quantitative
estimate, the debate is founded on anecdotal evidence.
We have demonstrated here that we can monitor the impact of LLMs in arXiv abstracts by using simple and
transparent statistical methods (e.g., word frequencies), which is easily extendable to other subjects and to
the complete text of articles.
Some formulas above look complicated, but with the help of the calibration, the final estimates are linear
regressions, i.e., Eq. (18). And those formulas and proofs tell us which words should be theoretically selected
for estimation, which to our knowledge other articles haven’t done. In addition, we also propose adaptive
word selection methods that are operationally simple.
Our estimates are founded on a population level and based on the output of simple prompts. Using more
precise prompts, it is entirely possible to achieve abstracts that are more ChatGPT-like (or LLM-like) texts
than our simulations. In addition, in the real world people might use LLMs other than ChatGPT to revise
articles, which may have similar but not identical word preferences to ChatGPT.
We found convincing evidence of a change in word frequency after ChatGPT’s release, consistent with
predictions obtained from simulating LLM impact from possible users’ prompts. The most enthusiastic
community (among the four we investigated) in terms of LLM adoption appears to be that of computer
scientists, a result that is perhaps unsurprising. Mathematicians, by contrast, are the least keen.
Our paper illustrates the importance of words chosen. Different types of articles with different LLM impact
need to be estimated using the corresponding words, which we proved theoretically under certain assumptions
and verified with simulated data. Not only did we focus on words that were increasing in frequency, but we
also took words that were decreasing in frequency, which are not covered in other papers.

7   Discussion

The debate around the usage of generative models such as ChatGPT in academic writing is multi-faceted:
from fears of lowering rigour due to “hallucinations” to uncertainty about the actual sources of AI-produced
text. It is however indisputable that LLM tools such as ChatGPT also have positive impacts: they help
non-English native writers to improve the quality and flow of their text, as well as to translate into English
from their mother tongue or vice versa. In this sense, generative AI is a great leveller, and as such it is a

                                                       10

welcome addition to the academic’s toolbox. What we need to be wary of is its use in fully generative mode,
without expert human supervision – something that we have not addressed in this paper.
We are aware that our methods can be further improved. For example, our results follow from analyzing a set
of words selected based on the value of qij
                                         d
                                            and r̂ij . It is actually possible to fine-tune this criterium for a more
accurate word selection, which would theoretically give better results, but would be more computationally
expensive. Similarly, trying a larger range of prompts should theoretically result in better estimates. And
better estimates may be made by more rigorous analysis, such as considering more complex noise terms. We
are more interested in the density of LLM-style texts and its relative value (comparisons between categories
and over time) than in establishing how many people are using LLMs – this can be estimated with the help
of questionnaires, and it is not possible to get an accurate estimate only based on simulated data.
As our results have shown, that LLMs, started by ChatGPT, are having an increasing impact on academic
publications. This trend is hard to avoid, and we need to adapt gradually. With the increasing influx of young
researchers, especially non-native English speakers, LLM tools represented by ChatGPT, are transforming
academic writing, at least for some disciplines. Even if you refuse to use them, you are likely to be influenced
indirectly.

References
Microsoft Research AI4Science and Microsoft Azure Quantum. The impact of large language models on
 scientific discovery: a preliminary study using gpt-4. arXiv preprint arXiv:2311.07361, 2023.

Mohammad Awad AlAfnan and Siti Fatimah MohdZuki. Do artificial intelligence chatbots have a writing
 style? an investigation into the stylistic features of chatgpt-4. Journal of Artificial intelligence and
 technology, 3(3):85–94, 2023.

Tatsuya Amano, Valeria Ramírez-Castañeda, Violeta Berdejo-Espinola, Israel Borokini, Shawan Chowdhury,
  Marina Golivets, Juan David González-Trujillo, Flavia Montaño-Centellas, Kumar Paudel, Rachel Louise
  White, et al. The manifold costs of being a non-native english speaker in science. PLoS Biology, 21(7):
  e3002184, 2023.

arXiv.org submitters. arxiv dataset, 2024. URL https://www.kaggle.com/dsv/7352739.

Anton Bakhtin, Sam Gross, Myle Ott, Yuntian Deng, Marc’Aurelio Ranzato, and Arthur Szlam. Real or
 fake? learning to discriminate machine from human generated text. arXiv preprint arXiv:1906.03351, 2019.

J Elliott Casal and Matthew Kessler. Can linguists distinguish between chatgpt/ai and human writing?: A
  study of research ethics and academic publishing. Research Methods in Applied Linguistics, 2(3):100068,
  2023.

Shu-Li Cheng, Shih-Jen Tsai, Ya-Mei Bai, Chih-Hung Ko, Chih-Wei Hsu, Fu-Chi Yang, Chia-Kuang Tsai,
  Yu-Kang Tu, Szu-Nian Yang, Ping-Tao Tseng, et al. Comparisons of quality, correctness, and similarity
  between chatgpt-generated and human-written abstracts for basic research: Cross-sectional study. Journal
  of Medical Internet Research, 25:e51229, 2023.

Suzanne Fergus, Michelle Botha, and Mehrnoosh Ostovar. Evaluating academic answers generated using
  chatgpt. Journal of Chemical Education, 100(4):1672–1675, 2023.

Tira Nur Fitria. Grammarly as ai-powered english writing assistant: Students’ alternative for writing english.
  Metathesis: Journal of English Language, Literature, and Teaching, 5(1):65–78, 2021.

Catherine A Gao, Frederick M Howard, Nikolay S Markov, Emma C Dyer, Siddhi Ramesh, Yuan Luo, and
 Alexander T Pearson. Comparing scientific abstracts generated by chatgpt to real abstracts with detectors
  and blinded human reviewers. NPJ Digital Medicine, 6(1):75, 2023.

Sebastian Gehrmann, Hendrik Strobelt, and Alexander M Rush. Gltr: Statistical detection and visualization
  of generated text. arXiv preprint arXiv:1906.04043, 2019.

                                                         11

Biyang Guo, Xin Zhang, Ziyuan Wang, Minqi Jiang, Jinran Nie, Yuxuan Ding, Jianwei Yue, and Yupeng Wu.
  How close is chatgpt to human experts? comparison corpus, evaluation, and detection. arXiv preprint
  arXiv:2301.07597, 2023.

Sung Il Hwang, Joon Seo Lim, Ro Woon Lee, Yusuke Matsui, Toshihiro Iguchi, Takao Hiraki, and Hyungwoo
  Ahn. Is chatgpt a “fire of prometheus” for non-native english-speaking researchers in academic writing?
  Korean Journal of Radiology, 24(10):952, 2023.

Jimoon Kang, June Seop Yoon, and Byungjoo Lee. How ai-based training affected the performance of
  professional go players. In Proceedings of the 2022 CHI Conference on Human Factors in Computing
  Systems, pp. 1–12, 2022.

Enkelejda Kasneci, Kathrin Seßler, Stefan Küchemann, Maria Bannert, Daryna Dementieva, Frank Fischer,
  Urs Gasser, Georg Groh, Stephan Günnemann, Eyke Hüllermeier, et al. Chatgpt for good? on opportunities
  and challenges of large language models for education. Learning and individual differences, 103:102274,
  2023.

John Kirchenbauer, Jonas Geiping, Yuxin Wen, Jonathan Katz, Ian Miers, and Tom Goldstein. A watermark
  for large language models. In International Conference on Machine Learning, pp. 17061–17084. PMLR,
  2023.

Kalpesh Krishna, Yixiao Song, Marzena Karpinska, John Wieting, and Mohit Iyyer. Paraphrasing evades
 detectors of ai-generated text, but retrieval is an effective defense. Advances in Neural Information
 Processing Systems, 36, 2024.

Weixin Liang, Zachary Izzo, Yaohui Zhang, Haley Lepp, Hancheng Cao, Xuandong Zhao, Lingjiao Chen,
 Haotian Ye, Sheng Liu, Zhi Huang, et al. Monitoring ai-modified content at scale: A case study on the
 impact of chatgpt on ai conference peer reviews. arXiv preprint arXiv:2403.07183, 2024a.

Weixin Liang, Yaohui Zhang, Zhengxuan Wu, Haley Lepp, Wenlong Ji, Xuandong Zhao, Hancheng Cao,
 Sheng Liu, Siyu He, Zhi Huang, et al. Mapping the increasing use of llms in scientific papers. arXiv
 preprint arXiv:2404.01268, 2024b.

Lorelei Lingard, Madawa Chandritilake, Merel de Heer, Jennifer Klasen, Fury Maulina, Francisco Olmos-Vega,
  and Christina St-Onge. Will chatgpt’s free language editing service level the playing field in science
  communication?: Insights from a collaborative project with non-native english scholars. Perspectives on
  Medical Education, 12(1):565, 2023.

Brady D Lund, Ting Wang, Nishith Reddy Mannuru, Bing Nie, Somipam Shimray, and Ziang Wang. Chatgpt
  and a new academic reality: Artificial intelligence-written research papers and the ethics of the large
  language models in scholarly publishing. Journal of the Association for Information Science and Technology,
  74(5):570–581, 2023.

Zheheng Luo, Qianqian Xie, and Sophia Ananiadou. Chatgpt as a factual inconsistency evaluator for
  abstractive text summarization. arXiv preprint arXiv:2303.15621, 2023.

Jean-Baptiste Michel, Yuan Kui Shen, Aviva Presser Aiden, Adrian Veres, Matthew K Gray, Google Books
  Team, Joseph P Pickett, Dale Hoiberg, Dan Clancy, Peter Norvig, et al. Quantitative analysis of culture
  using millions of digitized books. science, 331(6014):176–182, 2011.

Eric Mitchell, Yoonho Lee, Alexander Khazatsky, Christopher D Manning, and Chelsea Finn. Detectgpt:
  Zero-shot machine-generated text detection using probability curvature. In International Conference on
  Machine Learning, pp. 24950–24962. PMLR, 2023.

Klaus Mundt and Michael Groves. A double-edged sword: the merits and the policy implications of google
  translate in higher education. European Journal of Higher Education, 6(4):387–401, 2016.

Shakked Noy and Whitney Zhang. Experimental evidence on the productivity effects of generative artificial
  intelligence. Science, 381(6654):187–192, 2023.

                                                     12

Vinu Sankar Sadasivan, Aounon Kumar, Sriram Balasubramanian, Wenxiao Wang, and Soheil Feizi. Can
  ai-generated text be reliably detected? arXiv preprint arXiv:2303.11156, 2023.
David Silver, Julian Schrittwieser, Karen Simonyan, Ioannis Antonoglou, Aja Huang, Arthur Guez, Thomas
  Hubert, Lucas Baker, Matthew Lai, Adrian Bolton, et al. Mastering the game of go without human
  knowledge. nature, 550(7676):354–359, 2017.
William H Walters and Esther Isabelle Wilder. Fabrication and errors in the bibliographic citations generated
 by chatgpt. Scientific Reports, 13(1):14045, 2023.
Qihui Zhang, Chujie Gao, Dongping Chen, Yue Huang, Yixin Huang, Zhenyang Sun, Shilin Zhang, Weiye Li,
  Zhengyan Fu, Yao Wan, et al. Llm-as-a-coauthor: Can mixed human-written and machine-generated text
  be detected? In Findings of the Association for Computational Linguistics: NAACL 2024, pp. 409–436,
  2024.

                                                     13

A    Period divisions

                         Table 2: First and last arXiv paper identifier of 20 periods.

                                      period       first paper      last paper
                                      1           1805.08929        1810.00786
                                      2           1810.00787        1902.00889
                                      3           1902.00890        1905.13537
                                      4           1905.13538        1909.11935
                                      5           1909.11936        2001.06560
                                      6           2001.06561        2005.02178
                                      7           2005.02179        2008.04251
                                      8           2008.04252        2011.09225
                                      9           2011.09226        2103.01828
                                      10          2103.01829        2106.04209
                                      11          2106.04210        2109.09152
                                      12          2109.09153        2112.12197
                                      13          2112.12198        2204.01835
                                      14          2204.01836        2207.06075
                                      15          2207.06076        2210.10618
                                      16          2210.10619        2301.10909
                                      17          2301.10910        2304.13927
                                      18          2304.13928        2307.10978
                                      19          2307.10979        2310.09716
                                      20          2310.09717        2401.02417

B    arXiv categories

Formally, arXiv has 8 categories in total: physics, mathematics, computer science, quantitative biology,
quantitative finance, statistics, electrical engineering and systems science, economics. The first 3 categories
contribute the vast majority of arXiv articles, around 91% among the 1 million articles. Hence, we divided
the physics papers into sub-categories: astrophysics, condensed matter, high energy physics, etc. The four
categories (computer science, mathematics, astrophysics, condensed matter) we selected account for 70% of
the total number of articles. To avoid repetition, we also only count the first category of the article for those
that have multiple categories (cross-postings).

C    Other observations

We define the change factor in the frequency of word i, Ri , as follows:

                                                maxt (fi (t)) − mint (fi (t))
                                        Ri =                                                                   (30)
                                                       maxt (fi (t))

where fi (t) is the count of word i during the time period t.
Similarly, we define a change factor in the frequency of word i, Ri ′ :

                                                maxt (fi ′ (t)) − mint (fi ′ (t))
                                       Ri ′ =                                                                  (31)
                                                       maxt (fi ′ (t))

where fi ′ (t) is the count of word i in period t, normalized to the same value of   i fi (t) for all periods t.
                                                                                     P

                                                           14

Figure 4a and Figure 4b illustrate that most of the words with the largest change rate in the time period
considered (generally, an increase) in the abstracts are related to hot research topics of the last few years,
such as “Covid-19”, “LLMs”, “AI”.

(a) The 12 words with the highest change rate Ri and        (b) The 12 words with the highest change rate Ri ′ and
satisfying maxt (fi (t)) > 500.                             satisfying maxt (fi ′ (t)) > 500.

                         Figure 4: Words with the highest change rate in frequency

The total number of words in all abstracts of the first period is used as a base to normalize the frequency of
words in the other periods, and the corresponding results are shown Figure 5.

               Figure 5: Word frequency changes (with different normalization) in abstracts.

D    Correlation between simulated and real data

We also defined the word frequency change in all abstracts from year t − 1 to year t, Rij,t :
                                                     Fij,t − Fij,t−1
                                           Rij,t =                   ,                                        (32)
                                                         Fij,t−1
where Fij,t represent frequency of word i per arXiv abstract in category j in year t.

                                                       15

Only words with a frequency larger than 0.1 times per abstract before ChatGPT processing are plotted in
Figure 6a and Figure 6b. The correlation coefficient between the word frequency change in arXiv abstracts
and our estimated ChatGPT-induced word frequency change is very small in all four categories of abstracts,
as shown in Figure 6a.

                  (a) From 2021 to 2022.                                            (b) From 2022 to 2023.

Figure 6: Comparison of the predicted frequency change rate due to ChatGPT r̂ij (x-axis) and the actual
word frequency change for all abstracts (y-axis). CC indicates the correlation coefficient.

However, Figure 6b presents a totally different pattern, where r̂ij and Rij,2023 are strongly correlated,
especially in computer science abstracts. Although many words seem insensitive to ChatGPT, we can still
see a positive correlation for some words in this figure, even among the other categories.

E     Parameters

E.1    ChatGPT simulations
      • model: gpt-3.5-turbo-1106
      • temperature: 0.7
      • seed: 1106
      • top_p: 0.2

E.2   Calibration
         1
      • d : 10, 20, 30, 40, 50, 60, 70, 80, 100, 150, 200, 500
        qij
                                                                                           r̂ij + 1
      • r̂ij : 0.1, 0.15, 0.2, 0,3, 0.4, 0.5, 0.6, 0.7, 0.8 (corresponding value of             2   )
                                                                                              r̂ij

                                 1               r̂ij + 1    0.1 + 1
For example, when we take            < 10 and             <            for abstracts in computer science, the words that
                                  d
                                qij                   2
                                                    r̂ij       0.12
 satisfy the conditions are: ’the’, ’is’, ’for’, ’by’, ’be’, ’this’, ’are’, ’i’, ’at’, ’which’, ’an’, ’have’, ’but’, ’we’, ’all’,
’they’, ’one’, ’has’, ’their’, ’other’, ’there’, ’more’, ’new’, ’any’, ’these’, ’time’, ’than’, ’some’, ’only’, ’two’,
’into’, ’them’, ’our’, ’under’, ’first’, ’most’, ’then’, ’over’, ’work’, ’where’, ’many’, ’through’, ’well’, ’how’, ’even’,
’while’, ’however’, ’high’, ’given’, ’present’, ’large’, ’research’, ’different’, ’set’, ’study’, ’important’, ’several’,
’e’, ’further’, ’including’, ’often’, ’provide’, ’due’, ’using’, ’better’, ’various’, ’problem’, ’show’, ’problems’,

                                                               16

’design’, ’proposed’, ’g’, ’across’, ’approach’, ’existing’, ’compared’, ’task’, ’learn’, ’improve’, ’achieve’, ’novel’,
’domain’, ’demonstrate’, ’introduce’, ’propose’, ’prediction’.
               1               r̂ij + 1     0.8 + 1
And when          < 50 and               <           , the words are: ’i’, ’would’, ’so’, ’some’, ’what’, ’out’, ’work’,
               d
              qij                   2
                                  r̂ij        0.82
’very’, ’because’, ’much’, ’good’, ’way’, ’great’, ’here’, ’since’, ’might’, ’last’, ’end’, ’means’, ’having’, ’thus’,
’above’, ’give’, ’e’, ’further’, ’far’, ’find’, ’although’, ’show’, ’n’, ’help’, ’together’, ’particular’, ’whose’, ’issue’,
’according’, ’addition’, ’usually’, ’art’, ’especially’, ’respect’, ’works’, ’shows’, ’g’, ’makes’, ’hard’, ’significant’,
’run’, ’address’, ’particularly’, ’idea’, ’consider’, ’includes’, ’built’, ’adopted’, ’obtain’, ’establish’, ’useful’,
’leading’, ’performed’, ’create’, ’named’, ’conducted’, ’resulting’, ’hence’, ’findings’, ’towards’, ’prove’, ’build’,
’perform’, ’moreover’, ’describe’, ’besides’, ’demonstrated’, ’via’, ’presents’, ’mainly’, ’fail’, ’namely’, ’allowing’,
’demonstrate’, ’advances’, ’suffer’, ’overcome’, ’introduce’, ’accurately’, ’identifying’, ’enhance’, ’crucial’, ’etc’,
’utilize’, ’demonstrates’, ’additionally’, ’focuses’, ’motivated’, ’characterize’.

F     Noise analysis

F.1    Variance in real data

Abstracts in the cs category among the first 500,000 articles were divided into groups in chronological order,
with the same number in each group. We counted the number of occurrences of each word within each group,
and calculated the variance between the different groups. This was repeated as a function of the number of
abstracts included in each group, and the results are shown in Figure 7a.

            (a) Variance of the word counts.                                    (b) Coefficient of variation.

                                 Figure 7: Variance of the 12 most frequent words.

Then we also analyzed the coefficient of variation (defined as the standard deviation of the sum divided by
the mean of the sum) for the 12 most frequent words, as shown in Figure 7b, and the variance-to-mean ratio
(defined as the variance of the sum of a word’s counts divided by the mean of the sum), as shown in Figure 8.
We observe that, at least for a subset of the words considered here, the variance-to-mean ratios are essentially
on the same scale (although there are words that do not follow this pattern). Therefore, a simple Gaussian
distribution
                                                δij (fij ) ∼ N (0, fij σij
                                                                        2
                                                                           ).                                          (33)

which corresponds to case 2, seems to be a reasonable approximation.

                                                            17

                                                Figure 8: Variance-to-mean ratio

F.2   Calculation details

Case 1: Therefore, all terms on the right-hand side of Eq. (23) are zero-mean noise, except for the last one:

                             ∂gij (t)            ∗
                                                fij (t)(ηj (t)fij
                                                               ∗
                                                                  (t) + 2δij (∗))ϵij (1)            ∗ s
                                                                                                   fij ϵ (1)
                   gij (t)            = gij (t)                                          − gij (t)   qij     .                  (34)
                             ∂ηj (t)                                             3
                                                      2(ηj (t)fij (t) + δij (∗)) 2
                                                                ∗
                                                                                                        qd                 ij

Removing the items with zero means, we get

                        ∂gij (t)     ηj (t)(fij
                                             ∗
                                                (t))2 (ηj (t)fij
                                                              ∗
                                                                 (t) + 2δij (∗))σij,ϵ
                                                                                 2
                                                                                        ηj (t)(fij
                                                                                                ∗
                                                                                                   (t))2 σij,ϵ
                                                                                                          2
                                
              E gij (t)            =                                                  +                        .                (35)
                        ∂ηj (t)                2(ηj (t)fij (t) + δij (∗))
                                                          ∗               2                        d
                                                                                                 qij

Case 2:    We can define gij
                          c
                             (t) and ξij
                                      c
                                         (t):
                                                                        q
                         c
                        gij (t) =ηj (t)fij
                                         ∗
                                           (t)ϵηij (q, f, t) +                  ∗ (t)(r̂ + ϵη (q, f, t))δ (1)
                                                                         ηj (t)fij      ij  ij           ij                     (36)
                                 q
                         c
                        ξij (t) = fij ∗ (t)δ ′ (1)
                                            ij                                                                                  (37)

As ξij
    c
       (t) doesn’t depend on ηj (t), the loss function under this assumption is:

                                         1 X                                        1 X c
                       Lcj,t,g (ηj ) =       (hij (t) − ηj (t)xij (t) − gij
                                                                         c
                                                                            (t))2 =    (ξij (t))2 .                             (38)
                                         nj                                         nj
                                            i∈Ij                                                            i∈Ij

And we will get a complex expression for the bias part like Eq. (23).
                       ∂Lcj,t,g (ηj )
As in case 1, we set       ∂ηj        = 0 to obtain the new estimate η̂jg (t) corrected for bias and noise,

                                                X                       c
                                                                    X ∂gij (t)
                         (η̂jg (t) − η̂j (t))          x2ij (t) =                     (hij (t) − ηj (t)xij (t))
                                                                           ∂ηj (t)
                                                i∈Ij                i∈Ij
                                                                                                                                (39)
                                                                        X                          X                  c
                                                                                                                    ∂gij (t)
                                                                    −           xij (t)gij
                                                                                        c
                                                                                           (t) −           c
                                                                                                          gij (t)
                                                                                                                    ∂ηj (t)
                                                                        i∈Ij                       i∈Ij

                                                                           18

where
                                                                                       q
                                                                                   ∗ (t)
                                                                                  fij
                  c
                ∂gij (t)                                       ∂ϵηij (q, f, t)
                                    η
                           =fij (t)ϵij (q, f, t) + ηj (t)fij
                             ∗                              ∗
                                                                               + p       (r̂ij + ϵηij (q, f, t))δij (1)
                ∂ηj (t)                                           ∂ηj (t)       2 ηj (t)                                  (40)
                                q                ∂ϵηij (q, f, t)
                            + ηj (t)fij (t)∗                     δij (1) .
                                                    ∂ηj (t)

The bias part is also expressed as
                                                                                        ∂g c (t)
                                                                                h                  i
                                                                  i∈Ij E             (t) ∂ηijj (t)
                                                                                  c
                                                                  P
                                                                                 gij
                                           η̂j (t) − η̂jg (t) =                                        .                  (41)
                                                                           i∈Ij (fij (t)r̂ij )
                                                                                  ∗
                                                                      P                        2

Also with the same assumptions for ϵij (·) and ϵsij (·), ϵij (fij ) ∼ N (0, fij σij,ϵ
                                                                                 2
                                                                                      ) and ϵsij (fij ) ∼ N (0, fij σij,ϵ
                                                                                                                     2
                                                                                                                          ).
                                      η
then we can obtain an expression for ϵij (q, f, t),

                                                                ϵij (1)                  ϵsij (1)
                                ϵηij (q, f, t) = r                                     − q                                (42)
                                                                                               d
                                                                  q
                                                  ηj (t)fij
                                                         ∗ (t) +     ηj (t)fij
                                                                            ∗ (t)δ (1)
                                                                                  ij
                                                                                              qij

and its derivative,                                                     q              
                                                   − 2fij∗
                                                           (t) ηj (t) + fij ∗ (t)δ (1) ϵ (1)
                                                              p
                              ∂ϵηij (q, f, t)                                     ij        ij
                                                =                                              3 .                       (43)
                                 ∂ηj (t)                                 q
                                                                                    ∗ (t)δ (1) 2
                                                  4 ηj (t) ηj (t)fij
                                                                  ∗ (t) +   ηj (t)fij
                                                   p
                                                                                          ij

Combining the above equations, we can get similar conclusions as in case 1.

                                                                      19
