import pygame
import random
import os
import json
from piece import Piece
from button import Button
from utils import *

class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.load_settings()
        self.load_scores()
        self.reset_game()
        self.paused = False
        self.bg_image = None
        self.load_background()

        self.start_buttons = [
            Button("Iniciar Juego", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)),
            Button("Configuraciones", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            Button("Salir del Juego", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        ]

        self.config_buttons = [
            Button("Cambiar Fondo", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)),
            Button("Cambiar Teclas", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            Button("Volver", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        ]

    def load_settings(self):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = {
                "resolution": (SCREEN_WIDTH, SCREEN_HEIGHT),
                "fullscreen": False,
                "background": None,
                "key_bindings": {
                    "left": pygame.K_LEFT,
                    "right": pygame.K_RIGHT,
                    "down": pygame.K_DOWN,
                    "rotate": pygame.K_UP,
                    "hold": pygame.K_SPACE,
                    "pause": pygame.K_ESCAPE
                }
            }

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file)

    def load_background(self):
        background_path = self.settings.get("background")
        if background_path and os.path.exists(background_path):
            self.bg_image = pygame.image.load(background_path)

    def save_scores(self):
        with open(SCORES_FILE, "w") as file:
            json.dump(self.top_scores, file)

    def load_scores(self):
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as file:
                self.top_scores = json.load(file)
        else:
            self.top_scores = []

    def reset_game(self):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.create_piece()
        self.next_pieces = [self.create_piece() for _ in range(3)]
        self.hold_piece = None
        self.score = 0
        self.game_over = False

    def create_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice([WHITE, BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)])
        piece = Piece(shape, color)
        piece.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        piece.y = 0
        return piece

    def draw_board(self):
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col:
                    pygame.draw.rect(self.screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_next_pieces(self):
        for i, piece in enumerate(self.next_pieces):
            for y, row in enumerate(piece.shape):
                for x, col in enumerate(row):
                    if col:
                        pygame.draw.rect(self.screen, piece.color, (SCREEN_WIDTH - 80 + x * BLOCK_SIZE, 50 + i * 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 80 + x * BLOCK_SIZE, 50 + i * 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_hold_piece(self):
        if self.hold_piece:
            for y, row in enumerate(self.hold_piece.shape):
                for x, col in enumerate(row):
                    if col:
                        pygame.draw.rect(self.screen, self.hold_piece.color, (SCREEN_WIDTH - 80 + x * BLOCK_SIZE, 300 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 80 + x * BLOCK_SIZE, 300 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 100, 400))

    def show_start_screen(self):
        self.reset_game()  # Resetear el juego al mostrar la pantalla de inicio
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_scores()
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.start_buttons[0].is_clicked(mouse_pos):
                        running = False
                    elif self.start_buttons[1].is_clicked(mouse_pos):
                        self.show_config_screen()
                    elif self.start_buttons[2].is_clicked(mouse_pos):
                        self.save_scores()
                        pygame.quit()
                        quit()

            self.screen.fill(GRAY)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Tetris", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

            for button in self.start_buttons:
                button.draw(self.screen)

            pygame.display.flip()

    def show_config_screen(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_scores()
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.config_buttons[0].is_clicked(mouse_pos):
                        self.change_background()
                    elif self.config_buttons[1].is_clicked(mouse_pos):
                        self.change_keys()
                    elif self.config_buttons[2].is_clicked(mouse_pos):
                        running = False

            self.screen.fill(BLACK)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Configuraciones", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

            for button in self.config_buttons:
                button.draw(self.screen)

            pygame.display.flip()

    def change_background(self):
        # Implementar lógica para cambiar el fondo del juego
        pass

    def change_keys(self):
        # Implementar lógica para cambiar las teclas
        pass

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_scores()
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == self.settings["key_bindings"]["pause"]:
                    self.paused = not self.paused
                    if self.paused:
                        self.show_pause_screen()
                elif event.key == self.settings["key_bindings"]["left"]:
                    if not self.current_piece.check_collision(BOARD_WIDTH, BOARD_HEIGHT, self.board, dx=-1):
                        self.current_piece.move(-1, 0)
                elif event.key == self.settings["key_bindings"]["right"]:
                    if not self.current_piece.check_collision(BOARD_WIDTH, BOARD_HEIGHT, self.board, dx=1):
                        self.current_piece.move(1, 0)
                elif event.key == self.settings["key_bindings"]["down"]:
                    if not self.current_piece.check_collision(BOARD_WIDTH, BOARD_HEIGHT, self.board, dy=1):
                        self.current_piece.move(0, 1)
                elif event.key == self.settings["key_bindings"]["rotate"]:
                    self.current_piece.rotate(BOARD_WIDTH, BOARD_HEIGHT, self.board)
                elif event.key == self.settings["key_bindings"]["hold"]:
                    self.handle_hold()

    def update_board(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, col in enumerate(row):
                if col and self.current_piece.y + y >= 0:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = 1

    def clear_lines(self):
        full_rows = [i for i, row in enumerate(self.board) if all(row)]
        for row in full_rows:
            del self.board[row]
            self.board.insert(0, [0] * BOARD_WIDTH)
        self.score += len(full_rows) * 100

    def handle_hold(self):
        if not self.hold_piece:
            self.hold_piece = self.current_piece
            self.current_piece = self.next_pieces.pop(0)
            self.next_pieces.append(self.create_piece())
        else:
            self.hold_piece, self.current_piece = self.current_piece, self.hold_piece

        self.hold_piece.x = BOARD_WIDTH // 2 - len(self.hold_piece.shape[0]) // 2
        self.hold_piece.y = 0

    def run(self):
        self.show_start_screen()
        while not self.game_over:
            self.handle_events()

            if not self.paused:
                if not self.current_piece.check_collision(BOARD_WIDTH, BOARD_HEIGHT, self.board, dy=1):
                    self.current_piece.move(0, 1)
                else:
                    self.update_board()
                    self.clear_lines()
                    self.current_piece = self.next_pieces.pop(0)
                    self.next_pieces.append(self.create_piece())
                    if self.current_piece.check_collision(BOARD_WIDTH, BOARD_HEIGHT, self.board):
                        self.game_over = True

            self.screen.fill(BLACK)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))

            self.draw_board()
            self.current_piece.draw(self.screen, BLOCK_SIZE)
            self.draw_next_pieces()
            self.draw_hold_piece()
            self.draw_score()

            pygame.display.flip()
            self.clock.tick(5) #altera la velocidad de caida de las piezas 1 es lento, 10 es rapido.

        self.show_game_over_screen()

    def show_pause_screen(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_scores()
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == self.settings["key_bindings"]["pause"]:
                    self.paused = False
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if self.start_buttons[0].is_clicked(mouse_pos):
                        self.paused = False
                        running = False
                    elif self.start_buttons[1].is_clicked(mouse_pos):
                        self.show_config_screen()
                    elif self.start_buttons[2].is_clicked(mouse_pos):
                        self.save_scores()
                        pygame.quit()
                        quit()

            self.screen.fill(BLACK)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Tetris Pausado", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

            for button in self.start_buttons:
                button.draw(self.screen)

            pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        font = pygame.font.Font(None, 36)
        game_over_text = font.render(f"Game Over. Score: {self.score}", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2))

        self.save_scores()

        pygame.display.flip()
        pygame.time.wait(5000)

        self.show_start_screen()