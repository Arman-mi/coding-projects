# pieces.py
import pygame
import sys

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

def is_valid_pawn_move(board, start_row, start_col, end_row, end_col, is_white):
    direction = 1 if is_white else -1
    start_piece = board[start_row][start_col]
    end_piece = board[end_row][end_col]
    
    # Regular move: One square forward
    if start_col == end_col and end_piece == EMPTY:
        # Two squares forward from starting position
        if (is_white and start_row == 6 and end_row == 4) or (not is_white and start_row == 1 and end_row == 3):
            return True
        # One square forward
        elif end_row == start_row - direction:
            return True
    # Capturing: Diagonal move
    elif abs(start_col - end_col) == 1 and end_row == start_row - direction:
        if is_white and end_piece.islower() or not is_white and end_piece.isupper():
            return True

    return False

# Function for Rook Movement
def is_valid_rook_move(board, start_row, start_col, end_row, end_col):
    # Rooks move either horizontally or vertically
    if start_row == end_row or start_col == end_col:
        if no_piece_in_path(board, start_row, start_col, end_row, end_col):
            return True
    return False

# Function for Bishop Movement
def is_valid_bishop_move(board, start_row, start_col, end_row, end_col):
    # Bishops move diagonally, so row and column change must be equal
    if abs(start_row - end_row) == abs(start_col - end_col):
        if no_piece_in_path(board, start_row, start_col, end_row, end_col):
            return True
    return False

# Function for Knight Movement
def is_valid_knight_move(board, start_row, start_col, end_row, end_col):
    # Knights move in an "L" shape
    if (abs(start_row - end_row) == 2 and abs(start_col - end_col) == 1) or (abs(start_row - end_row) == 1 and abs(start_col - end_col) == 2):
        return True
    return False

# Function for Queen Movement
def is_valid_queen_move(board, start_row, start_col, end_row, end_col):
    # Queens move like both rooks and bishops
    if is_valid_rook_move(board, start_row, start_col, end_row, end_col) or is_valid_bishop_move(board, start_row, start_col, end_row, end_col):
        return True
    return False

# Function for King Movement
def is_valid_king_move(board, start_row, start_col, end_row, end_col):
    # Kings move one square in any direction
    if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
        return True
    return False

# Helper function to check if there are no pieces in the path
def no_piece_in_path(board, start_row, start_col, end_row, end_col):
    if start_row == end_row:
        # Horizontal move
        step = 1 if start_col < end_col else -1
        for col in range(start_col + step, end_col, step):
            if board[start_row][col] != EMPTY:
                return False
    elif start_col == end_col:
        # Vertical move
        step = 1 if start_row < end_row else -1
        for row in range(start_row + step, end_row, step):
            if board[row][start_col] != EMPTY:
                return False
    else:
        # Diagonal move
        row_step = 1 if start_row < end_row else -1
        col_step = 1 if start_col < end_col else -1
        for row, col in zip(range(start_row + row_step, end_row, row_step), range(start_col + col_step, end_col, col_step)):
            if board[row][col] != EMPTY:
                return False
    return True

"""
# Function to move a piece (wrapper for all piece movement validation)
def move_piece(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    
    if piece == WHITE_PAWN or piece == BLACK_PAWN:
        is_white = piece == WHITE_PAWN
        return is_valid_pawn_move(board, start_row, start_col, end_row, end_col, is_white)
    
    elif piece == WHITE_ROOK or piece == BLACK_ROOK:
        return is_valid_rook_move(board, start_row, start_col, end_row, end_col)
    
    elif piece == WHITE_BISHOP or piece == BLACK_BISHOP:
        return is_valid_bishop_move(board, start_row, start_col, end_row, end_col)
    
    elif piece == WHITE_KNIGHT or piece == BLACK_KNIGHT:
        return is_valid_knight_move(board, start_row, start_col, end_row, end_col)
    
    elif piece == WHITE_QUEEN or piece == BLACK_QUEEN:
        return is_valid_queen_move(board, start_row, start_col, end_row, end_col)
    
    elif piece == WHITE_KING or piece == BLACK_KING:
        return is_valid_king_move(board, start_row, start_col, end_row, end_col)
    
    return False  # Invalid move
    

# pieces.py

def move_piece(board, start, end):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    
    print(f"Attempting to move piece '{piece}' from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    handle_castling()
    handle_pawn_promotion()
    
    if piece == WHITE_PAWN or piece == BLACK_PAWN:
        is_white = piece == WHITE_PAWN
        if is_valid_pawn_move(board, start_row, start_col, end_row, end_col, is_white):
            board[end_row][end_col] = piece  # Move the piece to the new position
            board[start_row][start_col] = EMPTY  # Clear the starting position
            print(f"Move successful: {piece} moved to ({end_row}, {end_col})")
            return True
        else:
            print(f"Invalid move for pawn from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    
    elif piece == WHITE_ROOK or piece == BLACK_ROOK:
        if is_valid_rook_move(board, start_row, start_col, end_row, end_col):
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            print(f"Move successful: {piece} moved to ({end_row}, {end_col})")
            return True
        else:
            print(f"Invalid move for rook from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    
    elif piece == WHITE_BISHOP or piece == BLACK_BISHOP:
        if is_valid_bishop_move(board, start_row, start_col, end_row, end_col):
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            print(f"Move successful: {piece} moved to ({end_row}, {end_col})")
            return True
        else:
            print(f"Invalid move for bishop from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    
    elif piece == WHITE_KNIGHT or piece == BLACK_KNIGHT:
        if is_valid_knight_move(board, start_row, start_col, end_row, end_col):
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            print(f"Move successful: {piece} moved to ({end_row}, {end_col})")
            return True
        else:
            print(f"Invalid move for knight from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    
    elif piece == WHITE_QUEEN or piece == BLACK_QUEEN:
        if is_valid_queen_move(board, start_row, start_col, end_row, end_col):
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            print(f"Move successful: {piece} moved to ({end_row}, {end_col})")
            return True
        else:
            print(f"Invalid move for queen from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    
    elif piece == WHITE_KING or piece == BLACK_KING:
        if is_valid_king_move(board, start_row, start_col, end_row, end_col):
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            print(f"Move successful: {piece} moved to ({end_row}, {end_col})")
            return True
        else:
            print(f"Invalid move for king from ({start_row}, {start_col}) to ({end_row}, {end_col})")
    
    print(f"No valid piece at start position ({start_row}, {start_col})")
    return False  # Invalid move
"""
# pieces.py

