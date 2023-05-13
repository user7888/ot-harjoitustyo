import random
import pygame
from sprites.monster import Monster
from sprites.floor import Floor
from sprites.ground import Ground
from sprites.tower import Tower
from sprites.hearth import Hearth
from sprites.hover_outline import HoverOutline
from objects.projectile import Projectile
import utils.stats as stats

class Map:
    # Sprite groups.
    ground_tiles = pygame.sprite.Group()
    floors = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    hearth = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    outlines = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    # Tower selecting.
    selected_tower = {'active': False, 'tower': None}
    # Map dimensions (cell).
    map_size = {'height': None, 'width': None}

    def __init__(self, map_layout, cell_size, display, controller, player):
        self.cell_size = cell_size
        self.level_map = map_layout
        print("early level_map", type(self.level_map))
        print("early map_layout (parameter)", map_layout)
        self.display = display
        self.controller = controller
        self.player = player

        self._set_map_height_width()
        self._initialize_sprites(self.level_map)

    # level_map is the map state, based on it the game
    # is drawn.
    def _initialize_sprites(self, level_map):
        for y_cell in range(self.map_size['height']):
            for x_cell in range(self.map_size['width']):
                cell = level_map[y_cell][x_cell]
                normalized_x = x_cell * self.cell_size
                normalized_y = y_cell * self.cell_size
                if cell == 0:
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                elif cell == 1:
                    self.floors.add(Floor(normalized_x, normalized_y))
                elif cell == 2:
                    self.monsters.add(Monster(normalized_x, normalized_y))
                    self.floors.add(Ground(normalized_x, normalized_y))
                elif cell == 3:
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                    self.hearth.add(Hearth(self.player, normalized_x, normalized_y))
                elif cell == 4:
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                    self.floors.add(Floor(normalized_x, normalized_y))
                    self.towers.add(Tower('arrow', normalized_x, normalized_y))
                elif cell == 5:
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                    self.floors.add(Floor(normalized_x, normalized_y))
                    self.towers.add(Tower('wizard', normalized_x, normalized_y))
                elif cell == 6:
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                    self.floors.add(Floor(normalized_x, normalized_y))
                    self.towers.add(Tower('poison', normalized_x, normalized_y))

        self.all_sprites.add(
            self.ground_tiles,
            self.floors,
            self.monsters,
            self.towers,
            self.hearth
        )

    def _set_map_height_width(self):
        print("map size prints before", len(self.level_map), len(self.level_map[0]))
        print(self.level_map)
        print(len(self.level_map))
        print(type(self.level_map))
        self.map_size['height'] = len(self.level_map)
        self.map_size['width'] = len(self.level_map[0])
        print("map size prints after", self.map_size['height'], self.map_size['width'])

    def update(self, current_time):
        self._spawn_monsters(current_time)
        self._create_hover_effect()

        for hearth in self.hearth:
            hearth.collision(self.monsters)

        for monster in self.monsters:
            if monster.should_move(current_time):
                monster.move(current_time)
            monster.update_status(current_time)

        for projectile in self.projectiles:
            projectile_hit = projectile.update()
            if projectile_hit is True:
                projectile.resolve_hit(current_time, self.player)

        for tower in self.towers:
            if tower.should_shoot(current_time):
                tower.shoot_nearest_monster(self.monsters, self.projectiles, current_time)
            if tower.selected:
                tower.draw_range_circle(self.display)

        for outline in self.outlines:
            outline.update_position(self.outlines, self.cell_size)

    def place_tower(self, mouse_position, tower_type):
        # new mouse position tests.
        cell_x = mouse_position[0] // 64
        cell_y = mouse_position[1] // 64
        if mouse_position[0] > 768:
            return False
        
        cell_content = self.return_cell_content(cell_y, cell_x)
        if cell_content != 1:
            return "Can't build here"

        if not self.player.buy(stats.tower_types[tower_type]['cost']):
            return 'Not enough gold'

        new_tower = Tower(tower_type, cell_x * self.cell_size, cell_y * self.cell_size)
        if new_tower.type == 'arrow':
            self.level_map[cell_y][cell_x] = 4
        elif new_tower.type == 'wizard':
            self.level_map[cell_y][cell_x] = 5
        elif new_tower.type == 'poison':
            self.level_map[cell_y][cell_x] = 6

        self.towers.add(new_tower)
        self.all_sprites.add(new_tower)
        return 'Tower built successfully'

    def select_tower(self, mouse_position):
        for tower in self.towers:
            tower_click = tower.check_for_input(mouse_position)
            if tower_click:
                self.selected_tower['active'] = True
                self.selected_tower['tower'] = tower

    def deselect_all_towers(self):
        self.selected_tower['active'] = False
        for tower in self.towers:
            tower.deselect_tower()
    
    def sell_tower(self, mouse_position):
        for tower in self.towers:
            tower_click = tower.check_for_input(mouse_position)
            if tower_click:
                self.player.increase_gold(tower.tower_types[tower.type]['sell_value'])
                tower.delete()
                return 'Tower sold successfully'
        return False

    def _create_hover_effect(self):
        mouse_position = pygame.mouse.get_pos()
        cell_x = mouse_position[0] // 64
        cell_y = mouse_position[1] // 64

        hover = HoverOutline(cell_x * self.cell_size, cell_y * self.cell_size)
        self.outlines.add(hover)

    # Called in map.update()
    def _spawn_monsters(self, current_time):
        if self.controller.should_spawn_monster(current_time):
            new_monster = Monster(self.controller.get_next_monster_type(), -20, 0)
            self.monsters.add(new_monster)
            self.all_sprites.add(self.monsters)
            print("monster spawned")
            self.controller.set_previous_spawn_time(current_time)
    
    def get_level_map(self):
        return self.level_map

    def reset_map_sprites(self):
        for monster in self.monsters:
            monster.delete()
        for projectile in self.projectiles:
            projectile.delete()
    
    def reset_map(self, clear_map):
        self.level_map = clear_map
        for tower in self.towers:
            tower.delete()
        self._initialize_sprites(self.level_map)
    
    def return_cell_content(self, wanted_y, wanted_x):
        for y_cell in range(self.map_size['height']):
            for x_cell in range(self.map_size['width']):
                if y_cell == wanted_y and x_cell == wanted_x:
                    return self.level_map[y_cell][x_cell]
        return False
