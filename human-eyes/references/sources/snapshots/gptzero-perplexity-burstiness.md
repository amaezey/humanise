Title: What is perplexity & burstiness for AI detection? - GPTZero

URL Source: https://gptzero.me/news/perplexity-and-burstiness-what-is-it/

Published Time: 2023-03-01T05:07:00.000Z

Markdown Content:
# What is perplexity & burstiness for AI detection? - GPTZero

Toggle menu

[![Image 1](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/2024/08/solid-logo-2.png)](https://gptzero.me/ "AI Detection Resources | GPTZero")

*   [Search](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)
*   [Dashboard](https://app.gptzero.me/app?utm_source=blog&utm_medium=header)
*   [All News](https://gptzero.me/news)
*   [Education](https://gptzero.me/news/tag/education)
*   [Investigations](https://gptzero.me/news/tag/investigations)
*   [Technology](https://gptzero.me/news/tag/technology)
*   [Pricing](https://gptzero.me/pricing?utm_source=blog&utm_medium=header)
*   [About Us](https://gptzero.me/team?utm_source=blog&utm_medium=header)

 Search Search[Dashboard](https://app.gptzero.me/app)

[Technology](https://gptzero.me/news/tag/technology/)

# Perplexity, burstiness, and statistical AI detection

[![Image 2](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 3: Edward Tian](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/2024/01/profile-1.png)](https://gptzero.me/news/author/edward/)

[Edward Tian](https://gptzero.me/news/author/edward/)

 Mar 01, 2023 · 3 min read 

[Share on X](https://x.com/intent/tweet?text=Perplexity%2C%20burstiness%2C%20and%20statistical%20AI%20detection&url=https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)[Share on Facebook](https://www.facebook.com/sharer/sharer.php?u=https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)[Share on Linkedin](https://www.linkedin.com/sharing/share-offsite/?url=https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)

Fact checked

Copy citation to this article Copy link[Send by email](https://gptzero.me/cdn-cgi/l/email-protection#221d404d465b1f4a56565251180d0d4552565847504d0c4f470d4c4755510d524750524e475a4b565b0f434c460f40575051564b4c4751510f554a43560f4b510f4b560d04515740484741561f724750524e475a4b565b0e0240575051564b4c4751510e02434c4602515643564b51564b41434e02636b024647564741564b4d4c)

![Image 4](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w720/2024/03/CNN.png)

### Table of contents

In January, we released GPTZero’s first AI detection model publicly for everyone. The demand was deafening — with seven million views and half million users in the first week, GPTZero was called Hero of the Week on UK radio, internationally covered, in Japan, France, Australia and over thirty countries, even landing a feature on the front page of the NYT.

The thesis was simple — build a model that is efficient and effective, and make it accessible to every person who needs it. To do so, the original GPTZero model applied a ‘statistical approach’, leveraging academic research in natural language processing to convert written words to numbers for calculation.

Today, the first principles from GPTZero’s original detection model is still being applied widely. These methods are efficient — leveraging numerical analysis instead of deep text analysis. They are the least computationally expensive of AI detection methods. Additionally, they are actually the main applications behind dozens of other [AI detector](https://gptzero.me/) apps including ZeroGPT, Copyleaks, Originality, and Writer[dot]AI. They remain effective — and as such act as one of the [seven ‘indicators’](https://gptzero.me/technology) of the upgraded GPTZero detection model, alongside our novel text search and [deep learning](https://gptzero.me/news/deep-learning-model-updates/) detection approaches.

![Image 5](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/2023/07/Screen-Shot-2023-07-07-at-10.59.41-PM.png)

Figure 1: Anderson Cooper asking what is perplexity and burstiness

**What is Perplexity and Burstiness**

The statistical layer of GPTZero’s AI detection model is composed of a ‘perplexity’ and ‘burstiness’ calculation — together they form the first layer for GPTZero’s AI detection.

You can interpret the perplexities per sentence as a measure of how likely an AI model would have chosen the exact same set of words as found in the document. One aspect of GPTZero’s algorithm uses an AI model similar to language models like ChatGPT to measure the perplexity of the given document.

We’ve trained the AI model to identify when the input text looks very similar to something written by a language model. For example, the sentence, “Hi there, I am an AI _” would most likely be continued by an AI model with the word “assistant”, which would have low perplexity. On the other hand, if the next word that followed was “potato”, then that sentence would have much higher perplexity, and also a greater likelihood of being written by a human. Over the course of hundreds of words, these probabilities compound to give us a clear picture of the origin of this document. There isn’t an absolute scale for perplexity, but generally, a perplexity above 85 is more likely than not from a human source. Here’s a guide with more technical definitions of this measure:

[Perplexity in Language Models. Evaluating language models using the… | by Chiara Campagnola | Towards Data Science](https://towardsdatascience.com/perplexity-in-language-models-87a196019a94)

Burstiness, on the other hand, is a measure of how much writing patterns and text perplexities vary over the entire document. As humans, we have a tendency to vary our writing patterns. Philosophically, our short-term memory activates, and dissuades us from writing similar things twice. Conversely, language models have a significant ‘AI-print’ where they write with a very consistent level of AI-likeness. While a person could easily write an AI-like sentence by accident, people tend to vary their sentence construction and diction throughout a document.

On the other hand, models formulaically use the same rule to choose the next word in the sentence, leading to low burstiness. Compared to other statistical methods for AI detection, burstiness is a key factor unique to GPTZero detector, allowing our models to evaluate long-term-context, and perform better with additional inputs.

*   [Technology](https://gptzero.me/news/tag/technology/)
*   [GPTZero](https://gptzero.me/news/tag/gptzero/)

[![Image 6](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 7](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w250/2024/01/profile-1.png)](https://gptzero.me/news/author/edward/)

### [Written by Edward Tian](https://gptzero.me/news/author/edward/)

Edward is the CEO of GPTZero. He previously worked on synthetic data research at Microsoft AI, and as an investigative journalist at the BBC.

### Keep reading

[Technology](https://gptzero.me/news/tag/technology/)

[![Image 8](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 9: Edwin Thomas](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2024/11/IMG_5913.jpg)](https://gptzero.me/news/author/edwin/)

[Edwin Thomas](https://gptzero.me/news/author/edwin/)

[![Image 10](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w720/2026/01/Add-a-heading--10-.png)](https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/)

[Technology](https://gptzero.me/news/tag/technology/)

[![Image 11](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 12: Edwin Thomas](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2024/11/IMG_5913.jpg)](https://gptzero.me/news/author/edwin/)

[Edwin Thomas](https://gptzero.me/news/author/edwin/)

## [Detecting AI-Humanized Text: How GPTZero Stays Ahead](https://gptzero.me/news/detecting-ai-humanized-text-how-gptzero-stays-ahead/)

AI-generated content is becoming more widespread, and so too are “humanizers” that paraphrase AI text to dodge detection. Here, we show why GPTZero is best at identifying LLM texts that have undergone humanization attempts.

 Jan 26, 2026 · 5 min read 

[AI Research](https://gptzero.me/news/tag/ai-research/) Featured 

[![Image 13](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 14: Emily Napier](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2025/04/Remarkable-2024-070A8871--1--1.jpg)](https://gptzero.me/news/author/emily/)[![Image 15](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 16: Alex Adam](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2024/01/20180829_145610.jpg)](https://gptzero.me/news/author/alex-adam/)[![Image 17](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 18: Adele Barlow](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2024/09/adele-barlow-profile-pic.jpeg)](https://gptzero.me/news/author/adele-barlow/)

[Emily Napier](https://gptzero.me/news/author/emily/), [Alex Adam](https://gptzero.me/news/author/alex-adam/), [Adele Barlow](https://gptzero.me/news/author/adele-barlow/)

[![Image 19: Bar chart titled 'Accuracy of AI Detectors' showing GPTZero at 99.5%, Pangram at 99.1%, and Originality at 85% on the Chicago Booth benchmark](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w720/2026/01/Screenshot-2026-01-12-at-7.16.05---PM.png)](https://gptzero.me/news/chicago-booth-2026/)

[AI Research](https://gptzero.me/news/tag/ai-research/) Featured 

[![Image 20](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 21: Emily Napier](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2025/04/Remarkable-2024-070A8871--1--1.jpg)](https://gptzero.me/news/author/emily/)[![Image 22](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 23: Alex Adam](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2024/01/20180829_145610.jpg)](https://gptzero.me/news/author/alex-adam/)[![Image 24](https://gptzero.me/news/assets/images/avatar.jpg?v=0fb3259135)![Image 25: Adele Barlow](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/size/w100/2024/09/adele-barlow-profile-pic.jpeg)](https://gptzero.me/news/author/adele-barlow/)

[Emily Napier](https://gptzero.me/news/author/emily/), [Alex Adam](https://gptzero.me/news/author/alex-adam/), [Adele Barlow](https://gptzero.me/news/author/adele-barlow/)

## [GPTZero Tops Accuracy on Chicago Booth Benchmark in 2026](https://gptzero.me/news/chicago-booth-2026/)

GPTZero outperforms other AI detectors like Pangram on Chicago Booth Benchmark, achieving ~99% accuracy and industry-leading recall for AI detection.

 Jan 12, 2026 · 4 min read 

[Share on X](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/#)Copy link

[![Image 26](https://storage.ghost.io/c/93/d8/93d84efe-2017-4168-9591-b749ab8330d5/content/images/2024/08/solid-logo-2.png)](https://gptzero.me/ "AI Detection Resources | GPTZero")

### Products

*   [AI Detector](https://gptzero.me/?utm_source=blog&utm_medium=footer)
*   [Chrome Extension](https://chromewebstore.google.com/detail/gptzero-ai-detector-and-h/kgobeoibakoahbfnlficpmibdbkdchap)
*   [Integrations](https://gptzero.me/lms-integrations?utm_source=blog&utm_medium=footer)
*   [Plagiarism Checker](https://gptzero.me/plagiarism-checker?utm_source=blog&utm_medium=footer)

### Resources

*   [Pricing](https://gptzero.me/pricing?utm_source=blog&utm_medium=footer)
*   [Sales](https://gptzero.me/sales?utm_source=blog&utm_medium=footer)
*   [Blog](https://gptzero.me/news?utm_source=blog&utm_medium=footer)
*   [Education](https://gptzero.me/educators?utm_source=blog&utm_medium=footer)

### Company

*   [About us](https://gptzero.me/team?utm_source=blog&utm_medium=footer)
*   [Team](https://gptzero.me/team?utm_source=blog&utm_medium=footer)
*   [Affiliates](https://gptzero.getrewardful.com/signup)
