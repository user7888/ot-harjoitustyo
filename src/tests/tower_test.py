import unittest
from sprites.tower import Tower

class TestTower(unittest.TestCase):
    def setUp(self):
        # Create the map object for tests.
        self.tower = Tower(1, 1)

    def test_tower_location_on_game_map(self):
        self.assertEqual(self.tower.rect.x, 1)
        self.assertEqual(self.tower.rect.y, 1)