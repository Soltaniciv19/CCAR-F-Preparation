import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_capstone_connects_to_p3_server_and_escalates_unknown_policy():
    # The bridge is reference-only; learner tests target the coordinator interface.
    if os.environ.get("P6_WORKSPACE"):
        pytest.skip("the MCP bridge is a reference extension")
    result = subprocess.run(
        [sys.executable, str(ROOT / "solution" / "mcp_bridge.py"), "order-1"],
        capture_output=True,
        text=True,
        check=True,
    )
    import json

    outcome = json.loads(result.stdout)
    assert outcome["decision"] == "escalate"
    assert outcome["coverage"] == "partial" and outcome["mcp_calls"] == 2
    assert outcome["source"]["id"] == "policy://refund" and outcome["source"]["date"] is None


def test_mcp_missing_order_escalates():
    result = subprocess.run(
        [sys.executable, str(ROOT / "solution" / "mcp_bridge.py"), "absent"],
        capture_output=True,
        text=True,
        check=True,
    )
    import json

    outcome = json.loads(result.stdout)
    assert outcome["decision"] == "escalate" and outcome["mcp_calls"] == 1


def test_transport_failure_creates_handoff():
    code = """
import asyncio
import json
import sys
sys.path.insert(0, sys.argv[1])
import mcp_bridge

def fail(_server):
    raise OSError("server unavailable")

mcp_bridge.stdio_client = fail
print(json.dumps(asyncio.run(mcp_bridge.run("order-1"))))
"""
    result = subprocess.run(
        [sys.executable, "-c", code, str(ROOT / "solution")],
        capture_output=True,
        text=True,
        check=True,
    )
    import json

    outcome = json.loads(result.stdout)
    assert outcome["decision"] == "escalate" and outcome["coverage"] == "partial"
    assert (
        outcome["mcp_calls"] == 0
        and outcome["handoff"]["reason"] == "MCP server or transport unavailable"
    )
