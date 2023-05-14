from database_connection import get_database_connection

def drop_tables(connection):
    cursor = connection.cursor()
    cursor.execute('DROP TABLE IF EXISTS saves')
    connection.commit()


def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute(
        '''CREATE TABLE saves 
                (id INTEGER PRIMARY KEY, 
                player_health INTEGER, 
                player_gold INTEGER, 
                map_state TEXT, 
                wave_state INTEGER);'''
    )
    connection.commit()


def initialize_database():
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
