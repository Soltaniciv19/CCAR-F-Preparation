"""Contrast syntax with a simple semantic check."""

import json

record = json.loads('{"id":"A-1","amount":-2,"currency":"USD"}')
print("JSON parsed:", record)
print("nonnegative amount:", record["amount"] >= 0)
