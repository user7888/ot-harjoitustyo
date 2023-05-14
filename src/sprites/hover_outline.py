import os
import pygame

dirname = os.path.dirname(__file__)

class HoverOutline(pygame.sprite.Sprite):
    """A class for hover effect of the mouse cursor, displaying
    a white outline on top of the game map at cursors location.

    Attributes:
        x_coordinate: x coordinates for the sprite.
        y_coordinate: y coordinates for the sprite.
    """
    def __init__(self, x_coordinate=0, y_coordinate=0):
        """ Class constructor for creating a new hearth sprite.

        Args:
            x_coordinate: x coordinate for the sprite.
            y_coordinate: y coordinate for the sprite.
        """
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "hover_outline.png")
        )
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate
    
    def update_position(self, sprite_group, cell_size):
        """ This function is used for updating the location of
        the hover effect.

        Args:
            sprite_group: Sprite group for hover effects. Located in GameMap-class.
            cell_size: Size of a single cell in game map (64px)
        """
        mouse_position = pygame.mouse.get_pos()
        cell_x = mouse_position[0] // 64
        cell_y = mouse_position[1] // 64

        if mouse_position[0] > 768:
            for item in sprite_group:
                item.kill()
            return
        for item in sprite_group:
            item.kill()

        hover = HoverOutline(cell_x * cell_size, cell_y * cell_size)
        sprite_group.add(hover)
