"""IBAN validation.

Implements the ISO 13616 / SWIFT IBAN check: strip spaces, verify the
two-letter country code and its country-specific length, then run the full
modulo-97 checksum.
"""

# Maximum accepted input length (AC-14). Anything longer is rejected with a
# ValueError before any processing so the modulo arithmetic stays bounded.
_MAX_INPUT_LENGTH = 10_000

# Country-specific IBAN lengths from the SWIFT registry.
_IBAN_LENGTHS = {
    "AL": 28,
    "AD": 24,
    "AT": 20,
    "AZ": 28,
    "BH": 22,
    "BY": 28,
    "BE": 16,
    "BA": 20,
    "BR": 29,
    "BG": 22,
    "CR": 22,
    "HR": 21,
    "CY": 28,
    "CZ": 24,
    "DK": 18,
    "DO": 28,
    "EG": 29,
    "SV": 28,
    "EE": 20,
    "FO": 18,
    "FI": 18,
    "FR": 27,
    "GE": 22,
    "DE": 22,
    "GI": 23,
    "GR": 27,
    "GL": 18,
    "GT": 28,
    "HU": 28,
    "IS": 26,
    "IE": 22,
    "IL": 23,
    "IT": 27,
    "JO": 30,
    "KZ": 20,
    "XK": 20,
    "KW": 30,
    "LV": 21,
    "LB": 28,
    "LI": 21,
    "LT": 20,
    "LU": 20,
    "MT": 31,
    "MR": 27,
    "MU": 30,
    "MD": 24,
    "MC": 27,
    "ME": 22,
    "NL": 18,
    "MK": 19,
    "NO": 15,
    "PK": 24,
    "PS": 29,
    "PL": 28,
    "PT": 25,
    "QA": 29,
    "RO": 24,
    "SM": 27,
    "SA": 24,
    "RS": 22,
    "SK": 24,
    "SI": 19,
    "ES": 24,
    "SE": 24,
    "CH": 21,
    "TL": 23,
    "TN": 24,
    "TR": 26,
    "UA": 29,
    "AE": 23,
    "GB": 22,
    "VA": 22,
    "VG": 24,
}


def _mod97(number: str) -> int:
    remainder = 0
    for char in number:
        remainder = (remainder * 10 + int(char)) % 97
    return remainder


def is_valid_iban(text: str) -> bool:
    if len(text) > _MAX_INPUT_LENGTH:
        raise ValueError("is_valid_iban: input exceeds maximum length of 10000 characters")

    compact = text.replace(" ", "")

    country = compact[:2]
    expected_length = _IBAN_LENGTHS.get(country)
    if expected_length is None or len(compact) != expected_length:
        return False

    for char in compact:
        if not char.isdigit() and not ("A" <= char <= "Z"):
            return False

    rearranged = compact[4:] + compact[:4]
    digits = "".join(
        str(ord(char) - ord("A") + 10) if "A" <= char <= "Z" else char for char in rearranged
    )
    return _mod97(digits) == 1
