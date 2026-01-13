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

def get_argparser() -> argparse.ArgumentParser:
    
    parser = argparse.ArgumentParser(
        prog="sortbykey",
        description="Sort audio files by key."
    )

    parser.add_argument('-i', '--input', required=True, help="Input directory for the unsorted audio files.", type=readable_directory)
    parser.add_argument("-o", "--output", required=True, help="Output directory for the sorted audio files.", type=writeable_directory)

    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()