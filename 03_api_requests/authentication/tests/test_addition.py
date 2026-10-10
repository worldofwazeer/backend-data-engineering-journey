import pytest


def add(a, b):
    return a + b


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2, 3, 5),
        (10, 5, 15),
        (0, 4, 4),
        (-2, 2, 0),
    ],
)
def test_add_returns_expected_result(a, b, expected):
    result = add(a, b)

    assert result == expected