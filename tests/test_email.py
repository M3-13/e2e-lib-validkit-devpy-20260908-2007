import pytest

from validkit.email import is_valid_email


@pytest.mark.parametrize(
    "address",
    [
        "test@example.com",
        "user.name+tag@example.co.uk",
        "user@sub.domain.org",
        "a.b@example.com",
        "first.last@example.de",
    ],
)
def test_valid_emails(address):
    assert is_valid_email(address) is True


@pytest.mark.parametrize(
    "address",
    [
        "test@",
        "test@example",
        "a@b.c",
        "",
        None,
        "@example.com",
        "test@@example.com",
        "test@.com",
        "test@example.",
        "test@example.c",
        "test@example.c0m",
        "user name@example.com",
        "test@example.com ",
        "test@ example.com",
    ],
)
def test_invalid_emails(address):
    assert is_valid_email(address) is False


def test_email_at_maximum_length_is_valid():
    address = "a" * 242 + "@example.com"
    assert len(address) == 254
    assert is_valid_email(address) is True


def test_email_over_maximum_length_raises_value_error():
    address = "a" * 243 + "@example.com"
    assert len(address) == 255
    with pytest.raises(ValueError, match="is_valid_email"):
        is_valid_email(address)


def test_value_error_message_does_not_leak_input():
    address = "x" * 300
    with pytest.raises(ValueError) as exc_info:
        is_valid_email(address)
    message = str(exc_info.value)
    assert "is_valid_email" in message
    assert "300" not in message
    assert "x" * 300 not in message
