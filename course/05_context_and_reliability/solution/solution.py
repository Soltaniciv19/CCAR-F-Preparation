def summarize(results):
    evidence = []
    failed = []
    for item in results:
        if "error" in item:
            failed.append(item["source"])
        else:
            evidence.append({key: item[key] for key in ("source", "date", "fact")})
    return {"evidence": evidence, "failed_sources": failed, "partial": bool(failed)}
