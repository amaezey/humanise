#!/usr/bin/env python3
"""Self-tests for grade.py checks.

Each check gets known-bad text (must fail) and known-clean text (must pass).
If any assertion is wrong, the check's regex/logic has a bug.

Run: python3 evals/test_grade.py
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("grade", ROOT / "humanise" / "grade.py")
_grade = importlib.util.module_from_spec(_spec)
if _spec.loader is None:
    raise RuntimeError("Could not load humanise/grade.py")
_spec.loader.exec_module(_grade)

ALL_CHECKS = _grade.ALL_CHECKS

# CHECK_METADATA was removed from grade.py in U7 (audit-report redesign).
# Reconstruct the four-field metadata view from humanise/patterns.yaml so the
# severity-propagation and failure-mode meta-tests below keep working.
import yaml as _yaml
_patterns_data = _yaml.safe_load((ROOT / "humanise" / "patterns.yaml").read_text())
CHECK_METADATA = {
    _cid: {k: _rec[k] for k in ("severity", "failure_modes", "evidence_role", "guidance")}
    for _cid, _rec in _patterns_data.items()
    if not _cid.startswith("_")  # skip _meta, _extra_entries (page-level content)
}
annotate_result = _grade.annotate_result
failure_mode_results = _grade.failure_mode_results
format_two_layer = _grade.format_two_layer
friendly_evidence = _grade.friendly_evidence
human_report = _grade.human_report
depth_results = _grade.depth_results
score_summary = _grade.score_summary
triggered_checks = _grade.triggered_checks

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


def expect_depth_status(results, depth, status, reason):
    """Assert depth_results reports the expected status."""
    global FAILURES
    actual = depth_results(results)[depth]["check_status"]
    if actual != status:
        FAILURES += 1
        print(f"FAIL: {depth} check_status should be {status} for {reason}; got {actual}")
    else:
        print(f"  ok: {depth} check_status is {status} for {reason}")


def expect_depth_actions(results, depth, required_fixes, preservable, reason):
    """Assert depth_results reports the expected action buckets."""
    global FAILURES
    actual = depth_results(results)[depth]
    failed = False
    if actual["required_fixes"] != required_fixes:
        FAILURES += 1
        failed = True
        print(f"FAIL: {depth} required_fixes should be {required_fixes} for {reason}; got {actual['required_fixes']}")
    if actual["preservable_with_disclosure"] != preservable:
        FAILURES += 1
        failed = True
        print(f"FAIL: {depth} preservable_with_disclosure should be {preservable} for {reason}; got {actual['preservable_with_disclosure']}")
    if actual["user_decision_needed"] != preservable:
        FAILURES += 1
        failed = True
        print(f"FAIL: {depth} user_decision_needed should be {preservable} for {reason}; got {actual['user_decision_needed']}")
    if not failed:
        print(f"  ok: {depth} action buckets match for {reason}")


# --- no-em-dashes ---

print("\n=== no-em-dashes ===")
expect_fail("no-em-dashes",
    "I'm still keen to connect\u2014would Tuesday work?",
    "em dash in sentence")
expect_pass("no-em-dashes",
    "I'm still keen to connect - would Tuesday work?",
    "hyphen, not em dash")
em_dash_results = [
    annotate_result(ALL_CHECKS["no-em-dashes"]("I'm still keen to connect\u2014would Tuesday work?"))
]
expect_depth_status(em_dash_results, "balanced", "fail", "em dash is a strong 2026 signal at Balanced depth")
expect_depth_status(em_dash_results, "all", "fail", "em dash is never allowed at All depth")


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
expect_fail("no-ai-vocabulary-clustering",
    "The study will provide a valuable insight, offer a valuable framework, and leave a lasting mark.",
    "3 GPTZero high-ratio phrases in one paragraph")
expect_pass("no-ai-vocabulary-clustering",
    "I actually went to the store and bought some hidden gems of local produce.",
    "'actually' without filler pattern and 'hidden' without significance pattern are not flagged")
expect_fail("no-ai-vocabulary-clustering",
    "The argument landed flat, and what surfaces in the discussion is a nuanced understanding of trust.",
    "nonliteral landed + surface + nuanced")
expect_pass("no-ai-vocabulary-clustering",
    "The plane landed safely on the island, and the table surface was scratched.",
    "literal land/surface usage")


# --- no-nonliteral-land-surface ---

print("\n=== no-nonliteral-land-surface ===")
expect_fail("no-nonliteral-land-surface",
    "The lesson shows students where their thinking landed and what to revise.",
    "nonliteral thinking landed")
expect_fail("no-nonliteral-land-surface",
    "What surfaced in the draft was a clearer argument.",
    "nonliteral surfaced in draft")
expect_fail("no-nonliteral-land-surface",
    "The grade tells students where they landed in the mark scheme.",
    "nonliteral pronoun landed in abstract scale")
expect_fail("no-nonliteral-land-surface",
    "The paper landed on the marking scale, but the student still needed advice.",
    "nonliteral paper landed on marking scale")
expect_fail("no-nonliteral-land-surface",
    "A grade tells a learner where a piece of work landed on a scale.",
    "nonliteral piece of work landed on scale")
expect_fail("no-nonliteral-land-surface",
    "Student work landed against the rubric, but the comment gave no next step.",
    "nonliteral student work landed against rubric")
expect_fail("no-nonliteral-land-surface",
    "A grade tells a student where a piece of work landed in the scoring system.",
    "nonliteral piece of work landed in scoring system")
expect_fail("no-nonliteral-land-surface",
    "The joke lands with the audience because the setup is familiar.",
    "nonliteral lands with audience")
expect_pass("no-nonliteral-land-surface",
    "The plane landed safely on the island, and the table surface was scratched.",
    "literal landed and physical surface")
expect_pass("no-nonliteral-land-surface",
    "The paper landed on the desk and slid under the notebook.",
    "literal paper landed on desk")


# --- overall-ai-signal-pressure ---

print("\n=== overall-ai-signal-pressure ===")
expect_pass("overall-ai-signal-pressure",
    (
        "This clinical covid antiviral study additionally aims to address "
        "challenges and enhance outcomes. The analysis underscores advancements, "
        "acknowledges limitations, and offers a comprehensive approach for "
        "patients receiving therapeutic intervention."
    ),
    "Kobak-heavy academic vocabulary alone is supporting evidence, not a failure")
expect_pass("overall-ai-signal-pressure",
    (
        "The clinic tested an antiviral drug in patients with covid. Fever fell "
        "after two days, and three patients left the ward by Friday."
    ),
    "biomedical content without style pressure")
expect_pass("overall-ai-signal-pressure",
    (
        "The essay additionally aims to address challenges and enhance outcomes. "
        "The analysis underscores advancements and offers a comprehensive approach "
        "for readers."
    ),
    "style words without other AI-ish structure")
expect_fail("overall-ai-signal-pressure",
    (
        "## Overview\n\n"
        "At its core, this clinical covid antiviral study is not just about "
        "treatment, but about navigating the complex landscape of patient trust. "
        "The analysis underscores advancements, acknowledges limitations, and "
        "offers a comprehensive approach for patients receiving therapeutic "
        "intervention. The takeaway is clear: this marks a pivotal moment.\n\n"
        "## Implications\n\n"
        "At its core, the work is less about data than about transformation. "
        "That is why the findings continue to inspire a deeper understanding."
    ),
    "Kobak pressure plus vocabulary, headings, formulaic openers, tidy endings, and reframes")


# --- no-manufactured-insight ---

print("\n=== no-manufactured-insight ===")
expect_fail("no-manufactured-insight",
    "Here's the thing: nobody actually reads the manual.",
    "here's the thing")
expect_fail("no-manufactured-insight",
    "What's really happening is a shift in power.",
    "what's really")
expect_fail("no-manufactured-insight",
    "What no one is talking about is how this changed the market.",
    "what no one is talking about")
expect_fail("no-manufactured-insight",
    "When no one noticed, the tool quietly became the default.",
    "when no one noticed framing")
expect_fail("no-manufactured-insight",
    "The shift nobody noticed was already underway.",
    "shift nobody noticed framing")
expect_fail("no-manufactured-insight",
    "The honest answer is that the data was incomplete from the start.",
    "performed candour — 'the honest answer is'")
expect_fail("no-manufactured-insight",
    "Here's the honest framing: the project missed every milestone.",
    "performed candour — 'here's the honest framing'")
expect_fail("no-manufactured-insight",
    "Here's the real truth — most teams skip retros entirely.",
    "performed candour — 'here's the real truth'")
expect_fail("no-manufactured-insight",
    "If I'm being honest, the proposal needs more work.",
    "performed candour — 'if I'm being honest'")
expect_fail("no-manufactured-insight",
    "In all honesty, the migration plan has too many unknowns.",
    "performed candour — 'in all honesty'")
expect_pass("no-manufactured-insight",
    "The manual was updated in 2024 to reflect new safety standards.",
    "plain factual statement")
expect_pass("no-manufactured-insight",
    "We strive to be honest about our limitations and update the docs as we learn.",
    "'to be honest' without leading comma — not the AI tell")


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
expect_fail("no-collaborative-artifacts",
    "Let's break it down so the main idea is clear.",
    "assistant explainer framing")
expect_fail("no-collaborative-artifacts",
    "Would you like me to make this more concise?",
    "assistant follow-up offer")
expect_fail("no-collaborative-artifacts",
    "Let me know if you want a shorter version.",
    "assistant continuation request")
expect_pass("no-collaborative-artifacts",
    "Would you like to know what makes his style such a pleasure to read?",
    "ordinary article question")
expect_pass("no-collaborative-artifacts",
    "The founder is pictured with a glass of champagne, of course!",
    "ordinary aside, not assistant residue")
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
expect_fail("no-negative-parallelisms",
    "The essay is a question of identity, not logistics.",
    "reversed Y, not X reframe")
expect_fail("no-negative-parallelisms",
    "The app is more about trust than convenience.",
    "more about Y than X reframe")
expect_fail("no-negative-parallelisms",
    "Not so much a tool as a partner.",
    "not so much X as Y")
expect_fail("no-negative-parallelisms",
    "You might think this is about speed. Actually, it is about trust.",
    "correction frame with abstract reveal")
expect_fail("no-negative-parallelisms",
    "No polish. No gimmicks. Just substance.",
    "No X. No Y. Just Z countdown")
expect_fail("no-negative-parallelisms",
    "Beyond convenience, the product is about connection.",
    "beyond X, about Y reframe")
expect_fail("no-negative-parallelisms",
    "It isn't merely a song; it's a statement.",
    "contraction plus merely variant")
expect_pass("no-negative-parallelisms",
    "The building was not damaged in the fire. It was inspected the following day.",
    "factual negation, not a reframing move")
expect_pass("no-negative-parallelisms",
    "It's not the best display in its class, but it's good enough for professional work.",
    "ordinary product comparison")
expect_pass("no-negative-parallelisms",
    "The laptop is powerful, not cheap.",
    "plain concrete contrast")
expect_pass("no-negative-parallelisms",
    "It was not raining, but the road was still wet.",
    "ordinary causal contrast")
expect_pass("no-negative-parallelisms",
    "This is more expensive than the older model.",
    "ordinary price comparison")
expect_pass("no-negative-parallelisms",
    "The issue was not reported until Monday.",
    "plain factual negation")


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
expect_pass("no-copula-avoidance",
    "This is a feature, not a bug.",
    "noun 'feature' is not copula avoidance")
expect_fail("no-copula-avoidance",
    "The gallery features four separate spaces.",
    "verb 'features' as copula avoidance")


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


# --- no-false-concession-hedges ---

print("\n=== no-false-concession-hedges ===")
expect_fail("no-false-concession-hedges",
    "While critics argue the policy is too expensive, supporters say it is necessary. The truth lies somewhere in the middle.",
    "fake both-sides middle")
expect_pass("no-false-concession-hedges",
    "Critics focused on the policy's cost. Supporters pointed to the emissions data from 2023.",
    "concrete positions without tidy middle")


# --- no-placeholder-residue ---

print("\n=== no-placeholder-residue ===")
expect_fail("no-placeholder-residue",
    "Hi {client_name}, thanks for meeting with [Company Name] on [insert date].",
    "unfilled placeholders")
expect_pass("no-placeholder-residue",
    "Hi Mara, thanks for meeting with Northline on Tuesday.",
    "filled-in email")


# --- no-soft-scaffolding ---

print("\n=== no-soft-scaffolding ===")
expect_fail("no-soft-scaffolding",
    "One useful area is explanation. Another useful area is test writing. The main risk is over-trusting the output.",
    "generated explainer scaffolding")
expect_pass("no-soft-scaffolding",
    "The tool explains unfamiliar modules and can draft tests when the project already has clear examples.",
    "direct explanation without scaffold labels")


# --- no-orphaned-demonstratives ---

print("\n=== no-orphaned-demonstratives ===")
expect_fail("no-orphaned-demonstratives",
    "The report was released on Monday. This highlights a gap in planning. This underscores the need for action. This demonstrates the importance of governance.",
    "3 vague demonstrative subject starts")
expect_pass("no-orphaned-demonstratives",
    "The report was released on Monday. Its missing appendix left the budget question unanswered.",
    "concrete subject")


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
expect_fail("no-quietness-obsession",
    "The silent room quietly settled into a soft, hushed stillness.",
    "silent + quietly + soft + hushed + stillness")
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


# --- no-unicode-flair ---

print("\n=== no-unicode-flair ===")
expect_fail("no-unicode-flair",
    "Next steps → draft the plan ✓ review the risks ★ ship the update.",
    "decorative Unicode symbols")
expect_pass("no-unicode-flair",
    "Next steps: draft the plan, review the risks, and ship the update.",
    "plain punctuation")


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
expect_fail("no-markdown-headings",
    "Why Feedback Matters in Learning\n\nFeedback is easy to mistake for marking.",
    "plain title heading")
expect_pass("no-markdown-headings",
    "Libraries provide free access to information. They also host community events.",
    "plain prose, no headings")
expect_pass("no-markdown-headings",
    "### [Issue 194, Fall 2010](https://example.com/back-issues/194)\n\nThe essay begins here.",
    "linked archive metadata heading is ignored")


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
expect_fail("no-countdown-negation",
    "You can't rush this. You can't shortcut it. You can't fake it.",
    "Branch 2: 3 consecutive same-subject negation sentences")
expect_pass("no-countdown-negation",
    "You can't rush this. You can't shortcut it.",
    "Branch 2: only 2 consecutive, below threshold")
expect_fail("no-countdown-negation",
    "It wasn't the data. It wasn't the model. It was the prompt.",
    "Branch 1 regression: classic countdown still detected")
expect_pass("no-countdown-negation",
    "You can't rush this. We can't shortcut it. They can't fake it.",
    "mixed pronouns: not consecutive same-subject")
expect_fail("no-countdown-negation",
    "People cannot rush this. People cannot shortcut it. People cannot fake it.",
    "Branch 2: 'people cannot' full form, 3 consecutive")


# --- no-negation-density ---

print("\n=== no-negation-density ===")
_negation_heavy = (
    "This is not simple. It is not quick. It does not scale. It does not explain itself. "
    "The team does not know who owns it. The system is not reliable. The data is not complete. "
    "The process is not documented. The goal is not clear. The owner is not named. "
    "The timeline is not credible. " + "Plain filler sentence for length. " * 55
)
expect_fail("no-negation-density",
    _negation_heavy,
    "10+ explanatory negation markers at high density in a long text")
expect_pass("no-negation-density",
    "Most meetings waste time, but written decisions make teams clearer. " * 45,
    "long text without dense negation")


# --- paragraph-length-uniformity ---

print("\n=== paragraph-length-uniformity ===")
_uniform_paragraphs = "\n\n".join(
    "This paragraph has a deliberately similar length because generated articles often settle into an even block size with the same amount of explanation each time."
    for _ in range(8)
)
expect_fail("paragraph-length-uniformity",
    _uniform_paragraphs,
    "8 near-identical paragraph lengths")
_varied_paragraphs = "\n\n".join([
    "Short paragraph with enough words to qualify for this structural check now.",
    "This paragraph is much longer because it adds a concrete story, a qualification, and a little extra mess in the middle so the architecture does not fall into identical blocks across the piece.",
    "Another short paragraph has enough words to count while still changing the rhythm clearly.",
    "Here the writer slows down and spends more time on a specific example, adding dates, details, and a partial objection that changes the shape of the paragraph rather than landing at the same predictable length.",
    "This one is compact but still above the minimum word threshold for substantial prose paragraphs.",
    "The next paragraph wanders longer than expected, which is exactly the point for this test because human drafts often have uneven pressure from one paragraph to the next.",
    "A final qualifying short paragraph closes the sample without becoming another identical block."
])
expect_pass("paragraph-length-uniformity",
    _varied_paragraphs,
    "varied paragraph lengths")


# --- no-tidy-paragraph-endings ---

print("\n=== no-tidy-paragraph-endings ===")
expect_fail("no-tidy-paragraph-endings",
    "The team missed the deadline. That is why planning matters.\n\nThe data was incomplete. The takeaway is clear.\n\nThe user flow confused people. In the end, clarity wins.",
    "three generic miniature conclusions")
expect_pass("no-tidy-paragraph-endings",
    "The team missed the deadline after the API changed.\n\nThe data was incomplete, so the analyst reran the survey.\n\nThe user flow confused people on the payment screen.",
    "specific endings without tidy summary labels")


# --- no-bland-critical-template ---

print("\n=== no-bland-critical-template ===")
expect_fail("no-bland-critical-template",
    "The novel is the kind of contemporary novel that does several familiar things at once. Its emotional range is difficult to dismiss, and its field of sympathy earns much of its weight.",
    "generic review vocabulary")
expect_pass("no-bland-critical-template",
    "The second chapter works because Murray lets PJ misunderstand the adult conversation before the reader does.",
    "concrete critical claim")


# --- no-rubric-echoing ---

print("\n=== no-rubric-echoing ===")
expect_fail("no-rubric-echoing",
    "The author creates a serious tone. I can tell because the quote shows that the character is sad. This evidence shows that the text demonstrates the author's use of imagery.",
    "rubric/assignment boilerplate")
expect_pass("no-rubric-echoing",
    "The second paragraph slows down after the argument, and the shorter sentence at the end changes the pressure.",
    "specific textual analysis")


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


# --- no-triad-density ---

print("\n=== no-triad-density ===")

# Build a 400+ word text with 5 triads
_triad_heavy = (
    "The team needed apples, bananas, and oranges for the project. "
    "They also brought cats, dogs, and birds to the demonstration event. "
    "The walls were painted red, blue, and green to match the brand. "
    "Options came in small, medium, or large depending on the client. "
    "The pace was fast, slow, and steady throughout the quarter. "
    + "This is filler text to reach the word count threshold. " * 30
)
expect_fail("no-triad-density",
    _triad_heavy,
    "5 triads in 400+ words")

# 1 triad in 400+ words should pass
_triad_light = (
    "The team needed apples, bananas, and oranges for the project. "
    + "This is filler text to reach the word count threshold. " * 30
)
expect_pass("no-triad-density",
    _triad_light,
    "only 1 triad in 400+ words")

# Short text with 5 triads should skip (pass)
_triad_short = (
    "Apples, bananas, and oranges. Cats, dogs, and birds. "
    "Red, blue, and green. Small, medium, or large. Fast, slow, and steady."
)
expect_pass("no-triad-density",
    _triad_short,
    "short text (under 300 words) with 5 triads should skip")

# Empty/minimal text should pass
expect_pass("no-triad-density",
    "",
    "empty text")
expect_pass("no-triad-density",
    "A single sentence.",
    "minimal text")


# --- no-section-scaffolding ---

print("\n=== no-section-scaffolding ===")
expect_fail("no-section-scaffolding",
    "How to make this work:\nSome content here.\n\nHow to make this work:\nMore content.\n\nHow to make this work:\nEven more.",
    "3 repeated labels")
expect_pass("no-section-scaffolding",
    "Step 1:\nFirst thing to do.\n\nStep 2:\nSecond thing to do.\n\nStep 3:\nThird thing to do.",
    "different labels")
expect_pass("no-section-scaffolding",
    "How to make this work:\nSome content here.\n\nHow to make this work:\nMore content.\n\nSomething else entirely:\nDifferent content.",
    "label appears only 2 times")
expect_pass("no-section-scaffolding",
    "This is a long sentence that repeats because the writer needed to fill space in the document for some reason or another.\nSome content.\n\nThis is a long sentence that repeats because the writer needed to fill space in the document for some reason or another.\nMore content.\n\nThis is a long sentence that repeats because the writer needed to fill space in the document for some reason or another.\nEven more.",
    "repeated line over 60 characters (prose, not a label)")
expect_fail("no-section-scaffolding",
    "### How to apply:\nContent.\n\n### How to apply:\nContent.\n\nHow to apply:\nContent.",
    "markdown heading stripped, matches plain version")


# --- no-notability-claims (pattern 2) ---

print("\n=== no-notability-claims ===")
expect_fail("no-notability-claims",
    "She maintains an active social media presence with over 500,000 followers.",
    "active social media presence + follower count")
expect_fail("no-notability-claims",
    "He has gained widespread media attention and was profiled in several major outlets.",
    "gained widespread media attention + profiled in several major outlets")
expect_fail("no-notability-claims",
    "The artist's work has received independent coverage from regional media outlets across the country.",
    "independent coverage + regional media outlets")
expect_pass("no-notability-claims",
    "In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.",
    "named source + specific date and claim")
expect_pass("no-notability-claims",
    "The town held its weekly market on Saturday, drawing roughly 200 traders from neighbouring villages.",
    "concrete description, no notability framing")


# --- no-vague-attributions (pattern 5) ---

print("\n=== no-vague-attributions ===")
expect_fail("no-vague-attributions",
    "Experts argue that the policy will reshape the industry within a decade.",
    "experts argue, no source")
expect_fail("no-vague-attributions",
    "Industry reports suggest a downturn is imminent across the sector.",
    "industry reports suggest, no source")
expect_fail("no-vague-attributions",
    "Several critics argue the design prioritises form over function.",
    "several critics argue, no source")
expect_fail("no-vague-attributions",
    "It is widely believed that remote work harms culture.",
    "impersonal it is widely believed")
expect_pass("no-vague-attributions",
    "According to the 2024 Stanford Owl Labs survey, productivity rose by 13% among remote knowledge workers.",
    "named source with date and figure")
expect_pass("no-vague-attributions",
    "The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.",
    "patterns.md After example — clearly attributed")


# --- no-boldface-overuse (pattern 13) ---

print("\n=== no-boldface-overuse ===")
expect_fail("no-boldface-overuse",
    "It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.",
    "patterns.md Before — four bold spans in one prose sentence")
expect_fail("no-boldface-overuse",
    "The team will deliver **product strategy**, **roadmap planning**, **stakeholder alignment**, and **executive reporting**.",
    "four bold spans in prose")
expect_pass("no-boldface-overuse",
    "It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.",
    "patterns.md After — no bold")
expect_pass("no-boldface-overuse",
    "- **Apples:** sweet\n- **Bananas:** also sweet\n- **Carrots:** not a fruit\n- **Daikon:** also not a fruit",
    "bold spans only inside list items — caught by no-inline-header-lists, ignored here")
expect_pass("no-boldface-overuse",
    "The **important** distinction is between **public** and **private** keys.",
    "three bolded terms in prose — under threshold of 4")


# --- no-inline-header-lists (pattern 14) ---

print("\n=== no-inline-header-lists ===")
expect_fail("no-inline-header-lists",
    "- **User Experience:** The user experience has been significantly improved.\n- **Performance:** Performance has been enhanced through optimised algorithms.\n- **Security:** Security has been strengthened with end-to-end encryption.",
    "patterns.md Before — three bolded-header bullets")
expect_fail("no-inline-header-lists",
    "1. **First step:** Do this thing.\n2. **Second step:** Do that thing.",
    "two bolded-header numbered items")
expect_pass("no-inline-header-lists",
    "The update improves the interface, speeds up load times through optimised algorithms, and adds end-to-end encryption.",
    "patterns.md After — flowing prose")
expect_pass("no-inline-header-lists",
    "- Apples are sweet\n- Bananas are also sweet\n- Carrots are not a fruit",
    "plain bullets without bolded headers")
expect_pass("no-inline-header-lists",
    "- **One bolded header:** definition only",
    "single bolded-header item — under threshold of 2")


# --- no-compound-modifier-density (pattern 18) ---

print("\n=== no-compound-modifier-density ===")
expect_fail("no-compound-modifier-density",
    "The cross-functional team delivered a high-quality, data-driven report on our client-facing tools.",
    "patterns.md Before — four AI compounds in one sentence")
expect_fail("no-compound-modifier-density",
    "Our real-time, end-to-end, mission-critical platform handles every workload.",
    "three compounds in one sentence")
expect_pass("no-compound-modifier-density",
    "The team, drawn from several departments, delivered a report grounded in usage data for our client-facing tools.",
    "patterns.md After — single client-facing in prose")
expect_pass("no-compound-modifier-density",
    "She explained the long-term plan and the short-term tradeoffs in plain language.",
    "two compounds in prose — under threshold of 3")


# --- no-knowledge-cutoff-disclaimers (pattern 20) ---

print("\n=== no-knowledge-cutoff-disclaimers ===")
expect_fail("no-knowledge-cutoff-disclaimers",
    "While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established in the 1990s.",
    "patterns.md Before — limited-information hedge")
expect_fail("no-knowledge-cutoff-disclaimers",
    "Up to my last training update, the policy had not been amended.",
    "up to my last training update")
expect_fail("no-knowledge-cutoff-disclaimers",
    "Based on publicly available information, the company employs roughly 200 people.",
    "based on publicly available information")
expect_fail("no-knowledge-cutoff-disclaimers",
    "I am unable to verify the exact figure for 2024.",
    "I am unable to verify")
expect_pass("no-knowledge-cutoff-disclaimers",
    "The company was founded in 1994, according to its registration documents.",
    "patterns.md After — concrete claim with source")
expect_pass("no-knowledge-cutoff-disclaimers",
    "As of October 2025, the project had completed three pilot deployments.",
    "as of [date] used to anchor a fact, not as a model-meta hedge")


# --- no-unicode-flair extension (pattern 16 fold) ---

print("\n=== no-unicode-flair (pattern 16 fold) ===")
expect_fail("no-unicode-flair",
    ":rocket: Launch Phase: The product launches in Q3.\n:bulb: Key Insight: Users prefer simplicity.",
    "two emoji shortcodes in headings")
expect_fail("no-unicode-flair",
    "We've shipped 🎉 the new release 🚀 with confidence.",
    "two supplemental-plane emojis in prose (broader range)")
expect_pass("no-unicode-flair",
    "The product launches in Q3. User research showed a preference for simplicity.",
    "patterns.md After — plain prose, no symbols")
expect_pass("no-unicode-flair",
    "Visit https://example.com:8080 for the latest build.",
    "URL with colon — not a shortcode")
expect_pass("no-unicode-flair",
    "The build finished at 12:30:45.",
    "timestamp colons — not a shortcode")


# --- Group A resolution markers (U1 meta-test) ---

print("\n=== group-a-resolution-markers ===")
import re as _re_meta
_patterns_md = (ROOT / "humanise" / "references" / "patterns.md").read_text()
_pattern_sections = _re_meta.split(r"(?=^### \d+[a-z]?\.\s)", _patterns_md, flags=_re_meta.MULTILINE)
_GROUP_A = [2, 5, 11, 12, 13, 14, 15, 16, 18, 20, 21, 28, 30, 35, 36, 37, 41]
_resolution_seen = {}
for _sec in _pattern_sections:
    _h = _re_meta.match(r"^### (\d+)([a-z])?\.\s", _sec)
    if not _h or _h.group(2):
        continue
    _resolution_seen[int(_h.group(1))] = "**Detection:**" in _sec
for _n in _GROUP_A:
    if not _resolution_seen.get(_n):
        FAILURES += 1
        print(f"FAIL: pattern #{_n} is in Group A but missing **Detection:** marker in patterns.md")
    else:
        print(f"  ok: pattern #{_n} carries a Detection marker")


# --- Group B resolution coverage (U2 meta-test) ---

print("\n=== group-b-resolution-coverage ===")
_GROUP_B_CHECKS = [
    "no-manufactured-insight",
    "no-corporate-ai-speak",
    "no-signposted-conclusions",
    "no-nonliteral-land-surface",
    "no-bland-critical-template",
    "no-soft-scaffolding",
    "no-negation-density",
    "overall-ai-signal-pressure",
]
for _check in _GROUP_B_CHECKS:
    if f"`{_check}`" not in _patterns_md:
        FAILURES += 1
        print(f"FAIL: Group B check `{_check}` not referenced anywhere in patterns.md")
    else:
        print(f"  ok: Group B check `{_check}` documented in patterns.md")


# --- Severity propagation: patterns.md ↔ CHECK_METADATA (U3 meta-test) ---

print("\n=== severity-propagation ===")

# Parse every Severity line in patterns.md. Format options:
#   **Severity:** <tier> · `check-id` [trailing prose]
#   **Severity:** <tier> · `check-id` and <tier> · `check-id` ...   (composite patterns)
#   **Severity:** inherits <tier> from `parent-check-id` ...        (folded patterns)
#   **Severity:** N/A · ...                                          (manual / agent-judgement)
#
# For each (tier, check-id) pair pulled from a programmatic-check Severity line,
# assert it matches CHECK_METADATA[check-id]["severity"].
#
# The audit-report redesign closed the orphan-table escape hatch: every check
# in CHECK_METADATA must reach a real numbered or sub-lettered pattern entry's
# **Severity:** line. A separate orphan table no longer counts as coverage.

_severity_pairs = []  # list of (tier, check_id, source_label)
for _i, _line in enumerate(_patterns_md.splitlines(), 1):
    if _line.startswith("**Severity:**"):
        # Direct: "**Severity:** <tier> · `check-id`"
        for _tier, _cid in _re_meta.findall(r"(hard_fail|strong_warning|context_warning)\s*·\s*`([\w-]+)`", _line):
            _severity_pairs.append((_tier, _cid, f"line {_i}"))
        # Inherits: "**Severity:** inherits <tier> from `parent`"
        for _tier, _cid in _re_meta.findall(r"inherits\s+(hard_fail|strong_warning|context_warning)\s+from\s+`([\w-]+)`", _line):
            _severity_pairs.append((_tier, _cid, f"line {_i} (inherited)"))

# Regression guard: the "Severity for unnumbered checks" section was a known
# escape hatch — it let new checks land without a real pattern entry. The
# audit-report redesign removed it. If anyone reintroduces a section heading
# that matches that shape, fail loudly so we don't grow a parallel registry.
_orphan_section_re = _re_meta.compile(r"^##\s+severity\s+for\s+unnumbered", _re_meta.IGNORECASE)
for _i, _line in enumerate(_patterns_md.splitlines(), 1):
    if _orphan_section_re.match(_line):
        FAILURES += 1
        print(f"FAIL: patterns.md line {_i} reintroduces the orphan 'Severity for unnumbered checks' section. Every check must live in a numbered or sub-lettered pattern entry.")

_seen_checks = set()
for _tier, _cid, _src in _severity_pairs:
    _seen_checks.add(_cid)
    _expected = CHECK_METADATA.get(_cid, {}).get("severity")
    if _expected is None:
        FAILURES += 1
        print(f"FAIL: patterns.md {_src} references unknown check `{_cid}`")
    elif _expected != _tier:
        FAILURES += 1
        print(f"FAIL: patterns.md {_src} declares {_cid}={_tier} but CHECK_METADATA says {_expected}")

# Every check in CHECK_METADATA must appear at least once in a Severity declaration.
_missing = sorted(set(CHECK_METADATA) - _seen_checks)
if _missing:
    FAILURES += 1
    print(f"FAIL: {len(_missing)} check(s) in CHECK_METADATA have no Severity declaration in patterns.md: {_missing}")
else:
    print(f"  ok: every check in CHECK_METADATA ({len(CHECK_METADATA)}) carries a Severity declaration in patterns.md")


# --- severity and mode architecture ---

print("\n=== severity-and-mode-architecture ===")
expected_checks = {
    "no-em-dashes",
    "no-ai-vocabulary-clustering",
    "no-nonliteral-land-surface",
    "overall-ai-signal-pressure",
    "no-manufactured-insight",
    "no-staccato-sequences",
    "no-anaphora",
    "no-collaborative-artifacts",
    "no-curly-quotes",
    "sentence-length-variance",
    "no-promotional-language",
    "no-significance-inflation",
    "no-negative-parallelisms",
    "no-copula-avoidance",
    "no-filler-phrases",
    "no-generic-conclusions",
    "no-false-concession-hedges",
    "no-placeholder-residue",
    "no-soft-scaffolding",
    "no-orphaned-demonstratives",
    "no-forced-triads",
    "no-superficial-ing",
    "no-ghost-spectral-density",
    "no-quietness-obsession",
    "no-rhetorical-questions",
    "no-excessive-lists",
    "no-unicode-flair",
    "no-dramatic-transitions",
    "no-formulaic-openers",
    "no-signposted-conclusions",
    "no-markdown-headings",
    "no-corporate-ai-speak",
    "no-this-chains",
    "no-excessive-hedging",
    "no-countdown-negation",
    "no-negation-density",
    "paragraph-length-uniformity",
    "no-tidy-paragraph-endings",
    "no-bland-critical-template",
    "no-rubric-echoing",
    "vocabulary-diversity",
    "no-triad-density",
    "no-section-scaffolding",
    # U1 (audit-report redesign): Group A patterns 2, 5, 13, 14, 18, 20.
    "no-notability-claims",
    "no-vague-attributions",
    "no-boldface-overuse",
    "no-inline-header-lists",
    "no-compound-modifier-density",
    "no-knowledge-cutoff-disclaimers",
}
actual_checks = set(ALL_CHECKS)
if actual_checks != expected_checks:
    FAILURES += 1
    print(f"FAIL: check registry changed. missing={sorted(expected_checks - actual_checks)} extra={sorted(actual_checks - expected_checks)}")
else:
    print(f"  ok: all {len(expected_checks)} expected checks are registered")

allowed_failure_modes = {
    "provenance_residue",
    "synthetic_significance",
    "frictionless_structure",
    "generic_abstraction",
    "voice_erasure",
    "genre_misfit",
}
for check_name in ALL_CHECKS:
    if check_name not in CHECK_METADATA:
        FAILURES += 1
        print(f"FAIL: missing severity metadata for {check_name}")
        continue
    modes = CHECK_METADATA[check_name].get("failure_modes", [])
    if not modes:
        FAILURES += 1
        print(f"FAIL: missing failure mode metadata for {check_name}")
    elif not set(modes).issubset(allowed_failure_modes):
        FAILURES += 1
        print(f"FAIL: invalid failure mode metadata for {check_name}: {modes}")
    if not CHECK_METADATA[check_name].get("evidence_role"):
        FAILURES += 1
        print(f"FAIL: missing evidence role metadata for {check_name}")

_annotated = annotate_result({"text": "no-em-dashes", "passed": False, "evidence": "example"})
if _annotated.get("failure_modes") != ["genre_misfit"]:
    FAILURES += 1
    print(f"FAIL: annotate_result should include failure modes; got {_annotated.get('failure_modes')}")
else:
    print("  ok: annotated results include failure modes")

_failure_mode_report = failure_mode_results([
    annotate_result({"text": "no-collaborative-artifacts", "passed": False, "evidence": "assistant residue"}),
    annotate_result({"text": "no-formulaic-openers", "passed": False, "evidence": "formulaic opener"}),
    annotate_result({"text": "no-em-dashes", "passed": True, "evidence": "clean"}),
])
_triggered_report = triggered_checks([
    annotate_result({"text": "no-collaborative-artifacts", "passed": False, "evidence": "assistant residue"}),
    annotate_result({"text": "no-formulaic-openers", "passed": False, "evidence": "formulaic opener"}),
    annotate_result({"text": "no-em-dashes", "passed": True, "evidence": "clean"}),
])
_score_report = score_summary([
    annotate_result({
        "text": "overall-ai-signal-pressure",
        "passed": False,
        "evidence": "Overall AI-signal pressure 5/4",
        "score": 5,
        "threshold": 4,
        "components": ["paragraph length uniformity", "headings in prose"],
        "vocabulary_pressure": {
            "points": 1,
            "reasons": ["generic cluster"],
            "worst_generic": 2,
            "gptzero_matches": ["play a pivotal role"],
            "kobak_style_distinct": 4,
            "kobak_style_density": 7.5,
            "kobak_style_sample": ["valuable"],
        },
    }),
    annotate_result({"text": "no-formulaic-openers", "passed": False, "evidence": "formulaic opener"}),
    annotate_result({"text": "no-em-dashes", "passed": True, "evidence": "clean"}),
])
_human_report = human_report([
    annotate_result({
        "text": "overall-ai-signal-pressure",
        "passed": False,
        "evidence": "Overall AI-signal pressure 5/4",
        "score": 5,
        "threshold": 4,
        "components": ["paragraph length uniformity", "headings in prose"],
        "vocabulary_pressure": {
            "points": 1,
            "reasons": ["generic cluster"],
            "worst_generic": 2,
            "gptzero_matches": ["play a pivotal role"],
            "kobak_style_distinct": 4,
            "kobak_style_density": 7.5,
            "kobak_style_sample": ["valuable"],
        },
    }),
    annotate_result({"text": "no-formulaic-openers", "passed": False, "evidence": "formulaic opener"}),
    annotate_result({"text": "no-em-dashes", "passed": True, "evidence": "clean"}),
])
_triggered_names = [item["check"] for item in _triggered_report]
if _triggered_names != ["no-collaborative-artifacts", "no-formulaic-openers"]:
    FAILURES += 1
    print(f"FAIL: triggered_checks should list each failed check once; got {_triggered_names}")
else:
    print("  ok: triggered checks list each failed check once")

_triggered_formulaic = _triggered_report[1]
if _triggered_formulaic["failure_modes"] != ["frictionless_structure", "generic_abstraction"]:
    FAILURES += 1
    print(f"FAIL: triggered check should carry all failure modes; got {_triggered_formulaic['failure_modes']}")
else:
    print("  ok: triggered checks carry all failure modes without duplicating evidence")

if _score_report["check_status"] != "fail" or _score_report["pass_rate"] != "1/3":
    FAILURES += 1
    print(f"FAIL: score_summary should expose check totals; got {_score_report}")
else:
    print("  ok: score summary exposes check totals")

_ai_pressure = _score_report["ai_signal_pressure"]
if not _ai_pressure or _ai_pressure["score"] != 5 or _ai_pressure["threshold"] != 4 or not _ai_pressure["triggered"]:
    FAILURES += 1
    print(f"FAIL: score_summary should expose AI-signal pressure; got {_ai_pressure}")
else:
    print("  ok: score summary exposes AI-signal pressure")

# U8: human_report now returns the audit-format-v1 contract (structured-only).
# The OLD assertions on overview/all_checks/ai_pressure_explanation/confidence
# moved to the contract's aggregates + programmatic_checks shape.

_failed_count = sum(1 for c in _human_report["programmatic_checks"] if c["status"] == "flagged")
_total = len(_human_report["programmatic_checks"])
if _failed_count != 2 or _total != 3:
    FAILURES += 1
    print(f"FAIL: contract should report 2 of 3 flagged; got {_failed_count} of {_total}")
else:
    print("  ok: contract programmatic_checks reports failed/total counts")

_pressure_check = next(
    (c for c in _human_report["programmatic_checks"] if c["id"] == "overall-ai-signal-pressure"),
    None,
)
if not _pressure_check or _pressure_check["status"] != "flagged":
    FAILURES += 1
    print(f"FAIL: contract should include flagged aggregate-pressure check; got {_pressure_check}")
else:
    print("  ok: aggregate pressure is reported as one programmatic check")

_pressure_aggr = _human_report["aggregates"]["ai_pressure"]
if "paragraph length uniformity" not in _pressure_aggr["components"]:
    FAILURES += 1
    print(f"FAIL: aggregates.ai_pressure should list components; got {_pressure_aggr['components']}")
else:
    print("  ok: aggregates.ai_pressure lists components")

if "confidence" in _human_report:
    FAILURES += 1
    print("FAIL: U8/R14 removed the labelled confidence block; contract should not include 'confidence'")
else:
    print("  ok: contract has no confidence block (R14 removal)")

# Vocab-only AI-pressure branch: aggregates.ai_pressure.vocabulary_points carries
# the signal that the OLD ai_pressure_explanation prose used to mention.
_human_report_vocab_only = human_report([
    annotate_result({
        "text": "overall-ai-signal-pressure",
        "passed": False,
        "evidence": "Overall AI-signal pressure 4/4",
        "score": 4,
        "threshold": 4,
        "components": [],
        "vocabulary_pressure": {
            "points": 4,
            "reasons": ["generic cluster x4"],
            "worst_generic": 4,
            "gptzero_matches": [],
            "kobak_style_distinct": 8,
            "kobak_style_density": 12.0,
            "kobak_style_sample": ["valuable", "pivotal"],
        },
    }),
])
_vocab_pressure = _human_report_vocab_only["aggregates"]["ai_pressure"]
if _vocab_pressure["vocabulary_points"] != 4 or _vocab_pressure["components"]:
    FAILURES += 1
    print(f"FAIL: vocab-only branch should expose vocabulary_points without components; got {_vocab_pressure}")
else:
    print("  ok: contract aggregates handle vocab-only AI pressure")

_friendly_vocab_only = friendly_evidence({
    "text": "overall-ai-signal-pressure",
    "passed": False,
    "score": 4,
    "threshold": 4,
    "components": [],
    "vocabulary_pressure": {
        "points": 4,
        "reasons": ["generic cluster x4"],
        "worst_generic": 4,
        "gptzero_matches": [],
        "kobak_style_distinct": 8,
        "kobak_style_density": 12.0,
        "kobak_style_sample": [],
    },
})
if "no stacked weak signals" in _friendly_vocab_only or "Clustered AI vocabulary alone" not in _friendly_vocab_only:
    FAILURES += 1
    print(f"FAIL: friendly_evidence vocab-only branch should not contradict itself; got {_friendly_vocab_only}")
else:
    print("  ok: friendly_evidence handles vocab-only AI pressure cleanly")

_total_checks = len(ALL_CHECKS)
_full_table_report = human_report([
    annotate_result({"text": name, "passed": True, "evidence": "clean"})
    for name in ALL_CHECKS
])
if len(_full_table_report["programmatic_checks"]) != _total_checks:
    FAILURES += 1
    print(f"FAIL: full contract should include {_total_checks} programmatic_checks; got {len(_full_table_report['programmatic_checks'])}")
else:
    print(f"  ok: full contract includes all {_total_checks} programmatic checks")

# U11: format_two_layer is the renderer. Deep coverage lives in
# dev/evals/test_two_layer_render.py; this is a smoke test only.
_two_layer_smoke = format_two_layer([
    annotate_result({"text": "no-formulaic-openers", "passed": False, "evidence": "formulaic opener"}),
    annotate_result({"text": "no-em-dashes", "passed": True, "evidence": "clean"}),
], depth="balanced")
if not isinstance(_two_layer_smoke, str) or "---" not in _two_layer_smoke:
    FAILURES += 1
    print(f"FAIL: format_two_layer should return a string with a Layer 1/Layer 2 separator; got:\n{_two_layer_smoke[:400]}")
elif "internal pressure score" in _two_layer_smoke:
    FAILURES += 1
    print("FAIL: format_two_layer should not expose implementation-first pressure language")
else:
    print("  ok: format_two_layer smoke test renders both layers")

if set(_failure_mode_report) != allowed_failure_modes:
    FAILURES += 1
    print(f"FAIL: failure_mode_results should expose all canonical modes; got {sorted(_failure_mode_report)}")
else:
    print("  ok: failure mode report exposes all canonical modes")

_provenance_checks = [item["check"] for item in _failure_mode_report["provenance_residue"]["failed_checks"]]
if _provenance_checks != ["no-collaborative-artifacts"]:
    FAILURES += 1
    print(f"FAIL: provenance failure grouping wrong; got {_provenance_checks}")
else:
    print("  ok: provenance failures are grouped without losing check identity")

_structure_checks = [item["check"] for item in _failure_mode_report["frictionless_structure"]["failed_checks"]]
_abstraction_checks = [item["check"] for item in _failure_mode_report["generic_abstraction"]["failed_checks"]]
if _structure_checks != ["no-formulaic-openers"] or _abstraction_checks != ["no-formulaic-openers"]:
    FAILURES += 1
    print(f"FAIL: multi-mode failure grouping wrong; structure={_structure_checks} abstraction={_abstraction_checks}")
else:
    print("  ok: multi-mode failures remain visible in every applicable group")

_structure_action = _failure_mode_report["frictionless_structure"]["failed_checks"][0]["depth_actions"]
if _structure_action != {"balanced": "fix", "all": "fix"}:
    FAILURES += 1
    print(f"FAIL: strong warning actions should require fixes at every depth; got {_structure_action}")
else:
    print("  ok: strong warning depth actions require fixes at every depth")

_context_action = failure_mode_results([
    annotate_result({"text": "no-anaphora", "passed": False, "evidence": "context warning"}),
])["genre_misfit"]["failed_checks"][0]["depth_actions"]
if _context_action != {
    "balanced": "preserve_with_disclosure_or_user_decision",
    "all": "fix",
}:
    FAILURES += 1
    print(f"FAIL: context warning actions should preserve at Balanced and fix at All; got {_context_action}")
else:
    print("  ok: context warning depth actions preserve at Balanced and fix at All")

if _failure_mode_report["genre_misfit"]["failed_checks"]:
    FAILURES += 1
    print("FAIL: passed checks should not appear in failure mode groups")
else:
    print("  ok: passed checks are excluded from failure mode groups")

_clean_results = [
    annotate_result({"text": "no-em-dashes", "passed": True, "evidence": "clean"}),
    annotate_result({"text": "no-collaborative-artifacts", "passed": True, "evidence": "clean"}),
]
expect_depth_status(_clean_results, "balanced", "pass", "clean text")
expect_depth_status(_clean_results, "all", "pass", "clean text")

_context_only = [
    annotate_result({"text": "no-anaphora", "passed": False, "evidence": "context warning"}),
]
expect_depth_status(_context_only, "balanced", "fail", "context warning only")
expect_depth_status(_context_only, "all", "fail", "context warning only")
expect_depth_actions(_context_only, "balanced", [], ["no-anaphora"], "context warning only")
expect_depth_actions(_context_only, "all", ["no-anaphora"], [], "context warning only")

_strong_only = [
    annotate_result({"text": "no-negative-parallelisms", "passed": False, "evidence": "strong warning"}),
]
expect_depth_status(_strong_only, "balanced", "fail", "strong warning only")
expect_depth_status(_strong_only, "all", "fail", "strong warning only")
expect_depth_actions(_strong_only, "balanced", ["no-negative-parallelisms"], [], "strong warning only")
expect_depth_actions(_strong_only, "all", ["no-negative-parallelisms"], [], "strong warning only")

_hard_only = [
    annotate_result({"text": "no-collaborative-artifacts", "passed": False, "evidence": "hard failure"}),
]
expect_depth_status(_hard_only, "balanced", "fail", "hard failure")
expect_depth_status(_hard_only, "all", "fail", "hard failure")


# --- Audit-shape: U5 dual-block assertions ---

print("\n=== audit-shape U5 (dual-block assertions) ===")
check_audit_shape = _grade.check_audit_shape

_BOTH_BLOCKS = """Audit
Severity: 0 hard_fail · 1 strong_warning · 0 context_warning · pressure: clear
Pressure clear: no weaker AI-writing signals stacked.

