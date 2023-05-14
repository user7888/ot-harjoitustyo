import unittest
from repositories.save_repository import save_repository
from initialize_database import initialize_database
from objects.save import Save
from utils.setup import load_save

LEVEL_MAP = [[2, 1, 2, 3, 4],
             [5, 6, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]


class TestSaveRepository(unittest.TestCase):
    def setUp(self):
        initialize_database()
        save_repository.delete_all_saves()
        self.user_save = Save(20, 200, LEVEL_MAP, 1)
        self.user_save_newer = Save(10, 100, LEVEL_MAP, 2)

    def test_creating_and_finding_a_save(self):
        save_repository.create_save(self.user_save)
        save = save_repository.find_save()
        self.assertEqual(save[0], 20)
        self.assertEqual(save[1], 200)
        self.assertEqual(save[2], LEVEL_MAP)
        self.assertEqual(save[3], 1)

    def test_find_save_finds_newest_save(self):
        save_repository.create_save(self.user_save)
        save = save_repository.find_save()
        self.assertEqual(save[0], 20)
        self.assertEqual(save[1], 200)
        self.assertEqual(save[2], LEVEL_MAP)
        self.assertEqual(save[3], 1)

        save_repository.create_save(self.user_save_newer)
        save = save_repository.find_save()
        self.assertEqual(save[0], 10)
        self.assertEqual(save[1], 100)
        self.assertEqual(save[2], LEVEL_MAP)
        self.assertEqual(save[3], 2)

    def test_setup_module_load_save(self):
        save_repository.create_save(self.user_save)
        loaded_save = load_save()
        self.assertEqual(loaded_save.get_player_life(), 20)
        self.assertEqual(loaded_save.get_player_gold(), 200)
        self.assertEqual(loaded_save.map_state(), LEVEL_MAP)
        self.assertEqual(loaded_save.wave_state(), 1)
