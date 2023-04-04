import pygame
import os

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
        self.movement_speed = 10

    # Check if more than 0,7s have passed since this
    # monster was last moved.
    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 700
