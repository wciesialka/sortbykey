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

    parser.add_argument("-a", "--atonality", type=positive_orzero_float, default=0.2, metavar="ATONALITY_CONFIDENCE_LIMIT",
        help="If the strength of the key is less than this, the tagger won't write key metadata. Defaults to 0.2.")

    parser.add_argument("-b", "--ametric", type=positive_orzero_float, default=0.2, metavar="BPM_CONFIDENCE_LIMIT",
        help="If the strength of the tempo is less than this, the tagger won't write tempo metadata. Defaults to 0.2.")

    return parser

def parse_args() -> argparse.Namespace:
    parser = get_argparser()
    return parser.parse_args()