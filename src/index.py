import pygame
from game_map import Map
from game_loop import GameLoop
from renderer import Renderer
from clock import Clock
from event_queue import EventQueue
from utils.main_menu import MainMenu
from utils.pause_menu import PauseMenu

MAP = [[2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0,],
       [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1,],
       [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,]]

CELL_SIZE = 64

def main():
    height = len(MAP)
    width = len(MAP[0])

    display = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE))
    pygame.display.set_caption("Tower Defense")

    # Form all objects.
    map = Map(MAP, CELL_SIZE)
    event_queue = EventQueue()
    renderer = Renderer(display, map)
    clock = Clock()

    main_menu = MainMenu(clock, event_queue, display)
    pause_menu = PauseMenu(clock, event_queue, display)

    game_loop = GameLoop(map, 
                         clock, 
                         renderer, 
                         event_queue, 
                         display, 
                         main_menu, 
                         pause_menu)


    # Start game.
    pygame.init()
    game_loop.start()

if __name__ == "__main__":
    main()