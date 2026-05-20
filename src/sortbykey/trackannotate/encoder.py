import shutil
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Optional

FFMPEG = shutil.which("ffmpeg")
if not FFMPEG:
    raise RuntimeError("ffmpeg not found")
FFMPEG = Path(FFMPEG).resolve()

def write_aiff_metadata(input_path: Path, bpm: Optional[int] = None, key: Optional[str] = None, **other_metadata):
    # Create a temporary file to write into
    tmp = tempfile.NamedTemporaryFile(dir=input_path.parent, delete=False, suffix=input_path.suffix)
    tmp_path = Path(tmp.name)
    # Build the command
    command = [FFMPEG, "-y", "-i", str(input_path), "-c:a", "copy", "-write_id3v2", "1"]
    if not (bpm is None):
        command.extend(("-metadata", f"TBPM={round(bpm*10)/10}"))
    if not (key is None):
        command.extend(("-metadata", f"TKEY={key}"))
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