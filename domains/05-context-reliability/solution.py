"""Runnable offline worked solution. Run this file from any working directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from dataclasses import replace
from tempfile import TemporaryDirectory

from ccarf.reliability import Claim, compare_claims, load_manifest, route_case, save_manifest

claim = Claim(
    "sites", "4200", "sites", "2025", "registered", "register", "agency", "2026-03-01", "page 19"
)
print("Different period:", compare_claims(claim, replace(claim, period="2026")))
print("Same dimensions, different value:", compare_claims(claim, replace(claim, value="4300")))
with TemporaryDirectory() as directory:
    state = Path(directory) / "manifest.json"
    save_manifest(state, commit="old", completed=["map"], pending=["trace"])
    print("After revision change:", load_manifest(state, "new"))
print("Ambiguous identity:", route_case(ambiguous_identity=True))
