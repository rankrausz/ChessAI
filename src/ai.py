from board import Board
import numpy
from constants import *
from move import Move

# from piece import Piece
# from square import Square
import copy


class AI:
    INFINITI = 100000000
    COUNT = 0

    def __init__(self, board):
        self.board = board
        self.count = 0

    @staticmethod
    def evaluate(position: Board):
        evaluation = 0
        for row in range(ROWS):
            for col in range(COLS):
                square = position.squares[row][col]
                if square.piece:
                    sign = EVAL_SIGN[square.piece.color]
                    evaluation += sign * square.piece.VALUE
                    if square.piece.color == 'white':
                        evaluation += sign * square.piece.SQ_TABLE[row][col]
                    else:
                        evaluation += sign * numpy.flipud(square.piece.SQ_TABLE)[row][col]

        return evaluation

    @staticmethod
    def minimax(board, depth, alpha, beta, maximizing):
        if depth == 0:
            AI.COUNT += 1
            return AI.evaluate(board)

        if maximizing:
            max_eval = -AI.INFINITI
            for move in board.all_moves('white'):
                sr, sc, tr, tc = move.start.row, move.start.col, move.target.row, move.target.col
                copied = board.clone()
                cmove = Move(copied.squares[sr][sc], copied.squares[tr][tc])
                copied.make_move(cmove)
                max_eval = max(max_eval, AI.minimax(copied, depth - 1, alpha, beta, False))

                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = AI.INFINITI
            for move in board.all_moves('black'):
                sr, sc, tr, tc = move.start.row, move.start.col, move.target.row, move.target.col
                copied = board.clone()
                cmove = Move(copied.squares[sr][sc], copied.squares[tr][tc])
                copied.make_move(cmove)

                min_eval = min(min_eval, AI.minimax(copied, depth - 1, alpha, beta, True))

                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval





