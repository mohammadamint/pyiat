import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pytest
import pandas as pd
import pandas.testing as pdt
from pyiat.core.impact import Dimension, Indicator
from pyiat.error_log.errors import InvalidInput
from pyiat.utils.constants import EFFECT


def load_dummy_indicators():
    ind1 = Indicator(
        name="dummy ind.1", type="positive", unit="dummy unit", ex_ante=1, ex_post=4
    )

    ind2 = ind1.copy()
    ind2.type = "negative"
    ind2.name = "dummy ind.2"

    return [ind1, ind2]

def load_dummy_weight():
    return pd.Series(
        index=pd.MultiIndex.from_tuples(
            [("dummy ind.1", "dummy ind.2")],
            names=["Reference Impact", "Compared Impact"],
        ),
        dtype=float
    )

@pytest.fixture
def DummyDimension():

    return Dimension(name="dummy dimension", indicators=load_dummy_indicators())


def test_id_repr(DummyDimension):
    assert DummyDimension.id == "Dimension"
    assert repr(DummyDimension) == "Dimension:dummy dimension"


def test_len(DummyDimension):
    assert len(DummyDimension) == 2


def test_pairwised_items(DummyDimension):
    assert DummyDimension.pairwised_items == ["dummy ind.1", "dummy ind.2"]


def test_get_weight_matrix(DummyDimension):

    expected_output = load_dummy_weight()

    output = DummyDimension.get_weight_matrix()

    pdt.assert_series_equal(
        expected_output,output
    )


def test_set_weight_matrix(DummyDimension):
    # adding a new indicator
    ind1,_ = load_dummy_indicators()

    ind3 = ind1.copy()
    ind3.name = "dummy ind.3"

    DummyDimension.set_indicator([ind3])

    # at the begining there is no weight_matrix
    assert not hasattr(DummyDimension,"weight_matrix")



    weight_matrix = DummyDimension.get_weight_matrix()


    weight_matrix.loc[("dummy ind.1","dummy ind.2")] = 2
    weight_matrix.loc[("dummy ind.1","dummy ind.3")] = 4
    weight_matrix.loc[("dummy ind.2","dummy ind.3")] = 5

    expected_output = pd.DataFrame(
     data = [
        [1,2,4],
        [0.5,1,5],
        [0.25,0.2,1],
        ],
    index = ["dummy ind.1","dummy ind.2","dummy ind.3"],
    columns = ["dummy ind.1","dummy ind.2","dummy ind.3"],
    )

    DummyDimension.set_weight_matrix(weight_matrix)

    print(DummyDimension.weight_matrix)
    pdt.assert_frame_equal(
        expected_output , DummyDimension.weight_matrix,check_dtype=False
    )



