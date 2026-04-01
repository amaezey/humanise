#!/usr/bin/env python3
"""Self-tests for grade.py checks.

Each check gets known-bad text (must fail) and known-clean text (must pass).
If any assertion is wrong, the check's regex/logic has a bug.

Run: python3 evals/test_grade.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from grade import ALL_CHECKS

FAILURES = 0


def expect_fail(check_name, text, reason):
    """Assert that the check FAILS on this text."""
    global FAILURES
    result = ALL_CHECKS[check_name](text)
    if result["passed"]:
        FAILURES += 1
        print(f"FAIL: {check_name} should have failed on: {reason}")
        print(f"  Evidence: {result['evidence']}")
    else:
        print(f"  ok: {check_name} correctly fails on: {reason}")


def expect_pass(check_name, text, reason):
    """Assert that the check PASSES on this text."""
    global FAILURES
    result = ALL_CHECKS[check_name](text)
    if not result["passed"]:
        FAILURES += 1
        print(f"FAIL: {check_name} should have passed on: {reason}")
        print(f"  Evidence: {result['evidence']}")
    else:
        print(f"  ok: {check_name} correctly passes on: {reason}")


# --- no-em-dashes ---

print("\n=== no-em-dashes ===")
expect_fail("no-em-dashes",
    "I'm still keen to connect\u2014would Tuesday work?",
    "em dash in sentence")
expect_pass("no-em-dashes",
    "I'm still keen to connect - would Tuesday work?",
    "hyphen, not em dash")


# --- no-ai-vocabulary-clustering ---

print("\n=== no-ai-vocabulary-clustering ===")
expect_fail("no-ai-vocabulary-clustering",
    "The intricate landscape fosters a vibrant tapestry of culture.",
    "5 AI words in one paragraph")
expect_fail("no-ai-vocabulary-clustering",
    "This aligns with the broader landscape of fostering innovation.",
    "'aligns with' (inflected) + landscape + fostering = 3")
expect_pass("no-ai-vocabulary-clustering",
    "The project improves access to clean water in rural areas.",
    "no AI vocabulary")
expect_pass("no-ai-vocabulary-clustering",
    "This aligns with our goals. In a separate paragraph.\n\nThe landscape is flat.",
    "'aligns with' and 'landscape' in different paragraphs (max 1 per para)")
expect_fail("no-ai-vocabulary-clustering",
    "The seamless integration genuinely fosters a transformative experience.",
    "'seamless' + 'genuinely' + 'fosters' + 'transformative' = 4 AI words")
expect_pass("no-ai-vocabulary-clustering",
    "I actually went to the store and bought some hidden gems of local produce.",
    "'actually' without filler pattern and 'hidden' without significance pattern are not flagged")


# --- no-manufactured-insight ---

print("\n=== no-manufactured-insight ===")
expect_fail("no-manufactured-insight",
    "Here's the thing: nobody actually reads the manual.",
    "here's the thing")
expect_fail("no-manufactured-insight",
    "What's really happening is a shift in power.",
    "what's really")
expect_pass("no-manufactured-insight",
    "The manual was updated in 2024 to reflect new safety standards.",
    "plain factual statement")


# --- no-staccato-sequences ---

print("\n=== no-staccato-sequences ===")
expect_fail("no-staccato-sequences",
    "It works. It really works. Trust me. I know this.",
    "4 consecutive short sentences")
expect_pass("no-staccato-sequences",
    "The library was built in 1923 and has served the community ever since.",
    "one long sentence")


# --- no-anaphora ---

print("\n=== no-anaphora ===")
expect_fail("no-anaphora",
    "Every morning I run. Every morning I stretch. Every morning I eat.",
    "3 sentences starting with 'every'")
expect_pass("no-anaphora",
    "First I run. Then I stretch. After that I eat breakfast with coffee.",
    "varied sentence starts")


# --- no-collaborative-artifacts ---

print("\n=== no-collaborative-artifacts ===")
expect_fail("no-collaborative-artifacts",
    "I hope this helps with your project!",
    "I hope this helps")
expect_fail("no-collaborative-artifacts",
    "If needed, the explanation can be reframed for a policy audience.",
    "soft offer-to-continue")
expect_fail("no-collaborative-artifacts",
    "Feel free to reach out if you have questions.",
    "feel free to")
expect_pass("no-collaborative-artifacts",
    "The bridge was completed in 1937 after four years of construction.",
    "plain factual statement")


# --- no-curly-quotes ---

print("\n=== no-curly-quotes ===")
expect_fail("no-curly-quotes",
    "She said \u201chello\u201d to the crowd.",
    "curly double quotes")
expect_pass("no-curly-quotes",
    'She said "hello" to the crowd.',
    "straight quotes")


# --- sentence-length-variance ---

print("\n=== sentence-length-variance ===")
expect_fail("sentence-length-variance",
    "I went home after work. She went home after work. We all went home after work. They went home after work too. Everyone left work early today. He went home after work as well. They all went home after that. We went together after the meeting. She came along with the team. He tagged along with us too. I drove home alone after. She took the bus home today. We all ended up leaving early. They went to get some food first. Everyone was tired from work today. He walked all the way back home. They caught the train after five.",
    "uniform short sentences, low variance, 17 sentences over 100 words")
expect_pass("sentence-length-variance",
    "I went home. The extraordinarily complex municipal infrastructure project that had been debated for nearly a decade was finally approved by the city council after a marathon session. Yes. The report covered demographic shifts across three continents over a forty-year period using novel statistical methods.",
    "high variance between short and long")
expect_pass("sentence-length-variance",
    "Thanks for the invite. I can't make Tuesday but could do Thursday afternoon.",
    "short-form text skipped (under 100 words, under 6 sentences)")


# --- no-promotional-language ---

print("\n=== no-promotional-language ===")
expect_fail("no-promotional-language",
    "The stunning views and vibrant culture make this a must-visit destination.",
    "stunning + vibrant + must-visit")
expect_pass("no-promotional-language",
    "The hotel is on a quiet street near the old quarter.",
    "neutral description")


# --- no-significance-inflation ---

print("\n=== no-significance-inflation ===")
expect_fail("no-significance-inflation",
    "This marked a pivotal moment in the evolving landscape of regional policy.",
    "pivotal + evolving landscape")
expect_pass("no-significance-inflation",
    "The policy was introduced in 2019 and applied to three regions.",
    "plain factual")


# --- no-negative-parallelisms ---

print("\n=== no-negative-parallelisms ===")
expect_fail("no-negative-parallelisms",
    "It's not just about money, but about dignity.",
    "not just...but")
expect_fail("no-negative-parallelisms",
    "Learning to cook is not about becoming a chef. It is about reclaiming a fundamental capability.",
    "cross-sentence not about X. It is about Y")
expect_fail("no-negative-parallelisms",
    "Travel is less about new places than about testing yourself.",
    "is less about X than about Y")
expect_pass("no-negative-parallelisms",
    "The building was not damaged in the fire. It was inspected the following day.",
    "factual negation, not a reframing move")


# --- no-copula-avoidance ---

print("\n=== no-copula-avoidance ===")
expect_fail("no-copula-avoidance",
    "The library serves as a community hub.",
    "serves as (singular)")
expect_fail("no-copula-avoidance",
    "Libraries serve as trusted institutions.",
    "serve as (plural)")
expect_fail("no-copula-avoidance",
    "They function as informal education infrastructure.",
    "function as (plural)")
expect_pass("no-copula-avoidance",
    "The library is a community hub.",
    "plain copula 'is'")


# --- no-filler-phrases ---

print("\n=== no-filler-phrases ===")
expect_fail("no-filler-phrases",
    "In order to succeed, you must plan carefully.",
    "in order to")
expect_fail("no-filler-phrases",
    "It is worth recognising that this takes time.",
    "it is worth recognising")
expect_fail("no-filler-phrases",
    "Cooking is often framed as a chore.",
    "is often framed as")
expect_pass("no-filler-phrases",
    "Planning helps you succeed.",
    "clean rewrite")


# --- no-generic-conclusions ---

print("\n=== no-generic-conclusions ===")
expect_fail("no-generic-conclusions",
    "The future looks bright for renewable energy.",
    "the future looks bright")
expect_pass("no-generic-conclusions",
    "Solar capacity is projected to double by 2030.",
    "specific factual conclusion")


# --- no-forced-triads ---

print("\n=== no-forced-triads ===")
expect_fail("no-forced-triads",
    "It supports equity, participation, and resilience.",
    "equity doesn't match but participation (-tion) and resilience (-ence) do")
expect_fail("no-forced-triads",
    "The program builds curation, classification, and neutrality.",
    "all three match -tion/-ity")
expect_pass("no-forced-triads",
    "The store sells apples, bread, and milk.",
    "concrete nouns, not abstract")


# --- no-superficial-ing ---

print("\n=== no-superficial-ing ===")
expect_fail("no-superficial-ing",
    "The temple uses blue and gold, reflecting the community's deep connection to the land.",
    "tacked-on reflecting clause")
expect_pass("no-superficial-ing",
    "The temple uses blue and gold. According to the architect, these reference local flora.",
    "no tacked-on -ing")


# --- no-ghost-spectral-density ---

print("\n=== no-ghost-spectral-density ===")
expect_fail("no-ghost-spectral-density",
    "The ghost of memory whispers through the shadows of the old house, echoes lingering.",
    "ghost + whispers + shadows + echoes")
expect_pass("no-ghost-spectral-density",
    "The house was built in 1890 and renovated twice since.",
    "no spectral language")


# --- no-quietness-obsession ---

print("\n=== no-quietness-obsession ===")
expect_fail("no-quietness-obsession",
    "A quiet stillness settled over the room. She spoke softly, gently, in hushed tones.",
    "quiet + stillness + softly + gently + hushed = 5")
expect_pass("no-quietness-obsession",
    "The meeting ended at three. Everyone left quickly.",
    "no quietness words")


# --- no-rhetorical-questions ---

print("\n=== no-rhetorical-questions ===")
expect_fail("no-rhetorical-questions",
    "The data is clear. But what about cost? The answer is simple. But what about time? The answer is complicated.",
    "2 rhetorical questions with declarative answers")
expect_pass("no-rhetorical-questions",
    "The project was completed on time and under budget.",
    "no questions at all")


# --- no-excessive-lists ---

print("\n=== no-excessive-lists ===")
expect_fail("no-excessive-lists",
    "Key points:\n- First item\n- Second item\n- Third item\n- Fourth item\n- Fifth item\n- Sixth item\n- Seventh item\n- Eighth item\n- Ninth item\nDone.",
    "9/11 lines are bullets = 81%")
expect_pass("no-excessive-lists",
    "The bridge was built in two phases. First, the foundations were laid. Then the span was constructed. A small ceremony marked completion.",
    "no list markers")


# --- no-dramatic-transitions ---

print("\n=== no-dramatic-transitions ===")
expect_fail("no-dramatic-transitions",
    "And then something shifted. I saw the world differently.",
    "something shifted")
expect_pass("no-dramatic-transitions",
    "After the meeting, I revised the proposal based on their feedback.",
    "factual transition")


# --- no-formulaic-openers ---

print("\n=== no-formulaic-openers ===")
expect_fail("no-formulaic-openers",
    "At a foundational level, libraries provide access to information.\n\nBeyond this, they also serve communities.",
    "two formulaic openers")
expect_fail("no-formulaic-openers",
    "At its core, cooking is about autonomy.",
    "at its core")
expect_fail("no-formulaic-openers",
    "There is also a practical dimension that is difficult to ignore.",
    "there is also a")
expect_fail("no-formulaic-openers",
    "From a governance perspective, libraries support democratic participation.",
    "from a X perspective")
expect_pass("no-formulaic-openers",
    "Libraries provide access to information.\n\nThey also serve communities.",
    "plain direct openers")


# --- no-signposted-conclusions ---

print("\n=== no-signposted-conclusions ===")
expect_fail("no-signposted-conclusions",
    "The data supports this view.\n\nIn summary, the project was a success.",
    "In summary")
expect_fail("no-signposted-conclusions",
    "Some more text here.\n\n## Conclusion\n\nThe results were clear.",
    "Conclusion heading")
expect_fail("no-signposted-conclusions",
    "First point.\n\nTo summarise, the evidence is strong.",
    "To summarise")
expect_pass("no-signposted-conclusions",
    "The evidence points in one direction. I doubt this will change.",
    "natural ending without signpost")


# --- no-markdown-headings ---

print("\n=== no-markdown-headings ===")
expect_fail("no-markdown-headings",
    "# The Importance of Libraries\n\n## Access to Information\n\nLibraries provide free access.",
    "H1 + H2 headings")
expect_pass("no-markdown-headings",
    "Libraries provide free access to information. They also host community events.",
    "plain prose, no headings")


# --- no-corporate-ai-speak ---

print("\n=== no-corporate-ai-speak ===")
expect_fail("no-corporate-ai-speak",
    "I deliver impact quickly and drive measurable outcomes across cross-functional teams.",
    "deliver impact + measurable outcomes + cross-functional")
expect_fail("no-corporate-ai-speak",
    "I translate ambiguous requirements into deliverable outcomes.",
    "translate requirements into deliverable outcomes")
expect_fail("no-corporate-ai-speak",
    "I have led end-to-end development across backend services.",
    "end-to-end development")
expect_pass("no-corporate-ai-speak",
    "I built the payment service and mentored two junior engineers.",
    "plain description of work")


# --- no-this-chains ---

print("\n=== no-this-chains ===")
expect_fail("no-this-chains",
    "The policy changed in 2020. This exposed gaps in planning. This shifted the debate. This forced a rethink of priorities.",
    "3 consecutive This [verb] sentences")
expect_pass("no-this-chains",
    "The policy changed in 2020. This exposed gaps in planning. The government responded with new funding.",
    "only 1 This [verb], then a different subject")


# --- no-excessive-hedging ---

print("\n=== no-excessive-hedging ===")
expect_fail("no-excessive-hedging",
    "The impact is often framed as transformative. The role is widely regarded as essential. The outcome cannot be overstated. Success is contingent on execution.",
    "4 hedging constructions in one text")
expect_pass("no-excessive-hedging",
    "The bridge was built in 1937. It cost twelve million dollars. Construction took four years.",
    "no hedging")
expect_pass("no-excessive-hedging",
    "Cooking is often framed as a chore. The value is increasingly recognised. But most people just want dinner.",
    "2 hedging constructions (under threshold)")


# --- no-countdown-negation ---

print("\n=== no-countdown-negation ===")
expect_fail("no-countdown-negation",
    "It wasn't the data. It wasn't the model. It was the prompt.",
    "classic countdown negation: two negations then reveal")
expect_fail("no-countdown-negation",
    "This isn't about money. This isn't about power. This is about principle.",
    "countdown with 'this isn't'")
expect_pass("no-countdown-negation",
    "It wasn't ready on Monday. The team finished it by Wednesday.",
    "single negation followed by unrelated statement")
expect_pass("no-countdown-negation",
    "The building was not damaged. It was inspected the following day.",
    "factual negation, not a countdown pattern")


# --- vocabulary-diversity ---

print("\n=== vocabulary-diversity ===")
expect_pass("vocabulary-diversity",
    "Short text with only a few words.",
    "short text skipped (under 150 words)")
expect_fail("vocabulary-diversity",
    " ".join(["the system is very good and the system is very effective and the system is very reliable"] * 20),
    "extremely repetitive text with low TTR")
expect_pass("vocabulary-diversity",
    "The cathedral was built between 1163 and 1345 on the Ile de la Cite in Paris. "
    "Its flying buttresses were among the first in Gothic architecture, allowing thinner walls "
    "and larger stained glass windows. During the French Revolution, much of the religious imagery "
    "was damaged or destroyed, and the building served briefly as a warehouse. Victor Hugo's 1831 "
    "novel drew public attention to its deteriorating condition, prompting a major restoration led "
    "by architect Eugene Viollet-le-Duc. The spire he added collapsed during the 2019 fire, which "
    "also destroyed the oak roof frame known as 'the forest' because of the number of trees used "
    "in its construction. Rebuilding efforts have drawn craftspeople from across Europe using both "
    "traditional and modern techniques. The limestone facade has been cleaned for the first time in "
    "decades, revealing the original pale colour beneath centuries of pollution. Historians debate "
    "whether the restoration should preserve Viollet-le-Duc's additions or return to an earlier "
    "medieval form. The cathedral reopened in December 2024 after five years of intensive work.",
    "varied human prose with diverse vocabulary")


# --- new vocabulary items ---

print("\n=== new vocabulary items (spot check) ===")
expect_fail("no-ai-vocabulary-clustering",
    "The unparalleled results were invaluable to the meticulous research team.",
    "'unparalleled' + 'invaluable' + 'meticulous' = 3 new AI vocab items")


# --- Summary ---

print(f"\n{'='*40}")
if FAILURES:
    print(f"FAILED: {FAILURES} assertion(s) broken")
    sys.exit(1)
else:
    print("ALL PASSED")
    sys.exit(0)
