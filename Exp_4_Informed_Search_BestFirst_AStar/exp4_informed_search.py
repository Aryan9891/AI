"""
Artificial Intelligence Lab - LAB 04
Informed Search: Greedy Best-First Search and A* Search
Comparison, Visualization, and Heuristic Overestimation Impact
Author: Aryan Sachin
"""

import math
import heapq
import matplotlib.pyplot as plt
import networkx as nx

# =====================================================================
# 1. Graph Data Structures & Heuristic Dictionary
# =====================================================================
nodes = ['A', 'B', 'C', 'D', 'E', 'F']

# 1. Adjacency List (using a Dictionary)
adj_list = {
    'A': [('B', 4), ('C', 4)],
    'B': [('A', 4), ('C', 2), ('E', 1)],
    'C': [('A', 4), ('B', 2), ('D', 1)],
    'D': [('C', 1), ('F', 2)],
    'E': [('B', 1), ('F', 4)],
    'F': [('D', 2), ('E', 4)]
}

# 2. Adjacency Matrix (using a Nested List with math.inf)
# Note on Sentinel math.inf:
# In weighted graphs, 0 represents a valid edge of zero weight. Using 0 for absent edges
# causes algorithms to perceive non-existent links as cost-free pathways. math.inf is mandatory.
adj_matrix = [
    #  A         B         C         D         E         F
    [0,        4,        4,        math.inf, math.inf, math.inf],
    [4,        0,        2,        math.inf, 1,        math.inf],
    [4,        2,        0,        1,        math.inf, math.inf],
    [math.inf, math.inf, 1,        0,        math.inf, 2],
    [math.inf, 1,        math.inf, math.inf, 0,        4],
    [math.inf, math.inf, math.inf, 2,        4,        0]
]

# Standard Given Heuristic Table: h(n)
h = {
    'A': 6,
    'B': 2,
    'C': 3,
    'D': 2,
    'E': 2,
    'F': 0
}

# Overestimated (Inadmissible) Heuristic Table for experimentation
h_overestimated = {
    'A': 6,
    'B': 2,
    'C': 15,  # Severely overestimated (true remaining cost is 3)
    'D': 15,  # Severely overestimated (true remaining cost is 2)
    'E': 2,
    'F': 0
}

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
def plot_graph_representations(save_path=None):
    """Plots the base graph structure with weights and heuristic values."""
    G = nx.Graph()
    for u, neighbors in adj_list.items():
        for v, w in neighbors:
            G.add_edge(u, v, weight=w)

    plt.figure(figsize=(8, 5.5))
    pos = graph_pos

    # Node labels including heuristic h(n)
    node_labels = {n: f"{n}\nh={h[n]}" for n in nodes}

    nx.draw_networkx_nodes(G, pos, node_color='#b3cde3', node_size=1500, edgecolors='#333333', linewidths=2)
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=11, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='#666666')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

    plt.title("Visual Graph with Edge Costs & Heuristics h(n)", fontsize=13, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    plt.show()

# =====================================================================
# 3. Informed Search Implementations
# =====================================================================
def get_path_cost(adj, path):
    """Calculates total path cost."""
    cost = 0
    for u, v in zip(path[:-1], path[1:]):
        for nbr, w in adj[u]:
            if nbr == v:
                cost += w
                break
    return cost

# 1. best_first_path(adj_list, h, 'A', 'F') - Greedy Best-First Search
def best_first_path(adj, h_dict, start='A', goal='F'):
    """
    Greedy Best-First Search:
    Expands nodes based strictly on heuristic value h(n).
    Returns (path, total_cost, visit_order).
    """
    # Priority Queue elements: (heuristic_cost, current_node, path)
    pq = [(h_dict[start], start, [start])]
    visited = set()
    visit_order = []

    while pq:
        h_val, u, path = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        visit_order.append(u)

        if u == goal:
            return path, get_path_cost(adj, path), visit_order

        for v, _ in sorted(adj[u], key=lambda x: x[0]):
            if v not in visited:
                heapq.heappush(pq, (h_dict[v], v, path + [v]))

    return None, 0, visit_order

# 2. astar_path(adj_list, h, 'A', 'F') - A* Search
def astar_path(adj, h_dict, start='A', goal='F'):
    """
    A* Search:
    Expands nodes based on f(n) = g(n) + h(n), where g(n) is path cost from start.
    Returns (path, total_cost, visit_order).
    """
    # Priority Queue elements: (f_score, g_score, current_node, path)
    pq = [(h_dict[start], 0, start, [start])]
    g_score = {node: math.inf for node in adj}
    g_score[start] = 0
    visited = set()
    visit_order = []

    while pq:
        f_val, g_val, u, path = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        visit_order.append(u)

        if u == goal:
            return path, g_val, visit_order

        for v, weight in sorted(adj[u], key=lambda x: x[0]):
            tentative_g = g_val + weight
            if tentative_g < g_score[v]:
                g_score[v] = tentative_g
                f_val_v = tentative_g + h_dict[v]
                heapq.heappush(pq, (f_val_v, tentative_g, v, path + [v]))

    return None, 0, visit_order

# =====================================================================
# 4. Visualization of Search Paths
# =====================================================================
def visualize_search_path(adj, path, title, save_path=None):
    """Visualizes the graph highlighting the search path in bold red."""
    G = nx.Graph()
    for u, neighbors in adj.items():
        for v, w in neighbors:
            G.add_edge(u, v, weight=w)

    path_edges = list(zip(path[:-1], path[1:]))

    plt.figure(figsize=(7, 5))
    pos = graph_pos

    nx.draw_networkx_nodes(G, pos, node_color='#e0ecf4', node_size=1200, edgecolors='#8856a7', linewidths=2)
    nx.draw_networkx_labels(G, pos, font_size=13, font_weight='bold')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='#999999')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11)

    # Path in red
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='#ff9999', node_size=1350, edgecolors='#cc0000', linewidths=2.5)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4, edge_color='#cc0000')

    plt.title(title, fontsize=13, fontweight='bold', color='#990000')
    plt.axis('off')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=200)
    plt.show()

