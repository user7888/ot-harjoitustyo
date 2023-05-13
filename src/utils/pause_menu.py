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

dirname = os.path.dirname(__file__)
FPS = 60


class PauseMenu:
    def __init__(self, clock, event_queue, display, controller):
        self._clock = clock
        self._event_queue = event_queue
        self.display = display
        self.controller = controller

        self.screen_title = Button(270, 0, pygame.image.load(
            os.path.join(dirname, "..", "assets", "pause_title.png")))
        self.resume_button = Button(270, 150, pygame.image.load(
            os.path.join(dirname, "..", "assets", "resume_button.png")
        ))
        self.exit_button = Button(270, 300, pygame.image.load(
            os.path.join(dirname, "..", "assets", "exit_button.png")
        ))

        self.mouse_position = pygame.mouse.get_pos()
        self.menu_state = 'Empty'

    def start(self):
        while True:
            game_state = self.controller.get_game_state()
            if game_state != 'paused':
                break
            
            self._handle_events()
            self.display.fill((0, 0, 0))
            self.mouse_position = pygame.mouse.get_pos()
            self.screen_title.render(self.display)
            self.resume_button.render(self.display)
            self.exit_button.render(self.display)

            self._clock.tick(FPS)
            pygame.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            # Handle the event when game is
            # exited using pygame quit.
            if event.type == pygame.QUIT:
                self._handle_pygame_quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle resume button event.
                if self.resume_button.check_for_input(self.mouse_position):
                    self._handle_resume_button()
                    return False
                # Handle exit button event.
                if self.exit_button.check_for_input(self.mouse_position):
                    self._handle_exit_button()
                    return False
    
    def _handle_pygame_quit(self):
        self.controller.set_state_terminated()
    
    # Resume button needs to set the game state
    # to what ever the state was before pause
    def _handle_resume_button(self):
        if self.controller.get_previous_game_state() == 'pre wave':
            self.controller.set_state_pre_wave()
        elif self.controller.get_previous_game_state() == 'running':
            self.controller.set_state_running()
    
    def _handle_exit_button(self):
        self.controller.set_state_main_menu()
