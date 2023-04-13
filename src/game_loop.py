import pygame
from utils.button import Button
import os

FPS = 60
dirname = os.path.dirname(__file__)

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

class GameLoop:
    def __init__(self, map, clock, renderer, event_queue, display):
        self._map = map
        self._clock = clock
        self._renderer = renderer
        self._event_queue = event_queue

        self.state_main_menu = True
        self.state_playing = False
        self.display = display

    
    def start(self):
        #print("starting game loop")
        #if self.state_main_menu:
        #    self._main_menu()

        while True:
            handler_response = self._handle_events()
            if handler_response == False:
                print("exiting game loop")
                # Use break or return False to
                # main menu loop
                break
            elif handler_response == -1:
                return -1
            
            MOUSE_POSITION = pygame.mouse.get_pos()
            
            # Time/ticks elapsed since game start.
            current_time = self._clock.get_ticks()
            
            # Update and render
            self._map.update(current_time)
            self._render()
            self._clock.tick(FPS)
    
    def _handle_events(self):
        for event in pygame.event.get():
            # Check if a escape is pressed
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return False

            if event.type == pygame.QUIT:
                return -1

    def _render(self):
        self._renderer.render()