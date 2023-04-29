import random
import pygame
from sprites.monster import Monster
from sprites.floor import Floor
from sprites.ground import Ground
from sprites.tower import Tower
from sprites.hearth import Hearth
from sprites.hover_outline import HoverOutline
from objects.projectile import Projectile

class Map:
    def __init__(self, level_map, cell_size, display, controller, player):
        self.cell_size = cell_size
        self.level_map = level_map
        self.display = display
        self.controller = controller
        self.player = player

        self.ground_tiles = pygame.sprite.Group()
        self.floors = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.hearth = pygame.sprite.Group()

        self.outlines = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self._initialize_sprites(level_map)
        self.clicked = False
        # Selected tower rendering.
        self.selected_tower_active = False
        self.selected_tower = None

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
                    # Ground tile
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                elif cell == 1:
                    # Floor tile
                    self.floors.add(Floor(normalized_x, normalized_y))
                elif cell == 2:
                    # Monster tile
                    self.monsters.add(Monster(normalized_x, normalized_y))
                    self.floors.add(Ground(normalized_x, normalized_y))
                elif cell == 3:
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                    self.floors.add(Ground(normalized_x, normalized_y))
                    self.towers.add(Tower(normalized_x, normalized_y))
                elif cell == 4:
                    self.ground_tiles.add(Ground(normalized_x, normalized_y))
                    self.hearth.add(Hearth(self.player, normalized_x, normalized_y))

        self.all_sprites.add(
            self.ground_tiles,
            self.floors,
            self.monsters,
            self.towers,
            self.hearth
        )

    def update(self, current_time):
        self.spawn_monsters(current_time)

        for hearth in self.hearth:
            hearth.collision(self.monsters)

        for monster in self.monsters:
            # Old movement
            #if monster.should_move(current_time):
            #    self.move_monster_pixel(monster)
            #    monster.previous_move_time = current_time
            monster.set_destination()
            monster.move()
            #for tower in self.towers:
            #    tower.check_if_monster_is_in_range(monster)

        for projectile in self.projectiles:
            # update sets the new coordinates
            # for projectile sprite. Projectile
            # is drawn in renderer with sprite
            # group draw
            response = projectile.update()

            # If projectile reached target
            if response is True:
                print("test", projectile.target)
                projectile.damage_target()
                projectile.delete()
        
        for tower in self.towers:
            if tower.should_shoot(current_time):
                in_range = tower.calculate_distance_to_nearest_monster(self.monsters, self.projectiles)
                tower.time_of_previous_shooting = current_time
            if tower.selected:
                tower.draw_range_circle(self.display)


            #projectile.rect.move_ip(move_x, move_y)
            #projectile.rect.update()

    def move_monster_cell(self, dx=0, dy=0):
        # All monsters are in a pygame sprite group.
        monster_list = self.monsters.sprites()
        monster_list[0].rect.move_ip(dx, dy)

    def move_monster_pixel(self, monster):
        #print("monster was moved")
        directions = {"UP": (10, 0), "DOWN": (-10, 0),
                      "RIGHT": (0, 10), "LEFT": (0, -10)}
        direction = random.choice(list(directions.keys()))
        monster.rect.move_ip(directions[direction])

    # def move_monster_pixel_new(self, monster, destination):
    #     # if monster reaches destination, only then update
    #     # new destination for monster.

    #     current_location = monster.currrent_location()
    #     new_location = (current_location[0]+2, current_location[1]+2)
    #     final_location = current_location

    #     if new_location[0] <= monster.current_destination[0]:
    #         final_location[0] = new_location[0]
    #     if new_location[1] >= monster.current_destination[1]:
    #         final_location[1] = new_location[1]

    #     monster.rect.move_ip(final_location)

    # Causes a crash when clicking outside
    # game map
    def place_tower(self):
        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] > 768:
            return

        cell_x = mouse_position[0] // 64
        cell_y = mouse_position[1] // 64
        print("mouse click pixel", mouse_position)
        print("mouse click cell", cell_x, cell_y)

        self.level_map[cell_y][cell_x] = 3

        new_tower = Tower("green", cell_x * self.cell_size, cell_y * self.cell_size)
        self.towers.add(new_tower)
        self.all_sprites.add(new_tower)
        print("tower location:", new_tower.center)
        print("amount of towers:", len(self.towers))

        # Added to 'selected tower' so
        # that range circle can be drawn in renderer.
        #self.selected_tower = new_tower
        #self.selected_tower_active = True
    
    def set_selected_tower(self):
        for tower in self.towers:
            if tower.selected == True:
                self.selected_tower = tower
                self.selected_tower_active = True
    
    def deselect_all_towers(self):
        self.selected_tower_active = False
        for tower in self.towers:
            tower.selected = False
        
    def hover_effect(self):
        # Notes: event loops cause mouse
        # clicks to not register.
        # (fix: Move hover effect to game loop?)
        mouse_position = pygame.mouse.get_pos()
        cell_x = mouse_position[0] // 64
        cell_y = mouse_position[1] // 64

        if mouse_position[0] > 768:
            for item in self.outlines:
                item.kill()
            return

        for item in self.outlines:
            item.kill()
        hover = HoverOutline(cell_x * self.cell_size, cell_y * self.cell_size)

        self.outlines.add(hover)

    def shoot(self):
        mouse_position = pygame.mouse.get_pos()
        if mouse_position[0] > 768:
            return

        mouse_position = pygame.mouse.get_pos()

        new_projectile = Projectile(100, 100, mouse_position[0], mouse_position[1], 3, 3)

        self.projectiles.add(new_projectile)
    
    def spawn_monsters(self, current_time):
        # Get wave info
        wave_info = self.controller.get_current_wave()
        if self.controller.should_spawn_monster(current_time):
            new_monster = Monster(wave_info[2], -20, 0)
            self.monsters.add(new_monster)
            self.all_sprites.add(self.monsters)
            print("monster spawned")
            self.controller.set_previous_spawn_time(current_time)
            self.controller.update_wave_state()