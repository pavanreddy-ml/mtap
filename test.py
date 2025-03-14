import multiprocessing
from mtap.executor import MTAP

multiprocessing.set_start_method('spawn', force=True)

def download_file(url):
    import time
    time.sleep(1)  # Simulating a network operation
    print(f"Downloaded file from {url}")

def perform_heavy_computation(data):
    result = sum(i ** 2 for i in data)c
    print(f"Computation result: {result}")

if __name__ == "__main__":
    mtap_instance = MTAP()

    # Directly pass functions and arguments to MTAP
    for i in range(10):
        mtap_instance.network(download_file, "http://example.com/file1")
        mtap_instance.network(download_file, "http://example.com/file2")
        mtap_instance.compute(perform_heavy_computation, range(100000000))
        mtap_instance.compute(perform_heavy_computation, range(200000000))
