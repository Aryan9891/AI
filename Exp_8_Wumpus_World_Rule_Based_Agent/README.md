# Experiment 8: Knowledge-Based Rule Agent for Wumpus World

## 1. Overview & Objective
This experiment implements a **Knowledge-Based Rule Agent** exploring the **Wumpus World** without any initial map knowledge:
- **Environment**: $N \times N$ discrete grid (default $4 \times 4$), 1-indexed coordinates $(x, y)$ where $(1, 1)$ is the bottom-left starting cell.
- **Hazards & Goals**:
  - One Wumpus (never at $(1, 1)$), can co-exist with a pit.
  - Pits distributed with probability $p = 0.2$ (except $(1, 1)$).
  - One Gold piece in a safe cell (no pit, no Wumpus).
- **Percepts**:
  - `Stench`: Wumpus in orthogonal adjacent cell (dead Wumpus still emits stench).
  - `Breeze`: Pit in orthogonal adjacent cell.
  - `Glitter`: Gold in current cell.
  - `Scream`: Wumpus was just killed by arrow.
- **Safety Criterion**:
  - A cell is safe **iff** it is in `PitFree` **and** (`WumpusDead` or not in `WumpusCandidates`).
  - Killing the Wumpus does **not** make its cell pit-free!

---

## 2. Rule-Based Deduction Logic
1. **`PitFree` Tracking**:
   - Initialized to `{(1, 1)}`.
   - If current cell has **no Breeze**, all of its adjacent neighbors are added to `PitFree`.
2. **`WumpusCandidates` Tracking**:
   - Initialized to all cells except $(1, 1)$.
   - If current cell has **no Stench**, remove cell and its neighbors from `WumpusCandidates`.
   - If current cell has **Stench**, intersect `WumpusCandidates` with neighbors of current cell.
   - If arrow flies through a line of cells without triggering a `Scream`, those cells are removed from `WumpusCandidates`.
   - A `Scream` sets `WumpusDead = True`.
3. **Navigation**:
   - When multiple safe cells exist, the agent uses Breadth-First Search (BFS) through visited/safe cells to plan the shortest safe route.
   - If no safe cell is reachable and arrow is available, shoots towards candidate cells.
   - If no safe cell can be proven, terminates reporting `NOT POSSIBLE`.

---

## 3. Function Documentation

Here is the complete reference of every class and function in `exp8_wumpus_world.py`:

### Class `WumpusWorld`
- `__init__(self, n, wumpus_pos, pits, gold_pos, p, seed)`: Initializes grid, sets hazards and gold.
- `get_neighbors(self, pos)`: Returns orthogonal adjacent coordinates within grid bounds.
- `sense_percepts(self, pos, just_screamed)`: Evaluates `Stench`, `Breeze`, `Glitter`, and `Scream` at `pos`.
- `shoot_arrow(self, pos, direction)`: Propagates arrow along row/column; returns `True` if it hits the Wumpus.
- `print_true_map(self)`: Displays complete ground truth map with legend ($A, W, P, G, W+P, \cdot$).

### Class `RuleBasedAgent`
- `__init__(self, n)`: Initializes beliefs (`visited`, `pit_free`, `wumpus_candidates`, `wumpus_dead`).
- `is_safe(self, cell)`: Returns `True` iff `cell in pit_free` and (`wumpus_dead` or `cell not in wumpus_candidates`).
- `update_beliefs(self, percepts)`: Implements knowledge-base deduction from incoming percepts.
- `find_path_to_target(self, target)`: Executes BFS over safe cells to compute shortest path.
- `run(self, world)`: Main loop executing Glitter check, safe navigation, arrow firing, and termination.

### Helper & Driver Functions
- `run_test_case(test_num, n, wumpus_pos, pits, gold_pos)`: Runs a full simulated world test case and logs traces.
- `run_experiment()`: Replays Test 1, Test 2, and Test 3 from the lab assignment sheet.

---

## 4. Test Case Results

### Test Case 1: Standard Search
- Wumpus at $(1, 3)$, Gold at $(2, 3)$, Pits at $(3, 1), (3, 3), (4, 4)$.
- **Verdict**: `POSSIBLE`
- **Shortest Safe Path**: $(1, 1) \to (1, 2) \to (2, 2) \to (2, 3)$

### Test Case 2: Arrow Shot & Scream
- Wumpus at $(2, 1)$, Gold at $(3, 2)$, Pits at $(3, 3), (4, 1)$.
- **Action**: `SHOOT_RIGHT` triggers `Scream`, clearing $(2, 1)$ of Wumpus threat.
- **Verdict**: `POSSIBLE`
- **Shortest Safe Path**: $(1, 1) \to (1, 2) \to (2, 2) \to (3, 2)$

### Test Case 3: Blocked by Pit + Wumpus
- Co-located Wumpus and Pit at $(2, 1)$, Gold at $(4, 4)$.
- Even though arrow kills Wumpus, the cell remains unsafe due to the Pit.
- **Verdict**: `NOT POSSIBLE`

---

## 5. How to Run
### In Terminal:
```bash
python exp8_wumpus_world.py
```

### In JupyterLab:
Open `exp8_wumpus_world.ipynb` and run all cells.

