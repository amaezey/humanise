# Human-LLM Coevolution: Evidence from Academic Writing

- **Source URL:** https://aclanthology.org/2025.findings-acl.657.pdf
- **Snapshot method:** ACL PDF text extraction
- **Retrieved:** 2026-05-05

## Article Body

Human-LLM Coevolution: Evidence from Academic Writing

                                Mingmeng Geng1,2,3 Roberto Trotta1,4
1
    International School for Advanced Studies (SISSA) 2 École normale supérieure - Université PSL
                           3
                             Laboratoire LATTICE 4 Imperial College London
                                      mingmeng.geng@ens.psl.eu

                          Abstract
         With a statistical analysis of arXiv paper ab-
         stracts, we report a marked drop in the fre-
         quency of several words previously identified
         as overused by ChatGPT, such as “delve”, start-
         ing soon after they were pointed out in early
         2024. The frequency of certain other words
         favored by ChatGPT, such as “significant”, has
         instead kept increasing. These phenomena
         suggest that some authors of academic papers
         have adapted their use of large language mod-
         els (LLMs), for example, by selecting outputs
         or applying modifications to the LLM outputs.
                                                                 Figure 1: The frequency evolution of some words in
         Such coevolution and cooperation of humans
                                                                 arXiv abstracts (they were singled out around April
         and LLMs thus introduce additional challenges
                                                                 2024 as either favored or disfavored by ChatGPT).
         to the detection of machine-generated text in
         real-world scenarios. Estimating the impact of          but the performance of detectors has also been
         LLMs on academic writing by examining word              questioned early on (Sadasivan et al., 2023; Weber-
         frequency remains feasible, and more attention          Wulff et al., 2023; Ghosal et al., 2023). Recent
         should be paid to words that were already fre-
                                                                 studies continue to show that some methods are not
         quently employed, including those that have
         decreased in frequency due to LLMs’ disfavor.           sufficiently robust (Zhang et al., 2024b; Wang et al.,
         The coevolution between humans and LLMs                 2024; Creo and Pudasaini, 2025). The effective-
         also merits further study.                              ness of MGT detectors is also related to the model
                                                                 of LLMs and the type of text (Liu et al., 2024), and
     1   Introduction                                            their accuracy may also be exaggerated (Dough-
     After the launch of ChatGPT, large language mod-            man et al., 2024). The situations likely to arise in
     els (LLMs) began to be widely used and are now              reality are more complicated and are not limited
     transforming many aspects of our work and life,             to a binary classification framework (Zhang et al.,
     with academic writing being one of them. The                2024a). Thus, examining and analyzing the ongo-
     coevolution of AI and humans has also been recog-           ing evolution of word usage remains a useful and
     nized by researchers (Pedreschi et al., 2024).              meaningful task.
        For example, empirical studies from April 2024              Figure 1 illustrates the evolution in frequency
     observed that the frequency of certain words used           usage of some of the words that were singled out
     in academic papers published in 2023 had changed            as favored or disfavored by ChatGPT around April
     and confirmed a strong correlation between these            2024. The frequency of “significant” and “addition-
     changes and the use of LLMs (Liang et al., 2024b;           ally” continues to grow, while that of “is” and “are”
     Geng and Trotta, 2024). Survey results also show            continues its declining trend, as noted by Geng and
     that many researchers are utilizing LLMs in their           Trotta (2024). Meanwhile, the frequency of some
     work (Liao et al., 2024).                                   other words (e.g., “intricate” and “delve”) associ-
        The detection of machine-generated text (MGT)            ated with LLMs begins to decrease after March and
     has also attracted a lot of attention (Tang et al.,         April 2024, which corresponds to the time when
     2024; Chowdhury et al., 2024; Wang et al., 2025),           researchers identified these words in AI conference
                                                           12689
                    Findings of the Association for Computational Linguistics: ACL 2025, pages 12689–12696
                           July 27 - August 1, 2025 ©2025 Association for Computational Linguistics

                        (a)                                                           (b)

                        (c)                                                           (d)

