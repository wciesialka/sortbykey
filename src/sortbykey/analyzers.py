import pathlib
import logging
import essentia.standard as es

SUPPORTED_READ_FILETYPES = ("wav", "aiff", "flac", "ogg", "mp3")
SUPPORTED_WRITE_FILETYPES = ("aiff", "mp3", "aif")

__KEY_ANALYZER = es.KeyExtractor()
__BPM_ANALYZER = es.RhythmExtractor2013()

def analyze_key(path: pathlib.Path) -> str:
    loader = es.MonoLoader(filename = str(path))
    audio = loader()
    key, scale, strength = __KEY_ANALYZER(audio)
    return (key, scale, strength)

def analyze_bpm(path: pathlib.Path) -> str:
    loader = es.MonoLoader(filename = str(path))
    audio = loader()
    bpm, beats, beats_confidence, _, beats_intervals = __BPM_ANALYZER(audio)
    return (bpm, beats, beats_confidence)