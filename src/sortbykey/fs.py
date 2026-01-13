import pathlib
from sortbykey.analyzer import SUPPORTED_FILETYPES

def traverse(parent_path: pathlib.Path):
    for root, dirs, files in parent_path.walk():
        for filename in files:
            filepath = root / name
            suffix = filepath.suffix.lower()[1:]
            if suffix in SUPPORTED_FILETYPES:
                yield (root, filename)
    return