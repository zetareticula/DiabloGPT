"""Compatibility layer for mumford_switch using PyMC3."""
from pymc3 import *
from pymc3.distributions import *

# Re-export commonly used components
__all__ = [
    'Model', 'Normal', 'Categorical', 'Uniform', 'DiscreteUniform',
    'Dirichlet', 'Beta', 'Bernoulli', 'Poisson', 'Exponential'
]
