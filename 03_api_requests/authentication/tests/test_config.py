import pytest

from config import _parse_int_setting


def test_parse_int_setting_converts_valid_integer_string():
    # Arrange
    setting_name = "MAX_RETRIES"
    raw_value = "15"

    # Act
    result = _parse_int_setting(
        setting_name,
        raw_value,
        default=3,
        minimum=0,
    )

    # Assert
    assert result == 15
    assert isinstance(result, int)


@pytest.mark.parametrize(
    ("raw_value", "minimum", "expected"),
    [
        ("1", 1, 1),
        ("0", 0, 0),
    ],
)
def test_parse_int_setting_accepts_value_equal_to_minimum(
    raw_value,
    minimum,
    expected,
):
    # Arrange
    setting_name = "MAX_RETRIES"

    # Act
    result = _parse_int_setting(
        setting_name,
        raw_value,
        default=3,
        minimum=minimum,
    )

    # Assert
    assert result == expected
    assert isinstance(result, int)


def test_parse_int_setting_uses_integer_default_when_value_is_missing():
    # Arrange
    setting_name = "TIMEOUT"
    default = 15

    # Act
    result = _parse_int_setting(
        setting_name,
        None,
        default=default,
        minimum=1,
    )

    # Assert
    assert result == default
    assert isinstance(result, int)


@pytest.mark.parametrize("raw_value", ["abc", ""])
def test_parse_int_setting_rejects_invalid_integer_strings(raw_value):
    # Arrange
    setting_name = "TIMEOUT"

    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        _parse_int_setting(
            setting_name,
            raw_value,
            default=15,
            minimum=1,
        )

    assert str(exc_info.value) == f"{setting_name} must be an integer."


@pytest.mark.parametrize(
    ("raw_value", "minimum"),
    [
        ("0", 1),
        ("-1", 0),
    ],
)
def test_parse_int_setting_rejects_values_below_minimum(
    raw_value,
    minimum,
):
    # Arrange
    setting_name = "MAX_RETRIES"

    # Act / Assert
    with pytest.raises(ValueError) as exc_info:
        _parse_int_setting(
            setting_name,
            raw_value,
            default=3,
            minimum=minimum,
        )

    assert str(exc_info.value) == (
        f"{setting_name} must be greater than or equal to {minimum}."
    )

