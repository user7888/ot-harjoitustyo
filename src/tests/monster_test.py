import unittest
from sprites.monster import Monster

LEVEL_MAP = [[2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

CELL_SIZE = 64

class TestMonster(unittest.TestCase):
    def setUp(self):
        # Create the map object for tests.
        self.monster = Monster(1, 1)

    def test_monster_starting_waypoint_is_set_correctly(self):
        self.assertEqual(self.monster.current_waypoint, 1)
    
    def test_set_destination_updates_destination_reached_correctly(self):
        old_waypoint = self.monster.current_waypoint
        self.monster.set_destination_reached = True
        self.monster.set_destination()
        self.assertGreater(self.monster.current_waypoint, old_waypoint)
    
    def test_set_destination_sets_waypoint_to_two_after_the_first_waypoint_is_reached(self):
        self.monster.rect.x = 5
        self.monster.rect.y = 510
        self.monster.set_destination()
        self.assertEqual(self.monster.current_waypoint, 2)
    
    def test_monster_movement_positive_y_direction(self):
        self.assertEqual(self.monster.rect.y, 1)
        self.monster.set_destination()
        for n in range(20):
            self.monster.move()
        self.assertEqual(self.monster.rect.y, 21)
    
    def test_monster_movement_positive_x_direction(self):
        self.monster.rect.x = 5
        self.monster.rect.y = 510
        self.monster.set_destination()
        self.assertEqual(self.monster.rect.x, 5)
        for n in range(20):
            self.monster.move()
        self.assertEqual(self.monster.rect.x, 25)

    def test_monster_movement_negative_y_direction(self):
        self.monster.current_waypoint = 2
        self.monster.rect.x = 190
        self.monster.rect.y = 510
        self.monster.set_destination()
        print(self.monster.current_waypoint)
        self.assertEqual(self.monster.rect.y, 510)
        for n in range(20):
            self.monster.move()
        self.assertEqual(self.monster.current_waypoint, 3)
        self.assertEqual(self.monster.rect.y, 490)
    
    def test_monster_movement_negative_x_direction(self):
        self.monster.current_waypoint = 5
        self.monster.rect.x = 700
        self.monster.rect.y = 190
        self.monster.set_destination()
        print(self.monster.current_waypoint)
        self.assertEqual(self.monster.rect.x, 700)
        for n in range(20):
            self.monster.move()
        self.assertEqual(self.monster.current_waypoint, 6)
        self.assertEqual(self.monster.rect.x, 680)
    
    def test_current_location_function_works_correctly(self):
        current_location = self.monster.current_location()
        self.assertEqual((1, 1), current_location)