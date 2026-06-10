import os
import shutil
import logging
import asyncio
import sortbykey.analyzers as analyzer 
import sortbykey.trackannotate.encoder as encoder
from sortbykey import fs
from sortbykey.workmanager import Worker
from sortbykey.wheel import WheelOfFifths

class Sorter(Worker):

    def __init__(self, input_dir, output_dir, *, atonality=0.5, copy_files=False):
        # Establish input/output
        self.__input_dir = input_dir
        self.__output_dir = output_dir
        self.should_copy_files = copy_files
        self.atonality_confidence_limit = atonality
        # Setup cache
        # self.__cache = HashDB(self.output_dir)
        # logging.info("Updating cache...")
        # self.__cache.initialize_table()
        # self.__cache.update()
        # logging.info("Cache updated.")

    @property
    def input_dir(self):
        return self.__input_dir
    
    @property
    def output_dir(self):
        return self.__output_dir

    def generate_priority_queue_entries(self):
        for root, filename in fs.traverse(self.input_dir, filetype_filter=analyzer.SUPPORTED_READ_FILETYPES):
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
        # Try to get existing key
        camelot_key = encoder.get_key_metadata(filepath)
        # If key not found, analyze and encode
        if not camelot_key:
            key, scale, strength = analyzer.analyze_key(filepath)
            camelot_key = "atonal" if strength <= self.atonality_confidence_limit else WheelOfFifths.camelot_notation(key, scale)
            encoder.write_aiff_metadata(filepath, key=None if camelot_key == "atonal" else camelot_key)
        return (camelot_key,), (filepath, filename)     

    def task_callback(self, task_result):
        sorting_info, file_info = task_result
        camelot_key = sorting_info[0]
        filepath, filename = file_info
        relpath = filepath.relative_to(self.input_dir)
        logging.info(f"Analyzed: {filepath} -> {camelot_key}")
        output_path = self.output_dir / camelot_key / relpath
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
    
    def close(self):
        # self.__cache.close()
        pass
    
    def __del__(self):
        self.close()