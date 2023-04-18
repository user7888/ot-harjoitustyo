import pygame
import os

# Location of this file
dirname = os.path.dirname(__file__)

# Inherit the Sprite-class


class Monster(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        # Set the image for sprite
        self.image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "monster.png")
        )
        # Define the size for the object. Use
        # the dimensions of the monster image.
        self.rect = self.image.get_rect()
        # Coordinates for the object
        self.rect.x = x
        self.rect.y = y

        self.previous_move_time = 0
        self.hitpoints = 20
        self.movement_speed = 10

        # Make a function that checks if current destination
        # is reached. If it's reached, find new destination
        self.current_destination = (0, 0)

    # Check if more than 0,7s have passed since this
    # monster was last moved.
    def should_move(self, current_time):
        return current_time - self.previous_move_time >= 700

    def current_location(self):
        return (self.rect.x, self.rect.y)

    def find_new_path(self, map):
        starting_point_x = 0
        starting_point_y = 0
        cell_size = 64

        width = len(map[0])
        height = len(map)

        destination_x = 0
        destination_y = 0
        destination_cell_x = 0
        destination_cell_y = 0

        # for y in range(width):
        #    for x in range(height):

        if map[starting_point_x+1] == 1:
            destination_x = (starting_point_x+1) * cell_size
            destination_y = starting_point_y

            destination_cell_x = 0
            destination_cell_y
        elif map[starting_point_y+1] == 1:
            destination_x = starting_point_x
            destination_y = (starting_point_y+1) * cell_size

        # Form destination coordinates

        self.current_destination = (destination_x, destination_y)
