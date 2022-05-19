from constants import *
from square import Square
from piece import *


class Board:

    def __init__(self):
        self.squares = []
        self.clicked_square = None
        self.possible_squares = []
        self.white_pieces = []
        self.black_pieces = []
        self.white_sees = []
        self.black_sees = []

        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def _create(self):  # private methods
        """
        create square instances
        """
        self.squares = [[] for col in range(COLS)]  # empty 8X8 list

        for row in range(ROWS):
            for col in range(COLS):
                new_square = Square(row, col)
                self.squares[row].append(new_square)

    def add_to_player_pieces(self, color, piece):
        if color == "white":
            self.white_pieces.append(piece)
        else:
            self.black_pieces.append(piece)

    def _add_pieces(self, color):
        """
        add all pieces of single color to the starting positions
        """
        pawn_row, other_row = (6, 7) if color == "white" else (1, 0)

        # self.squares[3][4].change_piece(King("white"))

        # pawns
        for col in range(COLS):
            pawn = Pawn(color)
            pawn.pos = (pawn_row, col)
            self.squares[pawn_row][col].change_piece(pawn)
            self.add_to_player_pieces(color, pawn)

        # knights
        for col in [1, 6]:
            knight = Knight(color)
            knight.pos = (other_row, col)
            self.squares[other_row][col].change_piece(knight)
            self.add_to_player_pieces(color, knight)

        # bishops
        for col in [2, 5]:
            bishop = Bishop(color)
            bishop.pos = (other_row, col)
            self.squares[other_row][col].change_piece(bishop)
            self.add_to_player_pieces(color, bishop)

        # rooks
        for col in [0, 7]:
            rook = Rook(color)
            rook.pos = (other_row, col)
            self.squares[other_row][col].change_piece(Rook(color))
            self.add_to_player_pieces(color, rook)

        # queen
        queen = Queen(color)
        queen.pos = (other_row, 3)
        self.squares[other_row][3].change_piece(queen)
        self.add_to_player_pieces(color, queen)

        # king
        king = King(color)
        king.pos = (other_row, 4)
        self.squares[other_row][4].change_piece(king)
        self.add_to_player_pieces(color, king)

    def make_move(self, piece, target):
        """
        move piece to target square
        """

        self.clicked_square.change_piece(None)
        target.change_piece(piece)
        piece.moved = True

    def get_square(self, piece):
        """
        get the square holding a certain piece
        """
        for square_row in self.squares:
            for square in square_row:
                if square.piece == piece:
                    return square

    def knight_moves(self, knight, row, col):
        all_moves = [
            (row+2, col+1),
            (row+2, col-1),
            (row+1, col+2),
            (row+1, col-2),
            (row-1, col+2),
            (row-1, col-2),
            (row-2, col+1),
            (row-2, col-1)
        ]
        ret = []
        for move_row, move_col in all_moves:
            if Square.in_range(move_row, move_col):
                if self.squares[move_row][move_col].is_empty_or_rival(knight.color):
                    ret.append((move_row, move_col))
        return ret

    def pawn_moves(self, pawn, row, col):
        dir = pawn.direction
        ret = []

        # take moves
        take_moves = [(row + dir, col - 1), (row + dir, col + 1)]
        for move_row, move_col in take_moves:
            if Square.in_range(move_row, move_col):
                if self.squares[move_row][move_col].has_rival_piece(pawn.color):
                    ret.append((move_row, move_col))

        # checking one step forward
        move_row, move_col = row + dir, col
        if Square.in_range(move_row, move_col):
            if self.squares[move_row][move_col].is_empty():
                ret.append((move_row, move_col))

        # checking two steps forward
        if not pawn.moved:
            move_row, move_col = row + 2 * dir, col
            if Square.in_range(move_row, move_col):
                if not self.squares[move_row][move_col].has_piece():
                    ret.append((move_row, move_col))

        return ret

    def line_moves(self, piece, row, col):
        ret = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        # 0-3 are straight line moves, 4-7 are diagonal
        start, end = 0, 8
        if piece.name == "rook":  # only straight
            start, end = 0, 4
        elif piece.name == "bishop":  # only diagonal
            start, end = 4, 8

        def valid_move(r, c):
            # check if next move is valid
            if Square.in_range(r, c):
                if self.squares[r][c].is_empty_or_rival(piece.color):
                    return True
            return False

        for i, j in directions[start:end]:  # i is medial direction, j is lateral (side to side)
            move_row, move_col = row, col
            while valid_move(move_row + i, move_col + j):
                ret.append((move_row + i, move_col + j))
                if self.squares[move_row + i][move_col + j].has_rival_piece(piece.color):
                    break
                move_row += i
                move_col += j
        return ret

    def king_moves(self, piece, row, col):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        ret = []
        move_row, move_col = row, col

        def valid_king_move(r, c):
            # check if next move is valid
            if Square.in_range(r, c):
                rival_sees = self.rival_sees(piece.color)
                # print(rival_sees)
                return self.squares[r][c].is_empty_or_rival(piece.color) and (r, c) not in rival_sees
            return False

        for i, j in directions:
            if valid_king_move(move_row + i, move_col + j):
                ret.append((move_row + i, move_col + j))
        return ret

    def king_sees(self, piece, row, col):
        ret = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for i, j in directions:
            if Square.in_range(row+i, col+j):
                ret.append((row+i, col+j))
        return ret

    def calc_moves(self, piece, row, col):
        """
        calculate all possible moves for a piece in a specific location (row, col)
        :return a list of locations (row, col) representing possible new location
        """
        if piece.name == "pawn":
            return self.pawn_moves(piece, row, col)

        elif piece.name == "knight":
            return self.knight_moves(piece, row, col)

        elif piece.name == "king":
            return self.king_moves(piece, row, col)

        # bishop, rook or queen
        else:
            return self.line_moves(piece, row, col)

    def calc_sees(self, piece, row, col):
        """
        calculate what squares a piece sees
        """
        if piece.name == "pawn":
            dir = piece.direction
            ret = []
            take_moves = [(row + dir, col - 1), (row + dir, col + 1)]
            for move_row, move_col in take_moves:
                if Square.in_range(move_row, move_col):
                    ret.append((move_row, move_col))
            return ret

        elif piece.name == "knight":
            return self.knight_moves(piece, row, col)

        elif piece.name == "king":
            return self.king_sees(piece, row, col)

        # bishop, rook or queen
        else:
            return self.line_moves(piece, row, col)

    def rival_sees(self, color):
        ret = []
        if color == "black":
            for piece in self.white_pieces:
                ret += self.calc_sees(piece, piece.pos[0], piece.pos[1])  # prettier
        else:
            for piece in self.black_pieces:
                ret += self.calc_sees(piece, piece.pos[0], piece.pos[1])
        return ret

