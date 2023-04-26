import os
import math
import pygame
from objects.projectile import Projectile

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class
class Tower(pygame.sprite.Sprite):
    def __init__(self, type, x=0, y=0):
        super().__init__()
        # Tower types. Type is given in class constructor
        # and defines the attributes and image file of 
        # the tower.
        self.tower_types = {"green": {"damage": 20, "range": 90, "attack_speed": 20 },
                             "blue": {"damage": 20, "range": 90, "attack_speed": 20 },
                             "red": {"damage": 20, "range": 90, "attack_speed": 20 }}
        self.type = self.tower_types[type]
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", f'{type}_tower.png')
        )

        # Scale the image
        self.image_scaled = pygame.transform.scale(self.image, (70, 70))
        self.image = self.image_scaled
        # Define the size for the object. Use
        # the dimensions of the monster image.
        self.rect = self.image.get_rect()
        # Coordinates for the object
        self.rect.x = x
        self.rect.y = y
        self.center = ((self.rect.left+self.rect.right)/2, 
                       (self.rect.top+self.rect.bottom)/2 )

        # Shooting related variables.
        self.range = 90
        self.time_of_previous_shooting = 0
        self.selected = False

    def tower_was_clicked(self, menu_state):
        mouse_position = pygame.mouse.get_pos()

        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            print("tower was clicked")
            return True
    
    def calculate_distance_to_nearest_monster(self, monsters, sprite_group):
        for monster in monsters:
            distance = math.hypot(self.rect.x - monster.rect.x, self.rect.y - monster.rect.y)
            if distance < self.range:
                print(distance)
                self.shoot(monster, sprite_group)
                return True
    
    def should_shoot(self, current_time):
        # Time of previous shooting is
        # updated in the game map module.
        return current_time - self.time_of_previous_shooting >= 1000
    
    def shoot(self, target, sprite_group):
        projectile = Projectile(self.rect.x, self.rect.y, target.rect.x, target.rect.y, 3, 3)
        sprite_group.add(projectile)
    
    def draw_range_circle(self, display):
        # Problem: display is needed for pygame
        # draw.
        pygame.draw.circle(display, (200, 200, 200), self.center, 100, width=3)
        pass

    def delete(self):
        self.kill()
