class LoadBalancerBase:
    """
    Abstract base class for load balancers.
    """
    def __init__(self, workers):
        self.workers = workers

    def select_worker(self, is_compute):
        """
        Abstract method to select a worker based on task type.
        Should be implemented by subclasses.
        """
        raise NotImplementedError("This method should be implemented by subclasses.")