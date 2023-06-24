import numpy as np
import pandas as pd
import pytest
from covsirphy import Evaluator, UnExpectedValueError, NAFoundError


@pytest.mark.parametrize("metric", ["ME", "MAE", "MSE", "MSLE", "MAPE", "RMSE", "RMSLE", "R2"])
def test_score_series(metric):
    assert metric in Evaluator.metrics()
    true = pd.Series([5, 10, 8, 6])
    pred = pd.Series([8, 12, 6, 5])
    evaluator = Evaluator(true, pred, on=None)
    assert isinstance(evaluator.score(metric=metric), float)
    assert isinstance(Evaluator.smaller_is_better(metric=metric), bool)
    best_tuple = Evaluator.best_one({"A": 1.0, "B": 1.5, "C": 2.0}, metric=metric)
    if metric == "R2":
        assert best_tuple == ("C", 2.0)
    else:
        assert best_tuple == ("A", 1.0)


@pytest.mark.parametrize("metric", ["ME", "MAE", "MSE", "MSLE", "MAPE", "RMSE", "RMSLE", "R2"])
@pytest.mark.parametrize("how", ["all", "inner"])
@pytest.mark.parametrize("on", [None, "join_on"])
def test_score_dataframe(metric, how, on):
    true = pd.DataFrame(
        {
            "join_on": [0, 1, 2, 3, 4, 5],
            "value": [20, 40, 30, 50, 90, 10]
        }
    )
    pred = pd.DataFrame(
        {
            "join_on": [0, 2, 3, 4, 6, 7],
            "value": [20, 40, 30, 50, 110, 55]
        }
    )
    evaluator = Evaluator(true, pred, how=how, on=on)
    assert isinstance(evaluator.score(metric=metric), float)


def test_error():
    with pytest.raises(NAFoundError):
        Evaluator([1, 2, 3, np.nan], [2, 5, 7, 10])
    true = pd.Series([5, 10, 8, 6])
    pred = pd.Series([8, 12, 6, 5])
    evaluator = Evaluator(true, pred, on=None)
    with pytest.raises(UnExpectedValueError):
        evaluator.score(metric="Unknown")
    with pytest.raises(UnExpectedValueError):
        evaluator.smaller_is_better(metric="Unknown")
