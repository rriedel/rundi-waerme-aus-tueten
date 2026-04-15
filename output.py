from datetime import datetime
from pathlib import Path
from sensors import Sensors
from snapshot import Snapshot

OUTPUT_DIR = "data"
OUTPUT_BASENAME = "messwerte_"
OUTPUT_EXTENSION = ".csv"
OUTPUT_DATE_PATTERN = "%Y-%m-%d_%H-%M"

CSV_SEPARATOR = ";"

class OutputFile:
    """handles writing measurement results to a CSV file"""

    def __init__(self, basename: str, data_dir: str, sensors: Sensors):
        self.sensors = sensors

        self.base_time = datetime.now()
        base_time_formatted = self.base_time.strftime(OUTPUT_DATE_PATTERN)

        self.output_filename = str(Path(data_dir) / (basename + base_time_formatted + OUTPUT_EXTENSION))
        print(f"write results to: {self.output_filename}")

        self.csv_file = open(self.output_filename, "a")
        self._write_headline()

    def append_measurements(self, snapshot: Snapshot):
        """create a CSV line string from the provided measurements"""
        now = datetime.now()
        seconds_offset = int((now - self.base_time).total_seconds())
        values_str = [m.localized_value() for m in snapshot.measurements]

        csv_line = str(seconds_offset) + CSV_SEPARATOR + \
            CSV_SEPARATOR.join(values_str) + "\n"
        self._append_csv(csv_line)

    def close(self):
        """Close the output file"""
        if hasattr(self, 'csv_file') and self.csv_file:
            self.csv_file.close()

    def _write_headline(self):
        sensor_names = [repr(sensor) for sensor in self.sensors.sensors]
        headline = "time" + CSV_SEPARATOR + \
            CSV_SEPARATOR.join(sensor_names) + "\n"
        self.csv_file.write(headline)
        self.csv_file.flush()  # ensure data is written to disk
        
    def _append_csv(self, line: str):
        self.csv_file.write(line)
        self.csv_file.flush()  # ensure data is written to disk