# pieces.py
# pieces.py

def move_piece(board, start, end, check_only=False, screen =None):
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]
    target_piece = board[end_row][end_col]

    # Ensure we're not moving to a square occupied by a friendly piece
    if target_piece != EMPTY and ((piece.isupper() and target_piece.isupper()) or (piece.islower() and target_piece.islower())):
        return False  # Invalid move: cannot capture or move onto a friendly piece
    is_white = piece.isupper()
    if would_be_in_check(board, start, end, is_white):
        return False
    if piece == WHITE_PAWN or piece == BLACK_PAWN:
        is_white = piece == WHITE_PAWN
        if is_valid_pawn_move(board, start_row, start_col, end_row, end_col, is_white):
            if check_only:
                return True
            # Handle pawn promotion if it reaches the last rank
            if (is_white and end_row == 0) or (not is_white and end_row == 7):
                board[start_row][start_col] = EMPTY
                handle_pawn_promotion(board, end_row,end_col, is_white,screen)
            else:
                board[end_row][end_col] = piece
                board[start_row][start_col] = EMPTY
            return True
    
    elif piece == WHITE_ROOK or piece == BLACK_ROOK:
        if is_valid_rook_move(board, start_row, start_col, end_row, end_col):
            if check_only:
                return True
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            return True
    
    elif piece == WHITE_BISHOP or piece == BLACK_BISHOP:
        if is_valid_bishop_move(board, start_row, start_col, end_row, end_col):
            if check_only:
                return True
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            return True
    
    elif piece == WHITE_KNIGHT or piece == BLACK_KNIGHT:
        if is_valid_knight_move(board, start_row, start_col, end_row, end_col):
            if check_only:
                return True
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            return True
    
    elif piece == WHITE_QUEEN or piece == BLACK_QUEEN:
        if is_valid_queen_move(board, start_row, start_col, end_row, end_col):
            if check_only:
                return True
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            return True
    
    elif piece == WHITE_KING or piece == BLACK_KING:
        is_white = piece == WHITE_KING
        # Check for castling move
        if is_castling_move(board, start, end, is_white):
            if check_only:
                return True
            handle_castling(board, start, end, is_white)
            return True
        # Standard king move
        elif is_valid_king_move(board, start_row, start_col, end_row, end_col):
            if would_be_in_check(board, start, end, is_white):
                return False
            if check_only:
                return True
            board[end_row][end_col] = piece
            board[start_row][start_col] = EMPTY
            return True
    
    return False  # Invalid move







# Variable to track if kings and rooks have moved (needed for castling)
has_moved = {
    'white_king': False,
    'black_king': False,
    'white_rook_kingside': False,
    'white_rook_queenside': False,
    'black_rook_kingside': False,
    'black_rook_queenside': False,
}

def is_castling_move(board, start, end, is_white):
    # Kingside or Queenside castling check
    start_row, start_col = start
    end_row, end_col = end
    
    if is_white:
        if start == (7, 4) and end == (7, 6) and not has_moved['white_king'] and not has_moved['white_rook_kingside']:
            # Kingside castling for white
            if board[7][5] == EMPTY and board[7][6] == EMPTY:
                return 'kingside'
        elif start == (7, 4) and end == (7, 2) and not has_moved['white_king'] and not has_moved['white_rook_queenside']:
            # Queenside castling for white
            if board[7][1] == EMPTY and board[7][2] == EMPTY and board[7][3] == EMPTY:
                return 'queenside'
    else:
        if start == (0, 4) and end == (0, 6) and not has_moved['black_king'] and not has_moved['black_rook_kingside']:
            # Kingside castling for black
            if board[0][5] == EMPTY and board[0][6] == EMPTY:
                return 'kingside'
        elif start == (0, 4) and end == (0, 2) and not has_moved['black_king'] and not has_moved['black_rook_queenside']:
            # Queenside castling for black
            if board[0][1] == EMPTY and board[0][2] == EMPTY and board[0][3] == EMPTY:
                return 'queenside'
    
    return False

