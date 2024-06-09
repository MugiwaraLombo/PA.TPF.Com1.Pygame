# Tetris

Este proyecto es una implementación del clásico juego Tetris usando Pygame.

## Archivos del proyecto

### 1. `main.py`

Este es el punto de entrada del juego. Crea una instancia de la clase `Tetris`, muestra la pantalla de inicio y ejecuta el bucle principal del juego.

### 2. `tetris.py`

Contiene la clase `Tetris`, que maneja la lógica principal del juego. Sus funciones principales incluyen:
- `__init__`: Inicializa pygame, el estado del juego y define varios atributos.
- `load_settings`: Carga las configuraciones del juego importadas desde utils.py.
- `save_settings`: Guarda las configuraciones del juego.
- `load_background`: Carga el fondo de pantalla.
- `reset_game`: Reinicia la pantalla del juego.
- `create_piece`: Crea una nueva pieza aleatoria.
- `draw_board`: Crea el tablero de juego.
- `draw_next_pieces`: Dibuja las próximas piezas que aparecerán en el juego.
- `draw_hold_piece`: Dibuja la pieza retenida.
- `draw_score`: Muestra la puntuación actual.
- `show_start_screen`: Muestra la pantalla de inicio.
- `show_config_screen`: Muestra la pantalla de configuraciones.
- `change_backgrounds`: Funcion para cambiar el fondo de pantalla y mostrar la pantalla para configurarlo
- `change_keys`: Muestra la pantalla para cambiar las teclas
- `change_key`: Funcion para cambiar las teclas
- `handle_events`: Maneja los eventos del teclado.
- `update_board`: Actualiza el tablero después de que una pieza se ha colocado.
- `clear_lines`: Limpia una linea cuando esta se completa.
- `handle_hold`: Almacena una pieza o la intercambia por una ya almacenada.
- `run`: Ejecuta el bucle principal del juego.
- `show_pause_screen`: Muestra la pantalla de pausa.
- `show_game_over`: Muestra la pantalla de game over.

### 3. `piece.py`

Define la clase `Piece`, que representa una pieza de Tetris. Sus funciones principales incluyen:
- `__init__`: Inicializa la pieza con su forma y color.
- `rotate`: Rota la pieza.
- `check_collision`: Detecta la colision de las piezas.
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

Para ejecutar el juego, simplemente corre el archivo `main.py`. Esto creará una instancia del juego Tetris, mostrará la pantalla de inicio y comenzará el bucle principal del juego. 

Durante el juego, puedes usar las siguientes teclas:

- Flecha izquierda: Mueve la pieza a la izquierda.
- Flecha derecha: Mueve la pieza a la derecha.
- Flecha abajo: Mueve la pieza hacia abajo.
- Flecha arriba: Rota la pieza.
- Espacio: Guarda la pieza para usarla luego. (si ya hay una pieza guardada la intercambia por la actual)
- ESC: Pausa el juego.

(Todas estas teclas son configurables y solo funcionan tal cual en el readme cuando no hay un archivo `settings.json` con una configuracion distinta)

# Programacion Avanzada - Trabajo Practico Final - Comision 1 - Proyecto Tetris
- Tema : Pygame
- Proyecto : Tetris
- Grupo 4 : Javier Lopez Acuña, Thomas Lombardo y Matias Ezequiel Lovato.
- *Cooparticipacion de Kevin Lomazzi*