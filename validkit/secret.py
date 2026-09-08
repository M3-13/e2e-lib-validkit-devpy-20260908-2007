MAX_TEXT_LENGTH = 10_000


def mask_secret(text: str, keep: int = 4) -> str:
    if text is None:
        raise ValueError("mask_secret: text must not be None")
    if keep < 0:
        raise ValueError("mask_secret: keep must not be negative")
    if text == "":
        raise ValueError("mask_secret: text must not be empty")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError("mask_secret: text exceeds maximum length")
    if keep == 0:
        return "*" * len(text)
    if len(text) <= keep:
        return text
    return "*" * (len(text) - keep) + text[-keep:]
