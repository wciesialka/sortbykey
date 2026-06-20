import os
import shutil
import logging
import asyncio
import sortbykey.analyzers as analyzer 
import sortbykey.trackannotate.encoder as encoder
from sortbykey import fs
from sortbykey.workmanager import Worker

def get_bin(variable, bin_width):
    integer = variable // bin_width
    if integer < 0:
        low_end = (integer - 1) * bin_width
        high_end = integer * bin_width
    else:
        low_end = integer * bin_width
        high_end = (integer + 1) * bin_width
    return (low_end, high_end)

class BPMSorter(Worker):

    def __init__(self, input_dir, output_dir, *, bpm_confidence=0.5, copy_files=False, bin_width=1.0):
        self.__input_dir = input_dir
        self.__output_dir = output_dir
        self.should_copy_files = copy_files
        self.bpm_confidence = bpm_confidence
        self.bin_width = bin_width

    @property
    def input_dir(self):
        return self.__input_dir
    
    @property
    def output_dir(self):
        return self.__output_dir

    def generate_priority_queue_entries(self):
        for root, filename in fs.traverse(self.input_dir, filetype_filter=analyzer.SUPPORTED_READ_FILETYPES):
            filepath = root / filename
            size = filepath.stat().st_size
            yield (size, ((filepath, filename), {}))

    def perform_task(self, filepath, filename):
        relpath = filepath.relative_to(self.input_dir)
        logging.info("Analyzing %s...", relpath)
        # Try to get existing key
        tempo = encoder.get_bpm_metadata(filepath)
        # If key not found, analyze and encode
        if not tempo:
            bpm, beats, beats_confidence = analyzer.analyze_bpm(filepath)
            tempo = None if beats_confidence <= self.bpm_confidence else bpm
            encoder.write_aiff_metadata(filepath, bpm=tempo)
        if tempo:
            tempo_bin = get_bin(float(tempo), self.bin_width)
            tempo_bin = f"{tempo_bin[0]} - {tempo_bin[1]}"
        else:
            tempo_bin = "ametric"
        return (tempo_bin,), (filepath, filename)     

    def task_callback(self, task_result):
        sorting_info, file_info = task_result
        tempo_bin = sorting_info[0]
        filepath, filename = file_info
        relpath = filepath.relative_to(self.input_dir)
        logging.info(f"Analyzed: {filepath} -> {tempo_bin}")
        output_path = self.output_dir / tempo_bin / relpath
        output_dir = output_path.parent

        if output_path.exists():
            logging.warning(f"Skip: {output_path} already exists.")
            return

        output_dir.mkdir(parents=True, exist_ok=True)

        if self.should_copy_files:
            shutil.copy2(filepath, output_path)
            logging.info(f"Copied: {filepath} -> {output_path}")
        else:
            output_path.symlink_to(filepath)
            logging.info(f"Linked: {filepath} -> {output_path}")