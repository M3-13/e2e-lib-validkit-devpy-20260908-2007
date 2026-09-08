import pytest

from validkit import normalize_phone


def test_ac06_national_number():
    assert normalize_phone("030 1234567", "DE") == "+49301234567"


def test_ac06_international_with_plus():
    assert normalize_phone("+49 30 1234567", "DE") == "+49301234567"


def test_ac06_international_with_double_zero():
    assert normalize_phone("0049 30 1234567", "DE") == "+49301234567"


@pytest.mark.parametrize(
    ("text", "country", "expected"),
    [
        ("01 2345678", "AT", "+4312345678"),
        ("022 123 45 67", "CH", "+41221234567"),
        ("202 555 0123", "US", "+12025550123"),
        ("020 7946 0958", "GB", "+442079460958"),
        ("01 23 45 67 89", "FR", "+33123456789"),
    ],
)
def test_national_number_prepends_country_code(text, country, expected):
    assert normalize_phone(text, country) == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("+43 1 234567", "+431234567"),
        ("+41 22 123 45 67", "+41221234567"),
        ("+1 202 555 0123", "+12025550123"),
        ("+44 20 7946 0958", "+442079460958"),
        ("+33 1 23 45 67 89", "+33123456789"),
        ("0041 22 123 45 67", "+41221234567"),
    ],
)
def test_international_number_reads_dialing_code_from_input(text, expected):
    assert normalize_phone(text, "DE") == expected


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("030-1234567", "+49301234567"),
        ("(030) 1234567", "+49301234567"),
        ("030.123.4567", "+49301234567"),
        ("030 123 45 67", "+49301234567"),
        ("0301234567", "+49301234567"),
    ],
)
def test_separators_are_removed(text, expected):
    assert normalize_phone(text, "DE") == expected


def test_lowercase_country_code_is_accepted():
    assert normalize_phone("030 1234567", "de") == "+49301234567"


@pytest.mark.parametrize("text", ["", "abc", "123", "()-. ", "+", "00"])
def test_invalid_inputs_raise_value_error(text):
    with pytest.raises(ValueError):
        normalize_phone(text, "DE")


@pytest.mark.parametrize("text", ["030a", "49+30", "030 12x3 4567", "+ 49"])
def test_invalid_characters_raise_value_error(text):
    with pytest.raises(ValueError):
        normalize_phone(text, "DE")


@pytest.mark.parametrize("country", ["ZZ", "xx", "USA", ""])
def test_unknown_country_code_raises_value_error(country):
    with pytest.raises(ValueError):
        normalize_phone("030 1234567", country)


def test_minimum_length_boundary_is_inclusive():
    assert normalize_phone("1234567", "US") == "+11234567"


def test_below_minimum_length_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("123456", "US")


def test_maximum_length_boundary_is_inclusive():
    assert normalize_phone("12345678901234", "US") == "+112345678901234"


def test_above_maximum_length_raises_value_error():
    with pytest.raises(ValueError):
        normalize_phone("123456789012345", "US")


def test_input_over_documented_max_length_raises_before_processing():
    with pytest.raises(ValueError, match="normalize_phone: input too long"):
        normalize_phone("1" * 10_001, "DE")


def test_unknown_international_dialing_code_raises_value_error():
    with pytest.raises(ValueError, match="unknown international dialing code"):
        normalize_phone("+39 06 12345678", "DE")


@pytest.mark.parametrize(
    ("text", "country"),
    [
        ("abc", "DE"),
        ("123", "DE"),
        ("030 1234567x", "DE"),
        ("+" + "9" * 20, "DE"),
    ],
)
def test_error_message_names_function_and_hides_input(text, country):
    with pytest.raises(ValueError) as exc:
        normalize_phone(text, country)
    message = str(exc.value)
    assert message.startswith("normalize_phone:")
    assert text not in message
    assert country not in message


def test_no_output_on_stdout_or_stderr(capsys):
    normalize_phone("030 1234567", "DE")
    normalize_phone("+49 30 1234567", "DE")
    with pytest.raises(ValueError):
        normalize_phone("abc", "DE")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
