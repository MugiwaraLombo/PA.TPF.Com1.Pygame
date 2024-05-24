import pygame
from utils import *

class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, screen):
        for y, row in enumerate(self.shape):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(screen, self.color, (self.x * BLOCK_SIZE + x * BLOCK_SIZE, self.y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, GRAY, (self.x * BLOCK_SIZE + x * BLOCK_SIZE, self.y * BLOCK_SIZE + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)
