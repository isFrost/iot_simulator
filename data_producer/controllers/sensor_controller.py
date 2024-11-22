import json
from kafka import KafkaProducer
from .sensors.airflow_sensor import AirflowSensor
from .sensors.temperature_sensor import TemperatureSensor
from .sensors.humidity_sensor import HumiditySensor
from .sensors.pressure_sensor import PressureSensor
from .sensors.illuminance_sensor import IlluminanceSensor


class SensorController:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['kafka:9092'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        self.data_file = './data/sensors.json'
        self.sensors = []

    def create_sensors(self):
        """
        Create sensors from data file and store them in a list
        """
        with open(self.data_file, 'r') as f:
            sensors = json.load(f)['sensors']
            for data in sensors:
                sensor_data = (data['id'], data['room'], data['online'], data['anomaly'])
                if data['measurement'] == 'Temperature':
                    self.sensors.append(TemperatureSensor(*sensor_data))
                elif data['measurement'] == 'Humidity':
                    self.sensors.append(HumiditySensor(*sensor_data))
                elif data['measurement'] == 'Pressure':
                    self.sensors.append(PressureSensor(*sensor_data))
                elif data['measurement'] == 'Airflow':
                    self.sensors.append(AirflowSensor(*sensor_data))
                elif data['measurement'] == 'Illuminance':
                    self.sensors.append(IlluminanceSensor(*sensor_data))


    def run_sensors(self):
        """
        Generate values for each of the controller's sensors
        """
        for sensor in self.sensors:
            payload = sensor.generate_value()    # generate sensor value
            self.producer.send('climate', payload)    # send value to kafka
            print(
                f'Time: {payload["timestamp"]} '
                f'Sensor: {payload["sensor"]} '
                f'Room: {payload["room"]} '
                f'Status: {payload["status"]} '
                f'Parameter: {payload["measurement"]} '
                f'Value: {payload["value"]} {payload["unit"]}'
            )
