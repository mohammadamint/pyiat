import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest
from pyiat.core.impact import Indicator
from pyiat.error_log.errors import InvalidInput
from pyiat.utils.constants import EFFECT


@pytest.fixture
def NegativeIndicator():

    return Indicator(
        name="dummy name", unit="dummy unit", ex_ante=1, ex_post=4, type="negative"
    )


@pytest.fixture
def PositiveIndicator():

    return Indicator(name="dummy", unit="dummy", ex_ante=1, ex_post=4, type="positive")


def test_set_properties(NegativeIndicator):

    invalid_inputs = [
        ("ex_ante", [10, -1, "dummy"]),
        ("ex_post", [10, -1, "dummy"]),
        ("type", ["dummy"]),
    ]

    for parameter, invalids in invalid_inputs:
        for invalid in invalids:
            with pytest.raises(InvalidInput) as msg:
                setattr(NegativeIndicator, parameter, invalid)

            assert "Valid inputs" in str(msg.value)


def test_effect_calculation(NegativeIndicator):

    ex_ante = 1
    ex_post = 4
    type = "negative"
    diff = ex_post - ex_ante

    expected_output = EFFECT[type][diff]

    assert expected_output == NegativeIndicator.effect


def test_normalization(NegativeIndicator, PositiveIndicator):

    normalized_values = [NegativeIndicator.normalized, PositiveIndicator.normalized]

    expected_values = [
        {"ex_ante": 0.8, "ex_post": 0.2, "difference": -0.6},
        {"ex_ante": 0.2, "ex_post": 0.8, "difference": 0.6},
    ]
    for ii, case in enumerate(normalized_values):
        normalized_value = normalized_values[ii]
        expected_value = expected_values[ii]

        for k in normalized_value:
            assert round(normalized_value[k], 3) == round(expected_value[k], 3)


def test_all_properties(NegativeIndicator):

    expected_values = [
        ("type", "negative"),
        ("ex_ante", 1),
        ("ex_post", 4),
        ("name", "dummy name"),
        ("unit", "dummy unit"),
    ]

    for parameter, expected_value in expected_values:
        assert expected_value == getattr(NegativeIndicator, parameter)

    assert repr(NegativeIndicator) == "Indicator:dummy name"
