#!/usr/bin/env python3
"""Regression tests for iteration-harness measurement helpers.

Run: python3 dev/evals/test_iteration_harness_measurement.py
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "dev" / "evals" / "run_skill_creator_iteration.py"

spec = importlib.util.spec_from_file_location("run_skill_creator_iteration", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
iteration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(iteration)


FAILURES = 0


def ok(message: str) -> None:
    print(f"  ok: {message}")


def fail(message: str) -> None:
    global FAILURES
    FAILURES += 1
    print(f"FAIL: {message}")


print("=== catalogue_hits ===")

OUTPUT_WITH_LAYER_2_CATALOGUE_ROWS = """
Audit
Severity: 1 hard fail · 1 strong warning · 1 context warning · signal stacking: clear
Signal stacking clear.

x **Assistant residue** \u2014 "I hope this helps" \u2014 Action: Fix
! **Em dashes** \u2014 "\u2014" \u2014 Action: Fix
? **Rule of three** \u2014 "participation, resilience, and mobilisation" \u2014 Action: Disclose or ask before preserving

---

**Content patterns** \u2014 1 flagged of 12

| Pattern | Result | Action |
| --- | --- | --- |
| Manufactured insight | Clear | |
| Significance inflation | Clear | |
| Rule of three | Flagged | Disclose or ask before preserving |
| Signal stacking | Clear | |

**Language and grammar** \u2014 11/11 clear
"""

hits = iteration.catalogue_hits(OUTPUT_WITH_LAYER_2_CATALOGUE_ROWS)
expected = {"no-collaborative-artifacts", "no-em-dashes", "no-forced-triads"}
if hits == expected:
    ok("counts only Layer 1 flagged blocks and maps aliases")
else:
    fail(f"expected {sorted(expected)}, got {sorted(hits)}")

if "overall-signal-stacking" not in hits and "no-manufactured-insight" not in hits:
    ok("ignores Layer 2 catalogue rows and suppressed aggregate rows")
else:
    fail(f"Layer 2-only rows leaked into hits: {sorted(hits)}")

if iteration.catalogue_hits("No audit rendered here.") == set():
    ok("returns empty set when no Audit section exists")
else:
    fail("expected empty hit set without an Audit section")


# U3 measurement-lock fixture — the audit-output-redesign new shape.
# After U4 the audit header is followed by an `Auto-detected:` counts line
# (not `Severity:`), so AUDIT_HEADER_RE was relaxed in U3 to match either.
# After U5 the agent-judgement items move into the audit section as
# `! **Item**` / `? **Item**` openers; their labels (e.g. "Tonal uniformity")
# are NOT catalogue patterns and must NOT inflate the hit count.

OUTPUT_NEW_AUDIT_SHAPE_BOTH_BLOCKS_IN_AUDIT = """
Audit
Auto-detected: 2 of 12 flagged · Agent-assessed: 1 of 8 flagged
Severity: 0 hard fail · 2 strong warning · 1 context warning
Signal stacking: clear (weaker AI signals are not accumulating)

! **Em dashes** — "—"
! **Rule of three** — "participation, resilience, and mobilisation"
? **Tonal uniformity**
  - "register holds without breaks" — single tonal arc

**Next step**

Want the full coverage report, suggestions for edits, a full rewrite, or to save this audit as a file?
"""

hits = iteration.catalogue_hits(OUTPUT_NEW_AUDIT_SHAPE_BOTH_BLOCKS_IN_AUDIT)
expected = {"no-em-dashes", "no-forced-triads"}
if hits == expected:
    ok("counts new-shape Layer 1 openers and ignores agent-judgement-label openers in the audit body")
else:
    fail(f"expected {sorted(expected)} on new-shape audit body, got {sorted(hits)}")

if FAILURES:
    raise SystemExit(1)

print("\n========================================")
print("ALL PASSED")
