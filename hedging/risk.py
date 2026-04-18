import numpy as np

def var_cvar(pnl, confidence=0.95):
    VaR = -np.percentile(pnl, 100 * (1 - confidence))
    CVaR = -pnl[pnl <= -VaR].mean()
    return VaR, CVaR