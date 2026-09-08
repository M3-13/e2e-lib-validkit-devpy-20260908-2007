import pytest

from validkit.accents import MAX_INPUT_LENGTH, strip_accents


def test_removes_accents_from_latin_text():
    assert strip_accents("Crème brûlée — déjà vu") == "Creme brulee — deja vu"


def test_keeps_em_dash_unchanged():
    assert strip_accents("a—b") == "a—b"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("café", "cafe"),
        ("naïve", "naive"),
        ("über", "uber"),
        ("straße", "straße"),
        ("Ångström", "Angstrom"),
        ("München", "Munchen"),
        ("élève", "eleve"),
        ("coöperate", "cooperate"),
        ("façade", "facade"),
        ("niño", "nino"),
    ],
)
def test_removes_common_accents(text, expected):
    assert strip_accents(text) == expected


def test_empty_string():
    assert strip_accents("") == ""


def test_text_without_accents_unchanged():
    assert strip_accents("plain ascii 123 !@#") == "plain ascii 123 !@#"


def test_non_latin_script_unchanged():
    assert strip_accents("αβγδε 中文") == "αβγδε 中文"


def test_boundary_exactly_max_length_is_processed():
    text = "a" * MAX_INPUT_LENGTH
    assert strip_accents(text) == text


def test_over_max_length_raises_value_error():
    text = "a" * (MAX_INPUT_LENGTH + 1)
    with pytest.raises(ValueError):
        strip_accents(text)


def test_error_message_names_function_and_reason_but_not_input():
    secret_value = "top-secret-" * 2000
    with pytest.raises(ValueError) as excinfo:
        strip_accents(secret_value)
    message = str(excinfo.value)
    assert "strip_accents" in message
    assert "length" in message
    assert "top-secret" not in message
    assert "/" not in message and "\\" not in message


def test_no_output_on_stdout_or_stderr(capsys):
    strip_accents("Crème brûlée — déjà vu")
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
