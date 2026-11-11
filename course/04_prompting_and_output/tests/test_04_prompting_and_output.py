def test_valid_and_invalid(module):
    assert module.validate({"id": "A", "amount": 0, "currency": "USD"}) == []
    assert set(module.validate({"id": " ", "amount": -1, "currency": "GBP"})) == {
        "id",
        "amount",
        "currency",
    }
    assert module.validate(None) == ["record"]


def test_missing_boolean_and_nan(module):
    assert set(module.validate({})) == {"id", "amount", "currency"}
    assert "amount" in module.validate({"id": "A", "amount": True, "currency": "EUR"})
    assert "amount" in module.validate({"id": "A", "amount": float("nan"), "currency": "EUR"})
