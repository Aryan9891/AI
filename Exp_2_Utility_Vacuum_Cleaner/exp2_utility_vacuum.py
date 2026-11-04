"""
Artificial Intelligence Lab - LAB 02
Design a Utility-Based Vacuum Cleaner Agent (m x n Grid) with Performance Metrics
Includes:
1. Fully Observable World with exact BFS utility calculation
2. Partially Observable World with belief-state utility calculation
Author: Aryan Sachin
"""

import random
from collections import deque

# 1. create_environment(rows, cols)
def create_environment(rows, cols):
    """Creates a 2D matrix (rows x cols) filled with 0 (Clean)."""
    return [[0 for _ in range(cols)] for _ in range(rows)]

# 2. place_dirt(env, dirt_prob=0.4)
def place_dirt(env, dirt_prob=0.4):
    """Randomly sets cells to 1 (Dirty) based on dirt_prob."""
    rows, cols = len(env), len(env[0])
    dirt_count = 0
    for r in range(rows):
        for c in range(cols):
            if random.random() < dirt_prob:
                env[r][c] = 1
                dirt_count += 1
    # Ensure at least two dirty cells for meaningful evaluation
    if dirt_count == 0:
        env[0][0] = 1
        env[rows - 1][cols - 1] = 1
    return env

# 3. place_agent(rows, cols)
def place_agent(rows, cols):
    """Randomly places the agent at a starting (row, col) position."""
    return (random.randint(0, rows - 1), random.randint(0, cols - 1))

# 4. is_dirty(env, pos)
def is_dirty(env, pos):
    """Checks whether cell at (r, c) is dirty (1)."""
    r, c = pos
    return env[r][c] == 1

# 5. vacuum(env, pos)
def vacuum(env, pos):
    """Cleans the cell at position pos."""
    r, c = pos
    env[r][c] = 0
    return env

# 6. get_possible_moves(pos, rows, cols)
def get_possible_moves(pos, rows, cols):
    """
    Returns valid directional moves from pos: Up, Down, Left, Right
    as dictionary mapping action string to resulting (r, c).
    """
    r, c = pos
    moves = {}
    if r > 0:
        moves['Up'] = (r - 1, c)
    if r < rows - 1:
        moves['Down'] = (r + 1, c)
    if c > 0:
        moves['Left'] = (r, c - 1)
    if c < cols - 1:
        moves['Right'] = (r, c + 1)
    return moves

# 7. find_nearest_dirty_cell(env, pos, rows, cols)
def find_nearest_dirty_cell(env, pos, rows, cols):
    """
    Uses BFS shortest-path search over the grid to locate the nearest dirty cell
    and the distance to it. Returns (target_pos, distance).
    """
    if is_dirty(env, pos):
        return pos, 0

    queue = deque([(pos[0], pos[1], 0)])
    visited = {pos}

    while queue:
        r, c, dist = queue.popleft()
        if env[r][c] == 1:
            return (r, c), dist

        for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))

    return None, 0

# Helper: Count dirty cells within radius
def get_dirt_density_nearby(env, pos, rows, cols, radius=1):
    """Counts number of dirty cells within Chebyshev radius of pos."""
    r, c = pos
    density = 0
    for dr in range(-radius, radius + 1):
        for dc in range(-radius, radius + 1):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if env[nr][nc] == 1:
                    density += 1
    return density

# 8. compute_utility(action, pos, env, rows, cols)
def compute_utility(action, pos, env, rows, cols):
    """
    Formula:
    U(a) = VacuumReward(a) - DistanceToNearestDirty(a) - MovementCost(a) + DirtDensityNearby(a)
    """
    if action == 'vacuum':
        resulting_pos = pos
        vacuum_reward = 10 if is_dirty(env, pos) else -5
        movement_cost = 0
    else:
        # action is a move: 'Up', 'Down', 'Left', 'Right'
        moves = get_possible_moves(pos, rows, cols)
        resulting_pos = moves[action]
        vacuum_reward = 0
        movement_cost = 1

    _, dist_to_dirty = find_nearest_dirty_cell(env, resulting_pos, rows, cols)
    density = get_dirt_density_nearby(env, resulting_pos, rows, cols, radius=1)

    utility = vacuum_reward - dist_to_dirty - movement_cost + density
    return utility

