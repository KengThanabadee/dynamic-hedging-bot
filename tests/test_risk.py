import pytest
import numpy as np
from hedging import var_cvar

def test_var_cvar():
    pnl = np.array([-3, -2, -1, 0, 1])
    var, cvar = var_cvar(pnl, confidence=0.95)
    assert var == 2.8
    assert cvar == 3.0

def test_var_cvar_empty_array():
    with pytest.raises(ValueError):
        var_cvar(np.array([]))

def test_var_cvar_invalid_confidence():
    with pytest.raises(ValueError):
        var_cvar(np.array([-1, 0, 1]), confidence=1.5)