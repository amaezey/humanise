#!/usr/bin/env python3
"""extract_direct_html_snapshot.py — Extract article markdown from saved HTML.

Used when Jina Reader cannot fetch a URL (paywall, anti-bot, etc.) and we
have to operate on a locally saved HTML file instead. Produces a markdown
snapshot at OUT_PATH with a header block (source URL, retrieval date,
optional author / published date) followed by the article body with HTML
stripped and paragraph breaks preserved.

Extraction fallback chain:
    1. JSON-LD `articleBody`
    2. Site-specific paragraph CSS classes (see SITE_SELECTORS)
    3. Generic `<article>` / `<main>` body
    4. og:description meta tag

Usage:
    python3 extract_direct_html_snapshot.py SLUG SOURCE_URL HTML_PATH OUT_PATH

Stdlib only — no third-party dependencies.
"""

from __future__ import annotations

import datetime
import html as html_lib
import json
import re
import sys
from pathlib import Path

# Site-specific paragraph / container selectors keyed by a substring expected
# in the source URL. The snapshot tool walks this dict in order, so put more
# specific entries first if any ever overlap. Generic <article>/<main> fallbacks
# stay outside this dict — they apply regardless of the source.
SITE_SELECTORS = {
    # Substack publications wrap each article paragraph in <p class="...slate-paragraph...">.
    "substack.com": {"paragraph_class": "slate-paragraph"},
    # The New Yorker uses <section class="body main-article-body">...</section>.
    "newyorker.com": {"section_class": "body main-article-body"},
    # Blogger / Blogspot uses <div class="post-body">, terminated by a
    # `<!-- START SUBSCRIBE` comment sentinel before the subscribe widget.
    "blogspot.com": {
        "div_class": "post-body",
        "terminator": "<!-- START SUBSCRIBE",
    },
}


# ---------- HTML cleaning ----------

_SCRIPT_RE = re.compile(r"<script\b.*?</script>", re.IGNORECASE | re.DOTALL)
_STYLE_RE = re.compile(r"<style\b.*?</style>", re.IGNORECASE | re.DOTALL)
_BR_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_CLOSE_P_RE = re.compile(r"</p>", re.IGNORECASE)
_TAG_RE = re.compile(r"<[^>]+>")
_NBSP_RE = re.compile(r" ")
_SPACE_RUN_RE = re.compile(r"[ \t]+")
_LEADING_SPACE_RE = re.compile(r"\n[ \t]+")
_BLANK_LINE_RUN_RE = re.compile(r"\n{3,}")
_NOISE_TAGS_RE = re.compile(
    r"<(?:nav|script|style|aside|footer|form|iframe)\b.*?</(?:nav|script|style|aside|footer|form|iframe)>",
    re.IGNORECASE | re.DOTALL,
)
_BLOCK_CHUNK_RE = re.compile(
    r"<(h[1-4]|p|li)[^>]*>(.*?)</\1>",
    re.IGNORECASE | re.DOTALL,
)


def clean_html(text: str) -> str:
    """Strip tags, normalise whitespace, preserve paragraph breaks."""
    if not text:
        return ""
    text = html_lib.unescape(text)
    text = _SCRIPT_RE.sub(" ", text)
    text = _STYLE_RE.sub(" ", text)
    text = _BR_RE.sub("\n", text)
    text = _CLOSE_P_RE.sub("\n\n", text)
    text = _TAG_RE.sub(" ", text)
    text = _NBSP_RE.sub(" ", text)
    text = _SPACE_RUN_RE.sub(" ", text)
    text = _LEADING_SPACE_RE.sub("\n", text)
    text = _BLANK_LINE_RUN_RE.sub("\n\n", text)
    return text.strip()


# ---------- meta + JSON-LD extraction ----------

def meta_content(html: str, prop: str) -> str | None:
    """Return the content attribute of a <meta> tag matching property/name=prop."""
    escaped = re.escape(prop)
    pattern_a = re.compile(
        rf'<meta[^>]+(?:property|name)=["\']{escaped}["\'][^>]+content=["\']([^"\']*)["\']',
        re.IGNORECASE,
    )
    pattern_b = re.compile(
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+(?:property|name)=["\']{escaped}["\']',
        re.IGNORECASE,
    )
    for pattern in (pattern_a, pattern_b):
        match = pattern.search(html)
        if match:
            return html_lib.unescape(match.group(1))
    return None


_LD_JSON_RE = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)


def _flatten(value) -> list:
    """Recursively flatten a JSON-LD value into a list of dicts."""
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(_flatten(item))
        return out
    if isinstance(value, dict):
        out = [value]
        for sub in value.values():
            out.extend(_flatten(sub))
        return out
    return []


def ld_json_articles(html: str) -> list[dict]:
    """Return all dict-shaped nodes found in <script type=application/ld+json> blocks."""
    items = []
    for raw in _LD_JSON_RE.findall(html):
        stripped = raw.strip()
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            try:
                parsed = json.loads(html_lib.unescape(stripped))
            except json.JSONDecodeError:
                continue
        items.extend(_flatten(parsed))
    return items


def _author_string(value) -> str:
    """Coerce a JSON-LD `author` field into a comma-separated string.

    Handles all three valid shapes per the JSON-LD spec:
        - string ("Lily Chambers") — used directly
        - dict ({"name": "Lily Chambers"}) — name field extracted
        - list of strings/dicts — joined with ", "
    """
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        return str(value.get("name", "")).strip()
    if isinstance(value, list):
        names = []
        for item in value:
            if isinstance(item, str):
                names.append(item.strip())
            elif isinstance(item, dict):
                name = item.get("name")
                if name:
                    names.append(str(name).strip())
        return ", ".join(n for n in names if n)
    return ""


