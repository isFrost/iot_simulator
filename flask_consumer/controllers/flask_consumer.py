from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from json import loads
import requests
import time


class FlaskConsumer:
    def __init__(self):
        self.consumer = self._initialize_consumer()

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
                    group_id='flask-group',
                    value_deserializer=lambda x: loads(x.decode('utf-8'))
                )
            except NoBrokersAvailable:
                print("No brokers available. Retrying in 5 seconds...")
                time.sleep(5)


    def consume(self):
        """
        Receive messages from Kafka
        """
        msg_pack = self.consumer.poll(timeout_ms=1000)    # Poll for messages
        if msg_pack:
            # Iterate over the polled messages
            for topic_partition, messages in msg_pack.items():
                for message in messages:    # loop through the messages for the current TopicPartition
                    self.send_to_flask(payload=message.value)    # send message to Flask app

    @staticmethod
    def send_to_flask(payload):
        """
        Send messages to Flask app
        """
        try:
            r = requests.post('http://flask-app:5555/receive', json=payload)
        except requests.exceptions.RequestException as e:
            print(f'Error sending to Flask app: {e}')
