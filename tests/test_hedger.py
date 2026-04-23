import pytest
import numpy as np
from hedging import delta_hedge_pnl, HedgingBot

def test_hedgingbot_basic():
    bot = HedgingBot(cash=1000)
    bot.hedge(delta_t=0.5, S=100)
    assert bot.position == 0.5
    assert bot.cash == 1000 - 0.5 * 100

def test_hedgingbot_portfolio_value():
    bot = HedgingBot(cash=500)
    bot.hedge(delta_t=1.0, S=100)
    assert bot.portfolio_values(S=110) == 1.0 * 110 + 400

def test_delta_hedge_pnl_shape_mismatch():
    paths = np.ones((3, 10))
    all_deltas = np.ones((3, 9))
    with pytest.raises(ValueError):
        delta_hedge_pnl(paths, all_deltas, premium=5, r=0.0, T=1, t=np.linspace(0, 1, 10), fee_rate=0.001, K=100)

def test_delta_hedge_pnl_negative_fee():
    paths = np.ones((3, 10))
    all_deltas = np.ones((3, 10))
    with pytest.raises(ValueError):
        delta_hedge_pnl(paths, all_deltas, premium=5, r=0.0, T=1, t=np.linspace(0, 1, 10), fee_rate=-0.001, K=100)

def test_delta_hedge_pnl_invalid_option_type():
    paths = np.ones((3, 10))
    all_deltas = np.ones((3, 10))
    with pytest.raises(ValueError):
        delta_hedge_pnl(paths, all_deltas, premium=5, r=0.0, T=1, t=np.linspace(0, 1, 10), fee_rate=0.001, K=100, option_type="future")
