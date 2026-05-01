#!/usr/bin/env python3
"""Grade humanised text against programmatic assertions."""

import csv
import ast
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
    "genuinely", "unspoken", "seamless",
    # Added from April 2026 research (Nature biomedical study, practitioner guides)
    "unparalleled", "invaluable", "bolstered", "meticulous",
    # Added from Vollmer/GPTZero reference audit
    "mosaic", "ecosystem", "symphony", "labyrinth", "beacon",
    "cornerstone", "bedrock", "kaleidoscope", "odyssey", "robust",
    "dynamic", "comprehensive", "multifaceted", "nuanced", "holistic",
    "state-of-the-art", "ever-evolving", "ever-changing", "utilize",
    "optimize", "empower", "navigate", "unpack", "explore", "embrace",
    "unlock", "commendable", "paramount", "unwavering", "alignment",
    "resonate", "compelling",
]

# GPTZero's April 2026 public AI Vocabulary table exposes 100 high-ratio
# phrases. Treat them as tentative clustering signals, not single-phrase proof.
GPTZERO_AI_PHRASES = [
    "provide a valuable insight",
    "left an indelible mark",
    "a stark reminder",
    "a nuanced understanding",
    "significant role in shaping",
    "the complex interplay",
    "broad implication",
    "an unwavering commitment",
    "endure a legacy",
    "underscore the importance",
    "play a pivotal role",
    "a pivotal moment",
    "navigate the complex",
    "mark a turning point",
    "continue to inspire",
    "gain a deeper understanding",
    "the transformative power",
    "hold a significant",
    "play a crucial role",
    "particularly a concern",
    "the relentless pursuit",
    "emphasize the need",
    "target an intervention",
    "a multi-faceted approach",
    "a serf reminder",
    "highlight the potential",
    "a significant milestone",
    "implication to understand",
    "potential risk associated",
    "leave a lasting",
    "add a layer",
    "offer a valuable",
    "a profound implication",
    "case highlights the importance",
    "finding a highlight of the importance",
    "pave the way for the future",
    "a significant step forward",
    "face a significant",
    "finding an important implication",
    "emphasize the importance",
    "a significant implication",
    "delve deeper into",
    "reply in tone",
    "raise an important question",
    "make an informed decision in regard to",
    "far-reaching implications",
    "a comprehensive framework",
    "importance to consider",
    "a unique blend",
    "couldn't help but wonder",
    "underscore the need",
    "framework for understanding",
    "highlight the need",
    "a comprehensive understanding",
    "the journey begins",
    "understanding the fundamental",
    "despite the face",
    "a delicate balance",
    "the path ahead",
    "gain an insight",
    "laid the groundwork",
    "understand the behavior",
    "renew a sense",
    "aim to explore",
    "present a unique challenge",
    "provide a comprehensive",
    "particularly with regard to",
    "address the root cause",
    "loom large in",
    "the implication of the finding",
    "approach ensures a",
    "an ongoing dialogue",
    "carry a weight",
    "ability to navigate",
    "present a significant",
    "study shed light on",
    "a diverse perspective",
    "face an adversity",
    "a comprehensive overview",
    "potentially lead to",
    "a broad understanding",
    "contribute to the understanding",
    "shape the public",
    "particularly noteworthy",
    "the evidence base for decision making",
    "identify an area of improvement",
    "analysis of the data to analyze and use",
    "undergone a significant",
    "need a robust",
    "voice will fill",
    "concern a potential",
    "initiative aims to",
    "offering a unique",
    "a new avenue",
    "despite the challenge",
    "ready to embrace",
    "the societal expectation",
    "make accessible",
    "today at a fast pace",
    "stand in stark contrast",
]

KOBAK_EXCESS_WORDS_PATH = "kobak-excess-words.csv"
KOBAK_IGNORED_STYLE_POS = {"preposition", "pronoun", "pronoun/adverb", "particle"}
KOBAK_IGNORED_STYLE_WORDS = {"were", "based", "background", "like", "this", "their", "these"}
BIOMEDICAL_DOMAIN_TERMS = {
    "abstract", "abstracts", "acute", "antiviral", "biomedical", "biomarker",
    "biomarkers", "cancer", "cell", "cells", "clinical", "clinically",
    "cohort", "coronavirus", "covid", "diagnosis", "diagnostic", "disease",
    "diseases", "drug", "drugs", "gene", "genes", "genome", "genomic",
    "hospital", "hospitalized", "intervention", "mortality", "oncology",
    "patient", "patients", "placebo", "pneumonia", "protein", "proteins",
    "pubmed", "randomized", "sars", "therapeutic", "therapeutics", "therapy",
    "treatment", "treatments", "trial", "tumor", "tumors", "tumour",
    "tumours", "vaccine", "vaccination", "ventilation", "ventilator",
    "ventilators",
}


def _load_kobak_excess_vocab():
    """Load Kobak et al. excess-vocabulary annotations from the skill data file."""
    here = Path(__file__).resolve()
    candidates = [
        here.parent / "references" / KOBAK_EXCESS_WORDS_PATH,
        here.parents[2] / "humanise" / "references" / KOBAK_EXCESS_WORDS_PATH,
    ]
    for path in candidates:
        if path.exists():
            with path.open(newline="", encoding="utf-8") as f:
                rows = []
                for row in csv.DictReader(f):
                    word = row.get("word", "").strip().lower()
                    if word:
                        rows.append({
                            "word": word,
                            "type": row.get("type", "").strip().lower(),
                            "part_of_speech": row.get("part_of_speech", "").strip().lower(),
                        })
                return rows
    return []


KOBAK_EXCESS_VOCAB = _load_kobak_excess_vocab()
KOBAK_STYLE_WORDS = {
    row["word"]
    for row in KOBAK_EXCESS_VOCAB
    if "style" in row["type"]
    and row["part_of_speech"] not in KOBAK_IGNORED_STYLE_POS
    and row["word"] not in KOBAK_IGNORED_STYLE_WORDS
}
KOBAK_CONTENT_WORDS = {
    row["word"]
    for row in KOBAK_EXCESS_VOCAB
    if "content" in row["type"]
}

# Multi-word phrases where the first word may be inflected (e.g. "align with" ->
# "aligns with", "aligned with"). Checked via regex, not substring.
AI_VOCABULARY_REGEX = [
    r"aligns? with\b",
    r"aligned with\b",
    r"aligning with\b",
    # "actually" as filler intensifier (not "actually happened", "actually did")
    r"\bactually[,.]",
    r"\band actually\b",
    r"\bbut actually\b",
    # "land/lands" as metaphor for reception (not physical land)
    r"\bhow (?:it|that|this) lands?\b",
    r"\bhow (?:it|that|this) landed\b",
    r"\blands? (?:well|differently|flat|poorly|awkwardly)\b",
    r"\blanded (?:well|differently|flat|poorly|awkwardly)\b",
    r"\bthe way (?:it|that|this) lands?\b",
    r"\bthe way (?:it|that|this) landed\b",
    # "surface" as metaphor for appearing/becoming visible, not physical surface
    r"\bsurfaces? as\b",
    r"\bsurfaces? in (?:the|a|our|their) (?:conversation|discussion|debate|work|writing|text|story|essay|analysis|response)\b",
    r"\bsurfaced as\b",
    r"\bsurfaced in (?:the|a|our|their) (?:conversation|discussion|debate|work|writing|text|story|essay|analysis|response)\b",
    r"\bwhat surfaces?\b",
    r"\bwhen (?:it|this|that) surfaces?\b",
    # "hidden" when inflating significance of the ordinary
    r"\bhidden (?:truth|depth|meaning|complexity|beauty|power|gem|lesson|cost)\b",
    # "move/moves" as meta-rhetoric about writing/argument (not literal motion)
    r"\bthe move (?:here|there|above|below|in this|in that) is\b",
    r"\b(?:rhetorical|framing|writerly|literary|narrative|familiar|signature|telling|classic|clever|bold|cheap|risky) moves?\b",
    r"\b(?:make|makes|making|made) (?:this|that|the same|a similar|an opposite) move\b",
    r"\bwatch(?:ing)? (?:the writer|the author|him|her|them) make (?:a|this|that) move\b",
]

NONLITERAL_LAND_SURFACE = [
    r"\b(?:argument|claim|point|idea|thinking|analysis|story|piece|draft|sentence|paragraph|message|feedback|critique|comment|line|joke|scene|ending)\s+lands?\b",
    r"\b(?:argument|claim|point|idea|thinking|analysis|story|piece|draft|sentence|paragraph|message|feedback|critique|comment|line|joke|scene|ending)\s+landed\b",
    r"\bwhere (?:my|your|his|her|their|our|the)?\s*(?:argument|claim|point|idea|thinking|analysis|story|piece|draft|sentence|paragraph|message|feedback|critique|comment|line|scene|ending)\s+landed\b",
    r"\b(?:argument|claim|point|idea|thinking|analysis|story|piece|piece of work|student work|draft|paper|essay|grade|mark|score|sentence|paragraph|message|feedback|critique|comment|line|scene|ending)\s+landed (?:in|on|with|against) (?:the |a |an )?(?:mark scheme|marking scale|scoring system|rubric|scale|spectrum|ranking|assessment|category|argument|discussion|conversation|draft|analysis|process)\b",
    r"\bwhere (?:i|you|we|they|he|she|it)\s+landed (?:in|on|with|against) (?:the |a |an )?(?:mark scheme|marking scale|scoring system|rubric|scale|spectrum|ranking|assessment|category|argument|discussion|conversation|draft|analysis|process)\b",
    r"\blands? with (?:the )?(?:reader|readers|audience|user|users|team|client|stakeholders)\b",
    r"\bsurfaces? in (?:the|a|our|their) (?:conversation|discussion|debate|work|writing|text|story|essay|analysis|response|draft|argument)\b",
    r"\bsurfaced in (?:the|a|our|their) (?:conversation|discussion|debate|work|writing|text|story|essay|analysis|response|draft|argument)\b",
    r"\bwhat surfaces?\b",
    r"\bwhat surfaced\b",
]

# Broad set: catches both the obvious ("let that sink in") and the subtler
# framing moves ("the reason is straightforward", "what's strange is")
MANUFACTURED_INSIGHT = [
    # False revelation
    r"what's really", r"the real answer", r"here's what's really",
    r"the real story is", r"what's actually happening",
    # Contrived contrarianism
    r"what nobody is talking about", r"what no one seems to realize",
    r"what no one is talking about", r"what nobody seems to realize",
    r"contrary to popular belief", r"the uncomfortable truth",
    r"what gets lost in the conversation", r"what most people miss",
    r"what (?:no one|nobody) noticed", r"the shift (?:no one|nobody) noticed",
    r"when (?:no one|nobody) noticed", r"while (?:no one|nobody) noticed",
    r"before anyone noticed", r"without anyone noticing",
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
    # Performed candour / honesty framing
    # (Folded into manufactured insight for now — see #42 Hypothesis note in patterns.md
    # for the promotion criteria if this cluster grows.)
    r"the honest answer is",
    r"here's the honest (?:answer|framing|truth|version|take|story)",
    r"here's the (?:real )?truth\b",
    r"the real truth is",
    r"if i'm being honest",
    r"in all honesty",
    r"to be (?:perfectly )?honest,",
]

COLLABORATIVE_ARTIFACTS = [
    r"\bi hope this helps", r"\bgreat question", r"\bhere is a\b",
    r"\bwould you like (?:me|us) to\b", r"\bcertainly!",
    r"\byou're absolutely right",
    r"\bwhat a thoughtful (?:question|observation)\b",
    r"\bthat's a brilliant observation\b",
    r"\bi'd be happy to help\b", r"\blet me explain\b",
    r"\blet's break it down\b", r"\blet's unpack\b",
    # Soft offer-to-continue variants
    r"\blet me know (?:if|whether|what|when|how)\b",
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
    r"boasts?\b", r"features\b(?! film| movie| documentary)",
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
    r"\boverall,\s+(?:this|the|these|it)\b",
    r"\bremember,\s+when\b",
    r"\bas we navigate\b",
    r"\bthe journey (?:doesn't|does not) end here\b",
]

SOFT_SCAFFOLD_PHRASES = [
    r"\bone useful (?:area|way|approach|thing|strategy|habit)\b",
    r"\banother useful (?:area|way|approach|thing|strategy|habit)\b",
    r"\bthe main (?:strength|risk|benefit|challenge|advantage|drawback)\b",
    r"\bgood use usually comes down to\b",
    r"\bcomes down to (?:giving|using|making|keeping|knowing|understanding)\b",
    r"\bthis can be (?:helpful|useful|valuable|effective)\b",
    r"\bcan (?:be|also be) (?:helpful|useful|valuable|effective) when\b",
    r"\bespecially (?:helpful|useful|valuable|effective) when\b",
    r"\bin those cases,\b",
    r"\bwith (?:that|this) distinction in mind\b",
]

BLAND_CRITICAL_TEMPLATE = [
    r"\bthe kind of (?:contemporary )?(?:novel|film|book|album|show|essay) that\b",
    r"\bdoing several familiar things at once\b",
    r"\bwhat makes (?:the|this|it)\b.{0,80}\bmore than\b",
    r"\bemotional range\b",
    r"\bfield of sympathy\b",
    r"\bmoral strengths?\b",
    r"\bearns? (?:much of )?its weight\b",
    r"\bambitious in an old-fashioned way\b",
    r"\bsocial texture\b",
    r"\bslow revelation of\b",
    r"\bdifficult to dismiss\b",
]

TIDY_PARAGRAPH_ENDINGS = [
    r"\bthat is what makes\b",
    r"\bthat is why\b",
    r"\bthis is why\b",
    r"\bthe takeaway is\b",
    r"\bthe lesson is\b",
    r"\bthe result is\b",
    r"\bwhat matters is\b",
    r"\bin the end,",
    r"\bultimately,",
    r"\bused with (?:care|that distinction in mind)\b",
    r"\bwith (?:that|this) distinction in mind\b",
    r"\bwithout becoming\b",
]

