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
    "I went home. She went home. We all went home. They went home too. Everyone left.",
    "uniform short sentences, low variance")
expect_pass("sentence-length-variance",
    "I went home. The extraordinarily complex municipal infrastructure project that had been debated for nearly a decade was finally approved by the city council after a marathon session. Yes. The report covered demographic shifts across three continents over a forty-year period using novel statistical methods.",
    "high variance between short and long")


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


# --- Summary ---

print(f"\n{'='*40}")
if FAILURES:
    print(f"FAILED: {FAILURES} assertion(s) broken")
    sys.exit(1)
else:
    print("ALL PASSED")
    sys.exit(0)
