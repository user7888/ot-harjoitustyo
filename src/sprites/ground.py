import os
import pygame

dirname = os.path.dirname(__file__)

class Ground(pygame.sprite.Sprite):
    """Class for the ground tile of the game.
        Monster Sprites walk along the path
        marked by ground tiles.

    Attributes:
        x: x coordinates for the rect of this sprite.
        y: y coordinates for the rect of this sprite.
    """
    def __init__(self, x_coordinate=0, y_coordinate=0):
        """ Class constructor for creating a new ground Sprite.

        Args:
            x_coordinate: x coordinate for the sprite.
            y_coordinate: y coordinate for the sprite.
        """
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "ground.png")
        )
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate
