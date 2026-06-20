import asyncio
import logging
import os
import shutil
from abc import ABC, abstractmethod
from concurrent.futures import ProcessPoolExecutor
from typing import Tuple, Any, Generator, Dict
from traceback import print_tb, print_exception

class Worker(ABC):

    async def run_in_pool(self, executor: ProcessPoolExecutor, *task_args, **task_kwargs) -> Tuple:
        '''
        Use the priority queue to perform some task with some arguments.

        :param executor: The process executor.
        :return: The result of the task, and the result of the callback after the task.
        '''
        loop = asyncio.get_running_loop()
        task_result = await loop.run_in_executor(executor, self.perform_task, *task_args, **task_kwargs)
        after_task_result = self.task_callback(task_result)
        return (task_result, after_task_result)


    @abstractmethod
    def perform_task(self, *task_args, **task_kwargs) -> Any:
        '''
        This task will be performed in a pool.

        :return: Whatever your task should return.
        :rtype: Any
        '''
        raise NotImplementedError

    # Not @abstractmethod, but yes pass, as it should be optional to implement.
    def task_callback(self, task_result: Tuple[Any, ...]) -> Any:
        '''
        This function will run after a task has been done. Note that it is not
        concurrent, unlike perform_task.

        :param task_result: The result of the task, as a tuple.
        :type task_result: Tuple
        :return: The result of the callback.
        :rtype: Any
        '''
        pass
    
    def create_priority_queue(self, *args, **kwargs) -> asyncio.PriorityQueue:
        '''
        Create a priority queue through some method.
        Args and kwargs will be passed to generate_priority_queue_entries.

        :return: A priority queue.
        :rtype: asyncio.PriorityQueue
        '''
        logging.info("Creating priority queue...")
        queue = asyncio.PriorityQueue()
        for entry in self.generate_priority_queue_entries(*args, **kwargs):
            queue.put_nowait(entry)
        logging.info("Finished priority queue.")
        return queue
    
    @abstractmethod
    def generate_priority_queue_entries(self, *args, **kwargs) -> Generator[tuple[int, tuple[tuple[Any, ...], Dict[Any, Any]]], None, None]:
        '''
        Generate priority queue entries, one at a time.
        Entries in the queue should be a tuple of format (priority, (args: tuple, kwargs: dict)).
        '''
        raise NotImplementedError

    def __call__(self, executor, *args, **kwargs):
        return self.run_in_pool(executor, *args, **kwargs)

    async def __work(self, queue: asyncio.PriorityQueue, executor: ProcessPoolExecutor):
        while True:
            try:
                priority, data = await queue.get()
                task_args, task_kwargs = data
            except Exception as e:
                logging.error(f"Error retrieving from queue: {e}")
                continue
            try:
                await self.run_in_pool(executor, *task_args, **task_kwargs)
            except Exception as e:
                logging.error(f"Error processing {data}. See below for details:")
                print_exception(e)
                print_tb(e.__traceback__)
            finally:
                queue.task_done()

    async def start_work(self, num_workers: int):

        queue = self.create_priority_queue()
        
        with ProcessPoolExecutor() as executor:
            tasks = [asyncio.create_task(self.__work(queue, executor)) for _ in range(num_workers)]
            
            await queue.join() # Wait until all items are processed
            
            for t in tasks:
                t.cancel() # Stop the workers

            await asyncio.gather(*tasks, return_exceptions=True)