import os
import math
import pygame
from objects.projectile import Projectile
from utils.stats import tower_types

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class
class Tower(pygame.sprite.Sprite):
    def __init__(self, tower_type, x=0, y=0):
        super().__init__()
        # Tower types. Type is given in class constructor
        # and defines the attributes and image file of
        # the tower.
        self.tower_types = tower_types
        self.type = tower_type
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", f'{tower_type}_tower.png')
        )

        # Scale the image
        self.image_scaled = pygame.transform.scale(self.image, self.tower_types[tower_type]['size'])
        self.image = self.image_scaled
        # Define the size for the object. Use
        # the dimensions of the monster image.
        self.rect = self.image.get_rect()
        # Coordinates for the object
        self.rect.x = x
        self.rect.y = y -20
        self.center = ((self.rect.left+self.rect.right)/2,
                       (self.rect.top+self.rect.bottom)/2 )
        # Shooting related variables.
        self.range = 90
        self.time_of_previous_shooting = 0
        self.selected = False

    def check_for_input(self, mouse_position):
        print('checked for tower clik')

        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            print("tower was clicked")
            self.selected = True
            return True
        return False

    def shoot_nearest_monster(self, monsters, sprite_group, current_time):
        distances = []
        for monster in monsters:
            distance = math.hypot(self.rect.x - monster.rect.x, self.rect.y - monster.rect.y)
            if distance < self.tower_types[self.type]["range"]:
                distances.append((monster, distance))
        # If no monsters in range
        if len(distances) == 0:
            return
        # Else get min distance
        nearest_monster = min(distances, key=lambda t: t[1])
        # Monster sprite is in tuple[0]
        self.shoot(nearest_monster[0], sprite_group, monsters)
        self.time_of_previous_shooting = current_time
    
    def should_shoot(self, current_time):
        # Time of previous shooting is
        # updated in the game map module.
        return current_time - self.time_of_previous_shooting >= self.tower_types[self.type]["attack_speed"]
    
    def shoot(self, target, sprite_group, monsters):
        print(target)
        projectile = Projectile(self.type, self.rect.x, self.rect.y, target.rect.x, target.rect.y, 3, 3, target, monsters)
        sprite_group.add(projectile)
    
    def draw_range_circle(self, display):
        pygame.draw.circle(display, (200, 200, 200), self.center, self.tower_types[self.type]["range"], width=3)
    
    def deselect_tower(self):
        self.selected = False

    def delete(self):
        self.kill()