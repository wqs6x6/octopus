def prim_mst(graph):
    """
    Calculate Minimum Spanning Tree using Prim's algorithm
    Args:
        graph: Graph represented as adjacency matrix (2D list)
    Returns:
        Total weight of MST and selected edges
    """
    vertices = len(graph)
    # Track visited vertices
    visited = [False] * vertices
    # Store minimum weight edges
    min_edges = []
    # Track total weight of MST
    total_weight = 0
    
    # Start from the first vertex
    visited[0] = True
    
    # Need to find V-1 edges
    for _ in range(vertices - 1):
        min_weight = float('inf')
        min_u = min_v = -1
        
        # Find minimum weight edge from visited vertices
        for u in range(vertices):
            if visited[u]:
                for v in range(vertices):
                    if (not visited[v] and graph[u][v] > 0 and 
                        graph[u][v] < min_weight):
                        min_weight = graph[u][v]
                        min_u = u
                        min_v = v
        
        if min_u != -1:
            visited[min_v] = True
            min_edges.append((min_u, min_v, min_weight))
            total_weight += min_weight
            
    return total_weight, min_edges

# Usage example
if __name__ == "__main__":
    # Example graph as adjacency matrix (0 means no connection)
    # example_graph = [
    #     [0, 2, 0, 6, 0],
    #     [2, 0, 3, 8, 5],
    #     [0, 3, 0, 0, 7],
    #     [6, 8, 0, 0, 9],
    #     [0, 5, 7, 9, 0]
    # ]

    # example_graph = [
    #     [0, 4, 0, 0, 0, 0, 8, 0, 3, 0],
    #     [4, 0, 8, 0, 0, 0, 11, 0, 0, 7],
    #     [0, 8, 0, 7, 0, 4, 0, 2, 0, 0],
    #     [0, 0, 7, 0, 9, 14, 0, 0, 0, 0],
    #     [0, 0, 0, 9, 0, 10, 0, 0, 0, 5],
    #     [0, 0, 4, 14, 10, 0, 2, 0, 0, 0],
    #     [8, 11, 0, 0, 0, 2, 0, 1, 7, 0],
    #     [0, 0, 2, 0, 0, 0, 1, 0, 6, 0],
    #     [3, 0, 0, 0, 0, 0, 7, 6, 0, 0],
    #     [0, 7, 0, 0, 5, 0, 0, 0, 0, 0]
    # ]

    example_graph = [
        [0, 4, 0, 0, 0, 0, 8, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [4, 0, 8, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 7, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 0, 9, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 9, 0, 10, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 14, 10, 0, 2, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 2, 0, 1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 1, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 7, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 8, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 9, 0, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 7, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 3, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 2, 0, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 9, 0, 7],
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 7, 0]
    ]
    weight, edges = prim_mst(example_graph)
    print(f"Total weight of MST: {weight}")
    print("Edges in MST:")
    for u, v, w in edges:
        print(f"Edge {u} - {v}: weight = {w}")