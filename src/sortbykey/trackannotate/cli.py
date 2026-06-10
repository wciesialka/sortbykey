import argparse
import pathlib
import os
from sortbykey.cli import *
from sortbykey.trackannotate.encoder import ID3v2_FILETYPES, VORBIS_COMMENTS_FILETYPES

SUPPORTED_WRITE_FILETYPES = (*ID3v2_FILETYPES, *VORBIS_COMMENTS_FILETYPES)

def get_argparser() -> argparse.ArgumentParser:
    
    supported_filetypes = ", ".join(f".{ft}" for ft in SUPPORTED_WRITE_FILETYPES)

    parser = argparse.ArgumentParser(
        prog="trackannotate",
        description="Add key and bpm metadata to a music file.",
        epilog=f"Supported filetypes are: {supported_filetypes}"
    )

    parser.add_argument('input', type=readable_file, metavar="INPUT_FILE",
        help="Required. Filepath for the untagged audio file.")

    parser.add_argument("-a", "--atonality", type=float_0_to_1, default=0.5, metavar="ATONALITY_CONFIDENCE_LIMIT",
        help="If the analyzer isn't confident of any key to this percent, it won't write key metadata. Defaults to 0.5.")

    parser.add_argument("-b", "--bpmconf", type=float_0_to_1, default=0.5, metavar="BPM_CONFIDENCE_LIMIT",
        help="If the analyzer isn't confident of the BPM to this percent, it won't write BPM metadata. Defaults to 0.5.")

    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()