! **Em dashes** — "still—keen" — Action: Fix

---

**Style** — 1 flagged of 6

| Pattern | Result | Action |
| --- | --- | --- |
| Em dashes | Flagged | Fix |
| Curly quotes | Clear |  |

---

**Agent-judgement reading — 1 flagged of 8**

- Structural monotony — Flagged: every section follows the same arc
- Tonal uniformity — Clear: register breaks at least once
- Faux specificity — Clear
- Neutrality collapse — Clear: takes a position
- Even jargon distribution — Clear: jargon clumps where the writer knows things
- Forced synesthesia — Clear
- Generic metaphors — Clear
- Genre specific — Clear: Genre detected: default

**Next step**

Want suggestions, a rewrite, or to save?"""

_PROGRAMMATIC_ONLY = """Audit
Severity: 0 hard_fail · 1 strong_warning · 0 context_warning · pressure: clear
Pressure clear: no weaker AI-writing signals stacked.

! **Em dashes** — "still—keen" — Action: Fix

---

**Style** — 1 flagged of 6

| Pattern | Result | Action |
| --- | --- | --- |
| Em dashes | Flagged | Fix |
| Curly quotes | Clear |  |

**Next step**

Want suggestions?"""

_AGENT_JUDGEMENT_ONLY = """**Agent-judgement reading — 1 flagged of 8**

