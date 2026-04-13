import argparse
import time
import locale

from sensors import Sensors
from output import OutputFile, OUTPUT_BASENAME, OUTPUT_DIR


# set locale (used for floating point formatting)
locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')


def main(interval: int, output_basename: str, dryrun: bool, max_iterations: int, data_dir: str):

    print(f"measurement interval (seconds): {interval}")
    print(f"output filename base: {output_basename}")
    print(f"output directory: {data_dir}")
    print(f"dry run (no output written): {dryrun}")
    print(f"maximum iterations: {max_iterations}")

    # discover and store all temperature sensors found on this system
    sensors = Sensors()

    if sensors.has_sensors() == False:
        print("no sensors found, exiting")
        return

    output = OutputFile(output_basename, data_dir,
                        sensors) if not dryrun else None


    print("starting measurement...")
    print("press Ctrl+C to stop")
    print("----------------------------------------------------------------")

    iteration_count = 0
    while True:
        try: 
            if max_iterations > 0 and iteration_count >= max_iterations:
                break

            snapshot = sensors.read_all_sensors()
            print(snapshot)
            output.append_measurements(snapshot) if output is not None else None
            time.sleep(interval)
            iteration_count += 1
        except KeyboardInterrupt:
            print("\nmeasurement stopped by user")
            break

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

parser.add_argument(
    '--data-dir',
    type=str,
    default=OUTPUT_DIR,
    help='directory where the output CSV file will be saved'
)

args = parser.parse_args()

if __name__ == "__main__":
    main(args.interval, args.output, args.dryrun,
         args.max_iterations, args.data_dir)