FALSE_CONCESSION_PATTERNS = [
    r"\bwhile (?:critics|skeptics|some) (?:argue|say|claim|contend)\b.{0,160}\b(?:supporters|proponents|others) (?:argue|say|claim|maintain|counter)\b",
    r"\b(?:supporters|proponents) (?:argue|say|claim|maintain)\b.{0,160}\bwhile (?:critics|skeptics|others) (?:argue|say|claim|contend)\b",
    r"\bthe truth,?\s+as is often the case,?\s+lies somewhere in between\b",
    r"\bthe truth (?:lies|is) somewhere in (?:the )?middle\b",
    r"\bwhile this may vary\b.{0,120}\b(?:generally speaking|in most cases|it is worth noting)\b",
]

ORPHANED_DEMONSTRATIVE_VERBS = [
    "highlights", "underscores", "demonstrates", "illustrates", "reflects",
    "suggests", "creates", "shows", "reveals", "emphasizes", "reinforces",
    "points to", "speaks to", "allows", "enables",
]

PLACEHOLDER_PATTERNS = [
    r"\{[a-z0-9_ -]{2,40}\}",
    r"\[(?:insert|add|describe|include|client|company|name|title|date|source|citation)[^\]]{0,50}\]",
    r"<(?:client|company|name|title|date|source|citation)[^>]{0,40}>",
    r"\bhi\s+\{[^}]+\}",
    r"\bdear\s+\[(?:name|client|recipient)[^\]]*\]",
]

