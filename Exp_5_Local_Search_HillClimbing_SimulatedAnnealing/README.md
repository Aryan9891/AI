# Experiment 5: Local Search Algorithms (Hill Climbing & Simulated Annealing)

## 1. Overview & Objective
This experiment examines **Local Search Algorithms** across continuous optimization and discrete constraint-satisfaction problems:
1. **Part 1: 1D Landscape Optimization**:
   - Find global maximum of the multimodal landscape:
     $$f(x) = \sin(x) + \sin\left(\frac{10x}{3}\right), \quad x \in [0, 10]$$
   - Contrast **Hill Climbing** (greedy ascent susceptible to local peaks) with **Simulated Annealing** (stochastic search capable of escaping local optima via Boltzmann acceptance $P = e^{\Delta E / T}$).
   - Graph the objective function and plot the exact step-by-step optimization traces.
2. **Part 2: 8-Queens Problem**:
   - Place 8 non-attacking queens on an $8 \times 8$ chessboard.
   - Maximize the objective function: number of non-attacking queen pairs (maximum = $\binom{8}{2} = 28$, corresponding to 0 conflicts).
   - Implement **First-Choice Hill Climbing** and **Simulated Annealing**.

---

## 2. Theoretical Principles
### Simulated Annealing Acceptance Criterion:
When considering a transition from state $s$ to neighbor $s'$ with energy difference $\Delta E = f(s') - f(s)$:
- If $\Delta E > 0$ (improving move): Accept unconditionally.
- If $\Delta E \le 0$ (worse move): Accept with probability:
  $$P(\text{accept}) = \exp\left(\frac{\Delta E}{T}\right)$$
  As temperature $T$ gradually decreases according to cooling schedule $T_{k+1} = \alpha T_k$, the probability of accepting downhill moves drops to 0, smoothly transitioning from random exploration to greedy refinement.

---

## 3. Function Documentation

Here is the exhaustive documentation for functions in `exp5_local_search.py`:

### `objective_function(x)`
- **Purpose**: Computes $f(x) = \sin(x) + \sin(10x/3)$ for a given scalar float $x$.
- **Parameters**: `x` (`float`).
- **Returns**: `float` value of $f(x)$.

### `hill_climbing_continuous(x_init=1.5, step_size=0.05, max_iter=200)`
- **Purpose**: Explores neighboring points $x \pm \delta$. Moves strictly uphill. Terminates at the first local crest.
- **Parameters**: `x_init`, `step_size`, `max_iter`.
- **Returns**: Tuple `(best_x, best_f, history)`.

### `simulated_annealing_continuous(x_init=1.5, t_init=50.0, alpha=0.995, max_iter=2000)`
- **Purpose**: Performs simulated annealing with stochastic perturbations across $[0, 10]$ and temperature-regulated probabilistic downhill acceptance.
- **Parameters**: `x_init`, `t_init`, `alpha`, `max_iter`.
- **Returns**: Tuple `(best_x, best_f, history)`.

### `visualize_continuous_optimization(hc_hist, sa_hist, save_path=None)`
- **Purpose**: Plots a side-by-side comparison of the landscape $f(x)$ with the trajectory of points visited by Hill Climbing vs. Simulated Annealing.
- **Parameters**: `hc_hist`, `sa_hist`, `save_path`.
- **Returns**: `None`.

### `get_8queens_score(state)`
- **Purpose**: Evaluates candidate board state. Counts pairs of queens that do not attack each other along rows or diagonals.
- **Parameters**: `state` (`list[int]` of length 8 where `state[c]` is queen row in column `c`).
- **Returns**: Integer between 0 and 28. (28 indicates zero conflicts).

### `get_random_neighbor_8queens(state)`
- **Purpose**: Generates a single perturbed state by randomly selecting one column and picking a different row.
- **Parameters**: `state` (`list[int]`).
- **Returns**: A new state list.

### `first_choice_hill_climbing_8queens(max_iter=1000, max_tries_per_step=100)`
- **Purpose**: Generates random neighbors one by one and accepts the *very first* neighbor that strictly improves the objective score.
- **Parameters**: `max_iter`, `max_tries_per_step`.
- **Returns**: Tuple `(current_state, current_score, score_history)`.

### `simulated_annealing_8queens(t_init=20.0, alpha=0.995, max_iter=5000)`
- **Purpose**: Implements simulated annealing on the 8-Queens configuration space, enabling escape from plateaus and local optima to achieve 28/28 non-attacking pairs.
- **Parameters**: `t_init`, `alpha`, `max_iter`.
- **Returns**: Tuple `(best_state, best_score, score_history)`.

### `print_8queens_board(state)`
- **Purpose**: Formats and prints an ASCII chessboard showing queen positions (`Q`) and empty cells (`.`) with row numbers and column labels.
- **Parameters**: `state` (`list[int]`).
- **Returns**: `None`.

### `run_experiment()`
- **Purpose**: Main benchmark driver function executing continuous optimization and 8-Queens problem.
- **Returns**: `None`.

---

## 4. Experimental Results
```
--- PART 1: 1D Landscape Optimization ---
Hill Climbing Result:       x = 2.3000, f(x) = 1.7282 (Trapped at local peak!)
Simulated Annealing Result: x = 7.9979, f(x) = 1.9887 (Found True Global Max!)

--- PART 2: 8-Queens Problem ---
First-Choice Hill Climbing: Score = 26/28 (Trapped in local optimum with 2 conflicts)
Simulated Annealing:        Score = 28/28 (Perfect solution found with 0 conflicts!)
```

---

## 5. How to Run
### In Terminal:
```bash
python exp5_local_search.py
```

### In JupyterLab:
Open `exp5_local_search.ipynb` and run all cells.

