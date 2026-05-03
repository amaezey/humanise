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
Severity: 1 hard_fail · 1 strong_warning · 1 context_warning · pressure: clear
Pressure clear.

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
| Aggregate AI-signal pressure | Clear | |

**Language and grammar** \u2014 11/11 clear
"""

hits = iteration.catalogue_hits(OUTPUT_WITH_LAYER_2_CATALOGUE_ROWS)
expected = {"no-collaborative-artifacts", "no-em-dashes", "no-forced-triads"}
if hits == expected:
    ok("counts only Layer 1 flagged blocks and maps aliases")
else:
    fail(f"expected {sorted(expected)}, got {sorted(hits)}")

if "overall-ai-signal-pressure" not in hits and "no-manufactured-insight" not in hits:
    ok("ignores Layer 2 catalogue rows and suppressed aggregate rows")
else:
    fail(f"Layer 2-only rows leaked into hits: {sorted(hits)}")

if iteration.catalogue_hits("No audit rendered here.") == set():
    ok("returns empty set when no Audit section exists")
else:
    fail("expected empty hit set without an Audit section")

if FAILURES:
    raise SystemExit(1)

print("\n========================================")
print("ALL PASSED")
