import sortbykey.analyzers as analyzer
import sortbykey.trackannotate.encoder as encoder
import threading
import logging
from pathlib import Path
from sortbykey.wheel import WheelOfFifths

class Tagger:

    def __init__(self, input_file: Path, *, atonality: float = 0.5, bpm_confidence: float = 0.5, encode_key: bool = True, encode_bpm: bool = True):
        self.__file = input_file
        self.atonality_confidence_limit = atonality
        self.bpm_confidence_limit = bpm_confidence
        self.encode_bpm = encode_bpm
        self.encode_key = encode_key
    
    @property
    def filepath(self):
        return self.__file.resolve()

    def tag(self):
        if (not self.encode_bpm) and (not self.encode_key):
            raise RuntimeError("Must encode either bpm, key, or both. Cannot encode neither.")
        threads = []
        key_data = {"key": None, "scale": None, "strength": None}
        bpm_data = {"bpm": None, "beats": None, "strength": None}
        camelot_key = None
        tempo = None
        if self.encode_bpm:
            bpm_thread = threading.Thread(target=self.analyze_bpm, args=(bpm_data,))
            threads.append(bpm_thread)
        if self.encode_key:
            key_thread = threading.Thread(target=self.analyze_key, args=(key_data,))
            threads.append(key_thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        key = key_data["key"]
        scale = key_data["scale"]
        key_confidence = key_data["strength"]
        if not (key is None):
            camelot_key = None if key_confidence < self.atonality_confidence_limit else WheelOfFifths.camelot_notation(key, scale)
        bpm = bpm_data["bpm"]
        bpm_confidence = bpm_data["strength"]
        if not (bpm is None):
            tempo = None if bpm_confidence < self.bpm_confidence_limit else (round(bpm * 10) / 10)

        logging.info(f"Encoding metadata to {self.filepath}...")
        encoder.write_aiff_metadata(self.__file, bpm=tempo, key=camelot_key)
        logging.info(f"Wrote metadata to {self.filepath}.")
    
    def analyze_key(self, data: dict):
        logging.info(f"Analyzing key of {self.filepath}...")
        key_info = analyzer.analyze_key(self.filepath)
        key, scale, strength = key_info
        data["key"] = key
        data["scale"] = scale
        data["strength"] = strength
        logging.info(f"Analyzed key of {self.filepath}: {key} {scale} ({strength=})")

    def analyze_bpm(self, data: dict):
        logging.info(f"Analyzing bpm of {self.filepath}...")
        bpm_info = analyzer.analyze_bpm(self.filepath)
        bpm, beats, strength = bpm_info
        data["bpm"] = bpm
        data["beats"] = beats
        data["strength"] = strength
        logging.info(f"Analyzed bpm of {self.filepath}: {bpm} ({strength=})")