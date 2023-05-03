import os
import pygame

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class
class Hearth(pygame.sprite.Sprite):
    """Class for the Hearth Sprite.

    Attributes:
        x: x coordinates for the sprite.
        y: y coordinates for the sprite.
        player: Player object.
    """
    def __init__(self, player, x=0, y=0):
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "hearth.png")
        )
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.player = player

        # Define the size for the object. Use
        # the dimensions of the monster image.
        self.rect = self.image.get_rect()

        # Coordinates for the object
        self.rect.x = x
        self.rect.y = y

    def collision(self, monsters):
        for monster in monsters:
            if monster.rect.right in range(self.rect.left, self.rect.right) and monster.rect.bottom in range(self.rect.top, self.rect.bottom):
                # damage player(monster.damage)
                self.player.damage_player(monster.type['damage'])
                monster.delete()