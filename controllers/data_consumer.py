from kafka import KafkaConsumer
from json import loads


class DataConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'measurement',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='group1',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

    def print_data(self):
        for message in self.consumer:
            print(str(message))
