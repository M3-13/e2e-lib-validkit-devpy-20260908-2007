"""E.164 phone number normalization."""

# ISO 3166-1 alpha-2 country code -> international dialing code.
_COUNTRY_DIALING_CODES: dict[str, str] = {
    "DE": "49",
    "AT": "43",
    "CH": "41",
    "US": "1",
    "GB": "44",
    "FR": "33",
}

# Sorted longest-first so the longest dialing code wins when reading the
# country back out of an international number.
_COUNTRY_CODES_BY_DIALING_LENGTH: tuple[tuple[str, str], ...] = tuple(
    sorted(_COUNTRY_DIALING_CODES.items(), key=lambda item: len(item[1]), reverse=True)
)

_DIGITS = "0123456789"
_SEPARATORS = " -()."
# Documented maximum input length (see AC-14): inputs longer than this are
# rejected with a ValueError before any processing.
_MAX_INPUT_LENGTH = 10_000
# Valid E.164 national significant number length, excluding the leading '+'.
_MIN_DIGITS = 8
_MAX_DIGITS = 15


def _match_dialing_code(number: str) -> str:
    """Return the ISO country code whose dialing code *number* starts with.

    Longest match wins; a number matching no known dialing code is invalid.
    """
    for code, dialing in _COUNTRY_CODES_BY_DIALING_LENGTH:
        if number.startswith(dialing):
            return code
    raise ValueError("normalize_phone: unknown international dialing code")


def normalize_phone(text: str, country_code: str) -> str:
    """Normalize *text* into E.164 form (``+`` followed by digits only).

    - Inputs longer than ``10_000`` characters are rejected with a ValueError
      before any processing.
    - A leading ``+`` or ``00`` marks an international number: its dialing code
      is read from the number itself (longest match against the mapping above)
      and the digits are kept as-is.
    - Otherwise the number is national: the leading trunk prefix ``0`` is
      dropped and the dialing code of *country_code* is prepended.
    - Spaces and the separators ``-``, ``(``, ``)``, ``.`` are removed; the
      result must contain between 8 and 15 digits.
    """
    if len(text) > _MAX_INPUT_LENGTH:
        raise ValueError("normalize_phone: input too long")

    if not text:
        raise ValueError("normalize_phone: empty input")

    if len(country_code) > _MAX_INPUT_LENGTH:
        raise ValueError("normalize_phone: country code too long")

    country = country_code.strip().upper()
    if country not in _COUNTRY_DIALING_CODES:
        raise ValueError("normalize_phone: unknown country code")

    if text.startswith("+"):
        body = text[1:]
        international = True
    elif text.startswith("00"):
        body = text[2:]
        international = True
    else:
        body = text
        international = False

    digits: list[str] = []
    for ch in body:
        if ch in _SEPARATORS:
            continue
        if ch not in _DIGITS:
            raise ValueError("normalize_phone: invalid characters")
        digits.append(ch)

    number = "".join(digits)
    if not number:
        raise ValueError("normalize_phone: empty number")

    if international:
        _match_dialing_code(number)
    else:
        if number.startswith("0"):
            number = number[1:]
        number = _COUNTRY_DIALING_CODES[country] + number

    if not _MIN_DIGITS <= len(number) <= _MAX_DIGITS:
        raise ValueError("normalize_phone: number length out of range")

    return "+" + number