# ---------- body extraction ----------

def _site_selectors_for(source_url: str) -> dict | None:
    """Return the SITE_SELECTORS entry whose key appears in source_url."""
    for substring, selectors in SITE_SELECTORS.items():
        if substring in source_url:
            return selectors
    return None


def _paragraphs_by_class(html: str, class_name: str) -> list[str]:
    pattern = re.compile(
        rf'<p[^>]+class=["\'][^"\']*{re.escape(class_name)}[^"\']*["\'][^>]*>(.*?)</p>',
        re.IGNORECASE | re.DOTALL,
    )
    cleaned = [clean_html(chunk) for chunk in pattern.findall(html)]
    return [c for c in cleaned if c]


def _section_by_class(html: str, class_name: str) -> str | None:
    pattern = re.compile(
        rf'<section[^>]+class=["\'][^"\']*{re.escape(class_name)}[^"\']*["\'][^>]*>(.*?)(?:<footer\b|</article>)',
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html)
    return match.group(1) if match else None


def _div_by_class_with_terminator(html: str, class_name: str, terminator: str) -> str | None:
    pattern = re.compile(
        rf'<div[^>]+class=["\'][^"\']*{re.escape(class_name)}[^"\']*["\'][^>]*>(.*?)(?:{re.escape(terminator)}|</article>)',
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(html)
    return match.group(1) if match else None


def _largest_article_block(html: str) -> str | None:
    pattern = re.compile(r"<article\b[^>]*>(.*?)</article>", re.IGNORECASE | re.DOTALL)
    matches = pattern.findall(html)
    if not matches:
        return None
    return max(matches, key=len)


def _main_block(html: str) -> str | None:
    pattern = re.compile(r"<main\b[^>]*>(.*?)</main>", re.IGNORECASE | re.DOTALL)
    match = pattern.search(html)
    return match.group(1) if match else None


def _body_from_article_html(article_html: str) -> str:
    """Strip noise tags and join h1-h4/p/li chunks with paragraph breaks."""
    cleaned = _NOISE_TAGS_RE.sub(" ", article_html)
    chunks = []
    for _tag, content in _BLOCK_CHUNK_RE.findall(cleaned):
        text = clean_html(content)
        if text:
            chunks.append(text)
    return "\n\n".join(chunks)


def extract_body(html: str, source_url: str, article: dict | None) -> str:
    """Run the fallback chain to pull article body text from the HTML."""
    if article and str(article.get("articleBody", "")).strip():
        return str(article["articleBody"]).strip()

    selectors = _site_selectors_for(source_url) or {}

    paragraph_class = selectors.get("paragraph_class")
    if paragraph_class:
        paragraphs = _paragraphs_by_class(html, paragraph_class)
        if paragraphs:
            return "\n\n".join(paragraphs)

    article_html: str | None = None
    section_class = selectors.get("section_class")
    if section_class:
        article_html = _section_by_class(html, section_class)

    div_class = selectors.get("div_class")
    if not article_html and div_class:
        terminator = selectors.get("terminator", "</article>")
        article_html = _div_by_class_with_terminator(html, div_class, terminator)

    if not article_html:
        article_html = _largest_article_block(html)
    if not article_html:
        article_html = _main_block(html)

    if article_html:
        return _body_from_article_html(article_html)

    og_description = meta_content(html, "og:description")
    return og_description.strip() if og_description else ""


# ---------- metadata ----------

def extract_title(html: str, article: dict | None, slug: str) -> str:
    if article and article.get("headline"):
        return str(article["headline"]).strip()
    for prop in ("og:title", "twitter:title"):
        value = meta_content(html, prop)
        if value:
            return value.strip()
    title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if title_match:
        return clean_html(title_match.group(1)) or slug
    return slug


def extract_published(html: str, article: dict | None) -> str:
    if article:
        for key in ("datePublished", "dateCreated"):
            value = article.get(key)
            if value:
                return str(value).strip()
    for prop in ("article:published_time", "og:article:published_time", "datePublished"):
        value = meta_content(html, prop)
        if value:
            return value.strip()
    return ""


def extract_author(article: dict | None) -> str:
    if not article:
        return ""
    return _author_string(article.get("author"))


# ---------- main ----------

def build_markdown(slug: str, source_url: str, html: str) -> str:
    articles = ld_json_articles(html)
    article = next(
        (item for item in articles if str(item.get("articleBody", "")).strip()),
        None,
    )

    title = extract_title(html, article, slug)
    author = extract_author(article)
    published = extract_published(html, article)
    body = extract_body(html, source_url, article)

    if not body.strip():
        raise SystemExit(f"no article body extracted from {slug}")

    today = datetime.date.today().isoformat()
    lines = [f"# {title}", ""]
    lines.append(f"- **Source URL:** {source_url}")
    lines.append("- **Snapshot method:** direct HTML article extraction")
    lines.append(f"- **Retrieved:** {today}")
    if author:
        lines.append(f"- **Author:** {author}")
    if published:
        lines.append(f"- **Published:** {published}")
    lines.append("")
    lines.append("## Article Body")
    lines.append("")
    lines.append(clean_html(body))
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 4:
        print(
            "usage: extract_direct_html_snapshot.py SLUG SOURCE_URL HTML_PATH OUT_PATH",
            file=sys.stderr,
        )
        return 2
    slug, source_url, html_path, out_path = args

    html = Path(html_path).read_text(encoding="utf-8", errors="replace")
    markdown = build_markdown(slug, source_url, html)
    Path(out_path).write_text(markdown, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
