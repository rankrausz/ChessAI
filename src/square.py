from constants import *


class Square:

    def __init__(self, row, col, piece=None):  # piece
        self.row = row
        self.col = col
        self.piece = piece
        self.org_color = COLORS[(row + col) % 2]
        self.color = self.org_color
        self.possible = False

        self.seen_by_w = False
        self.seen_by_b = False

    def change_piece(self, piece):
        self.piece = piece

    def has_piece(self):
        return self.piece is not None

    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color

    def has_rival_piece(self, color):
        return self.has_piece() and self.piece.color != color

    def is_empty(self):
        return not self.has_piece()

    def is_empty_or_rival(self, color):
        return self.is_empty() or self.has_rival_piece(color)

    def piece_clicked(self):
        if self.piece:
            if self.piece.clicked:
                return True
        return False

    def __str__(self):
        return "(" + str(self.row) + "," + str(self.col) + ")"

    def __repr__(self):
        return str(self)

    @staticmethod
    def in_range(*args):
        for num in args:
            if num < 0 or num > 7:
                return False
        return True
