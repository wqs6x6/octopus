import numpy as np

def pagerank(adjacency_matrix, damping_factor=0.85, epsilon=1e-8, max_iterations=100):
    """
    Implement PageRank algorithm
    
    Parameters:
        adjacency_matrix: Adjacency matrix representing links between pages
        damping_factor: Damping factor (typically 0.85)
        epsilon: Convergence threshold
        max_iterations: Maximum number of iterations
    
    Returns:
        pagerank_scores: PageRank scores for each page
    """
    n = len(adjacency_matrix)
    
    # Convert adjacency matrix to probability transition matrix
    out_degrees = np.sum(adjacency_matrix, axis=1)
    transition_matrix = adjacency_matrix / out_degrees[:, np.newaxis]
    
    # Handle pages with zero out-degrees
    transition_matrix[np.isnan(transition_matrix)] = 1/n
    
    # Initialize PageRank scores
    pagerank_scores = np.ones(n) / n
    
    # Iteration calculation
    for _ in range(max_iterations):
        prev_scores = pagerank_scores.copy()
        
        # PageRank formula
        random_surfing = np.ones(n) / n
        pagerank_scores = (1 - damping_factor) * random_surfing + \
                         damping_factor * transition_matrix.T.dot(prev_scores)
        
        # Check convergence
        if np.sum(np.abs(pagerank_scores - prev_scores)) < epsilon:
            break
    
    return pagerank_scores

# Usage example
if __name__ == "__main__":
    # Create a sample adjacency matrix
    adj_matrix = np.array([
        [0, 1, 1, 0],
        [0, 0, 1, 0],
        [1, 0, 0, 1],
        [0, 0, 1, 0]
    ])
    
    # Calculate PageRank
    scores = pagerank(adj_matrix)
    
    # Print results
    for i, score in enumerate(scores):
        print(f"PageRank score for page {i}: {score:.4f}")
