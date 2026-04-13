from dataclasses import dataclass
from datetime import datetime
from sensor import Sensor, Measurement


@dataclass
class Snapshot:

    timestamp: datetime
    measurements: list[Measurement]

    def __init__(self, measurements: list[Measurement]):
        self.timestamp = datetime.now()
        self.measurements = measurements

    def __str__(self) -> str:
        return f"{self.timestamp}: {[self._format(m) for m in self.measurements]}"

    def _format(self, measurement: Measurement) -> tuple[str, str]:
        """printable output for a single measurement"""
        name = repr(measurement.sensor)
        temp = measurement.localized_value()
        return (name, temp)
