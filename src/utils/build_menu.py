import pygame
import os
from utils.button import Button
from utils.stats import tower_types

dirname = os.path.dirname(__file__)


# Menu size 300x576
# Game map end: 768
class BuildMenu():
    def __init__(self, clock, event_queue, display, controller, game_map, player):
        self._clock = clock
        self._event_queue = event_queue
        self.display = display
        self.controller = controller
        self.game_map = game_map
        self.player = player
        self.tower_types = tower_types

        # Text displayed in build menu.
        self.font = pygame.font.Font("freesansbold.ttf", 14)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 128)

        # Build menu buttons.
        self.default_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "default_button2.png"))
        self.default_button_image = pygame.transform.scale(self.default_button_image, (120, 120))
        self.default_button = Button(790, 230, self.default_button_image)

        self.sell_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "sell_button2.png"))
        self.sell_button_image = pygame.transform.scale(self.sell_button_image, (120, 120))
        self.sell_button = Button(925, 230, self.sell_button_image)

        self.build_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "build_button2.png"))
        self.build_button_image = pygame.transform.scale(self.build_button_image, (120, 120))
        self.build_button = Button(790, 320, self.build_button_image)

        self.start_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "start_button2.png"))
        self.start_button_image = pygame.transform.scale(self.start_button_image, (120, 120))
        self.start_button = Button(925, 320, self.start_button_image)

        self.arrow_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "arrow_button2.png"))
        self.arrow_button_image = pygame.transform.scale(self.arrow_button_image, (120, 120))
        self.arrow_button = Button(925, 250, self.arrow_button_image)

        self.wizard_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "wizard_button2.png"))
        self.wizard_button_image = pygame.transform.scale(self.wizard_button_image, (120, 120))
        self.wizard_button = Button(925, 320, self.wizard_button_image)

        self.poison_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "poison_button2.png"))
        self.poison_button_image = pygame.transform.scale(self.poison_button_image, (120, 120))
        self.poison_button = Button(925, 390, self.poison_button_image)

        self.back_button_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "back_button2.png"))
        self.back_button_image = pygame.transform.scale(self.back_button_image, (120, 120))
        self.back_button = Button(790, 250, self.back_button_image)

        # Build menu background image.
        self.background_image = pygame.image.load(
            os.path.join(dirname, "..", "assets", "side_menu_background.png")
        )
        self.background_image = pygame.transform.scale(self.background_image, (575, 576))

        # Menu states.
        self.states = {"building": "Building a tower",
                       "selling": "Selling a tower",
                       "default": "In default mode",
                       "select": "Selecting a tower"}

        self.current_state = "default"
        self.chosen_tower = None
        self.desc = "In default mode"
        self.hint = None
        self.text = None

        self.player_gold = 100
        self.player_health = 100

    def get_current_state(self):
        return self.current_state

    def handle_default_button(self, player):
        print("default button was pressed")
        self.current_state = "default"
        self.desc = "In default mode"
        print("menu state set to", self.current_state)

    def handle_sell_button(self):
        print("sell button was pressed")
        self.desc = "Click on a tower to sell it"
        self.current_state = "selling"

    def handle_build_button(self):
        self.current_state = "select"
        self.desc = "Select a tower to build"
        print("build button was pressed")

    def handle_start_button(self):
        self.current_state = "default"
        self.controller.set_state_running()
        print("start button was pressed")

    def handle_arrow_button(self):
        print('arrow button was pressed')
        self.current_state = "building"
        self.chosen_tower = "arrow"
        self.desc = "Arrow tower selected"
        self.hint = "Click on a tile to build a tower"
        self.text = f"Tower cost {self.tower_types['arrow']['cost']} "

    def handle_wizard_button(self):
        print('wizard button was pressed')
        self.current_state = "building"
        self.chosen_tower = "wizard"
        self.desc = "Wizard tower selected"
        self.hint = "Click on a tile to build a tower"
        self.text = f"Tower cost {self.tower_types['wizard']['cost']} "

    def handle_poison_button(self):
        print('poison button was pressed')
        self.current_state = "building"
        self.chosen_tower = "poison"
        self.desc = "Poison tower selected"
        self.hint = "Click on a tile to build a tower"
        self.text = f"Tower cost {self.tower_types['poison']['cost']} "
    
    def handle_back_button(self):
        self._back_to_default('')
    
    def _back_to_default(self, message):
        self.current_state = 'default'
        self.desc = message

    def _back_to_state(self, state, message):
        self.current_state = state
        self.desc = message
 
    def handle_game_map_click(self, mouse_position, player):
        if self.current_state == 'building':
            response = self.game_map.place_tower(mouse_position, self.chosen_tower)
            if response  == 'Tower built successfully':
                self._back_to_state('default', response)
                return
            if response == 'Not enough gold':
                self._back_to_state('default', response)
            if response == "Can't build here":
                self._back_to_state('building', response)

        if self.current_state == 'default':
            self.game_map.select_tower(mouse_position)

        if self.current_state == 'selling':
            response = self.game_map.sell_tower(mouse_position)
            if response:
                self._back_to_default(response)

    # Render function
    def draw(self):
        # rendering based on states causes bugs
        if self.current_state == 'default' or self.current_state == 'selling':
            text = self.font.render(self.desc, True, self.green, None)
            self.display.blit(self.background_image, (768, -1))
            self.display.blit(text, (815, 80))
            self.default_button.render(self.display)
            self.sell_button.render(self.display)
            self.build_button.render(self.display)
            self.start_button.render(self.display)

            # Info text
            gold = self.font.render(f'Gold: {str(self.player.current_gold())}',
                                      True, self.green, None)
            health = self.font.render(f'Health: {str(self.player.current_health())}',
                                      True, self.green, None)
            self.display.blit(gold, (795, 15))
            self.display.blit(health, (960, 15))


        elif self.current_state == 'building':
            text = self.font.render(self.desc, True, self.green, None)
            self.display.blit(self.background_image, (768, -1))
            self.display.blit(text, (815, 80))
            self.arrow_button.render(self.display)
            self.wizard_button.render(self.display)
            self.poison_button.render(self.display)
            self.back_button.render(self.display)

            # Info text
            gold = self.font.render(f'Gold: {str(self.player.current_gold())}',
                                      True, self.green, None)
            health = self.font.render(f'Health: {str(self.player.current_health())}',
                                      True, self.green, None)
            tower_info = self.font.render(f"Cost of this tower is {self.tower_types[self.chosen_tower]['cost']} gold",
                                      True, self.green, None)
            self.display.blit(gold, (795, 15))
            self.display.blit(health, (960, 15))
            self.display.blit(tower_info, (815, 135))

        
        elif self.current_state == 'select':
            text = self.font.render(self.desc, True, self.green, None)
            self.display.blit(self.background_image, (768, -1))
            self.display.blit(text, (815, 80))
            self.arrow_button.render(self.display)
            self.wizard_button.render(self.display)
            self.poison_button.render(self.display)
            self.back_button.render(self.display)

            # Info text
            gold = self.font.render(f'Gold: {str(self.player.current_gold())}',
                                      True, self.green, None)
            health = self.font.render(f'Health: {str(self.player.current_health())}',
                                      True, self.green, None)
            self.display.blit(gold, (795, 15))
            self.display.blit(health, (960, 15))

    # 1. check for inputs.
    # 2. handle button click
    # 3. call for actual function
    def check_for_inputs(self, mouse_position, player):
        # selling state and selling button can cause bugs
        if self.current_state == 'default':
            if self.default_button.check_for_input(mouse_position):
                self.handle_default_button(player)
            elif self.sell_button.check_for_input(mouse_position):
                self.handle_sell_button()
            elif self.build_button.check_for_input(mouse_position):
                self.handle_build_button()
            elif self.start_button.check_for_input(mouse_position):
                self.handle_start_button()
            return
        
        if self.current_state == 'selling':
            if self.default_button.check_for_input(mouse_position):
                self.handle_default_button(player)
            elif self.sell_button.check_for_input(mouse_position):
                self.handle_sell_button()
            elif self.build_button.check_for_input(mouse_position):
                self.handle_build_button()
            elif self.start_button.check_for_input(mouse_position):
                self.handle_start_button()
            return

        if self.current_state == 'select' or self.current_state == 'building':
            if self.arrow_button.check_for_input(mouse_position):
                self.handle_arrow_button()
            elif self.wizard_button.check_for_input(mouse_position):
                self.handle_wizard_button()
            elif self.poison_button.check_for_input(mouse_position):
                self.handle_poison_button()
            elif self.back_button.check_for_input(mouse_position):
                self.handle_back_button()
            return
        