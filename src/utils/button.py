import pygame


class Button():
    def __init__(self, x, y, image):
        self.height = image.get_height()
        self.width = image.get_width()
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.rect.update(x, y, self.width, self.height//2)
        self.clicked = False

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y-(self.height//4)))
        #pygame.draw.rect(display, (255, 0, 0), self.rect, 1)

    def checkForInput(self, mouse_position):
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