RUBRIC_ECHO_PATTERNS = [
    r"\bthe author creates? a .{0,50} tone\b",
    r"\bi can tell because\b",
    r"\bin paragraph (?:one|two|three|four|five|\d+)\b",
    r"\bthis (?:quote|evidence) shows that\b",
    r"\bthe (?:text|passage|essay) demonstrates (?:the author's )?(?:use|understanding|ability)\b",
    r"\baccording to the rubric\b",
    r"\bmeets? the criteria\b",
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


def normalize_for_regex(text):
    """Normalize punctuation variants that agents use to dodge phrase checks."""
    return (
        text.lower()
        .replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .replace("\u2014", " - ")
        .replace("\u2013", " - ")
    )


def word_counts(text):
    """Return lowercase word counts for exact vocabulary-set matching."""
    counts = {}
    for token in re.findall(r"\b[a-z][a-z0-9-]*\b", normalize_for_regex(text)):
        counts[token] = counts.get(token, 0) + 1
    return counts


def strip_front_matter(text):
    """Remove YAML front matter from markdown fixtures before prose checks."""
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            return parts[1]
    return text


def prose_paragraphs(text):
    """Return prose-like paragraphs, excluding fixture metadata and headings."""
    text = strip_front_matter(text)
    paragraphs = []
    for para in re.split(r"\n\s*\n", text):
        stripped = para.strip()
        if not stripped:
            continue
        lines = [
            line.strip()
            for line in stripped.splitlines()
            if not re.match(r"^#{1,6}\s+", line.strip())
        ]
        joined = " ".join(line for line in lines if line)
        if joined:
            paragraphs.append(joined)
    return paragraphs


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
    normalized = normalize_for_regex(text_lower)
    found = [w for w in AI_VOCABULARY if w in normalized]
    found.extend([w for w in GPTZERO_AI_PHRASES if w in normalized])
    for pat in AI_VOCABULARY_REGEX:
        if re.search(pat, normalized):
            found.append(re.search(pat, normalized).group())
    return found


def vocabulary_pressure_profile(text):
    """Score vocabulary evidence as one aggregate pressure signal."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    worst_generic = 0
    worst_words = []
    for para in paragraphs:
        found = _find_ai_words(para.lower())
        if len(found) > worst_generic:
            worst_generic = len(found)
            worst_words = found

    normalized = normalize_for_regex(text)
    gptzero_matches = [phrase for phrase in GPTZERO_AI_PHRASES if phrase in normalized]
    kobak = kobak_excess_profile(text)

    points = 0
    reasons = []
    if worst_generic >= 4:
        points += 2
        reasons.append(f"generic_cluster={worst_generic}")
    elif worst_generic >= 2:
        points += 1
        reasons.append(f"generic_cluster={worst_generic}")

    if len(gptzero_matches) >= 2:
        points += 1
        reasons.append(f"gptzero_phrases={len(gptzero_matches)}")

    if kobak["available"]:
        if kobak["style_distinct"] >= 25 and kobak["style_density"] >= 35:
            points += 2
            reasons.append(
                f"kobak_style={kobak['style_distinct']} distinct/{kobak['style_density']:.1f}"
            )
        elif kobak["style_distinct"] >= 12 and kobak["style_density"] >= 20:
            points += 1
            reasons.append(
                f"kobak_style={kobak['style_distinct']} distinct/{kobak['style_density']:.1f}"
            )

    return {
        "points": min(points, 4),
        "reasons": reasons,
        "worst_generic": worst_generic,
        "worst_words": worst_words,
        "gptzero_matches": gptzero_matches[:8],
        "kobak": kobak,
    }


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


def check_nonliteral_land_surface(text):
    """Detect land/surface used as generic discourse metaphors."""
    matches = []
    for pattern in NONLITERAL_LAND_SURFACE:
        matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    return {
        "text": "no-nonliteral-land-surface",
        "passed": len(matches) == 0,
        "evidence": (
            f"Found {len(matches)} nonliteral land/surface construction(s): {matches[:5]}"
            if matches
            else "No nonliteral land/surface constructions found"
        ),
    }


def kobak_excess_profile(text):
    """Return Kobak et al. excess-vocabulary evidence without deciding failure."""
    if not KOBAK_EXCESS_VOCAB:
        return {
            "available": False,
            "style_count": 0,
            "style_distinct": 0,
            "style_density": 0.0,
            "biomedical_count": 0,
            "content_count": 0,
            "style_sample": [],
            "biomedical_sample": [],
            "content_sample": [],
        }

    counts = word_counts(text)
    total_words = sum(counts.values())
    style_matches = {w: counts[w] for w in KOBAK_STYLE_WORDS if counts.get(w)}
    content_matches = {w: counts[w] for w in KOBAK_CONTENT_WORDS if counts.get(w)}
    biomedical_matches = {w: counts[w] for w in BIOMEDICAL_DOMAIN_TERMS if counts.get(w)}
    style_count = sum(style_matches.values())
    content_count = sum(content_matches.values())
    biomedical_count = sum(biomedical_matches.values())
    style_density = style_count / max(total_words, 1) * 1000

    style_sample = sorted(style_matches, key=lambda w: (-style_matches[w], w))[:10]
    content_sample = sorted(content_matches, key=lambda w: (-content_matches[w], w))[:8]
    biomedical_sample = sorted(
        biomedical_matches,
        key=lambda w: (-biomedical_matches[w], w),
    )[:8]
    return {
        "available": True,
        "style_count": style_count,
        "style_distinct": len(style_matches),
        "style_density": style_density,
        "biomedical_count": biomedical_count,
        "content_count": content_count,
        "style_sample": style_sample,
        "biomedical_sample": biomedical_sample,
        "content_sample": content_sample,
    }


def check_overall_signal_pressure(text):
    """Aggregate multiple weak/medium signals instead of overreacting to one list."""
    checks = {
        "manufactured_insight": check_manufactured_insight(text),
        "negative_parallelism": check_negative_parallelisms(text),
        "formulaic_openers": check_formulaic_openers(text),
        "soft_scaffolding": check_soft_scaffolding(text),
        "section_scaffolding": check_section_scaffolding(text),
        "tidy_endings": check_tidy_paragraph_endings(text),
        "paragraph_uniformity": check_paragraph_uniformity(text),
        "markdown_headings": check_markdown_headings(text),
        "excessive_lists": check_list_density(text),
        "collaborative_artifacts": check_collaborative_artifacts(text),
        "generic_conclusions": check_generic_conclusions(text),
        "bland_critical_template": check_bland_critical_template(text),
        "false_concession": check_false_concession(text),
    }
    weights = {
        "manufactured_insight": 2,
        "negative_parallelism": 2,
        "formulaic_openers": 1,
        "soft_scaffolding": 1,
        "section_scaffolding": 1,
        "tidy_endings": 1,
        "paragraph_uniformity": 2,
        "markdown_headings": 2,
        "excessive_lists": 1,
        "collaborative_artifacts": 2,
        "generic_conclusions": 2,
        "bland_critical_template": 1,
        "false_concession": 1,
    }
    component_labels = {
        "manufactured_insight": "manufactured insight framing",
        "negative_parallelism": "contrived contrast framing",
        "formulaic_openers": "formulaic openings",
        "soft_scaffolding": "soft scaffolding",
        "section_scaffolding": "section scaffolding",
        "tidy_endings": "tidy paragraph endings",
        "paragraph_uniformity": "paragraph length uniformity",
        "markdown_headings": "headings in prose",
        "excessive_lists": "excessive lists",
        "collaborative_artifacts": "assistant residue",
        "generic_conclusions": "generic conclusion endings",
        "bland_critical_template": "bland critical template",
        "false_concession": "false-concession hedges",
    }
    assert set(weights) <= set(component_labels), (
        f"component_labels missing keys: {sorted(set(weights) - set(component_labels))}"
    )

    vocab = vocabulary_pressure_profile(text)
    score = vocab["points"]
    components = []
    for name, result in checks.items():
        if not result["passed"]:
            score += weights[name]
            components.append(component_labels[name])

    failed = score >= 4
    return {
        "text": "overall-ai-signal-pressure",
        "passed": not failed,
        "score": score,
        "threshold": 4,
        "components": components,
        "vocabulary_pressure": {
            "points": vocab["points"],
            "reasons": vocab["reasons"],
            "worst_generic": vocab["worst_generic"],
            "gptzero_matches": vocab["gptzero_matches"],
            "kobak_style_distinct": vocab["kobak"]["style_distinct"],
            "kobak_style_density": vocab["kobak"]["style_density"],
            "kobak_style_sample": vocab["kobak"]["style_sample"],
        },
        "evidence": (
            f"Overall AI-signal pressure {score}/4 from [{', '.join(components)}]; "
            f"vocab={vocab['points']} point(s), "
            f"worst_generic={vocab['worst_generic']}, "
            f"gptzero={vocab['gptzero_matches']}, "
            f"kobak={vocab['kobak']['style_distinct']} distinct/"
            f"{vocab['kobak']['style_density']:.1f}/1000, "
            f"sample={vocab['kobak']['style_sample']}"
            if failed
            else (
                f"Overall AI-signal pressure {score}/4 from [{', '.join(components)}]; "
                f"vocab={vocab['points']} point(s), "
                f"worst_generic={vocab['worst_generic']}, "
                f"gptzero={vocab['gptzero_matches']}, "
                f"kobak={vocab['kobak']['style_distinct']} distinct/"
                f"{vocab['kobak']['style_density']:.1f}/1000"
            )
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
    word_count = len(text.split())
    # Skip for short-form text where low variance is expected, not an AI tell
    if len(sentences) < 6 and word_count < 100:
        return {
            "text": "sentence-length-variance",
            "passed": True,
            "evidence": f"Skipped: short text ({word_count} words, {len(sentences)} sentences)",
        }
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
    normalized = normalize_for_regex(text)
    subject = r"(?:it|this|that|the (?:point|question|problem|goal|story|work|piece|tool|song|film|book|app|product|value))"
    neg = r"(?:not|isn't|is not|wasn't|was not|aren't|are not|isnt|wasnt|arent)"
    soft = r"(?:just|only|merely|simply|really|actually|about|a matter of|a question of|a story of)"
    abstract = (
        r"(?:meaning|identity|dignity|human|humanity|connection|creativity|"
        r"trust|belonging|agency|purpose|truth|memory|resilience|empathy|"
        r"transformation|possibility|culture|power|relationship|experience|"
        r"what matters|what it means|reclaiming|unlocking|reminder|lesson|"
        r"journey|conversation|negotiation|reflection|statement|capability)"
    )

    hard_patterns = [
        # Canonical forms and their obvious lexical variants.
        r"\bnot\s+(?:just|only|merely|simply|about|a matter of|a question of|a story of)\b.{0,120}\bbut(?: also)?\b",
        r"\b(?:isn't|is not|wasn't|was not|aren't|are not|isnt|wasnt|arent)\s+(?:just|only|merely|simply|about|a matter of|a question of|a story of)\b.{0,120}\bbut(?: also)?\b",
        rf"\bnot\s+so\s+much\b.{{0,120}}\bas\b",
        rf"\b{subject}\s+{neg}\s+{soft}\s+.{{0,120}}[;:,\-]\s+(?:it's|that's|this is|it is|that is|it was|that was|this was|it becomes?|that becomes?|this becomes?)\b",
        rf"\b{subject}\s+{neg}\s+.{{0,120}}[;:,\-]\s+(?:it's|that's|this is|it is|that is|it was|that was|this was|it becomes?|that becomes?|this becomes?)\b[^.!?\n]{{0,120}}\b{abstract}\b",
        # Cross-sentence "not X. It is Y" reframing.
        rf"\b{neg}\s+(?:(?:just|only|merely|simply)\s+)?about\b.{{0,120}}[.!?]\s+(?:it|this|that)\s+(?:is|was|becomes?)\s+about\b[^.!?\n]{{0,120}}\b{abstract}\b",
        # Comparative reframes.
        r"\b(?:is|are|was|were|becomes?)\s+less\s+about\b.{0,120}\bthan\s+(?:about\s+)?",
        r"\b(?:is|are|was|were|becomes?)\s+more\s+about\b.{0,120}\bthan\s+(?:about\s+)?",
        r"\b(?:is|are|was|were|becomes?)\s+(?:less|more)\s+a\b.{0,120}\bthan\s+a\b",
        # Explicit countdown negation in miniature.
        r"\bno\s+[^.!?\n]{1,50}[.!?]\s+no\s+[^.!?\n]{1,50}[.!?]\s+just\s+",
        r"\bnot\s+[^.!?\n]{1,50}[.!?]\s+not\s+[^.!?\n]{1,50}[.!?]\s+just\s+",
        # "You thought X; actually Y" keeps the same fake revelation.
        r"\b(?:you might think|at first glance|on the surface|it may seem)\b.{0,120}\b(?:but|yet|actually|in reality)\b",
    ]

    abstract_reframe_patterns = [
        # Reversed order: "Y, not X" where Y is inflated abstraction.
        rf"\b(?:is|are|was|were|becomes?|means?)\b[^.!?\n]{{0,90}}\b{abstract}\b[^.!?\n]{{0,80}},?\s+(?:rather than|instead of|not)\b",
        rf"\b(?:a|an|the)\s+(?:question|matter|story|lesson|reminder|act|gesture|exercise|conversation|negotiation|reflection)\s+of\s+{abstract}\b[^.!?\n]{{0,80}},?\s+(?:rather than|instead of|not)\b",
        # "Beyond X, it is Y" / "More than X, it is Y".
        rf"\b(?:beyond|more than|larger than|deeper than)\b[^.!?\n]{{1,80}},?\s+(?:{subject}\s+)?(?:is|was|becomes?|means?)\b[^.!?\n]{{0,90}}\b{abstract}\b",
        # Correction moves that reveal an inflated abstract payload.
        rf"\b(?:actually|in reality|the real (?:point|story|question|issue|challenge) is)\b[^.!?\n]{{0,120}}\b{abstract}\b",
    ]

    matches = []
    for pat in hard_patterns + abstract_reframe_patterns:
        matches.extend(re.findall(pat, normalized, flags=re.IGNORECASE | re.DOTALL))
    count = len(matches)
    return {
        "text": "no-negative-parallelisms",
        "passed": count == 0,
        "evidence": (
            f"Found {count} contrived contrast/reframe pattern(s)"
            if count > 0
            else "No negative parallelisms or contrived reframes"
        ),
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


def check_false_concession(text):
    """Detect fake both-sides nuance that lands in a tidy middle."""
    count, matches = count_pattern_matches(text, FALSE_CONCESSION_PATTERNS)
    return {
        "text": "no-false-concession-hedges",
        "passed": count == 0,
        "evidence": (
            f"Found {count} false concession pattern(s): {matches[:3]}"
            if count > 0
            else "No false concession hedges"
        ),
    }


def check_placeholder_residue(text):
    """Detect unfilled template placeholders in generated prose/email."""
    count, matches = count_pattern_matches(text, PLACEHOLDER_PATTERNS)
    return {
        "text": "no-placeholder-residue",
        "passed": count == 0,
        "evidence": (
            f"Found {count} placeholder(s): {matches[:5]}"
            if count > 0
            else "No placeholder residue"
        ),
    }


def check_soft_scaffolding(text):
    """Detect bland transition scaffolding from generated explainers."""
    count, matches = count_pattern_matches(text, SOFT_SCAFFOLD_PHRASES)
    return {
        "text": "no-soft-scaffolding",
        "passed": count < 2,
        "evidence": (
            f"Found {count} soft scaffold phrase(s): {matches[:6]}"
            if count >= 2
            else f"Soft scaffold phrases: {count}"
        ),
    }


def check_orphaned_demonstratives(text):
    """Detect repeated vague 'This/That highlights...' subject starts."""
    pattern = (
        r"\b(?:this|that|these|those)\s+(?:"
        + "|".join(re.escape(v) for v in ORPHANED_DEMONSTRATIVE_VERBS)
        + r")\b"
    )
    count, matches = count_pattern_matches(text, [pattern])
    return {
        "text": "no-orphaned-demonstratives",
        "passed": count < 3,
        "evidence": (
            f"Found {count} vague demonstrative subject(s): {matches[:6]}"
            if count >= 3
            else f"Vague demonstrative subjects: {count}"
        ),
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
    words = ["quiet", "quietly", "silent", "silently", "softly", "stillness", "hushed",
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


def check_unicode_flair(text):
    """Detect decorative Unicode symbols and emoji shortcodes (patterns 31a + 16).

    Folds pattern 16 (Emojis) into this check: covers symbol glyphs, the
    broader emoji ranges, and ``:shortcode:`` forms (``:rocket:``, ``:bulb:``)
    that cluster in headings or bullet points.
    """
    symbols = re.findall(
        r"[✓✔✕✖★☆◆◇→⇒➜➤•●○◦※✨⭐✅❌🔥🚀]"
        r"|[\U0001F300-\U0001F9FF\U0001FA00-\U0001FAFF]",
        text,
    )
    shortcodes = re.findall(
        r"(?<![A-Za-z0-9]):[a-z][a-z0-9_]{2,}:(?![A-Za-z0-9])",
        text,
    )
    findings = symbols + shortcodes
    return {
        "text": "no-unicode-flair",
        "passed": len(findings) < 2,
        "evidence": (
            f"Found {len(findings)} decorative symbol(s)/shortcode(s): {findings[:8]}"
            if len(findings) >= 2
            else f"Decorative symbols/shortcodes: {len(findings)}"
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


def check_formulaic_openers(text):
    """Detect formulaic paragraph-opening phrases typical of AI text."""
    patterns = [
        r"^at (?:a|the) (?:foundational|fundamental|basic|practical|structural) level[,:]",
        r"^beyond (?:this|that|these|those|\w+(?:tion|ment|ness|ity|ance|ence)),",
        r"^at its core[,:]",
        r"^there is (?:also )?(?:a|an) \w+ (?:dimension|aspect|element|component|factor)",
        r"^it is (?:also )?worth (?:recognising|noting|mentioning|emphasising|acknowledging|highlighting)",
        r"^from (?:a|an|the) \w+ (?:perspective|standpoint|point of view)[,:]",
        r"^on a (?:\w+ )?level[,:]",
        r"^in (?:a|the) (?:broader|wider|larger|similar) (?:context|sense|vein)[,:]",
        r"^perhaps (?:most )?(?:importantly|significantly|notably|crucially)[,:]",
        r"^what (?:is|makes) (?:this|it) (?:particularly|especially|uniquely) \w+",
    ]
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    found = []
    for para in paragraphs:
        first_line = para.split('\n')[0].strip()
        first_lower = first_line.lower()
        for pat in patterns:
            if re.search(pat, first_lower):
                # Truncate to first 60 chars for evidence
                found.append(first_line[:60])
                break
    return {
        "text": "no-formulaic-openers",
        "passed": len(found) == 0,
        "evidence": (
            f"Found {len(found)} formulaic opener(s): {found}"
            if found
            else "No formulaic openers"
        ),
    }


def check_signposted_conclusions(text):
    """Detect explicitly labelled conclusions typical of AI text."""
    patterns = [
        r"^in (?:summary|conclusion)[,:]",
        r"^to (?:summarise|summarize|conclude|sum up|wrap up)[,:]",
        r"^(?:#+\s*)?conclusion\s*$",
        r"^(?:#+\s*)?final thoughts\s*$",
        r"^(?:#+\s*)?key takeaways?\s*$",
        r"^(?:#+\s*)?summing up\s*$",
    ]
    lines = text.strip().split('\n')
    found = []
    for line in lines:
        line_lower = line.strip().lower()
        for pat in patterns:
            if re.search(pat, line_lower):
                found.append(line.strip()[:60])
                break
    return {
        "text": "no-signposted-conclusions",
        "passed": len(found) == 0,
        "evidence": (
            f"Found {len(found)}: {found}"
            if found
            else "No signposted conclusions"
        ),
    }


def check_markdown_headings(text):
    """Detect markdown heading structure in prose (AI essays use ## sections)."""
    headings = []
    for match in re.finditer(r'^#{1,3}\s+.+', strip_front_matter(text), re.MULTILINE):
        heading = match.group()
        # Extracted source metadata often arrives as linked publication labels.
        # Keep detecting article/essay section scaffolding, but do not punish
        # archive chrome such as "### [Issue 194, Fall 2010](...)".
        if re.match(r'^#{1,3}\s+\[[^\]]+\]\([^)]+\)\s*$', heading):
            continue
        headings.append(heading)

    lines = strip_front_matter(text).splitlines()
    first_nonblank = next((idx for idx, line in enumerate(lines) if line.strip()), None)
    if first_nonblank is not None and first_nonblank + 1 < len(lines):
        title = lines[first_nonblank].strip()
        followed_by_blank = not lines[first_nonblank + 1].strip()
        words = re.findall(r"[A-Za-z][A-Za-z'-]*", title)
        significant = [w for w in words if w.lower() not in {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "with"}]
        title_case_words = sum(1 for w in significant if w[0].isupper())
        looks_like_plain_title = (
            followed_by_blank
            and 3 <= len(words) <= 12
            and len(title) <= 90
            and not re.search(r"[.!?]$", title)
            and not title.startswith(("[", "{", "("))
            and title_case_words >= max(2, len(significant) - 1)
        )
        if looks_like_plain_title:
            headings.append(title)
    return {
        "text": "no-markdown-headings",
        "passed": len(headings) == 0,
        "evidence": (
            f"Found {len(headings)} heading(s): {[h[:50] for h in headings[:5]]}"
            if headings
            else "No headings"
        ),
    }


def check_corporate_ai_speak(text):
    """Detect corporate/LinkedIn AI register."""
    patterns = [
        r"deliver(?:ing|s|ed)? impact\b",
        r"measurable outcomes?\b",
        r"deliverable outcomes?\b",
        r"scalable[,\s]+production[- ]grade",
        r"pragmatic approach\b",
        r"drives? (?:\w+ )?outcomes?\b",
        r"cross-functional\b",
        r"end-to-end (?:development|delivery|solution)",
        r"translate[sd]? (?:\w+ )?requirements into (?:\w+ )?(?:outcomes|deliverables|solutions|results)",
        r"stakeholder (?:alignment|engagement|management)\b",
        r"actionable insights?\b",
        r"leverage[sd]? (?:my |our |the )?\w+ (?:experience|expertise)\b",
    ]
    count, matches = count_pattern_matches(text, patterns)
    return {
        "text": "no-corporate-ai-speak",
        "passed": count == 0,
        "evidence": (
            f"Found {count}: {matches}"
            if count > 0
            else "No corporate AI speak"
        ),
    }


def check_this_chains(text):
    """Detect 3+ consecutive sentences starting with 'This [verb]'."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    worst_run = 0
    for para in paragraphs:
        sentences = split_sentences(para)
        current_run = 0
        for s in sentences:
            if re.match(r'^this\s+(?!is\b)\w+', s.strip().lower()):
                current_run += 1
                worst_run = max(worst_run, current_run)
            else:
                current_run = 0
    return {
        "text": "no-this-chains",
        "passed": worst_run < 3,
        "evidence": (
            f"Found {worst_run} consecutive 'This [verb]' sentences"
            if worst_run >= 3
            else f"Max 'This [verb]' run: {worst_run}"
        ),
    }


def check_countdown_negation(text):
    """Detect dramatic countdown negation.

    Branch 1: 'It wasn't X. It wasn't Y. It was Z.' - 2+ negation sentences
    with it/this/that followed by an affirmative reveal.

    Branch 2: 'You can't X. You can't Y. You can't Z.' - 3+ consecutive
    sentences where the same subject pronoun is followed by a negated verb.
    No affirmative reveal required. Threshold is 3 because 2 consecutive
    same-subject negations are common in opinion writing.
    """
    # Branch 1: existing countdown-then-reveal pattern (do not change)
    pattern = r'(?:(?:it|this|that) (?:wasn\'t|isn\'t|was not|is not) [^.?!]+[.]\s*){2,}(?:it|this|that) (?:was|is) [^.?!]+[.]'
    matches = re.findall(pattern, text.lower())
    if matches:
        return {
            "text": "no-countdown-negation",
            "passed": False,
            "evidence": f"Found {len(matches)} countdown negation sequence(s)",
        }

    # Branch 2: 3+ consecutive same-subject pronoun-negation sentences
    negated_verbs = r"(?:can't|won't|don't|shouldn't|couldn't|cannot|will not|do not|should not|could not)"
    subjects = ("you", "we", "they", "people")
    sentences = split_sentences(text)
    max_run = 0
    current_run = 0
    current_subject = None
    for s in sentences:
        s_lower = s.strip().lower()
        matched_subject = None
        for subj in subjects:
            if re.match(rf'^{subj}\s+{negated_verbs}\b', s_lower):
                matched_subject = subj
                break
        if matched_subject and matched_subject == current_subject:
            current_run += 1
            max_run = max(max_run, current_run)
        elif matched_subject:
            current_subject = matched_subject
            current_run = 1
        else:
            current_subject = None
            current_run = 0

    if max_run >= 3:
        return {
            "text": "no-countdown-negation",
            "passed": False,
            "evidence": f"Found {max_run} consecutive same-subject negation sentences",
        }

    return {
        "text": "no-countdown-negation",
        "passed": True,
        "evidence": "No countdown negation",
    }


def check_negation_density(text):
    """Detect heavy reliance on explanatory negation in otherwise smooth prose."""
    words = re.findall(r"\b\w+\b", text.lower())
    if len(words) < 300:
        return {
            "text": "no-negation-density",
            "passed": True,
            "evidence": f"Skipped: short text ({len(words)} words, need 300+)",
        }
    patterns = [
        r"\bis not\b", r"\bare not\b", r"\bwas not\b", r"\bwere not\b",
        r"\bdoes not\b", r"\bdo not\b", r"\bdid not\b",
        r"\bisn't\b", r"\baren't\b", r"\bwasn't\b", r"\bweren't\b",
        r"\bdoesn't\b", r"\bdon't\b", r"\bdidn't\b",
        r"\bnot merely\b", r"\bnot simply\b", r"\bnot just\b",
    ]
    normalized = normalize_for_regex(text)
    matches = []
    for pat in patterns:
        matches.extend(re.findall(pat, normalized))
    per_1000 = len(matches) / len(words) * 1000
    return {
        "text": "no-negation-density",
        "passed": not (len(matches) >= 10 and per_1000 >= 12),
        "evidence": (
            f"Found {len(matches)} negation markers ({per_1000:.1f} per 1000 words)"
            if len(matches) >= 10 and per_1000 >= 12
            else f"Negation markers: {len(matches)} ({per_1000:.1f} per 1000 words)"
        ),
    }


def check_paragraph_uniformity(text):
    """Detect generated-article paragraph architecture sameness."""
    lengths = []
    for para in prose_paragraphs(text):
        words = re.findall(r"\b\w+\b", para)
        if len(words) >= 25:
            lengths.append(len(words))
    if len(lengths) < 7:
        return {
            "text": "paragraph-length-uniformity",
            "passed": True,
            "evidence": f"Skipped: {len(lengths)} substantial paragraphs, need 7+",
        }
    avg = sum(lengths) / len(lengths)
    cv = stdev(lengths) / avg if avg else 0
    return {
        "text": "paragraph-length-uniformity",
        "passed": cv >= 0.18,
        "evidence": (
            f"Paragraph length CV: {cv:.2f} across {len(lengths)} paragraphs (target: >=0.18)"
            if cv < 0.18
            else f"Paragraph length CV: {cv:.2f} across {len(lengths)} paragraphs"
        ),
    }


def check_tidy_paragraph_endings(text):
    """Detect paragraphs that land with generic miniature conclusions."""
    endings = []
    paragraphs = prose_paragraphs(text)
    for para in paragraphs:
        sentences = split_sentences(para)
        if not sentences:
            continue
        last = sentences[-1].lower()
        for pat in TIDY_PARAGRAPH_ENDINGS:
            if re.search(pat, last):
                endings.append(sentences[-1][:90])
                break
    return {
        "text": "no-tidy-paragraph-endings",
        "passed": len(endings) < 3,
        "evidence": (
            f"Found {len(endings)} tidy paragraph ending(s): {endings[:5]}"
            if len(endings) >= 3
            else f"Tidy paragraph endings: {len(endings)}"
        ),
    }


def check_bland_critical_template(text):
    """Detect generated literary/review criticism that sounds balanced but generic."""
    count, matches = count_pattern_matches(text, BLAND_CRITICAL_TEMPLATE)
    return {
        "text": "no-bland-critical-template",
        "passed": count < 3,
        "evidence": (
            f"Found {count} bland critical template phrase(s): {matches[:6]}"
            if count >= 3
            else f"Bland critical template phrases: {count}"
        ),
    }


def check_rubric_echoing(text):
    """Detect student-essay boilerplate that mirrors assignment/rubric language."""
    count, matches = count_pattern_matches(text, RUBRIC_ECHO_PATTERNS)
    return {
        "text": "no-rubric-echoing",
        "passed": count < 3,
        "evidence": (
            f"Found {count} rubric echo phrase(s): {matches[:5]}"
            if count >= 3
            else f"Rubric echo phrases: {count}"
        ),
    }


def check_triad_density(text):
    """Detect high density of three-item lists ('X, Y, and/or Z') regardless of word type."""
    words = text.split()
    if len(words) < 300:
        return {
            "text": "no-triad-density",
            "passed": True,
            "evidence": f"Skipped: short text ({len(words)} words, need 300+)",
        }
    # Each item: 1-4 words (handles "peer learning", "decision-making structures")
    _item = r'\w+(?:[- ]\w+){0,3}'
    pattern = rf'({_item}),\s+({_item}),?\s+(?:and|or)\s+({_item})'
    matches = re.findall(pattern, text.lower())
    count = len(matches)
    match_strs = [', '.join(m) for m in matches]
    return {
        "text": "no-triad-density",
        "passed": count < 4,
        "evidence": (
            f"Found {count} triad(s): {match_strs}"
            if count >= 4
            else f"Triads: {count}"
        ),
    }


def check_type_token_ratio(text):
    """Detect low vocabulary diversity via type-token ratio."""
    # Strip markdown and punctuation, extract words
    clean = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = clean.split()
    if len(words) < 150:
        return {
            "text": "vocabulary-diversity",
            "passed": True,
            "evidence": f"Skipped: short text ({len(words)} words, need 150+)",
        }
    unique = len(set(words))
    ratio = unique / len(words)
    return {
        "text": "vocabulary-diversity",
        "passed": ratio > 0.40,
        "evidence": f"Type-token ratio: {ratio:.3f} ({unique} unique / {len(words)} total, target: >0.40)",
    }


HEDGING_PATTERNS = [
    r"\bis (?:often|frequently|widely|commonly|generally|typically) (?:framed|seen|viewed|regarded|considered|described|understood|presented|perceived|characterized|characterised)\b",
    r"\bis (?:increasingly|often) (?:measured|prioritised|prioritized|recognized|recognised|valued|questioned)\b",
    r"\bis (?:contingent|predicated|dependent) on\b",
    r"\bcannot be (?:overstated|understated|ignored|dismissed|overlooked)\b",
    r"\bis (?:difficult|hard|impossible) to (?:overstate|ignore|deny|dismiss|overlook)\b",
    r"\bremains (?:to be seen|unclear|uncertain|an open question)\b",
    r"\bit (?:could|might|may) be argued\b",
    r"\bis not (?:guaranteed|without)\b",
    r"\bis (?:overstated|understated|underestimated|overestimated)\b",
    r"\bis less about\b.*\bmore about\b",
    r"\ba common (?:assumption|misconception|objection|criticism) is\b",
]


def check_section_scaffolding(text):
    """Detect repeated identical subheadings across sections (pattern 38)."""
    lines = text.split('\n')
    counts = {}
    for line in lines:
        stripped = line.strip()
        # Strip leading markdown heading markers
        stripped = re.sub(r'^#+\s*', '', stripped)
        normalised = stripped.lower().strip()
        # Skip empty lines and lines that are only punctuation/markdown markers
        if not normalised or re.match(r'^[#*_\-=~`>|]+$', normalised):
            continue
        # Only count short lines (under 60 chars): these are labels, not prose
        if len(normalised) < 60:
            counts[normalised] = counts.get(normalised, 0) + 1
    # Flag if any normalised line appears 3+ times
    repeated = {label: n for label, n in counts.items() if n >= 3}
    if repeated:
        worst = max(repeated, key=repeated.get)
        return {
            "text": "no-section-scaffolding",
            "passed": False,
            "evidence": f"'{worst}' repeated {repeated[worst]} times",
        }
    return {
        "text": "no-section-scaffolding",
        "passed": True,
        "evidence": "No repeated section labels",
    }


def check_hedging_density(text):
    """Detect excessive impersonal passive hedging density."""
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    total_matches = 0
    all_found = []
    for para in paragraphs:
        para_lower = para.lower()
        for pat in HEDGING_PATTERNS:
            found = re.findall(pat, para_lower)
            if found:
                total_matches += len(found)
                all_found.extend(found)
    # Flag at 4+ hedging constructions across the whole text
    return {
        "text": "no-excessive-hedging",
        "passed": total_matches < 4,
        "evidence": (
            f"Found {total_matches} hedging constructions: {all_found[:5]}"
            if total_matches >= 4
            else f"Hedging constructions: {total_matches}"
        ),
    }


NOTABILITY_CLAIMS = [
    r"\bindependent (?:coverage|sources?|reviews?)\b",
    r"\b(?:local|regional|national|international) (?:news )?(?:media )?outlets?\b",
    r"\bwritten by a leading expert\b",
    r"\b(?:has|have|maintains?|with|showcasing|boasts?) (?:an? )?active social media presence\b",
    r"\bactive social media presence\b",
    r"\b(?:over|more than) [\d,]+\+? (?:followers?|subscribers?|fans?)\b",
    r"\b(?:cited|featured|covered|profiled) (?:in|by) (?:multiple|numerous|several) (?:major )?(?:outlets?|publications?|media)\b",
    r"\bgained (?:significant|widespread|notable) (?:media )?attention\b",
]


def check_notability_claims(text):
    """Detect notability claims that list authorities without context (pattern 2)."""
    count, matches = count_pattern_matches(text, NOTABILITY_CLAIMS)
    return {
        "text": "no-notability-claims",
        "passed": count == 0,
        "evidence": (
            f"Found {count} notability claim(s): {matches[:3]}"
            if count > 0
            else "No notability claims"
        ),
    }


VAGUE_ATTRIBUTIONS = [
    r"\bindustry reports? (?:say|state|claim|note|suggest|indicate|highlight|reveal|show|find)\b",
    r"\bobservers? (?:have )?(?:cited|noted|argued|claimed|suggested|pointed out)\b",
    r"\bexperts? (?:argue|believe|say|note|suggest|claim|indicate|warn|caution|agree)\b",
    r"\b(?:some|many|several|various|certain|a number of) (?:critics?|analysts?|scholars?|researchers?|commentators?|observers?) (?:argue|believe|say|note|suggest|claim|warn|cite|point out)\b",
    r"\bseveral (?:sources?|publications?|outlets?|reports?) (?:have )?(?:cited|noted|reported|claimed|confirmed)\b",
    r"\bit is (?:widely |often |frequently |commonly |generally )?(?:believed|argued|claimed|noted|reported|understood|accepted|acknowledged|recognised|recognized)\b",
    r"\b(?:research|studies) (?:has|have)? ?(?:shown|demonstrated|indicated|suggested|found) that\b",
]


def check_vague_attributions(text):
    """Detect vague-authority attributions without named sources (pattern 5)."""
    count, matches = count_pattern_matches(text, VAGUE_ATTRIBUTIONS)
    return {
        "text": "no-vague-attributions",
        "passed": count == 0,
        "evidence": (
            f"Found {count} vague attribution(s): {matches[:3]}"
            if count > 0
            else "No vague attributions"
        ),
    }


def check_boldface_overuse(text):
    """Detect mechanical boldface emphasis in prose (pattern 13)."""
    bold_pattern = re.compile(r"\*\*[^*\n]{1,80}\*\*")
    list_or_heading = re.compile(r"^\s*(?:[-*+•]|\d+\.|#{1,6})\s+")
    total = 0
    matches = []
    for line in text.split("\n"):
        if list_or_heading.match(line):
            continue
        for m in bold_pattern.findall(line):
            total += 1
            matches.append(m)
    return {
        "text": "no-boldface-overuse",
        "passed": total < 4,
        "evidence": (
            f"Found {total} bold span(s) in prose: {matches[:5]}"
            if total >= 4
            else f"Bold spans in prose: {total}"
        ),
    }


def check_inline_header_lists(text):
    """Detect list items that start with a bolded header and colon (pattern 14)."""
    header_in_list = re.compile(
        r"^\s*(?:[-*+•]|\d+\.)\s+\*\*[^*\n]{1,60}:\*\*",
        re.MULTILINE,
    )
    matches = header_in_list.findall(text)
    return {
        "text": "no-inline-header-lists",
        "passed": len(matches) < 2,
        "evidence": (
            f"Found {len(matches)} list item(s) with bolded headers"
            if len(matches) >= 2
            else f"List items with bolded headers: {len(matches)}"
        ),
    }


COMPOUND_MODIFIERS = [
    r"\bthird-party\b", r"\bcross-functional\b", r"\bclient-facing\b",
    r"\bcustomer-facing\b", r"\buser-facing\b",
    r"\bdata-driven\b", r"\bdecision-making\b",
    r"\bwell-known\b", r"\bwell-established\b", r"\bwell-defined\b",
    r"\bhigh-quality\b", r"\bhigh-impact\b", r"\bhigh-performance\b",
    r"\bhigh-level\b", r"\bhigh-stakes\b",
    r"\breal-time\b", r"\blong-term\b", r"\bshort-term\b",
    r"\bend-to-end\b", r"\bday-to-day\b", r"\bback-and-forth\b",
    r"\buser-friendly\b", r"\bcost-effective\b",
    r"\bforward-thinking\b", r"\bforward-looking\b",
    r"\bdetail-oriented\b", r"\bgoal-oriented\b", r"\bresults-oriented\b",
    r"\bmission-critical\b", r"\bbest-in-class\b",
    r"\bcutting-edge\b", r"\bnext-generation\b", r"\bworld-class\b",
    r"\bbest-of-breed\b", r"\bstate-of-the-art\b",
]
COMPOUND_MODIFIER_RE = re.compile("|".join(COMPOUND_MODIFIERS))


def check_compound_modifier_density(text):
    """Detect three or more hyphenated compound modifiers in a single sentence (pattern 18)."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    flagged = []
    for sent in sentences:
        sent_lower = sent.lower()
        if "-" not in sent_lower:
            continue
        per_sentence = COMPOUND_MODIFIER_RE.findall(sent_lower)
        if len(per_sentence) >= 3:
            flagged.append(per_sentence)
    return {
        "text": "no-compound-modifier-density",
        "passed": len(flagged) == 0,
        "evidence": (
            f"Found {len(flagged)} sentence(s) with 3+ AI compound modifiers: {flagged[:2]}"
            if flagged
            else "No dense compound-modifier sentences"
        ),
    }


KNOWLEDGE_CUTOFF_DISCLAIMERS = [
    r"\bup to my (?:last )?(?:training |knowledge )?(?:update|cutoff|cut-off)\b",
    r"\bas of my (?:last )?(?:training |knowledge )?(?:update|cutoff|cut-off)\b",
    r"\bbased on (?:available|the available|publicly available|publicly accessible) information\b",
    r"\bwhile (?:specific|exact|precise) (?:details|information|data) (?:are |is )?(?:limited|scarce|unavailable|sparse|not (?:extensively |readily )?(?:documented|available))\b",
    r"\b(?:specific|exact|precise) (?:details|information|data) (?:about|regarding|concerning) [^.!?\n]{0,80} (?:are|is) (?:limited|scarce|unavailable|not (?:readily )?available)\b",
    r"\bnot (?:extensively |widely |readily )?documented in (?:readily )?available sources\b",
    r"\bin readily available sources\b",
    r"\bi (?:do not|don't|cannot|can't) have (?:access to|information about|details on)\b",
    r"\bi am unable to (?:access|verify|confirm|provide)\b",
    r"\bmy (?:training|knowledge) (?:cutoff|cut-off|cuts off|ends|extends to|is limited to)\b",
]


def check_knowledge_cutoff_disclaimers(text):
    """Detect AI knowledge-cutoff or training-update disclaimers (pattern 20)."""
    count, matches = count_pattern_matches(text, KNOWLEDGE_CUTOFF_DISCLAIMERS)
    return {
        "text": "no-knowledge-cutoff-disclaimers",
        "passed": count == 0,
        "evidence": (
            f"Found {count} knowledge-cutoff disclaimer(s): {matches[:3]}"
            if count > 0
            else "No knowledge-cutoff disclaimers"
        ),
    }


# --- Registry ---

ALL_CHECKS = {
    "no-em-dashes": check_em_dashes,
    "no-ai-vocabulary-clustering": check_ai_vocabulary,
    "no-nonliteral-land-surface": check_nonliteral_land_surface,
    "overall-ai-signal-pressure": check_overall_signal_pressure,
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
    "no-false-concession-hedges": check_false_concession,
    "no-placeholder-residue": check_placeholder_residue,
    "no-soft-scaffolding": check_soft_scaffolding,
    "no-orphaned-demonstratives": check_orphaned_demonstratives,
    "no-forced-triads": check_rule_of_three,
    "no-superficial-ing": check_superficial_ing,
    "no-ghost-spectral-density": check_ghost_spectral,
    "no-quietness-obsession": check_quietness,
    "no-rhetorical-questions": check_rhetorical_questions,
    "no-excessive-lists": check_list_density,
    "no-unicode-flair": check_unicode_flair,
    "no-dramatic-transitions": check_dramatic_transitions,
    "no-formulaic-openers": check_formulaic_openers,
    "no-signposted-conclusions": check_signposted_conclusions,
    "no-markdown-headings": check_markdown_headings,
    "no-corporate-ai-speak": check_corporate_ai_speak,
    "no-this-chains": check_this_chains,
    "no-excessive-hedging": check_hedging_density,
    "no-countdown-negation": check_countdown_negation,
    "no-negation-density": check_negation_density,
    "paragraph-length-uniformity": check_paragraph_uniformity,
    "no-tidy-paragraph-endings": check_tidy_paragraph_endings,
    "no-bland-critical-template": check_bland_critical_template,
    "no-rubric-echoing": check_rubric_echoing,
    "vocabulary-diversity": check_type_token_ratio,
    "no-triad-density": check_triad_density,
    "no-section-scaffolding": check_section_scaffolding,
    "no-notability-claims": check_notability_claims,
    "no-vague-attributions": check_vague_attributions,
    "no-boldface-overuse": check_boldface_overuse,
    "no-inline-header-lists": check_inline_header_lists,
    "no-compound-modifier-density": check_compound_modifier_density,
    "no-knowledge-cutoff-disclaimers": check_knowledge_cutoff_disclaimers,
}


CHECK_REPORT_TEXT = {
    "no-em-dashes": ("Em dashes", "Checks for em dash punctuation, a strong current AI-style signal in this skill."),
    "no-ai-vocabulary-clustering": ("Clustered AI vocabulary", "Checks whether generic AI-associated words and phrases cluster together."),
    "no-nonliteral-land-surface": ("Nonliteral land/surface phrasing", "Checks for abstract uses such as ideas landing, concerns surfacing, or work landing on a scale."),
    "overall-ai-signal-pressure": ("AI pressure from stacked signals", "Looks for several weaker AI-writing signals appearing together, which can make a draft feel machine-packaged even when no single signal is decisive."),
    "no-manufactured-insight": ("Manufactured insight framing", "Checks for phrases that perform hidden depth or secret significance without earning it."),
    "no-staccato-sequences": ("Generic staccato emphasis", "Checks for repeated short dramatic sentences used as generic emphasis."),
    "no-anaphora": ("Mechanical repeated sentence starts", "Checks for repeated sentence openings that read like template rhythm."),
    "no-collaborative-artifacts": ("Assistant residue", "Checks for assistant-like collaboration phrases, follow-up offers, or generated-chat residue."),
    "no-curly-quotes": ("Curly quotes", "Checks for curly quotation marks when plain output is expected."),
    "sentence-length-variance": ("Sentence rhythm variance", "Checks whether sentence lengths are too uniform across longer prose."),
    "no-promotional-language": ("Generic promotional language", "Checks for stock hype and sales-like adjectives."),
    "no-significance-inflation": ("Inflated significance", "Checks for language that makes ordinary claims sound historically important."),
    "no-negative-parallelisms": ("Contrived contrast", "Checks for not-X-but-Y, beyond-X, less-X-than-Y, and related reveal structures."),
    "no-copula-avoidance": ("Avoiding plain 'is'", "Checks for inflated replacements such as serves as, functions as, or stands as."),
    "no-filler-phrases": ("Filler phrases", "Checks for stock padding such as in order to or it is worth noting."),
    "no-generic-conclusions": ("Generic conclusion", "Checks for empty endings such as the future looks bright."),
    "no-false-concession-hedges": ("False balance or concession", "Checks for fake both-sides framing that avoids taking a position."),
    "no-placeholder-residue": ("Placeholder residue", "Checks for unfilled template markers and placeholder instructions."),
    "no-soft-scaffolding": ("Soft explainer scaffolding", "Checks for phrases that announce structure instead of making a point."),
    "no-orphaned-demonstratives": ("Vague 'this/that' starts", "Checks for repeated vague sentence subjects such as This highlights or That shows."),
    "no-forced-triads": ("Decorative three-part lists", "Checks for forced triads used as rhythm rather than substance."),
    "no-superficial-ing": ("Tacked-on -ing analysis", "Checks for trailing -ing clauses that pretend to analyse without adding meaning."),
    "no-ghost-spectral-density": ("Ghost/spectral atmosphere", "Checks for clichéd ghost, shadow, whisper, and echo language."),
    "no-quietness-obsession": ("Generic quiet/still mood", "Checks for overused quiet, still, soft, and hushed atmosphere."),
    "no-rhetorical-questions": ("Template rhetorical questions", "Checks for article-style questions followed by obvious answers."),
    "no-excessive-lists": ("Excessive list formatting", "Checks whether prose has been over-converted into bullets or numbered lists."),
    "no-unicode-flair": ("Decorative Unicode", "Checks for symbols and decorative punctuation that look like generated formatting."),
    "no-dramatic-transitions": ("Unearned dramatic transitions", "Checks for generic turning points such as something shifted or everything changed."),
    "no-formulaic-openers": ("Formulaic openers", "Checks for generated openings such as at its core or from a broader perspective."),
    "no-signposted-conclusions": ("Signposted conclusion", "Checks for explicit conclusion labels and summary signposts."),
    "no-markdown-headings": ("Headings in prose", "Checks for markdown headings and plain title headings when prose should flow."),
    "no-corporate-ai-speak": ("Corporate AI-speak", "Checks for vague delivery, alignment, outcomes, and cross-functional clichés."),
    "no-this-chains": ("Repeated 'This...' chains", "Checks for several consecutive sentences beginning with vague This constructions."),
    "no-excessive-hedging": ("Excessive hedging", "Checks for evasive qualification and impersonal uncertainty."),
    "no-countdown-negation": ("Countdown negation", "Checks for repeated no/not/cannot setups that build toward a reveal."),
    "no-negation-density": ("Dense negation", "Checks whether negation markers are unusually dense across prose."),
    "paragraph-length-uniformity": ("Paragraph length uniformity", "Checks whether paragraphs are suspiciously similar in length."),
    "no-tidy-paragraph-endings": ("Tidy paragraph endings", "Checks for repeated miniature conclusions at paragraph ends."),
    "no-bland-critical-template": ("Bland critical template", "Checks for generic review language instead of concrete critical claims."),
    "no-rubric-echoing": ("Rubric echoing", "Checks for assignment or rubric phrasing leaking into the prose."),
    "vocabulary-diversity": ("Vocabulary diversity", "Checks for unusually repetitive vocabulary in longer text."),
    "no-triad-density": ("Triad density", "Checks whether three-part list structures are overused across the piece."),
    "no-section-scaffolding": ("Repeated section scaffolding", "Checks for repeated section labels or repeated structural templates."),
    "no-notability-claims": ("Notability claims", "Checks for fake-prestige framing such as active social media presence or coverage by unnamed major outlets."),
    "no-vague-attributions": ("Vague attributions", "Checks for unnamed-authority phrasing such as experts argue, observers note, or industry reports say."),
    "no-boldface-overuse": ("Boldface overuse", "Checks for mechanical bold emphasis stacked across a passage of prose."),
    "no-inline-header-lists": ("Inline-header lists", "Checks for list items that begin with a bolded header and colon, turning prose into a slide deck."),
    "no-compound-modifier-density": ("Hyphenated compound modifier overuse", "Checks for three or more AI-stock hyphenated compound modifiers crammed into one sentence."),
    "no-knowledge-cutoff-disclaimers": ("Knowledge-cutoff disclaimers", "Checks for AI training-update or limited-information hedges left in the prose."),
}


CHECK_WHY_IT_MATTERS = {
    "no-em-dashes": "Em dashes are now a strong style fingerprint in generated prose, especially when they appear as default punctuation.",
    "no-ai-vocabulary-clustering": "Generic AI-associated words become more suspicious when they cluster instead of appearing naturally in context.",
    "no-nonliteral-land-surface": "Abstract land/surface phrasing often makes ordinary ideas sound artificially managed or packaged.",
    "overall-ai-signal-pressure": "Several weak signals appearing together can make a draft feel machine-packaged even when each signal alone is explainable.",
    "no-manufactured-insight": "Manufactured insight framing performs depth without adding specific evidence or thought.",
    "no-staccato-sequences": "Repeated short emphasis beats can make prose sound generated rather than naturally paced.",
    "no-anaphora": "Mechanical repeated openings can signal template rhythm instead of intentional rhetoric.",
    "no-collaborative-artifacts": "Assistant residue makes the text look like chat output rather than finished prose.",
    "no-curly-quotes": "Curly quotes are not proof of AI, but they matter when the output is expected to be plain cleaned text.",
    "sentence-length-variance": "Low rhythm variation makes paragraphs feel mechanically produced.",
    "no-promotional-language": "Stock hype weakens credibility and often appears in generated product or venue copy.",
    "no-significance-inflation": "Inflated importance makes ordinary claims sound artificially momentous.",
    "no-negative-parallelisms": "Contrived contrast creates a fake reveal instead of making a direct, supported claim.",
    "no-copula-avoidance": "Avoiding plain 'is' often turns simple claims into inflated pseudo-analysis.",
    "no-filler-phrases": "Filler phrases add polish without information.",
    "no-generic-conclusions": "Generic conclusions make the ending feel templated and interchangeable.",
    "no-false-concession-hedges": "False balance can hide the writer's actual position.",
    "no-placeholder-residue": "Placeholder residue signals unfinished generated or templated text.",
    "no-soft-scaffolding": "Soft scaffolding announces structure instead of doing useful writing work.",
    "no-orphaned-demonstratives": "Vague this/that openings blur the actual subject and create generic analysis.",
    "no-forced-triads": "Decorative three-part lists can create artificial rhythm without substance.",
    "no-superficial-ing": "Tacked-on -ing clauses often pretend to analyse while adding little.",
    "no-ghost-spectral-density": "Stock spectral language can make atmosphere feel generated or borrowed.",
    "no-quietness-obsession": "Overused quiet/still mood language can create generic literary atmosphere.",
    "no-rhetorical-questions": "Template questions often simulate engagement without adding real inquiry.",
    "no-excessive-lists": "Too much list formatting can make prose feel like generated notes or slides.",
    "no-unicode-flair": "Decorative symbols can make output look like generated formatting.",
    "no-dramatic-transitions": "Unearned turning-point language claims drama the prose has not built.",
    "no-formulaic-openers": "Formulaic openings make paragraphs feel assembled from templates.",
    "no-signposted-conclusions": "Conclusion signposts often flatten the ending into a generic summary.",
    "no-markdown-headings": "Headings can make prose feel packaged by an assistant rather than written as a continuous piece.",
    "no-corporate-ai-speak": "Corporate AI-speak hides specific work behind vague operational language.",
    "no-this-chains": "Repeated vague This sentences create generic analysis and weak subject control.",
    "no-excessive-hedging": "Too much hedging weakens stance and can make prose feel evasive or machine-neutral.",
    "no-countdown-negation": "Countdown negation creates a synthetic reveal structure.",
    "no-negation-density": "Dense negation can make a piece feel over-framed around what it is not instead of what it is.",
    "paragraph-length-uniformity": "Paragraphs of similar length can signal generated structure and low natural variation.",
    "no-tidy-paragraph-endings": "Repeated tidy endings make paragraphs feel over-resolved and templated.",
    "no-bland-critical-template": "Bland critical language replaces concrete judgment with portable review phrases.",
    "no-rubric-echoing": "Rubric echoing makes writing sound like assignment compliance rather than independent thought.",
    "vocabulary-diversity": "Low vocabulary variety can make longer prose feel repetitive and mechanically produced.",
    "no-triad-density": "Too many three-part lists create a recognisable generated cadence.",
    "no-section-scaffolding": "Repeated section structure makes the whole piece feel assembled from a template.",
    "no-notability-claims": "Listing unnamed authorities or follower counts as if the mention itself were the story performs prestige instead of reporting it.",
    "no-vague-attributions": "Unnamed expert and report citations create the illusion of consensus without naming a real source.",
    "no-boldface-overuse": "Mechanical boldface stacking flattens prose into emphasis-by-default and reads like generated formatting.",
    "no-inline-header-lists": "Bolded-header list items convert prose into slide-deck shapes, a strong frictionless-structure tell.",
    "no-compound-modifier-density": "Stacking three or more hyphenated compound modifiers in one sentence is a recognisable AI cadence rather than a deliberate style choice.",
    "no-knowledge-cutoff-disclaimers": "AI training-update and limited-information hedges are model meta-residue and almost never belong in finished prose.",
}


CHECK_METADATA = {
    "no-collaborative-artifacts": {
        "severity": "hard_fail",
        "failure_modes": ["provenance_residue"],
        "evidence_role": "assistant_residue",
        "guidance": "Fix at every depth; this is assistant residue, not authorial style.",
    },
    "no-generic-conclusions": {
        "severity": "hard_fail",
        "failure_modes": ["provenance_residue", "synthetic_significance"],
        "evidence_role": "generic_closure",
        "guidance": "Fix at every depth unless quoted from source text.",
    },
    "no-placeholder-residue": {
        "severity": "hard_fail",
        "failure_modes": ["provenance_residue"],
        "evidence_role": "template_residue",
        "guidance": "Fix at every depth; unfilled placeholders are generated/template residue.",
    },
    "no-manufactured-insight": {
        "severity": "strong_warning",
        "failure_modes": ["synthetic_significance"],
        "evidence_role": "rhetorical_pattern",
        "guidance": "Fix at Balanced and All; at Balanced, recommend preserving only if it clearly belongs to the writer's voice.",
    },
    "no-false-concession-hedges": {
        "severity": "strong_warning",
        "failure_modes": ["voice_erasure"],
        "evidence_role": "stance_erasure",
        "guidance": "Fix fake both-sides framing at Balanced and All; preserve only if the piece actually argues both positions with evidence.",
    },
    "no-negative-parallelisms": {
        "severity": "strong_warning",
        "failure_modes": ["synthetic_significance"],
        "evidence_role": "rhetorical_pattern",
        "guidance": "Fix contrived reframes at Balanced and All; recommend preserving only purposeful contrast at Balanced.",
    },
    "no-ai-vocabulary-clustering": {
        "severity": "strong_warning",
        "failure_modes": ["generic_abstraction"],
        "evidence_role": "vocabulary_cluster",
        "guidance": "Fix clustered generic AI vocabulary; individual words may be fine in context.",
    },
    "no-nonliteral-land-surface": {
        "severity": "strong_warning",
        "failure_modes": ["generic_abstraction", "synthetic_significance"],
        "evidence_role": "metaphor_residue",
        "guidance": "Fix nonliteral land/surface phrasing; replace with the concrete action or claim.",
    },
    "overall-ai-signal-pressure": {
        "severity": "context_warning",
        "failure_modes": ["generic_abstraction", "frictionless_structure"],
        "evidence_role": "aggregate_pressure",
        "guidance": "Review aggregate signal pressure; this combines weak signals and Kobak excess-vocabulary evidence but is not an authorship verdict.",
    },
    "no-copula-avoidance": {
        "severity": "strong_warning",
        "failure_modes": ["synthetic_significance", "generic_abstraction"],
        "evidence_role": "grammar_substitution",
        "guidance": "Usually simplify at Balanced and All; recommend preserving if the construction is idiomatic or technical.",
    },
    "no-filler-phrases": {
        "severity": "strong_warning",
        "failure_modes": ["generic_abstraction"],
        "evidence_role": "filler_phrase",
        "guidance": "Fix stock filler at Balanced and All; at Balanced, disclose and remove unless it belongs to quoted or intentionally casual voice.",
    },
    "no-superficial-ing": {
        "severity": "strong_warning",
        "failure_modes": ["generic_abstraction"],
        "evidence_role": "analysis_substitution",
        "guidance": "Fix tacked-on analysis clauses unless they carry precise causal meaning.",
    },
    "no-corporate-ai-speak": {
        "severity": "strong_warning",
        "failure_modes": ["generic_abstraction"],
        "evidence_role": "domain_cliche",
        "guidance": "Fix at every depth; recommend preserving only when quoting corporate source language.",
    },
    "no-soft-scaffolding": {
        "severity": "strong_warning",
        "failure_modes": ["frictionless_structure"],
        "evidence_role": "explainer_scaffold",
        "guidance": "Fix at Balanced and All; these phrases usually mark generated explainer structure rather than content.",
    },
    "no-formulaic-openers": {
        "severity": "strong_warning",
        "failure_modes": ["frictionless_structure", "generic_abstraction"],
        "evidence_role": "formulaic_structure",
        "guidance": "Fix at Balanced and All; at Balanced, recommend preserving only if it matches the source genre.",
    },
    "no-section-scaffolding": {
        "severity": "strong_warning",
        "failure_modes": ["frictionless_structure"],
        "evidence_role": "repeated_template",
        "guidance": "Fix repeated templates at Balanced and All; recommend preserving only for genuinely structured reference material.",
    },
    "no-bland-critical-template": {
        "severity": "strong_warning",
        "failure_modes": ["generic_abstraction", "voice_erasure"],
        "evidence_role": "genre_cliche",
        "guidance": "Fix at Balanced and All for reviews and criticism; replace generic balance with concrete claims from the work.",
    },
    "no-em-dashes": {
        "severity": "strong_warning",
        "failure_modes": ["genre_misfit"],
        "evidence_role": "punctuation_signal",
        "guidance": "Treat as a strong 2026 AI-style signal. May be preserved only at Balanced depth with explicit disclosure; All requires removal.",
    },
    "no-curly-quotes": {
        "severity": "context_warning",
        "failure_modes": ["genre_misfit"],
        "evidence_role": "typographic_signal",
        "guidance": "Normalise in All/plain output; recommend preserving in sourced literary or typographic text.",
    },
    "no-staccato-sequences": {
        "severity": "context_warning",
        "failure_modes": ["genre_misfit", "frictionless_structure"],
        "evidence_role": "rhythm_signal",
        "guidance": "Fix generic emphasis; recommend preserving character voice, humour, panic, dialogue, or literary rhythm.",
    },
    "no-anaphora": {
        "severity": "context_warning",
        "failure_modes": ["genre_misfit", "frictionless_structure"],
        "evidence_role": "rhythm_signal",
        "guidance": "Fix mechanical repetition; recommend preserving deliberate rhetoric or literary patterning.",
    },
    "sentence-length-variance": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "rhythm_signal",
        "guidance": "Use as a rhythm signal, not a hard failure for short or intentionally uniform forms.",
    },
    "no-promotional-language": {
        "severity": "context_warning",
        "failure_modes": ["generic_abstraction", "synthetic_significance"],
        "evidence_role": "hype_language",
        "guidance": "Fix generic hype; recommend preserving quoted marketing copy or voiced enthusiasm.",
    },
    "no-significance-inflation": {
        "severity": "context_warning",
        "failure_modes": ["synthetic_significance"],
        "evidence_role": "importance_inflation",
        "guidance": "Fix inflated importance unless the source genuinely argues significance.",
    },
    "no-forced-triads": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "list_rhythm",
        "guidance": "Fix decorative triads; recommend preserving meaningful lists and deliberate rhetoric.",
    },
    "no-ghost-spectral-density": {
        "severity": "context_warning",
        "failure_modes": ["generic_abstraction", "genre_misfit"],
        "evidence_role": "atmospheric_cliche",
        "guidance": "Fix atmospheric filler; recommend preserving gothic, literary, or quoted prose.",
    },
    "no-quietness-obsession": {
        "severity": "context_warning",
        "failure_modes": ["synthetic_significance", "genre_misfit"],
        "evidence_role": "atmospheric_cliche",
        "guidance": "Fix generic quietness mood; recommend preserving if quietness is the actual subject or voice.",
    },
    "no-rhetorical-questions": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "rhetorical_template",
        "guidance": "Fix article-template questions; recommend preserving interviews, teaching prose, or deliberate argument.",
    },
    "no-excessive-lists": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "listification",
        "guidance": "Fix unnecessary listification; recommend preserving reference, instructional, or interview structure.",
    },
    "no-dramatic-transitions": {
        "severity": "context_warning",
        "failure_modes": ["synthetic_significance", "genre_misfit"],
        "evidence_role": "narrative_template",
        "guidance": "Fix generic turning-point beats; recommend preserving memoir or scene structure when earned.",
    },
    "no-signposted-conclusions": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "structural_signpost",
        "guidance": "Fix generic signposts in prose; recommend preserving academic/instructional structure when useful.",
    },
    "no-markdown-headings": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "formatting_signal",
        "guidance": "Fix markdown headings and plain title headings when prose should flow; recommend preserving web articles, guides, and reference docs.",
    },
    "no-this-chains": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "voice_erasure"],
        "evidence_role": "sentence_subject",
        "guidance": "Fix mechanical sentence starts; recommend preserving only if rhythmically deliberate.",
    },
    "no-orphaned-demonstratives": {
        "severity": "context_warning",
        "failure_modes": ["voice_erasure", "generic_abstraction"],
        "evidence_role": "sentence_subject",
        "guidance": "Review repeated 'This/That highlights...' starts; replace vague subjects with concrete nouns when the antecedent is unclear.",
    },
    "no-excessive-hedging": {
        "severity": "context_warning",
        "failure_modes": ["voice_erasure"],
        "evidence_role": "stance_erasure",
        "guidance": "Fix evasive hedging; recommend preserving scientific qualification and honest uncertainty.",
    },
    "no-countdown-negation": {
        "severity": "context_warning",
        "failure_modes": ["synthetic_significance", "frictionless_structure"],
        "evidence_role": "rhetorical_pattern",
        "guidance": "Fix generic reveal structures; recommend preserving deliberate rhetoric only with strong reason.",
    },
    "no-negation-density": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "rhetorical_density",
        "guidance": "Review dense negation as a style signal; preserve polemic or technical qualification when purposeful.",
    },
    "paragraph-length-uniformity": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure"],
        "evidence_role": "layout_rhythm",
        "guidance": "Review as a structural signal; vary paragraph lengths when the piece reads like a generated article template.",
    },
    "no-tidy-paragraph-endings": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "voice_erasure"],
        "evidence_role": "paragraph_closure",
        "guidance": "Cut generic paragraph-final summaries unless they carry a necessary argument turn.",
    },
    "no-unicode-flair": {
        "severity": "context_warning",
        "failure_modes": ["provenance_residue", "genre_misfit"],
        "evidence_role": "formatting_residue",
        "guidance": "Remove decorative symbols in prose; preserve only where symbols are part of a real UI, checklist, or quoted source.",
    },
    "no-rubric-echoing": {
        "severity": "context_warning",
        "failure_modes": ["provenance_residue", "voice_erasure"],
        "evidence_role": "assignment_residue",
        "guidance": "Review student/assignment prose for mirrored rubric language; preserve only where explicitly analysing a rubric.",
    },
    "vocabulary-diversity": {
        "severity": "context_warning",
        "failure_modes": ["generic_abstraction", "genre_misfit"],
        "evidence_role": "lexical_distribution",
        "guidance": "Use as a coarse signal; old prose, dialogue, and technical writing may fail legitimately.",
    },
    "no-triad-density": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "genre_misfit"],
        "evidence_role": "list_rhythm",
        "guidance": "Fix density-driven triads; recommend preserving if lists are structural or rhetorical.",
    },
    "no-notability-claims": {
        "severity": "strong_warning",
        "failure_modes": ["synthetic_significance", "generic_abstraction"],
        "evidence_role": "notability_inflation",
        "guidance": "Fix at Balanced and All; replace abstract notability claims with named sources or remove the framing.",
    },
    "no-vague-attributions": {
        "severity": "strong_warning",
        "failure_modes": ["synthetic_significance", "generic_abstraction"],
        "evidence_role": "attribution_vagueness",
        "guidance": "Fix at Balanced and All; replace unnamed authorities with a named source, study, or quote.",
    },
    "no-boldface-overuse": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure"],
        "evidence_role": "emphasis_pattern",
        "guidance": "Fix mechanical bold stacking; preserve only when bolded terms are genuine definition headers.",
    },
    "no-inline-header-lists": {
        "severity": "strong_warning",
        "failure_modes": ["frictionless_structure", "generic_abstraction"],
        "evidence_role": "list_template",
        "guidance": "Fix at Balanced and All; fold bolded-header bullets back into prose unless the format is a real spec or reference list.",
    },
    "no-compound-modifier-density": {
        "severity": "context_warning",
        "failure_modes": ["frictionless_structure", "generic_abstraction"],
        "evidence_role": "modifier_density",
        "guidance": "Restructure sentences with three or more stock hyphenated compounds; preserve only when the compounds are domain-specific terms of art.",
    },
    "no-knowledge-cutoff-disclaimers": {
        "severity": "strong_warning",
        "failure_modes": ["provenance_residue"],
        "evidence_role": "model_meta_residue",
        "guidance": "Fix at every depth; training-update and limited-information hedges are model meta-residue, not authorial uncertainty.",
    },
}


