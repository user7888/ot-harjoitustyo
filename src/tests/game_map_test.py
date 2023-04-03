import unittest
from game_map import Map

LEVEL_MAP = [[2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

CELL_SIZE = 64

class TestMap(unittest.TestCase):
    def setUp(self):
        # Create the map object for tests.
        self.map = Map(LEVEL_MAP, CELL_SIZE)

    # Helper function. Compare the location of sprite
    # to given coordinates.
    def assert_coordinates_equal(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)
    
    def test_a_monster_is_created_at_top_left_corner(self):
        # Get list of all monster sprites.
        monsters = self.map.monsters.sprites()
        self.assert_coordinates_equal(monsters[0], 0 * CELL_SIZE, 0 * CELL_SIZE)

    def test_monster_can_be_moved(self):
        monsters = self.map.monsters.sprites()
        # Starting location at the leftmost upper corner.
        self.assert_coordinates_equal(monsters[0], 0 * CELL_SIZE, 0 * CELL_SIZE)
        # Move monster 1 CELL_SIZE downwards.
        self.map.move_monster(dy=+CELL_SIZE)
        self.assert_coordinates_equal(monsters[0], 0 * CELL_SIZE, 1* CELL_SIZE)
        # Move monster 1 CELL_SIZE to right.
        self.map.move_monster(dx=+CELL_SIZE)
        self.assert_coordinates_equal(monsters[0], 1 * CELL_SIZE, 1* CELL_SIZE)