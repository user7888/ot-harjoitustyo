import os
import pygame

class Controller:
    def __init__(self):
        self.states = {'initialized': 'Game is initialized',
                       'main menu': 'Game is in main menu',
                       'running': 'Game is running',
                       'paused': 'Game is in pause menu',
                       'terminated': 'Game is exiting'}

        self._game_state = 'initialized'

    def get_game_state(self):
        return self._game_state
    
    def get_game_states(self):
        return self.states

    def set_state_initialized(self):
        self._game_state = 'initialized'
        print("game state set >", self._game_state)
    
    def set_state_main_menu(self):
        self._game_state = 'main menu'
        print("game state set >", self._game_state)
    
    def set_state_running(self):
        self._game_state = 'running'
        print("game state set >", self._game_state)
    
    def set_state_paused(self):
        self._game_state = 'paused'
        print("game state set >", self._game_state)
    
    def set_state_terminated(self):
        self._game_state = 'terminated'
        print("game state set >", self._game_state)
        

    