Figure 2: Frequency of words in arXiv abstracts previously identified as indicative of LLM usage. All word
frequencies are normalized based on 10,000 abstracts. In figure 2c, word groups a and b correspond to the average
frequencies of the words in 2a and 2b.

peer reviews (Liang et al., 2024a) and academic           2       Data
papers (Liang et al., 2024b).
                                                          arXiv paper metadata Metadata of arXiv pa-
   Changes in the words used in academic writing,
                                                          pers updated weekly on Kaggle1 . Our paper used
as discussed above, serve as an excellent example
                                                          version 214 of this dataset. Between January 2018
of AI and human coevolution. Researchers are
                                                          and December 2024, the total number of papers
constantly proposing new detection techniques, but
                                                          submitted to arXiv is 1,294,653. On a monthly
the language and expressions of LLM users are also
                                                          statistical basis, the lowest and highest numbers of
likely to evolve due to their use of LLMs (Geng
                                                          papers were recorded in February 2018 (10,593)
et al., 2024).
                                                          and October 2024 (24,226), respectively.
   Given the lack of a precise definition, LLM-
generated text might be undetectable in certain indi-     Withdrawn arXiv papers data WithdrarXiv
vidual instances. Therefore, statistically measuring      dataset (Rao et al., 2024), containing more than
the impact of LLMs on a large corpus of texts is a        14,000 arXiv withdrawn papers up to September
more practical option.                                    2024.
   This paper focuses on the following key points:
                                                          3       Word Frequency Analysis
   • The different fates of word frequencies after
     changes have been pointed out and scribed to         The analysis presented in Figure 2 is based on the
     LLMs usage.                                          abstracts of all arXiv papers submitted between
                                                          2018 and 2024. The frequency of words is calcu-
   • The challenges of MGT detectors.
                                                          lated on a monthly basis and normalized per 10,000
   • The long-term impact of LLMs in academic                 1
                                                              https://www.kaggle.com/datasets/
     writing.                                             Cornell-University/arxiv/data

                                                     12690

                        (a)                                                             (b)

                        (c)                                                             (d)

Figure 3: Frequency of words in arXiv abstracts previously identified as indicative of LLM usage. All word
frequencies are normalized based on 10,000 abstracts. The data for withdrawn papers represents a 12-month
rolling average, labeled by “w”. “cs” represents papers in the arXiv category of computer science, while “o”
represents papers from other categories. The labels “AI”, “CL”, and “CV” correspond to the subcategories “Artificial
Intelligence”, “Computation and Language”, and “Computer Vision and Pattern Recognition” within the “cs”
category on arXiv.

abstracts.                                                 searchers noticed such kind of words in March and
   Figure 2a shows the frequency of the 4 words            April and quickly changed their arXiv abstracts.
highlighted by Liang et al. (2024b) and Figure 2b          If new LLMs were the cause, the drop in word
presents the frequency of the 6 words emphasized           frequency would have been delayed.
by Liang et al. (2024a). The former paper analyzes            In addition, the frequency of words like “signifi-
academic papers, while the latter focuses on AI            cant”, specifically pointed out by Geng and Trotta
conference peer reviews, and the average frequency         (2024), continues to grow, as shown in Figure 2d.
of these words is shown in Figure 2c. The trend            This may be because these terms are relatively
is clear: starting from April 2024, the frequency          common and frequently used, their presence alone
of these well-known LLM-style words began to               would not easily lead one to suspect the text as the
decrease. Some other words show patterns of con-           product of LLMs. Besides, as presented in Table 1,
sistent growth or a rise followed by a decline, as         this article has attracted less attention than the for-
illustrated in Figure 8a of the Appendix.                  mer, for example, in terms of Google Scholar cita-
   A study published in December 2024 also ob-             tion counts. Therefore, fewer researchers should
