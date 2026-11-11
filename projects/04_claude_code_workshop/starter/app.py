import json
import sys

subtotal, discount, shipping = map(float, sys.argv[1:])
print(json.dumps({"total": round((subtotal + shipping) * (1 - discount), 2)}))
