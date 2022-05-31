import pygame
import sys
import copy
import random

from constants import *
from gui import GUI
from board import Board
from ai import AI
from move import Move


from button import Button


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")

        self.board = Board()
        self.gui = GUI(self.board)
        self.white_to_move = True
        self.game_over = False
        self.moves = []
        self.colors = ["black", "white"]

    def opening_screen(self):
        screen = self.screen
        while True:
            bg = pygame.image.load("images/gui/bg.png")
            bg_rect = bg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(bg, bg_rect)

            menu_mouse_pos = pygame.mouse.get_pos()

            header = pygame.image.load("images/gui/header.png")
            header_rect = header.get_rect(center=(WIDTH // 2, int(0.2*HEIGHT)))
            screen.blit(header, header_rect)

            play_ai = Button(image=pygame.image.load("images/gui/play_ai.png"),
                             hovered_img=pygame.image.load("images/gui/play_ai_p.png"),
                             pos=(HEIGHT // 2, int(0.45*WIDTH)))

            play_friend = Button(image=pygame.image.load("images/gui/play_f.png"),
                                 hovered_img=pygame.image.load("images/gui//play_f_p.png"),
                                 pos=(HEIGHT // 2, int(0.65*WIDTH)))

            for button in [play_ai, play_friend]:
                button.change_bg(menu_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_ai.check_for_input(menu_mouse_pos):
                        self.mainloop(True, DEPTH - 1)
                    if play_friend.check_for_input(menu_mouse_pos):
                        self.mainloop(False, -1)

            pygame.display.update()

    def mainloop(self, ai, depth):

        board = self.board
        gui = self.gui
        screen = self.screen

        while True:
            current_color = self.colors[self.white_to_move]

            # current color king in check
            if board.in_check(current_color):
                if board.game_over(current_color):
                    if not self.game_over:
                        print(f'{self.colors[not self.white_to_move]} wins!')
                        # TODO: play again?
                    self.game_over = True

            elif board.game_over(current_color):
                # no possible moves but not in check = stalemate
                if not self.game_over:
                    print("stalemate")
                self.game_over = True

            # make AI move
            if current_color == 'black' and ai and not self.game_over:
                print("AI is thinking...")
                best_score = AI.INFINITI
                best_move = 0
                for move in board.all_moves('black'):

                    board.make_move(move)
                    score = AI.minimax(board, depth, -AI.INFINITI, AI.INFINITI, True)
                    # score = AI.negamax(board, depth, -AI.INFINITI, AI.INFINITI, True)
                    board.undo_move(move, True)
                    if score < best_score:
                        best_score = score
                        best_move = move

                board.make_move(best_move)
                self.moves.append(best_move)
                ai_line = random.choice(AI_LINES)
                print(f'Positions evaluated: {AI.COUNT}\n{ai_line}\n')
                AI.COUNT = 0
                self.white_to_move = not self.white_to_move

            else:
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
                            board.make_move(move, True)
                            self.moves.append(move)

                            # restart clicked square and possible moves
                            board.clicked_square = None
                            board.possible_moves = []

                            self.white_to_move = not self.white_to_move  # change turn

                        # clicked on a piece
                        elif board.squares[clicked_row][clicked_col].has_team_piece(current_color):
                            square = board.squares[clicked_row][clicked_col]
                            piece = square.piece
                            board.possible_moves = []
                            if square == board.clicked_square:  # un-click clicked square
                                board.clicked_square = None
                            else:  # click new square
                                board.clicked_square = square
                                # calculate possible moves
                                board.possible_moves = board.calc_moves(piece, clicked_row, clicked_col)

                    elif event.type == pygame.KEYDOWN:
                        # press 'r' to restart
                        if event.key == pygame.K_r:
                            restart = Main()
                            restart.opening_screen()

                        # press 'u' to undo move
                        elif event.key == pygame.K_u:
                            if ai and self.moves:
                                board.undo_move(self.moves.pop())
                                board.undo_move(self.moves.pop())
                            elif self.moves:
                                board.undo_move(self.moves.pop())
                                self.white_to_move = not self.white_to_move

                    # quit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            # update gui
            gui.draw_background(screen)
            gui.draw_pieces(screen)
            if self.game_over:
                GUI.draw_game_over(screen)
            # font = pygame.font.Font('freesansbold.ttf', 32)
            # evalu = font.render(f'{AI.evaluate(board)}', True, (0, 0, 0))
            # menu_rect = evalu.get_rect(center=(HEIGHT // 2, WIDTH // 2))
            # screen.blit(evalu, menu_rect)

            pygame.display.update()


if __name__ == "__main__":
    main = Main()
    main.opening_screen()
