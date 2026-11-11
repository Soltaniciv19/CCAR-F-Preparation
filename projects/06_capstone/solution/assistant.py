"""A bounded, offline support decision simulation."""


class ServiceError(Exception):
    def __init__(self, message, retryable=False):
        super().__init__(message)
        self.retryable = retryable


def assist(request, services, max_calls=3):
    if type(max_calls) is not int or max_calls < 0:
        raise ValueError("max_calls must be a non-negative integer")
    result = {
        "decision": "escalate",
        "reasons": [],
        "citations": [],
        "coverage": "partial",
        "calls": 0,
        "handoff": None,
    }

    def finish(decision, reason):
        result["decision"] = decision
        result["reasons"].append(reason)
        if decision == "escalate":
            result["handoff"] = {
                "reason": reason,
                "order_id": request.get("order_id"),
                "coverage": result["coverage"],
            }
        return result

    if (
        not isinstance(request.get("order_id"), str)
        or not request["order_id"].strip()
        or request.get("requested_action") not in ("refund", "explain")
    ):
        return finish("escalate", "ambiguous request")

    def call(operation, *args):
        if result["calls"] >= max_calls:
            raise ServiceError("call budget exhausted")
        result["calls"] += 1
        return operation(*args)

    try:
        order = call(services.get_order, request["order_id"])
        if not isinstance(order, dict) or type(order.get("eligible")) is not bool:
            return finish("escalate", "order missing or ambiguous")
        policies = call(services.get_policies)
    except ServiceError as exc:
        return finish("escalate", f"service unavailable: {exc}")

    if not isinstance(policies, list) or not policies:
        return finish("escalate", "policy evidence missing")
    for policy in policies:
        if (
            not isinstance(policy, dict)
            or not isinstance(policy.get("id"), str)
            or not policy["id"]
            or not isinstance(policy.get("date"), str)
            or not policy["date"]
            or type(policy.get("refund_allowed")) is not bool
        ):
            return finish("escalate", "policy evidence incomplete")
        result["citations"].append({"id": policy["id"], "date": policy["date"]})
    result["coverage"] = "complete"
    decisions = {policy["refund_allowed"] for policy in policies}
    if len(decisions) != 1:
        return finish("escalate", "conflicting policy sources")
    if request["requested_action"] == "explain":
        return finish("allow", "evidence collected for explanation")
    if not order["eligible"] or not next(iter(decisions)):
        return finish("deny", "refund not authorized by order eligibility and policy")
    return finish("allow", "simulated refund is eligible and policy permits it")
