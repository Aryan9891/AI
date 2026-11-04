# Experiment 4: Informed Searches (Greedy Best-First & A* Search)

## 1. Overview & Objective
This experiment explores **Informed (Heuristic) Search Algorithms**:
1. **Greedy Best-First Search**: An informed search that selects nodes solely based on the heuristic function $h(n)$ estimating the remaining distance to the goal.
2. **A\* Search**: An optimal informed search that selects nodes using the evaluation function:
   $$f(n) = g(n) + h(n)$$
   where $g(n)$ is the true path cost incurred from the start node to $n$, and $h(n)$ is the estimated cost from $n$ to the goal.
3. **Admissibility & Overestimation Analysis**: Demonstrates how overestimating the heuristic ($h(n) > h^*(n)$) violates admissibility and causes A\* to find suboptimal paths.

---

## 2. Graph & Heuristic Definition
- **Graph Nodes**: `['A', 'B', 'C', 'D', 'E', 'F']`
- **Edges & Weights**:
  - $(A, B): 4, \quad (A, C): 4, \quad (B, C): 2$
  - $(B, E): 1, \quad (C, D): 1, \quad (D, F): 2, \quad (E, F): 4$
- **Heuristic Table $h(n)$**:
  | Node | $h(n)$ | True Shortest Cost to F $h^*(n)$ | Admissible? |
  | :---: | :---: | :---: | :---: |
  | **A** | 6 | 7 | Yes ($6 \le 7$) |
  | **B** | 2 | 5 | Yes ($2 \le 5$) |
  | **C** | 3 | 3 | Yes ($3 \le 3$, Exact) |
  | **D** | 2 | 2 | Yes ($2 \le 2$, Exact) |
  | **E** | 2 | 4 | Yes ($2 \le 4$) |
  | **F** | 0 | 0 | Yes (Goal) |

---

## 3. Function Breakdown

Here is the complete documentation of every function in `exp4_informed_search.py`:

### `plot_graph_representations(save_path=None)`
- **Purpose**: Plots the graph topology displaying edge weights and the node heuristic values $h(n)$.
- **Parameters**: `save_path` (`str`, optional).
- **Returns**: `None`.

### `get_path_cost(adj, path)`
- **Purpose**: Computes total path cost along a chain of nodes.
- **Parameters**: `adj` (`dict`), `path` (`list[str]`).
- **Returns**: Integer/float total cost.

### `best_first_path(adj, h_dict, start='A', goal='F')`
- **Purpose**: Implements Greedy Best-First Search from scratch. Uses a priority queue ordered strictly by $h(u)$.
- **Parameters**: `adj`, `h_dict`, `start`, `goal`.
- **Returns**: Tuple `(path, total_cost, visit_order)`.

### `astar_path(adj, h_dict, start='A', goal='F')`
- **Purpose**: Implements A\* Search from scratch. Uses a priority queue sorted by $f(n) = g(n) + h(n)$ and maintains cumulative minimum path costs `g_score`.
- **Parameters**: `adj`, `h_dict`, `start`, `goal`.
- **Returns**: Tuple `(path, total_cost, visit_order)`.

### `visualize_search_path(adj, path, title, save_path=None)`
- **Purpose**: Generates high-resolution visualization with the search path rendered in bold red.
- **Parameters**: `adj`, `path`, `title`, `save_path`.
- **Returns**: `None`.

### `run_experiment()`
- **Purpose**: Main benchmark driver function executing searches under admissible heuristics, overestimation analysis, printing comparison tables, and saving visual figures.
- **Returns**: `None`.

---

## 4. Key Experimental Observations
### Admissible Heuristic Results:
```
Algorithm Name               | Path                 | Edge Count | Total Cost
---------------------------------------------------------------------------
Best-First Search (Greedy)   | A -> B -> E -> F     | 3          | 9         
A* Search                    | A -> C -> D -> F     | 3          | 7         
---------------------------------------------------------------------------
```
- **Greedy Best-First Search** is misled by $h(B) = 2 < h(C) = 3$ and rushes down the path $A \to B \to E \to F$ (Cost = 9).
- **A\* Search** balances actual incurred cost $g(n)$ and heuristic estimate $h(n)$, correctly discovering the optimal path $A \to C \to D \to F$ (Cost = 7).

### Overestimation Experiment:
When heuristic values of $C$ and $D$ are inflated to $h(C) = 15$ and $h(D) = 15$ ($h > h^*$):
- A\* believes the optimal branch is prohibitively expensive ($f(C) = 4 + 15 = 19$).
- A\* is diverted along $A \to B \to E \to F$ (Cost = 9).
- **Conclusion**: Admissibility ($h(n) \le h^*(n)$) is strictly necessary for A\* to guarantee optimality.

---

## 5. How to Run
### In Terminal:
```bash
python exp4_informed_search.py
```

### In JupyterLab:
Open `exp4_informed_search.ipynb` and run all cells.

