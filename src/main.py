import pygame
import sys

from constants import *
from gui import GUI
from board import Board
from move import Move


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        self.board = Board()
        self.gui = GUI(self.board)  # reference
        self.white_to_move = True
        self.colors = ["black", "white"]
        self.game_over = False

    def mainloop(self):

        board = self.board
        gui = self.gui
        screen = self.screen

        print("white's turn")

        while True:
            gui.draw_background(screen)
            gui.draw_pieces(screen)

            current_color = self.colors[self.white_to_move]

            if board.in_check(current_color):
                if board.game_over(current_color):
                    if not self.game_over:
                        print(f'{self.colors[not self.white_to_move]} wins!')
                    self.game_over = True
                gui.highlight_king(screen, current_color)

            elif board.game_over(current_color):
                if not self.game_over:
                    print("stalemate")
                self.game_over = True

            # board.
            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:

                    # get the row and col of click location
                    click_x, click_y = event.pos
                    clicked_row = click_y // SQUARE_SIZE
                    clicked_col = click_x // SQUARE_SIZE

                    # make move
                    if board.squares[clicked_row][clicked_col] in board.target_squares():
                        target_square = board.squares[clicked_row][clicked_col]
                        # get move
                        move = board.get_move_from_target(target_square)
                        board.make_move(move)
                        board.possible_moves = []
                        board.clicked_square = None

                        self.white_to_move = not self.white_to_move

                        # print(f"{self.colors[self.white_to_move]}'s turn")

                    # clicked on a piece
                    elif board.squares[clicked_row][clicked_col].has_team_piece(current_color):
                        square = board.squares[clicked_row][clicked_col]
                        piece = square.piece
                        # board.possible_squares = []
                        board.possible_moves = []
                        if square == board.clicked_square:
                            # unclick
                            board.clicked_square = None
                        else:
                            board.clicked_square = square
                            board.possible_moves = board.calc_moves(piece, clicked_row, clicked_col)
                            # for move in possible_moves:
                            #     possible_square = move.target
                            #     board.possible_squares.append(possible_square)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart = Main()
                        restart.mainloop()

                # quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # return

            pygame.display.update()  ###

    def my_turn(self, piece):
        if piece.color == "white" and self.white_to_move:
            return True
        if piece.color == "black" and not self.white_to_move:
            return True
        return False

    def get_curr_color(self):
        if self.white_to_move:
            return "white"
        return "black"

    def get_other_color(self):
        if not self.white_to_move:
            return "white"
        return "black"


if __name__ == "__main__":
    main = Main()
    main.mainloop()

