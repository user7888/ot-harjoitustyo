import pygame
from game_map import Map
from game_loop import GameLoop
from renderer import Renderer
from clock import Clock
from event_queue import EventQueue
from utils.main_menu import MainMenu
from utils.pause_menu import PauseMenu
from utils.controller import Controller

MAP = [[2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [1, 1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0,],
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
    game_map = Map(MAP, CELL_SIZE)
    event_queue = EventQueue()
    renderer = Renderer(display, map)
    clock = Clock()

    controller = Controller()
    main_menu = MainMenu(clock, event_queue, display, controller)
    pause_menu = PauseMenu(clock, event_queue, display, controller)

    game_loop = GameLoop(game_map,
                         clock,
                         renderer,
                         event_queue,
                         display,
                         main_menu,
                         pause_menu,
                         controller)

    # Start game.
    pygame.init()
    game_loop.start()


if __name__ == "__main__":
    main()
