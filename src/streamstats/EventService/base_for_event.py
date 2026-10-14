from abc import ABC
from abc import abstractmethod
from abc import abstractproperty

from streamstats.MemoryCounter.memory_count import CreateVirtualMemory


class EventSkeleton(ABC, CreateVirtualMemory):
    BIG_FILE_SIZE = 500 * 1024 * 1024
    PERIOD_OF_DISPLAY = 100_000

    @abstractmethod
    def read(self):
        """
        Reads the incoming file and returns data in standard format and list of boolean which means
        which file's weight at least 500MB, and if it is, display memory from CreateVirtualMemory
        """
        pass

    @abstractproperty
    def big_data(self):
        """Returns array of boolean that means which file's weight is at least 500MB"""
        pass
