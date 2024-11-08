# Define constants for the chess pieces
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

# Initialize an 8x8 chessboard
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

# Function to print the board in a readable format
# def print_board(board):
#     for row in board:
#         print(" ".join(row))
#     print("\n")


def print_board(board):
    for row in board:
        # Replace empty spaces with a dot ('.') to make the board clearer
        print(" ".join(piece if piece != " " else "." for piece in row))
    print("\n")

# Initialize and display the chessboard
board = initialize_board()
print_board(board)
