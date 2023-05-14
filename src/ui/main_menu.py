from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import copy
import pygame
from ui.button import Button
import os
from utils import setup

dirname = os.path.dirname(__file__)
FPS = 60

class MainMenu:
    """A class for the main menu of the game. Through it, the
    user can start the game using "Start"-button, start a new using
    the "New game"-button and exit the game using the "Exit"-button.

    Attributes:
        clock: Clock object.
        event_queue: Pygame event queue.
        display: Pygame display object
        controller: GameStateController object.
        game_map: GameMap object.
        player: The player object.
        start_button: Starts the game.
        new_game_button: Starts a new game.
        quit_button: Closes the game.
    """
    
    def __init__(self, clock, event_queue, display, controller, game_map, player):
        """ Class constructor for creating the GameEndScreen object.

        Args:
            clock: Clock object.
            event_queue: Pygame event queue.
            display: Pygame display object
            controller: GameStateController object.
            game_map: The GameMap object.
            player: The Player object.
        """
        self._clock = clock
        self._event_queue = event_queue
        self.display = display
        self.controller = controller
        self.game_map = game_map
        self.player = player

        self.start_button = Button(270, 70, pygame.image.load(
            os.path.join(dirname, "..", "assets", "start_button22.png")
        ))

        self.new_game_button = Button(270, 200, pygame.image.load(
            os.path.join(dirname, "..", "assets", "new_game_button.png")
        ))

        self.quit_button = Button(270, 330, pygame.image.load(
            os.path.join(dirname, "..", "assets", "exit_button.png")
        ))

        self.mouse_position = None

    def start(self):
        while True:
            game_state = self.controller.get_game_state()
            if game_state != 'main menu':
                break
            self._handle_events()
            self.display.fill((0, 0, 0))

            self.mouse_position = pygame.mouse.get_pos()
            self.start_button.render(self.display)
            self.new_game_button.render(self.display)
            self.quit_button.render(self.display)

            self._clock.tick(FPS)
            pygame.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._handle_pygame_quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.check_for_input(self.mouse_position):
                    self._handle_start_button()
                    return False
                
                if self.new_game_button.check_for_input(self.mouse_position):
                    self._handle_new_game_button()
                    return False

                if self.quit_button.check_for_input(self.mouse_position):
                    self._handle_quit_button()
                    return False
    
    def _handle_pygame_quit(self):
        self.controller.set_state_terminated()
    
    def _handle_start_button(self):
        self.controller.set_state_pre_wave()
        self.game_map.reset_map_sprites()
        self.game_map.deselect_all_towers()
        self.controller.reset_waves()
    
    def _handle_new_game_button(self):
        print("reset function was called")
        self.controller.set_state_pre_wave()
        self.game_map.reset_map_sprites()
        print(copy.deepcopy(setup.MAP))
        self.game_map.reset_map(copy.deepcopy(setup.MAP))
        self.game_map.deselect_all_towers()
        self.controller.reset_waves()
        self.player.gold = 200
        self.player.life_total = 20
        self.controller.reset_current_wave()

    def _handle_quit_button(self):
        self.controller.set_state_terminated()
