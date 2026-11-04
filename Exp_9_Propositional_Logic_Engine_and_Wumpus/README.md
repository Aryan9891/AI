# Experiment 9: Propositional Logic Engine & Model Checking (Wumpus World Reasoning)

## 1. Overview & Objective
This experiment implements a **Propositional Logic Inference Engine** using model checking (truth-table enumeration) and applies it to **Wumpus World reasoning**:
1. **Sentence Representation**: Represent complex logical expressions using nested Python tuples:
   - Literal: `'P'`
   - Negation: `('not', 'P')`
   - Conjunction: `('and', 'P', 'Q', 'R')`
   - Disjunction: `('or', 'P', 'Q')`
   - Implication: `('implies', 'P', 'Q')`
   - Biconditional: `('iff', 'P', 'Q')`
2. **Model Checking & Inference**:
   - `pl_true(sentence, model)`: Recursively evaluates the truth value of any sentence under a given assignment dictionary.
   - `print_truth_table(sentence)`: Computes and prints the full truth table over all $2^n$ models.
   - `tt_entails(KB, alpha)`: Verifies whether $KB \models \alpha$ by proving that $\alpha$ holds in every model satisfying $KB$.
   - `is_valid(sentence)`: Checks if a sentence is a Tautology (true in all $2^n$ models).
   - `is_satisfiable(sentence)`: Checks if a sentence is true in at least one model.
3. **Application to Wumpus World**:
   - Encodes physical axioms connecting percepts to world hazards:
     $$B_{x,y} \iff \bigvee_{(nx, ny) \in \text{Neighbors}(x, y)} P_{nx, ny}$$
     $$S_{x,y} \iff \bigvee_{(nx, ny) \in \text{Neighbors}(x, y)} W_{nx, ny}$$
   - Formally proves a cell $(nx, ny)$ is safe by verifying $KB \models \neg P_{nx, ny}$ and $KB \models \neg W_{nx, ny}$.

---

## 2. Theoretical Verification Results
1. **Contrapositive Equivalence**:
   - $(P \implies Q) \iff (\neg Q \implies \neg P)$
   - Result: **Valid (Tautology = True)**
2. **Knowledge Base Entailment**:
   - $KB = \{P \implies Q, \quad Q \implies R, \quad P\}$
   - Query 1: $KB \models R \implies$ **True** (Modus Ponens chaining)
   - Query 2: $KB \models \neg R \implies$ **False**
3. **Validity & Satisfiability Table**:
   | Sentence | Valid (Tautology)? | Satisfiable? |
   | :--- | :---: | :---: |
   | $P \lor \neg P$ | **Yes** | **Yes** |
   | $P \land Q$ | **No** | **Yes** |
   | $P \land \neg P$ | **No** | **No** (Contradiction) |

---

## 3. Detailed Function Documentation

Here is the complete reference of every function in `exp9_propositional_logic_wumpus.py`:

### `pl_true(sentence, model)`
- **Purpose**: Evaluates boolean value of propositional sentence in assignment dictionary `model`.
- **Parameters**: `sentence` (`str`, `tuple`, or `bool`), `model` (`dict[str, bool]`).
- **Returns**: `bool`.

### `get_symbols(sentence)`
- **Purpose**: Recursively collects unique proposition variable names from sentence.
- **Parameters**: `sentence`.
- **Returns**: `set[str]`.

### `sentence_to_str(s)`
- **Purpose**: Converts nested tuple representation to standard algebraic logical notation (`~`, `&`, `|`, `=>`, `<=>`).
- **Parameters**: `s`.
- **Returns**: Formatted string.

### `print_truth_table(sentence)`
- **Purpose**: Generates and prints the complete ASCII truth table over all $2^n$ interpretations.
- **Parameters**: `sentence`.
- **Returns**: `None`.

### `tt_entails(kb, alpha)`
- **Purpose**: Checks semantic entailment $KB \models \alpha$ via truth-table enumeration.
- **Parameters**: `kb` (sentence or list of sentences), `alpha` (query sentence).
- **Returns**: `bool`.

### `is_valid(sentence)`
- **Purpose**: Returns `True` iff `sentence` evaluates to `True` under all $2^n$ possible truth assignments.
- **Parameters**: `sentence`.
- **Returns**: `bool`.

### `is_satisfiable(sentence)`
- **Purpose**: Returns `True` iff there exists at least one model where `sentence` evaluates to `True`.
- **Parameters**: `sentence`.
- **Returns**: `bool`.

### Class `LogicWumpusAgent`
- `__init__(self, n)`: Initializes $N \times N$ propositional knowledge base with initial safety axiom $\neg P_{1,1} \land \neg W_{1,1}$.
- `record_percepts(self, pos, percepts)`: Instantiates biconditional Breeze and Stench axioms and appends positive/negative percept observations.
- `is_cell_provably_safe(self, target)`: Evaluates $KB \models \neg P_{\text{target}}$ and $KB \models \neg W_{\text{target}}$ via model checking.
- `find_safe_path_to_gold(self, gold_pos, wumpus_pos, pits)`: Navigates through proven-safe cells to reach the gold.

### `run_experiment()`
- **Purpose**: Executes all assignment benchmark tests and displays the propositional logic Wumpus navigation path.
- **Returns**: `None`.

---

## 4. How to Run
### In Terminal:
```bash
python exp9_propositional_logic_wumpus.py
```

### In JupyterLab:
Open `exp9_propositional_logic_wumpus.ipynb` and run all cells.

