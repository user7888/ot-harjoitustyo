import pygame
from utils.button import Button
import os

dirname = os.path.dirname(__file__)
FPS = 60

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class MainMenu:
    def __init__(self, clock, event_queue, display, game_loop):
        self._clock = clock
        self._event_queue = event_queue
        self.display = display
        self.game_loop = game_loop

        self.start_button = Button(270, 70, pygame.image.load(
            os.path.join(dirname, "..", "assets", "start_button.png")
        ))

        self.quit_button = Button(270, 270, pygame.image.load(
            os.path.join(dirname, "..", "assets", "quit_button.png")
        ))

        self.mouse_position = pygame.mouse.get_pos()
    
    def start(self):
        while True:
            if self._handle_events() == False:
                break
            
            # Old screen was left in the background
            # and start button drawn over it. Now
            # background is filled with black.
            self.display.fill((0, 0, 0))

            # Render buttons as a group?
            self.mouse_position = pygame.mouse.get_pos()
            self.start_button.render(self.display)
            self.quit_button.render(self.display)

            self._clock.tick(FPS)
            pygame.display.update()
    
    def _handle_events(self):
        for event in pygame.event.get():
            # Check if a escape is pressed
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False

            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.checkForInput(self.mouse_position):
                    print("start button was pressed")

                    # if game loop was exited using
                    # pygame quit.
                    return_value = self.game_loop.start()
                    if return_value == -1:
                        return False
                    print("exiting from main menu")
                    return
                
                if self.quit_button.checkForInput(self.mouse_position):
                    print("button was pressed")
                    return False