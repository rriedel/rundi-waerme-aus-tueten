import locale
from dataclasses import dataclass

# map known sensor (device) ID to human readable names
SENSOR_ID_MAPPING = {
    "28-000000b323aa": "yellow",
    "28-0000001": "red",
    "28-0000002": "green",
    "28-0000003": "blue",
}

DEVICES_DIR = '/sys/bus/w1/devices/'
"""device folder in rasperry pi OS"""

# print(f"device base folder: {DEVICES_DIR}")

DEVICE_PATTERN = "28*"
"""matches the device folders for DS18B20 temparature sensors
see https://www.elektronik-kompendium.de/sites/praxis/bauteil_ds18b20.htm"""


@dataclass
class Measurement:
    """represents a single measurement of a specific sensor at a specific point in time"""
    
    sensor: "Sensor"
    value: float

    def localized_value(self) -> str:
        return locale.format_string("%.3f", self.value)

@dataclass
class Sensor:
    """represents a single DS18B20 temperature sensor device found on this system"""
    
    device_id: str
    name: str | None

    def __init__(self, device_id: str):
        self.device_id = device_id
        self.name = self._get_sensor_name()

    def __str__(self) -> str:
        return f"{self.name} ({self.device_id})" if self.name else self.device_id

    def __repr__(self) -> str:
        return self.name or self.device_id
     
    def _get_sensor_name(self) -> str | None:
        """lookup human readable name for the given device id"""
        return SENSOR_ID_MAPPING.get(self.device_id) or None

    def read_temperature(self) -> Measurement | None:
        """read temperature from a temperature sensor device"""
        sensor_file = DEVICES_DIR + self.device_id + "/w1_slave"
        with open(sensor_file, 'r') as f:
            lines = f.readlines()
        if lines[0].strip()[-3:] == 'YES':
            temp_pos = lines[1].find('t=')
            if temp_pos != -1:
                temp_string = lines[1][temp_pos+2:]
                temp_value = float(temp_string) / 1000.0
                return Measurement(self, temp_value)
        return None
