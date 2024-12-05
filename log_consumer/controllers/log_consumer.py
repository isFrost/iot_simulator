from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from json import loads
import time
import os
import fnmatch


class LogConsumer:
    def __init__(self):
        self.path = 'logs'    # folder for log files
        self.buffer = []    # buffer to store received messages
        self.consumer = self._initialize_consumer()    # Kafka consumer

    @staticmethod
    def _initialize_consumer():
        """
        Wait for Kafka to be available and create consumer
        """
        while True:
            try:
                print('Trying to connect to Kafka broker...')
                return KafkaConsumer(
                    'climate',
                    bootstrap_servers=['kafka:9092'],
                    auto_offset_reset='earliest',
                    enable_auto_commit=False,
                    group_id='log-group',
                    value_deserializer=lambda x: loads(x.decode('utf-8'))
                )
            except NoBrokersAvailable:
                print('No brokers available. Retrying in 5 seconds...')
                time.sleep(5)

    def consume(self):
        """
        Receive messages from Kafka
        """
        try:
            msg_pack: dict = self.consumer.poll(timeout_ms=1000)    # poll for kafka messages
            if msg_pack:
                # Iterate over the polled messages
                for topic_partition, messages in msg_pack.items():
                    # Iterate over the messages for the current TopicPartition
                    for message in messages:
                        self.buffer.append(message.value)    # add messages to buffer
                        if len(self.buffer) > 1999:
                            self.log_data()    # save data to log file when reaching 2000 records
                            self.buffer = []    # reset buffer
        except KeyboardInterrupt:
            self.log_data()    # save buffered data to log file on keyboard interrupt
            self.buffer = []   # reset buffer
            print('Exiting logging program')

    def log_data(self):
        """
        Store logged messages in *.txt files
        """
        file_count = len(fnmatch.filter(os.listdir(self.path), '*.txt'))    # count existing log files
        new_file = f'{self.path}/datalog-{file_count + 1}.txt'    # set name for new log file
        with open(new_file, 'w') as f:
            for message in self.buffer:
                f.write(f'{message}\n')     # iterate through buffer and write messages to file