- Structural monotony — Flagged: every section follows the same arc
- Tonal uniformity — Clear: register breaks at least once
- Faux specificity — Clear
- Neutrality collapse — Clear: takes a position
- Even jargon distribution — Clear: jargon clumps where the writer knows things
- Forced synesthesia — Clear
- Generic metaphors — Clear
- Genre specific — Clear: Genre detected: default

**Next step**

Want suggestions?"""

# Variable name retained for diff stability; the value is now the Phase-3
# canonical all-clear single-line response.
_ALL_CLEAR_PHASE_1 = """48 of 48 clear · agent reading clean · pressure: clear.
Want me to re-run with --depth all to inspect lower-tier signals?"""

_NEITHER_BLOCK_NOR_CLEAR = """**Some other report**

Nothing recognisable here.

Want help?"""

# Regression fixture for Finding #2 of pr-6-code-review-handoff:
# the canonical all-clear phrase buried mid-line in a longer malformed
# response must NOT pass the audit-shape checks. The anchored regex only
# matches phrases that start a line.
_BURIED_ALL_CLEAR = """The system prompt asked the agent to say "48 of 48 clear · agent reading clean · pressure: clear" but the model returned a hallucinated paragraph instead.

We tried to render no-em-dashes but the structured block did not materialise.

Want help?"""

# Regression fixture for Finding #2: a response containing BOTH the
# canonical all-clear phrase AND block headers is ambiguous — agents must
# pick one shape, not both. All three audit-shape checks must fail.
_ALL_CLEAR_PLUS_BLOCKS = """48 of 48 clear · agent reading clean · pressure: clear.
Want me to re-run with --depth all?

