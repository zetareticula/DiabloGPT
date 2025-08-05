"""Main module for the mumford_switch compatibility layer."""
import numpy as np
from .structure import Sum, Product, Node, IdentityNumericLeaf, Categorical
from .algorithms.ranges import NominalRange, NumericRange
from .algorithms.expectations import expectation

def mumford_switch(node, data, n_iter=100, learning_rate=0.01):
    """
    A simplified version of the mumford switch algorithm.
    
    Args:
        node: The root node of the SPN
        data: Training data
        n_iter: Number of iterations
        learning_rate: Learning rate for updates
        
    Returns:
        The trained SPN
    """
    if not isinstance(node, Node):
        raise ValueError("node must be an instance of Node")
    
    # Convert data to numpy array if it isn't already
    data = np.asarray(data)
    
    # Simple training loop
    for _ in range(n_iter):
        # Forward pass
        likelihood = node.likelihood(data)
        
        # Backward pass (simplified)
        if isinstance(node, Sum):
            # Update weights using gradient ascent
            gradients = np.zeros(len(node.children))
            for i, child in enumerate(node.children):
                child_likelihood = child.likelihood(data)
                gradients[i] = np.mean(child_likelihood / (likelihood + 1e-10))
            
            # Update weights
            node.weights += learning_rate * gradients
            node.weights = np.maximum(node.weights, 0)  # Ensure non-negative
            node.weights /= np.sum(node.weights)  # Normalize
            
            # Recursively update children
            for child in node.children:
                mumford_switch(child, data, n_iter=1, learning_rate=learning_rate)
                
        elif isinstance(node, Product):
            # For product nodes, just update children
            for child in node.children:
                mumford_switch(child, data, n_iter=1, learning_rate=learning_rate)
                
    return node
