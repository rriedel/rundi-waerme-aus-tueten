import glob
from sensor import Sensor, Measurement, DEVICES_DIR, DEVICE_PATTERN
from snapshot import Snapshot


class Sensors:
    """handles discovery and reading of all temperature sensors found on this system"""

    def __init__(self):
        self.sensors = self._lookup_sensors()
        print(f"DS18B20 temparature sensors discovered: {self.sensors}")

    def _lookup_sensors(self) -> list[Sensor]:
        """find all DS18B20 temperature sensors"""
        sensor_ids = glob.glob(DEVICE_PATTERN, root_dir=DEVICES_DIR)
        sensors = [Sensor(id) for id in sensor_ids]
        return sensors

    def read_all_sensors(self) -> Snapshot:
        results: list[Measurement] = []
        for sensor in self.sensors:
            measurement = sensor.read_temperature()
            if measurement is not None:
                results.append(measurement)
        return Snapshot(results)
