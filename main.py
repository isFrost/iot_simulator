import time

from sensors.airflow_sensor import AirflowSensor
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.pressure_sensor import PressureSensor
from sensors.illuminance_sensor import IlluminanceSensor
from controllers.sensor_controller import SensorController
from controllers.data_consumer import DataConsumer


sensors = [
    TemperatureSensor(1, 1),
    TemperatureSensor(2, 1),
    TemperatureSensor(3, 1),
    TemperatureSensor(4, 2),
    TemperatureSensor(5, 2),
    TemperatureSensor(6, 2),
    TemperatureSensor(7, 2),
    TemperatureSensor(8, 3),
    TemperatureSensor(9, 3),
    TemperatureSensor(10, 3),
    TemperatureSensor(11, 3, anomaly=True),
    HumiditySensor(12, 1),
    HumiditySensor(13, 1),
    HumiditySensor(14, 2),
    HumiditySensor(15, 2),
    HumiditySensor(16, 3),
    HumiditySensor(16, 3),
    PressureSensor(17, 1),
    PressureSensor(18, 1),
    PressureSensor(19, 2),
    PressureSensor(20, 2),
    PressureSensor(21, 3),
    PressureSensor(22, 3),
    AirflowSensor(23, 1),
    AirflowSensor(26, 2),
    AirflowSensor(25, 3),
    IlluminanceSensor(26, 1),
    IlluminanceSensor(27, 1),
    IlluminanceSensor(28, 1),
    IlluminanceSensor(29, 2),
    IlluminanceSensor(30, 2),
    IlluminanceSensor(31, 2),
    IlluminanceSensor(32, 3),
    IlluminanceSensor(33, 3),
    IlluminanceSensor(34, 3)
]

controller = SensorController(sensors)
consumer = DataConsumer()
while True:
    controller.run_sensors()
    time.sleep(3)
    consumer.consume()
