import pandas as pd
from collections import namedtuple
from pyiat.core.impact import Indicator, Impact, Capital, Dimension


def excel_parser(filepath, sheet_name=0, impact_name="unknows"):

    data = pd.read_excel(filepath, sheet_name=sheet_name, index_col=[0, 1, 2], header=0)

    capitals = {i: {} for i in data.index.unique(0)}
    dimensions = {i: {} for i in data.index.unique(1)}
    indicators = {i: {} for i in data.index.unique(2)}

    _capitals = []
    for cc in capitals:
        _dimensions = []
        for dd in dimensions:
            _indicators = []
            for ii in indicators:
                series = data.loc[(cc, dd, ii), :]
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
