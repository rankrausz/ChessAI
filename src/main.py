import pygame
import sys

from constants import *
from gui import GUI
from board import Board


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        self.board = Board()
        self.gui = GUI(self.board)  # reference
        self.white_to_move = True

    def mainloop(self):

        board = self.board
        gui = self.gui
        screen = self.screen

        while True:
            gui.draw_background(screen)
            gui.draw_pieces(screen)

            if board.game_over(self.get_color()):
                print("game over")

            current_color = self.get_color()
            if board.in_check(current_color):
                gui.highlight_king(screen, current_color)

            # board.
            for event in pygame.event.get():

                # click
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # get the row and col of click location
                    click_x, click_y = event.pos
                    clicked_row = click_y // SQUARE_SIZE
                    clicked_col = click_x // SQUARE_SIZE

                    # make move
                    if board.squares[clicked_row][clicked_col] in board.possible_squares:
                        piece_moving = board.clicked_square.piece
                        target_square = board.squares[clicked_row][clicked_col]
                        board.make_move(board.clicked_square, target_square)
                        self.white_to_move = not self.white_to_move
                        board.possible_squares = []
                        board.clicked_square = None

                    # clicked on a piece
                    elif board.squares[clicked_row][clicked_col].has_piece():
                        square = board.squares[clicked_row][clicked_col]
                        piece = square.piece
                        board.possible_squares = []
                        if square == board.clicked_square:
                            # unclick
                            board.clicked_square = None
                        elif self.my_turn(piece):
                            board.clicked_square = square
                            possible_moves = board.calc_moves(piece, clicked_row, clicked_col)
                            for row, col in possible_moves:
                                possible_square = board.squares[row][col]
                                board.possible_squares.append(possible_square)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart = Main()
                        restart.mainloop()

                # quit
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()  # return

            pygame.display.update()

    def my_turn(self, piece):
        if piece.color == "white" and self.white_to_move:
            return True
        if piece.color == "black" and not self.white_to_move:
            return True
        return False

    def get_color(self):
        if self.white_to_move:
            return "white"
        return "black"


if __name__ == "__main__":
    main = Main()
    main.mainloop()

