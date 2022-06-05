from constants import *
from square import Square
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = []
        self.clicked_square = None
        self.possible_moves = []
        self.last_squares = []

        self._create()
        self._add_pieces_fen(START_FEN)

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

    def _add_pieces_fen(self, fen: str):
        squares = self.squares
        colors = ['white', 'black']
        row, col = 0, 0
        for char in fen:
            if char.isdigit():
                col += int(char)
            elif char == '/':
                row += 1
                col = 0
            else:
                color = colors[char.islower()]
                char = char.lower()
                if char == 'p':
                    pawn = Pawn(color)
                    squares[row][col].change_piece(pawn)
                elif char == 'b':
                    bishop = Bishop(color)
                    squares[row][col].change_piece(bishop)
                elif char == 'n':
                    knight = Knight(color)
                    squares[row][col].change_piece(knight)
                elif char == 'r':
                    rook = Rook(color)
                    squares[row][col].change_piece(rook)
                elif char == 'q':
                    queen = Queen(color)
                    squares[row][col].change_piece(queen)
                elif char == 'k':
                    king = King(color)
                    squares[row][col].change_piece(king)
                col += 1

    # ============================= Moving methods ===============================

    def make_move(self, move, update_moved=False):
        """
        move piece from start to target square
        """

        piece = move.start.piece
        move.start.change_piece(None)
        move.target.change_piece(piece)
        piece.moved = piece.moved or update_moved

        if move.is_castling():
            # also move rook
            castle = move.rook_move
            rook = castle.start.piece
            castle.start.change_piece(None)
            castle.target.change_piece(rook)
            rook.moved = True

        self.promote(move.target)

    def undo_move(self, move):
        move.start.piece = move.s_piece
        move.target.piece = move.t_piece

        if move.is_castling():
            # move rook back
            move.rook_move.start.piece = move.rook_move.target.piece
            move.rook_move.start.piece.moved = False
            move.rook_move.target.piece = None

    def promote(self, piece_square):
        if piece_square.piece.color == 'white':
            if isinstance(piece_square.piece, Pawn) and piece_square.row == 0:
                piece_square.piece = Queen('white')
        else:
            if isinstance(piece_square.piece, Pawn) and piece_square.row == 7:
                piece_square.piece = Queen('black')

    # ========================= Calculating possible moves ========================

    def can_castle(self, color):
        """
        :returns list of 2 bools, [can_castle_left_side, can_castle_right_side]
        """
        can_castle_left_side, can_castle_right_side = False, False

        king_square = self.get_king_square(color)
        row = king_square.row
        col = king_square.col

        if king_square.piece.moved or self.in_check(color):
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

    def can_move(self, move):
        """
        try a move to see if there is check
        """
        ret = True
        color = move.start.piece.color

        self.make_move(move)  # making the move
        if self.in_check(color):
            ret = False
        self.undo_move(move)  # un-making the move

        return ret

    def calc_moves(self, piece_square):
        """
        calculate all possible moves for a piece in a specific location (row, col)
        :return a list of locations (row, col) representing possible new location
        """
        piece = piece_square.piece
        if isinstance(piece, Pawn):
            moves = self.pawn_moves(piece_square)

        elif isinstance(piece, Knight):
            moves = self.knight_moves(piece_square)

        elif isinstance(piece, King):
            moves = self.king_moves(piece_square)

        # bishop, rook or queen
        elif isinstance(piece, Queen) or isinstance(piece, Rook) or isinstance(piece, Bishop):
            moves = self.line_moves(piece_square)

        ret = []
        for move in moves:
            if self.can_move(move):
                ret.append(move)

        return ret

    def knight_moves(self, piece_square):
        knight = piece_square.piece
        row, col = piece_square.row, piece_square.col
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

    def pawn_moves(self, piece_square):
        pawn = piece_square.piece
        row, col = piece_square.row, piece_square.col
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
        if (pawn.color == 'black' and row == 1) or (pawn.color == 'white' and row == 6):
            move_row, move_col = row + 2 * updown, col
            if Square.in_range(move_row, move_col):
                if not self.squares[move_row][move_col].has_piece() and \
                        not self.squares[move_row - updown][move_col].has_piece():
                    target = self.squares[move_row][move_col]
                    ret.append(Move(start, target))
        return ret

    def line_moves(self, piece_square):
        piece = piece_square.piece
        row, col = piece_square.row, piece_square.col
        ret = []
        start = self.squares[row][col]
        directions = piece.DIRECTIONS

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

    def king_moves(self, piece_square):
        piece = piece_square.piece
        row, col = piece_square.row, piece_square.col
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
                castle.rook_move = Move(self.squares[row][0], self.squares[row][3])
                ret.append(castle)
            if can_castle[1]:  # right (short) castle
                target = self.squares[row][col + 2]
                castle = Move(start, target)
                castle.r_castle = True
                castle.rook_move = Move(self.squares[row][7], self.squares[row][5])
                ret.append(castle)
        return ret

    def all_moves(self, color):
        """
        calculate all possible moves of player color
        """
        ret = []
        for square in self.get_team_pieces(color):
            ret += self.calc_moves(square)
        return ret

    # ============================= Calculating sees ===============================

    def calc_sees(self, piece_square):
        """
        calculate what squares a piece sees
        """
        ret = []
        piece = piece_square.piece
        row, col = piece_square.row, piece_square.col

        if piece.name == "pawn":
            updown = piece.direction  # 1 for black, -1 for white
            take_moves = [(row + updown, col - 1), (row + updown, col + 1)]
            for move_row, move_col in take_moves:
                if Square.in_range(move_row, move_col):
                    ret.append(self.squares[move_row][move_col])
            return ret

        elif piece.name == "knight":
            for move in self.knight_moves(piece_square):
                ret.append(move.target)
            return ret

        elif piece.name == "king":
            return self.king_sees(row, col)

        # bishop, rook or queen
        else:
            for move in self.line_moves(piece_square):
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
            ret += self.calc_sees(square)

        return ret

    # =========================== Game, gets & others ===============================

    def game_over(self, rival_color):
        all_moves = []
        rival_pieces = self.get_team_pieces(rival_color)
        for square in rival_pieces:
            all_moves += self.calc_moves(square)
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
                    if self.squares[row][col].piece is None:  ###
                        print('why')
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

    # def clone(self):
    #     cloned = Board()
    #     cloned._create()
    #     all_pieces = self.get_team_pieces('white') + self.get_team_pieces('black')
    #     for square in all_pieces:
    #         row, col = square.row, square.col
    #         cloned.squares[row][col].piece = copy.deepcopy(square.piece)
    #     return cloned

