from datetime import datetime
from sensor import Sensor, Measurement


OUTPUT_BASENAME = "messwerte_"
OUTPUT_EXTENSION = ".csv"
OUTPUT_DATE_PATTERN = "%Y-%m-%d_%H-%M"

# set locale (used for floating point formatting)
# locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')

class OutputFile:

    def __init__(self, sensors: list[Sensor]):
        self.sensors = sensors
        self.base_time = datetime.now()
        base_time_formatted = self.base_time.strftime(OUTPUT_DATE_PATTERN)
        self.output_filename = OUTPUT_BASENAME + base_time_formatted + OUTPUT_EXTENSION
        print(f"write results to: {self.output_filename}")

        self._write_headline()

    def append_measurements(self, measured_values: list[Measurement]):
        """create a CSV line string from the provided measurements"""
        now = datetime.now()
        values_str = [m.localized_value() for m in measured_values]
        seconds_offset = int((now - self.base_time).total_seconds())
        csv_line = str(seconds_offset) + ";" + ";".join(values_str) + "\n"
        self._append_csv(self.output_filename, csv_line)

    def _write_headline(self):
        sensor_names = [repr(sensor) for sensor in self.sensors]
        headline = "time;" + ";".join(sensor_names) + "\n"
        with open(self.output_filename, "a") as csv:
            csv.write(headline)

    def _append_csv(self, output_filename: str, line: str):
        with open(output_filename, "a") as csv:
            csv.write(line)
