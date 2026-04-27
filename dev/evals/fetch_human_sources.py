#!/usr/bin/env python3
"""Fetch and extract user-nominated human source samples.

This is intentionally pragmatic rather than a general crawler. It extracts the
main readable text from the eight sources in human-sourced/manifest.json and
expands the Enchanting Marketing index into linked sample pages.
"""

from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "samples" / "human-sourced"
MANIFEST = OUT_DIR / "manifest.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

NOISE_SELECTORS = [
    "#comments",
    "#respond",
    ".comments",
    ".comments-area",
    ".comment",
    ".comment-content",
    ".comment-list",
    ".comment-respond",
    ".entry-comments",
    ".reader-comments",
    ".respond",
    ".sidebar",
    ".widget",
    ".wp-block-comments",
    "[class*='comment-']",
    "[id*='comment-']",
]


@dataclass
class Extracted:
    url: str
    title: str
    text: str
    status_code: int
    method: str


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:90]


def clean_text(value: str) -> str:
    value = value.replace("\xa0", " ")
    value = value.replace("\u2014", "--")
    value = value.replace("\u2013", "-")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def paragraph_text(nodes: Iterable) -> list[str]:
    paragraphs: list[str] = []
    for node in nodes:
        text = clean_text(node.get_text(" ", strip=True))
        if not text:
            continue
        if len(text) < 25 and not re.search(r"[.!?]$", text):
            continue
        if re.search(r"^(subscribe|advertisement|share this|sign up|related|comments?)$", text, re.I):
            continue
        paragraphs.append(text)
    return paragraphs


def best_article_node(soup: BeautifulSoup):
    selectors = [
        "article",
        "main article",
        "main",
        ".entry-content",
        ".post-content",
        ".article-content",
        ".article-body",
        ".story-body",
        ".meteredContent",
        "#story",
        "#content",
    ]
    candidates = []
    for selector in selectors:
        for node in soup.select(selector):
            text_len = len(node.get_text(" ", strip=True))
            p_count = len(node.find_all(["p", "li", "blockquote"]))
            if text_len > 500 and p_count >= 3:
                candidates.append((text_len, p_count, selector, node))
    if candidates:
        candidates.sort(reverse=True, key=lambda x: (x[0], x[1]))
        return candidates[0][3], candidates[0][2]
    body = soup.body or soup
    return body, "body"


def fetch_html(url: str) -> tuple[int, str]:
    response = requests.get(url, headers=HEADERS, timeout=12)
    return response.status_code, response.text


def extract_page(url: str) -> Extracted:
    status, html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg", "form", "nav", "footer", "header"]):
        tag.decompose()
    for selector in NOISE_SELECTORS:
        for tag in soup.select(selector):
            tag.decompose()

    title_node = soup.find("meta", property="og:title") or soup.find("title")
    title = ""
    if title_node:
        title = title_node.get("content") if title_node.name == "meta" else title_node.get_text(" ", strip=True)
    title = clean_text(title or urlparse(url).path.rsplit("/", 1)[-1] or url)

    article, method = best_article_node(soup)
    paragraphs = paragraph_text(article.find_all(["p", "li", "blockquote"]))
    text = "\n\n".join(paragraphs)
    return Extracted(url=url, title=title, text=clean_text(text), status_code=status, method=method)


def markdown_for(sample: dict, extracted: Extracted) -> str:
    metadata = {
        "id": sample["id"],
        "title": sample["title"],
        "author": sample["author"],
        "year": sample["year"],
        "period": sample["period"],
        "format": sample["format"],
        "source_url": extracted.url,
        "fetch_status": extracted.status_code,
        "extract_method": extracted.method,
        "expected_use": sample["expected_use"],
        "voice_targets": sample["voice_targets"],
    }
    return (
        "---\n"
        + json.dumps(metadata, indent=2, ensure_ascii=False)
        + "\n---\n\n"
        + extracted.text
        + "\n"
    )


def discover_enchanting_links(url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    article, _ = best_article_node(soup)
    links: list[str] = []
    for a in article.select("a[href]"):
        href = urljoin(url, a["href"])
        parsed = urlparse(href)
        if parsed.netloc != "www.enchantingmarketing.com":
            continue
        if href.rstrip("/") == url.rstrip("/"):
            continue
        text = a.get_text(" ", strip=True).lower()
        path = parsed.path.strip("/")
        if not path:
            continue
        if any(skip in path for skip in ("tag/", "category/", "author/", "privacy", "newsletter", "shop", "about", "contact", "books-and-courses", "mugs-for-writers", "free-writing-course")):
            continue
        if (
            "read more" in text
            or "examples" in text
            or "techniques" in text
            or path in {"how-to-simplify-writing", "how-to-improve-writing-skills"}
        ):
            links.append(href.split("#", 1)[0])
    seen = []
    for link in links:
        if link not in seen:
            seen.append(link)
    return seen[:40]


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    samples = manifest["samples"]
    written: list[str] = []

    for stale in OUT_DIR.glob("21c-enchanting-marketing-example-*.md"):
        stale.unlink()

    for sample in samples:
        if not sample["id"].startswith("21c-"):
            continue
        extracted = extract_page(sample["source_url"])
        fixture_path = OUT_DIR / f"{sample['id']}.md"
        fixture_path.write_text(markdown_for(sample, extracted))
        sample["fixture_path"] = str(fixture_path.relative_to(ROOT.parent.parent))
        sample["fetch_status"] = extracted.status_code
        sample["extract_method"] = extracted.method
        sample["word_count"] = len(extracted.text.split())
        written.append(str(fixture_path))
        print(f"wrote {fixture_path} ({sample['word_count']} words, status {extracted.status_code})", flush=True)
        time.sleep(0.5)

        if sample["id"] == "21c-enchanting-marketing-writing-examples":
            _, html = fetch_html(sample["source_url"])
            links = discover_enchanting_links(sample["source_url"], html)
            sample["discovered_sample_links"] = links
            for index, link in enumerate(links, 1):
                child = extract_page(link)
                child_id = f"21c-enchanting-marketing-example-{index:02d}-{slugify(child.title)}"
                child_sample = {
                    "id": child_id,
                    "title": child.title,
                    "author": "Enchanting Marketing",
                    "year": 2020,
                    "period": "21st",
                    "format": "instructional web writing sample",
                    "source_url": link,
                    "expected_use": ["style_reference", "false_positive_audit"],
                    "voice_targets": ["web-native teaching", "copywriting example", "clear direct address"],
                }
                child_path = OUT_DIR / f"{child_id}.md"
                child_path.write_text(markdown_for(child_sample, child))
                written.append(str(child_path))
                print(f"wrote {child_path} ({len(child.text.split())} words, status {child.status_code})", flush=True)
                time.sleep(0.35)

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"updated {MANIFEST}", flush=True)
    print(f"total files written: {len(written)}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
