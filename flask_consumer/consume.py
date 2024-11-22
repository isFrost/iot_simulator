from controllers.flask_consumer import FlaskConsumer


controller = FlaskConsumer()    # create consumer for Flask app
while True:
    controller.consume()    # consume messages from Kafka
