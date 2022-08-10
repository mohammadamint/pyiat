import pandas as pd
from collections import namedtuple
from pyiat.core.impact import Indicator, Impact, Capital, Dimension
from typing import Union

def excel_parser(filepath:str, sheet_name:Union[str,int]=0, impact_name:str="unknows") -> namedtuple:
    """reads the impact evaluation project from an excel file

    Parameters
    ----------
    filepath : str
        the path of excel file
    sheet_name : Union[str,int], optional
        name or index of the sheet with the information, by default 0
    impact_name : str, optional
        the name of impact evaluation project, by default "unknows"

    Returns
    -------
    namedtuple
        includes following properties with indeces:
            [0],indicators : a dict of all indicator objects
            [1],dimensions : a dict of all dimension objects
            [2],capitals : a dict of all capital objects
            [3],impact : the impact object
    """
    data = pd.read_excel(filepath, sheet_name=sheet_name, index_col=[0, 1, 2], header=0)

    capitals = {i: {} for i in data.index.unique(0)}
    dimensions = {i: {} for i in data.index.unique(1)}
    indicators = {i: {} for i in data.index.unique(2)}

    _capitals = []
    for cc in capitals:
        _dimensions = []
        capital_dimensions = data.loc[cc]
        for dd in capital_dimensions.index.unique(0):
            _indicators = []
            dimension_indicator = data.loc[cc].loc[dd]
            for ii in dimension_indicator.index.unique():
                series = data.loc[(cc,dd, ii), :]
                indicator = Indicator(
                    name=ii,
                    type=series.type,
                    unit=series.unit,
                    ex_ante=series.ex_ante,
                    ex_post=series.ex_post,
                    description=series.description,
                )

                indicators[ii] = indicator
                _indicators.append(indicator)

            dimension = Dimension(name=dd, indicators=_indicators)

            dimensions[dd] = dimension
            _dimensions.append(dimension)

        capital = Capital(name=cc, dimensions=_dimensions)
        capitals[cc] = capital
        _capitals.append(capital)

    impact = Impact(name=impact_name, capitals=_capitals)

    output = namedtuple("impact", ["indicators", "dimensions", "capitals", "impact"])

    return output(indicators, dimensions, capitals, impact)
