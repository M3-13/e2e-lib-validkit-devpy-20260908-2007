MAX_EMAIL_LENGTH = 254
MIN_TLD_LENGTH = 2


def is_valid_email(text: str) -> bool:
    if text is None:
        return False
    if not isinstance(text, str):
        return False
    if len(text) > MAX_EMAIL_LENGTH:
        raise ValueError("is_valid_email: text exceeds 254 characters")
    if text == "":
        return False
    if any(char.isspace() for char in text):
        return False
    if text.count("@") != 1:
        return False
    local, domain = text.split("@")
    if not local or not domain:
        return False
    if "." not in domain:
        return False
    labels = domain.split(".")
    if any(not label for label in labels):
        return False
    tld = labels[-1]
    if len(tld) < MIN_TLD_LENGTH:
        return False
    return tld.isalpha()
