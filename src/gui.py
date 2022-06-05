import pygame
import os
from constants import *
from ai import AI


class GUI:

    def __init__(self, board, moves):
        self.board = board
        self.squares = self.board.squares
        self.moves = moves

    def draw_background(self, surface):

        # drawing squares
        for squares_row in self.squares:
            for square in squares_row:
                row, col = square.row, square.col
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, square.color, rect)

        # highlight last move
        if self.moves:
            move = self.moves[-1]
            squares = ((move.start, L_YELLOW), (move.target, YELLOW))
            for square, color in squares:
                row, col = square.row, square.col
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

        # drawing frame around clicked square
        if self.board.clicked_square:
            square = self.board.clicked_square
            row, col = square.row, square.col
            rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, SELECTED_COLOR, rect, 5)

        # drawing circle if this square is a move option
        for square in self.board.target_squares():
            row, col = square.row, square.col
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                      row * SQUARE_SIZE + SQUARE_SIZE // 2)
            if square.has_piece():
                pygame.draw.circle(surface, POSSIBLE_COLOR, center, 24, 6)
            else:
                pygame.draw.circle(surface, POSSIBLE_COLOR, center, 15)

        # highlight king in check
        for color in ['white', 'black']:
            if self.board.in_check(color):
                king_square = self.board.get_king_square(color)
                row, col = king_square.row, king_square.col
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, CHECK_COLOR, rect, 5)

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    image = pygame.image.load(piece.image_path)
                    center_img = col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2
                    piece.img_frame = image.get_rect(center=center_img)
                    surface.blit(image, piece.img_frame)

    @staticmethod
    def draw_game_over(surface):
        # game over
        path = os.path.join(f'images/gui/checkmate_s.png')
        image = pygame.image.load(path)
        center_img = WIDTH // 2, int(0.46 * HEIGHT)
        img_frame = image.get_rect(center=center_img)
        surface.blit(image, img_frame)

        # restart
        path = os.path.join(f'images/gui/restart.png')
        image = pygame.image.load(path)
        center_img = WIDTH // 2, HEIGHT - HEIGHT // 4
        img_frame = image.get_rect(center=center_img)
        surface.blit(image, img_frame)

    def draw_evaluation(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 32)
        evalu = font.render(f'{AI.evaluate(self.board)}', True, (0, 0, 0))
        menu_rect = evalu.get_rect(center=(HEIGHT // 2, WIDTH // 2))
        screen.blit(evalu, menu_rect)