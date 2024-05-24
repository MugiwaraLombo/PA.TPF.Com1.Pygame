import pygame
import random
import os
import json
from piece import Piece
from button import Button
from utils import *
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.create_piece()
        self.next_pieces = [self.create_piece() for _ in range(3)]
        self.hold_piece = None
        self.score = 0
        self.game_over = False
        self.paused = False

    def create_piece(self):
        shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]],  # Z
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[1, 1], [1, 1]]  # O
        ]
        shape = random.choice(shapes)
        color = random.choice([WHITE, BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)])
        return Piece(shape, color)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.move_piece(1, 0)
                elif event.key == pygame.K_SPACE:
                    self.hold_current_piece()
                elif event.key == pygame.K_UP:
                    self.current_piece.rotate()
                elif event.key == pygame.K_DOWN:
                    while self.move_piece(0, 1):
                        pass
                    self.update_board()
                    self.current_piece = self.next_pieces.pop(0)
                    self.next_pieces.append(self.create_piece())
                elif event.key == pygame.K_p:
                    self.paused = not self.paused

    def move_piece(self, dx, dy):
        self.current_piece.move(dx, dy)
        if self.check_collision(self.current_piece):
            self.current_piece.move(-dx, -dy)
            return False
        return True

    def check_collision(self, piece):
        for y, row in enumerate(piece.shape):
            for x, col in enumerate(row):
                if col:
                    if (piece.x + x < 0 or piece.x + x >= BOARD_WIDTH or
                        piece.y + y >= BOARD_HEIGHT or self.board[piece.y + y][piece.x + x]):
                        return True
        return False

    def draw_board(self):
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_next_pieces(self):
        font = pygame.font.Font(None, 18)
        text_surface = font.render("Próximas piezas", True, WHITE)
        self.screen.blit(text_surface, (SCREEN_WIDTH - 150, 10))
        for i, piece in enumerate(self.next_pieces):
            for y, row in enumerate(piece.shape):
                for x, col in enumerate(row):
                    if col:
                        pygame.draw.rect(self.screen, piece.color,
                                         (SCREEN_WIDTH - 150 + x * BLOCK_SIZE, 50 + i * 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(self.screen, GRAY,
                                         (SCREEN_WIDTH - 150 + x * BLOCK_SIZE, 50 + i * 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_hold_piece(self):
        if self.hold_piece:
            font = pygame.font.Font(None, 36)
            text_surface = font.render("Hold", True, WHITE)
            self.screen.blit(text_surface, (10, 10))
            for y, row in enumerate(self.hold_piece.shape):
                for x, col in enumerate(row):
                    if col:
                        pygame.draw.rect(self.screen, self.hold_piece.color,
                                         (10 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(self.screen, GRAY,
                                         (10 + x * BLOCK_SIZE, 50 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text_surface, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50))

    def show_start_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        title_surface = font.render("TETRIS", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(title_surface, title_rect)

        font = pygame.font.Font(None, 36)
        instructions_surface = font.render("Press any key to start", True, WHITE)
        instructions_rect = instructions_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instructions_surface, instructions_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False

    def draw_pause_screen(self):
        font = pygame.font.Font(None, 74)
        pause_surface = font.render("PAUSED", True, WHITE)
        pause_rect = pause_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(pause_surface, pause_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    waiting = False
                    self.paused = False

    def draw_game_over_screen(self):
        self.screen.fill(BLACK)
        font = pygame.font.Font(None, 74)
        game_over_surface = font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_surface, game_over_rect)

        font = pygame.font.Font(None, 36)
        score_surface = font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(score_surface, score_rect)

        instructions_surface = font.render("Press any key to restart", True, WHITE)
        instructions_rect = instructions_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(instructions_surface, instructions_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    self.__init__()
                    waiting = False

    def hold_current_piece(self):
        if not self.hold_piece:
            self.hold_piece = self.current_piece
            self.current_piece = self.next_pieces.pop(0)
            self.next_pieces.append(self.create_piece())
        else:
            self.hold_piece, self.current_piece = self.current_piece, self.hold_piece
            self.hold_piece.x = BOARD_WIDTH // 2 - len(self.hold_piece.shape[0]) // 2
            self.hold_piece.y = 0

    def update_board(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, col in enumerate(row):
                if col:
                    if 0 <= self.current_piece.y + y < BOARD_HEIGHT and 0 <= self.current_piece.x + x < BOARD_WIDTH:
                        self.board[self.current_piece.y + y][self.current_piece.x + x] = 1

        lines_cleared = 0
        for y in range(BOARD_HEIGHT):
            if all(self.board[y]):
                del self.board[y]
                self.board.insert(0, [0] * BOARD_WIDTH)
                lines_cleared += 1

        self.score += lines_cleared * 100

    def run(self):
        running = True
        while running:
            self.handle_events()

            if self.game_over:
                self.draw_game_over_screen()
            elif self.paused:
                self.draw_pause_screen()
            else:
                if not self.move_piece(0, 1):
                    self.update_board()
                    self.current_piece = self.next_pieces.pop(0)
                    self.next_pieces.append(self.create_piece())
                    if self.check_collision(self.current_piece):
                        self.game_over = True

            self.screen.fill(BLACK)
            if not self.game_over:
                self.draw_board()
                self.current_piece.draw(self.screen)
                self.draw_next_pieces()
                self.draw_hold_piece()
                self.draw_score()
            pygame.display.flip()
            self.clock.tick(5)
