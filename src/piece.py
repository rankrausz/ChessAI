import os
from constants import *
import numpy


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
    VALUE = 100
    SQ_TABLE = numpy.array([[0,  0,  0,  0,  0,  0,  0,  0],
                            [50, 50, 50, 50, 50, 50, 50, 50],
                            [10, 10, 20, 30, 30, 20, 10, 10],
                            [ 5,  5, 10, 25, 25, 10,  5,  5],
                            [ 0,  0,  0, 20, 20,  0,  0,  0],
                            [ 5, -5,-10,  0,  0,-10, -5,  5],
                            [ 5, 10, 10,-20,-20, 10, 10,  5],
                            [ 0,  0,  0,  0,  0,  0,  0,  0]])

    def __init__(self, color):
        self.direction = -1 if color == "white" else 1  # one step up is -1 in coordinate
        super().__init__("pawn", color, Pawn.VALUE, INIT_POS)  # understand


class Knight(Piece):
    VALUE = 320
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
    SQ_TABLE = numpy.array([[-50,-40,-30,-30,-30,-30,-40,-50],
                            [-40,-20,  0,  0,  0,  0,-20,-40],
                            [-30,  0, 10, 15, 15, 10,  0,-30],
                            [-30,  5, 15, 20, 20, 15,  5,-30],
                            [-30,  0, 15, 20, 20, 15,  0,-30],
                            [-30,  5, 10, 15, 15, 10,  5,-30],
                            [-40,-20,  0,  5,  5,  0,-20,-40],
                            [-50,-40,-30,-30,-30,-30,-40,-50]])

    def __init__(self, color):
        super().__init__("knight", color, Knight.VALUE, INIT_POS)


class Bishop(Piece):
    VALUE = 330
    DIRECTIONS = [
        (1, 1),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]
    SQ_TABLE = numpy.array([[-20,-10,-10,-10,-10,-10,-10,-20],
                            [-10,  0,  0,  0,  0,  0,  0,-10],
                            [-10,  0,  5, 10, 10,  5,  0,-10],
                            [-10,  5,  5, 10, 10,  5,  5,-10],
                            [-10,  0, 10, 10, 10, 10,  0,-10],
                            [-10, 10, 10, 10, 10, 10, 10,-10],
                            [-10,  5,  0,  0,  0,  0,  5,-10],
                            [-20,-10,-10,-10,-10,-10,-10,-20]])

    def __init__(self, color):
        super().__init__("bishop", color, Bishop.VALUE, INIT_POS)


class Rook(Piece):
    VALUE = 500
    DIRECTIONS = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]
    SQ_TABLE = numpy.array([[ 0,  0,  0,  0,  0,  0,  0,  0],
                           [ 5, 10, 10, 10, 10, 10, 10,  5],
                           [-5,  0,  0,  0,  0,  0,  0, -5],
                           [-5,  0,  0,  0,  0,  0,  0, -5],
                           [-5,  0,  0,  0,  0,  0,  0, -5],
                           [-5,  0,  0,  0,  0,  0,  0, -5],
                           [-5,  0,  0,  0,  0,  0,  0, -5],
                           [ 0,  0,  0,  5,  5,  0,  0,  0]])

    def __init__(self, color):
        super().__init__("rook", color, Rook.VALUE, INIT_POS)


class Queen(Piece):
    VALUE = 900
    DIRECTIONS = Bishop.DIRECTIONS + Rook.DIRECTIONS
    SQ_TABLE = numpy.array([[-20,-10,-10, -5, -5,-10,-10,-20],
                           [-10,  0,  0,  0,  0,  0,  0,-10],
                           [-10,  0,  5,  5,  5,  5,  0,-10],
                           [ -5,  0,  5,  5,  5,  5,  0, -5],
                           [  0,  0,  5,  5,  5,  5,  0, -5],
                           [-10,  5,  5,  5,  5,  5,  0,-10],
                           [-10,  0,  5,  0,  0,  0,  0,-10],
                           [-20,-10,-10, -5, -5,-10,-10,-20]])

    def __init__(self, color):
        super().__init__("queen", color, Queen.VALUE, INIT_POS)


class King(Piece):
    VALUE = 20000
    DIRECTIONS = Queen.DIRECTIONS
    SQ_TABLE = numpy.array([[-30,-40,-40,-50,-50,-40,-40,-30],
                            [-30,-40,-40,-50,-50,-40,-40,-30],
                            [-30,-40,-40,-50,-50,-40,-40,-30],
                            [-30,-40,-40,-50,-50,-40,-40,-30],
                            [-20,-30,-30,-40,-40,-30,-30,-20],
                            [-10,-20,-20,-20,-20,-20,-20,-10],
                            [ 20, 20,  0,  0,  0,  0, 20, 20],
                            [ 20, 30, 10,  0,  0, 10, 30, 20]])

    def __init__(self, color):
        super().__init__("king", color, 100000.0, INIT_POS)
