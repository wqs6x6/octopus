from collections import deque
from typing import Dict, List, Set

def bfs(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Implementation of Breadth-First Search algorithm
    
    Args:
        graph: Graph represented as adjacency list where key is node and value is list of neighbors
        start: Starting node
        
    Returns:
        List of nodes in the order they were visited
    """
    # Initialize visited set and result list
    visited: Set[int] = set()
    result: List[int] = []
    
    # Create queue and add starting node
    queue = deque([start])
    visited.add(start)
    
    # Main BFS loop
    while queue:
        # Get next node from queue
        current = queue.popleft()
        result.append(current)
        
        # Visit all neighbors of current node
        for neighbor in graph[current]:
            # If neighbor hasn't been visited, add to queue
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

# Usage example
if __name__ == "__main__":
    # Create example graph
    # example_graph = {
    #     0: [1, 2],
    #     1: [0, 2, 3],
    #     2: [0, 1, 4],
    #     3: [1],
    #     4: [2]
    # }
    
    # # Start traversal from node 0
    # result = bfs(example_graph, 0)
    # print(f"BFS traversal order: {result}")



    # Create a more complex example graph
    complex_graph = {
        0: [1, 2, 3],
        1: [0, 4, 5],
        2: [0, 5, 6],
        3: [0, 7],
        4: [1, 8, 9],
        5: [1, 2, 9, 10],
        6: [2, 10, 11],
        7: [3, 11],
        8: [4, 12],
        9: [4, 5, 12, 13],
        10: [5, 6, 13, 14],
        11: [6, 7, 14],
        12: [8, 9, 15],
        13: [9, 10, 15],
        14: [10, 11, 15],
        15: [12, 13, 14]
    }
    
    # Start traversal from different nodes
    start_nodes = [0, 7, 15]
    for start in start_nodes:
        result = bfs(complex_graph, start)
        print(result)
        print(f"BFS traversal starting from node {start}: {result}")