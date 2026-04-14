import numpy as np
import pandas as pd
from scipy.stats import norm
class PriceSimulator:
    def __init__(self, S0, mu, sigma, T, n, m, model):
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.time = T
        self.n = n # Number of data points
        self.paths = m
        self.model = model

    def simulate(self):
        dt = self.time / (self.n - 1)
        W0 = np.zeros((self.paths, 1))
        t = np.linspace(0, self.time, self.n)
        w = np.cumsum(np.random.normal(0, np.sqrt(dt), size=(self.paths, self.n - 1)), axis=1)
        W = np.hstack([W0, w]) # cumulative sum of the Brownian increments
        # GBM closed form solution S_t = S0 * exp((mu - 0.5 * sigma^2) * t + sigma * Wt)
        S = self.S0 * np.exp((self.mu - 0.5 * self.sigma ** 2) * t + self.sigma * W)
        return S
    
class GreeksEngine:
    def __init__(self, option_type, K, r, sigma, T):
        if option_type.lower() not in ("call", "put"):
            raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")
        self.option_type = option_type.lower()
        self.K = K
        self.r = r
        self.sigma = sigma
        self.T = T

    def _compute_d1_d2(self, S, t):
        d1 = (np.log(S / self.K) + (self.r + 1 / 2 * self.sigma ** 2) * (self.T - t)) / (self.sigma * np.sqrt(self.T - t))
        d2 = d1 - (self.sigma * np.sqrt(self.T - t))
        return d1, d2

    def compute_all_deltas(self, S, t):
        d1, _ = self._compute_d1_d2(S[:, :-1], t[:-1])  # exclude last step because it's at expiry so delta at expiry will be computed separately
        if self.option_type == "call" :
            deltas = norm.cdf(d1)
            # compute expiry column and hstack
            delta_last = np.where(S[:, -1] > self.K, 1, np.where(S[:, -1] == self.K, 0.5, 0)).reshape(-1, 1)
            return np.hstack([deltas, delta_last])
        if self.option_type == "put":
            deltas = norm.cdf(d1) - 1
            # compute expiry column and hstack
            delta_last = np.where(S[:, -1] < self.K, -1, np.where(S[:, -1] == self.K, -0.5, 0)).reshape(-1, 1)
            return np.hstack([deltas, delta_last])

    def delta_compute(self, S, t):
        if self.option_type == "call" :
            if t >= self.T:
                return np.where(S > self.K, 1, np.where(S == self.K, 0.5, 0))
            else:
                d1, _ = self._compute_d1_d2(S, t)
                N_d1 = norm.cdf(d1)
                return N_d1
            
        if self.option_type == "put":
            if t >= self.T:
                return np.where(S < self.K, -1, np.where(S == self.K, -0.5, 0))
            else:
                d1, _ = self._compute_d1_d2(S, t)
                N_d1 = norm.cdf(d1)
                return N_d1 - 1
            
    def gamma_compute(self, S, t):
        if t >= self.T:
            return 0
        d1, _ = self._compute_d1_d2(S, t)
        gamma = norm.pdf(d1) / (S * self.sigma * np.sqrt(self.T - t))
        return gamma
    
    def vega_compute(self, S, t):
        if t >= self.T:
            return 0
        d1, _ = self._compute_d1_d2(S, t)
        vega = S * norm.pdf(d1) * np.sqrt(self.T - t)
        return vega
        
    def price(self, S, t):
        if t >= self.T:                                                          
          if self.option_type == "call" : 
              return np.maximum(S - self.K, 0)                                   
          if self.option_type == "put":
              return np.maximum(self.K - S, 0)  
          
        d1, d2 = self._compute_d1_d2(S, t)
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        discount = np.exp(-self.r * (self.T - t))
        C = S * N_d1 - self.K * discount * N_d2
        P = C + self.K * discount - S # put-call parity

        if self.option_type == "call" :
            return C
        if self.option_type == "put":
            return P
        
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