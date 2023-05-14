import copy
from repositories.save_repository import save_repository
from objects.save import Save

MAP = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,],
       [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,],
       [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1,],
       [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 3,]]
WAVE = 0
CELL_SIZE = 64
PLAYER_HEALTH = 20
PLAYER_GOLD = 200
SIDE_MENU_WIDTH = 300
HEIGHT = len(MAP)
WIDTH = len(MAP[0])

def load_save():
    save_data = save_repository.find_save()
    if not save_data:
        print("Save data not found")
        print("New save created")
        return create_new_save()

    return Save(save_data[0], save_data[1], save_data[2], save_data[3])

def create_new_save():
    return Save(PLAYER_HEALTH, PLAYER_GOLD, copy.deepcopy(MAP), WAVE)

if __name__ == "__main__":
    load_save()
