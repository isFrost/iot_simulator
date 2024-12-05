import psycopg2
from configparser import ConfigParser


class DBController:
    def __init__(self, config_file='./data/database.ini', section='postgresql'):
        self.parser = ConfigParser()
        self.parser.read(config_file)
        self.db = {}
        if self.parser.has_section(section):
            params = self.parser.items(section)
            self.db = {param[0]: param[1] for param in params}
        else:
            raise Exception(f'Section {section} not found in the {config_file} file.')

    def get_db_connection(self):
        # Establish database connection
        return psycopg2.connect(
            dbname=self.db['dbname'],
            user=self.db['user'],
            password=self.db['password'],
            host=self.db['host']
        )

    def insert_measurements(self, room, measurement, value, unit):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO measurements (room_id, measurement_type, average_value, unit)
                VALUES (%s, %s, %s, %s)
                """,
                (room, measurement, value, unit)
            )
            conn.commit()
        except Exception as e:
            print(f'Failed to insert new record to the database: {e}')
