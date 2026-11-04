"""
Artificial Intelligence Lab - LAB 09
Propositional Logic Engine (Model Checking) and Logic-Based Wumpus World Agent
Author: Aryan Sachin
"""

import itertools
from collections import deque

# =====================================================================
# 1. Propositional Logic Engine
# =====================================================================

def pl_true(sentence, model):
    """
    Evaluates a propositional sentence in a given model (dict of symbol -> bool).
    Representations:
      'P'                       -> string symbol
      ('not', s)                -> negation
      ('and', s1, s2, ...)      -> conjunction
      ('or', s1, s2, ...)       -> disjunction
      ('implies', p, q)         -> material implication (not p or q)
      ('iff', p, q)             -> biconditional (p == q)
    """
    if isinstance(sentence, bool):
        return sentence
    if isinstance(sentence, str):
        if sentence in model:
            return model[sentence]
        raise KeyError(f"Symbol '{sentence}' not assigned in model: {model}")

    op = sentence[0]
    args = sentence[1:]

    if op == 'not':
        return not pl_true(args[0], model)
    elif op == 'and':
        return all(pl_true(a, model) for a in args)
    elif op == 'or':
        return any(pl_true(a, model) for a in args)
    elif op == 'implies':
        return (not pl_true(args[0], model)) or pl_true(args[1], model)
    elif op == 'iff':
        return pl_true(args[0], model) == pl_true(args[1], model)
    else:
        raise ValueError(f"Unknown operator: {op}")

def get_symbols(sentence):
    """Extracts all propositional variable names from a sentence."""
    if isinstance(sentence, str):
        return {sentence}
    if isinstance(sentence, (list, tuple)):
        symbols = set()
        for elem in sentence[1:]:
            symbols |= get_symbols(elem)
        return symbols
    return set()

def sentence_to_str(s):
    """Pretty prints nested tuple propositional sentences."""
    if isinstance(s, str):
        return s
    op = s[0]
    if op == 'not':
        return f"~{sentence_to_str(s[1])}"
    elif op == 'and':
        return "(" + " & ".join(sentence_to_str(a) for a in s[1:]) + ")"
    elif op == 'or':
        return "(" + " | ".join(sentence_to_str(a) for a in s[1:]) + ")"
    elif op == 'implies':
        return f"({sentence_to_str(s[1])} => {sentence_to_str(s[2])})"
    elif op == 'iff':
        return f"({sentence_to_str(s[1])} <=> {sentence_to_str(s[2])})"
    return str(s)

def print_truth_table(sentence):
    """Generates and prints the complete truth table for any propositional sentence."""
    symbols = sorted(list(get_symbols(sentence)))
    n = len(symbols)
    expr_str = sentence_to_str(sentence)

    header = " | ".join(f"{s:^5}" for s in symbols) + f" | {expr_str:^25}"
    separator = "-" * len(header)

    print(f"\nTruth Table for: {expr_str}")
    print(separator)
    print(header)
    print(separator)

    for values in itertools.product([True, False], repeat=n):
        model = dict(zip(symbols, values))
        res = pl_true(sentence, model)
        row_str = " | ".join(f"{'T' if v else 'F':^5}" for v in values) + f" | {'T' if res else 'F':^25}"
        print(row_str)
    print(separator + "\n")

# =====================================================================
# 2. Entailment, Validity, and Satisfiability
# =====================================================================

def tt_entails(kb, alpha):
    """
    Checks KB |= alpha by truth-table enumeration:
    alpha must be True in every model where KB is True.
    """
    if isinstance(kb, (list, set)):
        kb_sentence = ('and', *kb) if len(kb) > 1 else (list(kb)[0] if kb else True)
    else:
        kb_sentence = kb

    symbols = sorted(list(get_symbols(kb_sentence) | get_symbols(alpha)))

    for values in itertools.product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        if pl_true(kb_sentence, model):
            if not pl_true(alpha, model):
                return False
    return True

def is_valid(sentence):
    """A sentence is valid (tautology) if it is True in all 2^n models."""
    symbols = sorted(list(get_symbols(sentence)))
    for values in itertools.product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        if not pl_true(sentence, model):
            return False
    return True

