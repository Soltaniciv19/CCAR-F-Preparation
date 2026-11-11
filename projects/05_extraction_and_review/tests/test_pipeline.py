import importlib.util
import os
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
path = Path(os.environ.get("P5_WORKSPACE", ROOT / "solution")) / "pipeline.py"
spec = importlib.util.spec_from_file_location("p5_pipeline", path)
pipeline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pipeline)


def record(merchant):
    return {"merchant": merchant, "amount_cents": 100, "currency": "USD"}


def test_validation():
    assert not pipeline.validate_record(record("Cafe"))
    assert pipeline.validate_record({"merchant": "", "amount_cents": True, "currency": "EUR"})
    assert pipeline.validate_record(None)


def test_reordering_retry_and_feedback():
    calls = []

    def extract(requests):
        calls.append(requests)
        if len(calls) == 1:
            return [{"id": "b", "record": record("B")}, {"id": "a", "record": {}}]
        assert requests[0]["feedback"]
        return [{"id": "a", "record": record("A")}]

    result = pipeline.process_batch([{"id": "a", "text": "A"}, {"id": "b", "text": "B"}], extract)
    assert result["a"]["record"]["merchant"] == "A" and result["a"]["attempts"] == 2
    assert result["b"]["record"]["merchant"] == "B" and result["b"]["attempts"] == 1


def test_failure_bounds_and_protocol():
    calls = []

    def extract(req):
        calls.append(req)
        return (
            [{"id": "a", "error": {"message": "denied", "retryable": False}}]
            if len(calls) == 1
            else []
        )

    result = pipeline.process_batch([{"id": "a", "text": ""}, {"id": "b", "text": ""}], extract, 2)
    assert result["a"]["attempts"] == 1 and result["b"]["attempts"] == 2
    with pytest.raises(ValueError):
        pipeline.process_batch([{"id": "a", "text": ""}], lambda _: [{"id": "unknown"}])
    with pytest.raises(ValueError):
        pipeline.process_batch([{"id": "a", "text": ""}, {"id": "a", "text": ""}], lambda _: [])


def test_metrics_and_evidence():
    metrics = pipeline.evaluate({"a": "A", "b": "B", "c": None}, {"a": "A", "b": "X"})
    assert metrics == {"precision": 0.5, "recall": 0.5}
    assert pipeline.evaluate({}, {}) == {"precision": 0, "recall": 0}
    findings = pipeline.review("# eval(text)\nx = eval(text)\n")
    assert (
        len(findings) == 1
        and findings[0]["line"] == 2
        and findings[0]["evidence"] == "x = eval(text)"
    )
    assert pipeline.review('message = "eval(text)"') == []
