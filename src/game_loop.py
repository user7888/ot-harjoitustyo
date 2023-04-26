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
                 display, main_menu, pause_menu, controller, player):

        self._map = game_map
        self._clock = clock
        self._renderer = renderer
        self._event_queue = event_queue
        self.display = display
        self.controller = controller
        self.player = player

        self.main_menu = main_menu
        self.pause_menu = pause_menu
        self.build_menu = BuildMenu(clock, event_queue, display, controller, game_map)
        self.mouse_position = pygame.mouse.get_pos()


    def start(self):
        while True:
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

                # Side menu inputs.
                if self.build_menu.buy_button.checkForInput(self.mouse_position):
                    self.build_menu.handle_buy_button(self.player)
                elif self.build_menu.sell_button.checkForInput(self.mouse_position):
                    self.build_menu.handle_sell_button(self.player)
                elif self.build_menu.build_button.checkForInput(self.mouse_position):
                    self.build_menu.handle_build_button(self.player)
                
                # Game sprite inputs.
                for tower in self._map.towers:
                    # Problems: selected tower needs
                    # two clicks to update.
                    self._map.set_selected_tower()
                    click = tower.tower_was_clicked(self.build_menu.get_current_state())
                    if click:
                        self.build_menu.handle_tower_click(self.player, tower)

                # Building.
                if self.build_menu.get_current_state() == "building":
                    self._map.place_tower()


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
