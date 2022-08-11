import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from pyiat.utils.tools import get_combination, generate_plot_grid, geometric_mean,evaluation_guide
import pandas as pd
import pandas.testing as pdt


def test_get_combination():

    inputs = ["A1", "A2", "A3"]
    expected_output = [("A1", "A2"), ("A1", "A3"), ("A2", "A3")]
    output = get_combination(inputs)

    assert expected_output == output


def test_generate_plot_grid():

    assert (
        2,
        3,
        [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
    ) == generate_plot_grid(6, ("rows", 2))
    assert (
        2,
        3,
        [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)],
    ) == generate_plot_grid(6, ("cols", 3))
    assert (2, 2, [(1, 1), (1, 2), (2, 1), (2, 2)]) == generate_plot_grid(
        3, ("rows", 2)
    )


def test_geometric_mean():

    geo_mean = pow(1 * 2 * 3, 1 / 3)
    inputs = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
    expected_output = pd.Series(data=geo_mean, index=inputs.index, dtype=float)
    output = geometric_mean(inputs)
    pdt.assert_series_equal(output, expected_output)


def test_evaluation_guide():

    pdt.assert_frame_equal(
        evaluation_guide("Tests"),evaluation_guide("Tests")
    )
