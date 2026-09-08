import re
import unicodedata

# Maximale zulässige Eingabelänge in Zeichen (AC-14).
_MAX_TEXT_LENGTH = 10_000

_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(text: str) -> str:
    """Return a URL-safe slug for *text*.

    Lowercases the input, strips accents via Unicode NFKD decomposition and
    replaces every run of non-alphanumeric characters with a single ``-``.
    Inputs longer than 10_000 characters are rejected with a ``ValueError``.
    """
    if len(text) > _MAX_TEXT_LENGTH:
        raise ValueError(f"slugify: text exceeds maximum length of {_MAX_TEXT_LENGTH} characters")

    decomposed = unicodedata.normalize("NFKD", text)
    without_marks = "".join(c for c in decomposed if not unicodedata.combining(c))
    return _ALNUM.sub("-", without_marks.lower()).strip("-")