served a decline in the use of certain words, such         have noticed the relationship between these words
as “delve”, in some selected arXiv papers (Leiter          and LLMs.
et al., 2024). While they suggested that this was             We compared the results with the abstracts of
likely due to the release of GPT-4o in May 2024,           the withdrawn papers, as illustrated in Figures 3a
we suggest that the main reason is that LLMs may           and 3b. Given the small number of withdrawn
have given these words a bad reputation. Many re-          papers, the 12-month rolling averages of their word
                                                      12691

                          (a)                                                        (b)
Figure 4: Comparing the ratio of word frequency between Computer Science abstracts and other disciplines. Only
words that appear at least 20 times on average per 10,000 abstracts are plotted.

frequency are used in the graphs. The frequency            word usage and diversity in LLM-generated con-
of some words, such as “intricate”, is higher in the       tent (Kobak et al., 2024; Reviriego et al., 2024; Guo
withdrawn papers, but the difference is not very           et al., 2024). Based on the above results, people are
large, as is also the case in Figures 8b, 8c and 8d        likely still using LLMs, but they may avoid some
of the Appendix.                                           words that are typical of LLM output. Therefore,
   We also categorized the abstracts into two groups       detecting LLM-generated content in real-world sce-
based on the first category of the papers: com-            narios may become more difficult.
puter science (cs) and others. Figure 3c shows that
the frequency of two words preferred by LLMs
                                                           4    Challenges in Machine-Generated Text
is higher in the cs category, but their frequency
                                                                Detection
in other categories is also increasing. The pattern        The first 1000 arXiv papers submitted each year
holds for different cs subcategories, as seen in Fig-      from 2018 to 2025 were utilized for this part of
ure 3d.                                                    the analysis. We also used the following two
   To better compare the changes in word fre-              simple prompts to examine the differences be-
quency, we define Rij (T1 , T2 ) (the ratio of word i      tween original arXiv abstracts and those revised
in the abstracts of category j between periods T1          by GPT-4o-mini (temperature = 1, top-p = 0.9):
                                       f (T1 )
and T2 ) as follows: Rij (T1 , T2 ) = fij
                                        ij (T2 )
                                                 , where       • (P1) Revise the following sentences: . . .
fij (T ) is the frequency of word i in the abstracts
of category j during the time period T .                       • (P2) Don’t use the following words in your re-
   Figure 4a represents the ratio R between 2023                 sponses: ’realm’, ’pivotal’, ’intricate’, ’show-
and 2022, where some words, like “diffusion”, are                casing’. Revise the following sentences: . . .
related to the research topics, but some other words          The results in Figure 5 reinforce the point
have also become much more common in differ-               that the frequency of certain words increases af-
ent fields. The ratio R in Figure 4b is calculated         ter LLMs revision. Using prompt P2, aimed at
using the word frequency in the first quarter of           suppressing them, reduces the frequency of such
2024 divided by the word frequency from January            words, although it does not completely eliminate
2023 to December 2024. Some words like “delve”             them.
and “showcasing” actually reached their peak us-              Figure 6 presents the detection results based on
age from January to March 2024, and such words             Binoculars (Hans et al., 2024), one of the state-
are very few. Figure 7 provides more detailed ex-          of-art MGT detectors, where a lower score indi-
amples. Words that appear more often in cs paper           cates a greater probability that the text is machine-
abstracts have also clearly increased in other disci-      generated. Unlike the results obtained with our
plines.                                                    frequency analysis, the outcomes of Binoculars de-
   More researchers have now noticed issues with           tector on average do not return any difference in
                                                      12692

       Figure 5: Comparison of word frequencies before and after LLM processing (with prompts P1 or P2).

    (a) The last 3 columns all include abstracts of 8 years.              (b) KDE means kernel density estimation.

Figure 6: MGT detection results for real and LLM-processing abstracts (with prompts P1 or P2). A lower score
indicates a greater probability that the text is machine-generated.

