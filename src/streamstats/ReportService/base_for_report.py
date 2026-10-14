from abc import ABC
from abc import abstractmethod


class ReportSkeleton(ABC):
    @abstractmethod
    def create_file(self):
        """create unexisting file and parent directories"""
        pass

    @abstractmethod
    def write_output_file(self):
        """writes all data into created one"""
        pass
