import pathlib
import logging
import essentia.standard as es

SUPPORTED_FILETYPES = ("flac")

class Analyzer:

    def __init__(self):
        self.__rhythm_extractor = es.RhythmExtractor2013()

    def analyze(self, path: pathlib.Path) -> str:
        loader = es.MonoLoader(filename = str(path))
        audio = loader()
        bpm, beats, beats_confidence, _, beats_intervals = self.__rhythm_extractor(audio)
        return (bpm, beats, beats_confidence)