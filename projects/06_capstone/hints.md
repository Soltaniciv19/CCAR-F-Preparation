# Hints

1. Validate the request before calling a service; an ambiguous request needs a human.
2. Keep one counter for every service invocation. A failure is still a call.
3. Record each policy's ID and date before comparing its decision with others.
4. Treat failures and incomplete evidence as escalation, not a negative eligibility finding.
