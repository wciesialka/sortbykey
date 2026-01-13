import pathlib
import logging
from sortbykey.analyzer import SUPPORTED_FILETYPES

def traverse(parent_path: pathlib.Path):
    for root, dirs, files in parent_path.walk():
        for filename in files:
            filepath = root / filename
            suffix = filepath.suffix.lower()[1:]
            if suffix in SUPPORTED_FILETYPES:
                yield (root, filename)
    return

def cleanup(root_path: pathlib.Path):
    dirs = [d for d in root_path.rglob('*') if d.is_dir()]
    
    # Sort by number of parts in the path
    dirs.sort(key=lambda x: len(x.parts), reverse=True)
    
    for d in dirs:
        try:
            for txt_file in d.glob('*.txt'):
                if txt_file.is_file():
                    txt_file.unlink()
            
            # 4. Now check if the directory is empty
            if not any(d.iterdir()):
                d.rmdir()
                logging.info(f"Removed empty directory: {d}")
                
        except Exception as e:
            logging.error(f"Error cleaning up {d}: {e}")