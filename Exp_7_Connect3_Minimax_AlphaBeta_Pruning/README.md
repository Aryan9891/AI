# Experiment 7: Connect-3 on a 4×4 Board (Minimax vs. Alpha–Beta Pruning)

## 1. Overview & Objective
This experiment implements the game of **Connect-3** played on a $4 \times 4$ board (16 cells total) under two search algorithms:
1. **Plain Minimax Search**: Exhaustively visits game tree states.
2. **Minimax with Alpha–Beta Pruning**: Prunes branches that cannot influence the final decision, dramatically cutting down the state space.

### Game Rules:
- **Board**: 4 columns $\times$ 4 rows (16 cells). Empty cells are represented by `-`.
- **Turns**: Two players, Human (`X`) and AI (`O`), move alternately. `X` moves first.
- **Gravity**: A move is a choice of column $[1, 4]$. The piece drops to the lowest unoccupied cell in that column. Full columns are invalid.
- **Winning Condition**: First player to form an uninterrupted line of 3 identical pieces horizontally, vertically, or diagonally wins immediately.
- **Draw**: All 16 cells are filled with no player achieving a 3-in-a-row.

---

## 2. Theoretical Principles: Alpha–Beta Pruning
Alpha–Beta pruning maintains two bounds during recursive exploration:
- $\alpha$: The best (maximum) value that the MAX player is guaranteed so far.
- $\beta$: The best (minimum) value that the MIN player is guaranteed so far.

Whenever a branch yields a condition where:
$$\beta \le \alpha$$
The current node's parent would never select this path. The remaining child branches are **pruned**, saving enormous numbers of recursive function calls without any loss in optimality.

---

## 3. Detailed Function Documentation

Here is the complete reference of every function in `exp7_connect3_alphabeta.py`:

### `create_board()`
- **Purpose**: Instantiates a $4 \times 4$ 2D list filled with `'-'`.
- **Parameters**: None.
- **Returns**: `list[list[str]]`.

### `display_board(board)`
- **Purpose**: Prints the board formatted as a Markdown table with column headers `| 1 | 2 | 3 | 4 |`.
- **Parameters**: `board` (`list[list[str]]`).
- **Returns**: `None`.

### `get_lowest_empty_row(board, col)`
- **Purpose**: Simulates gravity: scans column `col` from bottom (row 3) to top (row 0) and returns the first row containing `'-'`. If full, returns -1.
- **Parameters**: `board`, `col` (`int`).
- **Returns**: Integer row index $[0, 3]$ or $-1$.

### `is_valid_column(board, col)`
- **Purpose**: Checks whether column `col` is within boundaries and has space available.
- **Parameters**: `board`, `col`.
- **Returns**: `bool`.

### `check_win(board, player)`
- **Purpose**: Detects horizontal, vertical, and diagonal triplets for `player`.
- **Parameters**: `board`, `player` (`'X'` or `'O'`).
- **Returns**: `True` if winning line exists, else `False`.

### `is_board_full(board)`
- **Purpose**: Checks whether all 16 cells are occupied.
- **Parameters**: `board`.
- **Returns**: `bool`.

### `minimax(board, depth, is_maximizing, max_depth=7)`
- **Purpose**: Plain minimax search without pruning. Increments `minimax_search_count` at every call.
- **Parameters**: `board`, `depth`, `is_maximizing`, `max_depth`.
- **Returns**: Evaluation score (`int`).

### `get_best_move_minimax(board, max_depth=7)`
- **Purpose**: Evaluates each legal column using `minimax(...)` and returns column index with highest score.
- **Parameters**: `board`, `max_depth`.
- **Returns**: Selected column index $[0, 3]$.

### `alphabeta(board, depth, alpha, beta, is_maximizing, max_depth=7)`
- **Purpose**: Minimax search enhanced with alpha-beta cutoff conditions. Increments `alphabeta_search_count`.
- **Parameters**: `board`, `depth`, `alpha`, `beta`, `is_maximizing`, `max_depth`.
- **Returns**: Evaluation score (`int`).

### `get_best_move_alphabeta(board, max_depth=7)`
- **Purpose**: Evaluates legal columns using `alphabeta(...)` with dynamic $[\alpha, \beta]$ updating.
- **Parameters**: `board`, `max_depth`.
- **Returns**: Selected column index $[0, 3]$.

### `play_connect3(algorithm="alphabeta", preset_moves=None, max_depth=7)`
- **Purpose**: Full match driver managing alternating turns, input, board display, and winner announcement.
- **Parameters**: `algorithm` (`"minimax"` or `"alphabeta"`), `preset_moves`, `max_depth`.
- **Returns**: `None`.

### `run_experiment()`
- **Purpose**: Replays the benchmark game from the lab sheet under both Plain Minimax and Alpha–Beta Pruning, printing the comparison metrics and pruning efficiency percentage.
- **Returns**: `None`.

---

## 4. Benchmark Comparison

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

Alpha–Beta pruning reduces over **95%** of node evaluations while choosing the exact identical game-theoretic optimal moves.

---

## 5. How to Run
### In Terminal:
```bash
python exp7_connect3_alphabeta.py
```

### In JupyterLab:
Open `exp7_connect3_alphabeta.ipynb` and run all cells.

