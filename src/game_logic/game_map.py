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

class GameMap:
    """A class for the game map, responsible for forming the
    tile based game map and updating it. All Sprite objects are stored
    within this class in sprite groups. This class provides game map 
    related services for UI.

    Attributes:
        cell_size: Size of a single tile (64x64px)
        level_map: The tile map, a two dimensional array.
        display: Pygame display object.
        controller: GameStateController object.
        player: The player object.
    """
    ground_tiles = pygame.sprite.Group()
    floors = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    towers = pygame.sprite.Group()
    hearth = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    outlines = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    selected_tower = {'active': False, 'tower': None}
    map_size = {'height': None, 'width': None}

    def __init__(self, map_layout, cell_size, display, controller, player):
        """ Class constructor for creating the GameMap object. The initial state of 
        the tile map is provided in 'map_layout' as parameter to the constructor, 
        and based on it the game map is formed when '_initialize_sprites' function is called.

        Args:
            map_layout: Map layout, two dimensional array.
            cell_size: Size of individual sprite_type (64x64px).
            display: Pygame display object.
            controller: GameStateController object.
            player: The player object.
        """
        self.cell_size = cell_size
        self.level_map = map_layout
        print("early level_map", type(self.level_map))
        print("early map_layout (parameter)", map_layout)
        self.display = display
        self.controller = controller
        self.player = player

        self._set_map_height_width()
        self._initialize_sprites(self.level_map)

    def _initialize_sprites(self, level_map):
        """ This function forms the tile map. Together with
        _add_sprite function it creates all the needed sprite objects 
        and adds them to sprite groups.

        Args:
            level_map: Layout of the game map.
        """
        for y_cell in range(self.map_size['height']):
            for x_cell in range(self.map_size['width']):
                sprite_type = level_map[y_cell][x_cell]
                normalized_x = x_cell * self.cell_size
                normalized_y = y_cell * self.cell_size
                self._add_sprite(normalized_x, normalized_y, sprite_type)

        self.all_sprites.add(
            self.ground_tiles,
            self.floors,
            self.monsters,
            self.towers,
            self.hearth
        )

    def _add_sprite(self, normalized_x, normalized_y, sprite_type):
        if sprite_type == 0:
            self.ground_tiles.add(Ground(normalized_x, normalized_y))
        elif sprite_type == 1:
            self.floors.add(Floor(normalized_x, normalized_y))
        elif sprite_type == 3:
            self.ground_tiles.add(Ground(normalized_x, normalized_y))
            self.hearth.add(Hearth(self.player, normalized_x, normalized_y))
        elif sprite_type == 4:
            self.ground_tiles.add(Ground(normalized_x, normalized_y))
            self.floors.add(Floor(normalized_x, normalized_y))
            self.towers.add(Tower('arrow', normalized_x, normalized_y))
        elif sprite_type == 5:
            self.ground_tiles.add(Ground(normalized_x, normalized_y))
            self.floors.add(Floor(normalized_x, normalized_y))
            self.towers.add(Tower('wizard', normalized_x, normalized_y))
        elif sprite_type == 6:
            self.ground_tiles.add(Ground(normalized_x, normalized_y))
            self.floors.add(Floor(normalized_x, normalized_y))
            self.towers.add(Tower('poison', normalized_x, normalized_y))



    def _set_map_height_width(self):
        print("map size prints before", len(self.level_map), len(self.level_map[0]))
        print(self.level_map)
        print(len(self.level_map))
        print(type(self.level_map))
        self.map_size['height'] = len(self.level_map)
        self.map_size['width'] = len(self.level_map[0])
        print("map size prints after", self.map_size['height'], self.map_size['width'])

    def update(self, current_time):
        """ This function updates the game map and controlls all of the sprite groups.
        Sprite provided services are all called here, such as movement of monsters
        and projectiles and the shooting of towers.
        
        Args:
            level_map: Current game time.
        """
        self.spawn_monsters(current_time)
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
        """ A function for placing a tower on the game map.
        Used by the MainUI

        Args:
            mouse_position: Used for tower placement
            tower_type: Type of tower to be built
        Returns:
            False, if user clicks outside of the game map.
            "Can't build here", if the user tries to build somewhere building is not allowed.
            "Not enough gold", if the player doesn't have enough gold.
            "Tower built successfully", if the building succeeds.
        """
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
        """ Sets the 'selected tower' class variable
        when a user clicks on a tower. Used by the MainUI

        Args:
            mouse_position: Mouse position.
        """
        for tower in self.towers:
            tower_click = tower.check_for_input(mouse_position)
            if tower_click:
                self.selected_tower['active'] = True
                self.selected_tower['tower'] = tower

    def deselect_all_towers(self):
        """ Sets all towers unselected.
        """
        self.selected_tower['active'] = False
        for tower in self.towers:
            tower.deselect_tower()

    def sell_tower(self, mouse_position):
        """ A function used when the user sells a tower. It checks
        for input using mouse position and increases player gold
        if a tower is sold succesfully. Used by the MainUI.

        Args:
            mouse_position: Mouse position.

        Returns:
            "Tower sold succesfully" when selling succeeds, otherwise False.

        """
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

    def spawn_monsters(self, current_time):
        """ A function used to spawn monsters on the game map. The next
        monster type to be spawned is given by the GameStateController
        and then added to monsters sprite group.

        Args:
            current_time: Current game time.
        """
        if self.controller.should_spawn_monster(current_time):
            # new_monster = Monster(self.controller.get_next_monster_type(), -20, 0)
            # self.monsters.add(new_monster)
            # self.all_sprites.add(self.monsters)
            # print("monster spawned")
            # self.controller.set_previous_spawn_time(current_time)

            new_monster_type = self.controller.get_next_monster_type()
            if not None:
                monster = Monster(new_monster_type, -20, 0)
                self.monsters.add(monster)
                self.all_sprites.add(self.monsters)
                self.controller.set_previous_spawn_time(current_time)

    def get_level_map(self):
        return self.level_map

    def reset_map_sprites(self):
        """ A function used for soft resetting the game map. Used
        when the user exits the game but doesn't start a new game.
        """
        for monster in self.monsters:
            monster.delete()
        for projectile in self.projectiles:
            projectile.delete()

    def reset_map(self, clear_map):
        """ A function used when hard resetting the game map. Used
        when the user starts a new game.
        """
        self.level_map = clear_map
        for tower in self.towers:
            tower.delete()
        self._initialize_sprites(self.level_map)

    def return_cell_content(self, target_y, target_x):
        """ A function used finding the content of a target cell.

        Args:
            target_y: Target cell on y axis.
            target_x: Target cell on x axis.
        
        Returns:
            Integer: Numbers 1..6 based on the content of the cell.
            False: If nothing was found.
        """
        for y_cell in range(self.map_size['height']):
            for x_cell in range(self.map_size['width']):
                if y_cell == target_y and x_cell == target_x:
                    return self.level_map[y_cell][x_cell]
        return False
