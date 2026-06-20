import argparse
import pathlib
import os
from sortbykey.cli import *
from sortbykey.trackannotate.encoder import ID3v2_FILETYPES, VORBIS_COMMENTS_FILETYPES

SUPPORTED_WRITE_FILETYPES = (*ID3v2_FILETYPES, *VORBIS_COMMENTS_FILETYPES)

def get_argparser() -> argparse.ArgumentParser:
    
    supported_filetypes = ", ".join(f".{ft}" for ft in SUPPORTED_WRITE_FILETYPES)

    parser = argparse.ArgumentParser(
        prog="audiotags",
        description="Read key and bpm metadata from a music file.",
        epilog=f"Supported filetypes are: {supported_filetypes}"
    )

    parser.add_argument('input', type=readable_file, metavar="INPUT_FILE",
        help="Required. Filepath to an audio file.")

    parser.add_argument("--json", action='store_true',
        help="Output data in JSON format.")
    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()