# Experiment 1: Vacuum Cleaner World Agent (2×1 Grid)

## 1. Overview & Objective
This experiment implements a **Function-Based (No Classes)** Intelligent Vacuum Cleaner World Agent operating in a $2 \times 1$ grid environment. 

### Key Characteristics:
- **Environment**: A $2 \times 1$ discrete grid where each cell is either Clean (`0`) or Dirty (`1`). This represents the ground truth, hidden state.
- **Partially Observable**: The agent does not have access to the full environment state initially. It maintains its own internal **knowledge array** initialized to unknown values (`None` / `?`).
- **Perception-Driven**: The agent only discovers whether a cell is clean or dirty when it physically visits and perceives that specific cell.
- **Rational Actions**:
  - If the current cell is **dirty**, the agent **must vacuum** it before it is permitted to move.
  - If the current cell is **clean**, the agent chooses a valid move (**Left** or **Right**) within grid boundaries.
- **Agent-Centric Termination**: Stopping condition strictly depends on the agent's *own knowledge* confirming all cells are clean (or reaching a maximum step threshold). The agent never peeks into the hidden environment to decide whether to stop.

---

## 2. Visual Notation
The console output strictly follows the lab specification notation:
- `D`: Dirty cell (known to agent)
- `C`: Clean cell (known to agent)
- `?`: Unknown cell (agent has not yet visited or perceived it)
- `V`: Agent just vacuumed this cell
- `A()`: Agent present, no action taken this step (just perceiving/starting)
- `A(R)` / `A(L)`: Agent present, decided to move Right / Left

**Example output:**
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
```

---

## 3. Detailed Function Documentation

Here is the exhaustive breakdown of every function used in `exp1_vacuum_agent.py`:

### `create_environment()`
- **Purpose**: Creates and initializes the $2 \times 1$ environment array.
- **Parameters**: None.
- **Returns**: A list of length 2 `[0, 0]`.

### `place_dirt(env)`
- **Purpose**: Randomly places dirt in the environment cells.
- **Parameters**: 
  - `env` (`list`): The environment state list.
- **Returns**: Updated `env` list where each cell is randomly assigned `0` (Clean) or `1` (Dirty). Guarantees at least one dirty cell for simulation.

### `place_agent(grid_size=2)`
- **Purpose**: Randomly chooses a starting index for the vacuum cleaner agent.
- **Parameters**: 
  - `grid_size` (`int`, optional): Size of the grid. Default is 2.
- **Returns**: Integer index (0 or 1).

### `create_knowledge(grid_size=2)`
- **Purpose**: Initializes the agent's internal belief state where every cell is unknown (`None`).
- **Parameters**: 
  - `grid_size` (`int`, optional): Size of the grid. Default is 2.
- **Returns**: A list of length `grid_size` filled with `None` values (e.g. `[None, None]`).

### `perceive(env, knowledge, pos)`
- **Purpose**: Simulates the agent's sensor reading the true status of the current cell and updating its knowledge.
- **Parameters**:
  - `env` (`list`): The true hidden environment.
  - `knowledge` (`list`): The agent's current knowledge array.
  - `pos` (`int`): The current index of the agent.
- **Returns**: Updated `knowledge` list.

### `is_dirty(env, pos)`
- **Purpose**: Checks whether the cell at `pos` contains dirt.
- **Parameters**:
  - `env` (`list`): The environment state.
  - `pos` (`int`): Cell index.
- **Returns**: `True` if `env[pos] == 1`, else `False`.

### `vacuum(env, knowledge, pos)`
- **Purpose**: Actuator action: cleans the current cell in the physical environment and simultaneously updates the agent's knowledge to `0` (Clean).
- **Parameters**:
  - `env` (`list`): The physical environment.
  - `knowledge` (`list`): The agent's knowledge array.
  - `pos` (`int`): Agent's current position.
- **Returns**: Tuple `(env, knowledge)`.

### `get_possible_moves(pos, grid_size=2)`
- **Purpose**: Determines valid navigational actions from the current cell based on boundary constraints.
- **Parameters**:
  - `pos` (`int`): Current cell index.
  - `grid_size` (`int`): Total number of cells.
- **Returns**: List of strings containing valid directions (e.g., `['Right']` if at index 0, `['Left']` if at index 1).

### `move_agent(pos, grid_size=2)`
- **Purpose**: Selects a valid move and computes the new cell position.
- **Parameters**:
  - `pos` (`int`): Current position.
  - `grid_size` (`int`): Grid size.
- **Returns**: Tuple `(new_pos, direction_moved)` (e.g., `(1, 'Right')`).

### `knowledge_all_clean(knowledge)`
- **Purpose**: Checks if the agent believes all cells are clean. If any cell is still unknown (`None`) or dirty (`1`), returns `False`.
- **Parameters**:
  - `knowledge` (`list`): Agent's belief state.
- **Returns**: `True` if all cells are `0`, `False` otherwise.

### `all_clean(env)`
- **Purpose**: Ground-truth check used exclusively for debugging/logging, never for agent decision-making.
- **Parameters**:
  - `env` (`list`): True environment.
- **Returns**: `True` if all cells in `env` are 0.

### `display_environment(knowledge, agent_pos, action, step)`
- **Purpose**: Formats and prints the exact visual state of the grid according to the notation rules.
- **Parameters**:
  - `knowledge` (`list`): Knowledge array.
  - `agent_pos` (`int`): Current position index of agent.
  - `action` (`str`): Action performed in this step (`'perceive'`, `'vacuum'`, `'move_Right'`, `'move_Left'`).
  - `step` (`int`): Step counter (0 = Initial Stage, >=1 = Run $k$).
- **Returns**: `None` (prints to stdout).

### `run_vacuum_world(max_iterations=20)`
- **Purpose**: Main driver function that ties together environment creation, perception, agent action loop, display, and stopping conditions.
- **Parameters**:
  - `max_iterations` (`int`): Safety upper bound on loop execution.
- **Returns**: `None`.

### `run_vacuum_world_generalized(grid_size=4, max_iterations=50)`
- **Purpose**: Extension addressing Experiment 2 (scaling from $2 \times 1$ to arbitrary $N \times 1$ grid).
- **Parameters**:
  - `grid_size` (`int`): Length of linear grid.
  - `max_iterations` (`int`): Maximum allowed simulation steps.
- **Returns**: `None`.

---

## 4. How to Run
### In Terminal / Command Prompt:
```bash
python exp1_vacuum_agent.py
```

### In JupyterLab:
Open `exp1_vacuum_agent.ipynb` and select **Run All Cells**.

