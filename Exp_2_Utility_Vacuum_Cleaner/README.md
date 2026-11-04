# Experiment 2: Utility-Based Vacuum Cleaner Agent ($m \times n$ Grid)

## 1. Overview & Objective
This experiment implements a **Utility-Based Intelligent Agent** operating in an $m \times n$ 2D grid environment. The lab explores two paradigms:
1. **Fully Observable World**: The agent has complete and accurate visibility over the entire grid's state at all times. It can compute exact distances to dirty cells using Breadth-First Search (BFS) and evaluate precise expected utilities.
2. **Partially Observable World**: The agent only knows the status of cells it has directly visited, maintaining an internal belief state and balancing dirt cleanup with exploratory navigation.

### Performance Metrics Tracked:
- Total Steps Executed
- Total Vacuum Actions
- Total Moves
- Total Energy Consumed (Movement = 1 unit, Vacuuming = 2 units)
- Theoretical Minimum Steps (Lower bound)
- Optimality Ratio ($\text{Actual Steps} / \text{Theoretical Minimum}$)

---

## 2. Mathematical Utility Function
For a candidate action $a \in \{\text{vacuum}, \text{Up}, \text{Down}, \text{Left}, \text{Right}\}$:
$$U(a) = \text{VacuumReward}(a) - \text{DistanceToNearestDirty}(a) - \text{MovementCost}(a) + \text{DirtDensityNearby}(a)$$

Where:
- $\text{VacuumReward}(a)$: Large positive reward (+10) if $a = \text{'vacuum'}$ and the current cell is dirty; $-5$ otherwise.
- $\text{DistanceToNearestDirty}(a)$: BFS shortest-path distance from the resulting position to the nearest remaining dirty cell (0 if no dirt remains).
- $\text{MovementCost}(a)$: 1 if $a$ is a directional move, 0 if $a = \text{'vacuum'}$.
- $\text{DirtDensityNearby}(a)$: Number of dirty cells located within a Chebyshev neighborhood (radius $\le 1$) of the resulting position, incentivizing movement toward clusters of dirt.

---

## 3. Detailed Function Documentation

Here is the complete reference for every function implemented in `exp2_utility_vacuum.py`:

### `create_environment(rows, cols)`
- **Purpose**: Initializes an $m \times n$ 2D grid matrix of zeros (Clean).
- **Parameters**: 
  - `rows` (`int`): Number of rows.
  - `cols` (`int`): Number of columns.
- **Returns**: A 2D list of dimensions `rows x cols` with value `0`.

### `place_dirt(env, dirt_prob=0.4)`
- **Purpose**: Randomly distributes dirt (`1`) across cells according to probability `dirt_prob`.
- **Parameters**:
  - `env` (`list[list[int]]`): Environment grid.
  - `dirt_prob` (`float`): Probability of each cell containing dirt.
- **Returns**: Populated `env` grid with guaranteed dirt.

### `place_agent(rows, cols)`
- **Purpose**: Selects random coordinates $(r, c)$ for the agent's start position.
- **Parameters**: `rows`, `cols`.
- **Returns**: Tuple `(r, c)`.

### `is_dirty(env, pos)`
- **Purpose**: Checks if cell at $(r, c)$ is dirty (`1`).
- **Parameters**: `env`, `pos` (`tuple[int, int]`).
- **Returns**: Boolean `True` if dirty, `False` otherwise.

### `vacuum(env, pos)`
- **Purpose**: Cleans the cell at `pos` by setting `env[r][c] = 0`.
- **Parameters**: `env`, `pos`.
- **Returns**: Updated `env`.

### `get_possible_moves(pos, rows, cols)`
- **Purpose**: Generates boundary-constrained valid directional moves.
- **Parameters**: `pos`, `rows`, `cols`.
- **Returns**: Dictionary mapping valid action name (`'Up'`, `'Down'`, `'Left'`, `'Right'`) to resulting coordinate `(nr, nc)`.

### `find_nearest_dirty_cell(env, pos, rows, cols)`
- **Purpose**: Executes a Breadth-First Search (BFS) to compute the exact shortest-path distance from `pos` to the closest dirty cell.
- **Parameters**: `env`, `pos`, `rows`, `cols`.
- **Returns**: Tuple `(nearest_dirty_pos, distance)`. If no dirt exists, returns `(None, 0)`.

### `get_dirt_density_nearby(env, pos, rows, cols, radius=1)`
- **Purpose**: Evaluates local dirt concentration within Chebyshev radius of `pos`.
- **Parameters**: `env`, `pos`, `rows`, `cols`, `radius`.
- **Returns**: Integer count of dirty cells.

### `compute_utility(action, pos, env, rows, cols)`
- **Purpose**: Evaluates the utility formula $U(a)$ for a specific candidate action.
- **Parameters**: `action` (`str`), `pos`, `env`, `rows`, `cols`.
- **Returns**: Float/integer utility score.

### `choose_best_action(pos, env, rows, cols)`
- **Purpose**: Determines candidate actions and selects the one with maximal utility.
- **Parameters**: `pos`, `env`, `rows`, `cols`.
- **Returns**: Tuple `(best_action, best_utility)`.

### `all_clean(env)`
- **Purpose**: Evaluates termination condition (all cells `0`).
- **Parameters**: `env`.
- **Returns**: `True` if all cells are clean, else `False`.

### `compute_theoretical_minimum(env, start_pos, rows, cols)`
- **Purpose**: Computes theoretical lower-bound on steps (sum of dirt count + max distance from start to any dirty cell).
- **Parameters**: `env`, `start_pos`, `rows`, `cols`.
- **Returns**: Integer minimum step estimate.

### `update_metrics(metrics, action_taken)`
- **Purpose**: Updates performance tracker (steps, vacuums, moves, energy).
- **Parameters**: `metrics` (`dict`), `action_taken` (`str`).
- **Returns**: Updated `metrics` dictionary.

### `display_environment(env, agent_pos, action, step, rows, cols)`
- **Purpose**: Visualizes grid state with agent marker `[A(Action),Status]` and surrounding cells.
- **Parameters**: `env`, `agent_pos`, `action`, `step`, `rows`, `cols`.
- **Returns**: `None`.

### `display_performance_summary(metrics)`
- **Purpose**: Prints summary of steps, energy consumption, and optimality ratio.
- **Parameters**: `metrics` (`dict`).
- **Returns**: `None`.

### `run_vacuum_world(rows, cols, max_iterations)`
- **Purpose**: Main simulation loop for fully observable utility agent.
- **Parameters**: `rows`, `cols`, `max_iterations`.
- **Returns**: `None`.

### `run_partially_observable_utility_agent(rows, cols, max_iterations)`
- **Purpose**: Simulation loop for partially observable agent utilizing an internal belief state to balance exploration and cleaning.
- **Parameters**: `rows`, `cols`, `max_iterations`.
- **Returns**: `None`.

---

## 4. How to Run
### In Terminal / Command Prompt:
```bash
python exp2_utility_vacuum.py
```

### In JupyterLab:
Open `exp2_utility_vacuum.ipynb` and select **Run All Cells**.

