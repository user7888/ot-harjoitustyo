import os
import math
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class
class Monster(pygame.sprite.Sprite):
    def __init__(self, type, x=0, y=0):
        super().__init__()
        self.monster_types = {"normal": {"damage": 2, "movement_speed": 1.3, "hitpoints": 20 },
                             "fast": {"damage": 2, "movement_speed": 2, "hitpoints": 20 },
                             "big": {"damage": 2, "movement_speed": 1, "hitpoints": 20 }}
        self.type = self.monster_types[type]
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", f'monster_{type}.png')
        )
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.center = ((self.rect.left+self.rect.right)/2, 
                       (self.rect.top+self.rect.bottom)/2 )
        # Movement
        self.set_destination_reached_x = False
        self.set_destination_reached_y = False
        self.current_waypoint = 1
        self.current_destination = (0, 0)
        self.neg_y = False
        self.neg_x = False
    
    def move(self):
        self._check_destination_reached()
        negative_x = False
        negative_y = False

        if self.current_destination[0] < self.rect.x:
            negative_x = True
        if self.current_destination[1] < self.rect.y:
            negative_y = True

        if abs(self.rect.x - self.current_destination[0]) > 0:
            if not negative_x:
                self.rect.x += self.type['movement_speed']
            else:
                self.rect.x -= self.type['movement_speed']

        if abs(self.rect.y - self.current_destination[1]) > 0:
            if not negative_y:
                self.rect.y += self.type['movement_speed']
            else:
                self.rect.y -= self.type['movement_speed']
    
    def _check_destination_reached(self):
        waypoints = {1: (6, 510),
                     2: (190, 510),
                     3: (196, 60),
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


        if not self.neg_x and self.rect.x >= waypoints[self.current_waypoint][0]:
            self.set_destination_reached_x = True
        elif self.neg_x and self.rect.x <= waypoints[self.current_waypoint][0]:
            self.set_destination_reached_x = True
        
        if not self.neg_y and self.rect.y >= waypoints[self.current_waypoint][1]:
            self.set_destination_reached_y = True
        elif self.neg_y and self.rect.y <= waypoints[self.current_waypoint][1]:
            self.set_destination_reached_y = True
        
        if self.set_destination_reached_x == True and self.set_destination_reached_y == True:
            self._update_destination(waypoints)
    
    def _update_destination(self, waypoints):
        if self.set_destination_reached_x == True and self.set_destination_reached_y == True:
            if self.current_waypoint <= 11:
                self.current_waypoint += 1

            self.set_destination_reached_x = False
            self.set_destination_reached_y = False
            self.current_destination = waypoints[self.current_waypoint]

            if self.current_destination[0] < self.rect.x:
                self.neg_x = True
            else:
                self.neg_x = False

            if self.current_destination[1] < self.rect.y:
                self.neg_y = True
            else:
                self.neg_y = False
    
    def current_location(self):
        return (self.rect.x, self.rect.y)

    def delete(self):
        self.kill()
