import pytest

from validkit.secret import MAX_TEXT_LENGTH, mask_secret


def test_masks_all_but_last_four():
    assert mask_secret("geheim12345", 4) == "*******2345"


def test_text_shorter_or_equal_to_keep_stays_visible():
    assert mask_secret("abc", 4) == "abc"
    assert mask_secret("abcd", 4) == "abcd"


def test_keep_zero_masks_everything():
    assert mask_secret("abcd", 0) == "****"


def test_default_keep_is_four():
    assert mask_secret("12345678") == "****5678"


def test_empty_text_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("", 4)


def test_none_text_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret(None, 4)


def test_negative_keep_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("x", -1)


def test_text_over_max_length_raises_value_error():
    with pytest.raises(ValueError):
        mask_secret("a" * (MAX_TEXT_LENGTH + 1), 4)


def test_text_exactly_max_length_is_accepted():
    result = mask_secret("a" * MAX_TEXT_LENGTH, 4)
    assert result == "*" * (MAX_TEXT_LENGTH - 4) + "aaaa"


def test_error_message_names_function_and_reason_without_input_values():
    with pytest.raises(ValueError) as exc_info:
        mask_secret("x", -1)
    msg = str(exc_info.value)
    assert msg.startswith("mask_secret:")
    assert "x" not in msg


def test_error_message_does_not_leak_long_input():
    with pytest.raises(ValueError) as exc_info:
        mask_secret("sekret" + "Z" * MAX_TEXT_LENGTH, 4)
    msg = str(exc_info.value)
    assert "sekret" not in msg
    assert "Z" not in msg


def test_return_consists_only_of_stars_and_last_keep_chars():
    result = mask_secret("geheim12345", 4)
    assert result == "*" * 7 + "2345"
    assert set(result) == {"*", "2", "3", "4", "5"}


def test_no_output_on_stdout_or_stderr(capsys):
    mask_secret("geheim12345", 4)
    with pytest.raises(ValueError):
        mask_secret("x", -1)
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