# Function to handle castling
def handle_castling(board, start, end, is_white):
    castling_type = is_castling_move(board, start, end, is_white)
    if castling_type == 'kingside':
        board[end[0]][end[1]] = board[start[0]][start[1]]  # Move king
        board[start[0]][start[1]] = EMPTY
        # Move the rook
        if is_white:
            board[7][5] = WHITE_ROOK
            board[7][7] = EMPTY
        else:
            board[0][5] = BLACK_ROOK
            board[0][7] = EMPTY
        return True
    elif castling_type == 'queenside':
        board[end[0]][end[1]] = board[start[0]][start[1]]  # Move king
        board[start[0]][start[1]] = EMPTY
        # Move the rook
        if is_white:
            board[7][3] = WHITE_ROOK
            board[7][0] = EMPTY
        else:
            board[0][3] = BLACK_ROOK
            board[0][0] = EMPTY
        return True
    return False


# Function to handle pawn promotion
# def handle_pawn_promotion(board, row, col, is_white):
#     if (is_white and row == 0) or (not is_white and row == 7):
#         promotion_choice = input(f"Promote pawn to (Q/R/B/N): ").upper()
#         if promotion_choice not in ['Q', 'R', 'B', 'N']:
#             promotion_choice = 'Q'  # Default to queen
#         board[row][col] = promotion_choice.upper() if is_white else promotion_choice.lower()

# pieces.py

def handle_pawn_promotion(board, row, col, is_white, screen):
    font = pygame.font.Font(None, 36)
    options = ['Q', 'R', 'B', 'N']
    texts = [font.render(option, True, (0, 0, 0)) for option in options]
    
    # Display the promotion options on the main screen
    screen.fill((200, 200, 200), pygame.Rect(250, 300, 300, 100))  # Clear a rectangle area for the choices
    for i, text in enumerate(texts):
        pygame.draw.rect(screen, (255, 255, 255), (250 + 75 * i, 325, 50, 50))
        screen.blit(text, (260 + 75 * i, 335))
    
    pygame.display.flip()

    # Wait for user to select a promotion piece
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                chosen_piece = None
                if 250 <= x <= 300:
                    chosen_piece = options[0]
                elif 325 <= x <= 375:
                    chosen_piece = options[1]
                elif 400 <= x <= 450:
                    chosen_piece = options[2]
                elif 475 <= x <= 525:
                    chosen_piece = options[3]

                if chosen_piece:
                    # Assign the chosen piece and return
                    promoted_piece = chosen_piece.upper() if is_white else chosen_piece.lower()
                    board[row][col] = promoted_piece  # Replace pawn with chosen piece
                    return


# pieces.py

def find_king_position(board, is_white):
    king = WHITE_KING if is_white else BLACK_KING
    for row in range(8):
        for col in range(8):
            if board[row][col] == king:
                return (row, col)
    return None

def is_in_check(board, is_white):
    king_position = find_king_position(board, is_white)
    if not king_position:
        return False  # If no king found, return False (edge case)

    # Loop through all pieces on the board to see if any can attack the king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != EMPTY and ((is_white and piece.islower()) or (not is_white and piece.isupper())):
                # If the piece is an opponent's, check if it can legally move to the king's position
                if move_piece(board, (row, col), king_position, check_only=True):
                    return True
    return False



def has_legal_moves(board, is_white):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != EMPTY and ((is_white and piece.isupper()) or (not is_white and piece.islower())):
                # Generate all possible moves for this piece
                for end_row in range(8):
                    for end_col in range(8):
                        if move_piece(board, (row, col), (end_row, end_col), check_only=True):
                            # Simulate move
                            original_piece = board[end_row][end_col]
                            board[end_row][end_col] = piece
                            board[row][col] = EMPTY

                            # Check if this move resolves check
                            in_check = is_in_check(board, is_white)

                            # Undo the move
                            board[row][col] = piece
                            board[end_row][end_col] = original_piece

                            if not in_check:
                                return True  # Found a legal move that resolves check
    return False





# pieces.py

def would_be_in_check(board, start, end, is_white):
    """Simulate a move and check if it would result in the king being in check."""
    # Backup the current pieces at start and end positions
    start_piece = board[start[0]][start[1]]
    end_piece = board[end[0]][end[1]]

    # Simulate the move
    board[start[0]][start[1]] = EMPTY
    board[end[0]][end[1]] = start_piece

    # Check if this move puts the king in check
    in_check = is_in_check(board, is_white)

    # Restore the board to its original state
    board[start[0]][start[1]] = start_piece
    board[end[0]][end[1]] = end_piece

    return in_check

