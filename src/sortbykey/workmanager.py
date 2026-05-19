import asyncio
import logging
import os
import shutil
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from typing import Tuple

class Worker(ABC):

    @abstractmethod
    async def perform_task(self, executor, arguments: Tuple):
        '''
        Perform some task with some arguments

        :param arguments: A tuple of arguments to maybe do some task with.
        :type arguments: tuple
        '''
        pass
    
    @abstractmethod
    def create_priority_queue(self) -> asyncio.PriorityQueue:
        '''
        Create a priority queue through some method.

        :return: A priority queue.
        :rtype: asyncio.PriorityQueue
        '''
        pass

async def work(queue, executor, worker: Worker):
    while True:
        try:
            priority, arguments = await queue.get()
        except Exception as e:
            logging.error(f"Error retrieving from queue: {e}")
            continue

        try:
            await worker.perform_task(executor, arguments)
        except Exception as e:
            logging.error(f"Error processing {arguments}: {e}")
        finally:
            queue.task_done()

async def start_work(worker: Worker, num_workers):

    queue = worker.create_priority_queue()
    
    with ProcessPoolExecutor() as executor:
        tasks = [asyncio.create_task(work(queue, executor, worker)) for _ in range(num_workers)]
        
        await queue.join() # Wait until all items are processed
        
        for t in tasks:
            t.cancel() # Stop the workers

        await asyncio.gather(*tasks, return_exceptions=True)