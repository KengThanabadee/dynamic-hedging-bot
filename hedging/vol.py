import numpy as np

def realized_vol(df, window, annualization_factor): # log return vol
    if window >= len(df):
        raise ValueError(f"window ({window}) must be less than len(df) ({len(df)})")
    log_returns = np.log(df["close"] / df["close"].shift())
    result = log_returns.rolling(window).std() * np.sqrt(annualization_factor)
    return result.rename("realized_vol")