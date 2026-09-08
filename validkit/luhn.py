_MAX_LENGTH = 10_000


def luhn_check(digits: str) -> bool:
    """Return whether ``digits`` is a valid Luhn number.

    The Luhn algorithm doubles every second digit counting from the right,
    reduces doubled values above 9 to their digit sum, and requires the total
    to be a multiple of 10 (the last digit is the check digit).

    Non-digit input and inputs shorter than two characters return ``False``.
    Inputs longer than ``_MAX_LENGTH`` (10 000 characters) raise a
    ``ValueError`` before any processing.
    """
    if len(digits) > _MAX_LENGTH:
        raise ValueError("luhn_check: input exceeds the maximum length of 10000 characters")
    if len(digits) < 2:
        return False
    if not digits.isascii() or not digits.isdigit():
        return False

    total = 0
    parity = len(digits) % 2
    for index, char in enumerate(digits):
        value = ord(char) - ord("0")
        if index % 2 == parity:
            value *= 2
            if value > 9:
                value -= 9
        total += value
    return total % 10 == 0
