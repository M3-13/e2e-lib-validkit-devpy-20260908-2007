import pytest

from validkit.iban import is_valid_iban

VALID_IBANS = [
    "DE89 3704 0044 0532 0130 00",
    "DE89370400440532013000",
    "GB82 WEST 1234 5698 7654 32",
    "FR14 2004 1010 0505 0001 3M02 606",
]


@pytest.mark.parametrize("iban", VALID_IBANS)
def test_valid_ibans_return_true(iban):
    assert is_valid_iban(iban) is True


@pytest.mark.parametrize(
    "iban",
    [
        "DE89 3704 0044 0532 0130 10",
        "DE89 3704 0044 0532 1030 00",
        "FR89 3704 0044 0532 0130 00",
        "XX89 3704 0044 0532 0130 00",
        "DE89 3704 0044 0532 0130 0",
        "DE89 3704 0044 0532 0130 0000",
        "DE89 3704 0044 0532 0130 0a",
        "",
        "DE89",
    ],
)
def test_invalid_ibans_return_false(iban):
    assert is_valid_iban(iban) is False


def test_input_over_max_length_raises_value_error():
    with pytest.raises(ValueError):
        is_valid_iban("A" * 10_001)


def test_input_at_max_length_does_not_raise():
    assert is_valid_iban("A" * 10_000) is False


def test_value_error_names_function_and_reason_without_leaking_input(capsys):
    with pytest.raises(ValueError) as exc:
        is_valid_iban("Q" * 10_001)
    message = str(exc.value)
    assert "is_valid_iban" in message
    assert "Q" not in message
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_no_output_on_stdout_or_stderr(capsys):
    is_valid_iban("DE89 3704 0044 0532 0130 00")
    is_valid_iban("XX89 3704 0044 0532 0130 00")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
