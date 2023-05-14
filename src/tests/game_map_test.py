import unittest
import pygame
from game_logic.game_map import GameMap
from sprites.monster import Monster
from sprites.tower import Tower
from objects.projectile import Projectile
from clock import Clock

LEVEL_MAP = [[2, 1, 2, 3, 4],
             [5, 6, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]

CELL_SIZE = 64

class StubDisplay:
    def display(self):
        return 'display'

class StubPlayer:
    def __init__(self, health, gold):
        self.health = health
        self.gold = gold

    def buy(self, cost):
        self.gold -= cost
        return True

    def increase_gold(self, gold):
        self.gold += gold

class StubController:
    def __init__(self):
        self.state = 'normal'
        self.spawn_time = None

    def should_spawn_monster(self, current_time):
        self.spawn_time = current_time
        return True

    def get_next_monster_type(self):
        return 'normal'

    def set_previous_spawn_time(self, time):
        self.spawn_time = time

class TestMap(unittest.TestCase):
    def setUp(self):
        # Create the map object for tests.
        self.clock = Clock()
        display = pygame.display.set_mode((500, 500))

        self.map = GameMap(LEVEL_MAP, CELL_SIZE, display, StubController(), StubPlayer(20, 200))
        self.monster = Monster("normal", 1, 1)
        self.map.monsters.add(self.monster)
        self.current_time = self.clock.get_ticks()

    def assert_coordinates_equal(self, sprite, x, y):
        self.assertEqual(sprite.rect.x, x)
        self.assertEqual(sprite.rect.y, y)

    def test_update_function_moves_monsters(self):
        self.assert_coordinates_equal(self.monster, 1, 1)
        for _ in range(10):
            self.current_time = self.clock.get_ticks()
            self.map.update(self.current_time)
            self.clock.tick(60)
        # First destination of monster is x: 6 y: 510
        # and after 10 updates coordinates should be x:6 y: 10
        self.assert_coordinates_equal(self.monster, 6, 10)

    def test_projectile_hits_can_be_resolved(self):
        projectile = Projectile('wizard', 1, 1, 2, 2, 1, 2, self.monster,  self.map.monsters)
        self.map.projectiles.add(projectile)

        self.assertEqual(len(self.map.projectiles), 1)
        for _ in range(10):
            self.current_time = self.clock.get_ticks()
            self.map.update(self.current_time)
            self.clock.tick(60)
        # First destination of monster is x: 6 y: 510
        # and after 10 updates coordinates should be x:6 y: 10
        self.assertEqual(len(self.map.projectiles), 0)

    def test_tower_shooting_in_update_function(self):
        tower = Tower('arrow', 1, 1)
        self.map.towers.add(tower)
        time_before = tower.time_of_previous_shooting
        for _ in range(20):
            self.current_time = self.clock.get_ticks()
            self.map.update(self.current_time)
            self.clock.tick(60)
        time_after = tower.time_of_previous_shooting
        self.assertGreater(time_after, time_before)

    def test_place_tower_function(self):
        self.assertEqual(self.map.level_map[0][0], 2)
        # Mouse position for Map tile [0][1]
        mouse_position = (120, 0)
        return_value = self.map.place_tower(mouse_position, 'arrow')
        self.assertEqual(self.map.level_map[0][1], 4)
        self.assertEqual(return_value, 'Tower built successfully')

    def test_spawn_monster_adds_a_monster_to_sprite_group(self):
        before_test_monsters = len(self.map.monsters)
        self.assertEqual(len(self.map.monsters), before_test_monsters)
        self.map.spawn_monsters(self.current_time)
        self.assertEqual(len(self.map.monsters), before_test_monsters+1)

    def test_sell_tower_increases_player_gold(self):
        mouse_position = (0, 65)
        self.assertEqual(self.map.player.gold, 200)
        self.map.sell_tower(mouse_position)
        # Sell value of this tower is 40 gold.
        self.assertEqual(self.map.player.gold, 240)

    def test_select_tower_sets_selected_tower_active(self):
        mouse_position = (0, 65)
        self.assertEqual(self.map.selected_tower['active'], False)
        self.map.select_tower(mouse_position)
        self.assertEqual(self.map.selected_tower['active'], True)

    def test_reset_map_sprites_clears_monster_group(self):
        self.assertTrue(len(self.map.monsters) > 0)
        self.map.reset_map_sprites()
        self.assertEqual(len(self.map.monsters), 0)
