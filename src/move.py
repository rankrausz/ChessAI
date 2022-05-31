import copy
from square import Square


class Move:

    def __init__(self, start: Square, target: Square):
        self.start = start
        self.target = target
        self.s_piece = copy.deepcopy(start.piece)
        self.t_piece = copy.deepcopy(target.piece)
        self.l_castle = False
        self.r_castle = False
        self.rook_move = None

        self.score_guess = 0

    def __str__(self):
        s = ''
        s += f'({self.start.row}, {self.start.col})'
        s += f' -> ({self.target.row}, {self.target.col})'
        return s

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.start == other.start and self.target == other.target

    def is_castling(self):
        return self.l_castle or self.r_castle

    def get_score_guess(self):
        return self.score_guess

