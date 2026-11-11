"""One possible bounded budget implementation."""


def remaining(limit: int, used: int) -> int:
    if limit < 0 or used < 0:
        raise ValueError("budget inputs must be non-negative")
    return max(0, limit - used)
