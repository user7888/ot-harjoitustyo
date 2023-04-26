import pygame

class Renderer:
    def __init__(self, display, game_map):
        self._display = display
        self._level = game_map

    def render(self, ui):
        self._level.all_sprites.draw(self._display)
        self._level.outlines.draw(self._display)
        self._level.projectiles.draw(self._display)
        if self._level.selected_tower_active:
            self._level.selected_tower.draw_range_circle(self._display)
        ui.draw()
        pygame.display.update()
