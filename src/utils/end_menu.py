import os
import pygame
from utils.button import Button

dirname = os.path.dirname(__file__)
FPS = 60

class EndMenu:
    def __init__(self, clock, event_queue, display, controller):
        self._clock = clock
        self._event_queue = event_queue
        self.display = display
        self.controller = controller


        self.screen_title_1 = Button(270, 30, pygame.image.load(
            os.path.join(dirname, "..", "assets", "game_title.png")))
        self.screen_title_2 = Button(500, 30, pygame.image.load(
            os.path.join(dirname, "..", "assets", "over_title.png")))

        self.exit_button = Button(380, 200, pygame.image.load(
            os.path.join(dirname, "..", "assets", "exit_button.png")
        ))

        self.mouse_position = pygame.mouse.get_pos()
        self.menu_state = 'Empty'

    def start(self):
        while True:
            game_state = self.controller.get_game_state()
            if game_state != 'game over':
                break
            
            self._handle_events()

            # Old screen was left in the background
            # and start button drawn over it. Now
            # background is filled with black.
            self.display.fill((0, 0, 0))

            # Render buttons as a group?
            self.mouse_position = pygame.mouse.get_pos()
            self.screen_title_1.render(self.display)
            self.screen_title_2.render(self.display)
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
                # Handle exit button event.
                if self.exit_button.checkForInput(self.mouse_position):
                    self._handle_exit_button()
                    return False
    
    def _handle_pygame_quit(self):
        self.controller.set_state_terminated()
    
    def _handle_exit_button(self):
        self.controller.set_state_main_menu()