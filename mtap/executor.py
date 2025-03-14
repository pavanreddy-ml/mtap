import multiprocessing
from mtap.worker import Worker
from mtap.load_balancers import SimpleLoadBalancer
from mtap.config import MTAPConfig
from functools import wraps
import logging

# Set up logging
logger = logging.getLogger("MTAP")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class MTAP:
    """
    Manages multiple worker processes and assigns tasks to them using a load balancer.
    """
    def __init__(self, load_balancer_class=SimpleLoadBalancer):
        self.num_processes = MTAPConfig.get_num_processes()
        self.workers = [Worker() for _ in range(self.num_processes)]

        for worker in self.workers:
            worker.start()

        # Instantiate the load balancer
        self.load_balancer = load_balancer_class(self.workers)

    def network(self, func, *args, **kwargs):
        """
        Directly assigns a function as a network/IO bound operation.
        """
        worker = self.load_balancer.select_worker(is_compute=False)
        if worker:
            logger.info(f"Assigning network task {func.__name__} to process {worker.process.pid}")
            worker.add_task(func, args, kwargs, is_compute=False)
        else:
            logger.warning(f"No available worker for network task {func.__name__}")

    def compute(self, func, *args, **kwargs):
        """
        Directly assigns a function as a compute-bound operation.
        """
        worker = self.load_balancer.select_worker(is_compute=True)
        if worker:
            logger.info(f"Assigning compute task {func.__name__} to process {worker.process.pid}")
            worker.add_task(func, args, kwargs, is_compute=True)
        else:
            logger.warning(f"No available worker for compute task {func.__name__}")