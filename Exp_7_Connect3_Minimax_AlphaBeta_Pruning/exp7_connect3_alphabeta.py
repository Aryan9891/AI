"""
Artificial Intelligence Lab - LAB 07
Adversarial Search: Connect-3 on a 4x4 Board
Comparison: Plain Minimax Search vs. Minimax with Alpha-Beta Pruning
Author: Aryan Sachin
"""

ROWS = 4
COLS = 4

def create_board():
    """Initializes a 4x4 grid of empty cells ('-')."""
    return [['-' for _ in range(COLS)] for _ in range(ROWS)]

def display_board(board):
    """
    Displays the board according to the lab markdown table specification:
    | 1 | 2 | 3 | 4 |
    |:-:|:-:|:-:|:-:|
    | - | - | - | - |
    """
    print("| 1 | 2 | 3 | 4 |")
    print("|:-:|:-:|:-:|:-:|")
    for r in range(ROWS):
        row_str = "| " + " | ".join(board[r]) + " |"
        print(row_str)

def get_lowest_empty_row(board, col):
    """Returns row index of lowest empty cell in column (gravity), or -1 if full."""
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == '-':
            return r
    return -1

def is_valid_column(board, col):
    """Validates that col is within [0, 3] and column is not full."""
    if 0 <= col < COLS:
        return board[0][col] == '-'
    return False

def check_win(board, player):
    r"""
    Checks if 'player' has achieved 3-in-a-line:
    - Horizontal
    - Vertical
    - Diagonal (\ and /)
    """
    # Horizontal check
    for r in range(ROWS):
        for c in range(COLS - 2):
            if board[r][c] == board[r][c + 1] == board[r][c + 2] == player:
                return True

    # Vertical check
    for c in range(COLS):
        for r in range(ROWS - 2):
            if board[r][c] == board[r + 1][c] == board[r + 2][c] == player:
                return True

    # Diagonal \ check
    for r in range(ROWS - 2):
        for c in range(COLS - 2):
            if board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == player:
                return True

    # Diagonal / check
    for r in range(2, ROWS):
        for c in range(COLS - 2):
            if board[r][c] == board[r - 1][c + 1] == board[r - 2][c + 2] == player:
                return True

    return False

def is_board_full(board):
    """Checks if all 16 cells are filled."""
    return all(board[0][c] != '-' for c in range(COLS))

# =====================================================================
# 1. Plain Minimax Search
# =====================================================================
minimax_search_count = 0

def minimax(board, depth, is_maximizing, max_depth=7):
    """
    Plain recursive Minimax algorithm without pruning.
    Tracks every node evaluation in minimax_search_count.
    """
    global minimax_search_count
    minimax_search_count += 1

    if check_win(board, 'O'):  # AI wins
        return 100 - depth
    if check_win(board, 'X'):  # User wins
        return depth - 100
    if is_board_full(board) or depth == max_depth:
        return 0

    if is_maximizing:
        best_val = float('-inf')
        for c in range(COLS):
            r = get_lowest_empty_row(board, c)
            if r != -1:
                board[r][c] = 'O'
                val = minimax(board, depth + 1, False, max_depth)
                board[r][c] = '-'
                best_val = max(best_val, val)
        return best_val
    else:
        best_val = float('inf')
        for c in range(COLS):
            r = get_lowest_empty_row(board, c)
            if r != -1:
                board[r][c] = 'X'
                val = minimax(board, depth + 1, True, max_depth)
                board[r][c] = '-'
                best_val = min(best_val, val)
        return best_val

def get_best_move_minimax(board, max_depth=7):
    """Computes AI choice using plain Minimax."""
    best_val = float('-inf')
    best_col = None
    # Prefer center columns (col 2 and 1) if scores tie
    for c in [2, 1, 3, 0]:
        r = get_lowest_empty_row(board, c)
        if r != -1:
            board[r][c] = 'O'
            val = minimax(board, 1, False, max_depth)
            board[r][c] = '-'
            if val > best_val:
                best_val = val
                best_col = c
    return best_col

# =====================================================================
# 2. Minimax with Alpha-Beta Pruning
# =====================================================================
alphabeta_search_count = 0

