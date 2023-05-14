import copy
from repositories.save_repository import save_repository
from objects.save import Save
from utils.stats import waves

class GameStateController:
    """A class used to keep track of the game state. It provides
    services for other parts of the application to alter the state, most
    importantly for the UI. The functionality needed for the wave system of 
    monsters is also located here.

    Attributes:
        states: All game states.
        game_state: Current state the game is in.
        previous_game_state: Previous state of the game.

        waves: Monster waves with type amounts and frequency in ms.
        current_wave: Ongoing wave.
        wave_progress: Amount of monsters spawned in this wave.
        wave_completed: Updated when a wave ends.
        previous_spawn_time: Used to keep track of monster spawns.
    """
    def __init__(self, starting_wave):
        """ Class constructor for creating the GameStateController.

        Args:
            starting_wave: Determines the starting wave. Used when a save is
                           loaded from the database.
        """
        self.states = {'initialized': 'Game is initialized',
                       'main menu': 'Game is in main menu',
                       'running': 'Game is running',
                       'pre wave': 'Game is in pre wave state',
                       'paused': 'Game is in pause menu',
                       'terminated': 'Game is exiting',
                       'game over': 'Game over',
                       'game won': 'Game won'}
        self._game_state = 'initialized'
        self._previous_game_state = None
        self.waves = copy.deepcopy(waves)
        self._current_wave = starting_wave
        self._wave_progress = 0
        self.wave_completed = False
        self.previous_spawn_time = self.waves[self._current_wave]['frequency']

    def get_game_state(self):
        return self._game_state

    def get_previous_game_state(self):
        return self._previous_game_state

    def get_game_states(self):
        return self.states

    def set_state_initialized(self):
        self._previous_game_state = self._game_state
        self._game_state = 'initialized'
        print("game state set >", self._game_state)

    def set_state_main_menu(self):
        self._previous_game_state = self._game_state
        self._game_state = 'main menu'
        print("game state set >", self._game_state)

    def set_state_running(self):
        self._previous_game_state = self._game_state
        self._game_state = 'running'
        print("game state set >", self._game_state)

    def set_state_paused(self):
        self._previous_game_state = self._game_state
        self._game_state = 'paused'
        print("game state set >", self._game_state)

    def set_state_pre_wave(self):
        self._previous_game_state = self._game_state
        self._game_state = 'pre wave'
        print("game state set >", self._game_state)

    def set_state_terminated(self):
        self._previous_game_state = self._game_state
        self._game_state = 'terminated'
        print("game state set >", self._game_state)

    def set_state_game_over(self):
        self._previous_game_state = self._game_state
        self._game_state = 'game over'
        print("game state set >", self._game_state)

    def set_state_game_won(self):
        self._previous_game_state = self._game_state
        self._game_state = 'game won'
        print("game state set >", self._game_state)

    def should_spawn_monster(self, current_time):
        """ A function used for the wave system to determine
        if a new monster should be spawned on the game map. Sets
        wave completed status based on amount of monsters left 
        in a wave.

        Args:
            current_time: Current game time used for spawning frequency.
        Returns:
            True if there are still monsters left in a wave, otherwise False.
        """
        self.wave_completed = True
        if self.waves[self._current_wave]['normal'] > 0:
            self.wave_completed = False
        if self.waves[self._current_wave]['fast'] > 0:
            self.wave_completed = False
        if self.waves[self._current_wave]['big'] > 0:
            self.wave_completed = False

        time_delta = current_time - self.previous_spawn_time
        if self._game_state == 'running' and not self.wave_completed:
            if time_delta >= self.waves[self._current_wave]['frequency']:
                return True
        return False

    def get_next_monster_type(self):
        """ A function used by GameMap to get the next monster type
        to spawn. Subtracts the amount of monster in the current wave.
        
        Returns:
            The type of monster to be spawned, or None if there are no monsters left in the wave.
        """
        if self.waves[self._current_wave]['normal'] > 0:
            self.waves[self._current_wave]['normal'] -= 1
            return 'normal'
        if self.waves[self._current_wave]['fast'] > 0:
            self.waves[self._current_wave]['fast'] -= 1
            return 'fast'
        if self.waves[self._current_wave]['big'] > 0:
            self.waves[self._current_wave]['big'] -= 1
            return 'big'
        self.wave_completed = True
        return None

    def set_previous_spawn_time(self, current_time):
        self.previous_spawn_time = current_time

    def update_game_state(self, monsters):
        """ A function used to update game state to 'pre wave'
        when a wave is completed and to reset wave system variables.
        """
        if self._game_state == 'running' and self.wave_completed and len(monsters) == 0:
            self._game_state = 'pre wave'
            if self._current_wave+1 <= len(self.waves):
                self._current_wave += 1
                self.wave_completed = False
                self._wave_progress = 0

    def get_current_wave(self):
        return self.waves[self._current_wave]

    def get_info(self):
        return self._current_wave

    def all_waves_completed(self):
        if self._current_wave >= len(self.waves):
            return True
        return False

    def save_game(self, map_state, wave_state, player_health, player_gold):
        """ A function used to create a save file when the game is exited.
        """
        new_save = Save(player_health, player_gold, map_state, wave_state)
        save_repository.create_save(new_save)

    def reset_waves(self):
        # waves = [
        #     {'normal': 5, 'fast':2, 'big':0, 'frequency': 500},
        #     {'normal': 4, 'fast':2, 'big':0, 'frequency': 1000},
        #     {'normal': 5, 'fast':2, 'big':0, 'frequency': 1000}
        # ]
        self.waves = copy.deepcopy(waves)

    def reset_current_wave(self):
        self._current_wave = 0
