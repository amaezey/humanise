#!/usr/bin/env python3
"""Fetch 19th/20th-century human source fixtures into Markdown."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "samples" / "human-sourced"
MANIFEST = OUT_DIR / "manifest.json"

HEADERS = {"User-Agent": "Mozilla/5.0 human-eyes-eval-fetcher"}


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u2014", "--").replace("\u2013", "-")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch(url: str) -> str:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    text = response.text
    if "<html" in text[:1000].lower() or url.endswith((".htm", ".html")):
        soup = BeautifulSoup(text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text("\n")
    return clean_text(text)


def between(text: str, start: str, end: str | None = None, occurrence: str = "first") -> str:
    start_matches = list(re.finditer(start, text, flags=re.IGNORECASE | re.MULTILINE))
    if not start_matches:
        raise ValueError(f"start marker not found: {start}")
    start_match = start_matches[-1] if occurrence == "last" else start_matches[0]
    start_index = start_match.end()
    if end:
        end_match = re.search(end, text[start_index:], flags=re.IGNORECASE | re.MULTILINE)
        if not end_match:
            raise ValueError(f"end marker not found: {end}")
        return clean_text(text[start_index : start_index + end_match.start()])
    return clean_text(text[start_index:])


def first_words(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).strip()


def markdown_for(sample: dict, text: str, source_url: str, note: str) -> str:
    metadata = {
        "id": sample["id"],
        "title": sample["title"],
        "author": sample["author"],
        "year": sample["year"],
        "period": sample["period"],
        "format": sample["format"],
        "source_url": source_url,
        "extract_note": note,
        "expected_use": sample["expected_use"],
        "voice_targets": sample["voice_targets"],
    }
    return "---\n" + json.dumps(metadata, indent=2, ensure_ascii=False) + "\n---\n\n" + clean_text(text) + "\n"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    by_id = {sample["id"]: sample for sample in manifest["samples"]}

    specs = [
        {
            "id": "19c-austen-pride-and-prejudice",
            "url": "https://www.gutenberg.org/files/1342/1342-0.txt",
            "start": r"^Chapter I\.\]\s*$",
            "end": r"^CHAPTER II\.\s*$",
            "note": "Chapter I excerpt",
        },
        {
            "id": "19c-poe-tell-tale-heart",
            "url": "https://www.gutenberg.org/files/2148/2148-0.txt",
            "start": r"^\s*THE TELL-TALE HEART\.?\s*$",
            "end": r"^\s*BERENICE\s*$",
            "occurrence": "last",
            "note": "Short story excerpt from Poe collection",
        },
        {
            "id": "19c-gilman-yellow-wallpaper",
            "url": "https://www.gutenberg.org/files/1952/1952-0.txt",
            "start": r"^\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*\*\*\*",
            "end": r"^\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*\*\*\*",
            "note": "Complete short story",
        },
        {
            "id": "19c-darwin-origin",
            "url": "https://www.gutenberg.org/files/1228/1228-0.txt",
            "start": r"^INTRODUCTION\.\s*$",
            "end": r"^CHAPTER I\.\s*$",
            "occurrence": "last",
            "note": "Introduction excerpt",
        },
        {
            "id": "20c-dubois-souls",
            "url": "https://www.gutenberg.org/files/408/408-0.txt",
            "start": r"^Of Our Spiritual Strivings\s*$",
            "end": r"^Of the Dawn of Freedom\s*$",
            "note": "Chapter I excerpt",
        },
        {
            "id": "20c-glaspell-jury-of-her-peers",
            "url": "https://www.gutenberg.org/files/20872/20872-h/20872-h.htm",
            "start": r"^A JURY OF HER PEERS",
            "end": r"^THE END\s*$|^\*\*\* END OF THIS PROJECT GUTENBERG EBOOK",
            "note": "Short story excerpt",
        },
        {
            "id": "20c-woolf-room",
            "url": "https://gutenberg.net.au/ebooks02/0200791.txt",
            "start": r"^ONE\s*$",
            "end": r"^TWO\s*$",
            "note": "Chapter 1 excerpt",
        },
        {
            "id": "20c-christie-styles",
            "url": "https://www.gutenberg.org/files/863/863-0.txt",
            "start": r"^CHAPTER I\.\s*$",
            "end": r"^CHAPTER II\.\s*$",
            "occurrence": "last",
            "note": "Chapter I excerpt",
        },
    ]

    for spec in specs:
        sample = by_id[spec["id"]]
        source = fetch(spec["url"])
        try:
            text = between(source, spec["start"], spec["end"], spec.get("occurrence", "first"))
        except ValueError as exc:
            raise RuntimeError(f"{spec['id']}: {exc}") from exc
        text = first_words(text, 3500)
        path = OUT_DIR / f"{sample['id']}.md"
        path.write_text(markdown_for(sample, text, spec["url"], spec["note"]))
        sample["fixture_path"] = str(path.relative_to(ROOT.parent.parent))
        sample["word_count"] = len(text.split())
        sample["extract_note"] = spec["note"]
        print(f"wrote {path} ({sample['word_count']} words)")

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
