import pygame
import sys
import copy

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
        self.colors = ["black", "white"]

    def opening_screen(self):
        screen = self.screen
        while True:
            # screen.fill("black")
            self.gui.draw_background(screen)
            self.gui.draw_pieces(screen)

            menu_mouse_pos = pygame.mouse.get_pos()

            font = pygame.font.Font('freesansbold.ttf', 32)
            menu_text = font.render("Welcome!", True, (0, 0, 0))
            menu_rect = menu_text.get_rect(center=(HEIGHT // 2, WIDTH // 8))

            rankrausz = pygame.image.load("assets/rankrausz.png")

            play_ai = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(HEIGHT // 2, 3 * WIDTH // 8),
                                 text_input="Play vs. AI", font=font, base_color="#d7fcd4",
                                 hovering_color=CHECK_COLOR)

            play_friend = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(HEIGHT // 2, 5 * WIDTH // 8),
                                 text_input="Play vs. friend", font=font, base_color="#d7fcd4",
                                 hovering_color=CHECK_COLOR)

            screen.blit(menu_text, menu_rect)
            # screen.blit(rankrausz, [200, 200])
            for button in [play_ai, play_friend]:
                button.change_color(menu_mouse_pos)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_ai.check_for_input(menu_mouse_pos):
                        self.mainloop(True, 1)
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
                    GUI.draw_game_over(screen)
                    self.game_over = True

            elif board.game_over(current_color):
                # no possible moves but not in check = stalemate
                if not self.game_over:
                    print("stalemate")
                self.game_over = True

            if current_color == 'black' and ai:
                print("AI is thinking...")
                best_score = AI.INFINITI
                best_move = 0
                for move in board.all_moves('black'):
                    sr, sc, tr, tc = move.start.row, move.start.col, move.target.row, move.target.col
                    copied = board.clone()
                    cmove = Move(copied.squares[sr][sc], copied.squares[tr][tc])
                    copied.make_move(cmove)

                    score = AI.minimax(copied, depth, -AI.INFINITI, AI.INFINITI, True)
                    if score < best_score:
                        best_score = score
                        best_move = move

                board.make_move(best_move)
                print(f'Beat that!\nPosition evaluated: {AI.COUNT}\n')
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
                            board.make_move(move)

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

                    # press 'r' to restart
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            restart = Main()
                            restart.mainloop(ai, 1)

                    # quit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            # update gui



            gui.draw_background(screen)
            gui.draw_pieces(screen)

            font = pygame.font.Font('freesansbold.ttf', 32)
            evalu = font.render(f'{AI.evaluate(board)}', True, (0, 0, 0))
            menu_rect = evalu.get_rect(center=(HEIGHT // 2, WIDTH // 2))
            screen.blit(evalu, menu_rect)

            pygame.display.update()

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
    main.opening_screen()
