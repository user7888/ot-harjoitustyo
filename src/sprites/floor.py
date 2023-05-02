import os
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class

class Floor(pygame.sprite.Sprite):
    """Class for the floor tile of the game. 
       Towers can be built on top of floor tiles.

    Args:
        x: x coordinates for the rect of this sprite.
        y: y coordinates for the rect of this sprite.
    """
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "floor.png")
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
