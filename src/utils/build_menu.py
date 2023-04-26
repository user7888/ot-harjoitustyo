import pygame
import os
from utils.button import Button

dirname = os.path.dirname(__file__)


# Menu size 300x576
# Game map end: 768
class BuildMenu():
    def __init__(self, clock, event_queue, display, controller, game_map):
        self._clock = clock
        self._event_queue = event_queue
        self.display = display
        self.controller = controller
        self.game_map = game_map

        # Text displayed in build menu.
        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)

        # Build menu buttons.
        self.buy_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "buy_button.png"))
        self.buy_button_image = pygame.transform.scale(self.buy_button_image, (120, 85))
        self.buy_button = Button(780, 195, self.buy_button_image)

        self.sell_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "sell_button.png"))
        self.sell_button_image = pygame.transform.scale(self.sell_button_image, (120, 85))
        self.sell_button = Button(930, 195, self.sell_button_image)

        self.build_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "build_button.png"))
        self.build_button_image = pygame.transform.scale(self.build_button_image, (120, 85))
        self.build_button = Button(780, 300, self.build_button_image)

        # Build menu background image.
        self.background_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "side_menu_background.png")
        )
        self.background_image = pygame.transform.scale(self.background_image, (575, 576))

        # Menu states.
        self.states = {"building": "Side menu is in building state",
                       "selling": "Side menu is in selling state",
                       "default": "Side menu is in default state"}
        self.current_state = "default"
        self.text = "In default mode"
    
    def get_current_state(self):
        return self.current_state
    
    def handle_buy_button(self, player):
        print("buy button was pressed")
        self.current_state = "default"
        self.text = "In default mode"
        print("menu state set to", self.current_state)
        player.use_gold(20)
    
    def handle_sell_button(self, player):
        print("sell button was pressed")
        self.text = "Click on a tower to sell it"
        self.current_state = "selling"
    
    def handle_build_button(self, player):
        self.current_state = "building"
        self.text = "Click on a tile to build a tower"
        print("build button was pressed")

    def handle_tower_click(self, player):
        towers = self.game_map.towers
        if self.current_state == "building":
            self.game_map.place_tower()
        else:
            for tower in towers:
                tower.tower_was_clicked()
                if self.current_state == "selling" and tower.selected:
                    player.gold += 10
                    print("player gold +10")
                    tower.delete()
                elif self.current_state == "default":
                    self.game_map.set_selected_tower()


        #if self.current_state == "selling":
        #    player.gold += 10
        #    print("player gold +10")
        #    tower.delete()
        #elif self.current_state == "default":
        #    tower.selected = True
        #    self.game_map.set_selected_tower()

    # Render function
    def draw(self):
        text = self.font.render(self.text, True, self.green, None)
        self.display.blit(self.background_image, (768, -1))
        self.display.blit(text, (815, 80))
        self.buy_button.render(self.display)
        self.sell_button.render(self.display)
        self.build_button.render(self.display)