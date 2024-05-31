import os

# Directorio para almacenar los archivos de configuración y puntajes
CONFIG_DIR = "config"
SCORES_FILE = os.path.join(CONFIG_DIR, "scores.json")
SETTINGS_FILE = os.path.join(CONFIG_DIR, "settings.json")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# Dimensiones del tablero
BOARD_WIDTH = 10
BOARD_HEIGHT = 25

# Tamaño de la ventana del juego
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500

# Tamaño del bloque
BLOCK_SIZE = min(SCREEN_WIDTH // BOARD_WIDTH, SCREEN_HEIGHT // BOARD_HEIGHT)
