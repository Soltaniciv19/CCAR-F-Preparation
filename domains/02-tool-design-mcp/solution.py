"""Runnable offline worked solution. Run this file from any working directory."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from ccarf.tools import lookup_order, retry_read

orders = {"O-100": {"customer_id": "C-7", "status": "paid"}}
print("Accessible:", lookup_order({"order_id": "O-100"}, customer_id="C-7", orders=orders))
print(
    "No accessible match:",
    lookup_order({"order_id": "O-100"}, customer_id="C-other", orders=orders),
)
count = 0


def read():
    global count
    count += 1
    if count < 3:
        raise TimeoutError
    return {"ok": True, "data": []}


print("Recovered read:", retry_read(read, sleep=lambda delay: print("Backoff:", delay)))
