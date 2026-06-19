import argparse
import pathlib
import os
from sortbykey.cli import *
from sortbykey.analyzers import SUPPORTED_READ_FILETYPES

def get_argparser() -> argparse.ArgumentParser:
    
    supported_filetypes = ", ".join(f".{ft}" for ft in SUPPORTED_READ_FILETYPES)

    parser = argparse.ArgumentParser(
        prog="sortbytempo",
        description="Sort audio files by tempo.",
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

    parser.add_argument("-b", "--bpmconf", type=float_0_to_1, default=0.25, metavar="BPM_CONFIDENCE_LIMIT",
        help="If the analyzer isn't confident of the BPM to this percent, it will consider the audio file ametric. Defaults to 0.25.")

    parser.add_argument("-w", "--binwidth", type=positive_nonzero_float, default=1.0, metavar="TEMPO_BIN_WIDTH",
        help="The width of bins to sort audio files into, in beats per minute. Defaults to 1.0 bpm.")

    parser.add_argument("-c", "--copy", action="store_true", 
        help="Optional. Specify this flag to copy files instead of creating links to them.")

    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()