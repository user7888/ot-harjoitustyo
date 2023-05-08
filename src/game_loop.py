import os
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
)
import pygame
from utils.build_menu import BuildMenu

FPS = 60
dirname = os.path.dirname(__file__)


class GameLoop:
    def __init__(self, game_map, clock, renderer, event_queue,
                 display, main_menu, pause_menu, controller, player, main_ui):

        self._map = game_map
        self._clock = clock
        self._renderer = renderer
        self._event_queue = event_queue
        self.display = display
        self.controller = controller
        self.player = player

        self.main_menu = main_menu
        self.pause_menu = pause_menu
        self.build_menu = main_ui
        self.mouse_position = pygame.mouse.get_pos()


    def start(self):
        while True:
            self.controller.update_game_state(self._map.monsters)
            game_state = self.controller.get_game_state()
            self.mouse_position = pygame.mouse.get_pos()
            self._handle_events()

            if game_state == 'terminated':
                break
            if game_state == 'initialized':
                self.controller.set_state_main_menu()
                self.main_menu.start()
                continue
            if game_state == 'main menu':
                self.controller.set_state_main_menu()
                self.main_menu.start()
                continue
            if game_state == 'paused':
                self.controller.set_state_paused()
                self.pause_menu.start()
                continue

            # Time/ticks elapsed since game start.
            current_time = self._clock.get_ticks()

            # Update and render
            self._map.update(current_time)
            # _render() changed to _renderer.render(self.build_menu)
            self._renderer.render(self.build_menu)
            self._clock.tick(FPS)
            self._map.hover_effect()

            # Side menu rendering

            #self.build_menu.draw()
            # Duplicate updates in game loop
            # and renderer
            #pygame.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            # Game is paused with escape key.
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.controller.set_state_paused()

            if event.type == pygame.QUIT:
                self.controller.set_state_terminated()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._map.deselect_all_towers()
                self.build_menu.check_for_inputs(self.mouse_position, self.player)
                self.build_menu.handle_game_map_click(self.mouse_position, self.player)
                
    def _render(self):
        self._renderer.render()

    # def _pause_game(self):
    #     return_value = self.pause_menu.start()

    #     if return_value == 'resume':
    #         self.current_state = 'running'
    #     elif return_value == 'exit':
    #         self.current_state = 'main menu'
    #     elif return_value == 'quit':
    #         self.current_state = 'terminated'

    # def _open_main_menu(self):
    #     return_value = self.main_menu.start()

    #     if return_value == 'start':
    #         self.current_state = 'running'
    #     elif return_value == 'quit':
    #         self.current_state = 'terminated'
