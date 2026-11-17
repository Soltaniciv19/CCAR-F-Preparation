"""Domain 5: context, provenance, durable progress, and review routing."""

from __future__ import annotations

import json
import random
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Claim:
    metric: str
    value: str
    unit: str
    period: str
    population: str
    method: str
    source: str
    published: str
    locator: str


def compare_claims(a: Claim, b: Claim) -> str:
    dimensions = ("metric", "unit", "period", "population", "method")
    if any(getattr(a, d) != getattr(b, d) for d in dimensions):
        return "not_directly_comparable"
    return "consistent" if a.value == b.value else "conflict_requires_verification"


def build_context(*, facts: dict, claims: list[Claim], summary: str) -> dict:
    # Trusted facts must originate in application state. Summaries cannot overwrite them.
    return {
        "case_facts": facts.copy(),
        "evidence": [asdict(c) for c in claims],
        "conversation_summary": summary,
    }


def route_case(
    *, wants_human=False, ambiguous_identity=False, policy_exception=False, recovery_exhausted=False
) -> str:
    if wants_human:
        return "escalate_requested"
    if ambiguous_identity:
        return "clarify_identity"
    if policy_exception:
        return "escalate_policy"
    if recovery_exhausted:
        return "escalate_with_partial_findings"
    return "resolve_within_policy"


def save_manifest(path: Path, *, commit: str, completed: list[str], pending: list[str]) -> None:
    """Atomic file replacement on the same filesystem; not a distributed state store."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": 1, "commit": commit, "completed": completed, "pending": pending}
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle)
            handle.flush()
            import os

            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def load_manifest(path: Path, current_commit: str) -> dict:
    saved = json.loads(path.read_text())
    if saved["schema_version"] != 1:
        raise ValueError("Unsupported manifest version")
    return {**saved, "needs_revalidation": saved["commit"] != current_commit}


def stratified_sample(records: list[dict], *, per_stratum: int, seed: int = 0) -> list[dict]:
    if per_stratum < 0:
        raise ValueError("Sample size cannot be negative")
    strata: dict[tuple, list[dict]] = {}
    for record in records:
        key = (record["document_type"], record["field"], record["confidence_band"])
        strata.setdefault(key, []).append(record)
    rng = random.Random(seed)
    return [
        record
        for key in sorted(strata)
        for record in rng.sample(strata[key], min(per_stratum, len(strata[key])))
    ]
