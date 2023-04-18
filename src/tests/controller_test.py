import unittest
import pygame
from utils.main_menu import MainMenu
from utils.controller import Controller

class StubClock:
    def tick(self, fps):
        pass

    def get_ticks(self):
        return 0

class StubEvent:
    def __init__(self, event_type, event_key):
        self.type = event_type
        self.key = event_key

class StubEventQueue:
    def __init__(self, events):
        self._events = events
    
    def get(self):
        return self._events

class StubDisplay:
    def display(self):
        return 'display'

class StubController:
    def get_state(self):
        return 'current state'

class TestController(unittest.TestCase):
    def setUp(self):
        events = [ StubEvent(pygame.KEYDOWN, pygame.K_LEFT),
        ]
        self.controller = Controller()
        self.main_menu = MainMenu(StubClock(), StubEventQueue(events),  StubDisplay(), self.controller)

    def test_game_can_be_set_to_initialized_state(self):
        self.controller.set_state_initialized()
        self.assertEqual(self.controller.get_game_state(), 'initialized')
    
    def test_game_can_be_set_to_main_menu_state(self):
        self.controller.set_state_main_menu()
        self.assertEqual(self.controller.get_game_state(), 'main menu')
    
    def test_game_can_be_set_to_running_state(self):
        self.controller.set_state_running()
        self.assertEqual(self.controller.get_game_state(), 'running')
    
    def test_game_can_be_set_to_paused_state(self):
        self.controller.set_state_paused()
        self.assertEqual(self.controller.get_game_state(), 'paused')
    
    def test_game_can_be_set_to_terminated_state(self):
        self.controller.set_state_terminated()
        self.assertEqual(self.controller.get_game_state(), 'terminated')
