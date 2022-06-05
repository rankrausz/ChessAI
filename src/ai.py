from board import Board
import numpy
from constants import *


class AI:
    INFINITY = 100000000
    COLORS = ["black", "white"]
    COUNT = 0

    def __init__(self, board):
        self.board = board

    @staticmethod
    def evaluate(position: Board):
        evaluation = 0
        for row in range(ROWS):
            for col in range(COLS):
                square = position.squares[row][col]
                if square.piece:
                    sign = EVAL_SIGN[square.piece.color]  # minus for black, plus for white
                    evaluation += sign * square.piece.VALUE  # add pieces values
                    # now add piece-on-square value
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

        # white move
        if maximizing:
            max_eval = -AI.INFINITY
            moves = board.all_moves('white')
            # AI.order_moves(moves, 'white')
            for move in moves:
                board.make_move(move)
                max_eval = max(max_eval, AI.minimax(board, depth-1, alpha, beta, False))
                board.undo_move(move)
                # update alpha
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break  # prune
            return max_eval

        # black move
        else:
            min_eval = AI.INFINITY
            moves = board.all_moves('black')
            # AI.order_moves(moves, 'black')
            for move in moves:
                board.make_move(move)
                min_eval = min(min_eval, AI.minimax(board, depth-1, alpha, beta, True))
                board.undo_move(move)
                # update beta
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break  # prune
            return min_eval

    @staticmethod
    def negamax(board, depth, alpha, beta, color):
        if depth == 0:
            return AI.evaluate(board)

        moves = board.all_moves(AI.COLORS[color])
        for move in moves:
            board.make_move(move)
            score = -AI.negamax(board, depth-1, -beta, -alpha, not color)
            board.undo_move(move)
            alpha = max(alpha, score)
            if beta <= alpha:
                return score
        return score

    @staticmethod
    def order_moves(moves, color):
        for move in moves:
            if move.target.has_rival_piece(color):
                move.score_guess += 10 * (move.target.piece.VALUE - move.start.piece.VALUE)

        def get_score_guess(move_t):
            return move_t.score_guess

        moves.sort(key=get_score_guess)



