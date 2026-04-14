# Dynamic Hedging Bot

A dynamic hedging bot that neutralizes price directional risk on options by hedging delta and gamma, designed for live deployment on BTC crypto options markets.

## How It Works

The project is built around three core components:

- **PriceSimulator** — simulates asset price paths using Geometric Brownian Motion (GBM)
- **GreeksEngine** — computes Black-Scholes option price, delta, gamma, and vega
- **HedgingBot** — adjusts hedge position and tracks portfolio value (used for live trading)

The main simulation in `experiment.ipynb` runs 10,000 Monte Carlo paths to analyze hedging performance, including transaction costs and CVaR-based risk analysis.

## Installation

```bash
pip install numpy scipy matplotlib
```

## Usage

Open `experiment.ipynb` in Jupyter and run all cells. The notebook simulates a delta hedging strategy on a European call option and outputs:

- Monte Carlo asset price paths with confidence intervals
- Distribution of final P&L
- CVaR/VaR risk metrics
- CVaR-adjusted option premium
- Optimal rebalancing frequency analysis

## Current Status

This is a simulation prototype. Live exchange API integration is planned as the next step.
