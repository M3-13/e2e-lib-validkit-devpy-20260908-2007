import pytest

from validkit import slugify


def test_slugify_lowercases_strips_accents_and_replaces_punctuation():
    assert slugify("  Héllo, Wörld!  ") == "hello-world"


def test_slugify_strips_accents_from_other_words():
    assert slugify("Crème brûlée") == "creme-brulee"


def test_slugify_collapses_repeated_hyphens():
    assert slugify("a--b") == "a-b"
    assert slugify("a---b") == "a-b"


def test_slugify_strips_leading_and_trailing_hyphens():
    assert slugify("-hello-world-") == "hello-world"
    assert slugify("--hello--world--") == "hello-world"


def test_slugify_trims_surrounding_whitespace():
    assert slugify("  hello  ") == "hello"


def test_slugify_keeps_alphanumeric_runs():
    assert slugify("Foo Bar 123") == "foo-bar-123"


def test_slugify_handles_empty_and_punctuation_only_input():
    assert slugify("") == ""
    assert slugify("!!!") == ""


def test_slugify_accepts_input_at_max_length():
    text = "a" * 10_000
    assert slugify(text) == text


def test_slugify_rejects_input_above_max_length():
    with pytest.raises(ValueError, match="slugify"):
        slugify("a" * 10_001)


def test_slugify_error_message_does_not_leak_input():
    text = "secret-" * 10_000
    with pytest.raises(ValueError) as excinfo:
        slugify(text)
    message = excinfo.value.args[0]
    assert message.startswith("slugify:")
    assert "secret" not in message


def test_slugify_produces_no_stdout_or_stderr(capsys):
    slugify("Hello, World!")
    assert capsys.readouterr() == ("", "")
