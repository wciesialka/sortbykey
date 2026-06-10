import sortbykey.analyzers as analyzer
import sortbykey.trackannotate.encoder as encoder
from pathlib import Path
from sortbykey.wheel import WheelOfFifths

def analyze_and_annotate(input_file: Path, *, atonality: float = 0.5, bpm_confidence: float = 0.5):
    filepath = input_file.resolve()
    logging.info(f"Analyzing file \"{filepath}\" (atonality confidence limit={atonality}).")
    key_info = analyzer.analyze_key(filepath)
    bpm_info = analyzer.analyze_bpm(filepath)
    key, scale, strength = key_info
    bpm, beats, beats_confidence = bpm_info
    camelot_key = None if strength <= atonality else WheelOfFifths.camelot_notation(key, scale)
    tempo = None if beats_confidence <= bpm_confidence else bpm

    logging.info(f"Encoding key/bpm data to {filepath}...")
    encoder.write_aiff_metadata(input_file, bpm=tempo, key=camelot_key)
