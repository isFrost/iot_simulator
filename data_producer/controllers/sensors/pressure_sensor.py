from .base_sensor import BaseSensor


class PressureSensor(BaseSensor):
    def __init__(self, s_id, room, online=True, anomaly=False):
        super().__init__(s_id, room)
        self.measurement = 'Atmospheric Pressure'
        self.value_range = (990, 1020)
        self.anomaly_range = (500, 1500)
        self.unit = 'hPa'
        self.online = online
        self.anomaly = anomaly
