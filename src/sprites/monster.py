import os
import math
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class


class Monster(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        # Set the image for sprite
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "monster.png")
        )
        # Define the size for the object. Use
        # the dimensions of the monster image.
        self.rect = self.image.get_rect()
        # Coordinates for the object
        self.rect.x = x
        self.rect.y = y

        self.previous_move_time = 0
        self.hitpoints = 20
        self.movement_speed = 1

        self.set_destination_reached = False
        self.current_waypoint = 8
        self.current_destination = (0, 0)

    # Check if more than 0,7s have passed since this
    # monster was last moved.
    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 700
    
    def set_destination(self):
        waypoints = {1: (5, 510),
                     2: (190, 510),
                     3: (195, 60),
                     4: (700, 60),
                     5: (700, 190),
                     6: (320, 190),
                     7: (320, 510),
                     8: (450, 510),
                     9: (450, 380),
                     10: (570, 380),
                     11: (570, 500),
                     12: (700, 500)}
        
        self.current_destination = waypoints[self.current_waypoint]

        if self.rect.x == waypoints[self.current_waypoint][0] and  self.rect.y == waypoints[self.current_waypoint][1]:
            self.set_destination_reached = True

        if self.set_destination_reached == True:
            if self.current_waypoint <= 11:
                self.current_waypoint += 1
            self.set_destination_reached = False
            self.current_destination = waypoints[self.current_waypoint]
            print("set destination to:", self.current_waypoint)
    
    def move(self):
        negative_x = False
        negative_y = False
        # negative/positive checks
        if self.current_destination[0] < self.rect.x:
            negative_x = True
        if self.current_destination[1] < self.rect.y:
            negative_y = True

        if abs(self.rect.x - self.current_destination[0]) > 0:
            if not negative_x:
                self.rect.x += self.movement_speed
            else:
                self.rect.x -= self.movement_speed

        if abs(self.rect.y - self.current_destination[1]) > 0:
            if not negative_y:
                self.rect.y += self.movement_speed
            else:
                self.rect.y -= self.movement_speed
    
    def current_location(self):
        return (self.rect.x, self.rect.y)


