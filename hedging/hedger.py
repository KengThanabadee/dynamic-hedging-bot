import numpy as np

class HedgingBot:
    def __init__(self, cash):
        self.cash = cash
        self.position = 0

    def hedge(self, delta_t, S):
        delta_need_to_adjust = delta_t - self.position
        self.cash += -delta_need_to_adjust * S
        self.position = delta_t

    def portfolio_values(self, S):
        return self.position * S + self.cash
    
def delta_hedge_pnl(paths, all_deltas, premium, r, T, t, fee_rate, K, option_type="call"):
    if paths.shape != all_deltas.shape:
        raise ValueError(f"paths and all_deltas must have the same shape, got {paths.shape} and {all_deltas.shape}")
    if fee_rate < 0:
        raise ValueError(f"fee_rate must be >= 0, got {fee_rate}")
    delta_diff = all_deltas[:, 1:] - all_deltas[:, :-1]
    # prepend initial position change (from 0 to delta_0)
    initial_diff = all_deltas[:, 0:1] # shape (m, 1)
    delta_diff = np.hstack([initial_diff, delta_diff]) # shape (m, n)
    cash_changes = -delta_diff * paths
    cost = fee_rate * np.abs(delta_diff) * paths
    cash_changes -= cost
    time_remaining = T - t
    total_cash = premium * np.exp(r * T) + (cash_changes * np.exp(r * time_remaining)).sum(axis=1)

    if option_type.lower() not in ("call", "put"):           
      raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")
    payoff = np.maximum(paths[:, -1] - K, 0) if option_type.lower() == "call" else np.maximum(K - paths[:, -1], 0)

    fee_last = fee_rate * np.abs(all_deltas[:, -1]) * paths[:, -1]
    final_PnL = total_cash + all_deltas[:, -1] * paths[:, -1] - fee_last - payoff
    return final_PnL