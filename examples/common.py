"""Explicit live configuration: no model guessed and no key printed."""

import os


def model_id() -> str:
    value = os.environ.get("ANTHROPIC_MODEL", "").strip()
    if not value or value == "your-supported-model-id":
        raise RuntimeError("Set ANTHROPIC_MODEL to an enabled, feature-compatible model ID")
    return value


def client():
    from anthropic import Anthropic

    # SDK retries are bounded; do not wrap writes in generic retry loops.
    return Anthropic(timeout=45.0, max_retries=2)
