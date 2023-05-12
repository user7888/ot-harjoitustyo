class Save():
    def __init__(self, player_life, player_gold, map_state, wave_state):
        self._player_life = player_life
        self._player_gold = player_gold
        self._map_state = map_state
        self._wave_state = wave_state

    def get_player_life(self):
        return self._player_life

    def get_player_gold(self):
        return self._player_gold

    def map_state(self):
        return self._map_state

    def wave_state(self):
        return self._wave_state
    