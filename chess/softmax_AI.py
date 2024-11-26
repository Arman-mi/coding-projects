from simple_ai import get_legal_moves
# ai.py

piece_values = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100,  # White pieces
    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -100  # Black pieces
}

def evaluate_board(board):
    """Evaluate the board state and return a score."""
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in piece_values:
                score += piece_values[piece]

                # Reward center control
                if (row, col) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                    score += 0.5 if piece.isupper() else -0.5  # White gets positive, Black gets negative

                # Penalize pawns that are blocked
                if piece.lower() == 'p' and is_pawn_blocked(board, row, col):
                    score += -0.5 if piece.isupper() else 0.5
    return score

def is_pawn_blocked(board, row, col):
    """Check if a pawn is blocked."""
    direction = -1 if board[row][col].isupper() else 1  # White pawns move up (-1), Black down (+1)
    return board[row + direction][col] != " " if 0 <= row + direction < 8 else True

def find_targets(board, is_white):
    """Find all pieces that can be attacked by the given side."""
    targets = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != " " and ((is_white and piece.islower()) or (not is_white and piece.isupper())):
                targets.append((row, col))
    return targets


def choose_best_move(board, depth=2):
    """Choose the best move for the AI using improved logic."""
    best_move = None
    max_eval = float('-inf')

    for move in get_legal_moves(board, is_white=False):  # Black is maximizing
        start, end = move
        start_piece = board[start[0]][start[1]]

        # Simulate the move
        target_piece = board[end[0]][end[1]]
        board[start[0]][start[1]] = ' '
        board[end[0]][end[1]] = start_piece

        # Calculate the evaluation
        eval = evaluate_board(board)

        # Add bonus for attacking high-value targets
        if target_piece != " ":
            eval += abs(piece_values[target_piece]) * 2  # Double the value of attacking

        # Undo the move
        board[start[0]][start[1]] = start_piece
        board[end[0]][end[1]] = target_piece

        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move


