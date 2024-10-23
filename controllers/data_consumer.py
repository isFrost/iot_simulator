from kafka import KafkaConsumer
from json import loads


class DataConsumer:
    def __init__(self):
        self.consumer = KafkaConsumer(
            'measurement',
            bootstrap_servers=['kafka:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            group_id='group1',
            value_deserializer=lambda x: loads(x.decode('utf-8'))
        )

    def print_data(self):
        # Poll for messages
        msg_pack = self.consumer.poll(timeout_ms=1000)

        # Check if there are any messages
        if msg_pack:
            # Iterate over the polled messages
            for topic_partition, messages in msg_pack.items():
                # Extract the topic name from the TopicPartition object
                topic = topic_partition.topic

                # Loop through the messages for the current TopicPartition
                for message in messages:
                    # Extract the value (message data) from the ConsumerRecord
                    value = message.value

                    # Print the topic and message value
                    print(f'Topic: {topic}, Value: {value}')