from sensors.base_sensor import BaseSensor


class HumiditySensor(BaseSensor):
    def __init__(self, s_id, room, online=True, anomaly=False):
        super().__init__(s_id, room)
        self.measurement = 'Humidity'
        self.value_range = (30, 60)
        self.anomaly_range = (0, 100)
        self.unit = '%'
        self.online = online
        self.anomaly = anomaly
