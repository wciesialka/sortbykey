import asyncio
from concurrent.futures import ProcessPoolExecutor
from sortbykey import analyzer 
from sortbykey import fs

async def worker(queue, executor):
    while True:
        priority, file_path = await queue.get()

        try:
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(executor, analyzer.analyze, file_path)
            key, scale, strength = result
            print(key, scale, strength)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
        finally:
            queue.task_done()

async def start_work(input_dir, output_dir, num_workers):
    queue = asyncio.PriorityQueue()

    for root, filename in fs.traverse(input_dir):
        filepath = root / filename
        size = filepath.stat().st_size
        await queue.put((size, path))

    # Create a ProcessPool equal to number of CPU cores
    
    with ProcessPoolExecutor() as executor:
        # Start 4 concurrent workers
        tasks = [asyncio.create_task(worker(queue, executor)) for _ in range(num_workers)]
        
        await queue.join() # Wait until all items are processed
        
        for t in tasks:
            t.cancel() # Stop the workers

if __name__ == "__main__":
    main()