def is_satisfiable(sentence):
    """A sentence is satisfiable if it is True in at least one model."""
    symbols = sorted(list(get_symbols(sentence)))
    for values in itertools.product([True, False], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        if pl_true(sentence, model):
            return True
    return False

# =====================================================================
# 3. Propositional Logic-Driven Wumpus World
# =====================================================================

class LogicWumpusAgent:
    """
    Solves Wumpus World navigation using Propositional Logic Model Checking.
    Proves cell safety by querying:
      KB |= ~P_x_y   (provably Pit-free)
      KB |= ~W_x_y   (provably Wumpus-free)
    """
    def __init__(self, n=4):
        self.n = n
        self.pos = (1, 1)
        self.visited = set()
        self.proven_safe = {(1, 1)}
        self.pit_clauses = {}      # (x, y) -> list of breeze clauses
        self.wumpus_clauses = {}   # (x, y) -> list of stench clauses

    def get_neighbors(self, pos):
        x, y = pos
        nbrs = []
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= self.n and 1 <= ny <= self.n:
                nbrs.append((nx, ny))
        return nbrs

    def record_percepts(self, pos, percepts):
        x, y = pos
        self.visited.add(pos)
        nbrs = self.get_neighbors(pos)

        breeze_sym = f"B_{x}_{y}"
        pit_nbrs = [f"P_{nx}_{ny}" for nx, ny in nbrs]
        b_equiv = ('iff', breeze_sym, ('or', *pit_nbrs))
        b_fact = breeze_sym if "Breeze" in percepts else ('not', breeze_sym)
        self.pit_clauses[pos] = [b_equiv, b_fact]

        stench_sym = f"S_{x}_{y}"
        w_nbrs = [f"W_{nx}_{ny}" for nx, ny in nbrs]
        s_equiv = ('iff', stench_sym, ('or', *w_nbrs))
        s_fact = stench_sym if "Stench" in percepts else ('not', stench_sym)
        self.wumpus_clauses[pos] = [s_equiv, s_fact]

    def is_cell_provably_safe(self, target):
        if target in self.proven_safe:
            return True
        tx, ty = target
        p_target = f"P_{tx}_{ty}"
        w_target = f"W_{tx}_{ty}"

        # Collect clauses from visited neighbors of target
        relevant_pit_kb = []
        relevant_wumpus_kb = []
        for nbr in self.get_neighbors(target):
            if nbr in self.pit_clauses:
                relevant_pit_kb.extend(self.pit_clauses[nbr])
            if nbr in self.wumpus_clauses:
                relevant_wumpus_kb.extend(self.wumpus_clauses[nbr])

        if not relevant_pit_kb or not relevant_wumpus_kb:
            return False

        # Model checking for target
        pit_free = tt_entails(relevant_pit_kb, ('not', p_target))
        wumpus_free = tt_entails(relevant_wumpus_kb, ('not', w_target))

        if pit_free and wumpus_free:
            self.proven_safe.add(target)
            return True
        return False

    def find_safe_path_to_gold(self, gold_pos, wumpus_pos, pits, max_steps=25):
        current = (1, 1)
        path_taken = [current]
        step = 0

        while current != gold_pos and step < max_steps:
            step += 1
            nbrs = self.get_neighbors(current)
            stench = (wumpus_pos in nbrs)
            breeze = any(p in nbrs for p in pits)
            percepts = []
            if stench: percepts.append("Stench")
            if breeze: percepts.append("Breeze")

            self.record_percepts(current, percepts)

            # Deduce safety of adjacent cells using propositional logic
            for nbr in nbrs:
                self.is_cell_provably_safe(nbr)

            unvisited_safe = [c for c in self.proven_safe if c not in self.visited]
            if not unvisited_safe:
                break

            # BFS through proven safe cells to nearest unvisited safe cell
            queue = deque([(current, [current])])
            seen = {current}
            next_step = None

            while queue:
                node, path = queue.popleft()
                if node in unvisited_safe:
                    if len(path) > 1:
                        next_step = path[1]
                    break
                for n in self.get_neighbors(node):
                    if n in self.proven_safe and n not in seen:
                        seen.add(n)
                        queue.append((n, path + [n]))

            if next_step:
                current = next_step
                path_taken.append(current)
            else:
                break

        return path_taken


# =====================================================================
# Main Benchmark & Verification Driver
# =====================================================================
def run_experiment():
    print("=" * 70)
    print(" EXPERIMENT 9: Propositional Logic Engine & Model Checking")
    print("=" * 70)

    # 1. Test 1: (P => Q) <=> (~Q => ~P)
    print("\n--- 1. Testing Contrapositive Equivalence: (P => Q) <=> (~Q => ~P) ---")
    contrapositive = ('iff', ('implies', 'P', 'Q'), ('implies', ('not', 'Q'), ('not', 'P')))
    print_truth_table(contrapositive)
    valid_contra = is_valid(contrapositive)
    print(f"Is the sentence Valid (Tautology)? {valid_contra} (Expected: True)\n")

    # 2. Test 2: KB Entailment
    print("--- 2. Testing Entailment by Truth-Table Enumeration ---")
    kb = [
        ('implies', 'P', 'Q'),
        ('implies', 'Q', 'R'),
        'P'
    ]
    print(f"Knowledge Base (KB): {[sentence_to_str(s) for s in kb]}")
    entails_R = tt_entails(kb, 'R')
    entails_not_R = tt_entails(kb, ('not', 'R'))
    print(f"Query 1: Does KB |= R?    {entails_R} (Expected: True)")
    print(f"Query 2: Does KB |= ~R?   {entails_not_R} (Expected: False)\n")

    # 3. Test 3: Validity & Satisfiability Table
    print("--- 3. Validity and Satisfiability Checks ---")
    test_sentences = [
        ("P or ~P", ('or', 'P', ('not', 'P'))),
        ("P and Q", ('and', 'P', 'Q')),
        ("P and ~P", ('and', 'P', ('not', 'P')))
    ]

    print(f"{'Sentence':<15} | {'Valid?':<10} | {'Satisfiable?':<15}")
    print("-" * 45)
    for name, s in test_sentences:
        v = "Yes" if is_valid(s) else "No"
        sat = "Yes" if is_satisfiable(s) else "No"
        print(f"{name:<15} | {v:<10} | {sat:<15}")
    print("-" * 45 + "\n")

    # 4. Part 3: Propositional Logic in Wumpus World
    print("--- 4. Propositional Logic Wumpus World Navigation ---")
    agent = LogicWumpusAgent(n=4)
    gold = (2, 3)
    wumpus = (1, 3)
    pits = {(3, 1), (3, 3), (4, 4)}

    print(f"Goal: Gold at {gold} | Wumpus at {wumpus} | Pits: {pits}")
    safe_path = agent.find_safe_path_to_gold(gold, wumpus, pits)
    print(f"Path Discovered via Propositional Logic Entailment:")
    print(" -> ".join(f"({x},{y})" for x, y in safe_path))
    print("All traversed cells were formally proven pit-free and wumpus-free by model checking!")


if __name__ == "__main__":
    run_experiment()
