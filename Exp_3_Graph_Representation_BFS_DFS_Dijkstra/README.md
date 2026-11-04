# Experiment 3: Graph Representations & Uninformed Searches (BFS, DFS, Dijkstra)

## 1. Overview & Objective
This experiment covers the foundational graph representations used in Artificial Intelligence and implements three fundamental search algorithms from scratch:
1. **Adjacency List** using a Python dictionary of tuples `(neighbor, weight)`.
2. **Adjacency Matrix** using a 2D nested list with the sentinel `math.inf` representing the absence of an edge.
3. **Graph Visualizations** using `networkx` and `matplotlib`.
4. **Search Algorithms from Scratch**:
   - **Breadth-First Search (BFS)**: Unweighted shortest-path search in terms of edge count.
   - **Depth-First Search (DFS)**: Unweighted deep exploration.
   - **Dijkstra's Algorithm**: Weighted shortest-path search using a priority queue (`heapq`).

---

## 2. Theoretical Note: Why 0 is Wrong as a "No Edge" Sentinel
In unweighted graphs, `0` is often used to denote absence of an edge and `1` denotes presence. However, in **weighted graphs**, `0` is a valid edge weight representing a **zero-cost traversal** between two nodes.

If `0` is used to represent "no edge":
- Shortest-path algorithms like Dijkstra's algorithm would interpret `matrix[u][v] == 0` as a free edge between `u` and `v`.
- As a consequence, disconnected nodes would appear to have zero-distance paths between each other, leading to completely corrupted search paths and distance calculations.
- Hence, the sentinel `math.inf` (infinity) is mathematically and practically mandatory, representing infinite impedance or absence of a path.

---

## 3. The Visual Graph Structure
The graph nodes are: `['A', 'B', 'C', 'D', 'E', 'F']`
Edges and weights:
- $(A, B): 4$
- $(A, C): 4$
- $(B, C): 2$
- $(B, E): 1$
- $(C, D): 1$
- $(D, F): 2$
- $(E, F): 4$

---

## 4. Detailed Function Documentation

Here is the complete reference of every function in `exp3_graph_searches.py`:

### `plot_graph_from_adj_list(save_path=None)`
- **Purpose**: Constructs a `networkx.Graph` directly from the adjacency list dictionary and renders the weighted graph.
- **Parameters**: `save_path` (`str`, optional): Filepath to save image.
- **Returns**: `None`.

### `plot_graph_from_adj_matrix(save_path=None)`
- **Purpose**: Iterates through the upper triangle of `adj_matrix`, filtering out `math.inf` and self-loops (`0`), and visualizes the resulting graph.
- **Parameters**: `save_path` (`str`, optional).
- **Returns**: `None`.

### `get_path_cost(adj, path)`
- **Purpose**: Calculates the cumulative weighted cost along a sequence of vertices in `path`.
- **Parameters**: 
  - `adj` (`dict`): The graph adjacency list.
  - `path` (`list[str]`): List of node labels (e.g. `['A', 'C', 'D', 'F']`).
- **Returns**: `int` or `float` representing total path cost.

### `bfs_path(adj, start='A', goal='F')`
- **Purpose**: Performs Breadth-First Search using a queue (`collections.deque`). It explores neighbor nodes level-by-level, ignoring weights during the search. Once the goal is reached, the path cost is computed.
- **Parameters**: `adj`, `start`, `goal`.
- **Returns**: Tuple `(path, total_cost, visit_order)`.

### `dfs_path(adj, start='A', goal='F')`
- **Purpose**: Performs Depth-First Search using a LIFO stack. It traverses as deep as possible along each branch before backtracking, ignoring weights during the search.
- **Parameters**: `adj`, `start`, `goal`.
- **Returns**: Tuple `(path, total_cost, visit_order)`.

### `dijkstra_path(adj, start='A', goal='F')`
- **Purpose**: Implements Dijkstra's Single-Source Shortest Path algorithm using a min-heap priority queue (`heapq`), a distance dictionary `dist`, and a predecessor map `parent`. Guarantees finding the minimum total-weight path.
- **Parameters**: `adj`, `start`, `goal`.
- **Returns**: Tuple `(path, total_cost, visit_order)`.

### `visualize_search_path(adj, path, title, save_path=None)`
- **Purpose**: Draws the complete graph with the discovered path and its traversing edges highlighted in bold red.
- **Parameters**: `adj`, `path`, `title`, `save_path`.
- **Returns**: `None`.

### `run_experiment()`
- **Purpose**: Main benchmark driver function. Executes all three searches, prints the formatted comparison table, prints node visitation orders, and generates visual comparison figures.
- **Returns**: `None`.

---

## 5. Experimental Results

```
---------------------------------------------------------------------------
Algorithm Name                 | Path                 | Edge Count | Total Cost
---------------------------------------------------------------------------
Breadth-First Search (BFS)     | A -> B -> E -> F     | 3          | 9         
Depth-First Search (DFS)       | A -> B -> C -> D -> F | 4          | 9         
Dijkstra's Algorithm           | A -> C -> D -> F     | 3          | 7         
---------------------------------------------------------------------------
```

- **BFS** finds the path with the fewest edges (3 edges: $A \to B \to E \to F$, cost 9).
- **DFS** explores deep paths and finds $A \to B \to C \to D \to F$ (4 edges, cost 9).
- **Dijkstra** guarantees the lowest total path weight ($A \to C \to D \to F$, cost 7).

---

## 6. How to Run
### In Terminal:
```bash
python exp3_graph_searches.py
```

### In JupyterLab:
Open `exp3_graph_searches.ipynb` and run all cells.

