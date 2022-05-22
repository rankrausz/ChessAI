from constants import *
from square import Square
from piece import *
from move import Move
import copy


class Board:

    def __init__(self):
        self.squares = []
        self.clicked_square = None
        self.possible_moves = []

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

        # knights
        for col in [1, 6]:
            knight = Knight(color)
            knight.pos = (other_row, col)
            self.squares[other_row][col].change_piece(knight)

        # bishops
        for col in [2, 5]:
            bishop = Bishop(color)
            bishop.pos = (other_row, col)
            self.squares[other_row][col].change_piece(bishop)

        # rooks
        for col in [0, 7]:
            rook = Rook(color)
            rook.pos = (other_row, col)
            self.squares[other_row][col].change_piece(Rook(color))

        # queen
        queen = Queen(color)
        queen.pos = (other_row, 3)
        self.squares[other_row][3].change_piece(queen)

        # king
        king = King(color)
        king.pos = (other_row, 4)
        self.squares[other_row][4].change_piece(king)

    # ============================= Moving Functions =============================

    def can_move(self, move):
        """
        try a move to see if there is check
        """
        ret = True

        # save r/l castle values
        l_castle = move.l_castle
        r_castle = move.r_castle
        move.l_castle, move.r_castle = False, False  # changed in order to make move normally
        # will be restored later
        # saving original pieces
        start_piece = move.start.piece
        target_piece = move.target.piece

        # copying pieces to perform moves on them
        tmp_start_piece = copy.deepcopy(start_piece)
        tmp_target_piece = copy.deepcopy(target_piece)

        # switching to copied pieces
        move.start.piece = tmp_start_piece
        move.target.piece = tmp_target_piece

        self.make_move(move)  # making the move

        if self.in_check(start_piece.color):
            ret = False

        self.make_reverse_move(move)  # un-making the move

        # returning the original pieces to their
        move.start.piece = start_piece
        move.target.piece = target_piece

        move.l_castle = l_castle
        move.r_castle = r_castle

        if r_castle:
            # need to also check king move one square right
            target = self.squares[move.start.row][5]  # one step right
            return ret and self.can_move(Move(move.start, target))

        if l_castle:
            # need to also check king move one square left
            target = self.squares[move.start.row][3]  # one step left
            return ret and self.can_move(Move(move.start, target))

        return ret

    def make_move(self, move):
        """
        move piece from start to target square
        """
        if move.l_castle:
            # move king
            only_king_move = Move(move.start, move.target)
            self.make_move(only_king_move)

            # move rook
            rook_square = self.squares[move.start.row][0]
            rook_final = self.squares[move.start.row][3]
            self.make_move(Move(rook_square, rook_final))
            return

        if move.r_castle:
            # move king
            only_king_move = Move(move.start, move.target)
            self.make_move(only_king_move)

            # move rook
            rook_square = self.squares[move.start.row][7]
            rook_final = self.squares[move.start.row][5]
            self.make_move(Move(rook_square, rook_final))
            return

        piece = move.start.piece
        move.start.change_piece(None)
        move.target.change_piece(piece)
        piece.moved = True

    def make_reverse_move(self, move):
        start = move.target
        target = move.start
        self.make_move(Move(start, target))

        if move.r_castle:  # return the right rook
            # move is king(row, 4) -> (row, 6)
            # rook in (row, 5) needs to get back to (row, 7)
            row = move.start.row
            start = self.squares[row][5]
            target = self.squares[row][7]
            self.make_move(Move(start, target))

        if move.r_castle:  # return the left rook
            # rook in (row, 3) needs to get back to (row, 0)
            row = move.start.row
            start = self.squares[row][3]
            target = self.squares[row][0]
            self.make_move(Move(start, target))

    def can_castle(self, color):
        """
        :returns list of 2 bools, [can_castle_left_side, can_castle_right_side]
        """
        can_castle_left_side, can_castle_right_side = False, False
        king_square = self.get_king_square(color)
        row = king_square.row
        col = king_square.col

        if king_square.piece.moved:
            return [False, False]

        right_rook = self.squares[row][7].piece
        if right_rook:
            if right_rook.name == "rook" and not right_rook.moved \
                                         and not self.squares[row][col + 1].piece \
                                         and not self.squares[row][col + 2].piece:
                # these are the conditions for castling
                can_castle_right_side = True

        left_rook = self.squares[row][0].piece
        if left_rook:
            if left_rook.name == "rook" and not left_rook.moved \
                    and not self.squares[row][col - 1].piece \
                    and not self.squares[row][col - 2].piece \
                    and not self.squares[row][col - 3].piece:
                can_castle_left_side = True

        return [can_castle_left_side, can_castle_right_side]

    # ========================= Calculating possible moves ========================

    def calc_moves(self, piece, row, col):
        """
        calculate all possible moves for a piece in a specific location (row, col)
        :return a list of locations (row, col) representing possible new location
        """
        moves = []
        if piece.name == "pawn":
            moves = self.pawn_moves(piece, row, col)

        elif piece.name == "knight":
            moves = self.knight_moves(piece, row, col)

        elif piece.name == "king":
            moves = self.king_moves(piece, row, col)

        # bishop, rook or queen
        else:
            moves = self.line_moves(piece, row, col)

        ret = []
        # start = self.squares[row][col]
        for move in moves:
            if self.can_move(move):
                ret.append(move)

        return ret

    def knight_moves(self, knight, row, col):
        directions = knight.DIRECTIONS  # all knight moves
        start = self.squares[row][col]  # starting square of the knight
        ret = []

        # iterate all squares to see if its a valid move
        for add_to_row, add_to_col in directions:
            # calculate new square coordinates to check
            move_row = row + add_to_row
            move_col = col + add_to_col
            if Square.in_range(move_row, move_col):
                if self.squares[move_row][move_col].is_empty_or_rival(knight.color):
                    # valid move, add to returned list
                    target = self.squares[move_row][move_col]
                    ret.append(Move(start, target))
        return ret

    def pawn_moves(self, pawn, row, col):
        start = self.squares[row][col]
        updown = pawn.direction  # 1 for black, -1 for white
        ret = []

        # take moves
        take_moves = [(row + updown, col - 1), (row + updown, col + 1)]
        for move_row, move_col in take_moves:
            if Square.in_range(move_row, move_col):
                if self.squares[move_row][move_col].has_rival_piece(pawn.color):
                    # valid move, add to returned list
                    target = self.squares[move_row][move_col]
                    ret.append(Move(start, target))

        # checking one step forward
        move_row, move_col = row + updown, col
        if Square.in_range(move_row, move_col):
            if self.squares[move_row][move_col].is_empty():
                target = self.squares[move_row][move_col]
                ret.append(Move(start, target))

        # checking two steps forward
        if not pawn.moved:
            move_row, move_col = row + 2 * updown, col
            if Square.in_range(move_row, move_col):
                if not self.squares[move_row][move_col].has_piece():
                    target = self.squares[move_row][move_col]
                    ret.append(Move(start, target))
        return ret

    def line_moves(self, piece, row, col):
        ret = []
        start = self.squares[row][col]
        directions = piece.DIRECTIONS
        #
        # start, end = 0, 8
        # if piece.name == "rook":  # only straight
        #     start, end = 0, 4
        # elif piece.name == "bishop":  # only diagonal
        #     start, end = 4, 8

        def valid_move(r, c):
            # check if next move is valid
            if Square.in_range(r, c):
                if self.squares[r][c].is_empty_or_rival(piece.color):
                    return True
            return False

        for add_to_row, add_to_col in directions:
            move_row, move_col = row, col
            while valid_move(move_row + add_to_row, move_col + add_to_col):
                # valid, add it to returned list
                target = self.squares[move_row + add_to_row][move_col + add_to_col]
                ret.append(Move(start, target))
                if self.squares[move_row + add_to_row][move_col + add_to_col].has_rival_piece(piece.color):
                    break
                move_row += add_to_row
                move_col += add_to_col
        return ret

    def king_moves(self, piece, row, col):
        directions = King.DIRECTIONS
        start = self.squares[row][col]
        ret = []

        def valid_king_move(r, c):
            # check if next move is valid
            if Square.in_range(r, c):
                rival_sees = self.rival_sees(piece.color)
                square = self.squares[r][c]
                # print(rival_sees)
                return self.squares[r][c].is_empty_or_rival(piece.color) and square not in rival_sees
            return False

        for add_to_row, add_to_col in directions:
            if valid_king_move(row + add_to_row, col + add_to_col):
                target = self.squares[row + add_to_row][col + add_to_col]
                ret.append(Move(start, target))

        # castling
        can_castle = self.can_castle(piece.color)
        if any(can_castle):
            if can_castle[0]:  # left (long) castle
                target = self.squares[row][col - 2]
                castle = Move(start, target)
                castle.l_castle = True
                ret.append(castle)
            if can_castle[1]:  # right (short) castle
                target = self.squares[row][col + 2]
                castle = Move(start, target)
                castle.r_castle = True
                ret.append(castle)
        return ret

    # ============================= Calculating sees ===============================

    def calc_sees(self, piece, row, col):
        """
        calculate what squares a piece sees
        """
        ret = []
        if piece.name == "pawn":
            updown = piece.direction  # 1 for black, -1 for white
            take_moves = [(row + updown, col - 1), (row + updown, col + 1)]
            for move_row, move_col in take_moves:
                if Square.in_range(move_row, move_col):
                    ret.append(self.squares[move_row][move_col])
            return ret

        elif piece.name == "knight":
            for move in self.knight_moves(piece, row, col):
                ret.append(move.target)
            return ret

        elif piece.name == "king":
            return self.king_sees(row, col)

        # bishop, rook or queen
        else:
            for move in self.line_moves(piece, row, col):
                ret.append(move.target)
            return ret

    def king_sees(self, row, col):
        """
        returns list of squares a king in (row, col) sees
        """
        ret = []
        directions = King.DIRECTIONS
        for add_to_row, add_to_col in directions:
            if Square.in_range(row+add_to_row, col+add_to_col):
                ret.append(self.squares[row+add_to_row][col+add_to_col])
        return ret

    def rival_sees(self, color):
        """
        returns list of squares rival sees
        """
        # color is the color of the player (not rival)
        ret = []
        piece_squares = self.get_rival_pieces(color)
        for square in piece_squares:
            ret += self.calc_sees(square.piece, square.row, square.col)
        # if color == "black":
        #     for piece in self.white_pieces:
        #         ret += self.calc_sees(piece, piece.pos[0], piece.pos[1])  # prettier
        # else:
        #     for piece in self.black_pieces:
        #         ret += self.calc_sees(piece, piece.pos[0], piece.pos[1])
        return ret

    # =========================== Game, get's & others ===============================

    def game_over(self, color):
        all_moves = []
        rival_pieces = self.get_rival_pieces(color)
        for square in rival_pieces:
            all_moves += self.calc_moves(square.piece, square.row, square.col)
        # print(all_moves)
        if not all_moves:  # no moves
            return True
        return False

    def get_rival_pieces(self, color):
        """
        returns list of all squares containing pieces that doesn't belong to 'color'
        """
        ret = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_rival_piece(color):
                    ret.append(self.squares[row][col])
        return ret

    def get_team_pieces(self, color):
        """
        returns list of all squares containing pieces that belong to 'color'
        """
        ret = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(color):
                    ret.append(self.squares[row][col])
        return ret

    def get_king_square(self, color):
        team_squares = self.get_team_pieces(color)
        for square in team_squares:
            if square.piece.name == "king":
                return square

    def get_move_from_target(self, target):
        for move in self.possible_moves:
            if move.target == target:
                return move

    def in_check(self, color):
        """
        color player is in check
        """
        rival_sees = self.rival_sees(color)
        for square in rival_sees:
            # square = move.target
            if square.has_team_piece(color):
                if square.piece.name == "king":
                    return True
        return False

    def target_squares(self):
        ret = []
        for move in self.possible_moves:
            ret.append(move.target)
        return ret


