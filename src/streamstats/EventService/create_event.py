from streamstats.Errors.errors import InvalidMethodError
from streamstats.Parsers.parser import EVENTS

from ..AnalyzeService.analysis import Analyzator


class EventService:

    def __init__(self, data):
        self.paths = data["path"]
        self.type = data["type"]
        self.skipInvalid = data["skipInvalid"]
        self.data_good_format, self.__bool_big_data = self.create_event()

    def analyze(self, data):
        return Analyzator(self.skipInvalid, self.__bool_big_data).analyze(data)

    def create_event(self):
        handler = EVENTS.get(self.type)
        if handler is None:
            raise InvalidMethodError("Invalid event type")

        return handler(self.paths, self.skipInvalid)
