import shutil
import subprocess
import json
import tempfile
import os
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
    # Create a temporary file to write into
    tmp = tempfile.NamedTemporaryFile(dir=input_path.parent, delete=False, suffix=input_path.suffix)
    tmp_path = Path(tmp.name)
    # Find filetype, raise error if not accepted
    input_extension = input_path.suffix[1:]
    if input_extension in ID3v2_FILETYPES:
        bpm_fields = ("TBPM", )
        key_fields = ("TKEY", )
    elif input_extension in VORBIS_COMMENTS_FILETYPES:
        bpm_fields = ("BPM", "TEMPO")
        key_fields = ("KEY", "INITIALKEY")
    else:
        raise UnsupportedFiletypeError(input_extension)
    # Build the command
    command = [FFMPEG, "-y", "-i", str(input_path), "-c:a", "copy", "-write_id3v2", "1"]
    if not (bpm is None):
        for bpm_field in bpm_fields:
            command.extend(("-metadata", f"{bpm_field}={round(bpm*10)/10}"))
    if not (key is None):
        for key_field in key_fields:
            command.extend(("-metadata", f"{key_field}={key}"))
    if other_metadata:
        for metadata_name, metadata_value in other_metadata.items():
            command.extend(("-metadata", f"{metadata_name}={metadata_value}"))
    command.append(str(tmp_path))
    # Run the subprocess
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,    
                               stderr=subprocess.PIPE,    
                               text=True)
    stdout, stderr = process.communicate(timeout=300)

    if process.returncode != 0 or "Error" in stderr:    
        tmp_path.unlink(missing_ok=True)    
        raise RuntimeError(f"ffmpeg failed:\n{stderr}")
    # Replace the original file with the temporary file
    if tmp_path.exists() and tmp_path.stat().st_size > 0:
        os.replace(tmp_path, input_path)
    else:    
        raise RuntimeError("Output file was not created")

def get_metadata(input_path: Path, metadata_name: str):
    """Extract metadata from an audio file."""
    file_path = input_path.resolve()
    try:
        result = subprocess.run(
            [
                'ffprobe',
                '-v', 'error',
                '-print_format', 'json',
                '-show_format',
                str(file_path)
            ],
            capture_output=True,
            text=True,
            check=True
        )
        
        data = json.loads(result.stdout)
        tags = data.get('format', {}).get('tags', {})
        
        metadata_value = tags.get(metadata_name.upper()) or tags.get(metadata_name.lower()) or tags.get(metadata_name)
        return metadata_value
    
    except subprocess.CalledProcessError as e:
        print(f"ffprobe error: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print("Failed to parse ffprobe output")
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