def alphabeta(board, depth, alpha, beta, is_maximizing, max_depth=7):
    """
    Minimax with Alpha-Beta Pruning.
    Tracks every node evaluation in alphabeta_search_count.
    """
    global alphabeta_search_count
    alphabeta_search_count += 1

    if check_win(board, 'O'):
        return 100 - depth
    if check_win(board, 'X'):
        return depth - 100
    if is_board_full(board) or depth == max_depth:
        return 0

    if is_maximizing:
        best_val = float('-inf')
        for c in [2, 1, 3, 0]:
            r = get_lowest_empty_row(board, c)
            if r != -1:
                board[r][c] = 'O'
                val = alphabeta(board, depth + 1, alpha, beta, False, max_depth)
                board[r][c] = '-'
                best_val = max(best_val, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
        return best_val
    else:
        best_val = float('inf')
        for c in [2, 1, 3, 0]:
            r = get_lowest_empty_row(board, c)
            if r != -1:
                board[r][c] = 'X'
                val = alphabeta(board, depth + 1, alpha, beta, True, max_depth)
                board[r][c] = '-'
                best_val = min(best_val, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
        return best_val

def get_best_move_alphabeta(board, max_depth=7):
    """Computes AI choice using Alpha-Beta Pruning."""
    best_val = float('-inf')
    best_col = None
    alpha = float('-inf')
    beta = float('inf')

    for c in [2, 1, 3, 0]:
        r = get_lowest_empty_row(board, c)
        if r != -1:
            board[r][c] = 'O'
            val = alphabeta(board, 1, alpha, beta, False, max_depth)
            board[r][c] = '-'
            if val > best_val:
                best_val = val
                best_col = c
            alpha = max(alpha, val)
    return best_col

# =====================================================================
# Game Simulation Loops
# =====================================================================
def play_connect3(algorithm="alphabeta", preset_moves=None, max_depth=7):
    """
    Runs a Connect-3 game match between User (X) and AI (O).
    """
    global minimax_search_count, alphabeta_search_count
    if algorithm == "minimax":
        print("---- Connect 3 Using MinMax Algorithm ----")
        minimax_search_count = 0
    else:
        print("---- Connect 3 Using Alpha Beta Pruning ----")
        alphabeta_search_count = 0

    print("User is X")
    print("AI is O")
    print("Here is the empty board:")
    board = create_board()
    display_board(board)

    input_iter = iter(preset_moves) if preset_moves else None

    def get_user_choice():
        if input_iter:
            choice = next(input_iter)
            print(f"User Choice of Drop : {choice}")
            return choice
        while True:
            try:
                raw = input("User Choice of Drop (1-4): ").strip()
                val = int(raw)
                if 1 <= val <= 4 and is_valid_column(board, val - 1):
                    return val
                print("Invalid drop column! Column must be 1-4 and not full.")
            except (ValueError, EOFError):
                print("Please enter a number between 1 and 4.")

    while True:
        # User Turn
        user_col = get_user_choice() - 1
        ur = get_lowest_empty_row(board, user_col)
        board[ur][user_col] = 'X'
        display_board(board)

        if check_win(board, 'X'):
            print("User Won!")
            break
        if is_board_full(board):
            print("Game Over: Draw!")
            break

        # AI Turn
        if algorithm == "minimax":
            ai_col = get_best_move_minimax(board, max_depth)
            searches = minimax_search_count
        else:
            ai_col = get_best_move_alphabeta(board, max_depth)
            searches = alphabeta_search_count

        print(f"AI Thinking ... AI Choice : {ai_col + 1}")
        air = get_lowest_empty_row(board, ai_col)
        board[air][ai_col] = 'O'
        display_board(board)

        if check_win(board, 'O'):
            print(f"AI Won.... Number of Searches done in total : {searches:,}")
            break
        if is_board_full(board):
            print(f"Game Over: Draw! Searches done in total : {searches:,}")
            break

def run_experiment():
    print("=" * 70)
    print(" EXPERIMENT 7: Connect-3 on a 4x4 Board (Minimax vs. Alpha-Beta)")
    print("=" * 70)

    # Replay sequence from lab sample: User drops in column 2, then 4, then 2
    sample_user_drops = [2, 4, 2]

    print("\n--- 1. RUNNING WITH PLAIN MINIMAX ---")
    play_connect3(algorithm="minimax", preset_moves=sample_user_drops, max_depth=7)

    print("\n--- 2. RUNNING WITH ALPHA-BETA PRUNING ---")
    play_connect3(algorithm="alphabeta", preset_moves=sample_user_drops, max_depth=7)

    # Search reduction analysis
    mm_count = minimax_search_count
    ab_count = alphabeta_search_count
    pruned = mm_count - ab_count
    reduction_pct = (pruned / mm_count) * 100 if mm_count > 0 else 0

    print("\n" + "=" * 60)
    print("           SEARCH TREE PRUNING COMPARISON")
    print("=" * 60)
    print(f"Plain Minimax Total Node Evaluations:   {mm_count:,}")
    print(f"Alpha-Beta Pruning Node Evaluations:    {ab_count:,}")
    print(f"Nodes Pruned (Removed from Search):     {pruned:,}")
    print(f"Search Space Reduction:                 {reduction_pct:.2f}%")
    print("=" * 60)

if __name__ == "__main__":
    run_experiment()
