from controllers.log_consumer import LogConsumer


consumer = LogConsumer()    # create logger consumer
while True:
    consumer.consume()    # receive messages from Kafka
