import pygame

class Renderer:
    def __init__(self, display, map):
        self._display = display
        self._level = map
    
    def render(self):
        self._level.all_sprites.draw(self._display)
        pygame.display.update()
