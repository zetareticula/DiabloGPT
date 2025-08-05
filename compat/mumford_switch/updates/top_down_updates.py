"""Top-down updates for the mumford_switch compatibility layer."""
import numpy as np
from sklearn.cluster import KMeans
from ...structure import Sum, Product, Categorical, IdentityNumericLeaf

def cluster_center_update_dataset(node, data, n_clusters=5):
    """
    Update the SPN structure using k-means clustering on the data.
    
    Args:
        node: Root node of the SPN
        data: Input data for clustering
        n_clusters: Number of clusters to create
        
    Returns:
        The updated SPN
    """
    if data.size == 0:
        return node
        
    data = np.asarray(data)
    
    if isinstance(node, Sum):
        # For sum nodes, cluster the data and update weights
        if data.shape[0] < n_clusters:
            # Not enough data for clustering
            return node
            
        # Perform k-means clustering
        kmeans = KMeans(n_clusters=min(n_clusters, data.shape[0]))
        labels = kmeans.fit_predict(data)
        
        # Update weights based on cluster sizes
        unique_labels, counts = np.unique(labels, return_counts=True)
        node.weights = np.zeros(len(node.children))
        
        # Distribute weights based on cluster sizes
        for label, count in zip(unique_labels, counts):
            if label < len(node.weights):
                node.weights[label] = count / len(data)
        
        # Normalize weights
        node.weights = node.weights / np.sum(node.weights)
        
        # Recursively update children with their corresponding clusters
        for i, child in enumerate(node.children):
            cluster_data = data[labels == i]
            if len(cluster_data) > 0:
                cluster_center_update_dataset(child, cluster_data, n_clusters)
                
    elif isinstance(node, Product):
        # For product nodes, update each child with the full data
        for child in node.children:
            cluster_center_update_dataset(child, data, n_clusters)
            
    elif isinstance(node, IdentityNumericLeaf):
        # Update leaf node parameters
        if len(data) > 0:
            node.mean = np.mean(data)
            node.std = max(np.std(data), 1e-10)
            
    elif isinstance(node, Categorical):
        # Update categorical probabilities
        if len(data) > 0:
            unique, counts = np.unique(data, return_counts=True)
            probs = np.zeros_like(node.probs)
            for val, count in zip(unique, counts):
                if val < len(probs):
                    probs[val] = count
            probs = probs / np.sum(probs)
            node.probs = probs
    
    return node