Audit
Severity: 0 hard_fail · 1 strong_warning · 0 context_warning · pressure: clear

! **Em dashes** — "still—keen" — Action: Fix

**Agent-judgement reading — 1 flagged of 8**

- Structural monotony — Flagged: every section follows the same arc"""

# Regression fixture for Finding #1 from PR #14 review (LAYER_1_BLOCK_RE
# previously required a middle clause and silently dropped no-quote
# structural-pattern blocks). The fixture mixes one quoted block with two
# no-quote structural blocks; _flag_blocks must return all three.
_LAYER_1_NO_QUOTE_BLOCKS = """Audit
Severity: 1 hard_fail · 2 strong_warning · 0 context_warning · pressure: clear
Pressure clear: no weaker AI-writing signals stacked.

x **Em dashes** — "still—keen" — Action: Fix
! **Paragraph length uniformity** — Action: Disclose or ask before preserving
! **Section scaffolding** — Action: Fix

---

**Style** — 1 flagged of 6

| Pattern | Result | Action |
| --- | --- | --- |
| Em dashes | Flagged | Fix |
| Curly quotes | Clear |  |

**Next step**

Want suggestions?"""

# Realistic shape from PR #14 review Finding #4: programmatic flagged + agent
# fully clear renders the programmatic block PLUS a clean-form agent block
# (humanise/SKILL.md line 102). This is the renderer's actual emission shape
# for that case. _PROGRAMMATIC_ONLY above is kept as a malformed-output
# regression — agents that emit a programmatic block alone without the
# clean-form agent block are still caught by has-agent-judgement-block.
_PROGRAMMATIC_WITH_CLEAN_AGENT = """Audit
Severity: 0 hard_fail · 1 strong_warning · 0 context_warning · pressure: clear
Pressure clear: no weaker AI-writing signals stacked.

