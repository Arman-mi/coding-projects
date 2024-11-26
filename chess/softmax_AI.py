from simple_ai import get_legal_moves

""" in this section of the script we are trying to implement our AI to play against us
we are giving each piece a certain amount of value points and we want the AI to 
protect its pieces while at the same time attack the opponents pieces"""
piece_values = {
    'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100,  # White pieces
    'p': -1, 'n': -3, 'b': -3, 'r': -5, 'q': -9, 'k': -100  # Black pieces
}
#this function runs through the board to see what the current score is. by score i mean points i mentioned earlier
def evaluate_board(board):
    
    score = 0
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in piece_values:
                score += piece_values[piece]

                # Reward center control
                if (row, col) in [(3, 3), (3, 4), (4, 3), (4, 4)]:
                    score += 0.5 if piece.isupper() else -0.5  

                
                if piece.lower() == 'p' and is_pawn_blocked(board, row, col):
                    score += -0.5 if piece.isupper() else 0.5
    return score

def is_pawn_blocked(board, row, col):
    """Check if a pawn is blocked."""
    direction = -1 if board[row][col].isupper() else 1  
    return board[row + direction][col] != " " if 0 <= row + direction < 8 else True


#Find all pieces that can be attacked by the given side. this function helps with aggression
#so that the AI does not play defensivly
def find_targets(board, is_white):
    targets = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != " " and ((is_white and piece.islower()) or (not is_white and piece.isupper())):
                targets.append((row, col))
    return targets


def choose_best_move(board, depth=2):
    
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
        # Double the value of attacking
        if target_piece != " ":
            eval += abs(piece_values[target_piece]) * 2  

        # Undo the move
        board[start[0]][start[1]] = start_piece
        board[end[0]][end[1]] = target_piece

        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move


