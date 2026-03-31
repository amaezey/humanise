#!/usr/bin/env python3
"""Grade humanised text against programmatic assertions."""

import json
import re
import sys
from pathlib import Path
from statistics import stdev


# --- Pattern lists ---

AI_VOCABULARY = [
    "additionally", "crucial", "delve", "emphasizing",
    "enduring", "enhance", "fostering", "garner", "interplay",
    "intricate", "intricacies", "landscape", "pivotal", "showcase",
    "showcasing", "tapestry", "testament", "underscore", "underscoring",
    "valuable", "vibrant", "foster", "highlighting",
    # Added from Grammarly research
    "realm", "harness", "illuminate", "facilitate", "bolster",
    "streamline", "shed light on", "revolutionize", "innovative",
    "cutting-edge", "game-changing", "transformative", "seamlessly",
    # Added from user observations
    "genuinely", "unspoken",
]

# Multi-word phrases where the first word may be inflected (e.g. "align with" ->
# "aligns with", "aligned with"). Checked via regex, not substring.
AI_VOCABULARY_REGEX = [
    r"aligns? with\b",
    r"aligned with\b",
    r"aligning with\b",
]

# Broad set: catches both the obvious ("let that sink in") and the subtler
# framing moves ("the reason is straightforward", "what's strange is")
MANUFACTURED_INSIGHT = [
    # False revelation
    r"what's really", r"the real answer", r"here's what's really",
    r"the real story is", r"what's actually happening",
    # Contrived contrarianism
    r"what nobody is talking about", r"what no one seems to realize",
    r"contrary to popular belief", r"the uncomfortable truth",
    r"what gets lost in the conversation", r"what most people miss",
    # Performed knowingness
    r"let that sink in", r"read that again", r"if you know,? you know",
    r"and that changes everything", r"which tells you everything",
    r"and that's the point", r"and honestly\??",
    # Pseudo-profundity
    r"quietly revolutionary", r"quietly becoming", r"the quiet part",
    # Formulaic depth framing
    r"what's strange is", r"what's interesting is", r"what's remarkable is",
    r"the reason is straightforward", r"the reason is simple",
    r"here's the thing:?", r"here's why:?", r"but here's",
    # "The real X?" rhetorical revelation
    r"the real (?:insight|challenge|takeaway|kicker|question)\??",
    # Performed revelation closings
    r"a (?:quiet|powerful|important|profound) lesson",
    r"a (?:quiet|powerful|important|profound) reminder",
    r"sometimes the (?:bravest|hardest|most important)",
    # Contrived contrast as insight
    r"this isn't [\w\s]+\. it's ",
    r"that's not [\w\s]+\. that's ",
]

COLLABORATIVE_ARTIFACTS = [
    r"\bi hope this helps", r"\bgreat question", r"\blet me know",
    r"\bhere is a\b", r"\bwould you like", r"\bcertainly!",
    r"\bof course!", r"\byou're absolutely right",
    # Soft offer-to-continue variants
    r"if needed,?\s+(?:I can|the .* can be|this can be)\b",
    r"if (?:you'd like|you need|you want),?\s+I can\b",
    r"\bfeel free to\b", r"\bdon't hesitate to\b",
]

PROMOTIONAL = [
    "breathtaking", "stunning", "nestled", "profound",
    "showcasing", "exemplifies", "must-visit", "groundbreaking",
    "renowned",
]

SIGNIFICANCE_INFLATION = [
    "pivotal", "crucial", "vital role", "testament",
    "evolving landscape", "indelible mark", "key turning point",
    "deeply rooted", "setting the stage", "remarkably",
    "strikingly", "staggering",
]

COPULA_AVOIDANCE = [
    r"serves? as\b", r"stands? as\b", r"functions? as\b",
    r"marks? a\b", r"represents? a\b",
    r"boasts?\b", r"features?\b(?! film| movie| documentary)",
]

FILLER_PHRASES = [
    r"in order to\b", r"due to the fact that",
    r"at this point in time", r"it is important to note",
    r"it is worth noting", r"it is worth (?:recognising|mentioning|emphasising|highlighting|acknowledging)",
    r"it should be noted",
    r"has the ability to", r"in the event that",
    r"on the whole", r"at the end of the day",
    r"when all is said and done", r"the fact of the matter",
    r"is often framed as\b", r"is often (?:seen|viewed|regarded|described|characterized) as\b",
]

GENERIC_CONCLUSIONS = [
    r"the future looks bright", r"exciting times",
    r"continue (?:this|their|our) journey",
    r"a? ?step in the right direction",
    r"remains to be seen",
]


