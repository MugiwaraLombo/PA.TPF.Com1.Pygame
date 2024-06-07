import pygame

class Button:
    def __init__(self, text, font, color, position):
        self.text = text
        self.font = font
        self.color = color
        self.position = position

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        rect = text_surface.get_rect(center=self.position)
        screen.blit(text_surface, rect)

    def is_clicked(self, mouse_pos):
        rect = self.font.render(self.text, True, self.color).get_rect(center=self.position)
        return rect.collidepoint(mouse_pos)