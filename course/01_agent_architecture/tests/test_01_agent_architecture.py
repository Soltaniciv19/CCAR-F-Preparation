def test_multiple_calls_and_ids(module):
    calls = [
        {"id": "1", "name": "lookup", "input": {"order_id": "O-1"}},
        {"id": "2", "name": "delete", "input": {}},
        {"id": "3", "name": "lookup", "input": {"order_id": ""}},
    ]
    results = module.dispatch(calls, {"lookup"})
    assert [r["id"] for r in results] == ["1", "2", "3"]
    assert results[0]["result"] == {"order_id": "O-1", "status": "shipped"}
    assert results[1]["error"] == "not_allowed"
    assert results[2]["error"] == "invalid_input"


def test_denied_even_when_known(module):
    assert (
        module.dispatch([{"id": "x", "name": "lookup", "input": {"order_id": "O-1"}}], set())[0][
            "error"
        ]
        == "not_allowed"
    )
