# Dynamic Hedging Bot

A delta/gamma hedging bot for BTC options — built from simulation to live trading, one component at a time.

## How It Works

Options expose sellers to directional price risk. This project implements dynamic hedging strategies to neutralize that risk:

- **Delta hedging** — continuously rebalances a stock position to offset the option's delta, keeping the portfolio direction-neutral
- **Gamma hedging** — adds a second option position to offset gamma exposure, reducing P&L sensitivity to large price moves

Greeks are computed using the Black-Scholes model. Performance is measured using CVaR (Conditional Value at Risk) at the 95% confidence level — the expected loss in the worst 5% of outcomes.

The project progresses from Monte Carlo simulation (validating mechanics under GBM) to backtesting on real BTC price data (testing under actual market conditions).

## Project Structure

```
hedging/
    simulator.py    — PriceSimulator (GBM)
    pricing.py      — GreeksEngine (BS delta/gamma/vega/price)
    hedger.py       — HedgingBot, delta_hedge_pnl
    risk.py         — var_cvar (VaR, CVaR)
    vol.py          — realized_vol (rolling realized volatility)
data_loader.py      — DataLoader (Binance API, realized vol)
simulation.ipynb    — Monte Carlo simulation: delta + gamma hedging
backtest.ipynb      — Backtest on real BTC data (in progress)
```

## Installation

```bash
pip install numpy scipy matplotlib requests
```

## Usage

- **simulation.ipynb** — runs 10,000 Monte Carlo paths, analyzes delta and gamma hedging under GBM
- **backtest.ipynb** — fetches real BTC/USDT data from Binance, backtests delta hedging on historical prices
