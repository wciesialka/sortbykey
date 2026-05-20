import argparse
import pathlib
import os
from sortbykey.cli import *
from sortbykey.analyzers import SUPPORTED_WRITE_FILETYPES

def get_argparser() -> argparse.ArgumentParser:
    
    supported_filetypes = ",".join(f".{ft}" for ft in SUPPORTED_WRITE_FILETYPES)

    parser = argparse.ArgumentParser(
        prog="trackannotate",
        description="Add key and bpm metadata to music files.",
        epilog=f"Supported filetypes are: {supported_filetypes}"
    )

    parser.add_argument('-i', '--input', required=True, type=readable_directory, metavar="INPUT_DIRECTORY",
        help="Required. Input directory for the untagged audio files.")

    num_cores = os.cpu_count() or 1
    num_workers = (num_cores - 1) if num_cores > 1 else 1
    parser.add_argument("-j", "--jobs", type=positive_nonzero_int, default=num_workers, metavar="NUM_CORES",
        help="Number of concurrent jobs to run for analyzing. Defaults to all but one core on multi-core machines, one core on single-core machines.")

    parser.add_argument("-a", "--atonality", type=float_0_to_1, default=0.5, metavar="ATONALITY_CONFIDENCE_LIMIT",
        help="If the analyzer isn't confident of any key to this percent, it will label the sample as atonal. Defaults to 0.5.")

    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()