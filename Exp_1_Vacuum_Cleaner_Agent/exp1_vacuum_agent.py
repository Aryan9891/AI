"""
Artificial Intelligence Lab - LAB 01
Experiment 1: Design a Vacuum Cleaner World Agent (2x1 Grid) using Python (Function-based, No Classes)
Author: Aryan Sachin
"""

import random

# 1. create_environment() - creates and returns the 2x1 array representing true hidden state (0 = Clean, 1 = Dirty)
def create_environment():
    return [0, 0]

# 2. place_dirt(env) - randomly places dirt (1) in cells of the grid
def place_dirt(env):
    for i in range(len(env)):
        env[i] = random.choice([0, 1])
    # Ensure at least one cell has dirt for a meaningful simulation
    if sum(env) == 0:
        env[random.randint(0, len(env) - 1)] = 1
    return env

# 3. place_agent() - randomly selects and returns a starting position (cell index) for the agent
def place_agent(grid_size=2):
    return random.randint(0, grid_size - 1)

# 4. create_knowledge() - creates and returns agent's knowledge array, starting as None (unknown)
def create_knowledge(grid_size=2):
    return [None] * grid_size

# 5. perceive(env, knowledge, pos) - lets agent sense true status of occupied cell, updating knowledge
def perceive(env, knowledge, pos):
    knowledge[pos] = env[pos]
    return knowledge

# 6. is_dirty(env, pos) - checks whether agent's current cell is actually dirty
def is_dirty(env, pos):
    return env[pos] == 1

# 7. vacuum(env, knowledge, pos) - cleans current cell in true env and updates knowledge to clean (0)
def vacuum(env, knowledge, pos):
    env[pos] = 0
    knowledge[pos] = 0
    return env, knowledge

# 8. get_possible_moves(pos, grid_size=2) - returns valid moves (Left/Right) based on boundaries
def get_possible_moves(pos, grid_size=2):
    moves = []
    if pos > 0:
        moves.append('Left')
    if pos < grid_size - 1:
        moves.append('Right')
    return moves

# 9. move_agent(pos, grid_size=2) - moves agent to randomly chosen valid neighbor, returns (new_pos, direction)
def move_agent(pos, grid_size=2):
    valid_moves = get_possible_moves(pos, grid_size)
    if not valid_moves:
        return pos, None
    direction = random.choice(valid_moves)
    new_pos = pos - 1 if direction == 'Left' else pos + 1
    return new_pos, direction

# 10. knowledge_all_clean(knowledge) - checks if agent believes all cells are clean (False if None or 1)
def knowledge_all_clean(knowledge):
    for status in knowledge:
        if status is None or status == 1:
            return False
    return True

# 11. all_clean(env) - checks true hidden environment state (for reference/debugging)
def all_clean(env):
    return all(cell == 0 for cell in env)

# 12. display_environment(knowledge, agent_pos, action, step) - prints current grid state and action
def display_environment(knowledge, agent_pos, action, step):
    """
    Formats the grid:
    D = Dirty (known)
    C = Clean (known)
    ? = Unknown
    A() = Agent present, perceiving
    A(V) = Agent vacuumed
    A(R) = Agent moving Right
    A(L) = Agent moving Left
    """
    header = f"Initial Stage:" if step == 0 else f"Run {step}:"
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
            if status is None:
                cell_repr = "[?]"
            else:
                cell_repr = f"[{status_label}]"
        cells_str += cell_repr
    print(header)
    print(cells_str)

# 13. run_vacuum_world() - main driver function running the simulation loop
def run_vacuum_world(max_iterations=20, verbose=True):
    env = create_environment()
    env = place_dirt(env)
    agent_pos = place_agent(len(env))
    knowledge = create_knowledge(len(env))

    # Initial perception
    perceive(env, knowledge, agent_pos)
    step = 0
    display_environment(knowledge, agent_pos, "perceive", step)

    while not knowledge_all_clean(knowledge) and step < max_iterations:
        step += 1
        # If current cell is dirty in agent's knowledge, vacuum it first
        if knowledge[agent_pos] == 1:
            vacuum(env, knowledge, agent_pos)
            display_environment(knowledge, agent_pos, "vacuum", step)
        else:
            # Current cell is clean, decide to move
            new_pos, direction = move_agent(agent_pos, len(env))
            action_label = f"move_{direction}"
            display_environment(knowledge, agent_pos, action_label, step)
            # Move to new position and perceive
            agent_pos = new_pos
            perceive(env, knowledge, agent_pos)
            step += 1
            display_environment(knowledge, agent_pos, "perceive", step)

    if knowledge_all_clean(knowledge):
        print("All cells are clean! Task Completed.")
    else:
        print("Maximum iterations reached without full cleaning.")
    print(f"True environment state: {env} (All clean: {all_clean(env)})\n")


# Experiment 2: Generalized Vacuum Cleaner World (Nx1 Grid)
def run_vacuum_world_generalized(grid_size=4, max_iterations=50):
    print(f"--- Experiment 2: Generalized Grid (Size {grid_size}x1) ---")
    env = [0] * grid_size
    env = place_dirt(env)
    agent_pos = place_agent(grid_size)
    knowledge = create_knowledge(grid_size)

    perceive(env, knowledge, agent_pos)
    step = 0
    display_environment(knowledge, agent_pos, "perceive", step)

    while not knowledge_all_clean(knowledge) and step < max_iterations:
        step += 1
        if knowledge[agent_pos] == 1:
            vacuum(env, knowledge, agent_pos)
            display_environment(knowledge, agent_pos, "vacuum", step)
        else:
            new_pos, direction = move_agent(agent_pos, grid_size)
            action_label = f"move_{direction}"
            display_environment(knowledge, agent_pos, action_label, step)
            agent_pos = new_pos
            perceive(env, knowledge, agent_pos)
            step += 1
            display_environment(knowledge, agent_pos, "perceive", step)

    if knowledge_all_clean(knowledge):
        print("All cells are clean! Task Completed.")
    else:
        print("Maximum iterations reached.")
    print(f"True environment state: {env}\n")


if __name__ == "__main__":
    print("=== AI Lab 01 - Vacuum Cleaner World Agent (2x1 Grid) ===")
    random.seed(42)  # For reproducible output
    run_vacuum_world()

    print("=== Generalized N-Cell Grid Run ===")
    run_vacuum_world_generalized(grid_size=4)

