import pygame
import math
import os
from utils.stats import projectile_types
dirname = os.path.dirname(__file__)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, type, x, y, target_x, target_y, speed, damage, target, monsters):
        super().__init__()
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.types = projectile_types
        self.type = type
        self.target = target
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", f'{type}_projectile.png')
        )
        self.image_scaled = pygame.transform.scale(self.image, (64, 64))
        self.image = self.image_scaled
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.aoe_area = 50
        self.all_monsters = monsters

    
    #           DISCLAIMER:
    #
    # This function was written by ChatGPT.
    def update(self):
        # Check if projectile is
        # outiside game map
        if self.rect.x >= 720:
            self.delete()
            return
        # Calculate the direction towards the target
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        dist = math.sqrt(dx**2 + dy**2)
        dx /= dist
        dy /= dist
        
        # Move towards the target
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        
        # Check if the projectile has reached the target
        if abs(self.rect.x - self.target_x) < self.speed and abs(self.rect.y - self.target_y) < self.speed:
            if self.types[self.type]['effect']['area'] > 0:
                #self.area_of_effect()
                #self.delete()
                pass
            else:
                #self.target.damage(self.types[self.type]['damage'], self.types[self.type]['effect'])
                #self.delete()
                pass
            return True
        
        return False

    def resolve_hit(self, current_time, player):
        # Check for area of effect
        if self.types[self.type]['effect']['area'] > 0:
            self._area_of_effect(current_time, player)
        else:
            self.target.damage(self.types[self.type]['damage'], self.types[self.type]['effect'], current_time, player)
        self.delete()

    def _area_of_effect(self, current_time, player):
        for monster in self.all_monsters:
            distance = math.hypot(self.rect.x - monster.rect.x, self.rect.y - monster.rect.y)
            if distance < self.types[self.type]['effect']['area']:
                monster.damage(self.types[self.type]['damage'], self.types[self.type]['effect'], current_time, player)
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def delete(self):
        self.kill()
