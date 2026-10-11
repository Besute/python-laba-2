from .csv_event import CsvEvent
from .jsonl_event import JsonlEvent


class EventService:
    analyzed_data = None

    def __init__(self, data):
        self.paths = data["path"]
        self.type = data["type"]
        self.skipInvalid = data["skipInvalid"]
        self._handlers = {
            "csv": self.process_csv,
            "jsonl": self.process_jsonl,
        }

    def create_event(self):
        handler = self._handlers.get(self.type)
        if handler is None:
            raise TypeError("Invalid event type")

        return handler(self.paths, self.skipInvalid)

    def process_csv(self, paths, skip_invalid=False):
        event = CsvEvent(paths, skip_invalid)
        self.analyzed_data = event.analyze()

    def process_jsonl(self, paths, skip_invalid=False):
        event = JsonlEvent(paths, skip_invalid)
        self.analyzed_data = event.analyze()
