from concurrent.futures import ThreadPoolExecutor
import multiprocessing
from queue import Empty
import logging
from mtap.config import MTAPConfig

# Set up logging
logger = logging.getLogger("MTAP")

class Worker:
    """
    Represents a worker process that handles tasks.
    """
    def __init__(self):
        self.process = None
        self.task_queue = multiprocessing.Queue()
        self.current_task = None
        self.is_compute_task = False

    def start(self):
        """
        Starts the worker process.
        """
        self.process = multiprocessing.Process(target=self.run)
        self.process.start()

    def run(self):
        """
        Main loop for the worker process to execute tasks.
        """
        executor = ThreadPoolExecutor(max_workers=MTAPConfig.get_max_network_threads())

        while True:
            try:
                func, args, kwargs, is_compute = self.task_queue.get(timeout=3)
                self.is_compute_task = is_compute
                self.current_task = func
                future = executor.submit(func, *args, **kwargs)
                future.result()  # Wait for the task to complete
            except Empty:
                continue
            except Exception as e:
                logger.error(f"Error executing task: {e}")
            finally:
                self.current_task = None
                self.is_compute_task = False

    def add_task(self, func, args=(), kwargs=None, is_compute=False):
        """
        Adds a task to the worker's queue.
        """
        if kwargs is None:
            kwargs = {}
        self.task_queue.put((func, args, kwargs, is_compute))
