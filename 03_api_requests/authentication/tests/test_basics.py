import pytest


def get_items(limit):
    if limit <= 0:
        raise ValueError("limit must be positive")

    return limit


@pytest.mark.parametrize("limit", [1, 10, 25])
def test_get_items_accepts_valid_limit(limit):
    result = get_items(limit)

    assert result == limit


@pytest.mark.parametrize("limit", [0, -1, -2])
def test_get_items_rejects_invalid_limit(limit):
    with pytest.raises(
        ValueError,
        match="limit must be positive",
    ):
        get_items(limit)