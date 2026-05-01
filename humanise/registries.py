"""
humanise.registries — Loaders for the pattern and judgement YAML registries.

Schema for patterns.yaml (one record per check_id):

    Required:
        category: str — one of the eight category headings in patterns.md
        short_name: str — human-readable label for the check
        description: str — short "what it looks for" string
        why_it_matters: str — rationale shown in audit output
        severity: str — "hard_fail" | "strong_warning" | "context_warning"
        failure_modes: list[str] — one or more failure-mode keys
        evidence_role: str
        guidance: str — depth-aware action guidance

    Optional (reserved for U8+):
        alternatives: str — markdown content from alternatives.md
        references: list[str] — sources/citations
        mode_actions: dict[str, str] — depth → action
        structural: bool

Loader fails fast on schema violations with field name and offending check_id.
"""

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_PATH = REPO_ROOT / "humanise" / "patterns.yaml"
JUDGEMENT_PATH = REPO_ROOT / "humanise" / "judgement.yaml"

REQUIRED_PATTERN_FIELDS = {
    "category",
    "short_name",
    "description",
    "why_it_matters",
    "severity",
    "failure_modes",
    "evidence_role",
    "guidance",
}

VALID_SEVERITIES = {"hard_fail", "strong_warning", "context_warning"}

VALID_CATEGORIES = {
    "Content patterns",
    "Language and grammar",
    "Style",
    "Communication",
    "Filler and hedging",
    "Sensory and atmospheric",
    "Structural tells",
    "Voice and register",
    "Aggregate AI-signal pressure",
}

_PATTERNS_CACHE = None
_JUDGEMENT_CACHE = None


def _validate_pattern(check_id, record):
    if not isinstance(record, dict):
        raise ValueError(
            f"patterns.yaml[{check_id!r}]: record must be a dict, got {type(record).__name__}"
        )
    missing = REQUIRED_PATTERN_FIELDS - set(record)
    if missing:
        raise ValueError(
            f"patterns.yaml[{check_id!r}]: missing required field(s) {sorted(missing)}"
        )
    if record["severity"] not in VALID_SEVERITIES:
        raise ValueError(
            f"patterns.yaml[{check_id!r}].severity: {record['severity']!r} not in {sorted(VALID_SEVERITIES)}"
        )
    if record["category"] not in VALID_CATEGORIES:
        raise ValueError(
            f"patterns.yaml[{check_id!r}].category: {record['category']!r} not in {sorted(VALID_CATEGORIES)}"
        )
    if not isinstance(record["failure_modes"], list) or not record["failure_modes"]:
        raise ValueError(
            f"patterns.yaml[{check_id!r}].failure_modes: must be non-empty list"
        )


def load_patterns():
    """Load and validate patterns.yaml, returning only per-check records.

    Underscore-prefixed top-level keys (`_meta`, `_extra_entries`) carry
    page-level patterns.md content used by the U15 generator and are filtered
    out of the per-check view returned here. Cached after first call.
    """
    global _PATTERNS_CACHE
    if _PATTERNS_CACHE is None:
        data = yaml.safe_load(PATTERNS_PATH.read_text())
        if not isinstance(data, dict):
            raise ValueError(
                "patterns.yaml: top-level must be a mapping of check_id → record"
            )
        per_check = {k: v for k, v in data.items() if not k.startswith("_")}
        for check_id, record in per_check.items():
            _validate_pattern(check_id, record)
        _PATTERNS_CACHE = per_check
    return _PATTERNS_CACHE


def load_judgement():
    """Load judgement.yaml. Cached after first call."""
    global _JUDGEMENT_CACHE
    if _JUDGEMENT_CACHE is None:
        _JUDGEMENT_CACHE = yaml.safe_load(JUDGEMENT_PATH.read_text())
    return _JUDGEMENT_CACHE


def pattern_for(check_id):
    """Look up a pattern record by check_id. Raises KeyError with known ids if missing."""
    patterns = load_patterns()
    if check_id not in patterns:
        known = sorted(patterns.keys())
        raise KeyError(
            f"Unknown check_id {check_id!r}. {len(known)} known ids; first 10: {known[:10]}"
        )
    return patterns[check_id]


def judgement_for(item_id):
    """Look up an agent-judgement record by id."""
    judgement = load_judgement()
    for record in judgement.get("records", []):
        if record.get("id") == item_id:
            return record
    raise KeyError(f"Unknown agent-judgement id {item_id!r}")


_DEFAULT_METADATA = {
    "severity": "context_warning",
    "failure_modes": ["genre_misfit"],
    "evidence_role": "unclassified",
    "guidance": "Review in context.",
}


def metadata_for(check_id):
    """Return the four-field metadata subset (severity, failure_modes,
    evidence_role, guidance) for byte-compatible annotation in grade.py.

    Falls back to the legacy default when check_id is unknown — preserves
    annotate_result's pre-U7 behaviour.
    """
    try:
        rec = pattern_for(check_id)
    except KeyError:
        return dict(_DEFAULT_METADATA)
    return {k: rec[k] for k in ("severity", "failure_modes", "evidence_role", "guidance")}


def report_text_for(check_id):
    """Return (short_name, description) for byte-compatible labels.

    Falls back to the legacy default when check_id is unknown — preserves
    check_report_text's pre-U7 behaviour.
    """
    try:
        rec = pattern_for(check_id)
    except KeyError:
        return (check_id.replace("-", " ").title(), "Checks for this AI-writing signal.")
    return (rec["short_name"], rec["description"])


def why_it_matters_for(check_id):
    """Return why_it_matters for byte-compatible inclusion in audit rows.

    Falls back to the legacy default when check_id is unknown — preserves
    pre-U7 behaviour at grade.py line 2436.
    """
    try:
        rec = pattern_for(check_id)
    except KeyError:
        return "This pattern can make prose read as generated or over-templated."
    return rec["why_it_matters"]
