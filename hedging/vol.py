import numpy as np

def realized_vol(df, window, annualization_factor=252*24): # log return vol
    log_returns = np.log(df["close"] / df["close"].shift())
    result = log_returns.rolling(window).std() * np.sqrt(annualization_factor)
    return result.rename("realized_vol")