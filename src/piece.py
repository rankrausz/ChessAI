import os
from constants import *

class Piece:

    def __init__(self, name, color, value, pos, image_path=None, img_frame=None):
        self.name = name
        self.color = color
        self.pos = pos

        self.moves = []
        self.moved = False
        self.clicked = False

        value_sign = 1 if color == "white" else -1
        self.value = value_sign * value

        self.image_path = image_path
        self.set_image()

        self.img_frame = img_frame

    def set_image(self, size=60):
        self.image_path = os.path.join(f'images/imgs-{size}px/{self.color}_{self.name}.png')  # und

    def add_move(self, move):
        self.moves.append(move)

    def __str__(self):
        return(self.name)


class Pawn(Piece):
    VALUE = 1.0

    def __init__(self, color):
        self.direction = -1 if color == "white" else 1  # one step up is -1 in coordinate
        super().__init__("pawn", color, Pawn.VALUE, INIT_POS)  # understand


class Knight(Piece):
    VALUE = 3.0
    DIRECTIONS = [
        (2, 1),
        (2, -1),
        (1, 2),
        (1, -2),
        (-1, 2),
        (-1, -2),
        (-2, 1),
        (-2, -1)
    ]

    def __init__(self, color):
        super().__init__("knight", color, Knight.VALUE, INIT_POS)


class Bishop(Piece):
    VALUE = 3.001
    DIRECTIONS = [
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]

    def __init__(self, color):
        super().__init__("bishop", color, Bishop.VALUE, INIT_POS)


class Rook(Piece):
    VALUE = 5.0
    DIRECTIONS = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    def __init__(self, color):
        super().__init__("rook", color, Rook.VALUE, INIT_POS)


class Queen(Piece):
    VALUE = 9.0
    DIRECTIONS = Bishop.DIRECTIONS + Rook.DIRECTIONS

    def __init__(self, color):
        super().__init__("queen", color, Queen.VALUE, INIT_POS)


class King(Piece):
    VALUE = 3.0
    DIRECTIONS = Queen.DIRECTIONS

    def __init__(self, color):
        super().__init__("king", color, 100000.0, INIT_POS)
