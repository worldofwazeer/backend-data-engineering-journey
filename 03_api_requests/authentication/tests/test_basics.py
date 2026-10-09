import pytest


def get_items(limit):
    if limit <= 0:
        raise ValueError("limit must be positive")

    return limit


def test_get_items_with_valid_limit():
    result = get_items(10)

    assert result == 10


def test_get_items_rejects_zero():
    with pytest.raises(
        ValueError,
        match="limit must be positive",
    ):
        get_items(0)


def test_get_items_rejects_negative_limit():
    with pytest.raises(ValueError):
        get_items(-2)

def test_get_items_accepts_minimum_valid_limit():
    result = get_items(1)

    assert result == 1