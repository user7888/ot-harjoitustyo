import os
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class

class Floor(pygame.sprite.Sprite):
    """Class for the floor tile of the game. 
       Towers can be built on top of floor tiles.

    Attributes:
        x: x coordinates for the rect of this sprite.
        y: y coordinates for the rect of this sprite.
    """
    def __init__(self, x_coordinate=0, y_coordinate=0):
        """ Class constructor for creating a new floor Sprite.

        Args:
            x_coordinate: x coordinate for the sprite.
            y_coordinate: y coordinate for the sprite.
        """
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "floor.png")
        )
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate
