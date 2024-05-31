import pygame
from utils import *

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = 0
        self.y = 0

    def rotate(self, board_width, board_height, board):
        rotated_shape = [list(row) for row in zip(*self.shape[::-1])]
        if not self.check_collision(board_width, board_height, board, shape=rotated_shape):
            self.shape = rotated_shape
        else:
            for i in range(1, len(rotated_shape[0])):
                if not self.check_collision(board_width, board_height, board, shape=rotated_shape, dx=i):
                    self.x += i
                    self.shape = rotated_shape
                    return
                elif not self.check_collision(board_width, board_height, board, shape=rotated_shape, dx=-i):
                    self.x -= i
                    self.shape = rotated_shape
                    return

    def check_collision(self, board_width, board_height, board, dx=0, dy=0, shape=None):
        if shape is None:
            shape = self.shape
        for y, row in enumerate(shape):
            for x, col in enumerate(row):
                if col:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= board_width or new_y >= board_height or (new_y >= 0 and board[new_y][new_x]):
                        return True
        return False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen, block_size):
        for y, row in enumerate(self.shape):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(screen, self.color, (self.x * block_size + x * block_size, self.y * block_size + y * block_size, block_size, block_size))
                    pygame.draw.rect(screen, GRAY, (self.x * block_size + x * block_size, self.y * block_size + y * block_size, block_size, block_size), 1)