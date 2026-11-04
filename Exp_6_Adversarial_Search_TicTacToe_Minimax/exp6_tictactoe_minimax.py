"""
Artificial Intelligence Lab - LAB 06
Adversarial Search: Tic-Tac-Toe Game with Line User Interface (LUI)
Part 1: Two-Player Human Game
Part 2: Human vs. Minimax AI Agent
Author: Aryan Sachin
"""

def create_board():
    """Initializes empty 3x3 board as list of 9 spaces."""
    return [' ' for _ in range(9)]

def display_board(board):
    """
    Displays the board according to the lab specification:
    Empty squares show their 1-based number (1 to 9).
    Occupied squares show 'X' or 'O'.
    """
    def cell(idx):
        return str(idx + 1) if board[idx] == ' ' else board[idx]

    print(f"{cell(0)} | {cell(1)} | {cell(2)}")
    print("---+---+---")
    print(f"{cell(3)} | {cell(4)} | {cell(5)}")
    print("---+---+---")
    print(f"{cell(6)} | {cell(7)} | {cell(8)}")

def check_winner(board):
    """
    Checks for winning rows, columns, or diagonals.
    Returns: 'X', 'O', 'Draw' (if board is full), or None (ongoing).
    """
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for a, b, c in win_combinations:
        if board[a] == board[b] == board[c] and board[a] != ' ':
            return board[a]

    if ' ' not in board:
        return 'Draw'

    return None

def is_valid_move(board, move):
    """Returns True if move is an integer 1-9 and corresponding cell is empty."""
    if move in range(1, 10):
        return board[move - 1] == ' '
    return False

def minimax(board, depth, is_maximizing, ai_player='O', human_player='X'):
    """
    Minimax recursive game tree search with depth-based evaluation:
    - Faster wins have higher scores (10 - depth).
    - Delayed losses have higher scores (depth - 10).
    Returns: (best_score, best_move_index)
    """
    state = check_winner(board)
    if state == ai_player:
        return 10 - depth, None
    elif state == human_player:
        return depth - 10, None
    elif state == 'Draw':
        return 0, None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if board[i] == ' ':
                board[i] = ai_player
                score, _ = minimax(board, depth + 1, False, ai_player, human_player)
                board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for i in range(9):
            if board[i] == ' ':
                board[i] = human_player
                score, _ = minimax(board, depth + 1, True, ai_player, human_player)
                board[i] = ' '
                if score < best_score:
                    best_score = score
                    best_move = i
        return best_score, best_move

def get_computer_move(board, ai_player='O', human_player='X'):
    """Finds optimal move for AI agent using minimax tree search."""
    _, best_move_idx = minimax(board, 0, True, ai_player, human_player)
    return best_move_idx + 1

# =====================================================================
# Game Modes
# =====================================================================

def play_two_player():
    """Two-player human mode sharing the terminal."""
    print("\n--- TWO-PLAYER TIC-TAC-TOE ---")
    board = create_board()
    current_player = 'X'

    while True:
        display_board(board)
        try:
            raw = input(f"Player {current_player}'s move (1-9): ").strip()
            move = int(raw)
            if not is_valid_move(board, move):
                print("Invalid move or cell already occupied! Choose an empty cell between 1 and 9.")
                continue
        except (ValueError, EOFError):
            print("Invalid input! Please enter an integer from 1 to 9.")
            continue

        board[move - 1] = current_player
        result = check_winner(board)
        if result:
            display_board(board)
            if result == 'Draw':
                print("Game Over: It's a draw!")
            else:
                print(f"Player {result} wins!")
            break

        current_player = 'O' if current_player == 'X' else 'X'

def play_against_ai(preset_inputs=None):
    """
    Human vs Minimax AI Agent mode matching the lab sample output.
    If preset_inputs is provided, simulates the game autonomously.
    """
    print("--- TIC-TAC-TOE ---")
    input_iter = iter(preset_inputs) if preset_inputs else None

    def get_input(prompt):
        if input_iter:
            val = next(input_iter)
            print(f"{prompt}{val}")
            return val
        return input(prompt).strip()

    play_first = get_input("Do you want to play first? (y/n): ").lower()
    human = 'X' if play_first == 'y' else 'O'
    ai = 'O' if human == 'X' else 'X'

    print(f"You are {human}, the computer is {ai}.")
    board = create_board()
    display_board(board)

    current = 'X'
    while True:
        if current == human:
            while True:
                try:
                    move = int(get_input(f"Your move ({human}): "))
                    if is_valid_move(board, move):
                        board[move - 1] = human
                        break
                    print("Invalid or occupied square! Try again.")
                except ValueError:
                    print("Please enter a valid digit (1-9).")
        else:
            print("Computer is thinking...")
            comp_move = get_computer_move(board, ai_player=ai, human_player=human)
            print(f"Computer plays {comp_move}")
            board[comp_move - 1] = ai
            display_board(board)

        winner = check_winner(board)
        if winner:
            if current == human and winner != 'Draw':
                display_board(board)
            if winner == 'Draw':
                print("The game is a draw!")
            elif winner == ai:
                print(f"Computer ({ai}) wins!")
            else:
                print(f"Congratulations! You ({human}) win!")
            break

        current = 'O' if current == 'X' else 'X'

def run_demo():
    """Runs the exact simulation trace featured in the lab assignment sheet."""
    sample_moves = ['y', '1', '9', '4']
    play_against_ai(preset_inputs=sample_moves)

if __name__ == "__main__":
    run_demo()
