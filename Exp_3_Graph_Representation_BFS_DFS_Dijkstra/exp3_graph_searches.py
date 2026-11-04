"""
Artificial Intelligence Lab - LAB 03
Graph Representations (Adjacency List & Adjacency Matrix) and
Uninformed vs. Optimal Graph Searches (BFS, DFS, Dijkstra)
Author: Aryan Sachin
"""

import math
import heapq
from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

# =====================================================================
# 1. Graph Data Structures
# =====================================================================
# Node labels
nodes = ['A', 'B', 'C', 'D', 'E', 'F']
node_to_idx = {n: i for i, n in enumerate(nodes)}

# 1. Adjacency List (using a Dictionary)
# Key: node, Value: list of tuples (neighbor, weight)
adj_list = {
    'A': [('B', 4), ('C', 4)],
    'B': [('A', 4), ('C', 2), ('E', 1)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('C', 1), ('F', 2)],
    'E': [('B', 1), ('F', 4)],
    'F': [('D', 2), ('E', 4)]
}

# 2. Adjacency Matrix (using a Nested List)
# Note on Sentinel math.inf:
# In weighted graphs, 0 is a valid edge weight representing a zero-cost transition.
# Using 0 to represent 'no edge' would cause shortest path algorithms (like Dijkstra)
# to treat absent edges as free traversals. Thus, math.inf is the correct sentinel.
adj_matrix = [
    #  A         B         C         D         E         F
    [0,        4,        4,        math.inf, math.inf, math.inf],  # A
    [4,        0,        2,        math.inf, 1,        math.inf],  # B
    [4,        2,        0,        1,        math.inf, math.inf],  # C
    [math.inf, math.inf, 1,        0,        math.inf, 2],         # D
    [math.inf, 1,        math.inf, math.inf, 0,        4],         # E
    [math.inf, math.inf, math.inf, 2,        4,        0]          # F
]

# Fixed 2D layout matching the lab assignment diagram
graph_pos = {
    'A': (0.0, 1.0),
    'B': (1.0, 1.6),
    'C': (1.0, 0.4),
    'D': (2.0, 2.0),
    'E': (2.0, 0.5),
    'F': (2.8, 1.3)
}

# =====================================================================
# 2. Plotting Functions
# =====================================================================
def plot_graph_from_adj_list(save_path=None):
    """Plots the graph directly from the adjacency list."""
    G = nx.Graph()
    for u, neighbors in adj_list.items():
        for v, w in neighbors:
            G.add_edge(u, v, weight=w)

    plt.figure(figsize=(7, 5))
    pos = graph_pos
    nx.draw_networkx_nodes(G, pos, node_color='#6baed6', node_size=1200, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', font_color='white')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='#555555')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    plt.title("Visual Graph Representation (from Adjacency List)", fontsize=13, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    plt.show()

def plot_graph_from_adj_matrix(save_path=None):
    """Plots the graph directly from the adjacency matrix."""
    G = nx.Graph()
    n = len(nodes)
    for i in range(n):
        for j in range(i + 1, n):
            w = adj_matrix[i][j]
            if w != math.inf and w > 0:
                G.add_edge(nodes[i], nodes[j], weight=int(w))

    plt.figure(figsize=(7, 5))
    pos = graph_pos
    nx.draw_networkx_nodes(G, pos, node_color='#74c476', node_size=1200, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=14, font_weight='bold', font_color='white')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='#555555')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    plt.title("Visual Graph Representation (from Adjacency Matrix)", fontsize=13, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    plt.show()

# =====================================================================
# 3. Search Algorithms (Implemented From Scratch)
# =====================================================================
def get_path_cost(adj, path):
    """Calculates the total edge cost of a given path."""
    cost = 0
    for u, v in zip(path[:-1], path[1:]):
        for nbr, w in adj[u]:
            if nbr == v:
                cost += w
                break
    return cost

def bfs_path(adj, start='A', goal='F'):
    """
    Breadth-First Search (BFS): ignores weights during search.
    Returns (path, total_cost, visit_order).
    """
    queue = deque([[start]])
    visited = {start}
    visit_order = [start]

    while queue:
        path = queue.popleft()
        node = path[-1]
        if node == goal:
            return path, get_path_cost(adj, path), visit_order

        for nbr, _ in sorted(adj[node], key=lambda x: x[0]):
            if nbr not in visited:
                visited.add(nbr)
                visit_order.append(nbr)
                queue.append(path + [nbr])

    return None, 0, visit_order

def dfs_path(adj, start='A', goal='F'):
    """
    Depth-First Search (DFS): ignores weights during search.
    Returns (path, total_cost, visit_order).
    """
    stack = [[start]]
    visited = set()
    visit_order = []

    while stack:
        path = stack.pop()
        node = path[-1]
        if node not in visited:
            visited.add(node)
            visit_order.append(node)
            if node == goal:
                return path, get_path_cost(adj, path), visit_order

            # Explore neighbors in alphabetical order
            for nbr, _ in sorted(adj[node], key=lambda x: x[0], reverse=True):
                if nbr not in visited:
                    stack.append(path + [nbr])

    return None, 0, visit_order

def dijkstra_path(adj, start='A', goal='F'):
    """
    Dijkstra's Algorithm: uses heapq, dist, and parent dictionaries.
    Returns (path, total_cost, visit_order).
    """
    dist = {n: math.inf for n in adj}
    parent = {n: None for n in adj}
    dist[start] = 0
    pq = [(0, start)]
    visit_order = []
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        visit_order.append(u)
        if u == goal:
            break

        for v, weight in sorted(adj[u], key=lambda x: x[0]):
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))

    # Reconstruct shortest path
    path = []
    curr = goal
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return path, dist[goal], visit_order