# 9. choose_best_action(pos, env, rows, cols)
def choose_best_action(pos, env, rows, cols):
    """
    Evaluates candidate actions (vacuum if dirty, plus all valid directional moves)
    and selects the action with maximum utility.
    """
    candidate_actions = []

    # Mandatory rule: If current cell is dirty, vacuuming is highly prioritized
    if is_dirty(env, pos):
        candidate_actions.append('vacuum')
    else:
        moves = get_possible_moves(pos, rows, cols)
        candidate_actions.extend(moves.keys())

    if not candidate_actions:
        return None

    best_action = None
    best_utility = float('-inf')

    for a in candidate_actions:
        u = compute_utility(a, pos, env, rows, cols)
        if u > best_utility:
            best_utility = u
            best_action = a

    return best_action, best_utility

# 10. all_clean(env)
def all_clean(env):
    """Checks if all cells in grid are clean (0)."""
    return all(cell == 0 for row in env for cell in row)

# 11. compute_theoretical_minimum(env, start_pos, rows, cols)
def compute_theoretical_minimum(env, start_pos, rows, cols):
    """
    Estimates minimum actions needed:
    Total dirty cells to vacuum + Manhattan distance or MST distance to visit all dirty cells.
    """
    dirty_cells = [(r, c) for r in range(rows) for c in range(cols) if env[r][c] == 1]
    if not dirty_cells:
        return 0
    # Minimum steps = number of vacuums + minimum path length
    # A simple lower bound is total dirt + max distance from start to any dirt
    max_dist = max(abs(start_pos[0] - r) + abs(start_pos[1] - c) for r, c in dirty_cells)
    return len(dirty_cells) + max_dist

# 12. update_metrics(metrics, action_taken)
def update_metrics(metrics, action_taken):
    """Updates performance metric tracking counters."""
    metrics['total_steps'] += 1
    if action_taken == 'vacuum':
        metrics['vacuums'] += 1
        metrics['energy_consumed'] += 2  # vacuuming costs 2 units
    else:
        metrics['moves'] += 1
        metrics['energy_consumed'] += 1  # moving costs 1 unit
    return metrics

# 13. display_environment(env, agent_pos, action, step, rows, cols)
def display_environment(env, agent_pos, action, step, rows, cols):
    """Displays the grid state with agent marker and cell statuses."""
    header = "Initial Stage:" if step == 0 else f"Step {step} (Action: {action}):"
    print(header)
    for r in range(rows):
        row_str = ""
        for c in range(cols):
            status = "D" if env[r][c] == 1 else "C"
            if (r, c) == agent_pos:
                if action == 'vacuum':
                    cell_repr = f"[A(V),{status}]"
                elif action in ['Up', 'Down', 'Left', 'Right']:
                    abbr = action[0]
                    cell_repr = f"[A({abbr}),{status}]"
                else:
                    cell_repr = f"[A(),{status}]"
            else:
                cell_repr = f"[{status}]"
            row_str += cell_repr
        print(row_str)
    print()

# 14. display_performance_summary(metrics)
def display_performance_summary(metrics):
    """Prints final summary of metrics and optimality ratio."""
    print("=" * 45)
    print("        PERFORMANCE SUMMARY REPORT")
    print("=" * 45)
    print(f"Total Steps Executed:      {metrics['total_steps']}")
    print(f"Total Clean/Vacuum Actions:{metrics['vacuums']}")
    print(f"Total Movement Steps:      {metrics['moves']}")
    print(f"Total Energy Consumed:     {metrics['energy_consumed']} units")
    print(f"Theoretical Min Steps:     {metrics['theoretical_min']}")
    if metrics['theoretical_min'] > 0:
        ratio = metrics['total_steps'] / metrics['theoretical_min']
        print(f"Optimality Ratio:          {ratio:.2f} (Actual / Theoretical)")
    print("=" * 45)

