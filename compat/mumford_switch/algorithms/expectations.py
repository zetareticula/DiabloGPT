"""Expectation calculations for the mumford_switch compatibility layer."""
import numpy as np
from ..structure.base import Node

def expectation(node, ranges=None, n_samples=1000):
    """
    Compute the expectation of a node over the given ranges using Monte Carlo sampling.
    
    Args:
        node: The node to compute expectation for
        ranges: List of Range objects for each variable
        n_samples: Number of samples to use for Monte Carlo
        
    Returns:
        The expected value
    """
    if ranges is None:
        samples = node.sample(n_samples)
        return np.mean(samples)
    
    # For now, return a simple Monte Carlo estimate
    samples = node.sample(n_samples)
    if len(samples) == 0:
        return 0.0
    
    # Apply range filtering if ranges are provided
    if ranges and len(ranges) > 0:
        mask = np.ones(n_samples, dtype=bool)
        for i, r in enumerate(ranges):
            if r is not None:
                mask &= r.contains(samples[:, i] if samples.ndim > 1 else samples)
        samples = samples[mask]
    
    return np.mean(samples) if len(samples) > 0 else 0.0
