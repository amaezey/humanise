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

try:
    import yaml
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "humanise's registry-backed grader requires PyYAML. "
        "Install it with `python3 -m pip install PyYAML`, then rerun the grader."
    ) from exc

REPO_ROOT = Path(__file__).resolve().parents[1]
PATTERNS_PATH = REPO_ROOT / "humanise" / "patterns.yaml"
JUDGEMENT_PATH = REPO_ROOT / "humanise" / "judgement.yaml"
VOCABULARY_PATH = REPO_ROOT / "humanise" / "vocabulary.yml"

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

REQUIRED_JUDGEMENT_FIELDS = {"id", "prompt", "answer_schema", "flagged_when"}
VALID_JUDGEMENT_SCHEMA_TYPES = {"trichotomy", "state", "list", "composite"}

_PATTERNS_CACHE = None
_JUDGEMENT_CACHE = None
_VOCABULARY_CACHE = None


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
    """Load and validate judgement.yaml. Cached after first call."""
    global _JUDGEMENT_CACHE
    if _JUDGEMENT_CACHE is None:
        data = yaml.safe_load(JUDGEMENT_PATH.read_text())
        _validate_judgement(data)
        _JUDGEMENT_CACHE = data
    return _JUDGEMENT_CACHE


def _validate_judgement(data):
    if not isinstance(data, dict):
        raise ValueError(
            f"judgement.yaml: top-level must be a mapping, got {type(data).__name__}"
        )
    if data.get("schema_version") != "1":
        raise ValueError(
            f"judgement.yaml.schema_version: expected '1', got {data.get('schema_version')!r}"
        )
    records = data.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError("judgement.yaml.records: must be a non-empty list")
    seen = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(
                f"judgement.yaml.records[{index}]: record must be a dict, got {type(record).__name__}"
            )
        item_id = record.get("id", f"<record {index}>")
        missing = REQUIRED_JUDGEMENT_FIELDS - set(record)
        if missing:
            raise ValueError(
                f"judgement.yaml[{item_id!r}]: missing required field(s) {sorted(missing)}"
            )
        if item_id in seen:
            raise ValueError(f"judgement.yaml[{item_id!r}]: duplicate id")
        seen.add(item_id)
        answer_schema = record["answer_schema"]
        if not isinstance(answer_schema, dict):
            raise ValueError(
                f"judgement.yaml[{item_id!r}].answer_schema: must be a dict"
            )
        schema_type = answer_schema.get("type")
        if schema_type not in VALID_JUDGEMENT_SCHEMA_TYPES:
            raise ValueError(
                f"judgement.yaml[{item_id!r}].answer_schema.type: "
                f"{schema_type!r} not in {sorted(VALID_JUDGEMENT_SCHEMA_TYPES)}"
            )


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


# ---------------------------------------------------------------------------
# vocabulary.yml — user-facing strings + prose templates.
# ---------------------------------------------------------------------------


def load_vocabulary():
    """Load and validate vocabulary.yml. Cached after first call."""
    global _VOCABULARY_CACHE
    if _VOCABULARY_CACHE is None:
        data = yaml.safe_load(VOCABULARY_PATH.read_text())
        if not isinstance(data, dict):
            raise ValueError(
                "vocabulary.yml: top-level must be a mapping, got "
                f"{type(data).__name__}"
            )
        if data.get("schema_version") != "1":
            raise ValueError(
                f"vocabulary.yml.schema_version: expected '1', got "
                f"{data.get('schema_version')!r}"
            )
        _VOCABULARY_CACHE = data
    return _VOCABULARY_CACHE


def _resolve_vocab_path(key):
    """Resolve a dotted key (e.g. 'pressure_explanation.lead') to a value.

    Raises KeyError with the full key path on miss so callers can localise
    the typo.
    """
    vocab = load_vocabulary()
    parts = key.split(".")
    node = vocab
    for index, part in enumerate(parts):
        if not isinstance(node, dict) or part not in node:
            covered = ".".join(parts[:index]) or "<root>"
            available = sorted(node.keys()) if isinstance(node, dict) else []
            raise KeyError(
                f"vocabulary.yml[{key!r}]: missing at {covered}; "
                f"available keys at that level: {available}"
            )
        node = node[part]
    return node


def string_for(key, **placeholders):
    """Look up a vocabulary string and format placeholders into it.

    `key` is dotted (e.g. 'templates.summary_flagged'). Missing key fails
    fast with the full key path. Missing placeholder fails fast with the
    placeholder name and the template key.
    """
    template = _resolve_vocab_path(key)
    if not isinstance(template, str):
        raise TypeError(
            f"vocabulary.yml[{key!r}]: expected string template, got "
            f"{type(template).__name__}"
        )
    try:
        return template.format(**placeholders)
    except KeyError as exc:
        missing = exc.args[0] if exc.args else "<unknown>"
        raise KeyError(
            f"vocabulary.yml[{key!r}]: template references {{{missing}}} "
            f"but no value was supplied. Provided: {sorted(placeholders)}"
        ) from None


def severity_label(severity):
    """User-facing label for a severity tier."""
    return _resolve_vocab_path(f"severity_labels.{severity}")


def action_label(action):
    """User-facing label for a recommended-action key."""
    return _resolve_vocab_path(f"action_labels.{action}")


def status_label(status):
    """User-facing label for a check status (clear/flagged/none)."""
    return _resolve_vocab_path(f"status_labels.{status}")


def pressure_status(triggered):
    """Word for AI-pressure status — 'triggered' or 'clear'."""
    return _resolve_vocab_path(
        "pressure_status." + ("triggered" if triggered else "clear")
    )


def failure_mode_metadata():
    """Return the failure-mode label/summary catalogue.

    Shape mirrors the legacy FAILURE_MODE_METADATA constant so callers can
    iterate `.items()` and read `.label` / `.summary` unchanged.
    """
    return _resolve_vocab_path("failure_modes")


def depth_consequence_text(severity):
    """Per-severity depth-consequence sentence."""
    return _resolve_vocab_path(f"depth_consequence.{severity}")