score for the real abstracts of papers as a function              lar to those of ChatGPT (Rudnicka, 2023), and the
of time. Moreover, the change in the detection                    mix of human-written text and machine-generated
score between the original abstracts and the texts                text should be very common in academic writing.
processed by LLMs (true positives) is not signifi-                Detecting LLM-generated content with accuracy is
cant. Furthermore, the prompts used for processing                becoming more difficult, perhaps impossible on a
can influence the results of MGT detectors. These                 text-by-text basis.
results raise doubts about the accuracy of the detec-
tors, given that they are analyzing texts that have                  Our findings suggest that some researchers may
been fully processed by LLMs.                                     intentionally avoid using LLM-characteristic terms,
                                                                  and they are not as sensitive to some relatively com-
5    Conclusion and Discussion                                    mon words. The gradual decrease in the occurrence
                                                                  of “is” and “are” in arXiv abstracts is an excellent
Humans and LLMs are coevolving and we can al-                     example of such a trend, which we ascribe to a
ready conclude that, for this reason, the impact                  more subtle – and continually increasing– LLM
of LLMs on academic writing will fully assert it-                 influence.
self over the long term. According to recent stud-
ies, people who frequently use ChatGPT for writ-                    Therefore, using the frequency of more common
ing tasks can accurately distinguish AI-generated                 words to measure the impact of LLMs on a vast
text (Russell et al., 2025), which implies that they              number of publications will be more reliable, al-
are also able to foil MGT detectors.                              though this approach is less suitable for the precise
   Grammarly can sometimes achieve effects simi-                  detection of short texts.
                                                               12693

Limitations                                                 Andrew Gray. 2024. Chatgpt" contamination": estimat-
                                                              ing the prevalence of llms in the scholarly literature.
Our target is a short paper, so certain sections can          arXiv preprint arXiv:2403.16887.
be expanded or made more detailed.
                                                            Yanzhu Guo, Guokan Shang, and Chloé Clavel. 2024.
   There are many MGT detection methods, and                  Benchmarking linguistic diversity of large language
some might perform better. The first part of our              models. arXiv preprint arXiv:2412.10271.
analysis is based on word frequencies, while con-
sidering higher-level linguistic patterns might po-         Abhimanyu Hans, Avi Schwarzschild, Valeriia
                                                              Cherepanova, Hamid Kazemi, Aniruddha Saha,
tentially give us more coevolutionary patterns. Ex-           Micah Goldblum, Jonas Geiping, and Tom Goldstein.
ploring other data sources may also bring some                2024. Spotting llms with binoculars: Zero-shot
new insights.                                                 detection of machine-generated text. arXiv preprint
   This paper focuses on identifying correlations             arXiv:2401.12070.
from observed data, while causality remains to be           Dmitry Kobak, Rita González-Márquez, Emőke-Ágnes
explored through methods like questionnaires.                Horvát, and Jan Lause. 2024. Delving into chatgpt
                                                             usage in academic writing through excess vocabulary.
Acknowledgments                                              arXiv preprint arXiv:2406.07016.

M.G. is supported by DM Dottorati Innovazione               Christoph Leiter, Jonas Belouadi, Yanran Chen, Ran
                                                              Zhang, Daniil Larionov, Aida Kostikova, and Steffen
e Green ex DM1061 Anno 2021 (DM 1061 del                      Eger. 2024. Nllg quarterly arxiv report 09/24: What
10/08/2021). R.T. acknowledges co-funding from                are the most influential current ai papers? arXiv
Next Generation EU, in the context of the National            preprint arXiv:2412.12121.
Recovery and Resilience Plan, Investment PE1 –
                                                            Weixin Liang, Zachary Izzo, Yaohui Zhang, Haley Lepp,
Project FAIR “Future Artificial Intelligence Re-              Hancheng Cao, Xuandong Zhao, Lingjiao Chen, Hao-
search”.                                                      tian Ye, Sheng Liu, Zhi Huang, et al. 2024a. Moni-
                                                              toring ai-modified content at scale: A case study on
                                                              the impact of chatgpt on ai conference peer reviews.
