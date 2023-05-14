import os
import pygame

dirname = os.path.dirname(__file__)

class Hearth(pygame.sprite.Sprite):
    """Class for the Hearth Sprite. Located at the end of
    the game map path. Hearth checks for collision with
    nearby monsters and damages the player if collision
    occurs.

    Attributes:
        player: Player object.
        x_coordinate: x coordinates for the sprite.
        y_coordinate: y coordinates for the sprite.
    """
    def __init__(self, player, x_coordinate=0, y_coordinate=0):
        """ Class constructor for creating a new hearth sprite.

        Args:
            player: Player object.
            x_coordinate: x coordinate for the sprite.
            y_coordinate: y coordinate for the sprite.
        """
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "hearth.png")
        )
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.player = player
        self.rect = self.image.get_rect()
        self.rect.x = x_coordinate
        self.rect.y = y_coordinate

    def collision(self, monsters):
        """ A function used for checking if monster sprites come
        in contact with the hearth sprite. If contact occurs, 
        player is damaged.

        Args:
            monsters: Monsters sprite group from the GameMap-class.
        """
        for monster in monsters:
            if monster.rect.right in range(self.rect.left, self.rect.right):
                if monster.rect.bottom in range(self.rect.top, self.rect.bottom):
                    self.player.damage_player(monster.stats['damage'])
                    monster.delete()
