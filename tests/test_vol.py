import pytest
import numpy as np
import pandas as pd
from hedging import realized_vol

def test_realized_vol_shape():
    df = pd.DataFrame({"close": [100, 101, 102, 103, 104, 105]})
    result = realized_vol(df, window=3, annualization_factor=24*365)
    assert result.name == "realized_vol"
    assert len(result) == len(df)

def test_realized_vol_flat_prices():
    df = pd.DataFrame({"close": [100.0] * 10})
    result = realized_vol(df, window=3, annualization_factor=24*365)
    assert result.dropna().eq(0).all()

def test_realized_vol_window_too_large():
    df = pd.DataFrame({"close": [100, 101, 102]})
    with pytest.raises(ValueError):
        realized_vol(df, window=3, annualization_factor=24*365)