# 15. run_vacuum_world(rows, cols) - Fully Observable Mode
def run_vacuum_world(rows=3, cols=3, max_iterations=50):
    print(f"\n=======================================================")
    print(f" EXPERIMENT 2: Fully Observable Utility Vacuum ({rows}x{cols})")
    print(f"=======================================================\n")
    
    env = create_environment(rows, cols)
    env = place_dirt(env, dirt_prob=0.35)
    agent_pos = place_agent(rows, cols)

    metrics = {
        'total_steps': 0,
        'vacuums': 0,
        'moves': 0,
        'energy_consumed': 0,
        'theoretical_min': compute_theoretical_minimum(env, agent_pos, rows, cols)
    }

    display_environment(env, agent_pos, "None", 0, rows, cols)

    step = 0
    while not all_clean(env) and step < max_iterations:
        step += 1
        best_act, util = choose_best_action(agent_pos, env, rows, cols)

        if best_act == 'vacuum':
            vacuum(env, agent_pos)
            update_metrics(metrics, 'vacuum')
            display_environment(env, agent_pos, 'vacuum', step, rows, cols)
        else:
            moves = get_possible_moves(agent_pos, rows, cols)
            agent_pos = moves[best_act]
            update_metrics(metrics, best_act)
            display_environment(env, agent_pos, best_act, step, rows, cols)

    if all_clean(env):
        print("Success: All cells in grid are clean! Task Completed.")
    else:
        print("Stopped: Maximum iterations reached.")

    display_performance_summary(metrics)


# Partially Observable Utility Vacuum Extension (Belief State)
def run_partially_observable_utility_agent(rows=3, cols=3, max_iterations=60):
    print(f"\n=======================================================")
    print(f" Partially Observable Utility-Based Agent ({rows}x{cols})")
    print(f"=======================================================\n")

    env = create_environment(rows, cols)
    env = place_dirt(env, dirt_prob=0.35)
    agent_pos = place_agent(rows, cols)
    knowledge = [[None for _ in range(cols)] for _ in range(rows)]

    # Perceive starting cell
    r, c = agent_pos
    knowledge[r][c] = env[r][c]

    step = 0
    print(f"Initial State - Agent at {agent_pos}:")

    def belief_all_clean(k):
        return all(cell == 0 for row in k for cell in row if cell is not None) and \
               all(cell is not None for row in k for cell in row)

    while not belief_all_clean(knowledge) and step < max_iterations:
        step += 1
        r, c = agent_pos
        knowledge[r][c] = env[r][c]

        if knowledge[r][c] == 1:
            vacuum(env, agent_pos)
            knowledge[r][c] = 0
            action = 'vacuum'
        else:
            # Move towards nearest unvisited cell or known dirty cell
            moves = get_possible_moves(agent_pos, rows, cols)
            # Preference: move to unknown cells ('?') or dirty cells ('D')
            best_move = None
            best_score = float('-inf')
            for act, npos in moves.items():
                nr, nc = npos
                score = 0
                if knowledge[nr][nc] is None:
                    score += 5  # Exploration reward
                elif knowledge[nr][nc] == 1:
                    score += 10 # Known dirt
                else:
                    score -= 1  # Already clean
                if score > best_score:
                    best_score = score
                    best_move = act
            if best_move is None:
                best_move = random.choice(list(moves.keys()))
            agent_pos = moves[best_move]
            action = best_move

        # Print step
        print(f"Step {step}: Action = {action}, Agent Pos = {agent_pos}")

    print("Completed exploration & cleaning in Partially Observable World.\n")


if __name__ == "__main__":
    random.seed(42)
    run_vacuum_world(rows=3, cols=3)
    run_partially_observable_utility_agent(rows=3, cols=3)

