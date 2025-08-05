"""Range implementations for the mumford_switch compatibility layer."""
import numpy as np

class Range:
    """Base class for range types."""
    
    def __init__(self, values):
        self.values = np.array(values)
    
    def contains(self, x):
        """Check if x is within this range."""
        raise NotImplementedError


class NominalRange(Range):
    """Range for nominal/categorical values."""
    
    def contains(self, x):
        return np.isin(x, self.values)
    
    def __repr__(self):
        return f"NominalRange({self.values.tolist()})"


class NumericRange(Range):
    """Range for numeric values."""
    
    def __init__(self, min_val, max_val):
        super().__init__([min_val, max_val])
        self.min_val = min_val
        self.max_val = max_val
    
    def contains(self, x):
        return (x >= self.min_val) & (x <= self.max_val)
    
    def __repr__(self):
        return f"NumericRange({self.min_val}, {self.max_val})"
