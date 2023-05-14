import unittest
from objects.player import Player

LEVEL_MAP = [[2, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

CELL_SIZE = 64

class TestPlayer(unittest.TestCase):
    def setUp(self):
        # Create the map object for tests.
        self.player = Player(20, 200)

    def test_buying_reduces_gold_by_correct_amount(self):
        self.assertEqual(self.player.gold, 200)
        self.player.buy(100)
        self.assertEqual(self.player.gold, 100)
        self.player.buy(200)
        self.assertEqual(self.player.gold, 100)

    def test_player_gold_is_increased_by_correct_amount(self):
        self.assertEqual(self.player.gold, 200)
        self.player.increase_gold(10)
        self.assertEqual(self.player.gold, 210)

    def test_player_can_be_damaged(self):
        self.assertEqual(self.player.life_total, 20)
        self.player.damage_player(10)
        self.assertEqual(self.player.life_total, 10)

    def is_alive_function_works_correctly(self):
        self.assertEqual(self.player.is_alive(), True)
        self.player.damage_player(20)
        self.assertEqual(self.player.is_alive(), False)







