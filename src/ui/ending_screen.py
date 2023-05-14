import os
import pygame
from ui.button import Button

dirname = os.path.dirname(__file__)
FPS = 60

class GameEndScreen:
    """A class for the ending screen of the game displayed when
    game is over. In it, "Game Over" text and an "Exit"-button
    is displayed.

    Attributes:
        clock: Clock object.
        event_queue: Pygame event queue.
        display: Pygame display object
        controller: GameStateController object.
        screen_title_1: Part 1 of the screen title.
        screen_title_2: Part 2 of the screen title.
        exit_button: Button used to exit to main menu.
    """
    def __init__(self, clock, event_queue, display, controller):
        """ Class constructor for creating the GameEndScreen object.

        Args:
            clock: Clock object.
            event_queue: Pygame event queue.
            display: Pygame display object
            controller: GameStateController object.
        """
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

    def start(self):
        while True:
            game_state = self.controller.get_game_state()
            if game_state not in  ['game over', 'game won']:
                break

            self._handle_events()
            self.display.fill((0, 0, 0))

            self.mouse_position = pygame.mouse.get_pos()
            self.screen_title_1.render(self.display)
            self.screen_title_2.render(self.display)
            self.exit_button.render(self.display)

            self._clock.tick(FPS)
            pygame.display.update()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._handle_pygame_quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle exit button event.
                if self.exit_button.check_for_input(self.mouse_position):
                    self._handle_exit_button()
                    return False

    def _handle_pygame_quit(self):
        self.controller.set_state_terminated()

    def _handle_exit_button(self):
        self.controller.set_state_main_menu()
