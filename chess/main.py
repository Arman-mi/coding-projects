# main.py

import pygame
import sys
from board import initialize_board
from pieces import move_piece, has_legal_moves, is_in_check
from Graphics import initialize_screen, load_images, draw_board, draw_pieces, get_board_position
from simple_ai import choose_random_move

def play_game():
    # Initialize the screen and load images
    pygame.init()
    screen = initialize_screen()
    load_images()

    # Initialize the chessboard and game state
    board = initialize_board()
    selected_piece = None
    selected_pos = None
    is_white_turn = True

    # Main game loop
    while True:
        if is_white_turn:
            # Player's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = get_board_position(pygame.mouse.get_pos())

                    if selected_piece is None:
                        # Selecting a piece to move
                        piece = board[pos[0]][pos[1]]
                        if piece != " " and piece.isupper():  # White's turn, so must be an uppercase piece
                            selected_piece = piece
                            selected_pos = pos
                            print(f"Selected {piece} at {selected_pos}")
                    else:
                        # Moving the selected piece to the new position
                        if move_piece(board, selected_pos, pos, screen= screen):
                            print(f"Moved {selected_piece} from {selected_pos} to {pos}")
                            is_white_turn = False  # Switch turns after a valid move
                        selected_piece = None
                        selected_pos = None

        else:
            # AI's turn (black)
            ai_move = choose_random_move(board)
            if ai_move:
                start, end = ai_move
                print(f"AI is moving from {start} to {end}")
                move_piece(board, start, end, screen = screen)
                pygame.display.flip()
                pygame.time.delay(1)
                is_white_turn = True  # Switch back to player's turn
            else:
                print("No valid moves for AI; exiting.")
                pygame.quit()
                sys.exit()
        
        if is_in_check(board, not is_white_turn):
            if not has_legal_moves(board, not is_white_turn):
                winner = "White" if is_white_turn else "Black"
                print(f"Checkmate! {winner} wins.")
                pygame.quit()
                sys.exit()
        # Draw board and pieces
        draw_board(screen)
        draw_pieces(screen, board)
        
        pygame.display.flip()

if __name__ == "__main__":
    play_game()
