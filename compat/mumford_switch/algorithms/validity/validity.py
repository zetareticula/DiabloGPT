"""Validity checks for the mumford_switch compatibility layer."""
from ...structure.base import Node, Sum, Product

class Prune:
    """Class for pruning invalid nodes from the SPN."""
    
    @staticmethod
    def apply(node):
        """
        Prune invalid nodes from the SPN.
        
        Args:
            node: Root node of the SPN to prune
            
        Returns:
            The pruned SPN
        """
        if not is_valid(node):
            return None
        
        if isinstance(node, Sum):
            # Prune invalid children and update weights
            valid_children = []
            valid_weights = []
            
            for child, weight in zip(node.children, node.weights):
                pruned_child = Prune.apply(child)
                if pruned_child is not None:
                    valid_children.append(pruned_child)
                    valid_weights.append(weight)
            
            if not valid_children:
                return None
                
            # Renormalize weights
            total_weight = sum(valid_weights)
            if total_weight > 0:
                valid_weights = [w/total_weight for w in valid_weights]
            else:
                valid_weights = [1.0/len(valid_children)] * len(valid_children)
                
            node.children = valid_children
            node.weights = valid_weights
            
        elif isinstance(node, Product):
            # Prune invalid children
            valid_children = []
            for child in node.children:
                pruned_child = Prune.apply(child)
                if pruned_child is not None:
                    valid_children.append(pruned_child)
            
            if not valid_children:
                return None
                
            node.children = valid_children
            
        return node


def is_valid(node):
    """
    Check if a node is valid.
    
    Args:
        node: Node to check
        
    Returns:
        True if the node is valid, False otherwise
    """
    if node is None:
        return False
        
    if isinstance(node, Sum):
        if not node.children or not node.weights:
            return False
        if len(node.children) != len(node.weights):
            return False
        if not all(is_valid(child) for child in node.children):
            return False
            
    elif isinstance(node, Product):
        if not node.children:
            return False
        if not all(is_valid(child) for child in node.children):
            return False
            
    return True
