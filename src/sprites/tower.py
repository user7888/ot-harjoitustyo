import os
import math
import pygame
from objects.projectile import Projectile
from utils.stats import tower_types

dirname = os.path.dirname(__file__)

class Tower(pygame.sprite.Sprite):
    """A Class for the Tower Sprite of the game. Functionality 
    for tower shooting, checking if a tower was clicked on and
    drawing a range indicator around the tower is located in this class.

    Attributes:
        tower_type: Type of this tower (arrow, wizard, poison)
        x_coordinate: x coordinates for the sprite.
        y_coordinate: y coordinates for the sprite.
    """
    def __init__(self, tower_type, x_coordinate=0, y_coordinate=0):
        """ Class constructor for creating a new Tower Sprite. Tower
        type is given as a parameter and used to define the attributes
        of this tower. All attributes are located in utils.stats.

        Args:
            type: Type of this monster (arrow, wizard, poison)
            x_coordinate: x coordinate for the sprite.
            y_coordinate: y coordinate for the sprite.
        """
        super().__init__()
        self.tower_types = tower_types
        self.type = tower_type
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", f'{tower_type}_tower.png')
        )

        self.image_scaled = pygame.transform.scale(self.image, self.tower_types[tower_type]['size'])
        self.image = self.image_scaled
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate -20
        self.center = ((self.rect.left+self.rect.right)/2,
                       (self.rect.top+self.rect.bottom)/2 )
        self.range = 90
        self.time_of_previous_shooting = 0
        self.selected = False

    def check_for_input(self, mouse_position):
        """ A function used for selecting a tower.

        Args:
            mouse_position: Mouse position.

        Returns:
            True if mouse position is inside the rect of this tower, otherwise False is returned.
        """
        if mouse_position[0] in range(self.rect.left, self.rect.right):
            if mouse_position[1] in range(self.rect.top, self.rect.bottom):
                self.selected = True
                return True
        return False

    def shoot_nearest_monster(self, monsters, sprite_group, current_time):
        """ A function towers use to shoot the nearest monster. Distances to
        all monsters are calculated and the nearest monster is chosen as target.

        Args:
            mouse_position: Mouse position.
            sprite_group: Used for projectiles if a tower shoots.
            current_time: Used to update the time of shooting for towers.
        """
        distances = []
        for monster in monsters:
            distance = math.hypot(self.rect.x - monster.rect.x, self.rect.y - monster.rect.y)
            if distance < self.tower_types[self.type]["range"]:
                distances.append((monster, distance))
        if len(distances) == 0:
            return
        nearest_monster = min(distances, key=lambda t: t[1])
        self.shoot(nearest_monster[0], sprite_group, monsters)
        self.time_of_previous_shooting = current_time

    def should_shoot(self, current_time):
        """ A function for checking if a tower should shoot based on the
        "attack_speed" stat of the tower.

        Args:
            current_time: Current game time.
        Returns:
            True if enough time has passed, otherwise False is returned.
        """
        return current_time - self.time_of_previous_shooting >= self.tower_types[self.type]["attack_speed"]

    def shoot(self, target, sprite_group, monsters):
        """ A function used to create Projectile sprites. Projectiles
        are added to a sprite group in game map.

        Args:
            target: Target of this projectile (monster sprite).
            sprite_group: Projectiles sprite group.
            monsters: Monsters sprite group. Used if projectile has a Area of Effect.
        """
        projectile = Projectile(self.type, self.rect.x,
                                self.rect.y, target.rect.x,
                                target.rect.y, 3, 3, target, monsters)
        sprite_group.add(projectile)

    def draw_range_circle(self, display):
        """ A function used to draw a circle around a selected
        tower indicating it's range.

        Args:
            display: Pygame display object.
        """
        pygame.draw.circle(display, (200, 200, 200),
                           self.center, self.tower_types[self.type]["range"],
                           width=3)

    def deselect_tower(self):
        self.selected = False

    def delete(self):
        self.kill()
