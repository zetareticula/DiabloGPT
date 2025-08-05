"""Base classes for the mumford_switch compatibility layer."""
from abc import ABC, abstractmethod
import numpy as np

class Node(ABC):
    """Base class for all nodes in the SPN (Sum-Product Network)."""
    
    @abstractmethod
    def likelihood(self, data):
        """Compute the likelihood of the given data."""
        pass
    
    @abstractmethod
    def sample(self, n_samples=1):
        """Generate samples from the distribution."""
        pass


class Sum(Node):
    """Sum node in the SPN."""
    
    def __init__(self, children=None, weights=None):
        self.children = children or []
        self.weights = weights or np.ones(len(children)) / len(children)
    
    def likelihood(self, data):
        if not self.children:
            return np.ones(len(data))
        
        likelihoods = np.array([child.likelihood(data) for child in self.children])
        return np.dot(self.weights, likelihoods)
    
    def sample(self, n_samples=1):
        if not self.children:
            return np.array([])
            
        # Sample based on weights
        idx = np.random.choice(len(self.children), size=n_samples, p=self.weights)
        samples = []
        for i, child in enumerate(self.children):
            count = np.sum(idx == i)
            if count > 0:
                samples.append(child.sample(count))
        
        return np.concatenate(samples)


class Product(Node):
    """Product node in the SPN."""
    
    def __init__(self, children=None):
        self.children = children or []
    
    def likelihood(self, data):
        if not self.children:
            return np.ones(len(data))
            
        likelihood = np.ones(len(data))
        for child in self.children:
            likelihood *= child.likelihood(data)
        return likelihood
    
    def sample(self, n_samples=1):
        if not self.children:
            return np.array([])
            
        samples = [child.sample(n_samples) for child in self.children]
        return np.column_stack(samples)
