import pytest

from validkit.isbn import is_valid_isbn13


@pytest.mark.parametrize(
    "text",
    [
        "978-3-16-148410-0",
        "9783161484100",
        "978 3 16 148410 0",
        "978-1-4028-9462-6",
        "978-0-306-40615-7",
    ],
)
def test_valid_isbn13(text):
    assert is_valid_isbn13(text) is True


@pytest.mark.parametrize(
    "text",
    [
        "978-3-16-148410-1",
        "9783161484101",
        "978-1-4028-9462-7",
        "978-0-306-40615-8",
    ],
)
def test_invalid_check_digit(text):
    assert is_valid_isbn13(text) is False


def test_ten_digit_isbn_is_rejected():
    assert is_valid_isbn13("3-16-148410-0") is False


def test_wrong_digit_count_is_rejected():
    assert is_valid_isbn13("978-3-16-148410") is False
    assert is_valid_isbn13("978-3-16-148410-00") is False
    assert is_valid_isbn13("") is False


def test_non_digit_characters_are_rejected():
    assert is_valid_isbn13("978-3-16-14841X-0") is False
    assert is_valid_isbn13("978-3-16-148410-O") is False
    assert is_valid_isbn13("978-3-16-148410-0!") is False
    assert is_valid_isbn13("abc") is False


def test_exactly_thirteen_digits_after_ignoring_separators():
    assert is_valid_isbn13("9-7-8-3-1-6-1-4-8-4-1-0-0") is True


def test_overlong_input_raises_value_error():
    with pytest.raises(ValueError, match="is_valid_isbn13:"):
        is_valid_isbn13("1" * 10_001)


def test_overlong_input_message_hides_input_values():
    with pytest.raises(ValueError) as exc_info:
        is_valid_isbn13("9" * 10_001)
    message = str(exc_info.value)
    assert "9" not in message
    assert "is_valid_isbn13:" in message


def test_exactly_ten_thousand_characters_does_not_raise():
    assert is_valid_isbn13("x" * 10_000) is False
