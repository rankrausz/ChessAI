import pygame
from constants import *
from board import Board

class GUI:

    def __init__(self, board):
        self.board = board
        self.squares = self.board.squares

    def draw_background(self, surface):
        # for row in range(ROWS):
        #     for col in range(COLS):
        #         color = COLORS[(row+col) % 2]
        #         rect = (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) ##
        #         pygame.draw.rect(surface, color, rect)
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
        for square in self.board.possible_squares:
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

