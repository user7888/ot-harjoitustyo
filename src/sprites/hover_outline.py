import os
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class

class HoverOutline(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        # Set the image for sprite
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "hover_outline.png")
        )
        # Define the size for the object. Use
        # the dimensions of the monster image.
        self.rect = self.image.get_rect()
        # Coordinates for the object
        self.rect.x = x
        self.rect.y = y
    
    def update_position(self, sprite_group, cell_size):
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
