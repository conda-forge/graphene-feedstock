"""Handle quirks of in-tree tests that get stripped."""
import os
import sys
from pathlib import Path

REPLACEMENTS = {
    "relative imports don't resolve": ["from ...types", "from graphene.types"]
}

TESTS = Path(__file__).parent / "graphene/tests"

fixed = 0

test_files = sorted(TESTS.rglob("*.py"))

print(len(test_files), "test files in", TESTS)

if not len(test_files):
    sys.exit(1)

for p in test_files:
    print(p, "...", end=None, flush=True)
    old_text = new_text = p.read_text(encoding="utf-8")
    for kind, old_new in REPLACEMENTS.items():
        old, new = old_new
        if old in new_text:
            print("\n", f"... {kind}")
        new_text = new_text.replace(old, new)
    if old_text != new_text:
        p.write_text(new_text, encoding="utf-8")
        fixed += 1
    else:
        print("OK")

if fixed == 0:
    print("no files fixed")
