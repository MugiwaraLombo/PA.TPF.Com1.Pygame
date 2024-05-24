import pygame
from tetris import Tetris

if __name__ == "__main__":
    pygame.init()
    tetris = Tetris()
    tetris.show_start_screen()
    tetris.run()