FAILURE_MODE_METADATA = {
    "provenance_residue": {
        "label": "Provenance residue",
        "summary": "Text leaks assistant, template, formatting, assignment, or publication-workflow residue.",
    },
    "synthetic_significance": {
        "label": "Synthetic significance",
        "summary": "Text performs importance, revelation, or depth without enough concrete support.",
    },
    "frictionless_structure": {
        "label": "Frictionless structure",
        "summary": "Text is packaged too evenly through headings, lists, repeated shapes, or tidy closures.",
    },
    "generic_abstraction": {
        "label": "Generic abstraction",
        "summary": "Text relies on portable abstractions, stock vocabulary, or low-specificity claims.",
    },
    "voice_erasure": {
        "label": "Voice erasure",
        "summary": "Text loses stance, concrete subjects, asymmetry, or authorial pressure.",
    },
    "genre_misfit": {
        "label": "Genre misfit",
        "summary": "Text uses a device that may be valid in one genre but suspicious in another.",
    },
}


def annotate_result(result):
    """Attach severity metadata without changing existing pass/fail semantics."""
    meta = CHECK_METADATA.get(result["text"], {
        "severity": "context_warning",
        "failure_modes": ["genre_misfit"],
        "evidence_role": "unclassified",
        "guidance": "Review in context.",
    })
    return {**result, **meta}


