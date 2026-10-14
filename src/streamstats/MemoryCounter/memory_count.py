import os

import psutil


class CreateVirtualMemory:
    def __init__(self):
        self._mem = psutil.virtual_memory()

    @property
    def mem(self):
        return self._mem

    @property
    def memory(self):
        process = psutil.Process(os.getpid())
        memory = process.memory_full_info()
        return memory.rss / 1024 / 1024
