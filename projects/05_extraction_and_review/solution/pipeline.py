"""An offline example of validation, correlation and evidence checks."""

import ast


def validate_record(record):
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = []
    if not isinstance(record.get("merchant"), str) or not record["merchant"].strip():
        errors.append("merchant is required")
    amount = record.get("amount_cents")
    if type(amount) is not int or amount <= 0:
        errors.append("amount_cents must be a positive integer")
    if record.get("currency") != "USD":
        errors.append("currency must be USD")
    return errors


def process_batch(inputs, extractor, max_attempts=2):
    if type(max_attempts) is not int or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    items = {item["id"]: item for item in inputs}
    if len(items) != len(inputs):
        raise ValueError("duplicate input ID")
    pending = {key: "" for key in items}
    outcomes = {}
    for attempt in range(1, max_attempts + 1):
        if not pending:
            break
        requests = [
            {"id": key, "text": items[key]["text"], "feedback": feedback}
            for key, feedback in pending.items()
        ]
        responses = extractor(requests)
        received = {}
        for response in responses:
            key = response.get("id")
            if key not in pending or key in received:
                raise ValueError("unknown or duplicate response ID")
            received[key] = response
        next_pending = {}
        for key in pending:
            response = received.get(key)
            if response is None:
                error, retryable = "missing response", True
            elif "error" in response:
                error_info = response["error"]
                if (
                    not isinstance(error_info, dict)
                    or type(error_info.get("retryable")) is not bool
                    or not isinstance(error_info.get("message"), str)
                ):
                    raise ValueError("invalid error response")
                error, retryable = error_info["message"], error_info["retryable"]
            else:
                errors = validate_record(response.get("record"))
                if not errors:
                    outcomes[key] = {
                        "status": "ok",
                        "record": response["record"],
                        "attempts": attempt,
                    }
                    continue
                error, retryable = "; ".join(errors), True
            if retryable and attempt < max_attempts:
                next_pending[key] = error
            else:
                outcomes[key] = {
                    "status": "error",
                    "error": error,
                    "retryable": retryable,
                    "attempts": attempt,
                }
        pending = next_pending
    return outcomes


def evaluate(expected, predicted):
    # Non-null labels represent assessable positives; missing labels stay uncertain.
    labels = {key: value for key, value in expected.items() if value is not None}
    predictions = {
        key: value for key, value in predicted.items() if value is not None and key in labels
    }
    matches = sum(predictions.get(key) == value for key, value in labels.items())
    return {
        "precision": matches / len(predictions) if predictions else 0.0,
        "recall": matches / len(labels) if labels else 0.0,
    }


def review(source):
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    lines = source.splitlines()
    candidates = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "eval"
        ):
            candidates.append(
                {
                    "line": node.lineno,
                    "evidence": lines[node.lineno - 1],
                    "issue": "eval executes supplied code",
                }
            )
    return [
        item
        for item in candidates
        if 1 <= item["line"] <= len(lines) and lines[item["line"] - 1] == item["evidence"]
    ]