DEPTHS = ("balanced", "all")


def depth_consequence(result):
    """Describe what each severity means across rewrite depths."""
    severity = result["severity"]
    if severity == "hard_fail":
        return "Fix at Balanced and All."
    if severity == "strong_warning":
        return "Fix at Balanced and All unless the user explicitly accepts the risk after disclosure."
    return "Review at Balanced; All requires removal unless the user explicitly accepts the risk."


def action_for_depth(result, depth):
    """Return the required action for one failed check at a rewrite depth."""
    severity = result["severity"]
    if depth == "all":
        return "fix"
    if severity in {"hard_fail", "strong_warning"}:
        return "fix"
    return "preserve_with_disclosure_or_user_decision"


SEVERITY_LABELS = {
    "hard_fail": "Must fix",
    "strong_warning": "Strong AI-writing signal",
    "context_warning": "Context-sensitive signal",
}


ACTION_LABELS = {
    "fix": "Fix",
    "preserve_with_disclosure_or_user_decision": "Disclose or ask before preserving",
}


def check_report_text(check_name):
    """Return a plain-English label and description for a check."""
    return CHECK_REPORT_TEXT.get(
        check_name,
        (check_name.replace("-", " ").title(), "Checks for this AI-writing signal."),
    )


def friendly_evidence(result):
    """Convert check evidence into a concise human-facing explanation."""
    if result["text"] == "overall-ai-signal-pressure":
        score = result.get("score")
        threshold = result.get("threshold")
        components = list(result.get("components", []))
        vocab = result.get("vocabulary_pressure", {})
        vocab_points = vocab.get("points", 0)
        if components:
            component_text = ", ".join(components)
            sentence = (
                f"Stacked weak signals: {component_text}. Score: {score}/{threshold}. "
                "This points to machine-packaged structure rather than one isolated wording choice."
            )
            if vocab_points:
                sentence += f" Clustered AI vocabulary added {vocab_points} point(s)."
            return sentence
        return (
            f"Clustered AI vocabulary alone reached {vocab_points} point(s) at score {score}/{threshold}. "
            "The pressure check fired on vocabulary patterns rather than stacked structural signals."
        )
    evidence = result.get("evidence", "")
    list_match = re.search(r":\s*(\[[^\]]+\])", evidence)
    if not list_match:
        return evidence
    try:
        samples = ast.literal_eval(list_match.group(1))
    except (SyntaxError, ValueError):
        return evidence
    if not isinstance(samples, list):
        return evidence
    prefix = evidence[:list_match.start()].strip()
    if result["text"] == "no-triad-density":
        shown = samples[:3]
        sample_text = ", ".join(f'"{sample}"' for sample in shown)
        suffix = "" if len(samples) <= 3 else f", plus {len(samples) - 3} more"
        return f"{prefix}, including {sample_text}{suffix}."
    sample_text = ", ".join(f'"{sample}"' for sample in samples)
    return f"{prefix}: {sample_text}."


