def test_conflicts_and_partial_coverage(module):
    inputs = [
        {"source": "a", "date": "2025-01-01", "fact": "14 days"},
        {"source": "b", "date": "2025-02-01", "fact": "30 days"},
        {"source": "c", "date": "2025-02-02", "error": "timeout", "fact": "ignore"},
    ]
    result = module.summarize(inputs)
    assert result["evidence"] == inputs[:2]
    assert result["failed_sources"] == ["c"]
    assert result["partial"] is True


def test_no_evidence_and_no_failures(module):
    assert module.summarize([]) == {"evidence": [], "failed_sources": [], "partial": False}
