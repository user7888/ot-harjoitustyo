import pygame
from sprites.monster import Monster
from sprites.floor import Floor

class Map:
    def __init__(self, level_map, cell_size):
        self.cell_size = cell_size

        self.floors = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        
        self._initialize_sprites(level_map)
        return

    # Initialize all sprites
    def _initialize_sprites(self, level_map):
        height = len(level_map)
        width = len(level_map[0])

        for y in range(height):
            for x in range(width):
                cell = level_map[y][x]
                normalized_x = x * self.cell_size
                normalized_y = y * self.cell_size
            
                # Determine sprites here.
                if cell == 0:
                    # Floor tile
                    self.floors.add(Floor(normalized_x, normalized_y))
                elif cell == 2:
                    # Monster tile
                    self.monsters.add(Monster(normalized_x, normalized_y))
                    self.floors.add(Floor(normalized_x, normalized_y))
        
        self.all_sprites.add(
            self.floors,
            self.monsters
        )
    
    def move_monster(self, dx=0, dy=0):
        # All monsters are in a pygame sprite group.
        monster_list = self.monsters.sprites()
        monster_list[0].rect.move_ip(dx, dy)
        
    

    
