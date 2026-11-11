def validate(record):
    if not isinstance(record, dict):
        return ["record"]
    errors = []
    if not isinstance(record.get("id"), str) or not record["id"].strip():
        errors.append("id")
    amount = record.get("amount")
    if isinstance(amount, bool) or not isinstance(amount, (int, float)) or not (amount >= 0):
        errors.append("amount")
    if record.get("currency") not in ("USD", "EUR"):
        errors.append("currency")
    return errors
