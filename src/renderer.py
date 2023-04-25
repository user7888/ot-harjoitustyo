import pygame

class Renderer:
    def __init__(self, display, game_map):
        self._display = display
        self._level = game_map

    def render(self):
        self._level.all_sprites.draw(self._display)
        self._level.outlines.draw(self._display)

        self._level.projectiles.draw(self._display)
        pygame.display.update()
