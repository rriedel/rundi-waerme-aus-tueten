from datetime import datetime
from sensors import Sensors
from snapshot import Snapshot

OUTPUT_BASENAME = "messwerte_"
OUTPUT_EXTENSION = ".csv"
OUTPUT_DATE_PATTERN = "%Y-%m-%d_%H-%M"

CSV_SEPARATOR = ";"

class OutputFile:
    """handles writing measurement results to a CSV file"""

    def __init__(self, basename: str, sensors: Sensors):
        self.sensors = sensors

        self.base_time = datetime.now()
        base_time_formatted = self.base_time.strftime(OUTPUT_DATE_PATTERN)

        self.output_filename = basename + base_time_formatted + OUTPUT_EXTENSION
        print(f"write results to: {self.output_filename}")

        self._write_headline()

    def append_measurements(self, snapshot: Snapshot):
        """create a CSV line string from the provided measurements"""
        now = datetime.now()
        seconds_offset = int((now - self.base_time).total_seconds())
        values_str = [m.localized_value() for m in snapshot.measurements]

        csv_line = str(seconds_offset) + CSV_SEPARATOR + \
            CSV_SEPARATOR.join(values_str) + "\n"
        self._append_csv(self.output_filename, csv_line)

    def _write_headline(self):
        sensor_names = [repr(sensor) for sensor in self.sensors.sensors]
        headline = "time" + CSV_SEPARATOR + \
            CSV_SEPARATOR.join(sensor_names) + "\n"
        with open(self.output_filename, "a") as csv:
            csv.write(headline)

    def _append_csv(self, output_filename: str, line: str):
        with open(output_filename, "a") as csv:
            csv.write(line)
