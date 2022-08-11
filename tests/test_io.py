import os
import sys

pyiat_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.append(pyiat_path)

mock_path = f'{pyiat_path}/tests/mocks'

from pyiat.utils.io import excel_parser
import pandas as pd
import pandas.testing as pdt
from pyiat.core.impact import Capital,Dimension,Indicator,Impact


def test_excel_parser():

    output = excel_parser(f'{mock_path}/mock_01.xlsx',impact_name="dummy")

    assert isinstance(output,tuple)

    impact = output.impact
    capitals = output.capitals
    dimensions = output.dimensions
    indicators = output.indicators

    assert repr(impact) == "Impact:dummy"

    assert [*capitals]   == ["Cap.1","Cap.2"]
    assert [*dimensions] == ["Dim.1","Dim.2"]
    assert [*indicators] == ["Ind.1","Ind.2"]

    assert isinstance(impact,Impact)
    assert all([isinstance(obj,Indicator) for obj in indicators.values()])
    assert all([isinstance(obj,Dimension) for obj in dimensions.values()])
    assert all([isinstance(obj,Capital) for obj in capitals.values()])





