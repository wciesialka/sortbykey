import os
import shutil
import logging
import asyncio
from sortbykey.cache import HashDB
from sortbykey import analyzer 
from sortbykey import fs
from sortbykey.workmanager import Worker

class Sorter(Worker):

    def __init__(self, input_dir, output_dir, *, copy_files=False):
        # Establish input/output
        self.__input_dir = input_dir
        self.__output_dir = output_dir
        # Setup cache
        self.__cache = HashDB(self.output_dir)
        logging.info("Updating cache...")
        self.__cache.initialize_table()
        self.__cache.update()
        logging.info("Cache updated.")

    @property
    def input_dir(self):
        return self.__input_dir
    
    @property
    def output_dir(self):
        return self.__output_dir
    
    def create_priority_queue(self) -> asyncio.PriorityQueue:
        logging.info("Creating priority queue...")
        queue = asyncio.PriorityQueue()

        for root, filename in fs.traverse(self.input_dir, filetype_filter=analyzer.SUPPORTED_FILETYPES):
            filepath = root / filename
            # Check if file exists in database
            db_file = self.__cache.lookup_file_by_hash(filepath)
            # If hash doesn't exist in database, copy file over!
            if db_file is None:
                size = filepath.stat().st_size
                queue.put_nowait((size, (filepath, filename)))
                continue
            logging.info("File %s exists as %s (hash=%s). Skipping...", filepath, db_file[0], db_file[1].hex())
        logging.info("Finished priority queue.")
        return queue
    
    async def perform_task(self, executor, fileinfo):
        filepath, filename = fileinfo
        relpath = filepath.relative_to(self.input_dir)
        logging.info("Analyzing %s...", relpath)
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(executor, analyzer.analyze, filepath)
        key, scale, strength = result
        camelot_key = "atonal" if strength < 0.5 else analyzer.camelot(key, scale)
        logging.info(f"Analyzed: {filepath} -> {camelot_key}")
        output_path = self.output_dir / camelot_key / relpath
        output_dir = output_path.parent

        if output_path.exists():
            logging.warning(f"Skip: {output_path} already exists.")
            return

        output_dir.mkdir(parents=True, exist_ok=True)

        if copy_files:
            # Use run_in_executor for I/O bound tasks to avoid blocking the loop
            await loop.run_in_executor(executor, shutil.copy2, filepath, output_path)
            logging.info(f"Copied: {filepath} -> {output_path}")
        else:
            os.rename(filepath, output_path)
            logging.info(f"Moved: {filepath} -> {output_path}")
    
    def close(self):
        self.__cache.close()
    
    def __del__(self):
        self.close()