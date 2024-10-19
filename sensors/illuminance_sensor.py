from sensors.base_sensor import BaseSensor


class IlluminanceSensor(BaseSensor):
    def __init__(self, s_id, room, online=True, anomaly=False):
        super().__init__(s_id, room)
        self.measurement = 'Illuminance'
        self.value_range = (500, 800)
        self.anomaly_range = (0, 5000)
        self.unit = 'lx'
        self.online = online
        self.anomaly = anomaly
