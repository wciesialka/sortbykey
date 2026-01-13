import asyncio
import logging
import os
from concurrent.futures import ProcessPoolExecutor
from sortbykey import analyzer 
from sortbykey import fs

async def worker(queue, executor):
    while True:
        priority, fileinfo = await queue.get()
        filepath, filename, input_dir, output_dir = fileinfo
        relpath = filepath.relative_to(input_dir)

        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(executor, analyzer.analyze, filepath)
            key, scale, strength = result
            if strength < 0.5:
                camelot_key = "atonal"
            else:
                camelot_key = analyzer.camelot(key, scale)
            # logging.info(f"Analyzed: {filepath} -> {camelot_key}")
            output_path = output_dir / camelot_key / relpath
            output_dir = output_path.parent
            # os.makedirs(output_dir, exist_ok=True)
            # os.rename(filepath, output_path)
            # logging.info(f"Moved: {filepath} -> {output_path}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
        finally:
            queue.task_done()

async def start_work(input_dir, output_dir, num_workers):
    queue = asyncio.PriorityQueue()

    for root, filename in fs.traverse(input_dir):
        filepath = root / filename
        size = filepath.stat().st_size
        await queue.put((size, (filepath, filename, input_dir, output_dir)))

    with ProcessPoolExecutor() as executor:
        tasks = [asyncio.create_task(worker(queue, executor)) for _ in range(num_workers)]
        
        await queue.join() # Wait until all items are processed
        
        for t in tasks:
            t.cancel() # Stop the workers