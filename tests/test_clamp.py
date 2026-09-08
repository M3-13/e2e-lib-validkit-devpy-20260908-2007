import pytest

from validkit import clamp


def test_value_within_range_is_returned_unchanged():
    assert clamp(5, 0, 10) == 5


def test_value_below_range_returns_low():
    assert clamp(-5, 0, 10) == 0


def test_value_above_range_returns_high():
    assert clamp(15, 0, 10) == 10


def test_value_equal_to_low_is_returned_unchanged():
    assert clamp(0, 0, 10) == 0


def test_value_equal_to_high_is_returned_unchanged():
    assert clamp(10, 0, 10) == 10


def test_low_greater_than_high_raises_value_error():
    with pytest.raises(ValueError):
        clamp(1, 10, 0)


def test_error_message_names_function_and_reason_without_input_values():
    with pytest.raises(ValueError) as excinfo:
        clamp(1, 10, 0)
    message = str(excinfo.value)
    assert message.startswith("clamp: ")
    assert "1" not in message
    assert "10" not in message
    assert "0" not in message


def test_int_inputs_return_int():
    assert isinstance(clamp(5, 0, 10), int)
    assert isinstance(clamp(-5, 0, 10), int)
    assert isinstance(clamp(15, 0, 10), int)


def test_float_inputs_return_float():
    assert clamp(5.5, 0.0, 10.0) == 5.5
    assert isinstance(clamp(5.5, 0.0, 10.0), float)
    assert clamp(-5.5, 0.0, 10.0) == 0.0
    assert clamp(15.5, 0.0, 10.0) == 10.0


def test_float_value_unchanged_with_int_bounds():
    assert clamp(5.5, 0, 10) == 5.5
    assert isinstance(clamp(5.5, 0, 10), float)


def test_int_value_with_float_bounds_stays_int_when_in_range():
    assert clamp(5, 0.0, 10.0) == 5
    assert isinstance(clamp(5, 0.0, 10.0), int)
