"""
Artificial Intelligence Lab - LAB 08
Knowledge-Based Agents: Rule-Based Wumpus World Agent
With Safe Path Planning, Arrow Shooting, and Complete Map Visualizer
Author: Aryan Sachin
"""

import random
from collections import deque

class WumpusWorld:
    def __init__(self, n=4, wumpus_pos=None, pits=None, gold_pos=None, p=0.2, seed=None):
        self.n = n
        if seed is not None:
            random.seed(seed)

        all_cells = [(x, y) for x in range(1, n + 1) for y in range(1, n + 1) if (x, y) != (1, 1)]

        # Wumpus Placement
        if wumpus_pos is not None:
            self.wumpus_pos = wumpus_pos
        else:
            self.wumpus_pos = random.choice(all_cells)

        # Pit Placement
        if pits is not None:
            self.pits = set(pits)
        else:
            self.pits = {c for c in all_cells if random.random() < p}

        # Gold Placement (No pit and no Wumpus)
        if gold_pos is not None:
            self.gold_pos = gold_pos
        else:
            valid_gold = [c for c in all_cells if c not in self.pits and c != self.wumpus_pos]
            self.gold_pos = random.choice(valid_gold) if valid_gold else (n, n)

        self.wumpus_alive = True

    def get_neighbors(self, pos):
        x, y = pos
        nbrs = []
        # Move order preference: RIGHT, UP, LEFT, DOWN
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= self.n and 1 <= ny <= self.n:
                nbrs.append((nx, ny))
        return nbrs

    def sense_percepts(self, pos, just_screamed=False):
        nbrs = self.get_neighbors(pos)
        stench = (self.wumpus_pos in nbrs)  # Dead wumpus still smells
        breeze = any(p in nbrs for p in self.pits)
        glitter = (pos == self.gold_pos)
        percepts = []
        if stench: percepts.append("Stench")
        if breeze: percepts.append("Breeze")
        if glitter: percepts.append("Glitter")
        if just_screamed: percepts.append("Scream")
        return percepts

    def shoot_arrow(self, pos, direction):
        """Fires single arrow from pos along direction. Returns True if Wumpus is killed."""
        if not self.wumpus_alive:
            return False

        cx, cy = pos
        while True:
            if direction == 'RIGHT': cx += 1
            elif direction == 'LEFT': cx -= 1
            elif direction == 'UP': cy += 1
            elif direction == 'DOWN': cy -= 1

            if 1 <= cx <= self.n and 1 <= cy <= self.n:
                if (cx, cy) == self.wumpus_pos:
                    self.wumpus_alive = False
                    return True
            else:
                break
        return False

    def print_true_map(self):
        """Prints the true ground-truth map matching the lab assignment format."""
        print(f"| y \\ x | " + " | ".join(str(x) for x in range(1, self.n + 1)) + " |")
        print("|:-----:|" + ":-:|" * self.n)
        for y in range(self.n, 0, -1):
            row = [f"| {y} "]
            for x in range(1, self.n + 1):
                cell = (x, y)
                symbols = []
                if cell == (1, 1):
                    symbols.append("A")
                if cell == self.wumpus_pos and cell in self.pits:
                    symbols.append("W+P")
                elif cell == self.wumpus_pos:
                    symbols.append("W")
                elif cell in self.pits:
                    symbols.append("P")
                if cell == self.gold_pos:
                    symbols.append("G")
                if not symbols:
                    symbols.append(".")
                row.append(f"| {'+'.join(symbols)} ")
            row.append("|")
            print("".join(row))


