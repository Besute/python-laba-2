from .csv_event import CsvEvent
from .jsonl_event import JsonlEvent


class EventService:
    def __init__(self, data):
        self.paths = data["path"]
        self.type = data["type"]
        self.output = data["output"]
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

    @classmethod
    def process_csv(cls, paths, skip_invalid=False):
        event = CsvEvent(paths, skip_invalid)
        return event.analyze()

    @classmethod
    def process_jsonl(cls, paths, skip_invalid=False):
        event = JsonlEvent(paths, skip_invalid)
        return event.analyze()