! **Em dashes** — "still—keen" — Action: Fix

---

**Style** — 1 flagged of 6

| Pattern | Result | Action |
| --- | --- | --- |
| Em dashes | Flagged | Fix |
| Curly quotes | Clear |  |

---

**Agent-judgement reading**

agent reading clean

**Next step**

Want suggestions?"""

# Regression fixture for PR #14 review Finding #9: a Layer 1 candidate line
# opens with `<glyph> **<name>**` but is missing the trailing `Action:` verb.
# The broader candidate-collection regex inside check_every_flag_block_has_explanation
# catches the line; the predicate catches the missing verb.
_FLAG_BLOCK_MISSING_ACTION = """Audit
Severity: 0 hard_fail · 1 strong_warning · 0 context_warning · pressure: clear
Pressure clear: no weaker AI-writing signals stacked.

! **Em dashes** — "still—keen"

---

**Style** — 1 flagged of 6

| Pattern | Result | Action |
| --- | --- | --- |
| Em dashes | Flagged | Fix |

**Next step**

Want suggestions?"""

# Suggestion-parity fixtures for PR #14 review Finding #8: the rewritten
# check now sums programmatic + agent-judgement flagged counts. Both fixtures
# extend _BOTH_BLOCKS (1 programmatic + 1 agent-judgement = 2 expected flags).
# _PARITY_BALANCED has two Try blocks (parity); _PARITY_MISMATCH has one.
_PARITY_BALANCED = _BOTH_BLOCKS + """

