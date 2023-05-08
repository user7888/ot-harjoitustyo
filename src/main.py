import pygame
from game_map import Map
from game_loop import GameLoop
from renderer import Renderer
from clock import Clock
from event_queue import EventQueue
from utils.main_menu import MainMenu
from utils.build_menu import BuildMenu
from utils.pause_menu import PauseMenu
from utils.controller import Controller
from objects.player import Player

MAP = [[0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,],
       [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,],
       [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,],
       [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1,],
       [0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1,],
       [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 4,]]

CELL_SIZE = 64


def main():
    height = len(MAP)
    width = len(MAP[0])
    side_menu_width = 300

    display = pygame.display.set_mode((width * CELL_SIZE + side_menu_width, height * CELL_SIZE))
    pygame.display.set_caption("Tower Defense")
    pygame.font.init()


    # Form all objects.
    controller = Controller()
    player = Player()
    game_map = Map(MAP, CELL_SIZE, display, controller, player)
    event_queue = EventQueue()
    renderer = Renderer(display, game_map)
    clock = Clock()

    main_menu = MainMenu(clock, event_queue, display, controller)
    pause_menu = PauseMenu(clock, event_queue, display, controller)
    main_ui = BuildMenu(clock, event_queue, display, controller, game_map, player)

    game_loop = GameLoop(game_map,
                         clock,
                         renderer,
                         event_queue,
                         display,
                         main_menu,
                         pause_menu,
                         controller,
                         player,
                         main_ui)

    # Start game.
    pygame.init()
    game_loop.start()


if __name__ == "__main__":
    main()
