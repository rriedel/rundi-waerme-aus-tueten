import time
import locale

from sensors import Sensors
from output import OutputFile
from config import Configuration

# set locale (used for floating point formatting)
locale.setlocale(locale.LC_NUMERIC, 'de_DE.UTF-8')


def main(cfg: Configuration):

    # discover and store all temperature sensors found on this system
    sensors = Sensors()
    if not sensors.has_sensors():
        print("no sensors found, exiting")
        return

    output = OutputFile(cfg.output_basename, cfg.data_dir,
                        sensors) if not cfg.dryrun else None

    print("starting measurement...")
    print("press Ctrl+C to stop")
    print("----------------------------------------------------------------")

    iteration_count = 0

    while True:
        try:
            if cfg.max_iterations > 0 and iteration_count >= cfg.max_iterations:
                break

            # caution: this will block until all sensors have been read (which can take a while)
            snapshot = sensors.read_all_sensors()
            
            print(snapshot)
            output.append_measurements(
                snapshot) if output is not None else None
            
            time.sleep(cfg.interval)
            iteration_count += 1
            
        except KeyboardInterrupt:
            print("\nmeasurement stopped by user")
            break

    output.close() if output is not None else None


if __name__ == "__main__":
    main(Configuration())
