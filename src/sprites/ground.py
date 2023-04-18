import os
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class


class Ground(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()

        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "ground.png")
        )

        # Define the size for the object. Use
        # the dimensions of the monster image.
        self.rect = self.image.get_rect()

        # Coordinates for the object
        self.rect.x = x
        self.rect.y = y
