# Tetris

Este proyecto es una implementación del clásico juego Tetris usando Pygame.

## Archivos del proyecto

### 1. `main.py`

Este es el punto de entrada del juego. Inicializa Pygame, crea una instancia de la clase `Tetris`, muestra la pantalla de inicio y ejecuta el bucle principal del juego.

### 2. `tetris.py`

Contiene la clase `Tetris`, que maneja la lógica principal del juego. Sus funciones principales incluyen:
- `__init__`: Inicializa el estado del juego.
- `create_piece`: Crea una nueva pieza aleatoria.
- `handle_events`: Maneja los eventos del teclado.
- `move_piece`: Mueve la pieza actual.
- `check_collision`: Comprueba si una pieza ha colisionado con los límites o con otras piezas.
- `draw_board`: Dibuja el tablero de juego.
- `draw_next_pieces`: Dibuja las próximas piezas que aparecerán en el juego.
- `draw_hold_piece`: Dibuja la pieza retenida.
- `draw_score`: Muestra la puntuación actual.
- `show_start_screen`: Muestra la pantalla de inicio.
- `draw_pause_screen`: Muestra la pantalla de pausa.
- `draw_game_over_screen`: Muestra la pantalla de fin del juego.
- `hold_current_piece`: Permite al jugador retener una pieza para usarla más tarde.
- `update_board`: Actualiza el tablero después de que una pieza se ha colocado.
- `run`: Ejecuta el bucle principal del juego.

### 3. `piece.py`

Define la clase `Piece`, que representa una pieza de Tetris. Sus funciones principales incluyen:
- `__init__`: Inicializa la pieza con su forma y color.
- `rotate`: Rota la pieza.
- `move`: Mueve la pieza en el tablero.
- `draw`: Dibuja la pieza en la pantalla.

### 4. `button.py`

Define la clase `Button`, que representa un botón interactivo en la interfaz del juego. Sus funciones principales incluyen:
- `__init__`: Inicializa el botón con su posición, tamaño y texto.
- `draw`: Dibuja el botón en la pantalla.
- `is_clicked`: Verifica si el botón ha sido clicado.

### 5. `utils.py`

Contiene constantes y configuraciones usadas en el juego, como colores, dimensiones del tablero y de la pantalla, y rutas a archivos de configuración y puntuaciones.

## Bibliotecas utilizadas

- `pygame`: Biblioteca principal para la creación del juego, usada para manejar gráficos, eventos, y sonidos.
- `random`: Para generar piezas aleatorias.
- `os`: Para manejar rutas de archivos.
- `json`: Para leer y escribir archivos de configuración y puntuaciones.

## Ejecución del juego

Para ejecutar el juego, simplemente corre el archivo `main.py`. Esto inicializará Pygame, creará una instancia del juego Tetris, mostrará la pantalla de inicio y comenzará el bucle principal del juego. 

Durante el juego, puedes usar las siguientes teclas:

- Flecha izquierda: Mueve la pieza a la izquierda.
- Flecha derecha: Mueve la pieza a la derecha.
- Flecha abajo: Mueve la pieza hacia abajo.
- Flecha arriba: Rota la pieza.
- Espacio: Deja caer la pieza hasta el fondo.
- P: Pausa el juego.

# Programacion Avanzada - Trabajo Practico Final - Comision 1
- Tema : Pygame
- Proyecto : Tetris
- Grupo 4 : Kevin Lommazi, Thomas Lombardo y Matias Ezequiel Lovato.
