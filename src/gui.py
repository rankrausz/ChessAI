import pygame
import os
from constants import *
from board import Board


class GUI:

    def __init__(self, board):
        self.board = board
        self.squares = self.board.squares
        self.white_check = False
        self.black_check = False

    def draw_background(self, surface):

        for squares_row in self.squares:
            for square in squares_row:
                row, col = square.row, square.col
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, square.color, rect)

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

    def draw_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):

                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    image = pygame.image.load(piece.image_path)
                    center_img = col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2  # understand
                    piece.img_frame = image.get_rect(center=center_img)
                    surface.blit(image, piece.img_frame)  # understand

    def highlight_king(self, surface, color):
        king_square = self.board.get_king_square(color)
        row, col = king_square.row, king_square.col
        rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(surface, CHECK_COLOR, rect, 5)

    def draw_game_over(self, surface):
        path = os.path.join(f'images/checkmate_s.png')
        image = pygame.image.load(path)
        center_img = WIDTH // 2, int(0.46 * HEIGHT)
        img_frame = image.get_rect(center=center_img)
        surface.blit(image, img_frame)

        # font = pygame.font.Font('freesansbold.ttf', 26)
        # text = font.render("Press 'r' to restart", True, (0, 0, 0))
        # center_text = WIDTH // 2, HEIGHT - HEIGHT // 4
        # frame = text.get_rect(center=center_text)
        # surface.blit(text, frame)

        path = os.path.join(f'images/restart.png')
        image = pygame.image.load(path)
        center_img = WIDTH // 2, HEIGHT - HEIGHT // 4
        img_frame = image.get_rect(center=center_img)
        surface.blit(image, img_frame)
