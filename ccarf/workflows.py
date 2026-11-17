"""Domain 3: isolated CLI review and commit-aware duplicate suppression."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

FINDINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "line": {"type": "integer"},
                    "category": {"type": "string"},
                    "evidence": {"type": "string"},
                    "impact": {"type": "string"},
                },
                "required": ["path", "line", "category", "evidence", "impact"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}


def review_command() -> list[str]:
    return [
        "claude",
        "-p",
        "--output-format",
        "json",
        "--json-schema",
        json.dumps(FINDINGS_SCHEMA),
        "--tools",
        "Read,Grep,Glob",
        "--allowedTools",
        "Read,Grep,Glob",
        "--max-turns",
        "8",
    ]


def run_review(prompt: str, cwd: Path, *, runner=subprocess.run) -> dict:
    """Opt-in external process: caller supplies a disposable review checkout."""
    result = runner(
        review_command(),
        input=prompt,
        text=True,
        capture_output=True,
        cwd=cwd,
        timeout=180,
        check=True,
    )
    envelope = json.loads(result.stdout)
    if envelope.get("is_error") or envelope.get("subtype") != "success":
        raise RuntimeError("CLI review did not complete successfully")
    output = envelope.get("structured_output")
    if not isinstance(output, dict) or not isinstance(output.get("findings"), list):
        raise ValueError("Missing structured findings; do not interpret this as an empty review")
    return output


def finding_key(finding: dict) -> tuple[str, str, str]:
    # Evidence-based identity survives line movement better than line number alone.
    return (finding["path"], finding["category"], finding["evidence"].strip())


def new_findings(current: list[dict], previously_posted: list[dict]) -> list[dict]:
    seen = {finding_key(f) for f in previously_posted}
    output = []
    for finding in current:
        key = finding_key(finding)
        if key not in seen:
            output.append(finding)
            seen.add(key)
    return output
