"""Conflicting facts stay attributed instead of being silently merged."""

evidence = [
    {"source": "policy-a", "date": "2025-01-01", "fact": "14 days"},
    {"source": "policy-b", "date": "2025-02-01", "fact": "30 days"},
]
for item in evidence:
    print(f"{item['source']} ({item['date']}): {item['fact']}")
print("Conflict: verify which policy applies or escalate.")
