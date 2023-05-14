import os
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
)
import pygame
from ui.ending_screen import GameEndScreen
from repositories.save_repository import save_repository

FPS = 60
dirname = os.path.dirname(__file__)

class GameLoop:
    """A class for main game loop. It is started when the application
    starts. In the while-loop, it uses the GameStateControllers services to check the
    current game state and based on the response it starts the main menu, pause menu
    and game ending screen.

    Attributes:
        map: The game map object.
        clock: Clock object used for all time based events.
        renderer: Responsible for rendering the graphics.
        event_queue: Pygame event queue.
        display: Pygame display object.
        controller: GameStateController object.
        player: The player object.
        main_menu: The main menu object.
        pause_menu: The pause menu object.
        main_ui: The MainUI object
        end_screen: The GameEndScreen object.
    """
    def __init__(self, game_map, clock, renderer, event_queue,
                 display, main_menu, pause_menu, controller, player, main_ui):
        """ Class constructor for creating the GameLoop object.

        Args:
            map: The game map object.
            clock: Clock object used for all time based events.
            renderer: Responsible for rendering the graphics.
            event_queue: Pygame event queue.
            display: Pygame display object.
            controller: GameStateController object.
            player: The player object.
            main_menu: The main menu object.
            pause_menu: The pause menu object.
            main_ui: The MainUI object
            end_screen: The GameEndScreen object.
        """
        self._map = game_map
        self._clock = clock
        self._renderer = renderer
        self._event_queue = event_queue
        self.display = display
        self.controller = controller
        self.player = player

        self.main_menu = main_menu
        self.pause_menu = pause_menu
        self.main_ui = main_ui
        self.mouse_position = pygame.mouse.get_pos()
        self.end_screen = GameEndScreen(clock, event_queue, display, controller)


    def start(self):
        while True:
            self.controller.update_game_state(self._map.monsters)
            game_state = self.controller.get_game_state()
            self.mouse_position = pygame.mouse.get_pos()
            self._handle_events()

            if game_state == 'terminated':
                self._exit_game()
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
                # State sets should be removed right?
                #self.controller.set_state_paused()
                self.pause_menu.start()
                continue
            if not self.player.is_alive():
                self.controller.set_state_game_over()
                self.end_screen.start()
                continue
            if self.controller.all_waves_completed():
                self.controller.set_state_game_won()
                self.end_screen.start()
                continue

            current_time = self._clock.get_ticks()
            self._map.update(current_time)
            self._renderer.render(self.main_ui)
            self._clock.tick(FPS)


    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.controller.set_state_paused()

            if event.type == pygame.QUIT:
                self.controller.set_state_terminated()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self._map.deselect_all_towers()
                self.main_ui.check_for_inputs(self.mouse_position)
                self.main_ui.handle_game_map_click(self.mouse_position, self.player)

    def _render(self):
        self._renderer.render()

    def _exit_game(self):
        map_state = self._map.get_level_map()
        wave_state = self.controller.get_info()
        player_health = self.player.current_health()
        player_gold = self.player.current_gold()
        self.controller.save_game(map_state, wave_state, player_health, player_gold)
        