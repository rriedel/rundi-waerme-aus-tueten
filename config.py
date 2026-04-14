from dataclasses import dataclass
import argparse
from output import OUTPUT_BASENAME, OUTPUT_DIR

DEFAULT_INTERVAL = 15
"""time in seconds between measurements"""


@dataclass
class Configuration:

    interval: int
    output_basename: str
    dryrun: bool
    max_iterations: int
    data_dir: str

    def __init__(self):
        self._parse_command_line()
        print(f"measurement interval (seconds): {self.interval}")
        print(f"output filename base: {self.output_basename}")
        print(f"output directory: {self.data_dir}")
        print(f"dry run (no output written): {self.dryrun}")
        print(f"maximum iterations: {self.max_iterations}")

    def _parse_command_line(self):        
        parser = argparse.ArgumentParser(
            description="measure temperature from DS18B20 sensors and write to file")
        
        parser.add_argument(
            "-i", "--interval", 
            type=int, 
            default=DEFAULT_INTERVAL,
            help=f"time in seconds between measurements, default: {DEFAULT_INTERVAL} (values below 5 make no sense)"
        )
        parser.add_argument(
            "-o", "--output", 
            type=str, 
            default=OUTPUT_BASENAME,
            help=f"output filename base (without extension), default: {OUTPUT_BASENAME}"
        )
        parser.add_argument(
            "-d", "--data-dir", 
            type=str,
            default=OUTPUT_DIR, 
            help=f"output directory, default: {OUTPUT_DIR}"
        )
        parser.add_argument(
            "--dryrun", 
            action='store_true',
            help="do not write output to file"
        )
        parser.add_argument(
            "--max-iterations", 
            type=int, 
            default=0,
            help="maximum number of iterations (default: infinite)"
        )
        
        args = parser.parse_args()
        
        self.interval = max(0, args.interval -3)  # subtract 3 seconds to account for sensor read time (which can take a while)
        self.output_basename = args.output
        self.dryrun = args.dryrun
        self.max_iterations = args.max_iterations
        self.data_dir = args.data_dir
