import pytest
import numpy as np
from hedging import GreeksEngine

def test_invalid_option_type():
    with pytest.raises(ValueError):
        GreeksEngine(option_type="future", K=100, r=0.01)

def test_invalid_strike():
    with pytest.raises(ValueError):
        GreeksEngine(option_type="call", K=-100, r=0.01)

def test_call_delta_atm():
    engine = GreeksEngine(option_type="call", K=100, r=0.0)
    delta = engine.delta_compute(S=100, sigma=0.2, T=1, t=0)
    assert 0.5 < delta < 0.6

def test_put_delta_atm():
    engine = GreeksEngine(option_type="put", K=100, r=0.0)
    delta = engine.delta_compute(S=100, sigma=0.2, T=1, t=0)
    assert -0.6 < delta < -0.4

def test_call_delta_at_expiry_itm():
    engine = GreeksEngine(option_type="call", K=100, r=0.0)
    delta = engine.delta_compute(S=110, sigma=0.2, T=1, t=1)
    assert delta == 1

def test_invalid_S():
    engine = GreeksEngine(option_type="call", K=100, r=0.0)
    with pytest.raises(ValueError):
        engine.delta_compute(S=-10, sigma=0.2, T=1, t=0)