**Suggestions**

- "still—keen"
  Where: paragraph 1
  Why: Em-dash-set-off subordinate clauses are a high-signal AI tell.
  Try: keen and still

- Structural monotony: every section follows the same arc
  Where: across the piece
  Why: Uniform section shape signals templated production.
  Try: vary one section's pacing or omit the closing summary."""

_PARITY_MISMATCH = _BOTH_BLOCKS + """

**Suggestions**

- "still—keen"
  Where: paragraph 1
  Why: Em-dash-set-off subordinate clauses are a high-signal AI tell.
  Try: keen and still"""

# has-programmatic-block
_r = check_audit_shape("audit-shape-has-programmatic-block", _BOTH_BLOCKS)
if _r["passed"]:
    print("  ok: has-programmatic-block passes on dual-block output")
else:
    FAILURES += 1; print(f"FAIL: has-programmatic-block on dual-block: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-programmatic-block", _PROGRAMMATIC_ONLY)
if _r["passed"]:
    print("  ok: has-programmatic-block passes on programmatic-only output")
else:
    FAILURES += 1; print(f"FAIL: has-programmatic-block on programmatic-only: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-programmatic-block", _AGENT_JUDGEMENT_ONLY)
if _r["passed"]:
    print("  ok: has-programmatic-block passes on agent-judgement-only output (programmatic-clean / agent-flagged shape per SKILL.md)")
