from sensors.base_sensor import BaseSensor


class TemperatureSensor(BaseSensor):
    def __init__(self, s_id, room, online=True, anomaly=False):
        super().__init__(s_id, room)
        self.measurement = 'Temperature'
        self.value_range = (18.0, 26.0)
        self.anomaly_range = (-50.0, 100.0)
        self.unit = '°C'
        self.anomaly = anomaly
        self.online = online

