import pathlib
import logging
import essentia.standard as es

SUPPORTED_FILETYPES = ("wav", "aiff", "flac", "ogg", "mp3")

def camelot(key: str, scale: str) -> str:
    wheel = {
        ("Ab", "minor"): "1A",
        ("B", "major"): "1B",
        ("Eb", "minor"): "2A",
        ("F#", "major"): "2B",
        ("Bb", "minor"): "3A",
        ("C#", "major"): "3B",
        ("F", "minor"): "4A",
        ("Ab", "major"): "4B",
        ("C", "minor"): "5A",
        ("Eb", "major"): "5B",
        ("G", "minor"): "6A",
        ("Bb", "major"): "6B",
        ("D", "minor"): "7A",
        ("F", "major"): "7B",
        ("A", "minor"): "8A",
        ("C", "major"): "8B",
        ("E", "minor"): "9A",
        ("G", "major"): "9B",
        ("B", "minor"): "10A",
        ("D", "major"): "10B",
        ("F#", "minor"): "11A",
        ("A", "major"): "11B",
        ("C#", "minor"): "12A",
        ("E", "major"): "12B"
    }
    if (key, scale) in wheel:
        return wheel[(key, scale)]
    logging.warn(f"Unknown key/scale: {key} {scale}")

__ANALYZER = es.KeyExtractor()

def analyze(path: pathlib.Path) -> str:
    loader = es.MonoLoader(filename = str(path))
    audio = loader()
    key, scale, strength = __ANALYZER(audio)
    return (key, scale, strength)