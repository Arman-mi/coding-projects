# graphics.py

import pygame
import os
import sys

# Constants for display
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8

# Define colors for the chessboard
LIGHT_SQUARE = (245, 222, 179)  # Light beige color
DARK_SQUARE = (139, 69, 19)     # Dark brown color

# Dictionary for piece images
piece_images = {}

def resource_path(relative_path):
    # Get the absolute path for PyInstaller bundle or development
    try:
        # PyInstaller creates a temporary folder in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_images():
    pieces = {
        'P': 'wp', 'R': 'wr', 'N': 'wn', 'B': 'wb', 'Q': 'wq', 'K': 'wk',
        'p': 'bp', 'r': 'br', 'n': 'bn', 'b': 'bb', 'q': 'bq', 'k': 'bk'
    }
    for piece, filename in pieces.items():
        image_path = resource_path(f'images/{filename}.png')

        piece_images[piece] = pygame.image.load(image_path)
        piece_images[piece] = pygame.transform.scale(piece_images[piece], (SQUARE_SIZE, SQUARE_SIZE))

def initialize_screen():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    return screen

# Draw chessboard
def draw_board(screen):
    colors = [LIGHT_SQUARE, DARK_SQUARE]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces on the board
def draw_pieces(screen, board):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != " ":
                screen.blit(piece_images[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Convert mouse position to board coordinates
def get_board_position(mouse_pos):
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col
