#!/usr/bin/env python3
"""Asserts human-eyes/references/patterns.md equals the generator output from
dev/tools/render_patterns_md.py. Catches drift between the YAML registry
(authoritative source) and the on-disk markdown (generated transparency view).

Run: python3 dev/evals/tests/test_patterns_md_generator.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

result = subprocess.run(
    ["python3", str(ROOT / "dev" / "tools" / "render_patterns_md.py"), "--check"],
    capture_output=True,
    text=True,
)
print(result.stdout, end="")
if result.stderr:
    print(result.stderr, file=sys.stderr, end="")

if result.returncode != 0:
    print()
    print("FAIL: human-eyes/references/patterns.md is out of sync with human-eyes/scripts/patterns.json.")
    print("      Edit patterns.json, then regenerate:")
    print("      python3 dev/tools/render_patterns_md.py --write")
    sys.exit(1)

print()
print("========================================")
print("ALL PASSED")
