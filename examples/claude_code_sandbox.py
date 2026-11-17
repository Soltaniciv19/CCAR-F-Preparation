"""Create a fresh disposable Claude Code workshop without touching real configuration.

Usage: python -m examples.claude_code_sandbox /tmp/ccarf-workshop
The target must not already exist. This script makes no Claude or network calls.
"""

import argparse
from pathlib import Path

FILES = {
    "CLAUDE.md": """# Python pricing workshop
Use integer cents. Keep parsing and pricing contracts explicit about units.
@docs/testing-standard.md
Run `python -m unittest discover -s verification -v` from this workshop root.
""",
    "docs/testing-standard.md": """# Testing standard
Use unittest and deterministic synthetic fixtures. Check public behavior and boundary cases.
For price calculations include full boxes, zero, negative, boolean and partial-box inputs.
Read existing verification tests before suggesting new scenarios.
""",
    ".claude/rules/python-tests.md": """---
paths:
  - "**/test_*.py"
  - "**/*_test.py"
---
Use explicit expected integer cents and independent input/output examples.
Do not assert private helper structure when public behavior captures the requirement.
""",
    ".claude/rules/infrastructure.md": """---
paths:
  - "infra/**/*.tf"
---
Describe state, access scope and rollback before changing infrastructure.
""",
    ".claude/skills/inspect-flow/SKILL.md": """---
name: inspect-flow
description: Trace a Python entrypoint through wrappers and report cited evidence.
argument-hint: "[entrypoint or question]"
context: fork
agent: Explore
allowed-tools: Read, Grep, Glob
---
Inspect $ARGUMENTS. If no usable entrypoint or question is supplied, ask for one.
Read only. Return paths, symbols, observed units and contracts, and unresolved assumptions.
Keep the result concise. Verify aliases instead of assuming the original symbol is the only name.
The host must separately enforce actual read-only capabilities where required.
""",
    ".claude/commands/review-pricing.md": """Review the pricing entrypoint using its requirements and existing tests.
Input: $ARGUMENTS
Report reachable behavioral defects with path, evidence, trigger and impact.
Skip style preferences. Trace units across parser and pricing interfaces.
""",
    "pricing/__init__.py": "from .core import price_pieces as quote\n",
    "pricing/core.py": '''"""Public API accepts pieces; prices are cents per twelve-piece box."""

def price_pieces(pieces: int, cents_per_box: int = 1200) -> int:
    if type(pieces) is not int or pieces <= 0 or pieces % 12:
        raise ValueError("A positive whole number of twelve-piece boxes is required")
    if type(cents_per_box) is not int or cents_per_box < 0:
        raise ValueError("Nonnegative integer cents required")
    return (pieces // 12) * cents_per_box
''',
    "api.py": """from pricing import quote

def total_for_order(pieces: int) -> int:
    return quote(pieces)
""",
    "verification/test_pricing.py": """import unittest
from api import total_for_order

class PricingTests(unittest.TestCase):
    def test_two_boxes(self):
        self.assertEqual(total_for_order(24), 2400)

    def test_invalid_piece_quantities(self):
        for quantity in (0, -12, True, 13):
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                total_for_order(quantity)

if __name__ == "__main__":
    unittest.main()
""",
    "README.md": """# Disposable CCAR-F workshop
Run `python -m unittest discover -s verification -v`.
Inspect `/memory`, then invoke `/inspect-flow api.total_for_order` in Claude Code.
Compare filename discovery with searching the reexported `quote` symbol.
Ask a fresh reviewer to trace pieces versus boxes; do not alter global settings.
Optional fault injection: replace the division by 12 with direct multiplication, then run tests.
The initial implementation is correct; injected faults are deliberate workshop changes.
""",
}


def create_sandbox(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=False)
    for name, content in FILES.items():
        path = target / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    args = parser.parse_args()
    create_sandbox(args.target)
    print("Created disposable workshop:", args.target.resolve())