class RuleBasedAgent:
    def __init__(self, n=4):
        self.n = n
        self.pos = (1, 1)
        self.visited = set()
        self.pit_free = {(1, 1)}
        self.all_cells = {(x, y) for x in range(1, n + 1) for y in range(1, n + 1)}
        self.wumpus_candidates = self.all_cells - {(1, 1)}
        self.wumpus_dead = False
        self.arrow_used = False
        self.actions_log = []
        self.trace = []

    def get_neighbors(self, pos):
        x, y = pos
        nbrs = []
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= self.n and 1 <= ny <= self.n:
                nbrs.append((nx, ny))
        return nbrs

    def is_safe(self, cell):
        """A cell is safe iff it is in PitFree and (WumpusDead or not a WumpusCandidate)."""
        return (cell in self.pit_free) and (self.wumpus_dead or (cell not in self.wumpus_candidates))

    def update_beliefs(self, percepts):
        self.visited.add(self.pos)

        # 1. PitFree Update: If no breeze, all neighbors are pit free
        if "Breeze" not in percepts:
            for nbr in self.get_neighbors(self.pos):
                self.pit_free.add(nbr)

        # 2. WumpusCandidates Update
        nbrs = set(self.get_neighbors(self.pos))
        if "Stench" in percepts:
            if not self.wumpus_dead:
                self.wumpus_candidates &= nbrs
        else:
            self.wumpus_candidates -= nbrs
            self.wumpus_candidates.discard(self.pos)

    def find_path_to_target(self, target):
        """BFS shortest path through visited/safe cells from current pos to target."""
        queue = deque([(self.pos, [self.pos])])
        visited_bfs = {self.pos}
        while queue:
            curr, path = queue.popleft()
            if curr == target:
                return path
            for nbr in self.get_neighbors(curr):
                if (nbr in self.visited or self.is_safe(nbr)) and nbr not in visited_bfs:
                    visited_bfs.add(nbr)
                    queue.append((nbr, path + [nbr]))
        return None

    def run(self, world):
        step = 0
        just_screamed = False

        while True:
            step += 1
            percepts = world.sense_percepts(self.pos, just_screamed)
            just_screamed = False
            self.update_beliefs(percepts)

            safe_cells = sorted([c for c in self.all_cells if self.is_safe(c)])

            # 1. Glitter Check: GRAB and stop
            if "Glitter" in percepts:
                self.actions_log.append("GRAB")
                self.trace.append({
                    'step': step,
                    'action': 'GRAB',
                    'pos': self.pos,
                    'percepts': percepts,
                    'safe_cells': safe_cells
                })
                shortest_path = self.find_path_to_target((1, 1))
                if shortest_path:
                    shortest_path.reverse()
                return "POSSIBLE", self.actions_log, shortest_path, self.trace

            # 2. Search for nearest unvisited safe cell
            unvisited_safe = [c for c in self.all_cells if self.is_safe(c) and c not in self.visited]

            if unvisited_safe:
                # Find closest unvisited safe cell via BFS
                best_path = None
                for candidate in unvisited_safe:
                    path = self.find_path_to_target(candidate)
                    if path:
                        if best_path is None or len(path) < len(best_path):
                            best_path = path

                if best_path and len(best_path) > 1:
                    next_pos = best_path[1]
                    dx = next_pos[0] - self.pos[0]
                    dy = next_pos[1] - self.pos[1]
                    act = "RIGHT" if dx == 1 else ("LEFT" if dx == -1 else ("UP" if dy == 1 else "DOWN"))
                    self.actions_log.append(act)
                    self.trace.append({
                        'step': step,
                        'action': f"MOVE {act} -> {next_pos}",
                        'pos': self.pos,
                        'percepts': percepts,
                        'safe_cells': safe_cells
                    })
                    self.pos = next_pos
                    continue

            # 3. If no safe unvisited cell and arrow unused, shoot along candidate line
            if not self.arrow_used and self.wumpus_candidates:
                self.arrow_used = True
                shot_direction = None

                # Prioritize adjacent direction containing candidate (RIGHT, UP, LEFT, DOWN)
                for direction in ['RIGHT', 'UP', 'LEFT', 'DOWN']:
                    cx, cy = self.pos
                    if direction == 'RIGHT': target = (cx + 1, cy)
                    elif direction == 'LEFT': target = (cx - 1, cy)
                    elif direction == 'UP': target = (cx, cy + 1)
                    elif direction == 'DOWN': target = (cx, cy - 1)
                    if target in self.wumpus_candidates:
                        shot_direction = direction
                        break

                # Otherwise find any candidate along row or column
                if shot_direction is None:
                    sorted_cands = sorted(list(self.wumpus_candidates), key=lambda c: (abs(c[0]-self.pos[0]) + abs(c[1]-self.pos[1])))
                    for cand in sorted_cands:
                        if cand[1] == self.pos[1]:
                            shot_direction = "RIGHT" if cand[0] > self.pos[0] else "LEFT"
                            break
                        elif cand[0] == self.pos[0]:
                            shot_direction = "UP" if cand[1] > self.pos[1] else "DOWN"
                            break

                if shot_direction:
                    hit = world.shoot_arrow(self.pos, shot_direction)
                    act_label = f"SHOOT_{shot_direction}"
                    if hit:
                        self.wumpus_dead = True
                        self.wumpus_candidates.clear()
                        just_screamed = True
                        act_label += " (Scream)"
                    else:
                        cx, cy = self.pos
                        while True:
                            if shot_direction == "RIGHT": cx += 1
                            elif shot_direction == "LEFT": cx -= 1
                            elif shot_direction == "UP": cy += 1
                            elif shot_direction == "DOWN": cy -= 1
                            if 1 <= cx <= self.n and 1 <= cy <= self.n:
                                self.wumpus_candidates.discard((cx, cy))
                            else:
                                break

                    self.actions_log.append(act_label)
                    self.trace.append({
                        'step': step,
                        'action': act_label,
                        'pos': self.pos,
                        'percepts': percepts,
                        'safe_cells': safe_cells
                    })
                    continue

            # 4. If still no safe unvisited cells, report NOT POSSIBLE
            self.trace.append({
                'step': step,
                'action': 'TERMINATE (No safe moves)',
                'pos': self.pos,
                'percepts': percepts,
                'safe_cells': safe_cells
            })
            return "NOT POSSIBLE", self.actions_log, None, self.trace


