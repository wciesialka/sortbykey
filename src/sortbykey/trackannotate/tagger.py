import sortbykey.analyzers as analyzer
import sortbykey.trackannotate.encoder as encoder
import logging
from sortbykey import fs
from sortbykey.workmanager import Worker
from sortbykey.wheel import WheelOfFifths

class Tagger(Worker):

    def __init__(self, input_dir, *, atonality=0.5):
        # Establish input/output
        self.__input_dir = input_dir
        self.atonality_confidence_limit = atonality

    @property
    def input_dir(self):
        return self.__input_dir

    def generate_priority_queue_entries(self):
        for root, filename in fs.traverse(self.input_dir, filetype_filter=analyzer.SUPPORTED_WRITE_FILETYPES):
            filepath = root / filename
            # Check if file exists in database
            # db_file = self.__cache.lookup_file_by_hash(filepath)
            # If hash doesn't exist in database, copy file over!
            # if db_file is None:
            size = filepath.stat().st_size
            yield (size, ((filepath, filename), {}))

    def perform_task(self, filepath, filename):
        relpath = filepath.relative_to(self.input_dir)
        logging.info("Analyzing %s...", relpath)
        key_info = analyzer.analyze_key(filepath)
        bpm_info = analyzer.analyze_bpm(filepath)
        logging.info(f"Analyzed: {filepath}")
        key, scale, strength = key_info
        bpm, beats, beats_confidence = bpm_info
        camelot_key = None if strength <= self.atonality_confidence_limit else WheelOfFifths.camelot_notation(key, scale)

        logging.info("Writing to %s...", relpath)
        encoder.write_aiff_metadata(filepath, bpm=bpm, key=camelot_key)
        logging.info("Wrote to %s.", relpath)

        return (key_info, bpm_info), (filepath, filename)     

    def task_callback(self, task_result):
        pass