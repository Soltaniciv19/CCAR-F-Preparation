def lookup(order_id, records, available=True):
    if not isinstance(order_id, str) or not order_id.strip():
        return {"ok": False, "error": "invalid_input", "retryable": False}
    if not available:
        return {"ok": False, "error": "unavailable", "retryable": True}
    if order_id not in records:
        return {"ok": False, "error": "not_found", "retryable": False}
    return {"ok": True, "record": records[order_id]}
