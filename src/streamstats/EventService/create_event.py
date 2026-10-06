from .csv_event import CsvEvent


class EventService(CsvEvent):
    def __init__(self, data):
        self.path = data["path"]
        self.type = data["type"]
        self.output = data["output"]
        self.skipInvalid = data["skipInvalid"]
        print(self.path)
        self.read_csv(self.path)
