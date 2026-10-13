from abc import ABC
from abc import abstractmethod


class EventSkeleton(ABC):
    @abstractmethod
    def read(self):
        """Reads the incoming file and returns data in standard format"""
        pass
