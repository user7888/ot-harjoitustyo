import pygame
from game_logic.game_map import GameMap
from game_logic.game_loop import GameLoop
from renderer import Renderer
from clock import Clock
from game_logic.event_queue import EventQueue
from ui.main_menu import MainMenu
from ui.main_ui import MainUI
from ui.pause_menu import PauseMenu
from ui.ending_screen import GameEndScreen
from game_logic.controller import GameStateController
from objects.player import Player
from utils import setup

def main():
    display = pygame.display.set_mode((setup.WIDTH * setup.CELL_SIZE + setup.SIDE_MENU_WIDTH,
                                       setup.HEIGHT * setup.CELL_SIZE))
    pygame.display.set_caption("Tower Defense")
    pygame.font.init()
    game_save = setup.load_save()
    controller = GameStateController(game_save.wave_state())
    player = Player(game_save.get_player_life(),
                    game_save.get_player_gold())

    game_map = GameMap(game_save.map_state(),
                   setup.CELL_SIZE,
                   display,
                   controller,
                   player)
    
    event_queue = EventQueue()
    renderer = Renderer(display, game_map)
    clock = Clock()
    main_menu = MainMenu(clock, event_queue, display, controller, game_map, player)
    pause_menu = PauseMenu(clock, event_queue, display, controller)
    end_menu = GameEndScreen(clock, event_queue, display, controller)
    main_ui = MainUI(clock, event_queue, display, controller, game_map, player)
    end_menu = GameEndScreen(clock, event_queue, display, controller)

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
