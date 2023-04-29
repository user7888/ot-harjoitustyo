import pygame
import math
import os
dirname = os.path.dirname(__file__)

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed, damage, target):
        super().__init__()
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        # Target is a monster sprite
        self.target = target
        self.damage = 10

        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "projectile.png")
        )
        self.image_scaled = pygame.transform.scale(self.image, (64, 64))
        self.image = self.image_scaled

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
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
            return True
        
        return False
    
    def damage_target(self):
        self.target.hitpoints -= self.damage
        if self.target.hitpoints <= 0:
            self.target.delete()
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def delete(self):
        self.kill()
