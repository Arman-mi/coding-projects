"""
im assigning a string to each variable for better representation on the board. 
upper case for white pieces and lower case for black pieces, using 2 letter for a representaiton (like bq for black queen)
should be avoided because it will then mess up the amount of space a peice will take on the board.
"""

EMPTY = " "
WHITE_PAWN = "P"
WHITE_ROOK = "R"
WHITE_KNIGHT = "N"
WHITE_BISHOP = "B"
WHITE_QUEEN = "Q"
WHITE_KING = "K"
BLACK_PAWN = "p"
BLACK_ROOK = "r"
BLACK_KNIGHT = "n"
BLACK_BISHOP = "b"
BLACK_QUEEN = "q"
BLACK_KING = "k"

# Im using this function to create my 8 by 8 board
def initialize_board():
    board = [
        [BLACK_ROOK, BLACK_KNIGHT, BLACK_BISHOP, BLACK_QUEEN, BLACK_KING, BLACK_BISHOP, BLACK_KNIGHT, BLACK_ROOK],
        [BLACK_PAWN] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [EMPTY] * 8,
        [WHITE_PAWN] * 8,
        [WHITE_ROOK, WHITE_KNIGHT, WHITE_BISHOP, WHITE_QUEEN, WHITE_KING, WHITE_BISHOP, WHITE_KNIGHT, WHITE_ROOK]
    ]
    return board



def print_board(board):
    for row in board:
        print(" ".join(piece if piece != " " else "." for piece in row))
    print("\n")
    

board = initialize_board()
print_board(board)
