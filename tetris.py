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
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Crea la pantalla del juego
        pygame.display.set_caption("Proyecto: TETRIS") #Leyenda del del juego
        self.clock = pygame.time.Clock() #Velocidad de movimiento de las piezas
        self.load_settings()
        self.paused = False
        self.bg_image = None
        self.load_background()
        self.play_music()

        self.start_buttons = [ #Botones del inicio
            Button("Iniciar Juego", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)),
            Button("Configuraciones", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            Button("Salir del Juego", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        ]

        self.config_buttons = [ #Botones de las configuraciones
            Button("Cambiar Fondo", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)),
            Button("Cambiar Teclas", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            Button("Volver", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        ]

        self.background_buttons = [ #Botones de los ajustes de background
            Button("Fondo de pantalla 1", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)),
            Button("Fondo de pantalla 2", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            Button("Fondo de pantalla 3", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)),
            Button("Volver", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
        ]

        self.key_buttons = [ #Botones de los ajustes de las teclas
            Button("LEFT", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50)),
            Button("RIGHT", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - 50)),
            Button("DOWN", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)),
            Button("ROTATE", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)),
            Button("HOLD", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)),
            Button("PAUSE", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50)),
            Button("Volver", pygame.font.Font(None, 24), WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 125))
        ]

    def load_settings(self):
        if not os.path.exists(CONFIG_DIR): #Consulta si existe el directorio definido en la variable "CONFIG_DIR"
            os.makedirs(CONFIG_DIR) #Crea un directorio de forma recursiva.
        if os.path.exists(SETTINGS_FILE): #Consulta si existe el archivo definido en la variable "SETTINGS_FILE"
            with open(SETTINGS_FILE, "r") as file: #Abre el archivo y lo identifica como "file"
                self.settings = json.load(file) #Carga al atributo "settings" los datos del archivo identificado como "file"
        else:
            self.settings = {#Si no existe, se crean las configuraciones por defecto
                "resolution": (SCREEN_WIDTH, SCREEN_HEIGHT),
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

    def save_settings(self): #Guarda las configuraciones
        with open(SETTINGS_FILE, "w") as file:
            json.dump(self.settings, file)

    def load_background(self): #Carga la imagen de fondo
        background_path = self.settings.get("background")
        if background_path and os.path.exists(background_path):
            self.bg_image = pygame.image.load(background_path)

    def play_music(self):
        pygame.mixer.music.load(os.path.join("config", "Background.mp3"))  #Carga el archivo de música
        pygame.mixer.music.play(-1) #Reproduce el archivo en bucle

    def reset_game(self): #Reinicia la pantalla de juego
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.create_piece()
        self.next_pieces = [self.create_piece() for _ in range(3)]
        self.hold_piece = None
        self.score = 0
        self.game_over = False

    def create_piece(self):
        shape = random.choice(SHAPES) #Elige una pieza al azar
        color = random.choice([WHITE, BLACK, (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255)]) #Elige un color al azar
        piece = Piece(shape, color) #Crea una pieza
        #A continuacion pociciona la pieza en el centro alto del tablero
        piece.x = BOARD_WIDTH // 2 - len(shape[0]) // 2
        piece.y = 0 
        return piece #Devuelve la pieza creada

    def draw_board(self):
        pygame.draw.rect(self.screen, GRAY, (BOARD_WIDTH * BLOCK_SIZE, 0, SCREEN_WIDTH, SCREEN_HEIGHT)) #Dibuja en el tablero al borde derecho un rectangulo en la pantalla no jugable sobre el que se mostraran estadisticas
        for y, row in enumerate(self.board):
            for x, col in enumerate(row):
                if col:
                    #Se dibuja la parte del tablero jugable
                    pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(self.screen, GRAY, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_next_pieces(self): #Dibuja las 3 siguientes piezas del juego
        font = pygame.font.Font(None, 24)
        next_pieces_text = font.render("Next Pieces:", True, WHITE)
        self.screen.blit(next_pieces_text, (SCREEN_WIDTH - 100, 40))
        for i, piece in enumerate(self.next_pieces):
            for y, row in enumerate(piece.shape):
                for x, col in enumerate(row):
                    if col:
                        pygame.draw.rect(self.screen, piece.color, (SCREEN_WIDTH - 100 + x * BLOCK_SIZE, 70 + i * 80 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 100 + x * BLOCK_SIZE, 70 + i * 80 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_hold_piece(self): #Dibuja la pieza que esta almacenada
        font = pygame.font.Font(None, 24)
        hold_pieces_text = font.render("Hold Piece:", True, WHITE)
        self.screen.blit(hold_pieces_text, (SCREEN_WIDTH - 100, 300))
        if self.hold_piece:
            for y, row in enumerate(self.hold_piece.shape):
                for x, col in enumerate(row):
                    if col:
                        pygame.draw.rect(self.screen, self.hold_piece.color, (SCREEN_WIDTH - 100 + x * BLOCK_SIZE, 320 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH - 100 + x * BLOCK_SIZE, 320 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_score(self): #Dibuja el puntaje del jugador
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 100, 450))

    def show_start_screen(self): #Muestra la pantalla de inicio
        self.reset_game()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    #A continuacion los botones de la pantalla de inicio con sus funciones
                    if self.start_buttons[0].is_clicked(mouse_pos):
                        running = False
                    elif self.start_buttons[1].is_clicked(mouse_pos):
                        self.show_config_screen()
                    elif self.start_buttons[2].is_clicked(mouse_pos):
                        pygame.quit()
                        quit()

            self.screen.fill(GRAY)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            #El codigo superior es reutilizado, por defecto la pantalla tiene backgrounds predefinidos pero si hay una imagen definida por el usuario se intercambia por los predefinidos
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Proyecto: TETRIS", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 6))

            for button in self.start_buttons:
                button.draw(self.screen) #Dibuja en la pantalla los botones

            pygame.display.flip()

    def show_config_screen(self): #Muestra la pantalla de configuraciones
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    #A cada boton se le asigna una funcion
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
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 6))

            for button in self.config_buttons:
                button.draw(self.screen) #Se dibujan los botones en pantalla

            pygame.display.flip()

    def change_background(self): #Funcion para cambiar el fondo de pantalla ("background")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    #A los 3 primeros botones se les asigno un fondo de pantalla para cambiar a preferencia del usuario, el cuarto boton vuelve a la pantalla anterior
                    if self.background_buttons[0].is_clicked(mouse_pos):
                        self.settings["background"] = BACKGROUND_OPTION[0]
                        self.load_background()
                        self.save_settings()
                    elif self.background_buttons[1].is_clicked(mouse_pos):
                        self.settings["background"] = BACKGROUND_OPTION[1]
                        self.load_background()
                        self.save_settings()
                    elif self.background_buttons[2].is_clicked(mouse_pos):
                        self.settings["background"] = BACKGROUND_OPTION[2]
                        self.load_background()
                        self.save_settings()
                    elif self.background_buttons[3].is_clicked(mouse_pos):
                        running = False

            self.screen.fill(BLACK)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Backgrounds", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 6))

            for button in self.background_buttons:
                button.draw(self.screen)

            pygame.display.flip()

    def change_keys(self): #Funcion para cambiar las teclas a preferencia
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for button in self.key_buttons:
                        #Para todos excepto el ultimo boton que es el de "volver" se les asigno la funcion para cambiar de tecla
                        if self.key_buttons[6].is_clicked(mouse_pos):
                            running = False
                        elif button.is_clicked(mouse_pos):
                            self.change_key(button.text.lower())

            self.screen.fill(BLACK)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Change Keys", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 6))
            for button in self.key_buttons:
                button.draw(self.screen)

            pygame.display.flip()

    def change_key(self, key_name): #La funcion esta hecha para cambiar la tecla que esta por defecto a una elegida por el usuario
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.settings["key_bindings"][key_name] = event.key
                    self.save_settings()
                    waiting_for_key = False

            self.screen.fill(BLACK)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            message_font = pygame.font.Font(None, 24)
            message_text = message_font.render("Oprima una tecla para cambiar el boton", True, WHITE)
            self.screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2))
            pygame.display.flip()

    def handle_events(self): #Maneja los eventos del teclado
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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

    def update_board(self): #Actualiza el tablero después de que una pieza se coliziona.
        for y, row in enumerate(self.current_piece.shape):
            for x, col in enumerate(row):
                if col and self.current_piece.y + y >= 0:
                    self.board[self.current_piece.y + y][self.current_piece.x + x] = 1

    def clear_lines(self): #Actualiza las lineas cada vez que una se completa, las borra y sumas 100 puntos al score
        full_rows = [i for i, row in enumerate(self.board) if all(row)]
        for row in full_rows:
            del self.board[row]
            self.board.insert(0, [0] * BOARD_WIDTH)
        self.score += len(full_rows) * 100

    def handle_hold(self): # Esta funcion se encarga de almacenar una pieza o intercambiarla por una ya almacenada.
        if not self.hold_piece:
            self.hold_piece = self.current_piece
            self.current_piece = self.next_pieces.pop(0)
            self.next_pieces.append(self.create_piece())
        else:
            self.hold_piece, self.current_piece = self.current_piece, self.hold_piece

        self.hold_piece.x = BOARD_WIDTH // 2 - len(self.hold_piece.shape[0]) // 2
        self.hold_piece.y = 0

    def run(self): #Esta funcion ejecuta el bucle principal del juego.
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
            a = int(self.score)
            x = (a / 1500) + 5
            self.clock.tick(x) # Altera la velocidad de caida de las piezas en base al "score"

        self.show_game_over_screen() #Al perder muestra la pantalla de "Game Over"

    def show_pause_screen(self): #Al pausar el juego muestra la pantalla de inicio.
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
                        pygame.quit()
                        quit()

            self.screen.fill(BLACK)
            if self.bg_image:
                self.screen.blit(self.bg_image, (0, 0))
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("PAUSA", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 6))

            for button in self.start_buttons:
                button.draw(self.screen)

            pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill(BLACK)
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("GAME OVER", True, WHITE)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4 ))
        font_score = pygame.font.Font(None, 36)
        score_text = font_score.render(f"Your score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        pygame.time.wait(5000)

        self.run()