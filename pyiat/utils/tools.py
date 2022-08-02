import pandas as pd
import numpy as np
from typing import List


def get_combination(array: List) -> List:
    """returns the dual combination of list items

    Parameters
    ----------
    array : List
        original items

    Returns
    -------
    List
        dual combination of items
    """
    combination = []
    for a in array:
        for b in array:
            if a != b and (a, b) not in combination and (b, a) not in combination:
                combination.append((a, b))

    return combination


def reverse_series(series: pd.Series) -> pd.Series:
    """returns the a series similar to the input with reversed values for counter values

    Parameters
    ----------
    series : pd.Series
        the original series

    Returns
    -------
    pd.Series
        the reversed counter items
    """
    output = pd.Series(dtype=series.dtype)

    for row, val in series.iteritems():
        output.loc[row[1], row[0]] = 1 / val


def geometric_mean(frame: pd.DataFrame) -> pd.Series:
    """returns the geometric mean

    Parameters
    ----------
    frame : pd.DataFrame
        the original frame

    Returns
    -------
    pd.Series
        geometric mean of rows
    """
    geo_mean = pd.Series(index=frame.index, dtype=float)

    for row, vals in frame.iterrows():
        geo_mean.loc[row] = np.exp(np.log(vals).mean())

    return geo_mean