def sentence_text(text):
    """Ensure report fragments read as sentences."""
    stripped = str(text).strip()
    if not stripped:
        return stripped
    if stripped[-1] in ".!?":
        return stripped
    return f"{stripped}."


def confidence_assessment(results):
    """Assess confidence that the text shows AI-writing patterns, not authorship."""
    summary = score_summary(results)
    failures = summary["failed_checks"]
    severities = summary["failures_by_severity"]
    ai_pressure = summary.get("ai_signal_pressure") or {}
    hard = severities.get("hard_fail", 0)
    strong = severities.get("strong_warning", 0)
    context = severities.get("context_warning", 0)
    pressure_triggered = ai_pressure.get("triggered", False)

    if failures == 0:
        level = "Low"
        explanation = "No programmatic checks showed AI-writing patterns."
    elif hard or strong >= 3 or (pressure_triggered and failures >= 6) or failures >= 8:
        level = "High"
        explanation = (
            "Multiple strong or structural signals fired. Treat this as a high-confidence "
            "style diagnosis, not proof of authorship."
        )
    elif strong or pressure_triggered or failures >= 3:
        level = "Medium"
        explanation = (
            "Several signs of AI-like writing appeared, but the evidence is pattern-based "
            "and should be read in context."
        )
    else:
        level = "Low to medium"
        explanation = "Only a small number of context-sensitive signals appeared."

    basis = []
    if hard:
        basis.append(f"{hard} must-fix issue(s)")
    if strong:
        basis.append(f"{strong} strong AI-writing signal(s)")
    if context:
        basis.append(f"{context} context-sensitive signal(s)")
    if pressure_triggered:
        basis.append(
            f"AI pressure score reached {ai_pressure.get('score')}/{ai_pressure.get('threshold')}"
        )
    if not basis:
        basis.append("all checks passed")

    return {
        "level": level,
        "meaning": explanation,
        "basis": basis,
        "caveat": "This is a confidence assessment about AI-writing signs, not an authorship verdict.",
    }


