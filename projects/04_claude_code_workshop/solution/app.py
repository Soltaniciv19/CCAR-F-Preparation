import json
import sys
from pricing import quote

try:
    if len(sys.argv) != 4:
        raise ValueError("expected subtotal, discount and shipping")
    print(json.dumps({"total": quote(*map(float, sys.argv[1:]))}))
except ValueError as exc:
    print(str(exc), file=sys.stderr)
    sys.exit(2)
