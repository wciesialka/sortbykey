import argparse
import pathlib
import os
from sortbykey.cli import *
from sortbykey.analyzers import SUPPORTED_READ_FILETYPES

def get_argparser() -> argparse.ArgumentParser:
    
    supported_filetypes = ", ".join(f".{ft}" for ft in SUPPORTED_READ_FILETYPES)

    parser = argparse.ArgumentParser(
        prog="sortbykey",
        description="Sort audio files by key.",
        epilog=f"Supported filetypes are: {supported_filetypes}"
    )

    parser.add_argument('-i', '--input', required=True, type=readable_directory, metavar="INPUT_DIRECTORY",
        help="Required. Input directory for the unsorted audio files.")
    parser.add_argument("-o", "--output", required=True, type=writeable_directory, metavar="OUTPUT_DIRECTORY",
        help="Required. Output directory for the sorted audio files.")

    num_cores = os.cpu_count() or 1
    num_workers = (num_cores - 1) if num_cores > 1 else 1
    parser.add_argument("-j", "--jobs", type=positive_nonzero_int, default=num_workers, metavar="NUM_CORES",
        help="Number of concurrent jobs to run for analyzing. Defaults to all but one core on multi-core machines, one core on single-core machines.")

    parser.add_argument("-a", "--atonality", type=positive_orzero_float, default=0.2, metavar="ATONALITY_STRENGTH_LIMIT",
        help="If the strength of the key is below this limit, the audio file will be labeled atonal. Defaults to 0.2.")

    parser.add_argument("-c", "--copy", action="store_true", 
        help="Optional. Specify this flag to copy files instead of creating links to them.")

    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()