def checks_table(results):
    """Return every check as a plain-English row for user-facing reports."""
    rows = []
    for result in results:
        label, description = check_report_text(result["text"])
        action = None
        if not result["passed"]:
            action = {
                depth: ACTION_LABELS.get(action_for_depth(result, depth), action_for_depth(result, depth))
                for depth in DEPTHS
            }
        rows.append({
            "check_id": result["text"],
            "check": label,
            "what_it_checks": description,
            "why_it_matters": CHECK_WHY_IT_MATTERS.get(result["text"], "This pattern can make prose read as generated or over-templated."),
            "status": "Clear" if result["passed"] else "Flagged",
            "severity": SEVERITY_LABELS.get(result["severity"], "Context-sensitive signal"),
            "why": "No issue found in this text." if result["passed"] else sentence_text(friendly_evidence(result)),
            "recommended_action": action or {depth: "None" for depth in DEPTHS},
        })
    return rows


def human_report(results):
    """Return a plain-English report contract for agents and end users."""
    summary = score_summary(results)
    confidence = confidence_assessment(results)
    ai_pressure = summary.get("ai_signal_pressure") or {}
    table = checks_table(results)
    failed = [row for row in table if row["status"] != "Clear"]
    failed_count = summary["failed_checks"]
    total = summary["total_checks"]
    if failed_count:
        overview = f"{failed_count} of {total} checks were flagged for AI-style writing patterns."
    else:
        overview = f"All {total} checks were clear."

    pressure_components = []
    vocab_points = 0
    for result in results:
        if result["text"] == "overall-ai-signal-pressure":
            pressure_components = list(result.get("components", []))
            vocab_points = result.get("vocabulary_pressure", {}).get("points", 0)
            break
    pressure_lead = (
        "AI-pressure looks for accumulation: weaker patterns that may be harmless alone "
        "but become more meaningful when they appear together. "
    )
    pressure_tail = (
        f"Score: {ai_pressure.get('score')}/{ai_pressure.get('threshold')}, "
        f"so this check {'was flagged' if ai_pressure.get('triggered') else 'stayed clear'}."
    )
    if pressure_components:
        vocab_clause = (
            f", plus {vocab_points} point(s) from clustered AI vocabulary"
            if vocab_points
            else ""
        )
        pressure_middle = (
            f"Here the stacked signals were {', '.join(pressure_components)}{vocab_clause}. "
            "That means the draft looked machine-packaged, with too much visible structure "
            "and too little natural variation. "
        )
    elif vocab_points:
        pressure_middle = (
            f"The only contribution here was {vocab_points} point(s) from clustered AI vocabulary. "
        )
    else:
        pressure_middle = (
            "This text did not stack enough weak signals to suggest machine-packaged structure. "
        )
    ai_pressure_explanation = pressure_lead + pressure_middle + pressure_tail

    return {
        "overview": overview,
        "score": {
            "status": summary["check_status"],
            "failed_checks": failed_count,
            "total_checks": total,
            "pass_rate": summary["pass_rate"],
            "severity_counts": {
                SEVERITY_LABELS.get(key, key): value
                for key, value in summary["failures_by_severity"].items()
            },
        },
        "confidence": confidence,
        "ai_pressure_explanation": ai_pressure_explanation,
        "failed_checks": failed,
        "all_checks": table,
    }


def table_cell(value):
    """Escape a value for a Markdown table cell."""
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_checks_table(rows, depth):
    """Render every check row as a Markdown table."""
    depth_key = depth.lower()
    header = f"| Check | Status | What it looks for | What happened here | Why this matters | {depth_key.title()} action |"
    lines = [header, "|---|---|---|---|---|---|"]
    for row in rows:
        action = row["recommended_action"].get(depth_key, row["recommended_action"].get("all", "None"))
        lines.append(
            "| "
            + " | ".join([
                table_cell(row["check"]),
                table_cell(row["status"]),
                table_cell(row["what_it_checks"]),
                table_cell(row["why"]),
                table_cell(row["why_it_matters"]),
                table_cell(action),
            ])
            + " |"
        )
    return "\n".join(lines)


def format_human_report(results, depth="all", heading="Initial assessment"):
    """Render the plain-English report contract as user-facing Markdown."""
    depth_key = depth.lower()
    report = human_report(results)
    confidence = report["confidence"]
    lines = [
        heading,
        f"Summary: {report['overview']}",
        "",
        f"Confidence: {confidence['level']}. {confidence['meaning']}",
        f"Basis: {'; '.join(confidence['basis'])}.",
        f"Note: {confidence['caveat']}",
        "",
        f"AI-pressure explanation: {report['ai_pressure_explanation']}",
        "",
        "Main issues found",
    ]
    if report["failed_checks"]:
        for row in report["failed_checks"]:
            action = row["recommended_action"].get(depth_key, row["recommended_action"].get("all", "Fix"))
            lines.append(
                f"- {row['check']}: {row['status']}. "
                f"What it looks for: {row['what_it_checks']} "
                f"What happened here: {sentence_text(row['why'])} "
                f"Why this matters: {row['why_it_matters']} "
                f"{depth_key.title()} action: {action}."
            )
    else:
        lines.append("- None.")
    lines.extend([
        "",
        "Full check table",
        "",
        markdown_checks_table(report["all_checks"], depth_key),
    ])
    return "\n".join(lines)


def triggered_checks(results):
    """Return each failed check exactly once for user-facing reports."""
    triggered = []
    for result in results:
        if result["passed"]:
            continue
        triggered.append({
            "check": result["text"],
            "severity": result["severity"],
            "failure_modes": result.get("failure_modes", ["genre_misfit"]),
            "evidence_role": result.get("evidence_role", "unclassified"),
            "evidence": result.get("evidence", ""),
            "guidance": result.get("guidance", "Review in context."),
            "depth_consequence": depth_consequence(result),
            "depth_actions": {
                depth: action_for_depth(result, depth) for depth in DEPTHS
            },
        })
    return triggered


def score_summary(results):
    """Return structured totals for human-facing reports."""
    passed = sum(1 for result in results if result["passed"])
    total = len(results)
    failures = [result for result in results if not result["passed"]]
    failures_by_severity = {}
    for result in failures:
        failures_by_severity[result["severity"]] = failures_by_severity.get(result["severity"], 0) + 1

    overall_signal = next(
        (result for result in results if result["text"] == "overall-ai-signal-pressure"),
        None,
    )
    ai_signal_pressure = None
    if overall_signal:
        ai_signal_pressure = {
            "score": overall_signal.get("score"),
            "threshold": overall_signal.get("threshold"),
            "triggered": not overall_signal["passed"],
            "components": overall_signal.get("components", []),
            "vocabulary_pressure": overall_signal.get("vocabulary_pressure", {}),
        }

    return {
        "check_status": "fail" if failures else "pass",
        "passed_checks": passed,
        "failed_checks": len(failures),
        "total_checks": total,
        "pass_rate": f"{passed}/{total}",
        "failures_by_severity": failures_by_severity,
        "ai_signal_pressure": ai_signal_pressure,
    }


def failure_mode_results(results):
    """Group failed checks by failure mode without changing legacy report fields."""
    grouped = {
        key: {
            **meta,
            "failed_checks": [],
            "check_refs": [],
            "failures_by_severity": {},
        }
        for key, meta in FAILURE_MODE_METADATA.items()
    }

    for result in results:
        if result["passed"]:
            continue
        for failure_mode in result.get("failure_modes", ["genre_misfit"]):
            group = grouped.setdefault(failure_mode, {
                "label": failure_mode.replace("_", " ").title(),
                "summary": "Unclassified failure mode.",
                "failed_checks": [],
                "check_refs": [],
                "failures_by_severity": {},
            })
            severity = result["severity"]
            group["failures_by_severity"][severity] = group["failures_by_severity"].get(severity, 0) + 1
            group["check_refs"].append(result["text"])
            group["failed_checks"].append({
                "check": result["text"],
                "severity": severity,
                "evidence_role": result.get("evidence_role", "unclassified"),
                "evidence": result.get("evidence", ""),
                "guidance": result.get("guidance", "Review in context."),
                "depth_consequence": depth_consequence(result),
                "depth_actions": {
                    depth: action_for_depth(result, depth) for depth in DEPTHS
                },
            })

    return grouped


def depth_results(results):
    """Summarise readiness by rewrite depth.

    Balanced does not silently approve preserved warnings; it indicates what
    still needs disclosure or user decision. All requires a clean pass.
    """
    failures = [r for r in results if not r["passed"]]
    by_severity = {}
    for result in failures:
        by_severity.setdefault(result["severity"], []).append(result["text"])

    hard_failures = by_severity.get("hard_fail", [])
    strong_warnings = by_severity.get("strong_warning", [])
    context_warnings = by_severity.get("context_warning", [])
    check_status = "fail" if failures else "pass"

    return {
        "balanced": {
            "status": check_status,
            "check_status": check_status,
            "required_fixes": hard_failures + strong_warnings,
            "preservable_with_disclosure": context_warnings,
            "user_decision_needed": context_warnings,
            "must_fix": hard_failures + strong_warnings,
            "needs_user_decision": context_warnings,
            "summary": (
                "Hard failures or strong warnings remain; fix or ask user before Balanced depth output."
                if hard_failures or strong_warnings
                else (
                    "No hard failures or strong warnings; context warnings need user decision."
                    if context_warnings
                    else "No hard failures, strong warnings, or context warnings."
                )
            ),
        },
        "all": {
            "status": check_status,
            "check_status": check_status,
            "required_fixes": [r["text"] for r in failures],
            "preservable_with_disclosure": [],
            "user_decision_needed": [],
            "must_fix": [r["text"] for r in failures],
            "needs_user_decision": [],
            "summary": (
                "All checks pass."
                if not failures
                else "One or more checks fail; All depth requires a clean pass unless user explicitly accepts risk."
            ),
        },
    }


def grade_file(filepath, assertion_names=None):
    """Grade a file against specified assertions (or all if none specified)."""
    text = Path(filepath).read_text()
    results = []
    checks_to_run = assertion_names or ALL_CHECKS.keys()
    for name in checks_to_run:
        if name in ALL_CHECKS:
            results.append(annotate_result(ALL_CHECKS[name](text)))
    return results


# ---------------------------------------------------------------------------
# Audit-shape assertions
# ---------------------------------------------------------------------------
# These checks evaluate the *agent's output* against the user's *input*, not
# the prose itself. They live in their own registry because they take two
# arguments (output_text, input_text) and produce contract-shape results, not
# AI-writing-pattern results. They are not annotated with severity metadata.

AUDIT_HEADER_RE = re.compile(r"^\*\*Audit[,]?[^*]*\*\*\s*$", re.MULTILINE)
REWRITE_HEADER_RE = re.compile(r"^\*\*Rewrite\*\*\s*$", re.MULTILINE)
DRAFT_HEADER_RE = re.compile(r"^\*\*Draft\*\*\s*$", re.MULTILINE)
SUGGESTIONS_HEADER_RE = re.compile(r"^\*\*Suggestions[,]?[^*]*\*\*\s*$", re.MULTILINE)
AGENT_JUDGEMENT_HEADER_RE = re.compile(r"^\*\*Agent[- ]judgement reading[^*]*\*\*\s*$", re.MULTILINE)
SECTION_HEADER_RE = re.compile(r"^\*\*[^*]+\*\*\s*$", re.MULTILINE)
QUOTED_PHRASE_RE = re.compile(r'["“]([^"”]+)["”]')

