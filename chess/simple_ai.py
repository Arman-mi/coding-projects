"""this AI does not take aggresion into acount was only written to pick any availble move and to do it
it was written for a sanity check to see if thing are working or not
"""
import random

from pieces import would_be_in_check, move_piece

def get_legal_moves(board, is_white):
   
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != " " and ((is_white and piece.isupper()) or (not is_white and piece.islower())):
                # Generate all possible moves for this piece
                for end_row in range(8):
                    for end_col in range(8):
                        if move_piece(board, (row, col), (end_row, end_col), check_only=True):
                            # Check if the move leaves the king safe
                            if not would_be_in_check(board, (row, col), (end_row, end_col), is_white):
                                moves.append(((row, col), (end_row, end_col)))
    return moves

"""Choose a random valid move for the given side that does not leave the king in check."""
def choose_random_move(board, is_white=False):
    legal_moves = get_legal_moves(board, is_white)
    if legal_moves:
        return random.choice(legal_moves)
    return None
