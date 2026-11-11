import math


def quote(subtotal: float, discount: float, shipping: float) -> float:
    if (
        not all(math.isfinite(value) for value in (subtotal, discount, shipping))
        or subtotal < 0
        or shipping < 0
        or not 0 <= discount <= 1
    ):
        raise ValueError("amounts must be non-negative and discount between 0 and 1")
    return round(subtotal * (1 - discount) + shipping, 2)
