import time
import psutil
import os
import json


class PerformanceLogger:
    def __init__(self, filename="performance_log.json"):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, mode='w') as file:
                json.dump([], file, indent=4)

    def log(self, algorithm_name, start_time):
        elapsed_time = time.time() - start_time
        process = psutil.Process(os.getpid())
        ram_usage = process.memory_info().rss / (1024 * 1024)  # MB
        disk_usage = psutil.disk_usage('.').used / (1024 ** 3)  # GB

        log_entry = {
            "Algorithm": algorithm_name,
            "Elapsed Time (s)": round(elapsed_time, 6),
            "RAM Used (MB)": round(ram_usage, 2),
            "ROM Used (GB)": round(disk_usage, 2)
        }

        try:
            with open(self.filename, mode='r') as file:
                data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            data = []

        data.append(log_entry)

        with open(self.filename, mode='w') as file:
            json.dump(data, file, indent=4)