# =====================================================================
# 5. Main Experiment Execution
# =====================================================================
def run_experiment():
    print("=" * 70)
    print(" EXPERIMENT 4: Informed Searches (Best-First Search vs. A* Search)")
    print("=" * 70)

    # 1. Searches with Given Admissible Heuristic
    bfs_res = best_first_path(adj_list, h, 'A', 'F')
    astar_res = astar_path(adj_list, h, 'A', 'F')

    print("\n--- RESULTS WITH ADMISSIBLE HEURISTIC ---")
    print(f"{'Algorithm Name':<28} | {'Path':<20} | {'Edge Count':<10} | {'Total Cost':<10}")
    print("-" * 75)
    for name, res in [("Best-First Search (Greedy)", bfs_res), ("A* Search", astar_res)]:
        path, cost, _ = res
        print(f"{name:<28} | {' -> '.join(path):<20} | {len(path)-1:<10} | {cost:<10}")
    print("-" * 75)

    print(f"Best-First Search Visit Order: {' -> '.join(bfs_res[2])}")
    print(f"A* Search Visit Order:          {' -> '.join(astar_res[2])}\n")

    # 2. Heuristic Overestimation Study
    astar_over_res = astar_path(adj_list, h_overestimated, 'A', 'F')
    print("--- HEURISTIC OVERESTIMATION OBSERVATION ---")
    print("Original Heuristic:     h(C)=3, h(D)=2 (Admissible: h <= true cost)")
    print("Overestimated Heuristic:h(C)=15, h(D)=15 (Inadmissible: h > true cost)")
    print(f"A* under Overestimation Path:  {' -> '.join(astar_over_res[0])}")
    print(f"A* under Overestimation Cost:  {astar_over_res[1]} (Suboptimal vs Optimal 7!)")
    print("Observation: When h(n) overestimates the true remaining cost, A* loses its guarantee")
    print("of optimality because it mistakenly prunes or defers exploring the optimal branch.\n")

    # Visualizations
    visualize_search_path(adj_list, bfs_res[0], f"Greedy Best-First Search: {' -> '.join(bfs_res[0])} (Cost: {bfs_res[1]})", "Exp_4_Informed_Search_BestFirst_AStar/best_first_path.png")
    visualize_search_path(adj_list, astar_res[0], f"A* Search (Optimal): {' -> '.join(astar_res[0])} (Cost: {astar_res[1]})", "Exp_4_Informed_Search_BestFirst_AStar/astar_path.png")
    visualize_search_path(adj_list, astar_over_res[0], f"A* under Overestimated Heuristic: {' -> '.join(astar_over_res[0])} (Cost: {astar_over_res[1]})", "Exp_4_Informed_Search_BestFirst_AStar/astar_overestimated_path.png")


if __name__ == "__main__":
    run_experiment()

