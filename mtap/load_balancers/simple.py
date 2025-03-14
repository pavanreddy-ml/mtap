from mtap.load_balancers import LoadBalancerBase

class SimpleLoadBalancer(LoadBalancerBase):
    """
    A simple load balancer implementation.
    """
    def select_worker(self, is_compute):
        if is_compute:
            # Only consider workers not currently handling compute-bound tasks
            available_workers = [worker for worker in self.workers if not worker.is_compute_task]
        else:
            available_workers = self.workers

        if not available_workers:
            return None

        # Select the worker with the least number of tasks in the queue
        least_loaded_worker = min(available_workers, key=lambda w: w.task_queue.qsize())
        return least_loaded_worker