# --- Utility ---

def split_sentences(text):
    """Split text into sentences (rough but usable)."""
    text = re.sub(r'\n+', ' ', text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def count_pattern_matches(text, patterns):
    """Count total matches of regex patterns in text (case-insensitive)."""
    text_lower = text.lower()
    total = 0
    matches = []
    for pat in patterns:
        found = re.findall(pat, text_lower)
        if found:
            total += len(found)
            matches.extend(found)
    return total, matches


# --- Checks ---

def check_em_dashes(text):
    count = text.count('\u2014')
    return {
        "text": "no-em-dashes",
        "passed": count == 0,
        "evidence": f"Found {count} em dash(es)" if count > 0 else "No em dashes found",
    }


def _find_ai_words(text_lower):
    """Find AI vocabulary in text, including inflected multi-word phrases."""
    found = [w for w in AI_VOCABULARY if w in text_lower]
    for pat in AI_VOCABULARY_REGEX:
        if re.search(pat, text_lower):
            found.append(re.search(pat, text_lower).group())
    return found


def check_ai_vocabulary(text):
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    max_count = 0
    worst_words = []
    for para in paragraphs:
        para_lower = para.lower()
        found = _find_ai_words(para_lower)
        if len(found) > max_count:
            max_count = len(found)
            worst_words = found
    # Also report total count across the whole text
    text_lower = text.lower()
    total = len(_find_ai_words(text_lower))
    return {
        "text": "no-ai-vocabulary-clustering",
        "passed": max_count < 3,
        "evidence": (
            f"Worst paragraph has {max_count} AI words: {worst_words} ({total} total in text)"
            if max_count >= 3
            else f"Max AI words per paragraph: {max_count} ({total} total in text)"
        ),
    }


def check_manufactured_insight(text):
    count, matches = count_pattern_matches(text, MANUFACTURED_INSIGHT)
    return {
        "text": "no-manufactured-insight",
        "passed": count == 0,
        "evidence": f"Found {count}: {matches}" if count > 0 else "No manufactured insight phrases",
    }


def check_staccato(text):
    sentences = split_sentences(text)
    max_run = 0
    current_run = 0
    for s in sentences:
        words = len(s.split())
        if words < 6:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 0
    return {
        "text": "no-staccato-sequences",
        "passed": max_run < 3,
        "evidence": (
            f"Found sequence of {max_run} consecutive short sentences"
            if max_run >= 3
            else f"Max consecutive short sentences: {max_run}"
        ),
    }


def check_anaphora(text):
    """Detect 3+ consecutive sentences starting with the same word/phrase."""
    sentences = split_sentences(text)
    if len(sentences) < 3:
        return {
            "text": "no-anaphora",
            "passed": True,
            "evidence": "Too few sentences to check",
        }
    max_run = 1
    current_run = 1
    worst_word = ""
    for i in range(1, len(sentences)):
        prev_start = sentences[i - 1].split()[0].lower() if sentences[i - 1].split() else ""
        curr_start = sentences[i].split()[0].lower() if sentences[i].split() else ""
        if prev_start == curr_start and prev_start not in ("i", "a", "the", "it's", "it"):
            current_run += 1
            if current_run > max_run:
                max_run = current_run
                worst_word = curr_start
        else:
            current_run = 1
    return {
        "text": "no-anaphora",
        "passed": max_run < 3,
        "evidence": (
            f"Found {max_run} consecutive sentences starting with '{worst_word}'"
            if max_run >= 3
            else f"Max anaphora run: {max_run}"
        ),
    }


def check_collaborative_artifacts(text):
    count, matches = count_pattern_matches(text, COLLABORATIVE_ARTIFACTS)
    return {
        "text": "no-collaborative-artifacts",
        "passed": count == 0,
        "evidence": f"Found: {matches}" if count > 0 else "No collaborative artifacts",
    }


def check_curly_quotes(text):
    curly = ['\u201c', '\u201d', '\u2018', '\u2019']
    count = sum(text.count(c) for c in curly)
    return {
        "text": "no-curly-quotes",
        "passed": count == 0,
        "evidence": f"Found {count} curly quote(s)" if count > 0 else "No curly quotes",
    }


def check_sentence_variance(text):
    sentences = split_sentences(text)
    if len(sentences) < 3:
        return {
            "text": "sentence-length-variance",
            "passed": False,
            "evidence": "Too few sentences to measure variance",
        }
    lengths = [len(s.split()) for s in sentences]
    sd = stdev(lengths)
    return {
        "text": "sentence-length-variance",
        "passed": sd > 4,
        "evidence": f"Sentence length stdev: {sd:.1f} (target: >4)",
    }


def check_promotional(text):
    text_lower = text.lower()
    found = [w for w in PROMOTIONAL if w in text_lower]
    return {
        "text": "no-promotional-language",
        "passed": len(found) == 0,
        "evidence": f"Found: {found}" if found else "No promotional language",
    }


def check_significance_inflation(text):
    text_lower = text.lower()
    found = [w for w in SIGNIFICANCE_INFLATION if w in text_lower]
    return {
        "text": "no-significance-inflation",
        "passed": len(found) == 0,
        "evidence": f"Found: {found}" if found else "No significance inflation",
    }


def check_negative_parallelisms(text):
    patterns = [r"not just\b.*?\bbut\b", r"not only\b.*?\bbut also\b",
                r"it's not about\b.*?\bit's about\b",
                r"it's not [\w\s]+[;,] it's\b",
                # Cross-sentence "not X. It is Y" reframing
                r"not (?:about|just about) [\w\s]+\.\s+it is (?:about|a\b)",
                r"is less about\b.*?\bthan (?:about )?\b",
                r"is not [\w\s]+but\b",
                ]
    count, matches = count_pattern_matches(text, patterns)
    return {
        "text": "no-negative-parallelisms",
        "passed": count == 0,
        "evidence": f"Found {count} negative parallelism(s)" if count > 0 else "No negative parallelisms",
    }


def check_copula_avoidance(text):
    count, matches = count_pattern_matches(text, COPULA_AVOIDANCE)
    return {
        "text": "no-copula-avoidance",
        "passed": count == 0,
        "evidence": f"Found {count}: {matches}" if count > 0 else "No copula avoidance",
    }


def check_filler_phrases(text):
    count, matches = count_pattern_matches(text, FILLER_PHRASES)
    return {
        "text": "no-filler-phrases",
        "passed": count == 0,
        "evidence": f"Found {count}: {matches}" if count > 0 else "No filler phrases",
    }


def check_generic_conclusions(text):
    count, matches = count_pattern_matches(text, GENERIC_CONCLUSIONS)
    return {
        "text": "no-generic-conclusions",
        "passed": count == 0,
        "evidence": f"Found {count}: {matches}" if count > 0 else "No generic conclusions",
    }


def check_rule_of_three(text):
    """Detect forced triads: 'X, Y, and Z' patterns that cluster heavily."""
    # Find all "A, B, and C" patterns where all three are abstract nouns
    # Suffixes: -ing, -tion, -sion, -ment, -ness, -ity, -ity, -nce, -ncy, -cy, -ism, -ity
    _abs = r'\b\w+(?:ing|tion|sion|ment|ness|ity|ence|ance|ency|ancy|cy|ism)\b'
    pattern = rf'({_abs}), ({_abs}),? and ({_abs})'
    matches = re.findall(pattern, text.lower())
    count = len(matches)
    return {
        "text": "no-forced-triads",
        "passed": count == 0,
        "evidence": (
            f"Found {count} abstract triad(s): {[', '.join(m) for m in matches]}"
            if count > 0
            else "No forced triads"
        ),
    }


def check_superficial_ing(text):
    """Detect sentences ending with tacked-on -ing phrases (pattern 3)."""
    pattern = r',\s+(?:highlighting|underscoring|emphasizing|reflecting|symbolizing|contributing to|cultivating|fostering|encompassing|showcasing|ensuring|demonstrating|illustrating|reinforcing|signaling|representing)\b[^.]*\.'
    matches = re.findall(pattern, text.lower())
    count = len(matches)
    return {
        "text": "no-superficial-ing",
        "passed": count == 0,
        "evidence": (
            f"Found {count} tacked-on -ing phrase(s)"
            if count > 0
            else "No superficial -ing phrases"
        ),
    }


def check_ghost_spectral(text):
    """Detect ghost/spectral language density (pattern 26)."""
    words = ["ghost", "ghosts", "spectral", "shadow", "shadows", "whisper",
             "whispers", "echo", "echoes", "phantom", "haunting", "haunted",
             "lingering", "remnant", "remnants", "unspoken", "hidden"]
    text_lower = text.lower()
    found = [w for w in words if w in text_lower]
    count = sum(text_lower.count(w) for w in found)
    return {
        "text": "no-ghost-spectral-density",
        "passed": count < 3,
        "evidence": (
            f"Found {count} ghost/spectral words: {found}"
            if count >= 3
            else f"Ghost/spectral words: {count}"
        ),
    }


def check_quietness(text):
    """Detect quietness obsession density (pattern 27)."""
    words = ["quiet", "quietly", "softly", "stillness", "hushed",
             "murmur", "gentle", "tender", "settled"]
    text_lower = text.lower()
    count = sum(text_lower.count(w) for w in words)
    # Allow some usage. Flag at 4+ in a piece, which suggests obsession.
    word_count = len(text_lower.split())
    density = count / max(word_count, 1) * 1000  # per 1000 words
    return {
        "text": "no-quietness-obsession",
        "passed": count < 4,
        "evidence": (
            f"Found {count} quietness words ({density:.1f} per 1000 words)"
            if count >= 4
            else f"Quietness words: {count}"
        ),
    }


def check_rhetorical_questions(text):
    """Detect mid-sentence rhetorical questions (pattern 29)."""
    # Pattern: short question (under 8 words) followed by a declarative answer
    pattern = r'[.!]\s+([^.?!]{3,50}\?)\s+(?:It\'?s?|They\'re|You|We|The|This|That|And)\b'
    matches = re.findall(pattern, text)
    count = len(matches)
    return {
        "text": "no-rhetorical-questions",
        "passed": count < 2,
        "evidence": (
            f"Found {count} mid-sentence rhetorical question(s): {matches[:3]}"
            if count >= 2
            else f"Rhetorical questions: {count}"
        ),
    }


def check_list_density(text):
    """Detect excessive list-making (pattern 31)."""
    lines = text.strip().split('\n')
    bullet_lines = sum(1 for line in lines if re.match(r'\s*[-*]\s', line) or re.match(r'\s*\d+\.\s', line))
    total_lines = max(len(lines), 1)
    ratio = bullet_lines / total_lines
    return {
        "text": "no-excessive-lists",
        "passed": ratio < 0.3,
        "evidence": (
            f"List ratio: {ratio:.0%} ({bullet_lines}/{total_lines} lines are bullets)"
            if ratio >= 0.3
            else f"List ratio: {ratio:.0%}"
        ),
    }


def check_dramatic_transitions(text):
    """Detect dramatic narrative transitions (pattern 32)."""
    patterns = [
        r"something shifted", r"everything changed", r"everything clicked",
        r"that's when it hit me", r"and that made all the difference",
        r"that changed everything", r"nothing was the same",
        r"the beginning of everything", r"the real turning point",
    ]
    count, matches = count_pattern_matches(text, patterns)
    return {
        "text": "no-dramatic-transitions",
        "passed": count == 0,
        "evidence": (
            f"Found {count}: {matches}"
            if count > 0
            else "No dramatic transitions"
        ),
    }


# --- Registry ---

ALL_CHECKS = {
    "no-em-dashes": check_em_dashes,
    "no-ai-vocabulary-clustering": check_ai_vocabulary,
    "no-manufactured-insight": check_manufactured_insight,
    "no-staccato-sequences": check_staccato,
    "no-anaphora": check_anaphora,
    "no-collaborative-artifacts": check_collaborative_artifacts,
    "no-curly-quotes": check_curly_quotes,
    "sentence-length-variance": check_sentence_variance,
    "no-promotional-language": check_promotional,
    "no-significance-inflation": check_significance_inflation,
    "no-negative-parallelisms": check_negative_parallelisms,
    "no-copula-avoidance": check_copula_avoidance,
    "no-filler-phrases": check_filler_phrases,
    "no-generic-conclusions": check_generic_conclusions,
    "no-forced-triads": check_rule_of_three,
    "no-superficial-ing": check_superficial_ing,
    "no-ghost-spectral-density": check_ghost_spectral,
    "no-quietness-obsession": check_quietness,
    "no-rhetorical-questions": check_rhetorical_questions,
    "no-excessive-lists": check_list_density,
    "no-dramatic-transitions": check_dramatic_transitions,
}


def grade_file(filepath, assertion_names=None):
    """Grade a file against specified assertions (or all if none specified)."""
    text = Path(filepath).read_text()
    results = []
    checks_to_run = assertion_names or ALL_CHECKS.keys()
    for name in checks_to_run:
        if name in ALL_CHECKS:
            results.append(ALL_CHECKS[name](text))
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: grade.py <file> [assertion1,assertion2,...]")
        sys.exit(1)

    filepath = sys.argv[1]
    assertions = sys.argv[2].split(",") if len(sys.argv) > 2 else None

    results = grade_file(filepath, assertions)

    passed = sum(1 for r in results if r["passed"])
    total = len(results)

    output = {
        "file": filepath,
        "pass_rate": f"{passed}/{total}",
        "expectations": results,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
