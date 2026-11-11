"""A bounded loop: predict the result before changing the limit."""


def count_steps(limit: int) -> int:
    return sum(1 for _ in range(max(0, limit)))


if __name__ == "__main__":
    print(count_steps(3))
