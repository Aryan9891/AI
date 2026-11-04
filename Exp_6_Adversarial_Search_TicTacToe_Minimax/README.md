# Experiment 6: Adversarial Search (Tic-Tac-Toe & Minimax)

## 1. Overview & Objective
This experiment implements the classic **Minimax Adversarial Search Algorithm** in the context of the game of Tic-Tac-Toe with a Line User Interface (LUI):
1. **Part 1: Two-Player Human Game**:
   - Allows two human players to share the terminal.
   - Robust input handling: rejects out-of-range values or already occupied squares without crashing.
   - Instant win and draw detection.
2. **Part 2: Minimax AI Agent**:
   - Computes moves by recursively searching the entire game tree.
   - Operates with depth-discounted scoring to prefer faster victories and delay defeats.
   - Guarantees the AI never loses (optimal game-theoretic play).

---

## 2. Minimax Mathematical Formulation
For a game state $s$, the minimax value is defined recursively:
$$\text{Minimax}(s) = \begin{cases} 
\text{Utility}(s) & \text{if } \text{Terminal}(s) \\
\max_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a)) & \text{if } \text{Player}(s) = \text{MAX (AI)} \\
\min_{a \in \text{Actions}(s)} \text{Minimax}(\text{Result}(s, a)) & \text{if } \text{Player}(s) = \text{MIN (Human)}
\end{cases}$$

With depth penalty:
- AI Win: $+10 - \text{depth}$
- Human Win: $\text{depth} - 10$
- Draw: $0$

---

## 3. Detailed Function Documentation

Here is the complete reference of every function in `exp6_tictactoe_minimax.py`:

### `create_board()`
- **Purpose**: Creates a list of 9 blank spaces representing the initial empty $3 \times 3$ grid.
- **Parameters**: None.
- **Returns**: `list[str]` of length 9: `[' ', ' ', ..., ' ']`.

### `display_board(board)`
- **Purpose**: Formats the board. Empty squares display their 1-based index (1-9), while occupied squares show `X` or `O`.
- **Parameters**: `board` (`list[str]`).
- **Returns**: `None`.

### `check_winner(board)`
- **Purpose**: Evaluates rows, columns, and diagonals for 3-in-a-row alignment or board saturation.
- **Parameters**: `board` (`list[str]`).
- **Returns**: `'X'`, `'O'`, `'Draw'`, or `None` (if game is still ongoing).

### `is_valid_move(board, move)`
- **Purpose**: Validates that `move` is an integer in $[1, 9]$ and the square is unassigned (`' '`).
- **Parameters**: `board`, `move` (`int`).
- **Returns**: `bool`.

### `minimax(board, depth, is_maximizing, ai_player='O', human_player='X')`
- **Purpose**: Recursive adversarial search exploring all possible game trajectories to return the optimal game-theoretic evaluation score and best move index.
- **Parameters**:
  - `board` (`list[str]`): Current state.
  - `depth` (`int`): Current tree depth.
  - `is_maximizing` (`bool`): `True` if it is AI's turn, `False` for human's turn.
  - `ai_player` (`str`): Marker for AI (`'O'`).
  - `human_player` (`str`): Marker for Human (`'X'`).
- **Returns**: Tuple `(best_score, best_move_index)`.

### `get_computer_move(board, ai_player='O', human_player='X')`
- **Purpose**: Wrapper calling `minimax(...)` from depth 0 and returning the chosen square index (1-based, 1 to 9).
- **Parameters**: `board`, `ai_player`, `human_player`.
- **Returns**: Integer in $[1, 9]$.

### `play_two_player()`
- **Purpose**: Interactive terminal loop for two human players alternating turns.
- **Returns**: `None`.

### `play_against_ai(preset_inputs=None)`
- **Purpose**: Interactive game loop against the Minimax agent. Accepts optional `preset_inputs` for automated demonstration and testing without interactive blocking.
- **Returns**: `None`.

### `run_demo()`
- **Purpose**: Automatically plays the exact sample move trace featured in the lab manual (`y -> 1 -> 9 -> 4`), producing the identical terminal log.
- **Returns**: `None`.

---

## 4. How to Run
### In Terminal:
```bash
python exp6_tictactoe_minimax.py
```

### In JupyterLab:
Open `exp6_tictactoe_minimax.ipynb` and run all cells.

