import pygame
from game_map import Map
from game_loop import GameLoop
from renderer import Renderer
from clock import Clock
from event_queue import EventQueue
from utils.main_menu import MainMenu
from utils.build_menu import BuildMenu
from utils.pause_menu import PauseMenu
from utils.end_menu import EndMenu
from utils.controller import Controller
from objects.player import Player
from utils import setup

def main():
    display = pygame.display.set_mode((setup.WIDTH * setup.CELL_SIZE + setup.SIDE_MENU_WIDTH,
                                       setup.HEIGHT * setup.CELL_SIZE))
    pygame.display.set_caption("Tower Defense")
    pygame.font.init()
    game_save = setup.load_save()
    controller = Controller(game_save.wave_state())
    player = Player(game_save.get_player_life(),
                    game_save.get_player_gold())

    game_map = Map(game_save.map_state(),
                   setup.CELL_SIZE,
                   display,
                   controller,
                   player)
    
    event_queue = EventQueue()
    renderer = Renderer(display, game_map)
    clock = Clock()
    main_menu = MainMenu(clock, event_queue, display, controller, game_map, player)
    pause_menu = PauseMenu(clock, event_queue, display, controller)
    end_menu = EndMenu(clock, event_queue, display, controller)
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

    pygame.init()
    game_loop.start()

if __name__ == "__main__":
    main()
