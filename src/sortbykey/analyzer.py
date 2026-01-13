import pathlib
import essentia.standard as es

SUPPORTED_FILETYPES = ("wav", "aiff", "flac", "ogg", "mp3")

key_extractor = es.KeyExtractor()

def analyze(path: pathlib.Path) -> str:
    audio = es.AudioLoader(filename = path)
    key, scale, strength = key_extractor(audio)
    return (key, scale, strength)