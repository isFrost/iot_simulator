import random
from datetime import datetime


class BaseSensor:
    def __init__(self, s_id, room, online=True, anomaly=False):
        self.s_id = s_id
        self.r_id = room
        self.measurement = 'Weight'
        self.value_range = (1.0, 3.0)
        self.anomaly_range = (1000, 4000)
        self.unit = 'kg'
        self.online = online
        self.anomaly = anomaly

    def generate_value(self):
        value = None
        if self.online:
            value_range = self.anomaly_range if self.anomaly else self.value_range
            value = round(random.uniform(*value_range), 2)
        # return self.s_id, self.r_id, self.online, self.measurement, value, self.unit
        return {
            'timestamp': str(datetime.now()),
            'sensor': self.s_id,
            'room': self.r_id,
            'status': 'on' if self.online else 'off',
            'measurement': self.measurement,
            'value': value,
            'unit': self.unit
        }
