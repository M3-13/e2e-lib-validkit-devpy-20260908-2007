"""ISBN-13 validation."""

# Maximum input length accepted by this function before raising.
# Inputs longer than this are rejected up front (AC-14).
_MAX_LENGTH = 10_000


def is_valid_isbn13(text: str) -> bool:
    """Return True if ``text`` is a valid ISBN-13 number.

    Hyphens and spaces are ignored. The string must contain exactly 13
    digits; any other character makes the input invalid. The check digit
    (last digit) is validated with the alternating 1/3 weighting rule: the
    weighted sum of all 13 digits must be a multiple of 10.
    """
    if len(text) > _MAX_LENGTH:
        raise ValueError("is_valid_isbn13: input exceeds maximum length of 10000 characters")

    digits = text.replace("-", "").replace(" ", "")
    if len(digits) != 13:
        return False
    if not all("0" <= ch <= "9" for ch in digits):
        return False

    total = 0
    for index, ch in enumerate(digits):
        value = ord(ch) - ord("0")
        total += value if index % 2 == 0 else value * 3
    return total % 10 == 0
