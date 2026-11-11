# Hints

1. Check types before ranges: Python booleans are integers for `isinstance`.
2. Retain a dictionary keyed by input ID and send only unresolved requests on the next attempt.
3. Preserve validation messages in the next request's feedback; retry only while attempts remain.
4. Evaluate predictions on the same IDs as the holdout and verify review evidence against source lines.
