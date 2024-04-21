"""
Contains the functions that build the board and the interactive GUI, including pieces.
"""

import os
import logging
import tkinter as tk
import chess
from PIL import Image, ImageTk

logging.basicConfig(level='INFO')

class ChessBoard:
    """Class representing a chess board with interactive GUI."""

    def __init__(self, root, square_size=80):
        """Initialize the ChessBoard instance."""
        self.root = root
        self.square_size = square_size
        self.canvas = tk.Canvas(root, width=8 * square_size, height=8 * square_size)
        self.canvas.pack()
        self.board = chess.Board()
        self.board_pieces = {}
        self.square_coordinates = {}
        self.image_dir = os.path.join(os.path.dirname(__file__), "pieces")

    def create_chess_board(self):
        """Create the tkinter canvas, build the chess board, and place pieces."""
        self._build_chess_board()
        self._place_board_pieces()

    def _build_chess_board(self):
        """Build the chess board on the canvas."""
        for row in range(8):
            for col in range(8):
                self._create_chess_square(row, col)

    def _create_chess_square(self, row, col):
        """Create a single chess square on the canvas."""
        x1, y1 = col * self.square_size, row * self.square_size
        x2, y2 = x1 + self.square_size, y1 + self.square_size
        color = "white" if (row + col) % 2 == 0 else "gray"
        square_index = chess.square(col, 7 - row)
        centre_x, centre_y = (x1 + x2) / 2, (y1 + y2) / 2

        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
        self.square_coordinates[square_index] = (centre_x, centre_y)

        self._place_piece_on_square(square_index, centre_x, centre_y)

    def _place_piece_on_square(self, square_index, centre_x, centre_y):
        """Place a piece on the given square if it exists."""
        piece = self.board.piece_at(square_index)
        if piece:
            piece_color = "white" if piece.color == chess.WHITE else "black"
            piece_type = chess.piece_name(piece.piece_type)
            filename = f"{piece_color}_{piece_type}.png"
            image_path = os.path.join(self.image_dir, filename)

            piece_image = Image.open(image_path)
            piece_image = piece_image.resize((
                int(self.square_size * 0.9),
                int(self.square_size * 0.9)
            ))
            piece_image_tk = ImageTk.PhotoImage(piece_image)
            self.board_pieces[(centre_x, centre_y)] = piece_image_tk

    def _place_board_pieces(self):
        """
        Place all pieces stored in board_pieces onto the canvas.
        """
        for (centre_x, centre_y), piece_image_tk in self.board_pieces.items():
            self.canvas.create_image(centre_x, centre_y, image=piece_image_tk)
