from database.database_connection import get_database_connection
from sqlite3 import IntegrityError

import json
import sqlite3


class SaveExistsError(Exception):
    pass

class SaveRepository:
    def __init__(self, connection):
        self._connection = connection

    def find_save(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM saves ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return False
        # Convert map_state to array
        map_state = json.loads(row['map_state'])
        return row['player_health'], row['player_gold'], map_state, row['wave_state']
    
    def create_save(self, map_state, wave_state, player_health, player_gold):
        print("Creating a save..")
        cursor = self._connection.cursor()
        map_state_convert = json.dumps(map_state)
        cursor.execute(
            '''INSERT INTO saves (player_health, player_gold, map_state, wave_state)
                           VALUES (?, ?, ?, ?)''',
                           (player_health, player_gold, json.dumps(map_state), wave_state)
        )
        self._connection.commit()

    
    def delete_all_saves(self):
        """Delete all saves from database.
        """

        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM saves")

        self._connection.commit()


save_repository = SaveRepository(get_database_connection())