# =====================================================================
# 4. Visualization of Search Paths
# =====================================================================
def visualize_search_path(adj, path, title, save_path=None):
    """Draws the graph highlighting the selected path and its edges in bold red."""
    G = nx.Graph()
    for u, neighbors in adj.items():
        for v, w in neighbors:
            G.add_edge(u, v, weight=w)

    path_edges = list(zip(path[:-1], path[1:]))

    plt.figure(figsize=(7, 5))
    pos = graph_pos

    # Base graph
    nx.draw_networkx_nodes(G, pos, node_color='#cfe2f3', node_size=1200, edgecolors='#4a86e8', linewidths=2)
    nx.draw_networkx_labels(G, pos, font_size=13, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='#aaaaaa')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11)

    # Highlighted path in red
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#ff9999', node_size=1300, edgecolors='#cc0000', linewidths=2.5)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='#cc0000')

    plt.title(title, fontsize=13, fontweight='bold', color='#990000')
    plt.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    plt.show()

# =====================================================================
# 5. Execution and Comparison Table
# =====================================================================
def run_experiment():
    print("=" * 70)
    print(" EXPERIMENT 3: Graph Representations & Search Algorithms (BFS, DFS, Dijkstra)")
    print("=" * 70)

    # Execute searches
    bfs_res = bfs_path(adj_list, 'A', 'F')
    dfs_res = dfs_path(adj_list, 'A', 'F')
    dijkstra_res = dijkstra_path(adj_list, 'A', 'F')

    results = [
        ("Breadth-First Search (BFS)", bfs_res),
        ("Depth-First Search (DFS)", dfs_res),
        ("Dijkstra's Algorithm", dijkstra_res)
    ]

    # Print Comparison Table
    print("\n" + "-" * 75)
    print(f"{'Algorithm Name':<30} | {'Path':<20} | {'Edge Count':<10} | {'Total Cost':<10}")
    print("-" * 75)
    for name, (path, cost, order) in results:
        path_str = " -> ".join(path)
        edge_count = len(path) - 1
        print(f"{name:<30} | {path_str:<20} | {edge_count:<10} | {cost:<10}")
    print("-" * 75 + "\n")

    for name, (path, cost, order) in results:
        print(f"{name} Visit Order: {' -> '.join(order)}")

    # Visualizations
    visualize_search_path(adj_list, bfs_res[0], f"BFS Path: {' -> '.join(bfs_res[0])} (Cost: {bfs_res[1]})", "Exp_3_Graph_Representation_BFS_DFS_Dijkstra/bfs_path.png")
    visualize_search_path(adj_list, dfs_res[0], f"DFS Path: {' -> '.join(dfs_res[0])} (Cost: {dfs_res[1]})", "Exp_3_Graph_Representation_BFS_DFS_Dijkstra/dfs_path.png")
    visualize_search_path(adj_list, dijkstra_res[0], f"Dijkstra Path: {' -> '.join(dijkstra_res[0])} (Cost: {dijkstra_res[1]})", "Exp_3_Graph_Representation_BFS_DFS_Dijkstra/dijkstra_path.png")


if __name__ == "__main__":
    run_experiment()

