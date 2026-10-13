from streamstats.Parsers.json_parser import BasicJsonParser

from .base_for_event import EventSkeleton


class JsonlEvent(BasicJsonParser, EventSkeleton):

    def __init__(self, paths, bool_skip_invalid):
        self._paths = paths
        self._bool_skip_invalid = bool_skip_invalid

    def read(self):
        final_data = []
        for path in self._paths:
            with open(path) as jsonfile:
                line = jsonfile.readline()
                data_of_file = []
                while line:
                    line = self.from_json(line)
                    data_of_file.append(line)
                    line = jsonfile.readline()
                final_data.append(data_of_file)
        data_to_go = final_data
        return data_to_go
