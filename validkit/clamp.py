def clamp(value: float | int, low: float | int, high: float | int) -> float | int:
    if low > high:
        raise ValueError("clamp: low must not be greater than high")
    if value < low:
        return low
    if value > high:
        return high
    return value
