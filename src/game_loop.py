import pygame

FPS = 60
class GameLoop:
    def __init__(self, map, clock, renderer, event_queue):
        self._map = map
        self._clock = clock
        self._renderer = renderer
        self._event_queue = event_queue
    
    def start(self):
        while True:
            if self._handle_events() == False:
                break
            
            # Time/ticks elapsed since game start.
            current_time = self._clock.get_ticks()
            
            # Update and render
            self._map.update(current_time)
            self._render()
            self._clock.tick(FPS)
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    
    def _render(self):
        self._renderer.render()