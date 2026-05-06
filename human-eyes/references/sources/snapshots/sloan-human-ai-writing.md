Title: Writing with the machine

URL Source: https://www.robinsloan.com/notes/writing-with-the-machine/

Markdown Content:
I made some­thing new: a plugin that pro­vides inline text com­ple­tions pow­ered by an AI lan­guage model.

![Image 1: rnn-writer example](https://www.robinsloan.com/img/rnn-example-1.gif)

Building this felt like playing with Lego, except instead of plastic bricks, I was snap­ping together conveniently-packaged blocks of human intel­lect and effort.

One block: a recur­rent neural network, fruit of the deep learning boom, able to model and gen­erate sequences of char­ac­ters with spooky verisimilitude. Snap!

Another block: a pow­er­fully exten­sible text editor. Snap!

Together: responsive, inline “autocomplete” pow­ered by an RNN trained on a corpus of old sci-fi stories.

If I had to offer an extrav­a­gant analogy (and I do) I’d say it’s like writing with a deranged but very well-read parrot on your shoulder. Any­time you feel brave enough to ask for a suggestion, you press `tab`, and …

![Image 2: rnn-writer example](https://www.robinsloan.com/img/rnn-example-extra.gif)

If you’d like to try it yourself, the code is now avail­able, in two parts:

*   [`torch-rnn-server`](https://github.com/robinsloan/torch-rnn-server?utm_source=Robin_Sloan_sent_me) is a server that runs the neural network, accepts snippets of text, and returns “completions” of that text. In truth, it’s just a couple of tiny shims laid beneath Justin Johnson’s indispensable `torch-rnn`project.
*   [`rnn-writer`](https://github.com/robinsloan/rnn-writer?utm_source=Robin_Sloan_sent_me) is a package for the Atom text editor that knows how to talk to `torch-rnn-server` and present its completions to the user. I’m also providing an API for folks who want to try this but don’t feel up to the task of running a local server.

You’ll find instruc­tions for both tools on their respec­tive GitHub pages, and if you have dif­fi­cul­ties with either, feel free to open an issue or drop me a line.

Mainly, I wanted to share those links, but as long as I’m here I’ll add a few more things: first a note on motivations, then an obser­va­tion about the deep learning scene, and finally a link to the sci-fi corpus.

## The vision

From my first tin­ker­ings with the [`torch-rnn`](https://github.com/jcjohnson/torch-rnn?utm_source=Robin_Sloan_sent_me) project, gen­er­ating goofy/spooky text mim­icry on the com­mand line, I was struck — almost overwhelmed — by a vision of typing nor­mally in a text editor and then sum­moning the help of the RNN with a keystroke. (When I say “help,” I mean: less Clippy, more séance.)

After fum­bling around for a few weeks and learning five per­cent of two new pro­gram­ming lan­guages, I had the blocks snapped together; the RNN trained; the vision realized. And then my first hour playing with it was totally deflating. _Huh. Not as cool as I imag­ined it would be._

This is an unavoid­able emo­tional waysta­tion in any project, and pos­sibly a cru­cial one.

As I’ve spent more time with `rnn-writer`, my opinion has — er — reinflated somewhat. I am just so com­pelled by the notion of a text editor that pos­sesses a deep, nuanced model of … what? Every­thing you’ve ever written? Every­thing written by all your favorite authors? By your nemesis? By everyone on the internet? It’s provoca­tive any way you slice it.

I should say clearly: I am absolutely 100% not talking about an editor that “writes for you,” what­ever that means. The world doesn’t need any more dead-eyed robo-text.

The ani­mating ideas here are augmentation; partnership; call and response.

The goal is not to make writing “easier”; it’s to make it harder.

The goal is not to make the resulting text “better”; it’s to make it _different_—weirder, with effects maybe not avail­able by other means.

The tools I’m sharing here don’t achieve that goal; their effects are not yet suf­fi­cient com­pen­sa­tion for the effort required to use them. But! I think they could get there! And if this project has any con­tri­bu­tion to make beyond weird fun, I think it might be the simple trick of get­ting an RNN off the com­mand line and into a text editor, where its output becomes some­thing you can really _work_ with.

## Deep scenius

Like any tech-adjacent person, I’d been reading about deep learning for a couple of years, but it wasn’t until a long con­ver­sa­tion ear­lier this year with an old friend (who is eye-poppingly excited about these techniques) that I felt moti­vated to dig in myself. And, I have to report: it really is a remark­able com­mu­nity at a remark­able moment. Tracking papers on Arxiv, projects on Github, and threads on Twitter, you get the sense of a group of people nearly trip­ping over them­selves to do the next thing — to push the state of the art forward.

That’s all buoyed by a strong (recent?) cul­ture of clear explanation. My excited friend claims this has been as cru­cial to deep learning’s rise as the (more commonly-discussed) avail­ability of fast GPUs and large datasets. Having ben­e­fited from that cul­ture myself, it seems to me like a rea­son­able argument, and an impor­tant thing to recognize.

Here are a couple of resources I found espe­cially useful:

*   For get­ting acquainted with RNNs, the canon­ical doc­u­ment is Andrej Karpathy’s essay, [The Unrea­son­able Effec­tive­ness of Recur­rent Neural Networks](http://karpathy.github.io/2015/05/21/rnn-effectiveness/?utm_source=Robin_Sloan_sent_me). It’s a really remark­able example of tech­nical communication — deep and detailed but friendly, even playful.

*   Google’s [free deep learning course](https://www.udacity.com/course/deep-learning--ud730) is really very good, and it provided a crucial foundation for me. Structured learning: who knew??

*   Ross Goodwin's [Adventures in Nar­rated Reality](https://medium.com/@rossgoodwin/adventures-in-narrated-reality-6516ff395ba3?utm_source=Robin_Sloan_sent_me) brings RNNs into a cre­ative con­text and doesn't skimp on tech­nical details. I learned some key tricks from Ross's piece.

## 149,326,361 characters

Most of the energy in the deep learning scene is focused on what I’d call “generic” prob­lems, the solu­tions to which are very broadly useful to a lot of people: image recognition, speech recognition, sen­tence translation … you get the idea. Many of these prob­lems have asso­ci­ated bench­mark chal­lenges, and if your model gets a better score than the reigning champ, you know you’ve done some­thing worthwhile. These chal­lenges all depend on stan­dard datasets. And these … datasets … are … _extremely_ boring.

So, a large part of the work (and fun) of applying the deep learning scenesters’ hard-won tech­nical tri­umphs to weird/fun objec­tives is tracking down non-stan­dard, non-boring datasets. For me, deci­sions about the col­lec­tion and pro­cessing of the text corpus have been more con­se­quen­tial than deci­sions about the RNN’s design and sub­se­quent training.

The corpus I’ve used most is derived from the Internet Archive’s [Pulp Mag­a­zine Archive](https://archive.org/details/pulpmagazinearchive): 150MB of _Galaxy_ and _IF Mag­a­zine_. It’s very noisy, with tons of OCR errors and plenty of adver­tise­ments mixed in with the sci-fi stories, but _wow_ there is a lot of text, and the RNN seems to thrive on that. I lightly processed and nor­mal­ized it all, and the com­bined corpus — now just a huge text file without a single soli­tary line break — [is avail­able on the Internet Archive](https://archive.org/details/scifi-corpus).

So, in conclusion:

![Image 3](https://www.robinsloan.com/img/lego-ship-instrux.jpg)

Snap. Snap. Snap!

May 2016, Oak­land
