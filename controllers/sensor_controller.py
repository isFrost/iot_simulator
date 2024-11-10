from json import dumps
from kafka import KafkaProducer


class SensorController:
    def __init__(self, sensors):
        self.sensors = sensors
        self.producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda x: dumps(x).encode('utf-8')
        )

    def run_sensors(self):
        for sensor in self.sensors:
            # print(sensor.generate_value())
            self.producer.send('climate', sensor.generate_value())
