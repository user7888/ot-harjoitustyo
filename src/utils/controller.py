class Controller:
    def __init__(self):
        self.states = {'initialized': 'Game is initialized',
                       'main menu': 'Game is in main menu',
                       'running': 'Game is running',
                       'pre wave': 'Game is in pre wave state',
                       'paused': 'Game is in pause menu',
                       'terminated': 'Game is exiting'}
        self._game_state = 'initialized'
        
        # Amount of enemies, frequency of enemies in ms.
        # Give monster damage and types here.
        self.waves = [
            [5, 1000, 2],
            [2, 1000, 2]
        ]
        self._current_wave = 0
        self._wave_progress = 0
        self.wave_completed = False
        self.previous_spawn_time = self.waves[self._current_wave][1]

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
    
    def set_state_pre_wave(self):
        self._game_state = 'pre wave'
        print("game state set >", self._game_state)

    def set_state_terminated(self):
        self._game_state = 'terminated'
        print("game state set >", self._game_state)
    
    def should_spawn_monster(self, current_time):
        # Time of previous spawn time is
        # updated in the game map module.
        if self._game_state == 'running':
            if current_time - self.previous_spawn_time >= self.waves[self._current_wave][1] and self._wave_progress < self.waves[self._current_wave][0]:
                self._wave_progress += 1
                return True
    
    def set_previous_spawn_time(self, current_time):
        self.previous_spawn_time = current_time
    
    def update_wave_state(self):
        if self._wave_progress >= self.waves[self._current_wave][0]:
            # wave_completed -> all monsters spawned
            self.wave_completed = True
    
    def update_game_state(self, monsters):
        if self._game_state == 'running' and self.wave_completed and len(monsters) == 0:
            self._game_state = 'pre wave'
            if self._current_wave+1 < len(self.waves):
                self._current_wave += 1
                self.wave_completed = False
                self._wave_progress = 0
                print("set current wave to", self._current_wave)
            print('game state >', self._game_state)
        
        if self._current_wave+1 == len(self.waves):
            print("all waves completed")
    
    def get_current_wave(self):
        return self.waves[self._current_wave]
