import numpy as np

class PriceSimulator:
    def __init__(self, S0, mu, sigma, T, n, m, model):
        self.S0 = S0
        self.mu = mu
        self.sigma = sigma
        self.time = T
        self.n = n # Number of data points
        self.paths = m
        self.model = model

    def simulate(self, seed=None):
        rng = np.random.default_rng(seed)
        dt = self.time / (self.n - 1)
        W0 = np.zeros((self.paths, 1))
        t = np.linspace(0, self.time, self.n)
        w = np.cumsum(rng.normal(0, np.sqrt(dt), size=(self.paths, self.n - 1)), axis=1)
        W = np.hstack([W0, w]) # cumulative sum of the Brownian increments
        # GBM closed form solution S_t = S0 * exp((mu - 0.5 * sigma^2) * t + sigma * Wt)
        S = self.S0 * np.exp((self.mu - 0.5 * self.sigma ** 2) * t + self.sigma * W)
        return S