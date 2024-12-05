import time
from controllers.sensor_controller import SensorController


controller = SensorController()    # create sensor controller
controller.create_sensors()    # create set of sensors
while True:
    controller.run_sensors()    # read data from the sensors
    time.sleep(5)
