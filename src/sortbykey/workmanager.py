import asyncio
import logging
import os
import shutil
from concurrent.futures import ProcessPoolExecutor
from sortbykey import analyzer 
from sortbykey import fs
from sortbykey.cache import HashDB

async def worker(queue, executor, copy_files=False):
    while True:
        priority, fileinfo = await queue.get()
        filepath, filename, input_dir, output_dir = fileinfo
        relpath = filepath.relative_to(input_dir)
        logging.info("Analyzing %s...", relpath)

        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(executor, analyzer.analyze, filepath)
            key, scale, strength = result
            camelot_key = "atonal" if strength < 0.5 else analyzer.camelot(key, scale)
            logging.info(f"Analyzed: {filepath} -> {camelot_key}")
            output_path = output_dir / camelot_key / relpath
            output_dir = output_path.parent

            if output_path.exists():
                logging.warning(f"Skip: {output_path} already exists.")
                continue

            output_dir.mkdir(parents=True, exist_ok=True)

            if copy_files:
                # Use run_in_executor for I/O bound tasks to avoid blocking the loop
                await loop.run_in_executor(executor, shutil.copy2, filepath, output_path)
                logging.info(f"Copied: {filepath} -> {output_path}")
            else:
                os.rename(filepath, output_path)
                logging.info(f"Moved: {filepath} -> {output_path}")
        except Exception as e:
            logging.error(f"Error processing {filepath}: {e}")
        finally:
            queue.task_done()

async def start_work(input_dir, output_dir, num_workers, copy):
    
    queue = asyncio.PriorityQueue()

    cache_db = HashDB(output_dir)
    logging.info("Updating cache...")
    cache_db.initialize_table()
    cache_db.update()
    logging.info("Cache updated. Starting analyzation...")

    for root, filename in fs.traverse(input_dir):
        filepath = root / filename
        # Check if file exists in database
        db_file = cache_db.lookup_file_by_hash(filepath)
        # If hash doesn't exist in database, copy file over!
        if db_file is None:
            size = filepath.stat().st_size
            logging.info("Enqueueing %s...", filepath)
            await queue.put((size, (filepath, filename, input_dir, output_dir)))
            continue
        logging.info("File %s exists as %s (hash=%s). Skipping...", filepath, db_file[0], db_file[1].hex())

    with ProcessPoolExecutor() as executor:
        tasks = [asyncio.create_task(worker(queue, executor, copy_files=copy)) for _ in range(num_workers)]
        
        await queue.join() # Wait until all items are processed
        
        for t in tasks:
            t.cancel() # Stop the workers
    cache_db.close()