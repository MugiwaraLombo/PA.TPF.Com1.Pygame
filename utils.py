import os

# Directorio para almacenar los archivos de configuración
CONFIG_DIR = "config"
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Dimensiones del tablero
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Tamaño de la ventana del juego
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500

# Tamaño del bloque
BLOCK_SIZE = min(SCREEN_WIDTH // BOARD_WIDTH, SCREEN_HEIGHT // BOARD_HEIGHT)

#Piezas del juego
SHAPES = [
            [[1, 1, 1, 1]],#I
            [[1, 1], [1, 1]],#O
            [[0, 1, 1], [1, 1, 0]],#S
            [[1, 1, 0], [0, 1, 1]],#Z
            [[1, 0, 0], [1, 1, 1]],#L
            [[0, 0, 1], [1, 1, 1]],#J
            [[0, 1, 0], [1, 1, 1]]#T
        ]

#Opciones de background
BACKGROUND_OPTION = ("config/bg1.jpg", "config/bg2.jpg", "config/bg3.jpg")