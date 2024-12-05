from sensors.base_sensor import BaseSensor


class AirflowSensor(BaseSensor):
    def __init__(self, s_id, room, online=True, anomaly=False):
        super().__init__(s_id, room)
        self.measurement = 'Air Flow Speed'
        self.value_range = (0.1, 1.0)
        self.anomaly_range = (10.0, 20.0)
        self.unit = 'm/s'
        self.online = online
        self.anomaly = anomaly
