import unittest
from objects.projectile import Projectile

class TestProjectile(unittest.TestCase):
    def setUp(self):
        # Create the map object for tests.
        self.projectile = Projectile(1, 1, 2, 2, 1, 2)

    def test_projectile_reaches_its_target(self):
        self.projectile.update()
        self.assertEqual(self.projectile.rect.x, 2)
        self.assertEqual(self.projectile.rect.y, 2)