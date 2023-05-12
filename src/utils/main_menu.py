from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import pygame
from utils.button import Button
import os
from utils import setup

dirname = os.path.dirname(__file__)
FPS = 60

class MainMenu:
    def __init__(self, clock, event_queue, display, controller, game_map, player):
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
        self.menu_state = 'Empty'

    def start(self):
        while True:
            game_state = self.controller.get_game_state()
            if game_state != 'main menu':
                break
            self._handle_events()
            
            # Old screen was left in the background
            # and start button drawn over it. Now
            # background is filled with black.
            self.display.fill((0, 0, 0))

            # Render buttons as a group?
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
        self.controller.reset_waves()
    
    def _handle_new_game_button(self):
        self.controller.set_state_pre_wave()
        self.game_map.reset_map_sprites()
        self.game_map.reset_map(setup.MAP)
        self.controller.reset_waves()
        self.player.gold = 200
        self.player.life_total = 20
        self.controller.reset_current_wave()

    def _handle_quit_button(self):
        self.controller.set_state_terminated()
