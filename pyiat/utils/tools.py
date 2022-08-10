from math import ceil
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


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


def evaluation_guide(item) -> pd.DataFrame:

    """returns a data frame for the weighting excel guide

    Returns
    -------
    pd.DataFrame
        weighting guide
    """

    if item[-1] == "s":
        item == item[:-1]

    scores = [
        [f"{item} A is extremely more important than {item} B", "5"],
        [f"{item} A is highly more important than {item} B", "4"],
        [f"{item} A is more important than {item} B", "3"],
        [f"{item} A is slightly more important than {item} B", "2"],
        [f"{item}s A and B have the same importance", "1"],
        [f"{item} A is slightly less important than {item} B", "1/2"],
        [f"{item} A is less important than {item} B", "1/3"],
        [f"{item} A is highly less important than {item} B", "1/4"],
        [f"{item} A is extremely less important than {item} B", "1/5"],
    ]

    return pd.DataFrame(
        data = scores,columns = ["Assigned Score","Meaning (example Capital A vs. Capital B)"]
        )


def generate_plot_grid(size:int,size_identifier:Tuple) -> Tuple:
    """returns a dict for subplot griding

    Parameters
    ----------
    size : int
        number of sub-figures
    size_identifier : Tuple
        defines the main size identifier and the size.
        example:
            1. size_identifer = ("rows",2) -> fixes the number of rows to 2 and calculates the number of cols
            2. size_identifer = ("cols",2) -> fixes the number of cols to 2 and calculates the number of rows

    Returns
    -------
    Tuple
        includes the number rows,cols and iterator.
        (
            rows -> int, number of rows,
            cols -> int, number of cols,
            iterator -> List[Tuple], a list of positions of the figures as tuples of size of 2.
        )
    """

    if size_identifier[0] == "rows":
        rows = size_identifier[1]
        cols = ceil(size/rows)

    else:
        cols = size_identifier[1]
        rows = ceil(size/cols)


    iterator = [(row+1,col+1) for row in range(rows) for col in range(cols)]

    return rows,cols,iterator