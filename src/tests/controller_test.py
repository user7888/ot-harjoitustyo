import unittest
import pygame
from ui.main_menu import MainMenu
from game_logic.controller import GameStateController
from clock import Clock

MAP = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,],
       [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,],
       [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1,],
       [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3,]]

class StubClock:
    def tick(self, fps):
        pass

    def get_ticks(self):
        return 0
class StubGameMap:
    def __init__(self, game_map):
        self.map = game_map

class StubPlayer:
    def __init__(self):
        self.player = "player"

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
        starting_wave = 1
        self.controller = GameStateController(starting_wave)
        self.player = StubPlayer()
        self.clock = Clock()
        self.waves = [
            {'normal': 5, 'fast':2, 'big':1, 'frequency': 500},
            {'normal': 4, 'fast':1, 'big':1, 'frequency': 1000},
            {'normal': 5, 'fast':2, 'big':1, 'frequency': 1000}
        ]

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

    def test_game_can_be_set_to_pre_wave_state(self):
        self.controller.set_state_pre_wave()
        self.assertEqual(self.controller.get_game_state(), 'pre wave')

    def test_game_can_be_set_to_game_over_state(self):
        self.controller.set_state_game_over()
        self.assertEqual(self.controller.get_game_state(), 'game over')

    def test_game_can_be_set_to_game_won_state(self):
        self.controller.set_state_game_won()
        self.assertEqual(self.controller.get_game_state(), 'game won')

    def test_should_spawn_monster_returns_false_when_wave_is_empty(self):
        self.controller.set_state_running()
        self.controller.waves[self.controller.get_info()]['normal'] -= 100
        self.controller.waves[self.controller.get_info()]['fast'] -= 100
        self.controller.waves[self.controller.get_info()]['big'] -= 100
        response = self.controller.should_spawn_monster(self.clock.get_ticks())
        self.assertEqual(response, False)
        # Check if wave is completed
        self.assertEqual(self.controller.get_info(), True)

    def test_get_next_monster_type_returns_the_correct_type(self):
        self.controller.waves[self.controller.get_info()]['normal'] -= 100
        self.controller.waves[self.controller.get_info()]['fast'] -= 100
        self.assertEqual(self.controller.get_next_monster_type(), None)

        # self.controller.reset_waves()
        # self.controller.waves[self.controller.get_info()]['normal'] -= 100
        # self.assertEqual(self.controller.get_next_monster_type(), 'fast')

        self.controller.reset_waves()
        self.assertEqual(self.controller.get_next_monster_type(), 'normal')

    def test_game_state_is_set_to_pre_wave_after_wave_is_completed(self):
        self.controller.set_state_running()
        self.controller.waves[self.controller.get_info()]['normal'] -= 100
        self.controller.waves[self.controller.get_info()]['fast'] -= 100
        self.controller.waves[self.controller.get_info()]['big'] -= 100
        self.controller.get_next_monster_type()
        self.controller.update_game_state([])
        self.assertEqual(self.controller.get_game_state(), 'pre wave')
