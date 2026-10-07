from .csv_event import CsvEvent
from .jsonl_event import JsonlEvent


class EventService(CsvEvent, JsonlEvent):
    def __init__(self, data):
        self.path = data["path"]
        self.type = data["type"]
        self.output = data["output"]
        self.skipInvalid = data["skipInvalid"]
        self.data = self.__read()

    def __read(self):
        if self.type == "csv":
            return self.read_csv(self.path)
        elif self.type == "jsonl":
            return self.read_jsonl(self.path)
        return None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value
