import glob
import time
import locale
from datetime import datetime
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

#print(f"device base folder: {DEVICES_DIR}")

DEVICE_PATTERN = "28*"
"""matches the device folders for DS18B20 temparature sensors
see https://www.elektronik-kompendium.de/sites/praxis/bauteil_ds18b20.htm"""

MEASUREMENT_INTERVAL = 15
"""time in seconds between measurements"""
print(f"measurement interval (seconds): {MEASUREMENT_INTERVAL}")

OUTPUT_BASENAME = "messwerte_"
OUTPUT_EXTENSION = ".csv"
OUTPUT_DATE_PATTERN = "%Y-%m-%d_%H-%M"

# set locale (used for floating point formatting)
locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')

@dataclass
class Sensor:
    device_id: str
    name: str

@dataclass
class Measurement:
    sensor: Sensor
    value: float

def get_sensor_name(device_id: str) -> str:
    """lookup human readable name for the given device id"""
    return SENSOR_ID_MAPPING.get(device_id) or device_id

def lookup_sensors() -> list[Sensor]:
    """find all DS18B20 temperature sensors"""
    sensor_ids = glob.glob(DEVICE_PATTERN, root_dir=DEVICES_DIR)
    sensors = [Sensor(id, get_sensor_name(id)) for id in sensor_ids]
    print(f"DS18B20 temparature sensors: {sensors}")
    return sensors

def read_single_sensor(sensor: Sensor) -> Measurement | None:
    """read temperature from a temperature sensor device"""
    sensor_file = DEVICES_DIR + sensor.device_id + "/w1_slave"
    with open(sensor_file, 'r') as f:
        lines = f.readlines()
    if lines[0].strip()[-3:] == 'YES':
        temp_pos = lines[1].find('t=')
        if temp_pos != -1:
            temp_string = lines[1][temp_pos+2:]
            temp_value = float(temp_string) / 1000.0
            return Measurement(sensor, temp_value)
    return None

def read_all_sensors(sensors: list[Sensor]):
    results: list[Measurement] = []
    for sensor in sensors:
        results.append(read_single_sensor(sensor))
    return results

def localized_temperature(measurement: Measurement) -> str:
    return locale.format_string("%.3f", measurement.value)

def format_measurement(measurement: Measurement) -> str:
    """printable output for a single measurement"""
    name = measurement.sensor.name
    temp = localized_temperature(measurement)
    return f"{name}={temp}"

def format_csv_line(base_time: datetime, measured_values: list[Measurement]) -> str:
    """create a CSV line string from the provided measurements"""
    now = datetime.now()
    print(f"{now}: {[format_measurement(m) for m in measured_values]}")

    values_str = [localized_temperature(m) for m in measured_values]
    seconds_offset = int((now - base_time).total_seconds())
    return str(seconds_offset) + ";" + ";".join(values_str) + "\n"

def write_headline(output_filename: str, sensors: list[Sensor]):
    sensor_names = [sensor.name for sensor in sensors]
    headline = "time;" + ";".join(sensor_names) + "\n"
    with open(output_filename, "a") as csv:
        csv.write(headline)

def append_csv(output_filename: str, line: str):
    with open(output_filename, "a") as csv:
        csv.write(line)

# list of all temperature sensors found on this system
sensors = lookup_sensors()

base_time = datetime.now()
base_time_formatted = base_time.strftime(OUTPUT_DATE_PATTERN)

output_filename = OUTPUT_BASENAME + base_time_formatted + OUTPUT_EXTENSION
print(f"write results to: {output_filename}")

write_headline(output_filename, sensors)

while True:
    results = read_all_sensors(sensors)
    csv_line = format_csv_line(base_time, results)
    append_csv(output_filename, csv_line)
    time.sleep(MEASUREMENT_INTERVAL)
