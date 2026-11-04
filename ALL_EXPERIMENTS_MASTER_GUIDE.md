# Artificial Intelligence Lab — Master Guide (Experiments 1 to 9)

**Author:** Aryan Sachin  
**Environment:** Python 3 / JupyterLab  
**Repository Structure:** All experiments are organized in modular directories containing standalone Python scripts (`.py`), interactive Jupyter Notebooks (`.ipynb`), and individual documentation files (`README.md`).

---

# Table of Contents
1. [Experiment 1: Vacuum Cleaner World Agent (2×1 Grid)](#experiment-1-vacuum-cleaner-world-agent-21-grid)
2. [Experiment 2: Utility-Based Vacuum Cleaner Agent ($m \times n$ Grid)](#experiment-2-utility-based-vacuum-cleaner-agent-m--n-grid)
3. [Experiment 3: Graph Representations & Uninformed Searches (BFS, DFS, Dijkstra)](#experiment-3-graph-representations--uninformed-searches-bfs-dfs-dijkstra)
4. [Experiment 4: Informed Searches (Greedy Best-First & A* Search)](#experiment-4-informed-searches-greedy-best-first--a-search)
5. [Experiment 5: Local Search (Hill Climbing & Simulated Annealing)](#experiment-5-local-search-hill-climbing--simulated-annealing)
6. [Experiment 6: Adversarial Search (Tic-Tac-Toe & Minimax)](#experiment-6-adversarial-search-tic-tac-toe--minimax)
7. [Experiment 7: Connect-3 on a 4×4 Board (Minimax vs. Alpha–Beta Pruning)](#experiment-7-connect-3-on-a-44-board-minimax-vs-alphabeta-pruning)
8. [Experiment 8: Knowledge-Based Rule Agent for Wumpus World](#experiment-8-knowledge-based-rule-agent-for-wumpus-world)
9. [Experiment 9: Propositional Logic Engine & Model Checking](#experiment-9-propositional-logic-engine--model-checking)

---

# Experiment 1: Vacuum Cleaner World Agent (2×1 Grid)

## 1. Overview & Objective
Design a **Function-Based (No Classes)** Vacuum Cleaner World Agent in a $2 \times 1$ grid environment.
- **Environment**: Discrete $2 \times 1$ grid. Each cell is either `0` (Clean) or `1` (Dirty), representing the hidden physical ground truth.
- **Agent Knowledge**: The agent maintains its own internal belief array `[None, None]` (`?`). It knows nothing about any cell until it visits and perceives it.
- **Actions**:
  - If current cell is dirty: **Vacuum** first before moving.
  - If current cell is clean: Move **Left** or **Right** within grid boundaries.
- **Termination**: Terminates strictly when the agent's *own knowledge* confirms all cells are clean (no `None`, no `1`), or maximum iterations are reached.

## 2. Functions & Implementation Details
- `create_environment()`: Creates and returns `[0, 0]`.
- `place_dirt(env)`: Randomly assigns `0` or `1` to cells (guaranteeing at least one dirty cell).
- `place_agent(grid_size)`: Returns random starting index (0 or 1).
- `create_knowledge(grid_size)`: Initializes belief array with `None` values (`[None, None]`).
- `perceive(env, knowledge, pos)`: Senses true status of cell at `pos` and updates `knowledge[pos]`.
- `is_dirty(env, pos)`: Returns `True` if `env[pos] == 1`.
- `vacuum(env, knowledge, pos)`: Sets `env[pos] = 0` and `knowledge[pos] = 0`.
- `get_possible_moves(pos, grid_size)`: Returns boundary-checked directions (`['Right']` at 0, `['Left']` at 1).
- `move_agent(pos, grid_size)`: Randomly selects a valid move; returns `(new_pos, direction)`.
- `knowledge_all_clean(knowledge)`: Returns `True` iff every entry in `knowledge` is `0`.
- `all_clean(env)`: Debug function checking ground truth state.
- `display_environment(knowledge, agent_pos, action, step)`: Formats output using exact lab notation:
  - `D`: Dirty (known)
  - `C`: Clean (known)
  - `?`: Unknown
  - `A()`: Agent perceiving
  - `A(V)`: Agent vacuuming
  - `A(R)` / `A(L)`: Agent moving Right / Left
- `run_vacuum_world()`: Main driver simulation loop.
- `run_vacuum_world_generalized(grid_size)`: Experiment 2 extension for arbitrary $N \times 1$ grid.

## 3. Python Source Code
```python
import random

def create_environment():
    return [0, 0]

def place_dirt(env):
    for i in range(len(env)):
        env[i] = random.choice([0, 1])
    if sum(env) == 0:
        env[random.randint(0, len(env) - 1)] = 1
    return env

def place_agent(grid_size=2):
    return random.randint(0, grid_size - 1)

def create_knowledge(grid_size=2):
    return [None] * grid_size

def perceive(env, knowledge, pos):
    knowledge[pos] = env[pos]
    return knowledge

def is_dirty(env, pos):
    return env[pos] == 1

def vacuum(env, knowledge, pos):
    env[pos] = 0
    knowledge[pos] = 0
    return env, knowledge

def get_possible_moves(pos, grid_size=2):
    moves = []
    if pos > 0:
        moves.append('Left')
    if pos < grid_size - 1:
        moves.append('Right')
    return moves

def move_agent(pos, grid_size=2):
    valid_moves = get_possible_moves(pos, grid_size)
    if not valid_moves:
        return pos, None
    direction = random.choice(valid_moves)
    new_pos = pos - 1 if direction == 'Left' else pos + 1
    return new_pos, direction

def knowledge_all_clean(knowledge):
    for status in knowledge:
        if status is None or status == 1:
            return False
    return True

def all_clean(env):
    return all(cell == 0 for cell in env)

def display_environment(knowledge, agent_pos, action, step):
    header = "Initial Stage:" if step == 0 else f"Run {step}:"
    cells_str = ""
    for i in range(len(knowledge)):
        status = knowledge[i]
        status_label = "?" if status is None else ("D" if status == 1 else "C")
        if i == agent_pos:
            if action == "perceive" or action is None:
                cell_repr = f"[A(),{status_label}]"
            elif action == "vacuum":
                cell_repr = f"[A(V),{status_label}]"
            elif action == "move_Right":
                cell_repr = f"[A(R),{status_label}]"
            elif action == "move_Left":
                cell_repr = f"[A(L),{status_label}]"
            else:
                cell_repr = f"[A({action}),{status_label}]"
        else:
            cell_repr = "[?]" if status is None else f"[{status_label}]"
        cells_str += cell_repr
    print(header)
    print(cells_str)

def run_vacuum_world(max_iterations=20):
    env = create_environment()
    env = place_dirt(env)
    agent_pos = place_agent(len(env))
    knowledge = create_knowledge(len(env))

    perceive(env, knowledge, agent_pos)
    step = 0
    display_environment(knowledge, agent_pos, "perceive", step)

    while not knowledge_all_clean(knowledge) and step < max_iterations:
        step += 1
        if knowledge[agent_pos] == 1:
            vacuum(env, knowledge, agent_pos)
            display_environment(knowledge, agent_pos, "vacuum", step)
        else:
            new_pos, direction = move_agent(agent_pos, len(env))
            display_environment(knowledge, agent_pos, f"move_{direction}", step)
            agent_pos = new_pos
            perceive(env, knowledge, agent_pos)
            step += 1
            display_environment(knowledge, agent_pos, "perceive", step)

    if knowledge_all_clean(knowledge):
        print("All cells are clean! Task Completed.")
    else:
        print("Maximum iterations reached.")
    print(f"True environment state: {env} (All clean: {all_clean(env)})\n")
```

## 4. Output
```
Initial Stage:
[A(),C][?]
Run 1:
[A(R),C][?]
Run 2:
[C][A(),D]
Run 3:
[C][A(V),C]
All cells are clean! Task Completed.
True environment state: [0, 0] (All clean: True)
```

---

# Experiment 2: Utility-Based Vacuum Cleaner Agent ($m \times n$ Grid)

## 1. Overview & Objective
Implements a **Utility-Based Intelligent Agent** operating in an $m \times n$ grid:
- **Fully Observable Mode**: Agent has complete access to the grid state, calculates exact BFS distances to remaining dirty cells, and picks the action maximizing expected utility.
- **Partially Observable Mode**: Agent maintains a belief matrix, rewarding exploration of unknown (`None`) cells while prioritizing known dirty cells.
- **Performance Metrics**: Steps, Vacuums, Moves, Energy Consumed, Theoretical Minimum, and Optimality Ratio.

## 2. Mathematical Utility Function
$$U(a) = \text{VacuumReward}(a) - \text{DistanceToNearestDirty}(a) - \text{MovementCost}(a) + \text{DirtDensityNearby}(a)$$
- $\text{VacuumReward}(a) = 10$ if $a == \text{'vacuum'}$ and current cell is dirty; $-5$ otherwise.
- $\text{DistanceToNearestDirty}(a)$: BFS shortest-path distance from resulting position to nearest remaining dirty cell.
- $\text{MovementCost}(a) = 1$ for directional moves, $0$ for vacuuming.
- $\text{DirtDensityNearby}(a)$: Number of dirty cells within Chebyshev neighborhood ($r \le 1$).

## 3. Key Functions
- `find_nearest_dirty_cell(env, pos, rows, cols)`: Executes queue-based BFS over 2D grid to compute true shortest distance to closest dirt.
- `compute_utility(action, pos, env, rows, cols)`: Evaluates $U(a)$ for candidate action.
- `choose_best_action(pos, env, rows, cols)`: Selects $\arg\max_{a} U(a)$.
- `compute_theoretical_minimum(env, start_pos, rows, cols)`: Lower-bound estimation of minimal moves.
- `update_metrics(metrics, action_taken)`: Accumulates energy and step counters.
- `display_performance_summary(metrics)`: Prints optimality report.

## 4. Output
```
Step 11 (Action: Right):
[C][C][A(R),D]
[C][C][C]
[C][C][C]

Step 12 (Action: vacuum):
[C][C][A(V),C]
[C][C][C]
[C][C][C]

Success: All cells in grid are clean! Task Completed.
=============================================
        PERFORMANCE SUMMARY REPORT
=============================================
Total Steps Executed:      12
Total Clean/Vacuum Actions:4
Total Movement Steps:      8
Total Energy Consumed:     16 units
Theoretical Min Steps:     7
Optimality Ratio:          1.71 (Actual / Theoretical)
=============================================
```

---

# Experiment 3: Graph Representations & Uninformed Searches (BFS, DFS, Dijkstra)

## 1. Overview & Objective
- Translates a visual weighted graph with vertices `A, B, C, D, E, F` into:
  1. `adj_list` (Dictionary)
  2. `adj_matrix` (2D nested list with sentinel `math.inf`)
- Explains why `0` is mathematically incorrect as an edge sentinel in weighted graphs (0 denotes a valid zero-cost traversal, whereas `math.inf` denotes absence of a connection).
- Implements from scratch:
  - **BFS** (ignores weights, finds shortest path in terms of edge count)
  - **DFS** (deep traversal)
  - **Dijkstra** (priority queue via `heapq`, finds lowest weighted path cost)
- Visualizes the graph and highlights the returned paths in bold red using `networkx` and `matplotlib`.

## 2. Graph Definition
Edges and weights:
- $(A, B): 4, \quad (A, C): 4, \quad (B, C): 2$
- $(B, E): 1, \quad (C, D): 1, \quad (D, F): 2, \quad (E, F): 4$

## 3. Comparison Results Table
```
---------------------------------------------------------------------------
Algorithm Name                 | Path                 | Edge Count | Total Cost
---------------------------------------------------------------------------
Breadth-First Search (BFS)     | A -> B -> E -> F     | 3          | 9         
Depth-First Search (DFS)       | A -> B -> C -> D -> F | 4          | 9         
Dijkstra's Algorithm           | A -> C -> D -> F     | 3          | 7         
---------------------------------------------------------------------------

BFS Visit Order:      A -> B -> C -> E -> D -> F
DFS Visit Order:      A -> B -> C -> D -> F
Dijkstra Visit Order: A -> B -> C -> D -> E -> F
```

---

# Experiment 4: Informed Searches (Greedy Best-First & A* Search)

## 1. Overview & Objective
- Implements **Greedy Best-First Search** (driven strictly by remaining heuristic $h(n)$).
- Implements **A\* Search** (driven by evaluation function $f(n) = g(n) + h(n)$).
- Investigates the requirement of **heuristic admissibility** ($h(n) \le h^*(n)$) and demonstrates how overestimating heuristic values causes A\* to miss the optimal path.

## 2. Heuristics Table $h(n)$
- $h(A) = 6, \quad h(B) = 2, \quad h(C) = 3, \quad h(D) = 2, \quad h(E) = 2, \quad h(F) = 0$

## 3. Comparison Results
```
--- RESULTS WITH ADMISSIBLE HEURISTIC ---
Algorithm Name               | Path                 | Edge Count | Total Cost
---------------------------------------------------------------------------
Best-First Search (Greedy)   | A -> B -> E -> F     | 3          | 9         
A* Search                    | A -> C -> D -> F     | 3          | 7         
---------------------------------------------------------------------------

--- HEURISTIC OVERESTIMATION OBSERVATION ---
Original Heuristic:      h(C)=3,  h(D)=2   (Admissible: h <= true cost)
Overestimated Heuristic: h(C)=15, h(D)=15  (Inadmissible: h > true cost)

A* under Overestimated Heuristic Path: A -> B -> E -> F
A* under Overestimated Heuristic Cost: 9 (Suboptimal vs Optimal 7!)
```

---

# Experiment 5: Local Search (Hill Climbing & Simulated Annealing)

## 1. Overview & Objective
- **Part 1: 1D Landscape Optimization**:
  - Global maximization of $f(x) = \sin(x) + \sin\left(\frac{10x}{3}\right)$ over $x \in [0, 10]$.
  - Compares Hill Climbing vs. Simulated Annealing with temperature cooling schedule $T_{k+1} = \alpha T_k$ and Metropolis criterion $P = \exp(\Delta E / T)$.
- **Part 2: 8-Queens Problem**:
  - Representation: list of 8 integers indicating queen rows in each column.
  - Objective: Number of non-attacking queen pairs ($\max = \binom{8}{2} = 28$, corresponding to 0 conflicts).
  - Compares **First-Choice Hill Climbing** vs. **Simulated Annealing**.

## 2. Experimental Output
```
--- PART 1: 1D Landscape Optimization ---
Hill Climbing Result:       x = 2.3000, f(x) = 1.7282 (Trapped at local peak!)
Simulated Annealing Result: x = 7.9979, f(x) = 1.9887 (Found True Global Max!)

--- PART 2: 8-Queens Problem ---
First-Choice Hill Climbing: Score = 26/28 (Trapped in local optimum with 2 conflicts)
Simulated Annealing:        Score = 28/28 (Zero conflicts solution discovered!)
  +-----------------+
8 | . . . Q . . . . |
7 | . . . . . . Q . |
6 | . . Q . . . . . |
5 | . . . . . . . Q |
4 | . Q . . . . . . |
3 | . . . . Q . . . |
2 | Q . . . . . . . |
1 | . . . . . Q . . |
  +-----------------+
    A B C D E F G H
```

---

# Experiment 6: Adversarial Search (Tic-Tac-Toe & Minimax)

## 1. Overview & Objective
- **Part 1: Two-Player Human Game**: Alternating turns sharing the terminal with robust input validation and win/draw detection.
- **Part 2: Minimax AI Agent**:
  - Game tree search exploring recursive outcomes.
  - Depth-discounted scoring ($+10 - \text{depth}$ for AI win, $\text{depth} - 10$ for human win) to guarantee fastest win and delayed loss.
  - Matches the exact line user interface (LUI) and sample output format in the lab brief.

## 2. Sample Match Output
```
--- TIC-TAC-TOE ---
Do you want to play first? (y/n): y
You are X, the computer is O.
1 | 2 | 3
---+---+---
4 | 5 | 6
---+---+---
7 | 8 | 9
Your move (X): 1
Computer is thinking...
Computer plays 5
X | 2 | 3
---+---+---
4 | O | 6
---+---+---
7 | 8 | 9
Your move (X): 9
Computer is thinking...
Computer plays 2
X | O | 3
---+---+---
4 | O | 6
---+---+---
7 | 8 | X
Your move (X): 4
Computer is thinking...
Computer plays 8
X | O | 3
---+---+---
X | O | 6
---+---+---
7 | O | X
Computer (O) wins!
```

---

# Experiment 7: Connect-3 on a 4×4 Board (Minimax vs. Alpha–Beta Pruning)

## 1. Overview & Objective
- Connect-3 on a $4 \times 4$ board (16 cells total).
- Pieces obey gravity: drop to lowest unoccupied cell in chosen column $[1, 4]$.
- First player to complete 3-in-a-row (horizontal, vertical, diagonal) wins.
- Quantifies search tree reduction between **Plain Minimax** and **Alpha–Beta Pruning** ($\beta \le \alpha$ cutoffs).

## 2. Pruning Comparison Results
```
============================================================
           SEARCH TREE PRUNING COMPARISON
============================================================
Plain Minimax Total Node Evaluations:   26,589
Alpha-Beta Pruning Node Evaluations:    1,270
Nodes Pruned (Removed from Search):     25,319
Search Space Reduction:                 95.22%
============================================================
```

---

# Experiment 8: Knowledge-Based Rule Agent for Wumpus World

## 1. Overview & Objective
- $N \times N$ Wumpus World grid (1-based, $(1, 1)$ bottom-left).
- Percepts: `Stench`, `Breeze`, `Glitter`, `Scream`.
- Rule-based deduction:
  - `PitFree`: Visited cells + neighbors of visited cells with no Breeze.
  - `WumpusCandidates`: Starts as all cells except $(1, 1)$. Refined via Stench intersection and no-Stench elimination. Line of arrow flight eliminated if no scream.
  - `Safe`: In `PitFree` AND (`WumpusDead` OR not in `WumpusCandidates`).
- Planning: BFS through visited/safe cells to nearest safe unvisited cell; arrow shot when blocked.

## 2. Benchmark Test Cases
1. **Test 1**: Gold at $(2, 3)$, Wumpus at $(1, 3)$, Pits at $(3, 1), (3, 3), (4, 4)$.
   - Verdict: **POSSIBLE**
   - Shortest Safe Path: $(1, 1) \to (1, 2) \to (2, 2) \to (2, 3)$
2. **Test 2**: Gold at $(3, 2)$, Wumpus at $(2, 1)$, Pits at $(3, 3), (4, 1)$.
   - Action: `SHOOT_RIGHT` $\to$ Scream!
   - Verdict: **POSSIBLE**
   - Shortest Safe Path: $(1, 1) \to (1, 2) \to (2, 2) \to (3, 2)$
3. **Test 3**: Wumpus and Pit co-located at $(2, 1)$, Gold at $(4, 4)$.
   - Verdict: **NOT POSSIBLE** (Killing Wumpus does not clear the pit).

---

# Experiment 9: Propositional Logic Engine & Model Checking

## 1. Overview & Objective
- Propositional logic engine representing formulas as nested tuples.
- **Model Checking**: Evaluates sentences over all $2^n$ interpretations to decide:
  - Entailment: $KB \models \alpha$ iff $\alpha$ is True in every model where $KB$ is True.
  - Validity: Tautology check ($2^n$ models evaluate to True).
  - Satisfiability: At least one model evaluates to True.
- **Wumpus World Reasoning**: Replaces heuristics with formal logical entailment:
  $$B_{x,y} \iff \bigvee_{n \in \text{nbrs}} P_n, \quad S_{x,y} \iff \bigvee_{n \in \text{nbrs}} W_n$$
  Proves cells pit-free and wumpus-free via model checking before visiting.

## 2. Test Verification Output
```
--- 1. Testing Contrapositive Equivalence: (P => Q) <=> (~Q => ~P) ---
Truth Table for: ((P => Q) <=> (~Q => ~P))
-----------------------------------------
  P   |   Q   | ((P => Q) <=> (~Q => ~P))
-----------------------------------------
  T   |   T   |             T            
  T   |   F   |             T            
  F   |   T   |             T            
  F   |   F   |             T            
-----------------------------------------
Is the sentence Valid (Tautology)? True

--- 2. Testing Entailment by Truth-Table Enumeration ---
KB: ['(P => Q)', '(Q => R)', 'P']
Query 1: Does KB |= R?    True
Query 2: Does KB |= ~R?   False

--- 3. Validity and Satisfiability Checks ---
Sentence        | Valid?     | Satisfiable?   
---------------------------------------------
P or ~P         | Yes        | Yes            
P and Q         | No         | Yes            
P and ~P        | No         | No             
---------------------------------------------

--- 4. Propositional Logic Wumpus World Navigation ---
Path Discovered via Propositional Logic Entailment:
(1,1) -> (2,1) -> (1,1) -> (1,2) -> (2,2) -> (3,2) -> (2,2) -> (2,3)
All traversed cells were formally proven pit-free and wumpus-free by model checking!
```

---

# How to Run Everything

### Running via JupyterLab:
1. Launch JupyterLab in the workspace:
   ```bash
   jupyter lab
   ```
2. In the file browser, navigate to any experiment folder (e.g., `Exp_1_Vacuum_Cleaner_Agent`) and open the `.ipynb` notebook.
3. Select **Run -> Run All Cells**.

### Running via Terminal:
Execute any script directly:
```bash
python Exp_1_Vacuum_Cleaner_Agent/exp1_vacuum_agent.py
python Exp_2_Utility_Vacuum_Cleaner/exp2_utility_vacuum.py
python Exp_3_Graph_Representation_BFS_DFS_Dijkstra/exp3_graph_searches.py
python Exp_4_Informed_Search_BestFirst_AStar/exp4_informed_search.py
python Exp_5_Local_Search_HillClimbing_SimulatedAnnealing/exp5_local_search.py
python Exp_6_Adversarial_Search_TicTacToe_Minimax/exp6_tictactoe_minimax.py
python Exp_7_Connect3_Minimax_AlphaBeta_Pruning/exp7_connect3_alphabeta.py
python Exp_8_Wumpus_World_Rule_Based_Agent/exp8_wumpus_world.py
python Exp_9_Propositional_Logic_Engine_and_Wumpus/exp9_propositional_logic_wumpus.py
```

