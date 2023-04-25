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

        self.range = 200
        # Inflate rectangle size to use it
        # as range of tower.
        #self.rect = self.rect.inflate(100, 100)
    
    def tower_was_clicked(self, menu_state):
        mouse_position = pygame.mouse.get_pos()

        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            print("tower was clicked")
            return True
        
    def check_if_monster_is_in_range(self, monster):
        rect_in_range = pygame.Rect.colliderect(self.rect, monster.rect)
        if rect_in_range:
            print("collision")
    
    def delete(self):
        self.kill()
