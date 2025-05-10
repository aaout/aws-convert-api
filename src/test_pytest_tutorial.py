import pytest
from pytest_tutorial import return_odd_or_even


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, "Odd"),
        (2, "Odd"),  # あえてOddにしておく エラーケース
        (3, "Even"),  # あえてEvenにしておく エラーケース
        (4, "Even"),
        (5, "Odd"),
        (6, "Even"),
        (7, "Odd"),
        (8, "Even"),
        (9, "Odd"),
        (10, "Even"),
    ],
)
def test_return_odd_or_even(number, expected):
    assert return_odd_or_even(number) == expected
