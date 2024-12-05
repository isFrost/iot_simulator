from datetime import datetime, timedelta
from statistics import mean
from collections import defaultdict
from kafka import KafkaConsumer
from json import loads
from controllers.db_controller import DBController
import requests


class DataConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'climate',
            bootstrap_servers=['kafka:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='group1',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
        self.buffer = []    # Buffer for calculating averages
        self.last_flush_time = datetime.now()    # Point to calculate time periods

    def consume(self):
        msg_pack = self.consumer.poll(timeout_ms=1000)    # Poll for messages
        if msg_pack:
            # Iterate over the polled messages
            for topic_partition, messages in msg_pack.items():
                topic = topic_partition.topic    # Extract the topic name from the TopicPartition object
                for message in messages:    # Loop through the messages for the current TopicPartition
                    value = message.value    # Extract the value (message data) from the ConsumerRecord
                    if value['value']:
                        self.buffer.append(value)    # Store values for calculating average values
                    print(f'Topic: {topic}, Value: {value}')    # Print the topic and message value
                    self.send_to_flask(payload=value)    # Send message to Flask app
                    if self.buffer:
                        self.store_avg()    # Send data to database

    def store_avg(self):
        if (datetime.now() - self.last_flush_time) >= timedelta(minutes=5):
            db_c = DBController()
            grouped_messages = defaultdict(lambda: defaultdict(list))
            for message in self.buffer:
                grouped_messages[message['room']][message['measurement']].append(
                    {'value': message['value'], 'unit': message['unit']})
            for room, message in grouped_messages.items():
                for param, values in message.items():
                    db_c.insert_measurements(
                        room=room,
                        measurement=param,
                        value=round(sum([i['value'] for i in values]) / len(values), 2),
                        unit=values[0]['unit']
                    )
            self.buffer.clear()
            self.last_flush_time = datetime.now()

    @staticmethod
    def send_to_flask(payload):
        try:
            r = requests.post('http://flask-app:5555/receive', json=payload)
        except requests.exceptions.RequestException as e:
            print(f'Error sending to Flask app: {e}')
