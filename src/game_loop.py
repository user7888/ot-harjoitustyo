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
    def __init__(self, map, clock, renderer, event_queue, display, main_menu, pause_menu):
        self._map = map
        self._clock = clock
        self._renderer = renderer
        self._event_queue = event_queue

        self.state_main_menu = True
        self.state_playing = False
        self.display = display

        self.main_menu = main_menu
        self.pause_menu = pause_menu
        self.states = {'initialized': 'Game is initialized', 
                       'main menu': 'Game is in main menu',
                       'running': 'Game is running',
                       'paused': 'Game is in pause menu',
                       'terminated': 'Game is exiting'}
        
        self.current_state = 'initialized'

    
    def start(self):
        while True:
            handler_response = self._handle_events()

            if self.current_state == 'terminated':
                break
            elif self.current_state == 'initialized':
                self._open_main_menu()
            elif self.current_state == 'main menu':
                self._open_main_menu()

            MOUSE_POSITION = pygame.mouse.get_pos()
            
            # Time/ticks elapsed since game start.
            current_time = self._clock.get_ticks()
            
            # Update and render
            self._map.update(current_time)
            self._render()
            self._clock.tick(FPS)
    
    def _handle_events(self):
        for event in pygame.event.get():
            # Game is paused with escape key.
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.current_state = 'paused'
                    self._pause_game()
                    return

            if event.type == pygame.QUIT:
                self.current_state = 'terminated'
                return

    def _render(self):
        self._renderer.render()
    
    def _pause_game(self):
        return_value = self.pause_menu.start()

        if return_value == 'resume':
            self.current_state = 'running'
        elif return_value == 'exit':
            self.current_state = 'main menu'
        elif return_value == 'quit':
            self.current_state = 'terminated'
    
    def _open_main_menu(self):
        return_value = self.main_menu.start()

        if return_value == 'start':
            self.current_state = 'running'
        elif return_value == 'quit':
            self.current_state = 'terminated'