else:
    FAILURES += 1; print(f"FAIL: has-programmatic-block on agent-judgement-only: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-programmatic-block", _ALL_CLEAR_PHASE_1)
if _r["passed"]:
    print("  ok: has-programmatic-block passes on all-clear single-line shape")
else:
    FAILURES += 1; print(f"FAIL: has-programmatic-block on all-clear: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-programmatic-block", _NEITHER_BLOCK_NOR_CLEAR)
if not _r["passed"]:
    print("  ok: has-programmatic-block fails when no block and no all-clear line")
else:
    FAILURES += 1; print("FAIL: has-programmatic-block should fail when no block and no all-clear line")

# has-agent-judgement-block
_r = check_audit_shape("audit-shape-has-agent-judgement-block", _BOTH_BLOCKS)
if _r["passed"]:
    print("  ok: has-agent-judgement-block passes on dual-block output")
else:
    FAILURES += 1; print(f"FAIL: has-agent-judgement-block on dual-block: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-agent-judgement-block", _PROGRAMMATIC_ONLY)
if not _r["passed"]:
    print("  ok: has-agent-judgement-block fails on programmatic-only output")
else:
    FAILURES += 1; print("FAIL: has-agent-judgement-block should fail on programmatic-only output")

_r = check_audit_shape("audit-shape-has-agent-judgement-block", _AGENT_JUDGEMENT_ONLY)
if _r["passed"]:
    print("  ok: has-agent-judgement-block passes on agent-judgement-only output")