def run_test_case(test_num, n, wumpus_pos, pits, gold_pos):
    print(f"\n{'=' * 65}")
    print(f" TEST CASE {test_num}")
    print(f"{'=' * 65}")

    world = WumpusWorld(n=n, wumpus_pos=wumpus_pos, pits=pits, gold_pos=gold_pos)
    agent = RuleBasedAgent(n=n)

    verdict, actions, shortest_path, trace = agent.run(world)

    print("\n--- AGENT ACTION & PERCEPTION TRACE ---")
    for step_info in trace:
        percepts_str = ", ".join(step_info['percepts']) if step_info['percepts'] else "None"
        safe_str = ", ".join(f"({x},{y})" for x, y in step_info['safe_cells'])
        print(f"Step {step_info['step']:02d}: At {step_info['pos']} | Percepts: [{percepts_str}]")
        print(f"         Action: {step_info['action']}")
        print(f"         Safe Cells: [{safe_str}]")

    print(f"\nVERDICT: {verdict}")
    if verdict == "POSSIBLE":
        print(f"Actions Executed: {', '.join(actions)}")
        if shortest_path:
            path_str = " -> ".join(f"({x},{y})" for x, y in shortest_path)
            print(f"Shortest Safe Path: {path_str}")

    print("\n--- TRUE WORLD MAP ---")
    world.print_true_map()


def run_experiment():
    print("=================================================================")
    print(" EXPERIMENT 8: Rule-Based Wumpus World Agent")
    print("=================================================================")

    # Test 1: W at (1,3), G at (2,3), Pits at (3,1), (3,3), (4,4)
    run_test_case(1, 4, wumpus_pos=(1, 3), pits={(3, 1), (3, 3), (4, 4)}, gold_pos=(2, 3))

    # Test 2: W at (2,1), G at (3,2), Pits at (3,3), (4,1)
    run_test_case(2, 4, wumpus_pos=(2, 1), pits={(3, 3), (4, 1)}, gold_pos=(3, 2))

    # Test 3: W+P at (2,1), G at (4,4)
    run_test_case(3, 4, wumpus_pos=(2, 1), pits={(2, 1)}, gold_pos=(4, 4))


if __name__ == "__main__":
    run_experiment()