References                                                    arXiv preprint arXiv:2403.07183.

Shammur Absar Chowdhury, Hind Almerekhi, Muc-               Weixin Liang, Yaohui Zhang, Zhengxuan Wu, Haley
  ahid Kutlu, Kaan Efe Keles, Fatema Ahmad, Tas-             Lepp, Wenlong Ji, Xuandong Zhao, Hancheng Cao,
  nim Mohiuddin, George Mikros, and Firoj Alam.              Sheng Liu, Siyu He, Zhi Huang, et al. 2024b. Map-
  2024. Genai content detection task 2: Ai vs.               ping the increasing use of llms in scientific papers.
  human–academic essay authenticity challenge. arXiv         arXiv preprint arXiv:2404.01268.
  preprint arXiv:2412.18274.
                                                            Zhehui Liao, Maria Antoniak, Inyoung Cheong, Evie
Aldan Creo and Shushanta Pudasaini. 2025. Silvers-            Yu-Yen Cheng, Ai-Heng Lee, Kyle Lo, Joseph Chee
  peak: Evading ai-generated text detectors using ho-         Chang, and Amy X Zhang. 2024. Llms as research
  moglyphs. In Proceedings of the 1stWorkshop on              tools: A large scale survey of researchers’ usage and
  GenAI Content Detection (GenAIDetect), pages 1–             perceptions. arXiv preprint arXiv:2411.05025.
  46.
                                                            Jialin Liu and Yi Bu. 2024. Towards the relationship
Jad Doughman,         Osama Mohammed Afzal,                    between aigc in manuscript writing and author pro-
  Hawau Olamide Toyin, Shady Shehata, Preslav                  files: evidence from preprints in llms. arXiv preprint
  Nakov, and Zeerak Talat. 2024. Exploring the                 arXiv:2404.15799.
  limitations of detecting machine-generated text.
  arXiv preprint arXiv:2406.11073.                          Yule Liu, Zhiyuan Zhong, Yifan Liao, Zhen Sun, Jingyi
                                                              Zheng, Jiaheng Wei, Qingyuan Gong, Fenghua Tong,
Mingmeng Geng, Caixi Chen, Yanru Wu, Dongping                 Yang Chen, Yang Zhang, et al. 2024. On the gener-
  Chen, Yao Wan, and Pan Zhou. 2024. The impact of            alization ability of machine-generated text detectors.
  large language models in academia: from writing to          arXiv preprint arXiv:2412.17242.
  speaking. arXiv preprint arXiv:2409.13686.
                                                            Dino Pedreschi, Luca Pappalardo, Emanuele Ferragina,
Mingmeng Geng and Roberto Trotta. 2024. Is chat-              Ricardo Baeza-Yates, Albert-László Barabási, Frank
  gpt transforming academics’ writing style? arXiv            Dignum, Virginia Dignum, Tina Eliassi-Rad, Fosca
  preprint arXiv:2404.08627.                                  Giannotti, János Kertész, et al. 2024. Human-ai co-
                                                              evolution. Artificial Intelligence, page 104244.
Soumya Suvra Ghosal, Souradip Chakraborty, Jonas
  Geiping, Furong Huang, Dinesh Manocha, and Am-            Delip Rao, Jonathan Young, Thomas Dietterich, and
  rit Singh Bedi. 2023. Towards possibilities & im-           Chris Callison-Burch. 2024. Withdrarxiv: A large-
  possibilities of ai-generated text detection: A survey.     scale dataset for retraction study. arXiv preprint
  arXiv preprint arXiv:2310.15264.                            arXiv:2412.03775.
                                                       12694

Pedro Reviriego, Javier Conde, Elena Merino-Gómez,          A   Appendix
  Gonzalo Martínez, and José Alberto Hernández.
  2024. Playing with words: Comparing the vocab-
  ulary and lexical diversity of chatgpt and humans.
  Machine Learning with Applications, 18:100602.
