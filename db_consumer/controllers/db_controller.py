from datetime import datetime, timedelta
from configparser import ConfigParser
from collections import defaultdict
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from json import loads
from psycopg2 import OperationalError
import psycopg2
import time


class DBController:
    def __init__(self, config_file='./data/database.ini', section='postgresql'):
        self.buffer = []  # buffer for calculating averages
        self.last_flush_time = datetime.now()  # mark to calculate time periods
        self.db = self._load_db_config(config_file, section)    # db config
        self.consumer = self._initialize_consumer()    # kafka consumer

    @staticmethod
    def _load_db_config(config_file, section):
        """
        Load the database configuration from the config file.
        """
        parser = ConfigParser()
        parser.read(config_file)
        if parser.has_section(section):
            params = parser.items(section)
            return {param[0]: param[1] for param in params}
        else:
            raise Exception(f'Section {section} not found in the {config_file} file.')

    @staticmethod
    def _initialize_consumer():
        """
        Wait for Kafka to be available and create a Kafka consumer.
        """
        while True:
            try:
                print('Trying to connect to Kafka broker...')
                return KafkaConsumer(
                    'climate',
                    bootstrap_servers=['kafka:9092'],
                    auto_offset_reset='earliest',
                    enable_auto_commit=False,
                    group_id='db_group',
                    value_deserializer=lambda x: loads(x.decode('utf-8'))
                )
            except NoBrokersAvailable:
                print('No brokers available. Retrying in 5 seconds...')
                time.sleep(5)

    def get_db_connection(self):
        """
        Establish database connection
        """
        try:
            return psycopg2.connect(
                dbname=self.db['dbname'],
                user=self.db['user'],
                password=self.db['password'],
                host=self.db['host'],
                port=self.db['port']
            )
        except OperationalError as e:
            print(f'Failed to connect to database: {e}')

    def insert_measurements(self, room, measurement, value, unit):
        """
        Insert value to measurement table
        """
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
        finally:
            conn.close()

    def store_avg(self):
        """
        Store average values for each measurement in a room every 5 minutes
        """
        # Group messages by rooms and measurements
        grouped_messages = defaultdict(lambda: defaultdict(list))
        for message in self.buffer:
            grouped_messages[message['room']][message['measurement']].append(
                {'value': message['value'], 'unit': message['unit']})
        # Send records to database
        db_c = DBController()
        for room, message in grouped_messages.items():
            for param, values in message.items():
                db_c.insert_measurements(
                    room=room,
                    measurement=param,
                    value=round(sum([i['value'] for i in values]) / len(values), 2),    # calculate average
                    unit=values[0]['unit']
                )

    def consume(self):
        """
        Receive messages from Kafka
        """
        try:
            msg_pack = self.consumer.poll(timeout_ms=1000)  # Poll for messages
            if msg_pack:
                # Iterate over the polled messages
                for topic_partition, messages in msg_pack.items():
                    # Loop through the messages for the current TopicPartition
                    for message in messages:
                        self.buffer.append(message.value)    # store message in the buffer
                        # Every 5 minutes store average values in database
                        if self.buffer and (datetime.now() - self.last_flush_time) >= timedelta(minutes=5):
                            self.store_avg()
                            self.buffer.clear()
                            self.last_flush_time = datetime.now()
        except KeyboardInterrupt:
            print('Exiting program')