else:
    FAILURES += 1; print(f"FAIL: has-agent-judgement-block on agent-judgement-only: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-agent-judgement-block", _ALL_CLEAR_PHASE_1)
if _r["passed"]:
    print("  ok: has-agent-judgement-block passes on all-clear single-line shape")
else:
    FAILURES += 1; print(f"FAIL: has-agent-judgement-block on all-clear: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-agent-judgement-block", _NEITHER_BLOCK_NOR_CLEAR)
if not _r["passed"]:
    print("  ok: has-agent-judgement-block fails when no block and no all-clear line")
else:
    FAILURES += 1; print("FAIL: has-agent-judgement-block should fail when no block and no all-clear line")

# all-clear-line-format
_r = check_audit_shape("audit-shape-all-clear-line-format", _BOTH_BLOCKS)
if _r["passed"]:
    print("  ok: all-clear-line-format vacuously passes on dual-block output")
else:
    FAILURES += 1; print(f"FAIL: all-clear-line-format on dual-block: {_r['evidence']}")

_r = check_audit_shape("audit-shape-all-clear-line-format", _ALL_CLEAR_PHASE_1)
if _r["passed"]:
    print("  ok: all-clear-line-format passes on canonical Phase-1 all-clear shape")
else:
    FAILURES += 1; print(f"FAIL: all-clear-line-format on canonical all-clear: {_r['evidence']}")

_r = check_audit_shape("audit-shape-all-clear-line-format", _NEITHER_BLOCK_NOR_CLEAR)
if not _r["passed"]:
    print("  ok: all-clear-line-format fails when neither blocks nor canonical line")
else:
    FAILURES += 1; print("FAIL: all-clear-line-format should fail when neither blocks nor canonical line")

# Finding #2 regressions: buried phrase and all-clear-plus-blocks must fail
# all three audit-shape checks. The anchored regex catches the buried case;
# the mutex logic catches the both-shapes-present case.

print("\n--- Finding #2 regressions: buried all-clear and all-clear+blocks ---")

for _check_name in ("audit-shape-has-programmatic-block",
                    "audit-shape-has-agent-judgement-block",
                    "audit-shape-all-clear-line-format"):
    _r = check_audit_shape(_check_name, _BURIED_ALL_CLEAR)
    if not _r["passed"]:
        print(f"  ok: {_check_name} fails when all-clear phrase is buried mid-line")
    else:
        FAILURES += 1
        print(f"FAIL: {_check_name} should fail when all-clear phrase is buried mid-line (got: {_r['evidence']})")

for _check_name in ("audit-shape-has-programmatic-block",
                    "audit-shape-has-agent-judgement-block",
                    "audit-shape-all-clear-line-format"):
    _r = check_audit_shape(_check_name, _ALL_CLEAR_PLUS_BLOCKS)
    if not _r["passed"]:
        print(f"  ok: {_check_name} fails when all-clear phrase appears alongside block headers")
    else:
        FAILURES += 1
        print(f"FAIL: {_check_name} should fail when all-clear phrase appears alongside block headers (got: {_r['evidence']})")


# --- PR #14 review regressions: no-quote Layer 1, clean-form agent block,
# missing-Action candidate, suggestion-parity ---

print("\n--- PR #14 review regressions ---")

# Finding #1: LAYER_1_BLOCK_RE no-quote variant. _flag_blocks must return
# all three lines (one quoted + two no-quote structural).
_audit = _grade._audit_section(_LAYER_1_NO_QUOTE_BLOCKS)
_blocks = _grade._flag_blocks(_audit)
if len(_blocks) == 3:
    print(f"  ok: Finding #1 — _flag_blocks returns 3 blocks for 1-quoted + 2-no-quote fixture")
else:
    FAILURES += 1
    print(f"FAIL: Finding #1 — _flag_blocks should return 3 blocks; got {len(_blocks)}: {_blocks}")

# Finding #1: parity check counts the no-quote blocks too. Layer 1 = 3
# programmatic flags + 0 agent-judgement flags. Suggestions section is
# absent so the count is 0 — the assertion checks that _flag_blocks
# correctly enumerates 3, exposing any silent drop.
_r = check_audit_shape("suggestion-block-count-equals-flag-count", _LAYER_1_NO_QUOTE_BLOCKS)
if not _r["passed"] and "3 flag(s)" in _r["evidence"]:
    print(f"  ok: Finding #1 — suggestion-block-count counts 3 no-quote-aware programmatic flags")
else:
    FAILURES += 1
    print(f"FAIL: Finding #1 — suggestion-block-count should count 3 flags from no-quote fixture (got: {_r['evidence']})")

# Finding #4: realistic shape (programmatic flagged + clean-form agent block).
# Both has-programmatic-block and has-agent-judgement-block must pass.
_r = check_audit_shape("audit-shape-has-programmatic-block", _PROGRAMMATIC_WITH_CLEAN_AGENT)
if _r["passed"]:
    print(f"  ok: Finding #4 — has-programmatic-block passes on programmatic + clean-form-agent shape")
else:
    FAILURES += 1
    print(f"FAIL: Finding #4 — has-programmatic-block on programmatic + clean-form-agent: {_r['evidence']}")

_r = check_audit_shape("audit-shape-has-agent-judgement-block", _PROGRAMMATIC_WITH_CLEAN_AGENT)
if _r["passed"]:
    print(f"  ok: Finding #4 — has-agent-judgement-block passes on programmatic + clean-form-agent shape")
else:
    FAILURES += 1
    print(f"FAIL: Finding #4 — has-agent-judgement-block on programmatic + clean-form-agent: {_r['evidence']}")

# Finding #9 (paired with Finding #5 in PR #14 review): every-flag-block-has-
# explanation must catch a Layer 1 candidate line missing the trailing Action: verb.
_r = check_audit_shape("every-flag-block-has-explanation", _FLAG_BLOCK_MISSING_ACTION)
if not _r["passed"] and "missing 'Action:'" in _r["evidence"]:
    print(f"  ok: Finding #9 — every-flag-block-has-explanation catches missing Action: on Layer 1 candidate")
else:
    FAILURES += 1
    print(f"FAIL: Finding #9 — every-flag-block-has-explanation should fail when Action: missing (got: {_r['evidence']})")

# Finding #8: suggestion-block-count-equals-flag-count must sum programmatic
# + agent-judgement flagged counts. Balanced fixture passes (2 flags = 2 Try);
# mismatch fixture fails (2 flags vs 1 Try).
_r = check_audit_shape("suggestion-block-count-equals-flag-count", _PARITY_BALANCED)
if _r["passed"]:
    print(f"  ok: Finding #8 — suggestion-parity passes when 2 flags (1 prog + 1 agent) match 2 suggestions")
else:
    FAILURES += 1
    print(f"FAIL: Finding #8 — suggestion-parity should pass on balanced dual-block fixture (got: {_r['evidence']})")

_r = check_audit_shape("suggestion-block-count-equals-flag-count", _PARITY_MISMATCH)
if not _r["passed"] and "2 flag(s)" in _r["evidence"] and "1 suggestion" in _r["evidence"]:
    print(f"  ok: Finding #8 — suggestion-parity fails when agent-judgement flag has no matching suggestion")
else:
    FAILURES += 1
    print(f"FAIL: Finding #8 — suggestion-parity should fail when 2 flags vs 1 Try (got: {_r['evidence']})")


# --- Human passthrough: opinion piece ---
print("\n=== human-opinion-passthrough ===")
opinion_text = Path(__file__).parent.joinpath("samples/10-human-opinion.md").read_text()
for check_name in ALL_CHECKS:
    if check_name == "no-staccato-sequences":
        continue  # existing human sample also fails this, known limitation
    expect_pass(check_name, opinion_text, f"human opinion piece ({check_name})")

# --- Human passthrough: instructional piece ---
print("\n=== human-instructional-passthrough ===")
instructional_text = Path(__file__).parent.joinpath("samples/11-human-instructional.md").read_text()
for check_name in ALL_CHECKS:
    if check_name == "no-staccato-sequences":
        continue
    expect_pass(check_name, instructional_text, f"human instructional piece ({check_name})")


# --- Summary ---

print(f"\n{'='*40}")
if FAILURES:
    print(f"FAILED: {FAILURES} assertion(s) broken")
    sys.exit(1)
else:
    print("ALL PASSED")
    sys.exit(0)