Karolina Rudnicka. 2023. Can grammarly and chatgpt
  accelerate language change? ai-powered technolo-
  gies and their impact on the english language: wordi-
  ness vs. conciseness. Procesamiento de Lenguaje
  Natural, 71.
Jenna Russell, Marzena Karpinska, and Mohit Iyyer.
  2025. People who frequently use chatgpt for writing
  tasks are accurate and robust detectors of ai-generated
  text. arXiv preprint arXiv:2501.15654.
Vinu Sankar Sadasivan, Aounon Kumar, Sriram Bala-
  subramanian, Wenxiao Wang, and Soheil Feizi. 2023.                                 (a)
  Can ai-generated text be reliably detected? arXiv
  preprint arXiv:2303.11156.
Ruixiang Tang, Yu-Neng Chuang, and Xia Hu. 2024.
  The science of detecting llm-generated text. Commu-
  nications of the ACM, 67(4):50–59.
Yichen Wang, Shangbin Feng, Abe Bohan Hou, Xiao
  Pu, Chao Shen, Xiaoming Liu, Yulia Tsvetkov, and
  Tianxing He. 2024. Stumbling blocks: Stress testing
  the robustness of machine-generated text detectors
  under attacks. arXiv preprint arXiv:2402.11638.
Yuxia Wang, Artem Shelmanov, Jonibek Mansurov,
  Akim Tsvigun, Vladislav Mikhailov, Rui Xing, Zhuo-
  han Xie, Jiahui Geng, Giovanni Puccetti, Ekate-                                   (b)
  rina Artemova, et al. 2025. Genai content de-
  tection task 1: English and multilingual machine-         Figure 7: Frequency of some words in arXiv abstracts.
  generated text detection: Ai vs. human. arXiv
  preprint arXiv:2501.11012.

Debora Weber-Wulff, Alla Anohina-Naumeca, Sonja
  Bjelobaba, Tomáš Foltỳnek, Jean Guerrero-Dib, Olu-
  mide Popoola, Petr Šigut, and Lorna Waddington.
  2023. Testing of detection tools for ai-generated
  text. International Journal for Educational Integrity,
  19(1):26.
Qihui Zhang, Chujie Gao, Dongping Chen, Yue Huang,
  Yixin Huang, Zhenyang Sun, Shilin Zhang, Weiye
  Li, Zhengyan Fu, Yao Wan, et al. 2024a. Llm-as-a-
  coauthor: Can mixed human-written and machine-
  generated text be detected? In Findings of the Asso-
  ciation for Computational Linguistics: NAACL 2024,
  pages 409–436.
Yuehan Zhang, Yongqiang Ma, Jiawei Liu, Xiaozhong
  Liu, Xiaofeng Wang, and Wei Lu. 2024b. Detection
  vs. anti-detection: Is text generated by ai detectable?
  In International Conference on Information, pages
  209–222. Springer.

                                                       12695

                         (a)                                                          (b)

                         (c)                                                         (d)

Figure 8: Frequency of some words in arXiv abstracts. The data for withdrawn papers represents a 12-month rolling
average, labeled by “w”.

Table 1: Papers on word frequency analysis published in March and April 2024 (submitted to arXiv). The Google
citation counts are as of January 16, 2025.

 Paper                         Citations    Highlighted words
 (Liang et al., 2024a)         87           commendable, innovative, meticulous, intricate, notable,
                                            versatile.
 (Liang et al., 2024b)         58           pivotal, intricate, realm, showcasing.
 (Gray, 2024)                  41           words listed based on Liang et al. (2024a)
 (Geng and Trotta, 2024)       11           significant, crucial, effectively, additionally, comprehensive,
                                            enhance, capabilities, valuable.
 (Liu and Bu, 2024)            4            No words are highlighted.

                                                     12696
