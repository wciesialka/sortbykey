import argparse
import pathlib
import os

def readable_directory(p: str) -> pathlib.Path:
    path = pathlib.Path(p)
    abspath = path.expanduser().resolve()
    if abspath.exists() and abspath.is_dir() and os.access(abspath, os.R_OK):
        return abspath
    raise TypeError("Path must point to an existing and readable directory.")

def writeable_directory(p: str) -> pathlib.Path:
    path = pathlib.Path(p)
    abspath = path.expanduser().resolve()
    if abspath.exists():
        if abspath.is_dir() and os.access(abspath, os.W_OK):
            return abspath
        else:
            raise TypeError("If path exists, must point to a writable directory.")
    return abspath

def positive_nonzero_int(v: int) -> int:
    if isinstance(v, int):
        if v <= 0:
            raise ValueError("Must be a positive, non-zero integer.")
        return v
    try:
        v2 = int(v)
    except:
        raise TypeError("Must be an int")
    else:
        return positive_nonzero_int(v2)

def float_0_to_1(p: float) -> float:
    if isinstance(p, float):
        if p < 0:
            raise ValueError("Value must be (0, 1)")
        if p > 1:
            raise ValueError("Value must be (0, 1)")
        return p
    try:
        p2 = float(p)
    except:
        raise TypeError("Must be a float")
    else:
        return float_0_to_1(p2)

def get_argparser() -> argparse.ArgumentParser:
    
    parser = argparse.ArgumentParser(
        prog="sortbykey",
        description="Sort audio files by key."
    )

    parser.add_argument('-i', '--input', required=True, type=readable_directory, metavar="INPUT_DIRECTORY",
        help="Required. Input directory for the unsorted audio files.")
    parser.add_argument("-o", "--output", required=True, type=writeable_directory, metavar="OUTPUT_DIRECTORY",
        help="Required. Output directory for the sorted audio files.")

    num_cores = os.cpu_count() or 1
    num_workers = (num_cores - 1) if num_cores > 1 else 1
    parser.add_argument("-j", "--jobs", type=positive_nonzero_int, default=num_workers, metavar="NUM_CORES",
        help="Number of concurrent jobs to run for analyzing. Defaults to all but one core on multi-core machines, one core on single-core machines.")

    parser.add_argument("-a", "--atonality", type=float_0_to_1, default=0.5, metavar="ATONALITY_CONFIDENCE_LIMIT",
        help="If the analyzer isn't confident of any key to this percent, it will label the sample as atonal. Defaults to 0.5.")

    parser.add_argument("-c", "--copy", action="store_true", 
        help="Optional. Specify this flag to copy files instead of creating links to them.")

    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()