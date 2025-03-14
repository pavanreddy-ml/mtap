import psutil
import sys
import math
import platform

import logging


logger = logging.getLogger("MTAPConfig")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class MTAPConfig:
    __num_processes = max(1, math.floor(psutil.cpu_count(logical=False) * 0.75))
    __max_network_threads = 5
    __max_compute_threads = 1

    @classmethod
    def set_num_processes(cls, num, force=False):
        total_physical_cores = psutil.cpu_count(logical=False)

        os_type = platform.system()
        if os_type == 'Linux':
            reserved_cores = 1
        elif os_type == 'Windows':
            reserved_cores = 2
        else:
            reserved_cores = 2

        min_cores_available = max(1, total_physical_cores - reserved_cores)

        if num > total_physical_cores:
            logger.critical(
                f"Attempt to set num_processes to {num} exceeds the number of available physical CPU cores ({total_physical_cores}). "
                "Please update the source code in config.py if this behavior is intended."
            )
            sys.exit(1)

        if num > min_cores_available and not force:
            logger.critical(
                f"Setting num_processes to {num} is not permitted as it requires more than the available CPU cores ({min_cores_available}) "
                f"after reserving {reserved_cores} core(s) for the operating system. "
                "To override this restriction, set the force parameter to True."
            )
            sys.exit(1)
        else:
            cls.__num_processes = num
            logger.info(f"Number of processes successfully set to {cls.__num_processes}.")

    @classmethod
    def get_num_processes(cls):
        return cls.__num_processes

    @classmethod
    def get_max_network_threads(cls):
        return cls.__max_network_threads
    
    @classmethod
    def get_max_compute_threads(cls):
        return cls.__max_compute_threads