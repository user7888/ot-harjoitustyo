class Controller:
    def __init__(self, starting_wave):
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
        
        # Amount of enemies, frequency of enemies in ms.
        # Give monster damage and types here.

        # Types: amount of different monster types per wave.
        # Frequency: sets how frequenlty new monsters are spawned in that wave.
        self.waves = [
            {'normal': 5, 'fast':2, 'big':0, 'frequency': 500},
            {'normal': 4, 'fast':0, 'big':0, 'frequency': 1000},
            {'normal': 5, 'fast':2, 'big':0, 'frequency': 1000}
        ]
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
        # Time of previous spawn time is
        # updated in the game map module.
        self.wave_completed = True
        if self.waves[self._current_wave]['normal'] > 0:
            self.wave_completed = False
        if self.waves[self._current_wave]['fast'] > 0:
            self.wave_completed = False
        if self.waves[self._current_wave]['big'] > 0:
            self.wave_completed = False

        if self._game_state == 'running' and not self.wave_completed:
            if current_time - self.previous_spawn_time >= self.waves[self._current_wave]['frequency']:
                return True
    
    def get_next_monster_type(self):
        if self.waves[self._current_wave]['normal'] > 0:
            self.waves[self._current_wave]['normal'] -= 1
            return 'normal'
        elif self.waves[self._current_wave]['fast'] > 0:
            self.waves[self._current_wave]['fast'] -= 1
            return 'fast'
        elif self.waves[self._current_wave]['big'] > 0:
            self.waves[self._current_wave]['big'] -= 1
            return 'big'
        else:
            self.wave_completed = True
    
    def set_previous_spawn_time(self, current_time):
        self.previous_spawn_time = current_time
    
    def update_game_state(self, monsters):
        if self._game_state == 'running' and self.wave_completed and len(monsters) == 0:
            self._game_state = 'pre wave'
            # change: < to <=. Bugs?
            if self._current_wave+1 <= len(self.waves):
                self._current_wave += 1
                self.wave_completed = False
                self._wave_progress = 0
                print("set current wave to", self._current_wave)
            print('game state >', self._game_state)
    
    def get_current_wave(self):
        return self.waves[self._current_wave]

    def get_info(self):
        return self._current_wave

    def all_waves_completed(self):
        #print("current wave:", self._current_wave, "len of waves:", len(self.waves))
        if self._current_wave >= len(self.waves):
            return True
        return False

    def reset_waves(self):
        waves = [
            {'normal': 5, 'fast':2, 'big':0, 'frequency': 500},
            {'normal': 4, 'fast':0, 'big':0, 'frequency': 1000},
            {'normal': 5, 'fast':2, 'big':0, 'frequency': 1000}
        ]
        self.waves = waves
    
    def reset_current_wave(self):
        self._current_wave = 0

    