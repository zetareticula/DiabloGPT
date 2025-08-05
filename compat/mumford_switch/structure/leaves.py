"""Leaf node implementations for the mumford_switch compatibility layer."""
import numpy as np
from scipy import stats
from .base import Node

class IdentityNumericLeaf(Node):
    """Leaf node for numeric data with identity transformation."""
    
    def __init__(self, mean=0.0, std=1.0):
        self.mean = mean
        self.std = max(std, 1e-10)  # Avoid division by zero
    
    def likelihood(self, data):
        return stats.norm.pdf(data, loc=self.mean, scale=self.std)
    
    def sample(self, n_samples=1):
        return np.random.normal(loc=self.mean, scale=self.std, size=n_samples)


class Categorical(Node):
    """Leaf node for categorical data."""
    
    def __init__(self, probs=None, n_categories=2):
        if probs is None:
            probs = np.ones(n_categories) / n_categories
        self.probs = probs / np.sum(probs)  # Ensure normalization
        self.n_categories = len(probs)
    
    def likelihood(self, data):
        # For each data point, return the probability of its category
        likelihoods = np.zeros(len(data))
        for i, prob in enumerate(self.probs):
            likelihoods[data == i] = prob
        return likelihoods
    
    def sample(self, n_samples=1):
        return np.random.choice(self.n_categories, size=n_samples, p=self.probs)


def categorical_likelihood_range(categories, ranges, data):
    """
    Compute the likelihood of data falling within the given ranges for each category.
    
    Args:
        categories: List of category values
        ranges: List of (min, max) tuples for each category
        data: Input data
        
    Returns:
        Likelihood values for each data point
    """
    likelihoods = np.zeros(len(data))
    for cat, (min_val, max_val) in zip(categories, ranges):
        mask = (data >= min_val) & (data <= max_val)
        likelihoods[mask] = 1.0 / (max_val - min_val + 1e-10)
    return likelihoods


def identity_distinct_ranges(data, n_bins=10):
    """
    Compute distinct ranges for numeric data.
    
    Args:
        data: Input data
        n_bins: Number of bins to create
        
    Returns:
        List of (min, max) tuples for each bin
    """
    if len(data) == 0:
        return []
    
    min_val, max_val = np.min(data), np.max(data)
    if min_val == max_val:
        return [(min_val, max_val)]
    
    bin_edges = np.linspace(min_val, max_val, n_bins + 1)
    ranges = list(zip(bin_edges[:-1], bin_edges[1:]))
    return ranges