# Phase 1 all-clear shape (per humanise/SKILL.md after U4): a single line
# stating both blocks came back clean. Phase 3 (U11/U12) will replace this
# with the canonical "X of X clear · agent reading clean · pressure: clear"
# shape; for U5 we match the Phase-1 form.
ALL_CLEAR_LINE_RE = re.compile(
    r"audit clean[:.]?\s+no\s+ai\s+tells?\s+detected,?\s+agent\s+reading\s+clean",
    re.IGNORECASE,
)


def _section_text(output_text, header_re):
    """Return the text of a section starting at header_re, ending at the next bold header."""
    match = header_re.search(output_text)
    if not match:
        return None
    start = match.end()
    next_match = SECTION_HEADER_RE.search(output_text, start)
    end = next_match.start() if next_match else len(output_text)
    return output_text[start:end]


def _audit_section(output_text):
    return _section_text(output_text, AUDIT_HEADER_RE)


def _suggestions_section(output_text):
    return _section_text(output_text, SUGGESTIONS_HEADER_RE)


def _flag_blocks(audit_text):
    """Return paragraphs in the audit that contain a 'Why:' line."""
    if not audit_text:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", audit_text) if p.strip()]
    return [p for p in paragraphs if re.search(r"^\s*Why\s*:", p, re.MULTILINE)]


def _suggestion_blocks(suggestions_text):
    """Return paragraphs in the suggestions section that contain a 'Try' marker."""
    if not suggestions_text:
        return []
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", suggestions_text) if p.strip()]
    return [p for p in paragraphs if re.search(r"^\s*Try\s*[:\s]", p, re.MULTILINE)]


def check_audit_shape_block_precedes_rewrite_block(output_text, input_text=None):
    """Verify the audit appears before any rewrite or suggestions block."""
    name = "audit-shape-block-precedes-rewrite-block"
    audit = AUDIT_HEADER_RE.search(output_text)
    rewrite = REWRITE_HEADER_RE.search(output_text) or DRAFT_HEADER_RE.search(output_text)
    suggestions = SUGGESTIONS_HEADER_RE.search(output_text)
    if rewrite and suggestions:
        follow = rewrite if rewrite.start() < suggestions.start() else suggestions
    else:
        follow = rewrite or suggestions
    if not audit:
        return {"text": name, "passed": False, "evidence": "No audit header found in output"}
    if not follow:
        return {"text": name, "passed": False, "evidence": "No rewrite, draft, or suggestions header found in output"}
    if audit.start() < follow.start():
        return {"text": name, "passed": True, "evidence": f"audit at offset {audit.start()}; follow-up at offset {follow.start()}"}
    return {"text": name, "passed": False, "evidence": f"follow-up appears before audit (audit={audit.start()}, follow={follow.start()})"}


def check_every_flag_block_contains_input_substring(output_text, input_text=None):
    """Each flag block must quote a phrase that appears in the input."""
    name = "every-flag-block-contains-input-substring"
    if input_text is None:
        return {"text": name, "passed": False, "evidence": "input_text required for this check"}
    blocks = _flag_blocks(_audit_section(output_text))
    if not blocks:
        return {"text": name, "passed": True, "evidence": "no flag blocks (vacuously true)"}
    misses = []
    for block in blocks:
        if re.search(r"^\s*Where\s*:", block, re.MULTILINE):
            continue  # structural patterns describe location, not quotable phrase
        phrases = QUOTED_PHRASE_RE.findall(block)
        if not phrases or not any(phrase in input_text for phrase in phrases):
            misses.append(block.split("\n", 1)[0])
    if misses:
        return {"text": name, "passed": False, "evidence": f"{len(misses)} block(s) lack input-matching quotes: {misses[:3]}"}
    return {"text": name, "passed": True, "evidence": f"all {len(blocks)} flag block(s) anchor to input"}


def check_every_flag_block_has_explanation(output_text, input_text=None):
    """Each flag block must include a 'Why:' line."""
    name = "every-flag-block-has-explanation"
    audit = _audit_section(output_text)
    if not audit:
        return {"text": name, "passed": False, "evidence": "no audit section found"}
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", audit) if p.strip()]
    candidates = [p for p in paragraphs if re.search(r'(^\s*-\s*["“])|(^\s*Where\s*:)|(^\s*Why\s*:)', p, re.MULTILINE)]
    if not candidates:
        return {"text": name, "passed": True, "evidence": "no flag blocks (vacuously true)"}
    missing = [p.split("\n", 1)[0] for p in candidates if not re.search(r"^\s*Why\s*:", p, re.MULTILINE)]
    if missing:
        return {"text": name, "passed": False, "evidence": f"{len(missing)} flag block(s) missing 'Why:': {missing[:3]}"}
    return {"text": name, "passed": True, "evidence": f"all {len(candidates)} flag block(s) include 'Why:'"}


def check_final_non_empty_line_ends_with_question(output_text, input_text=None):
    """The output's last non-empty line must end with '?'."""
    name = "final-non-empty-line-ends-with-question"
    lines = [line for line in output_text.rstrip().split("\n") if line.strip()]
    if not lines:
        return {"text": name, "passed": False, "evidence": "output is empty"}
    last = lines[-1].rstrip()
    if last.endswith("?"):
        return {"text": name, "passed": True, "evidence": f"final line: {last[:80]}"}
    return {"text": name, "passed": False, "evidence": f"final line does not end with '?': {last[:80]}"}


def check_no_large_prose_block_not_in_input(output_text, input_text=None):
    """Audit-only outputs must not contain a rewrite or draft block."""
    name = "no-large-prose-block-not-in-input"
    rewrite = REWRITE_HEADER_RE.search(output_text)
    draft = DRAFT_HEADER_RE.search(output_text)
    if rewrite:
        return {"text": name, "passed": False, "evidence": f"found **Rewrite** header at offset {rewrite.start()}"}
    if draft:
        return {"text": name, "passed": False, "evidence": f"found **Draft** header at offset {draft.start()}"}
    return {"text": name, "passed": True, "evidence": "no rewrite or draft block present"}


def check_suggestion_block_count_equals_flag_count(output_text, input_text=None):
    """Number of suggestion blocks must equal number of flag blocks."""
    name = "suggestion-block-count-equals-flag-count"
    flag_count = len(_flag_blocks(_audit_section(output_text)))
    suggestion_count = len(_suggestion_blocks(_suggestions_section(output_text)))
    if flag_count == suggestion_count:
        return {"text": name, "passed": True, "evidence": f"{flag_count} flag(s) and {suggestion_count} suggestion(s) match"}
    return {"text": name, "passed": False, "evidence": f"{flag_count} flag(s) vs {suggestion_count} suggestion(s)"}


def check_every_suggestion_block_has_replacement(output_text, input_text=None):
    """Each suggestion block must contain a 'Try' replacement."""
    name = "every-suggestion-block-has-replacement"
    suggestions = _suggestions_section(output_text)
    if suggestions is None:
        return {"text": name, "passed": True, "evidence": "no suggestions section (vacuously true)"}
    blocks = _suggestion_blocks(suggestions)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", suggestions) if p.strip()]
    flag_like = [p for p in paragraphs if re.search(r'(^\s*-\s*["“])|(^\s*Where\s*:)|(^\s*Try\s*[:\s])', p, re.MULTILINE)]
    if not flag_like:
        return {"text": name, "passed": False, "evidence": "suggestions section has no flag-shaped blocks"}
    missing = [p.split("\n", 1)[0] for p in flag_like if not re.search(r"^\s*Try\s*[:\s]", p, re.MULTILINE)]
    if missing:
        return {"text": name, "passed": False, "evidence": f"{len(missing)} suggestion block(s) missing 'Try': {missing[:3]}"}
    return {"text": name, "passed": True, "evidence": f"all {len(blocks)} suggestion block(s) include 'Try'"}


def check_audit_shape_has_programmatic_block(output_text, input_text=None):
    """An Audit response must carry the programmatic block (`**Audit, ...**`)
    or be in the all-clear single-line shape."""
    name = "audit-shape-has-programmatic-block"
    if AUDIT_HEADER_RE.search(output_text):
        return {"text": name, "passed": True, "evidence": "**Audit** header present"}
    if ALL_CLEAR_LINE_RE.search(output_text):
        return {"text": name, "passed": True, "evidence": "all-clear single-line shape (programmatic block implicit)"}
    return {"text": name, "passed": False, "evidence": "no **Audit** header and no all-clear line"}


def check_audit_shape_has_agent_judgement_block(output_text, input_text=None):
    """An Audit response must carry the agent-judgement block
    (`**Agent-judgement reading...**`) or be in the all-clear single-line shape.

    Phase 1 (U4) introduced the block; Phase 3 (U12) will redesign it but
    keep the header recognisable. This check holds across both phases."""
    name = "audit-shape-has-agent-judgement-block"
    if AGENT_JUDGEMENT_HEADER_RE.search(output_text):
        return {"text": name, "passed": True, "evidence": "**Agent-judgement reading** header present"}
    if ALL_CLEAR_LINE_RE.search(output_text):
        return {"text": name, "passed": True, "evidence": "all-clear single-line shape (agent-judgement block implicit)"}
    return {"text": name, "passed": False, "evidence": "no **Agent-judgement reading** header and no all-clear line"}


def check_audit_shape_all_clear_line_format(output_text, input_text=None):
    """When neither block is present in the output, the response is expected
    to be the all-clear single-line shape: `Audit clean: no AI tells detected,
    agent reading clean.` followed by the next-step question.

    On non-all-clear outputs (where the bold headers are present), the check
    vacuously passes — the all-clear shape only applies to all-clear runs.
    """
    name = "audit-shape-all-clear-line-format"
    has_programmatic = bool(AUDIT_HEADER_RE.search(output_text))
    has_agent_judgement = bool(AGENT_JUDGEMENT_HEADER_RE.search(output_text))
    if has_programmatic or has_agent_judgement:
        return {"text": name, "passed": True, "evidence": "non-all-clear output (vacuously passes)"}
    if ALL_CLEAR_LINE_RE.search(output_text):
        return {"text": name, "passed": True, "evidence": "all-clear single-line shape matches Phase-1 canonical form"}
    return {"text": name, "passed": False, "evidence": "all-clear shape expected but neither block headers nor canonical line found"}


AUDIT_SHAPE_CHECKS = {
    "audit-shape-block-precedes-rewrite-block": check_audit_shape_block_precedes_rewrite_block,
    "every-flag-block-contains-input-substring": check_every_flag_block_contains_input_substring,
    "every-flag-block-has-explanation": check_every_flag_block_has_explanation,
    "final-non-empty-line-ends-with-question": check_final_non_empty_line_ends_with_question,
    "no-large-prose-block-not-in-input": check_no_large_prose_block_not_in_input,
    "suggestion-block-count-equals-flag-count": check_suggestion_block_count_equals_flag_count,
    "every-suggestion-block-has-replacement": check_every_suggestion_block_has_replacement,
    "audit-shape-has-programmatic-block": check_audit_shape_has_programmatic_block,
    "audit-shape-has-agent-judgement-block": check_audit_shape_has_agent_judgement_block,
    "audit-shape-all-clear-line-format": check_audit_shape_all_clear_line_format,
}


def check_audit_shape(check_name, output_text, input_text=None):
    """Run a single audit-shape check by name."""
    fn = AUDIT_SHAPE_CHECKS.get(check_name)
    if fn is None:
        raise KeyError(f"Unknown audit-shape check: {check_name!r}; known: {sorted(AUDIT_SHAPE_CHECKS)}")
    return fn(output_text, input_text)


# ---------------------------------------------------------------------------
# Re-grading helper
# ---------------------------------------------------------------------------

def regrade(text, depth="balanced"):
    """Re-grade prose at a chosen depth.

    Returns a dict with depth-aware fail counts so an eval grader can verify
    that a rewrite or draft cleared what the chosen depth requires.

    Keys:
        depth: the depth queried.
        results: every annotated check result (passed and failed).
        fails: count of failures the chosen depth requires fixing.
        failed_checks: names of those failures.
        all_failures: count of all failures regardless of depth.
        all_failed_checks: names of all failed checks.
    """
    if depth not in DEPTHS:
        raise ValueError(f"depth must be one of {DEPTHS}, got {depth!r}")
    results = [annotate_result(fn(text)) for fn in ALL_CHECKS.values()]
    failures = [r for r in results if not r["passed"]]
    must_fix = [r for r in failures if action_for_depth(r, depth) == "fix"]
    return {
        "depth": depth,
        "results": results,
        "fails": len(must_fix),
        "failed_checks": [r["text"] for r in must_fix],
        "all_failures": len(failures),
        "all_failed_checks": [r["text"] for r in failures],
    }


USAGE = "Usage: grade.py [--format json|markdown] [--depth balanced|all] <file> [assertion1,assertion2,...]"


def main():
    args = sys.argv[1:]
    output_format = "json"
    depth = "all"

    if "--format" in args:
        index = args.index("--format")
        try:
            output_format = args[index + 1]
        except IndexError:
            print(USAGE)
            sys.exit(1)
        del args[index:index + 2]

    if "--depth" in args:
        index = args.index("--depth")
        try:
            depth = args[index + 1].lower()
        except IndexError:
            print(USAGE)
            sys.exit(1)
        del args[index:index + 2]

    if output_format not in {"json", "markdown"} or depth not in DEPTHS or not args:
        print(USAGE)
        sys.exit(1)

    filepath = args[0]
    assertions = args[1].split(",") if len(args) > 1 else None

    results = grade_file(filepath, assertions)

    summary = score_summary(results)

    if output_format == "markdown":
        print(format_human_report(results, depth=depth))
        return

    output = {
        "file": filepath,
        "pass_rate": summary["pass_rate"],
        "failures_by_severity": summary["failures_by_severity"],
        "score_summary": summary,
        "human_report": human_report(results),
        "triggered_checks": triggered_checks(results),
        "failure_mode_results": failure_mode_results(results),
        "depth_results": depth_results(results),
        "expectations": results,
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
