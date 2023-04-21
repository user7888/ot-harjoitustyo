import os
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class

class Tower(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        # Set the image for sprite
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "tower.png")
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
