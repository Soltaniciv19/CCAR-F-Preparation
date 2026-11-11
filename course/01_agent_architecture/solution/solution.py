def dispatch(calls, allowed):
    results = []
    for call in calls:
        result = {"id": call["id"]}
        if call.get("name") != "lookup" or "lookup" not in allowed:
            result["error"] = "not_allowed"
        else:
            args = call.get("input")
            order_id = args.get("order_id") if isinstance(args, dict) else None
            if not isinstance(order_id, str) or not order_id.strip():
                result["error"] = "invalid_input"
            else:
                result["result"] = {"order_id": order_id, "status": "shipped"}
        results.append(result)
    return results
