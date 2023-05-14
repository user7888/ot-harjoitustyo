import unittest
from sprites.monster import Monster
from clock import Clock

LEVEL_MAP = [[2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

CELL_SIZE = 64

class TestMonster(unittest.TestCase):
    def setUp(self):
        self.monster = Monster("normal", 1, 1)
        self.clock = Clock()

    def test_monster_starting_waypoint_is_set_correctly(self):
        self.assertEqual(self.monster.current_waypoint, 1)

    def test_monster_movement_y_direction(self):
        self.monster.rect.x = 1
        self.monster.rect.y = 1
        for _ in range(20):
            self.monster.move(self.clock.get_ticks())
        self.assertEqual(self.monster.rect.y, 21)

    def test_monster_movement_x_direction(self):
        self.monster.rect.x = 1
        self.monster.rect.y = 1
        for _ in range(20):
            self.monster.move(self.clock.get_ticks())
        self.assertEqual(self.monster.rect.x, 6)

    def test_waypoint_is_updated_after_old_is_reached(self):
        self.monster.rect.x = 180
        self.monster.rect.y = 500
        self.assertEqual(self.monster.current_waypoint, 1)
        for _ in range(20):
            self.monster.move(self.clock.get_ticks())
        self.assertEqual(self.monster.current_waypoint, 2)

    def test_current_location_function_works_correctly(self):
        current_location = self.monster.current_location()
        self.assertEqual(current_location[0], 1)
        self.assertEqual(current_location[1],  1)
