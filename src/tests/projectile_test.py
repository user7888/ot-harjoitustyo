import unittest
from objects.projectile import Projectile



class TestProjectile(unittest.TestCase):
    def setUp(self):
        monsters = ['monster', 'monster']
        # Create the map object for tests.
        self.projectile = Projectile('arrow', 1, 1, 2, 2, 1, 2, "monster",  monsters)

    # def __init__(self, type, x, y, target_x, target_y, speed, damage, target, monsters):
    def test_projectile_reaches_its_target(self):
        self.projectile.update()
        self.assertEqual(self.projectile.rect.x, 2)
        self.assertEqual(self.projectile.rect.y, 2)
    
    # after resolving a hit projetile is deleted
    def test_resolve_hit_function_works_correctly(self):
        pass