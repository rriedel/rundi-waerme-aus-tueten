import argparse
import time
import locale

from sensors import Sensors
from output import OutputFile, OUTPUT_BASENAME


# set locale (used for floating point formatting)
locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')


def main(interval: int, output_basename: str, dryrun: bool, max_iterations: int):

    print(f"measurement interval (seconds): {interval}")
    print(f"output filename base: {output_basename}")
    print(f"dry run (no output written): {dryrun}")
    print(f"maximum iterations: {max_iterations}")

    # discover and store all temperature sensors found on this system
    sensors = Sensors()

    if sensors.sensors == []:
        print("no sensors found, exiting")
        return

    output = OutputFile(output_basename, sensors) if not dryrun else None

    iteration_count = 0
    while True:
        if max_iterations > 0 and iteration_count >= max_iterations:
            break

        snapshot = sensors.read_all_sensors()
        print(snapshot)
        output.append_measurements(snapshot) if output is not None else None
        time.sleep(interval)
        iteration_count += 1


DEFAULT_INTERVAL = 15
"""time in seconds between measurements"""

parser = argparse.ArgumentParser(description='Rundi und die Wärme aus Tüten')

parser.add_argument(
    '--interval',
    type=int,
    default=DEFAULT_INTERVAL,
    help='time in seconds between measurements'
)

parser.add_argument(
    '--output',
    type=str,
    default=OUTPUT_BASENAME,
    help='base filename for the output CSV file'
)

parser.add_argument(
    '--dryrun',
    type=bool,
    default=False,
    help='perform a dry run without writing to the output file'
)

parser.add_argument(
    '--max-iterations',
    type=int,
    default=0,
    help='maximum number of measurement iterations to perform (0 for infinite)'
)

args = parser.parse_args()

if __name__ == "__main__":
    main(args.interval, args.output, args.dryrun, args.max_iterations)
