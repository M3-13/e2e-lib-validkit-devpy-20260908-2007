import pytest

from validkit.luhn import luhn_check


@pytest.mark.parametrize(
    "digits",
    [
        "4532015112830366",
        "79927398713",
        "0" * 2,
        "00",
    ],
)
def test_luhn_check_valid(digits):
    assert luhn_check(digits) is True


@pytest.mark.parametrize(
    "digits",
    [
        "4532015112830367",
        "123",
        "12a4",
        "",
        "7",
        "1",
        "a",
        "12 34",
        "12-34",
    ],
)
def test_luhn_check_invalid(digits):
    assert luhn_check(digits) is False


def test_luhn_check_single_digit_is_false():
    assert luhn_check("0") is False


def test_luhn_check_non_ascii_digits_are_false():
    assert luhn_check("١٢") is False


def test_luhn_check_known_visa_card():
    assert luhn_check("4532015112830366") is True


def test_luhn_check_known_visa_card_wrong_check_digit():
    assert luhn_check("4532015112830367") is False


def test_luhn_check_just_under_max_length_does_not_raise():
    digits = "0" * 10_000
    assert luhn_check(digits) in (True, False)


def test_luhn_check_over_max_length_raises_value_error():
    with pytest.raises(ValueError):
        luhn_check("0" * 10_001)


def test_luhn_check_error_message_has_no_input_values():
    digits = "5" * 10_001
    with pytest.raises(ValueError) as excinfo:
        luhn_check(digits)
    message = str(excinfo.value)
    assert message.startswith("luhn_check:")
    assert "5" not in message
    assert "10_001" not in message


def test_luhn_check_error_message_mentions_function_and_reason():
    with pytest.raises(ValueError) as excinfo:
        luhn_check("0" * 10_001)
    message = str(excinfo.value)
    assert "luhn_check" in message
    assert "maximum length" in message
