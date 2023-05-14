import pygame

class Button():
    """A class used for creating the buttons used across
    the game UI's.

    Attributes:
        height: Height of the button determined by button image height.
        width: Width of the button determined by button image width.
        image: Image file for the button.
        rect: Rect for button formed based on the image.
        rect.x: x axis coordinate for the button
        rect.y: y axis coordinate for the button
    """
    def __init__(self, x, y, image):
        """ Class constructor for creating a new button object.

        Args:
            x: x axis location for the button.
            y: y axis location for the button.
            image: Image file for the button
        """
        self.height = image.get_height()
        self.width = image.get_width()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.update(x, y, self.width, self.height//2)

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y-(self.height//4)))

    def check_for_input(self, mouse_position):
        """ A function used for checking button input
        based on mouse position.

        Args:
            mouse_position: Mouse position.

        Returns:
            True if mouse position is inside the rect of this button, otherwise False is returned.
        """
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
