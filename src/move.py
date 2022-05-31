
class Move:

    def __init__(self, start, target):
        self.start = start
        self.target = target
        self.l_castle = False
        self.r_castle = False

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

