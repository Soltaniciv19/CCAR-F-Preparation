def test_success_and_missing(module):
    records = {"O-1": {"status": "shipped"}}
    assert module.lookup("O-1", records) == {"ok": True, "record": {"status": "shipped"}}
    assert module.lookup("O-2", records) == {"ok": False, "error": "not_found", "retryable": False}


def test_input_and_availability(module):
    assert module.lookup(" ", {}, False)["error"] == "invalid_input"
    assert module.lookup("O-1", {}, False) == {
        "ok": False,
        "error": "unavailable",
        "retryable": True,
    }
    assert module.lookup(None, {})["retryable"] is False
