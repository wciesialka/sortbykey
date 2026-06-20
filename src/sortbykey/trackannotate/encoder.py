import shutil
import subprocess
import json
import tempfile
import os
import mutagen
from mutagen.id3 import TBPM, TKEY, TIT2
from pathlib import Path
from typing import Optional

FFMPEG = shutil.which("ffmpeg")
if not FFMPEG:
    raise RuntimeError("ffmpeg not found")
FFMPEG = Path(FFMPEG).resolve()

ID3v2_FILETYPES = ("aiff", "mp3", "aif")
VORBIS_COMMENTS_FILETYPES = ("flac", "ogg", "opus")

class UnsupportedFiletypeError(Exception):

    def __init__(self, filetype):
        valid_filetypes = ",".join(f'"{valid_filetype}"' for valid_filetype in (*ID3v2_FILETYPES, *VORBIS_COMMENTS_FILETYPES))
        self.message = f"Invalid filetype \"{filetype}\" is not of valid filetype ({valid_filetypes})."

def write_aiff_metadata(input_path: Path, bpm: Optional[int] = None, key: Optional[str] = None, **other_metadata):
    # Find filetype, raise error if not accepted
    input_extension = input_path.suffix[1:]
    is_id3 = False
    if input_extension in ID3v2_FILETYPES:
        bpm_fields = ("TBPM", )
        key_fields = ("TKEY", )
        is_id3 = True
    elif input_extension in VORBIS_COMMENTS_FILETYPES:
        bpm_fields = ("BPM", "TEMPO")
        key_fields = ("KEY", "INITIALKEY")
    else:
        raise UnsupportedFiletypeError(input_extension)
    # Load the file to mutagen
    filepath = input_path.resolve()
    audio_file = mutagen.File(filepath)

    if not (bpm is None):
        tempo = f"{round(bpm*10)/10}"
        if is_id3:
            audio_file["TBPM"] = TBPM(text=[tempo])  # Use the actual frame ID
        else:
            for bpm_field in bpm_fields:  # Loop only for Vorbis
                audio_file[bpm_field] = tempo

    if not (key is None):
        if is_id3:
            audio_file["TKEY"] = TKEY(text=[key])  # Use the actual frame ID
        else:
            for key_field in key_fields:  # Loop only for Vorbis
                audio_file[key_field] = key

    if other_metadata:
        for metadata_name, metadata_value in other_metadata.items():
            if is_id3:
                audio_file.tags[metadata_name] = TIT2(text=[str(metadata_value)])
            else:
                audio_file.tags[metadata_name] = str(metadata_value)
    audio_file.save()

def get_metadata(input_path: Path, metadata_name: str):
    """Extract metadata from an audio file."""
    filepath = input_path.resolve()
    audio_file = mutagen.File(filepath)
    try:
        return audio_file[metadata_name]
    except:
        return None

def get_key_metadata(input_path: Path): 
    input_extension = input_path.suffix[1:]
    if input_extension in ID3v2_FILETYPES:
        return get_metadata(input_path, "TKEY")
    elif input_extension in VORBIS_COMMENTS_FILETYPES:
        return get_metadata(input_path, "KEY") or get_metadata(input_path, "INITALKEY")
    else:
        raise UnsupportedFiletypeError(input_extension)

def get_bpm_metadata(input_path: Path):
    input_extension = input_path.suffix[1:]
    if input_extension in ID3v2_FILETYPES:
        return get_metadata(input_path, "TBPM")
    elif input_extension in VORBIS_COMMENTS_FILETYPES:
        return get_metadata(input_path, "BPM") or get_metadata(input_path, "TEMPO")
    else:
        raise UnsupportedFiletypeError(input_extension)