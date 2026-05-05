Title: The Em Dash Dilemma: How a Punctuation Mark Became AI’s Stubborn Signature

URL Source: https://medium.com/@brentcsutoras/the-em-dash-dilemma-how-a-punctuation-mark-became-ais-stubborn-signature-684fbcc9f559

Published Time: 2025-04-29T18:45:36Z

Markdown Content:
[![Image 1: Brent Csutoras](https://miro.medium.com/v2/resize:fill:32:32/0*__oHKItzIB47Y1nm.jpg)](https://medium.com/@brentcsutoras?source=post_page---byline--684fbcc9f559---------------------------------------)

4 min read

Apr 29, 2025

Almost a year ago, I stumbled into a weird rabbit hole, trying to outsmart AI. Since I moderate a number of very large subreddits, I started noticing certain patterns in posts that felt just a little too polished or off. One tell in particular kept showing up no matter what, the em dash.

This was around the same time there was a lot of buzz about AI detection tools and that Hard Fork story about the teacher who wrongly flunked a whole class for “cheating” with ChatGPT (spoiler, they didn’t cheat). It got me wondering, could I actually reverse-engineer the patterns that gave AI away?

I documented some of it [on LinkedIn](https://www.linkedin.com/posts/brentcsutoras_chatgpt-and-i-are-having-a-bit-of-a-battle-activity-7262492741337591809-7Nv_) as I went. I managed to strip out almost every recognizable AI signature, except for one. That stupid, stubborn, persistent em dash. No matter what settings, prompts, warnings, or threats I tried, AI just could not, or would not, quit it.

I pulled out every trick I could think of. Hard-coded instructions? Check.

Multiple reminders inside the prompt? Check.

![Image 2](https://miro.medium.com/v2/resize:fit:631/0*qVbzmQiepQydP2tA)

I pushed, pulled, rewired, and begged, but nothing made it stop.

And the AI even acknowledged it knew better, “You specifically instructed me to avoid em dashes. I recognize that.” And then, two sentences later, boom. Another em dash, right in my face. At one point, I even put a “Critical Error” label on any output that included one.

Didn’t matter. Those little punctuation bandits kept sneaking back in.

Eventually, after hammering away at it in different models and forums, I got a straight answer, it’s baked into their DNA. Turns out, em dashes are absolutely everywhere in the training data. In books, articles, essays, humans used them so often that AIs learned them as a default natural flow. It’s like asking a bird not to chirp.

Press enter or click to view image in full size

![Image 3](https://miro.medium.com/v2/resize:fit:700/0*U-upXwwYY7O6Ka0U)

Someone over on [OpenAI’s Community Forum](https://community.openai.com/t/cannot-get-responses-to-not-include-dashes-and-em-dashes/1023216/5) said it best, the em dash wasn’t flagged during AI training as something special or risky, so the models never learned to avoid it. Another discussion [here](https://community.openai.com/t/chatgpts-em-dash-habit-a-training-artifact-or-design-choice/1115873) pointed out that it’s basically a “deep bias” embedded into how the models understand written flow.

## Get Brent Csutoras’s stories in your inbox

Join Medium for free to get updates from this writer.

Remember me for faster sign in

And now? Humans are ditching em dashes, not because they don’t like them, but because they’re terrified their writing will look fake. One [commenter](https://news.ycombinator.com/item?id=43500389) on Hacker News even called it out directly, saying _‘the em dash is now a GPT-ism and is not advisable unless you want people to think your writing is the output of a LLM._

It’s a little heartbreaking for some. As Adam Cecil over at _Night Water_[put it](https://www.nightwater.email/em-dash-ai/), _“I love em dashes so much that I set up a custom text replacement shortcut years ago across all of my Apple devices to make it dead easy to type them.”_

But is the em dash actually a reliable way to tell if something was written by AI? Not really. If you dig into actual research, it’s clear em dashes aren’t a real giveaway. They show up because humans trained the models that way.

People like Daphne Ippolito, a senior scientist at Google Brain, say you have to look elsewhere for real clues. In an interview with [_MIT Technology Review_](https://www.technologyreview.com/2022/12/19/1065596/how-to-spot-ai-generated-text/), she pointed out that one easy signal is word frequency, especially how often AI uses “the” compared to humans. Another tip-off? Typos, or the lack of them. AI-generated text is usually spotless, while human writing is full of little mistakes and quirks.

The em dash mess is just one weird little example of a much bigger story, AI is subtly changing the way we write, talk, and think. Writers who love em dashes are backing off. Readers are second-guessing themselves. Even real humans are worried they sound too robotic.

As for me? I want to say I’ve made peace with it, but honestly, it still bugs me. That said, I’ve stopped wasting my time yelling at AIs about their em dash addiction. There are better battles to fight.

What I’m way more interested in is what this all means next, not just for writing, but for authenticity online. If a tiny piece of punctuation can create this much noise, just imagine what’s coming when the lines between real and generated blur even more.

This is still an issue today. So if you ever hear about a real fix, or if you figure out a trick that actually gets rid of the em dash for good, let me know. I would love to finally win this battle.

**Update: September 27,2025:**

I finally found a solution that’s working consistently through Claude. Create a project and in the instructions have it 1) create the initial output, 2) put the output into a holding area, and then 3) replace all em dash usage with commas.

I had it provide both the original and refined outputs initially and noticed the em dash usage in draft content, but the corrected comma usage in the final output.

**Update: August 21, 2025:**

Still no official acknowledgment or fix from OpenAI, Anthropic, or other AI companies. Community forums continue reporting the same problem with no effective solutions. The issue remains unsolved.
