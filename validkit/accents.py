import unicodedata

MAX_INPUT_LENGTH = 10_000


def strip_accents(text: str) -> str:
    if len(text) > MAX_INPUT_LENGTH:
        raise ValueError("strip_accents: input exceeds maximum length of 10000 characters")
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(ch for ch in decomposed if unicodedata.category(ch) != "Mn")
