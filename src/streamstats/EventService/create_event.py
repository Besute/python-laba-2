from streamstats.Errors.errors import InvalidMethodError
from streamstats.Parsers.parser import CURRENT_EVENTS

from .csv_event import CsvEvent
from .jsonl_event import JsonlEvent


class EventService:
    analyzed_data = None

    def __init__(self, data):
        self.paths = data["path"]
        self.type = data["type"]
        self.skipInvalid = data["skipInvalid"]

    def create_event(self):
        handler = CURRENT_EVENTS.get(self.type)
        if handler is None:
            raise InvalidMethodError("Invalid event type")

        return handler(self.paths, self.skipInvalid)

    @classmethod
    def process_csv(cls, paths, skip_invalid=False):
        event = CsvEvent(paths, skip_invalid)
        return event.analyze()

    @classmethod
    def process_jsonl(cls, paths, skip_invalid=False):
        event = JsonlEvent(paths, skip_invalid)
        return event.analyze()
