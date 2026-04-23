import numpy as np

def var_cvar(pnl, confidence=0.95):
    if len(pnl) == 0:
        raise ValueError("pnl array is empty")
    if not (0 < confidence < 1):                         
        raise ValueError(f"confidence must be in (0, 1), got {confidence}")
    VaR = -np.percentile(pnl, 100 * (1 - confidence))
    CVaR = -pnl[pnl <= -VaR].mean()
    return VaR, CVaR