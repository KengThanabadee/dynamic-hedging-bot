import numpy as np
from scipy.stats import norm

class GreeksEngine:
    def __init__(self, option_type, K, r):
        if option_type.lower() not in ("call", "put"):
            raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")
        self.option_type = option_type.lower()
        self.K = K
        self.r = r

    def _compute_d1_d2(self, S, sigma, T, t):
        tau = np.maximum(T - t, 1e-12)
        d1 = (np.log(S / self.K) + (self.r + 0.5 * sigma ** 2) * (tau)) / (sigma * np.sqrt(tau))
        d2 = d1 - (sigma * np.sqrt(tau))
        return d1, d2

    def compute_all_deltas(self, S, sigma, T, t):
        d1, _ = self._compute_d1_d2(S[:, :-1], sigma, T, t[:-1])  # exclude last step because it's at expiry so delta at expiry will be computed separately
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
        
    def compute_all_gammas(self, S, sigma, T, t):
        d1, _ = self._compute_d1_d2(S[:, :-1], sigma, T, t[:-1])
        gammas = norm.pdf(d1) / (S[:, :-1] * sigma * np.sqrt(T - t[:-1]))
        gamma_last = np.zeros((S.shape[0], 1))
        return np.hstack([gammas, gamma_last])

    def delta_compute(self, S, sigma, T, t):
        if self.option_type == "call" :
            if t >= T:
                return np.where(S > self.K, 1, np.where(S == self.K, 0.5, 0))
            else:
                d1, _ = self._compute_d1_d2(S, sigma, T, t)
                N_d1 = norm.cdf(d1)
                return N_d1
            
        if self.option_type == "put":
            if t >= T:
                return np.where(S < self.K, -1, np.where(S == self.K, -0.5, 0))
            else:
                d1, _ = self._compute_d1_d2(S, sigma, T, t)
                N_d1 = norm.cdf(d1)
                return N_d1 - 1
            
    def gamma_compute(self, S, sigma, T, t):
        if t >= T:
            return 0
        d1, _ = self._compute_d1_d2(S, sigma, T, t)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T - t))
        return gamma
    
    def vega_compute(self, S, sigma, T, t):
        if t >= T:
            return 0
        d1, _ = self._compute_d1_d2(S, sigma, T, t)
        vega = S * norm.pdf(d1) * np.sqrt(T - t)
        return vega
        
    def compute_all_prices(self, S, sigma, T, t):
        d1, d2 = self._compute_d1_d2(S[:, :-1], sigma, T, t[:-1])  # exclude last step because it's at expiry so price at expiry will be computed separately
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        discount = np.exp(-self.r * (T - t[:-1]))
        C = S[:, :-1] * N_d1 - self.K * discount * N_d2
        P = C + self.K * discount - S[:, :-1] # put-call parity
        
        C_last = np.maximum(S[:, -1] - self.K, 0).reshape(-1, 1)
        P_last = np.maximum(self.K - S[:, -1], 0).reshape(-1, 1)

        C = np.hstack([C, C_last])
        P = np.hstack([P, P_last])
        if self.option_type == "call" :
            return C
        if self.option_type == "put":
            return P
        
    def price(self, S, sigma, T, t):
        if t >= T:                                                          
          if self.option_type == "call" : 
              return np.maximum(S - self.K, 0)                                   
          if self.option_type == "put":
              return np.maximum(self.K - S, 0)  
          
        d1, d2 = self._compute_d1_d2(S, sigma, T, t)
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        discount = np.exp(-self.r * (T - t))
        C = S * N_d1 - self.K * discount * N_d2
        P = C + self.K * discount - S # put-call parity

        if self.option_type == "call" :
            return C
        if self.option_type == "put":
            return P