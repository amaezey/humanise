#!/usr/bin/env python3
"""
render_patterns_md.py — Generate humanise/references/patterns.md from
humanise/scripts/patterns.json.

Two modes:
    --enrich   One-shot: parse current patterns.md, enrich patterns.json
               with per-section markdown bodies (heading number + heading
               text + body content). Run once during U7/U15 migration.
    --render   Default: emit patterns.md from patterns.json. Used by the
               CI check to verify the on-disk file equals regenerated output.
    --check    Render and diff against on-disk patterns.md. Exits non-zero
               on drift. Used by test_patterns_md_generator.py.

After U15, patterns.json is the source of truth. patterns.md is generated.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PATTERNS_JSON = REPO_ROOT / "humanise" / "scripts" / "patterns.json"
PATTERNS_MD = REPO_ROOT / "humanise" / "references" / "patterns.md"

# Order of H2 categories as they appear in patterns.md.
CATEGORY_ORDER = [
    "Content patterns",
    "Language and grammar",
    "Style",
    "Communication",
    "Filler and hedging",
    "Sensory and atmospheric",
    "Structural tells",
    "Voice and register",
]

# Page-level content that lives in the generator (rarely changes; kept here
# rather than as YAML strings to keep patterns.json focused on per-pattern data).
# Captured verbatim from current patterns.md during U15.

# These strings are populated by --enrich on first run; the loader writes them
# back to patterns.json under the _meta key. After enrichment, the values are
# read from patterns.json.


def _clean_h2_body(body):
    """Strip leading newlines (from after H2 title + blank line) and the
    trailing `\n\n---\n` separator (which belongs between sections)."""
    body = body.lstrip("\n")
    body = re.sub(r"\n+---\s*$", "", body)
    return body.rstrip()


def parse_patterns_md(text):
    """Split patterns.md into structured chunks: preamble, TOC, evidence
    section, per-category H3 sections, and the meta-check section.

    Section bodies do NOT include the trailing `\n\n---\n` separator; that
    separator is re-emitted by render() between sections.

    Returns dict with:
        preamble: str
        toc_body: str (just the body of ## Contents, no heading)
        evidence_body: str
        categories: dict[category_name, list[(heading_number, heading_text, body)]]
        meta_check_body: str
    """
    # Identify section boundaries by H2.
    h2_split = re.split(r"(?m)^## (.+)$", text)
    # h2_split = [preamble, h2_title_1, body_1, h2_title_2, body_2, ...]
    preamble = h2_split[0]
    # Strip trailing `---\n` from preamble too (separator before first H2 section).
    preamble = re.sub(r"\n+---\s*$", "", preamble).rstrip()

    toc_body = None
    evidence_body = None
    meta_check_body = None
    categories = {}

    for i in range(1, len(h2_split), 2):
        title = h2_split[i].strip()
        body = h2_split[i + 1] if i + 1 < len(h2_split) else ""
        body = _clean_h2_body(body)

        if title == "Contents":
            toc_body = body
        elif title.startswith("Evidence hierarchy"):
            evidence_body = body
        elif title.startswith("Aggregate AI-signal pressure"):
            meta_check_body = body
        elif title in CATEGORY_ORDER:
            categories[title] = parse_category_body(body)
        else:
            raise ValueError(f"Unrecognised H2 section: {title!r}")

    return {
        "preamble": preamble,
        "toc_body": toc_body,
        "evidence_body": evidence_body,
        "categories": categories,
        "meta_check_body": meta_check_body,
    }


def parse_category_body(body):
    """Parse a category H2 body into (preamble, list-of-H3-entries).

    Each H3 entry: (heading_number, heading_text, body_markdown, leading_blanks).
    body_markdown excludes the H3 line and its trailing newline.
    leading_blanks counts blank lines BEFORE the H3 within the previous body
    (preserves source idiosyncrasies — sub-letter entries are inconsistently
    spaced in the source).
    """
    h3_split = re.split(r"(?m)^### (\d+[a-z]?)\. (.+)$", body)
    # h3_split = [pre_h3_content, num1, title1, body1, num2, title2, body2, ...]
    preamble = h3_split[0].strip()
    entries = []
    for i in range(1, len(h3_split), 3):
        number = h3_split[i].strip()
        title = h3_split[i + 1].strip()
        raw_body = h3_split[i + 2]
        # Strip a trailing run of blank lines from raw_body (those blank lines
        # belong to the spacing BEFORE the next entry, not to this entry's body).
        m = re.search(r"(\n*)$", raw_body)
        trailing_newlines = len(m.group(1))
        # Number of blank lines (a blank line is a `\n` that ends an empty line).
        # raw_body ends with the body-final-newline + N blank-line-newlines.
        # If trailing_newlines >= 1, we have at least the body-final newline.
        # Each additional newline = one blank line of separator.
        next_entry_leading_blanks = max(0, trailing_newlines - 1) if i + 3 < len(h3_split) else 0
        h3_body = raw_body.lstrip("\n").rstrip()
        entries.append({
            "number": number,
            "title": title,
            "body": h3_body,
            # leading_blanks BEFORE this entry — set retroactively from prev's trailing.
            "leading_blanks": None,  # filled by post-processing
            "_next_entry_leading_blanks": next_entry_leading_blanks,
        })
    # Set leading_blanks on each entry from the previous entry's trailing count.
    # Compute first, then delete temp field, to avoid reading deleted values.
    for i, entry in enumerate(entries):
        if i == 0:
            entry["leading_blanks"] = 1
        else:
            entry["leading_blanks"] = entries[i - 1]["_next_entry_leading_blanks"]
    for entry in entries:
        del entry["_next_entry_leading_blanks"]
    return {"preamble": preamble, "entries": entries}


def find_check_id_in_body(body):
    """Extract the check_id from the body's **Severity:** line, if present.

    Returns (check_id, kind) where kind is 'check', 'folded', or 'manual'.
    """
    # **Severity:** <tier> · `check-id`
    m = re.search(r"\*\*Severity:\*\*\s+(\w+)\s*·\s*`([\w-]+)`", body)
    if m:
        return (m.group(2), "check")
    # **Severity:** N/A · ...  → manual
    if re.search(r"\*\*Severity:\*\*\s+N/A", body):
        return (None, "manual")
    # **Severity:** inherits <tier> from `parent`
    m = re.search(r"\*\*Severity:\*\*\s+inherits\s+\w+\s+from\s+`([\w-]+)`", body)
    if m:
        return (m.group(1), "folded")
    return (None, "unknown")


def enrich():
    """Parse patterns.md, enrich patterns.json with per-section content.

    Reads existing patterns.json records (keyed by check_id) and adds the
    fields pattern_number, patterns_md_heading, patterns_md_body to each.

    Folded and manual entries (no own check_id) are added under
    _extra_entries: [{number, heading, category, body}, ...].

    Page-level content (preamble, TOC, evidence, meta-check) is added under
    _meta: {preamble, toc_section, evidence_section, meta_check_section}.
    """
    md_text = PATTERNS_MD.read_text()
    parsed = parse_patterns_md(md_text)

    data = json.loads(PATTERNS_JSON.read_text())

    enriched = {}
    enriched["_meta"] = {
        "preamble": parsed["preamble"],
        "toc_body": parsed["toc_body"],
        "evidence_body": parsed["evidence_body"],
        "meta_check_body": parsed["meta_check_body"],
    }

    extra_entries = []
    category_preambles = {}

    for category, parsed_cat in parsed["categories"].items():
        if parsed_cat["preamble"]:
            category_preambles[category] = parsed_cat["preamble"]
        for entry in parsed_cat["entries"]:
            number = entry["number"]
            heading = entry["title"]
            body = entry["body"]
            leading_blanks = entry["leading_blanks"]
            check_id, kind = find_check_id_in_body(body)
            if kind == "check" and check_id in data:
                rec = dict(data[check_id])
                rec["pattern_number"] = number
                rec["patterns_md_heading"] = heading
                rec["patterns_md_body"] = body
                rec["patterns_md_leading_blanks"] = leading_blanks
                data[check_id] = rec
            else:
                extra_entries.append({
                    "pattern_number": number,
                    "patterns_md_heading": heading,
                    "category": category,
                    "kind": kind,
                    "check_id": check_id,
                    "patterns_md_body": body,
                    "patterns_md_leading_blanks": leading_blanks,
                })

    enriched["_extra_entries"] = extra_entries
    enriched["_meta"]["category_preambles"] = category_preambles

    # Re-emit JSON: _meta + _extra_entries first, then per-check records sorted.
    out = {}
    out["_meta"] = enriched["_meta"]
    out["_extra_entries"] = enriched["_extra_entries"]
    # Only include per-check records (skip _meta / _extra_entries from the
    # previously-enriched file, which would otherwise overwrite the fresh
    # ones we just built).
    for cid in sorted(k for k in data if not k.startswith("_")):
        out[cid] = data[cid]

    PATTERNS_JSON.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n"
    )
    n_check = sum(1 for k in out if not k.startswith("_"))
    print(f"enriched {PATTERNS_JSON.relative_to(REPO_ROOT)}:")
    print(f"  {n_check} check records (added pattern_number, patterns_md_heading, patterns_md_body)")
    print(f"  {len(extra_entries)} extra entries (folded/manual)")
    print(f"  _meta: preamble + toc_body + evidence_body + meta_check_body")


def render():
    """Read patterns.json and emit patterns.md text."""
    data = json.loads(PATTERNS_JSON.read_text())
    meta = data.get("_meta", {})
    extras = data.get("_extra_entries", [])

    # Group all entries (checks + extras) by category, preserving original order via pattern_number.
    by_category = {cat: [] for cat in CATEGORY_ORDER}
    for cid, rec in data.items():
        if cid.startswith("_"):
            continue
        if "pattern_number" not in rec:
            continue
        by_category[rec["category"]].append({
            "number": rec["pattern_number"],
            "heading": rec["patterns_md_heading"],
            "body": rec["patterns_md_body"],
            "leading_blanks": rec.get("patterns_md_leading_blanks", 1),
        })
    for entry in extras:
        by_category[entry["category"]].append({
            "number": entry["pattern_number"],
            "heading": entry["patterns_md_heading"],
            "body": entry["patterns_md_body"],
            "leading_blanks": entry.get("patterns_md_leading_blanks", 1),
        })

    # Sort each category by pattern_number — the original patterns.md order
    # uses numeric+letter suffix; sort by (numeric_prefix, letter_suffix).
    def sort_key(entry):
        m = re.match(r"(\d+)([a-z]?)", entry["number"])
        return (int(m.group(1)), m.group(2))
    for cat in by_category:
        by_category[cat].sort(key=sort_key)

    # Build sections. Preamble → Contents has NO `---` separator. All other
    # transitions get `---`.
    preamble_and_toc = meta["preamble"] + f"\n\n## Contents\n\n{meta['toc_body']}"
    sections = [preamble_and_toc]
    sections.append(f"## Evidence hierarchy from the reference audit\n\n{meta['evidence_body']}")

    category_preambles = meta.get("category_preambles", {})
    for cat in CATEGORY_ORDER:
        cat_header = f"## {cat}"
        if cat in category_preambles:
            cat_header += f"\n\n{category_preambles[cat]}"

        # Build category block: header, then each entry preceded by its
        # leading_blanks (number of blank lines between previous body and this H3).
        cat_block = cat_header
        for i, entry in enumerate(by_category[cat]):
            if i == 0:
                # First entry: one blank line between category header (or its
                # preamble) and the first H3.
                separator = "\n\n"
            else:
                # `\n` ends previous body's last line; then leading_blanks * `\n`
                # adds blank lines; the next H3 starts at the first char after.
                separator = "\n" * (entry["leading_blanks"] + 1)
            cat_block += f"{separator}### {entry['number']}. {entry['heading']}\n\n{entry['body']}"
        sections.append(cat_block)

    sections.append(f"## Aggregate AI-signal pressure (meta-check)\n\n{meta['meta_check_body']}")

    return "\n\n---\n\n".join(sections).rstrip() + "\n"


def check():
    """Render and diff against on-disk patterns.md. Exit non-zero on drift."""
    rendered = render()
    on_disk = PATTERNS_MD.read_text()
    if rendered == on_disk:
        print("OK  patterns.md matches generator output")
        return 0
    # Find first divergence for actionable error message.
    for i, (a, b) in enumerate(zip(rendered, on_disk)):
        if a != b:
            line = on_disk[:i].count("\n") + 1
            col = i - on_disk.rfind("\n", 0, i)
            print(f"DRIFT at line {line}, col {col}:")
            print(f"  generator: {rendered[max(0, i-30):i+30]!r}")
            print(f"  on disk:   {on_disk[max(0, i-30):i+30]!r}")
            return 1
    # Lengths differ, content matches up to shorter length
    print(f"DRIFT: length differs (generator={len(rendered)}, on_disk={len(on_disk)})")
    return 1


def main():
    if "--enrich" in sys.argv:
        enrich()
    elif "--check" in sys.argv:
        sys.exit(check())
    else:
        # Default: render to stdout (for inspection) or file (with --write).
        out = render()
        if "--write" in sys.argv:
            PATTERNS_MD.write_text(out)
            print(f"wrote {PATTERNS_MD.relative_to(REPO_ROOT)}")
        else:
            sys.stdout.write(out)


if __name__ == "__main__":
    main()
