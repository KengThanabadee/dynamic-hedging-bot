import numpy as np
from hedging import PriceSimulator

def test_simulate_shape():
    sim = PriceSimulator(S0=100, mu=0.1, sigma=0.2, T=1, n=10, m=3, model=None)
    S = sim.simulate(seed=42)
    assert S.shape == (3, 10)

def test_seed_reproducibility():
    sim1 = PriceSimulator(S0=100, mu=0.1, sigma=0.2, T=1, n=10, m=3, model=None)
    S1 = sim1.simulate(seed=42)
    sim2 = PriceSimulator(S0=100, mu=0.1, sigma=0.2, T=1, n=10, m=3, model=None)
    S2 = sim2.simulate(seed=42)
    assert np.array_equal(S1, S2)