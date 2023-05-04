import os
import math
import pygame
from objects.projectile import Projectile

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class
class Tower(pygame.sprite.Sprite):
    def __init__(self, tower_type, x=0, y=0):
        super().__init__()
        # Tower types. Type is given in class constructor
        # and defines the attributes and image file of 
        # the tower.
        self.tower_types = {"arrow": {"damage": 20, "range": 130, "attack_speed": 20, "size": (75, 75)},
                             "wizard": {"damage": 20, "range": 90, "attack_speed": 20, "size": (70, 70) },
                             "poison": {"damage": 20, "range": 90, "attack_speed": 20, "size": (70, 70) }}
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

    def tower_was_clicked(self):
        mouse_position = pygame.mouse.get_pos()
        print('checked for tower clik')

        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            print("tower was clicked")
            self.selected = True
            return True
        return False
    
    def calculate_distance_to_nearest_monster(self, monsters, sprite_group):
        for monster in monsters:
            distance = math.hypot(self.rect.x - monster.rect.x, self.rect.y - monster.rect.y)
            if distance < self.tower_types[self.type]["range"]:
                print(distance)
                self.shoot(monster, sprite_group)
                return True
    
    def should_shoot(self, current_time):
        # Time of previous shooting is
        # updated in the game map module.
        return current_time - self.time_of_previous_shooting >= 1000
    
    def shoot(self, target, sprite_group):
        print(target)
        projectile = Projectile(self.rect.x, self.rect.y, target.rect.x, target.rect.y, 3, 3, target)
        sprite_group.add(projectile)
    
    def draw_range_circle(self, display):
        pygame.draw.circle(display, (200, 200, 200), self.center, self.tower_types[self.type]["range"], width=3)

    def delete(self):
        self.kill()